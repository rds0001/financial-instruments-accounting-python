# Copyright 2026 RiskDataScience GmbH
# SPDX-License-Identifier: Apache-2.0
"""Scope, recognition and regular-way decisions from approved canonical facts."""


def assess_scope_and_recognition(instrument: dict) -> dict:
    required = ["scope_assessment", "recognition_status", "trade_date_policy"]
    missing = [x for x in required if instrument.get(x) in (None, "")]
    if missing:
        raise ValueError(
            f"Fehlende Scope-/Ansatzentscheidung für {instrument.get('instrument_id')}: {missing}"
        )
    scope = instrument["scope_assessment"]
    if scope == "OUTSIDE_IFRS9_OWN_USE":
        nature_criteria = bool(
            instrument.get("nature_dependent_contract")
            and instrument.get("purchaser_net_buyer")
            and instrument.get("quantity_consistent_expected_usage")
            and instrument.get("sale_timing_uncontrollable")
            and instrument.get("repurchase_within_reasonable_time")
        )
        if (
            not instrument.get("own_use")
            or instrument.get("instrument_type") != "NATURE_DEPENDENT_ELECTRICITY"
            or not nature_criteria
        ):
            raise ValueError("Own-use-Ausnahme ist inkonsistent dokumentiert")
        decision, reason = "NO_IFRS9_SCOPE", "IFRS9.2.4_B2.7-B2.8"
    elif scope == "IN_IFRS9_SCOPE":
        decision, reason = "IN_IFRS9_SCOPE", "IFRS9.2.1-2.7"
    elif scope.startswith("OUTSIDE_IFRS9_"):
        standard = str(instrument.get("interface_standard") or "")
        decision_id = instrument.get("interface_decision_id")
        if standard not in {
            "IAS32",
            "IFRS7",
            "IFRS13",
            "IFRS15",
            "IFRS16",
            "IFRS17",
            "IAS21",
            "IAS28",
            "IAS36",
            "IAS37",
            "IFRS10",
        }:
            raise ValueError(f"Unbekannte angrenzende Standard-Schnittstelle: {standard}")
        if not decision_id or not instrument.get("interface_approved"):
            raise ValueError("Scope-Schnittstelle ohne dokumentierte Freigabe")
        decision, reason = "NO_IFRS9_SCOPE", f"CONTROLLED_INTERFACE_{standard}_{decision_id}"
    else:
        raise ValueError(f"Unbekannte Scope-Entscheidung: {scope}")
    recognition = instrument["recognition_status"]
    if decision == "IN_IFRS9_SCOPE" and recognition not in {"RECOGNISED", "PENDING_REGULAR_WAY"}:
        raise ValueError("In-scope-Instrument ohne zulässigen Ansatzstatus")
    if instrument.get("regular_way") and instrument["trade_date_policy"] not in {
        "TRADE_DATE",
        "SETTLEMENT_DATE",
    }:
        raise ValueError("Regular-way-Policy fehlt")
    epay = "NOT_APPLICABLE"
    if instrument.get("electronic_payment_election"):
        criteria = bool(
            instrument.get("liability")
            and instrument.get("payment_irrevocable")
            and not instrument.get("withdrawal_access_practical")
            and instrument.get("settlement_risk_insignificant")
            and instrument.get("settlement_short_period")
        )
        if not criteria:
            raise ValueError(
                "Electronic-payment-Derecognition-Wahlrecht ohne vollständige Kriterien"
            )
        epay = "ELECTRONIC_PAYMENT_EXCEPTION_APPLIED"
    return {
        "instrument_id": instrument["instrument_id"],
        "scope_decision": decision,
        "recognition_event": recognition,
        "regular_way_policy": instrument["trade_date_policy"]
        if instrument.get("regular_way")
        else "NOT_APPLICABLE",
        "electronic_payment_result": epay,
        "controlled_interface": instrument.get("interface_standard") or "NOT_APPLICABLE",
        "interface_decision_id": instrument.get("interface_decision_id"),
        "decision_rule_id": "SCOPE-001",
        "source_reference": reason,
    }
