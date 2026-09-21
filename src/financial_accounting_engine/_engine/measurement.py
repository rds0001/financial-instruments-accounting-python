# Copyright 2026 RiskDataScience GmbH
# SPDX-License-Identifier: Apache-2.0
from .formulas import amortised_cost_step, effective_interest_rate


def initial_measurement(instrument: dict, classification: str) -> dict:
    fv = float(instrument["fair_value"])
    costs = float(instrument["transaction_costs"])
    if classification in {"FVTPL", "FVTPL_LIABILITY"}:
        initial = fv
        cost_treatment = "P&L"
    elif classification == "NO_IFRS9_SCOPE":
        initial, cost_treatment = 0.0, "NOT_APPLICABLE"
    else:
        sign = -1.0 if instrument.get("liability") else 1.0
        initial, cost_treatment = fv + sign * costs, "IN_EFFECTIVE_INTEREST_RATE"
    return {
        "instrument_id": instrument["instrument_id"],
        "initial_carrying_amount": initial,
        "transaction_cost_treatment": cost_treatment,
        "day_one_difference": fv - float(instrument["transaction_price"]),
        "formula_id": "F-INIT-001",
        "source_reference": "IFRS9.5.1.1-5.1.3",
    }


def calculate_eir(instrument: dict, cashflows: list[dict], initial_amount: float) -> dict:
    if instrument.get("poci"):
        rate = float(instrument["credit_adjusted_eir"])
        method = "CREDIT_ADJUSTED_EIR"
    else:
        flows = [
            (float(x["year_fraction"]), float(x["amount"]))
            for x in cashflows
            if x.get("include_in_eir") and x.get("contractual")
        ]
        excluded_types = {
            "FINANCIAL_GUARANTEE",
            "LOAN_COMMITMENT",
            "DERIVATIVE",
            "NATURE_DEPENDENT_ELECTRICITY",
        }
        if (
            not flows
            or initial_amount <= 0
            or instrument.get("equity")
            or instrument.get("instrument_type") in excluded_types
            or instrument.get("scope_assessment") != "IN_IFRS9_SCOPE"
        ):
            return {
                "instrument_id": instrument["instrument_id"],
                "calculated_eir": None,
                "contractual_eir": instrument.get("eir"),
                "eir_method": "NOT_APPLICABLE",
                "formula_id": "F-EIR-001",
            }
        rate = effective_interest_rate(initial_amount, flows)
        method = "EXPECTED_CONTRACTUAL_CASHFLOWS"
    return {
        "instrument_id": instrument["instrument_id"],
        "calculated_eir": rate,
        "contractual_eir": float(instrument.get("eir") or 0),
        "eir_method": method,
        "formula_id": "F-EIR-001",
        "source_reference": "IFRS9.Appendix_A_B5.4.1",
    }


def interest_revenue(instrument: dict, stage: str, allowance: float) -> dict:
    gross = float(instrument["gross_amount"] or 0)
    rate = float(
        instrument.get("credit_adjusted_eir")
        if instrument.get("poci")
        else instrument.get("eir") or 0
    )
    basis = max(gross - allowance, 0) if stage in {"STAGE_3", "POCI"} else gross
    method = "NET" if stage == "STAGE_3" else "CREDIT_ADJUSTED" if stage == "POCI" else "GROSS"
    return {
        "instrument_id": instrument["instrument_id"],
        "interest_basis": basis,
        "interest_rate": rate,
        "interest_revenue": basis * rate,
        "interest_method": method,
        "formula_id": "F-AC-001",
        "source_reference": "IFRS9.5.4.1",
    }


def own_credit(market: dict, classification: str) -> dict:
    total = float(market.get("total_fv_change") or 0)
    own = float(market.get("own_credit_change") or 0)
    if classification != "FVTPL_LIABILITY":
        own = 0.0
    mismatch = bool(market.get("own_credit_oci_mismatch"))
    own_oci = 0.0 if mismatch else own
    return {
        "instrument_id": market["instrument_id"],
        "total_fv_change": total,
        "own_credit_oci": own_oci,
        "own_credit_pnl_due_to_mismatch": own if mismatch else 0.0,
        "other_fv_change_pnl": total - own_oci,
        "formula_id": "F-OWNCR-001",
        "source_reference": "IFRS9.5.7.7-5.7.9",
    }


def subsequent_measurement(
    instrument: dict, classification: str, opening: float, cashflows: list[dict]
) -> dict:
    """One-period AC schedule; resets update future interest without changing original EIR lineage."""
    if classification not in {
        "AMORTISED_COST",
        "AMORTISED_COST_LIABILITY",
        "AC_HOST_PLUS_SEPARATE_DERIVATIVE",
        "FVOCI_DEBT",
    }:
        return {
            "instrument_id": instrument["instrument_id"],
            "opening_gross": opening,
            "interest": 0.0,
            "cash_received": 0.0,
            "closing_gross": opening,
            "rate_method": "NOT_APPLICABLE",
            "formula_id": "F-AC-001",
        }
    original_rate = float(
        instrument.get("credit_adjusted_eir")
        if instrument.get("poci")
        else instrument.get("eir") or 0
    )
    applied_rate = (
        float(instrument.get("reset_rate"))
        if instrument.get("rate_type") == "FLOATING" and instrument.get("reset_rate") is not None
        else original_rate
    )
    cash = sum(
        float(x["amount"])
        for x in cashflows
        if x.get("contractual") and 0 < float(x["year_fraction"]) <= 1
    )
    closing = amortised_cost_step(opening, applied_rate, 1.0, cash)
    return {
        "instrument_id": instrument["instrument_id"],
        "opening_gross": opening,
        "interest": opening * applied_rate,
        "cash_received": cash,
        "closing_gross": closing,
        "original_eir": original_rate,
        "applied_rate": applied_rate,
        "rate_method": "FLOATING_RESET" if applied_rate != original_rate else "ORIGINAL_EIR",
        "formula_id": "F-AC-001",
        "source_reference": "IFRS9.B5.4.5-B5.4.6",
    }


def fair_value_presentation(instrument: dict, market: dict, classification: str) -> dict:
    total = float(market.get("total_fv_change") or 0)
    if classification in {"FVTPL", "FVTPL_LIABILITY"}:
        own = own_credit(market, classification)
        pnl, oci, recycling = (
            float(own["other_fv_change_pnl"]),
            float(own["own_credit_oci"]),
            "NOT_APPLICABLE",
        )
    elif classification == "FVOCI_DEBT":
        pnl, oci, recycling = 0.0, total, "RECYCLE_ON_DERECOGNITION"
    elif classification == "FVOCI_EQUITY":
        pnl, oci, recycling = 0.0, total, "NO_RECYCLING"
    else:
        pnl, oci, recycling = 0.0, 0.0, "NOT_APPLICABLE"
    return {
        "instrument_id": instrument["instrument_id"],
        "classification": classification,
        "fair_value": float(market["fair_value"]),
        "total_fv_change": total,
        "pnl_fv_change": pnl,
        "oci_fv_change": oci,
        "recycling_policy": recycling,
        "ifrs13_level": market["ifrs13_level"],
        "valuation_model": market["valuation_model"],
        "valuation_status": market["valuation_status"],
        "formula_id": "F-FV-001",
        "source_reference": "IFRS9.5.7_IFRS13",
    }
