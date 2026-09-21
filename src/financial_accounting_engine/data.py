"""Offline reference data, policy, schema and bitemporal validation API."""

from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
from typing import cast

from ._checks import number, row
from ._engine.contracts import WORKBOOKS
from ._engine.validation import ValidationRejected, select_official_snapshot, validate_tables
from ._resources import configuration, read_bytes, read_json, verify_resources
from .models import AccountingError, Dataset, JSONValue, ResourceError, Row, ValidationError

__all__ = [
    "get_schema",
    "get_parameters",
    "get_policy",
    "get_formula",
    "get_sources",
    "validate_dataset",
    "select_snapshot",
    "list_profiles",
    "export_profile",
    "load_reference_data",
]
DEFAULT_POLICY = "EU_FINANCIAL_INSTRUMENTS_2026_V1"
DEFAULT_RULES = "FIA_RULES_2026_V1"


def get_policy(policy_id: str = DEFAULT_POLICY) -> dict[str, JSONValue]:
    """Return an independent copy of an explicitly versioned accounting policy."""
    return configuration("accounting", policy_id, "policy_id")


def get_parameters(policy_id: str = DEFAULT_POLICY) -> dict[str, JSONValue]:
    """Policy parameters with units/conventions identified by the schema and policy keys."""
    return get_policy(policy_id)


def get_schema(table: str | None = None) -> dict[str, JSONValue]:
    """Canonical 1.1.0 input columns/dictionaries; unknown table raises ResourceError."""
    schema = read_json("schema.json")
    if table is None:
        return schema
    if table not in schema:
        raise ResourceError(f"Unknown input table: {table}")
    return cast(dict[str, JSONValue], schema[table])


def get_formula(formula_id: str, rule_set_id: str = DEFAULT_RULES) -> dict[str, JSONValue]:
    """Return one versioned registry entry containing its ID, version and public name.

    Source references are attached to calculation/decision results and the rule
    registry.  The formula implementation and its assumptions are documented on
    the corresponding API page; the registry deliberately does not duplicate a
    free-text expression that could drift from executable code.
    """
    rules = configuration("rules", rule_set_id, "rule_set_id")
    for item in cast(list[dict[str, JSONValue]], rules["formulas"]):
        if item["id"] == formula_id:
            return item
    raise ResourceError(f"Unknown formula: {formula_id}")


def get_sources() -> list[dict[str, JSONValue]]:
    """Official source metadata only; never downloads or redistributes standard texts."""
    return cast(list[dict[str, JSONValue]], read_json("sources.json")["sources"])


def list_profiles() -> tuple[str, ...]:
    """Stable identifiers of the two complete synthetic 1.0.0 reference profiles."""
    return ("MID_SIZE_UNIVERSAL_FIA", "SMALL_SA_RETAIL_FIA")


def load_reference_data(profile_id: str) -> dict[str, list[Row]]:
    """Load independent in-memory canonical tables; no files are written."""
    if profile_id not in list_profiles():
        raise ResourceError(f"Unknown profile: {profile_id}")
    verify_resources()
    return cast(dict[str, list[Row]], read_json(profile_id + ".json"))


def export_profile(profile_id: str, destination: str | Path) -> Path:
    """Copy 19 sealed XLSX inputs and their original manifest into a new directory.

    Existing destinations are rejected; the package resources are never modified.
    Returned path is absolute. All copied bytes match their resource hashes.
    """
    if profile_id not in list_profiles():
        raise ResourceError(f"Unknown profile: {profile_id}")
    verify_resources()
    target = Path(destination).resolve()
    if target.exists():
        raise ResourceError(f"Export destination already exists: {target}")
    target.mkdir(parents=True)
    for name in (*WORKBOOKS, "profile_manifest.json"):
        (target / name).write_bytes(read_bytes(f"profiles/{profile_id}/1.0.0/{name}"))
    return target


def select_snapshot(
    tables: Dataset, reporting_date: str, knowledge_time: str
) -> dict[str, list[Row]]:
    """Select exactly one ACTIVE official version per business key at both cutoffs.

    Valid and known intervals are inclusive. Date is ISO YYYY-MM-DD; knowledge
    timestamp must include UTC offset. Missing or overlapping versions reject.
    Input record official flags do not grant official status to library results.
    """
    try:
        date.fromisoformat(reporting_date)
        if datetime.fromisoformat(knowledge_time.replace("Z", "+00:00")).tzinfo is None:
            raise AccountingError("knowledge_time requires an explicit timezone")
        values, issues = select_official_snapshot(
            {k: [dict(r) for r in rows] for k, rows in tables.items()},
            reporting_date,
            knowledge_time,
        )
    except (ValueError, TypeError) as exc:
        raise AccountingError(str(exc)) from exc
    if issues:
        raise ValidationError(issues)
    return cast(dict[str, list[Row]], values)


def validate_dataset(
    tables: Dataset, reporting_date: str | None = None, knowledge_time: str | None = None
) -> dict[str, list[Row]]:
    """Validate complete in-memory contract; return the selected independent snapshot.

    Missing tables/columns, nonfinite values, wrong booleans, duplicate keys,
    model approvals, probabilities and unsupported official view reject with
    ValidationError. Neither inputs nor global policies are mutated.
    """
    schemas = get_schema()
    issues: list[Row] = []
    clean: dict[str, list[Row]] = {}
    if set(tables) != set(schemas):
        raise ValidationError(
            [
                dict(
                    severity="FATAL",
                    code="TABLE_SET",
                    object="dataset",
                    message="Exactly the 19 canonical tables are required",
                )
            ]
        )
    for name, rows in tables.items():
        schema = cast(dict[str, JSONValue], schemas[name])
        fields = cast(list[dict[str, JSONValue]], schema["fields"])
        clean[name] = []
        ids = set()
        for record in rows:
            try:
                current = row(
                    record,
                    (
                        "record_id",
                        "business_key",
                        "version_no",
                        "valid_from",
                        "valid_to",
                        "known_from",
                        "known_to",
                        "record_status",
                    ),
                )
                if set(current) != set(cast(list[str], schema["columns"])):
                    raise AccountingError("Columns differ from canonical schema")
                if current["record_id"] in ids:
                    raise AccountingError("Duplicate record_id")
                ids.add(current["record_id"])
                for field in fields:
                    key = str(field["field"])
                    value = current[key]
                    if value is not None and field["type"] == "number":
                        number(value, key)
                    if value is not None and field["type"] == "boolean" and type(value) is not bool:
                        raise AccountingError(f"{key}: boolean required")
                for key in ("sicr_override", "sppi_override", "own_credit_oci_mismatch"):
                    if (
                        key in current
                        and current[key] is not None
                        and type(current[key]) is not bool
                    ):
                        raise AccountingError(f"{key}: boolean required")
                clean[name].append(current)
            except (AccountingError, TypeError) as exc:
                issues.append(
                    dict(severity="ERROR", code="ROW_SCHEMA", object=name, message=str(exc))
                )
    if issues:
        raise ValidationError(issues)
    rc = clean["run_control"]
    if len(rc) != 1:
        raise ValidationError(
            [
                dict(
                    severity="ERROR",
                    code="RUN_CONTROL",
                    object="run_control",
                    message="Exactly one run control row required",
                )
            ]
        )
    if rc[0].get("view") not in {"REFERENCE", "MANAGEMENT"}:
        raise ValidationError(
            [
                dict(
                    severity="ERROR",
                    code="OFFICIAL_BLOCKED",
                    object="run_control",
                    message="Only REFERENCE or MANAGEMENT view supported",
                )
            ]
        )
    rd = reporting_date or str(rc[0]["reporting_date"])
    kt = knowledge_time or str(rc[0]["knowledge_time"])
    selected = select_snapshot(clean, rd, kt)
    try:
        result, _ = validate_tables(selected, rd, kt)
        if not result["scenarios"]:
            raise AccountingError("Scenario population required")
        for rec in result["scenarios"]:
            number(rec["probability"], "probability", 0, 1)
        for table in ("pd_curves", "lgd_profiles", "ead_profiles"):
            keys = [(r["instrument_id"], r["scenario_id"], r["year"]) for r in result[table]]
            if len(set(keys)) != len(keys):
                raise AccountingError(f"Duplicate curve key in {table}")
        for rec in result["market_data"]:
            if number(rec["fx_rate"], "fx_rate", 0) == 0:
                raise AccountingError("Positive FX rate required")
    except ValidationRejected as exc:
        raise ValidationError(exc.issues) from exc
    except (ValueError, TypeError, KeyError) as exc:
        raise ValidationError(
            [dict(severity="ERROR", code="DOMAIN_VALIDATION", object="dataset", message=str(exc))]
        ) from exc
    return cast(dict[str, list[Row]], result)
