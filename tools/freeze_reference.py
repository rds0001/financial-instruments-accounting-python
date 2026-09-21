"""Explicit maintenance command: review baseline deltas and freeze corrected reference tables.

Not invoked by builds/tests. Changes require reviewing the resulting correction ledger.
"""

import hashlib
import json
import math
from pathlib import Path

import financial_accounting_engine as f

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "src/financial_accounting_engine/resources"


def key(sheet, row, index):
    if sheet == "JOURNALS":
        return str((row["journal_batch_id"], row["account"]))
    if sheet == "ECL_COMPONENTS":
        return str((row["instrument_id"], row["scenario_id"], row["year"]))
    if sheet == "DISCLOSURE_AGGREGATES":
        return str((row["aggregation_level"], row["dimension_key"]))
    for field in (
        "control_id",
        "metric",
        "event_id",
        "instrument_id",
        "relationship_id",
        "reserve_type",
        "scenario_id",
    ):
        if field in row:
            return str(row[field])
    if "model_version_id" in row:
        return str(
            (
                row.get("model_type"),
                row["model_version_id"],
                row.get("segment"),
                row.get("challenger_flag"),
            )
        )
    return str(index)


def normal(row):
    return {
        k: (None if k == "explanation" and v == "" else v) for k, v in row.items() if k != "run_id"
    }


def same(a, b):
    if (
        isinstance(a, (int, float))
        and isinstance(b, (int, float))
        and not isinstance(a, bool)
        and not isinstance(b, bool)
    ):
        return math.isclose(a, b, rel_tol=1e-10, abs_tol=1e-8)
    return a == b


def decimalize(value):
    if isinstance(value, float):
        return {"decimal": str(value)}
    if isinstance(value, dict):
        return {k: decimalize(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [decimalize(v) for v in value]
    return value


def main():
    baseline = json.loads((RES / "baseline.json").read_text())
    frozen = {}
    changes = []
    for profile in f.list_profiles():
        result = f.run_dataset(f.load_reference_data(profile))
        assert result.status == "APPROVED_REFERENCE"
        for table, oldrows in baseline[profile]["tables"].items():
            sheet = table.split("/")[-1]
            before = {key(sheet, r, i): normal(r) for i, r in enumerate(oldrows)}
            after = {key(sheet, r, i): normal(r) for i, r in enumerate(result.tables[table])}
            assert len(before) == len(oldrows) and len(after) == len(result.tables[table]), table
            for identity in sorted(before.keys() | after.keys()):
                a, b = before.get(identity, {}), after.get(identity, {})
                for field in sorted(a.keys() | b.keys()):
                    old, new = a.get(field), b.get(field)
                    if same(old, new):
                        continue
                    reason = None
                    if (
                        field in {"basis_adjustment", "poci_initial_lifetime_ecl"}
                        and old is None
                        and new == 0
                    ):
                        reason = "EXPLICIT_ZERO_NONAPPLICABLE_MOVEMENT"
                    elif sheet == "JOURNALS" and identity.startswith("('HDG-"):
                        reason = "HEDGE_GAIN_CREDIT_AND_RESERVE_RELEASE"
                    elif (
                        sheet == "JOURNALS" and "EVT-" in identity and field in {"debit", "credit"}
                    ):
                        reason = "MODIFICATION_GAIN_LOSS_JOURNAL_SIGN"
                    elif (
                        field == "pnl_effect"
                        and sheet in {"DERECOGNITION", "MODIFICATIONS", "EVENTS"}
                        and old == -25000
                        and new == 0
                    ):
                        reason = "WRITEOFF_ALLOWANCE_UTILISATION_NO_DUPLICATE_EXPENSE"
                    elif profile == "MID_SIZE_UNIVERSAL_FIA" and (
                        "U_POCI_09" in identity
                        or sheet
                        in {"SUMMARY", "CONTROLS", "DISCLOSURE_AGGREGATES", "SCENARIO_SENSITIVITY"}
                    ):
                        reason = "POCI_CREDIT_ADJUSTED_RATE_AND_NET_INTEREST"
                    if reason is None:
                        raise AssertionError(
                            (
                                "UNREVIEWED BASELINE CHANGE",
                                profile,
                                table,
                                identity,
                                field,
                                old,
                                new,
                            )
                        )
                    changes.append(
                        dict(
                            profile=profile,
                            table=table,
                            key=identity,
                            field=field,
                            before=old,
                            after=new,
                            reason=reason,
                        )
                    )
        frozen[profile] = {
            "status": result.status,
            "metrics": result.metrics,
            "tables": {k: [normal(r) for r in rows] for k, rows in result.tables.items()},
        }
    payload = {
        "schema_version": "1.0",
        "numeric_encoding": "floating-point numbers as {decimal: string}; integer counts retained",
        "ignored_technical_fields": ["run_id"],
        "normalized_excel_fields": {"explanation": "empty string and null equivalent"},
        "absolute_tolerance": "0.00000001",
        "relative_tolerance": "0.0000000001",
        "r_parity": "PENDING_NOT_IMPLEMENTED",
        "profiles": decimalize(frozen),
    }
    (RES / "golden.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    (ROOT / "docs/correction_ledger.json").write_text(
        json.dumps(decimalize(changes), indent=2, ensure_ascii=False) + "\n"
    )
    (RES / "manifest.json").write_text(
        json.dumps(
            {
                p.relative_to(RES).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted(RES.rglob("*"))
                if p.is_file() and p.name != "manifest.json"
            },
            indent=2,
        )
        + "\n"
    )
    print("Reviewed correction entries:", len(changes))
    from collections import Counter

    print(Counter(c["reason"] for c in changes))


if __name__ == "__main__":
    main()
