# Copyright 2026 RiskDataScience GmbH
# SPDX-License-Identifier: Apache-2.0
from .formulas import hedge_ineffectiveness


def measure(row: dict) -> dict:
    if row.get("hedge_type") not in {"FAIR_VALUE", "CASH_FLOW", "NET_INVESTMENT"}:
        raise ValueError("Unknown hedge type")
    complete = all(
        bool(row.get(x))
        for x in [
            "hedging_instrument_eligible",
            "hedged_item_eligible",
            "risk_component_eligible",
            "designation_documented",
            "risk_management_objective",
        ]
    )
    if row.get("nature_dependent_electricity_hedge"):
        complete = bool(
            complete
            and row.get("variable_nominal_volume")
            and row.get("volume_assumptions_documented")
            and row.get("forecast_transaction_expected")
            and row.get("hedge_type") == "CASH_FLOW"
        )
    eligible = bool(
        complete
        and row.get("designated")
        and row.get("economic_relationship")
        and not row.get("credit_risk_dominates")
        and float(row.get("hedge_ratio", 0)) > 0
    )
    if not eligible:
        return {
            "relationship_id": row["relationship_id"],
            "status": "REJECTED",
            "ineffectiveness_pnl": 0.0,
            "oci_effective": 0.0,
            "cost_of_hedging_reserve": 0.0,
            "recycle_amount": 0.0,
            "basis_adjustment": 0.0,
            "formula_id": "F-HDG-001",
        }
    ineffective = hedge_ineffectiveness(float(row["hedging_change"]), float(row["hedged_change"]))
    gain, item = float(row["hedging_change"]), float(row["hedged_change"])
    oci = 0.0
    if row["hedge_type"] != "FAIR_VALUE":
        oci = (1 if gain >= 0 else -1) * min(abs(gain), abs(item)) if gain * item < 0 else 0.0
        ineffective = gain - oci
    if row.get("discontinue") or (
        row["hedge_type"] == "CASH_FLOW" and not row.get("forecast_transaction_expected")
    ):
        status = "DISCONTINUED"
    elif (
        row.get("rebalancing_required")
        or abs(float(row["hedge_ratio"]) - float(row["target_hedge_ratio"])) > 1e-12
    ):
        status = "REBALANCE_REQUIRED"
    else:
        status = "ELIGIBLE"
    costs = (
        float(row.get("option_time_value_change") or 0)
        + float(row.get("forward_element_change") or 0)
        + float(row.get("basis_spread_change") or 0)
    )
    return {
        "relationship_id": row["relationship_id"],
        "hedge_type": row["hedge_type"],
        "status": status,
        "nature_dependent_electricity_hedge": bool(row.get("nature_dependent_electricity_hedge")),
        "ineffectiveness_pnl": ineffective,
        "oci_effective": oci,
        "cost_of_hedging_reserve": costs,
        "recycle_amount": float(row.get("recycle_amount") or 0),
        "basis_adjustment": float(row.get("basis_adjustment") or 0),
        "formula_id": "F-HDG-001",
        "source_reference": "IFRS9.6.4-6.5_6.10",
    }
