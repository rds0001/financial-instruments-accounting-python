# Copyright 2026 RiskDataScience GmbH
# SPDX-License-Identifier: Apache-2.0
"""IFRS 7-oriented aggregations and strictly separated regulatory bridges."""

from __future__ import annotations

from collections import defaultdict


def aggregate_disclosures(rows: list[dict]) -> list[dict]:
    result = []
    dimensions = (
        ("entity_id",),
        ("portfolio",),
        ("classification",),
        ("stage",),
        ("currency",),
        ("entity_id", "portfolio", "classification", "stage", "currency"),
    )
    for fields in dimensions:
        groups = defaultdict(list)
        for row in rows:
            groups[tuple(row.get(field) for field in fields)].append(row)
        for key, members in sorted(groups.items(), key=lambda item: str(item[0])):
            gross = sum(float(x["gross_carrying_amount"]) for x in members)
            allowance = sum(float(x["allowance"]) for x in members)
            result.append(
                {
                    "aggregation_level": "+".join(fields),
                    "dimension_key": "|".join(str(x) for x in key),
                    "instrument_count": len(members),
                    "gross_carrying_amount": gross,
                    "allowance": allowance,
                    "net_carrying_amount": gross - allowance,
                    "coverage_ratio": allowance / gross if gross else None,
                    "formula_id": "F-AGG-001",
                }
            )
    return result


def allowance_rollforward(
    instruments: list[dict],
    opening: dict[str, float],
    ecl: dict[str, dict],
    events: list[dict],
    fx: dict[str, float],
) -> list[dict]:
    by_instrument = defaultdict(list)
    for event in events:
        by_instrument[event["instrument_id"]].append(event)
    rows = []
    for instrument in instruments:
        iid = instrument["instrument_id"]
        opened = float(opening.get(iid, 0))
        target = float(ecl[iid]["final_ecl"])
        writeoff = sum(
            float(x["amount"]) * fx[iid]
            for x in by_instrument[iid]
            if x["event_type"] == "WRITEOFF"
        )
        remeasurement = target - opened
        closing = (
            opened + remeasurement - writeoff
            if instrument.get("poci")
            else max(opened + remeasurement - writeoff, 0)
        )
        rows.append(
            {
                "instrument_id": iid,
                "prior_stage": ecl[iid].get("prior_stage"),
                "current_stage": ecl[iid]["stage"],
                "opening_allowance": opened,
                "ecl_remeasurement": remeasurement,
                "writeoff": writeoff,
                "closing_allowance": closing,
                "formula_id": "F-ROLL-001",
            }
        )
    return rows


def gross_rollforward(
    instruments: list[dict],
    opening_gross: dict[str, float],
    events: list[dict],
    fx: dict[str, float],
) -> list[dict]:
    by_instrument = defaultdict(list)
    for event in events:
        by_instrument[event["instrument_id"]].append(event)
    rows = []
    for instrument in instruments:
        if instrument.get("liability"):
            continue
        iid = instrument["instrument_id"]
        opened = float(opening_gross.get(iid, 0))
        current = float(instrument.get("gross_amount") or 0) * fx[iid]
        writeoff = sum(
            float(x["amount"]) * fx[iid]
            for x in by_instrument[iid]
            if x["event_type"] == "WRITEOFF"
        )
        derecognition = sum(
            max(float(x["amount"]) - float(x.get("continuing_involvement") or 0), 0) * fx[iid]
            for x in by_instrument[iid]
            if x["event_type"] == "ASSET_TRANSFER"
            and x["derecognition_result"] != "NO_DERECOGNITION"
        )
        modification = sum(
            float(x.get("modification_result") or 0) * fx[iid]
            for x in by_instrument[iid]
            if x["event_type"].startswith("ASSET_MODIFICATION")
        )
        other = current - opened - modification
        closing = opened + modification + other - writeoff - derecognition
        rows.append(
            {
                "instrument_id": iid,
                "opening_gross": opened,
                "modification": modification,
                "other_contractual_and_fx_movements": other,
                "writeoff": writeoff,
                "derecognition": derecognition,
                "closing_gross": closing,
                "formula_id": "F-ROLL-001",
            }
        )
    return rows


def regulatory_bridge(
    instruments: list[dict], ecl: dict[str, dict], stages: dict[str, str], fx: dict[str, float]
) -> list[dict]:
    return [
        {
            "instrument_id": row["instrument_id"],
            "view": "REGULATORY_BRIDGE",
            "regulatory_approach": row.get("regulatory_approach"),
            "ifrs9_stage": stages[row["instrument_id"]],
            "regulatory_default_flag": bool(row.get("regulatory_default_flag")),
            "ifrs9_ecl": float(ecl[row["instrument_id"]]["final_ecl"]),
            "regulatory_expected_loss": float(row.get("regulatory_expected_loss") or 0)
            * fx[row["instrument_id"]],
            "difference": float(ecl[row["instrument_id"]]["final_ecl"])
            - float(row.get("regulatory_expected_loss") or 0) * fx[row["instrument_id"]],
            "accounting_value_used_in_regulatory_calculation": False,
            "formula_id": "F-REG-BRIDGE-001",
        }
        for row in instruments
    ]
