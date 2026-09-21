"""In-memory and explicit file workflows using the same accounting kernel."""

from __future__ import annotations

import copy
import hashlib
import json
from importlib.metadata import version
from importlib.resources import files
from pathlib import Path
from typing import Mapping, cast

from ._engine.excel_io import write_output
from ._engine.pipeline import compute
from ._engine.validation import ValidationRejected, load_and_validate
from ._resources import configuration, verify_resources
from .data import get_policy, validate_dataset
from .models import (
    AccountingError,
    AnalysisResult,
    Dataset,
    JSONValue,
    ResourceError,
    Table,
    ValidationError,
)

__all__ = [
    "run_dataset",
    "export_results",
    "get_metrics",
    "get_table",
    "get_controls",
    "get_lineage",
]


def _hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(
            value, sort_keys=True, ensure_ascii=False, allow_nan=False, separators=(",", ":")
        ).encode()
    ).hexdigest()


def _code_hash() -> str:
    root = files("financial_accounting_engine")
    h = hashlib.sha256()

    def visit(folder: object, prefix: str) -> None:
        # Traversable is structural; runtime package data remains read-only.
        from importlib.abc import Traversable

        for child in sorted(cast(Traversable, folder).iterdir(), key=lambda p: p.name):
            if child.is_dir() and child.name not in {"resources", "__pycache__"}:
                visit(child, prefix + child.name + "/")
            elif child.name.endswith(".py"):
                h.update((prefix + child.name).encode())
                h.update(child.read_bytes())

    visit(root, "")
    return h.hexdigest()


def run_dataset(
    dataset: Dataset | str | Path, policy: Mapping[str, JSONValue] | None = None
) -> AnalysisResult:
    """Validate and compute an in-memory dataset or a directory of 19 input workbooks.

    No files are written. Explicit export_results writes a new user directory.
    Returns AnalysisResult with reference status, named tables and input/code/policy
    fingerprints. Rejection raises ValidationError or AccountingError, never an
    approved partial result. The policy date and run-control dates must agree.
    """
    p = dict(get_policy() if policy is None else policy)
    required = (
        "reporting_date",
        "knowledge_time",
        "policy_id",
        "source_rule_set",
        "presentation_currency",
    )
    for key in required:
        if key not in p:
            raise AccountingError(f"Missing policy field: {key}")
    verify_resources()
    try:
        if isinstance(dataset, (str, Path)):
            original, _ = load_and_validate(
                Path(dataset), str(p["reporting_date"]), str(p["knowledge_time"])
            )
        else:
            original = {k: [dict(r) for r in rows] for k, rows in dataset.items()}
        tables = validate_dataset(original, str(p["reporting_date"]), str(p["knowledge_time"]))
    except ValidationRejected as exc:
        raise ValidationError(exc.issues) from exc
    except (ValueError, KeyError, TypeError) as exc:
        if isinstance(exc, AccountingError):
            raise
        raise AccountingError(str(exc)) from exc
    rc = tables["run_control"][0]
    for key, expected in [
        ("reporting_date", p["reporting_date"]),
        ("knowledge_time", p["knowledge_time"]),
        ("policy_id", p["policy_id"]),
        ("rule_set_id", p["source_rule_set"]),
    ]:
        if rc[key] != expected:
            raise AccountingError(f"Run control and policy differ: {key}")
    for parameter in tables["parameters"]:
        key = str(parameter["parameter_id"])
        if (
            parameter["policy_id"] != p["policy_id"]
            or parameter["rule_set_id"] != p["source_rule_set"]
        ):
            raise AccountingError("Parameter policy/rule IDs differ from run")
        if key in p:
            supplied = str(parameter["parameter_value"])
            chosen = p[key]
            if isinstance(chosen, (int, float)) and not isinstance(chosen, bool):
                try:
                    matches = float(supplied) == float(chosen)
                except ValueError:
                    matches = False
            else:
                matches = supplied == str(chosen)
            if not matches:
                raise AccountingError(f"Input parameter conflicts with policy: {key}")
    rules = configuration("rules", str(p["source_rule_set"]), "rule_set_id")
    lineage: dict[str, JSONValue] = {
        "input_hash": _hash(tables),
        "policy_hash": _hash(p),
        "rule_hash": _hash(rules),
        "code_hash": _code_hash(),
        "resource_hash": _hash(verify_resources()),
        "engine_version": version("financial-instruments-accounting"),
        "contract_version": "1.1.0",
        "policy_id": p["policy_id"],
        "rule_set_id": p["source_rule_set"],
        "as_of_date": p["reporting_date"],
        "knowledge_time": p["knowledge_time"],
        "official": False,
    }
    run_id = "FAE-" + _hash(lineage)[:20]
    lineage["run_id"] = run_id
    try:
        groups, metrics, status = compute(tables, p, rules, run_id, [])
    except (ValueError, KeyError, TypeError, ArithmeticError) as exc:
        raise AccountingError(str(exc)) from exc
    flattened = {
        f"{book}/{sheet}": rows for book, sheets in groups.items() for sheet, rows in sheets.items()
    }
    return AnalysisResult(
        cast(Mapping[str, Table], flattened),
        cast(Mapping[str, JSONValue], metrics),
        lineage,
        status,
    )


def get_metrics(result: AnalysisResult) -> dict[str, JSONValue]:
    """Independent copy of money totals and classification/stage/hedge distributions."""
    return copy.deepcopy(dict(result.metrics))


def get_table(result: AnalysisResult, name: str) -> Table:
    """Copy table by workbook/sheet key or unique sheet name; ambiguity is rejected."""
    if name in result.tables:
        return copy.deepcopy(result.tables[name])
    matches = [v for k, v in result.tables.items() if k.split("/")[-1] == name]
    if len(matches) != 1:
        raise AccountingError(f"Unknown or ambiguous result table: {name}")
    return copy.deepcopy(matches[0])


def get_controls(result: AnalysisResult) -> Table:
    """Expected/actual/tolerance/status audit controls from the summary workbook."""
    return get_table(result, "00_Summary/CONTROLS")


def get_lineage(result: AnalysisResult) -> dict[str, JSONValue]:
    """Independent copy of code/input/resource/policy fingerprints and historical cutoffs."""
    return copy.deepcopy(dict(result.lineage))


def export_results(result: AnalysisResult, destination: str | Path) -> Path:
    """Write seven XLSX outputs, neutral JSON and a SHA256 manifest into a new directory.

    Existing targets are rejected. JSON is authoritative for typed values; Excel
    formula-like text is escaped. Does not upload, post journals or mutate inputs.
    """
    target = Path(destination).resolve()
    if target.exists():
        raise ResourceError(f"Destination already exists: {target}")
    target.mkdir(parents=True)
    groups: dict[str, dict[str, Table]] = {}
    for key, values in result.tables.items():
        book, sheet = key.split("/", 1)
        groups.setdefault(book, {})[sheet] = values
    for book, sheets in groups.items():
        write_output(
            target / f"FAE_OUT_{book}.xlsx",
            {k: [dict(r) for r in rows] for k, rows in sheets.items()},
            dict(result.lineage),
        )
    payload = dict(
        tables=result.tables,
        metrics=result.metrics,
        lineage=result.lineage,
        status=result.status,
        official=False,
    )
    (target / "results.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8"
    )
    manifest = {
        "status": result.status,
        "official": False,
        "lineage": dict(result.lineage),
        "files": {
            p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(target.iterdir())
        },
    }
    (target / "run_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return target
