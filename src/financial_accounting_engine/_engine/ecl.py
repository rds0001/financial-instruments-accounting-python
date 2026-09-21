# Copyright 2026 RiskDataScience GmbH
# SPDX-License-Identifier: Apache-2.0
from .._checks import weights
from ..formulas import poci_allowance_change, provision_matrix_ecl
from .formulas import cash_shortfall_ecl, component_ecl


def calculate_ecl(
    instrument: dict,
    stage: str,
    pd_rows: list[dict],
    lgd_rows: list[dict],
    ead_rows: list[dict],
    scenarios: dict[str, float],
    cashflow_rows: list[dict] | None = None,
    reporting_date: str | None = None,
) -> tuple[list[dict], dict]:
    if (
        stage == "NO_IMPAIRMENT_SCOPE"
        or instrument.get("impairment_scope") == "NO_IMPAIRMENT_SCOPE"
        or instrument.get("liability")
        or instrument.get("equity")
    ):
        return [], {
            "instrument_id": instrument["instrument_id"],
            "stage": "NO_IMPAIRMENT_SCOPE",
            "weighted_ecl": 0.0,
            "overlay": 0.0,
            "final_ecl": 0.0,
            "formula_id": "F-ECL-001",
        }
    weights(scenarios)
    rate = float(instrument["credit_adjusted_eir"] if stage == "POCI" else instrument["eir"])
    overlay = float(instrument.get("overlay") or 0)
    if overlay:
        governance = [
            instrument.get("overlay_id"),
            instrument.get("overlay_owner"),
            instrument.get("overlay_approved"),
            instrument.get("overlay_expiry"),
            instrument.get("overlay_thesis"),
            instrument.get("overlay_double_count_checked"),
        ]
        if not all(governance) or (
            reporting_date and str(instrument["overlay_expiry"]) < reporting_date
        ):
            raise ValueError(f"Overlay-Governance ungültig: {instrument['instrument_id']}")
    method = instrument.get("ecl_method")
    if method == "PROVISION_MATRIX":
        base = provision_matrix_ecl(
            float(instrument["gross_amount"]), float(instrument["provision_rate"])
        )
        return [
            {
                "instrument_id": instrument["instrument_id"],
                "scenario_id": "PROVISION_MATRIX",
                "year": 0,
                "marginal_pd": None,
                "ead": instrument["gross_amount"],
                "lgd": None,
                "discounted_ecl": base,
                "formula_id": "F-PM-001",
            }
        ], {
            "instrument_id": instrument["instrument_id"],
            "stage": stage,
            "ecl_method": method,
            "weighted_ecl": base,
            "overlay": overlay,
            "final_ecl": base + overlay,
            "formula_id": "F-PM-001",
            "model_version_id": "SYNTH_PROVISION_MATRIX_V1",
        }
    if method == "DIRECT_CASH_SHORTFALL":
        cashflow_rows = cashflow_rows or []
        contractual = [
            (float(x["year_fraction"]), float(x["amount"]))
            for x in cashflow_rows
            if x.get("contractual")
        ]
        details = []
        weighted = 0.0
        if not contractual:
            raise ValueError(f"Vertragliche Cashflows fehlen: {instrument['instrument_id']}")
        for sid, probability in scenarios.items():
            expected = [
                (float(x["year_fraction"]), float(x["amount"]))
                for x in cashflow_rows
                if x.get("expected") and x.get("scenario_id") == sid
            ]
            if not expected:
                raise ValueError(f"Expected Cashflows fehlen: {instrument['instrument_id']}/{sid}")
            value = cash_shortfall_ecl(contractual, expected, rate)
            weighted += probability * value
            details.append(
                {
                    "instrument_id": instrument["instrument_id"],
                    "scenario_id": sid,
                    "year": 0,
                    "marginal_pd": None,
                    "ead": None,
                    "lgd": None,
                    "discounted_ecl": value,
                    "formula_id": "F-CS-001",
                }
            )
        return details, {
            "instrument_id": instrument["instrument_id"],
            "stage": stage,
            "ecl_method": method,
            "weighted_ecl": weighted,
            "overlay": overlay,
            "final_ecl": (
                poci_allowance_change(weighted, float(instrument["poci_initial_lifetime_ecl"]))
                if stage == "POCI"
                else weighted
            )
            + overlay,
            "poci_initial_lifetime_ecl": float(instrument["poci_initial_lifetime_ecl"])
            if stage == "POCI"
            else 0.0,
            "formula_id": "F-CS-001",
            "model_version_id": "SYNTH_CASH_SHORTFALL_V1",
        }
    if method != "COMPONENT_PD_LGD_EAD":
        raise ValueError(f"Unbekannte ECL-Methode: {method}")
    horizon = 1 if stage == "STAGE_1" else 10**9
    pd_index = {(x["scenario_id"], int(x["year"])): x for x in pd_rows}
    lgd_index = {(x["scenario_id"], int(x["year"])): x for x in lgd_rows}
    ead_index = {(x["scenario_id"], int(x["year"])): x for x in ead_rows}
    if any(
        len(index) != len(rows)
        for index, rows in [(pd_index, pd_rows), (lgd_index, lgd_rows), (ead_index, ead_rows)]
    ):
        raise ValueError("Duplicate scenario/year curve keys")
    if set(pd_index) != set(lgd_index) or set(pd_index) != set(ead_index):
        raise ValueError("PD/LGD/EAD curve keys differ")
    for sid in scenarios:
        curve = [x for x in pd_rows if x["scenario_id"] == sid]
        if sum(float(x["marginal_pd"]) for x in curve) > 1 + 1e-9:
            raise ValueError("Marginal PD sum exceeds one")
        if any(
            type(x["year"]) not in (int, float)
            or float(x["year"]) < 1
            or int(x["year"]) != x["year"]
            for x in curve
        ):
            raise ValueError("Annual curve years must be positive integers")
    details, weighted = [], 0.0
    for scenario_id, probability in scenarios.items():
        years = sorted(y for (s, y) in pd_index if s == scenario_id and y <= horizon)
        if not years:
            raise ValueError(f"Missing default horizon: {scenario_id}")
        scenario_ecl = 0.0
        for year in years:
            pd = float(pd_index[(scenario_id, year)]["marginal_pd"])
            lgd = float(lgd_index[(scenario_id, year)]["lgd"])
            ead = float(ead_index[(scenario_id, year)]["ead"])
            component = component_ecl(pd, ead, lgd, rate, year)
            scenario_ecl += component
            details.append(
                {
                    "instrument_id": instrument["instrument_id"],
                    "scenario_id": scenario_id,
                    "year": year,
                    "marginal_pd": pd,
                    "ead": ead,
                    "lgd": lgd,
                    "discounted_ecl": component,
                    "formula_id": "F-ECL-001",
                }
            )
        weighted += probability * scenario_ecl
    poci_origin = (
        float(instrument.get("poci_initial_lifetime_ecl") or 0) if stage == "POCI" else 0.0
    )
    measured = poci_allowance_change(weighted, poci_origin) if stage == "POCI" else weighted
    return details, {
        "instrument_id": instrument["instrument_id"],
        "stage": stage,
        "ecl_method": method,
        "weighted_ecl": weighted,
        "poci_initial_lifetime_ecl": poci_origin,
        "overlay": overlay,
        "final_ecl": measured + overlay,
        "formula_id": "F-ECL-001",
        "model_version_id": "SYNTH_PD_LGD_EAD_V1",
    }
