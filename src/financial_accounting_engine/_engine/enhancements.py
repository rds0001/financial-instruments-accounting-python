# Copyright 2026 RiskDataScience GmbH
# SPDX-License-Identifier: Apache-2.0
def assess_allocations(collateral_rows: list[dict], instruments: dict[str, dict]) -> list[dict]:
    results = []
    for row in collateral_rows:
        available = max(
            float(row["fair_value"]) * (1 - float(row["haircut"])) - float(row["cost"]), 0
        )
        allocated = float(row["allocated_amount"])
        if allocated > available + 1e-9:
            raise ValueError(f"Überallokation Credit Enhancement: {row['collateral_id']}")
        included = not bool(row.get("separately_recognised"))
        results.append(
            {
                "collateral_id": row["collateral_id"],
                "instrument_id": row["instrument_id"],
                "available_protection": available,
                "allocated_amount": allocated,
                "included_in_ecl": included,
                "recovery_year": row["recovery_year"],
                "formula_id": "F-COL-001",
                "source_reference": "IFRS9.B5.5.55",
            }
        )
    return results
