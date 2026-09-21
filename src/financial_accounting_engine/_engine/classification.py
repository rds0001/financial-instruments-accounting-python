# Copyright 2026 RiskDataScience GmbH
# SPDX-License-Identifier: Apache-2.0
def assess_sppi(features: dict) -> tuple[bool, str]:
    if features.get("sppi_override") is not None:
        if not features.get("approval_id"):
            raise ValueError("SPPI override ohne Freigabe")
        return bool(features["sppi_override"]), "APPROVED_OVERRIDE"
    features = dict(features)
    if features.get("de_minimis_or_non_genuine"):
        features["contingent_feature_basic"] = True
    checks = [
        "principal_consistent",
        "basic_interest",
        "modified_time_value_pass",
        "prepayment_compensation_reasonable",
        "extension_basic",
        "non_recourse_pass",
        "cli_lookthrough_pass",
        "contingent_feature_basic",
    ]
    missing = [x for x in checks if features.get(x) is None]
    if missing:
        raise ValueError(f"SPPI-Facts fehlen: {missing}")
    passed = all(bool(features[x]) for x in checks) and not bool(features.get("leverage"))
    return passed, "ALL_BASIC_LENDING_FEATURES" if passed else "NON_BASIC_OR_LEVERAGED_FEATURE"


def classify(
    row: dict, features: dict | None = None, scope_decision: str = "IN_IFRS9_SCOPE"
) -> dict:
    if scope_decision == "NO_IFRS9_SCOPE":
        return {
            "instrument_id": row["instrument_id"],
            "classification": "NO_IFRS9_SCOPE",
            "sppi_result": "NOT_APPLICABLE",
            "sppi_reason": "NOT_APPLICABLE",
            "decision_rule_id": "SCOPE-001",
            "source_reference": "IFRS9.2",
        }
    if features is None:
        sppi_pass, sppi_reason = bool(row.get("sppi_pass")), "LEGACY_TEST_INPUT"
    else:
        sppi_pass, sppi_reason = assess_sppi(features)
    itype = row.get("instrument_type")
    if (row.get("fvoci_equity_election") or row.get("fair_value_option")) and not row.get(
        "designation_approval_id"
    ):
        raise ValueError("Unwiderrufliche Designation ohne Freigabenachweis")
    if (
        features
        and features.get("business_model_change")
        and (row.get("liability") or row.get("equity"))
    ):
        raise ValueError("Unzulässige Reklassifizierung außerhalb finanzieller Vermögenswerte")
    if itype == "FINANCIAL_GUARANTEE":
        category, reason = "FINANCIAL_GUARANTEE", "IFRS9.4.2.1(c)_5.5"
    elif itype == "LOAN_COMMITMENT":
        category, reason = "LOAN_COMMITMENT", "IFRS9.2.1(g)_5.5"
    elif row.get("liability"):
        if (
            row.get("hybrid_contract")
            and row.get("host_contract_type") == "FINANCIAL_LIABILITY"
            and row.get("embedded_derivative_separated")
        ):
            category = "AC_HOST_PLUS_SEPARATE_DERIVATIVE"
        else:
            category = (
                "FVTPL_LIABILITY"
                if row.get("held_for_trading") or row.get("fair_value_option")
                else "AMORTISED_COST_LIABILITY"
            )
        reason = "IFRS9.4.2"
    elif row.get("equity"):
        if row.get("fvoci_equity_election") and row.get("held_for_trading"):
            raise ValueError("Trading equity cannot elect FVOCI")
        category = "FVOCI_EQUITY" if row.get("fvoci_equity_election") else "FVTPL"
        reason = "IFRS9.5.7.5" if row.get("fvoci_equity_election") else "IFRS9.4.1.4"
    elif row.get("fair_value_option"):
        category, reason = "FVTPL", "IFRS9.4.1.5_ACCOUNTING_MISMATCH"
    elif not sppi_pass or row.get("business_model") == "OTHER":
        category, reason = "FVTPL", "IFRS9.4.1.4"
    elif row.get("business_model") == "HOLD_TO_COLLECT_AND_SELL":
        category, reason = "FVOCI_DEBT", "IFRS9.4.1.2A"
    elif row.get("business_model") == "HOLD_TO_COLLECT":
        category, reason = "AMORTISED_COST", "IFRS9.4.1.2"
    else:
        raise ValueError(f"Unbekanntes Geschäftsmodell: {row.get('business_model')}")
    reclassification = (
        "PROSPECTIVE_RECLASSIFICATION"
        if features and features.get("business_model_change")
        else "NO_RECLASSIFICATION"
    )
    return {
        "instrument_id": row["instrument_id"],
        "classification": category,
        "sppi_result": "PASS" if sppi_pass else "FAIL",
        "sppi_reason": sppi_reason,
        "reclassification_status": reclassification,
        "decision_rule_id": "CLS-001",
        "source_reference": reason,
    }
