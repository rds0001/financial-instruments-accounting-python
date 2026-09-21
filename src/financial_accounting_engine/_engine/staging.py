# Copyright 2026 RiskDataScience GmbH
# SPDX-License-Identifier: Apache-2.0
def assess_stage(row: dict, policy: dict) -> dict:
    override = row.get("sicr_override")
    if override is not None or row.get("sicr_rebuttal"):
        if (
            not row.get("override_approved")
            or not row.get("override_reason")
            or not row.get("override_expiry")
        ):
            raise ValueError(f"Unvollständiger Stage Override: {row.get('instrument_id')}")
        if str(row["override_expiry"]) < str(policy["reporting_date"]):
            raise ValueError(f"Abgelaufener Stage Override: {row.get('instrument_id')}")
    if row.get("impairment_scope") == "NO_IMPAIRMENT_SCOPE":
        stage, reason = "NO_IMPAIRMENT_SCOPE", "OUTSIDE_IMPAIRMENT_REQUIREMENTS"
    elif row.get("poci"):
        stage, reason = "POCI", "POCI_AT_ORIGINATION"
    elif row.get("simplified"):
        stage, reason = "SIMPLIFIED_LIFETIME", "SIMPLIFIED_APPROACH"
    elif (
        row.get("credit_impaired")
        or row.get("unlikely_to_pay")
        or row.get("days_past_due", 0) >= policy["default_backstop_days"]
    ):
        stage, reason = "STAGE_3", "CREDIT_IMPAIRED_OR_DEFAULT_BACKSTOP"
    elif policy.get("low_credit_risk_relief") and row.get("low_credit_risk"):
        stage, reason = "STAGE_1", "LOW_CREDIT_RISK_RELIEF"
    else:
        triggers = []
        if override is True:
            triggers.append("APPROVED_OVERRIDE")
        if row.get("watchlist"):
            triggers.append("WATCHLIST")
        if row.get("forbearance"):
            triggers.append("FORBEARANCE")
        if row.get("forward_looking_sicr"):
            triggers.append("FORWARD_LOOKING_SICR")
        if row.get("collective_assessment"):
            triggers.append("COLLECTIVE_TOP_DOWN")
        if row.get("days_past_due", 0) >= policy["past_due_sicr_days"]:
            if row.get("sicr_rebuttal"):
                if (
                    not row.get("override_approved")
                    or not row.get("override_reason")
                    or not row.get("override_expiry")
                ):
                    raise ValueError(
                        f"Past-due-Widerlegung ohne Freigabe: {row.get('instrument_id')}"
                    )
            else:
                triggers.append("PAST_DUE_REBUTTABLE_PRESUMPTION")
        if row.get("rating_current", 0) - row.get("rating_orig", 0) >= policy["rating_notch_sicr"]:
            triggers.append("RATING_MIGRATION")
        orig_pd, current_pd = row.get("lifetime_pd_orig"), row.get("lifetime_pd_current")
        if orig_pd not in (None, "") and current_pd not in (None, ""):
            if float(current_pd) - float(orig_pd) >= float(
                policy.get("absolute_lifetime_pd_sicr", 1.0)
            ):
                triggers.append("ABSOLUTE_LIFETIME_PD_CHANGE")
            if float(orig_pd) > 0 and float(current_pd) / float(orig_pd) >= float(
                policy.get("relative_lifetime_pd_sicr", 10**9)
            ):
                triggers.append("RELATIVE_LIFETIME_PD_CHANGE")
        if int(row["months_since_cure"] if row.get("months_since_cure") is not None else 999) < int(
            policy["cure_months"]
        ):
            triggers.append("CURE_PERIOD")
        if int(
            row["months_since_forbearance"]
            if row.get("months_since_forbearance") is not None
            else 999
        ) < int(policy["probation_months"]):
            triggers.append("FORBEARANCE_PROBATION")
        stage, reason = ("STAGE_2", "+".join(triggers)) if triggers else ("STAGE_1", "NO_SICR")
    return {
        "instrument_id": row["instrument_id"],
        "prior_stage": row.get("prior_stage") or "NOT_AVAILABLE",
        "stage": stage,
        "stage_movement": f"{row.get('prior_stage') or 'NOT_AVAILABLE'}->{stage}",
        "stage_reason": reason,
        "decision_rule_id": "STG-001",
        "source_reference": "IFRS9.5.5.3-5.5.11",
    }
