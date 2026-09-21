"""Executable analyst examples, one direct call with a checked result per public function.

Run from an installed environment: python examples/analyst_workbook.py.
Only explicit export cases write to the supplied workspace.
"""

import math
from pathlib import Path

import financial_accounting_engine as f


def cases(workspace: Path):
    data = f.load_reference_data("MID_SIZE_UNIVERSAL_FIA")
    result = f.run_dataset(data)
    inst = data["instruments"][0]
    features = data["classification_inputs"][0]
    stage = data["staging_inputs"][0]
    market = data["market_data"][0]
    hedge = data["hedges"][0]
    ecl = [{"instrument_id": "x", "stage": "STAGE_1", "final_ecl": 20}]
    simple = [
        dict(
            instrument_id="x",
            gross_amount=100,
            liability=False,
            poci=False,
            entity_id="E",
            portfolio="P",
            currency="EUR",
            regulatory_expected_loss=15,
        )
    ]
    facts = [
        dict(
            instrument_id="x",
            entity_id="E",
            portfolio="P",
            classification="AMORTISED_COST",
            stage="STAGE_1",
            currency="EUR",
            presentation_currency="EUR",
            gross_carrying_amount=100,
            allowance=20,
        )
    ]
    overlay = dict(
        overlay=10,
        overlay_id="O",
        overlay_owner="Risk",
        overlay_approved=True,
        overlay_expiry="2026-12-31",
        overlay_thesis="Emerging risk",
        overlay_double_count_checked=True,
    )
    source = {"instrument_id": "x", "gross_amount": 100}

    def event(kind, **extra):
        return dict(
            event_id="EV",
            instrument_id="x",
            event_type=kind,
            approved=True,
            reason_code="APPROVED",
            amount=10,
            **extra,
        )

    def close(expected):
        return lambda actual: math.isclose(actual, expected, rel_tol=1e-9, abs_tol=1e-9)

    def field(key, value):
        return lambda actual: actual[key] == value

    cf = dict(
        instrument_id="x",
        impairment_scope="GENERAL_ECL",
        ecl_method="COMPONENT_PD_LGD_EAD",
        eir=0.05,
        overlay=0,
    )
    curve = [dict(scenario_id="base", year=1, marginal_pd=0.02)]
    lgd = [dict(scenario_id="base", year=1, lgd=0.4)]
    ead = [dict(scenario_id="base", year=1, ead=100000)]
    # (arguments, keyword arguments, independently specified check)
    c = {
        "discount_factor": ((0.05, 1), {}, close(1 / 1.05)),
        "effective_interest_rate": ((1000, [(1, 1100)]), {}, close(0.1)),
        "amortised_cost_step": ((1000, 0.1, 1, 200), {}, close(900)),
        "amortisation_schedule": (
            (1000, 0.1, [(1, 200), (2, 990)]),
            {},
            lambda r: close(0)(r[-1]["closing"]) and close(100)(r[0]["interest"]),
        ),
        "marginal_pd_from_cumulative": (
            ([0.1, 0.3],),
            {},
            lambda r: close(0.1)(r[0]) and close(0.2)(r[1]),
        ),
        "survival_from_pd": (([0.1, 0.2],), {}, lambda r: close(0.7)(r[-1])),
        "cumulative_pd_from_conditional": (([0.1, 0.2],), {}, lambda r: close(0.28)(r[-1])),
        "component_ecl": ((0.02, 100000, 0.4, 0.05, 1), {}, close(761.9047619047619)),
        "cash_shortfall_ecl": (([(1, 105)], [(2, 55.125)], 0.05), {}, close(50)),
        "modification_gain_loss": ((100, [(1, 99)], 0.1), {}, close(-10)),
        "hedge_ineffectiveness": ((100, -90), {}, close(10)),
        "ead_profile": (([100], [50], [0.4], [0.1]), {}, lambda r: r == [110]),
        "recovery_present_value": (([(2, 121)], 0.1), {}, close(100)),
        "lgd_from_recoveries": ((100, [(1, 55)], 0.1), {}, close(0.5)),
        "provision_matrix_ecl": ((1000, 0.03), {}, close(30)),
        "weighted_ecl": (
            ({"base": 10, "stress": 30}, {"base": 0.75, "stress": 0.25}),
            {},
            close(15),
        ),
        "poci_allowance_change": ((20, 30), {}, close(-10)),
        "liability_modification_test": ((100, 110), {}, field("substantial", True)),
        "coverage_ratio": ((20, 100), {}, close(0.2)),
        "assess_scope": ((inst,), {}, field("scope_decision", "IN_IFRS9_SCOPE")),
        "assess_recognition": ((inst,), {}, field("recognition_event", "RECOGNISED")),
        "assess_business_model": (("HOLD_TO_COLLECT",), {}, field("judgement_required", True)),
        "assess_sppi": ((features,), {}, field("sppi_pass", True)),
        "classify_instrument": ((inst, features), {}, field("classification", "AMORTISED_COST")),
        "assess_reclassification": (
            (inst, features),
            {},
            field("reclassification_status", "NO_RECLASSIFICATION"),
        ),
        "initial_measurement": (
            (
                dict(instrument_id="x", fair_value=100, transaction_costs=2, transaction_price=100),
                "AMORTISED_COST",
            ),
            {},
            field("initial_carrying_amount", 102),
        ),
        "present_fair_value": (
            (inst, {**market, "total_fv_change": 10}, "FVOCI_EQUITY"),
            {},
            field("oci_fv_change", 10),
        ),
        "split_own_credit": (
            (dict(instrument_id="x", total_fv_change=10, own_credit_change=4), "FVTPL_LIABILITY"),
            {},
            field("other_fv_change_pnl", 6),
        ),
        "interest_revenue": (
            (dict(instrument_id="x", gross_amount=100, eir=0.1), "STAGE_3", 20),
            {},
            field("interest_revenue", 8),
        ),
        "impairment_scope": ((inst,), {}, field("approach", "GENERAL")),
        "assess_stage": ((stage,), {}, field("stage", "STAGE_1")),
        "assess_sicr": (({**stage, "watchlist": True},), {}, field("sicr", True)),
        "stage_movements": (
            ([dict(prior_stage="STAGE_1", stage="STAGE_2")] * 2,),
            {},
            lambda r: r[0]["instruments"] == 2,
        ),
        "allocate_credit_enhancements": (
            (
                [
                    dict(
                        collateral_id="C",
                        instrument_id="x",
                        fair_value=100,
                        haircut=0.2,
                        cost=5,
                        allocated_amount=70,
                        recovery_year=2,
                    )
                ],
                simple,
            ),
            {},
            lambda r: r[0]["available_protection"] == 75,
        ),
        "scenario_ecl": (
            (cf, "STAGE_1", curve, lgd, ead, {"base": 1}),
            {},
            lambda r: close(761.9047619047619)(r[1]["final_ecl"]),
        ),
        "validate_overlay": ((overlay, "2026-12-31"), {}, field("status", "VALID")),
        "allocate_overlay": ((10, {"x": 0.3, "y": 0.7}), {}, lambda r: r == {"x": 3, "y": 7}),
        "reconcile_overlay": ((10, {"x": 3, "y": 7}), {}, field("status", "PASS")),
        "assess_derecognition": (
            (event("ASSET_TRANSFER", risks_rewards_transferred=True), source),
            {},
            field("derecognition_result", "FULL_DERECOGNITION"),
        ),
        "continuing_involvement": (
            (
                event("ASSET_TRANSFER", control_retained=True, continuing_involvement_amount=4),
                source,
            ),
            {},
            field("continuing_involvement", 4),
        ),
        "process_modification": (
            (event("ASSET_MODIFICATION_NO_DERECOGNITION", modified_present_value=90), source),
            {},
            field("pnl_effect", -10),
        ),
        "process_writeoff": (
            (event("WRITEOFF"), source),
            {},
            field("derecognition_result", "WRITEOFF"),
        ),
        "process_recovery": ((event("RECOVERY"), source), {}, field("pnl_effect", 10)),
        "validate_hedge_designation": ((hedge,), {}, field("eligible", True)),
        "assess_hedge_effectiveness": (
            ({**hedge, "hedge_type": "CASH_FLOW", "hedging_change": 80, "hedged_change": -100},),
            {},
            field("ineffectiveness_pnl", 0),
        ),
        "measure_hedge": (
            ({**hedge, "hedge_type": "CASH_FLOW", "hedging_change": 120, "hedged_change": -100},),
            {},
            field("ineffectiveness_pnl", 20),
        ),
        "oci_rollforward": (
            (10,),
            dict(fair_value_movement=5, recycling=2, basis_adjustment=1),
            field("closing_reserve", 12),
        ),
        "hedge_reserve_rollforward": (
            (
                10,
                [
                    dict(
                        oci_effective=5,
                        cost_of_hedging_reserve=3,
                        recycle_amount=2,
                        basis_adjustment=1,
                    )
                ],
            ),
            {},
            field("closing_reserve", 15),
        ),
        "build_journals": (
            (ecl, {"x": 5}, {"x": "AMORTISED_COST"}, simple),
            {},
            lambda r: len(r) == 2 and r[0]["debit"] == 15 and r[1]["credit"] == 15,
        ),
        "allowance_rollforward": (
            (simple, {"x": 5}, ecl, [], {"x": 1}),
            {},
            lambda r: r[0]["closing_allowance"] == 20 and r[0]["ecl_remeasurement"] == 15,
        ),
        "gross_rollforward": (
            (simple, {"x": 90}, [], {"x": 1}),
            {},
            lambda r: (
                r[0]["closing_gross"] == 100 and r[0]["other_contractual_and_fx_movements"] == 10
            ),
        ),
        "reconcile_ledger": ((100, 99), {}, field("status", "FAIL")),
        "disclosure_facts": (
            (simple, ecl, {"x": "AMORTISED_COST"}, {"x": "STAGE_1"}, {"x": 1}, "EUR"),
            {},
            lambda r: r[0]["net_carrying_amount"] == 80,
        ),
        "aggregate_disclosures": (
            (facts,),
            {},
            lambda r: len(r) == 6 and all(x["coverage_ratio"] == 0.2 for x in r),
        ),
        "scenario_sensitivity": (
            ({"base": 10, "stress": 30}, {"base": 0.75, "stress": 0.25}),
            {},
            lambda r: sum(x["weighted_contribution"] for x in r) == 15,
        ),
        "compare_challenger": (
            (
                [dict(model_type="PD", segment="X", mean_absolute_error=0.1, bias=0.02)],
                [dict(model_type="PD", segment="X", mean_absolute_error=0.05, bias=0.01)],
            ),
            {},
            lambda r: close(-0.05)(r[0]["mae_difference"]),
        ),
        "regulatory_bridge": (
            (simple, ecl, {"x": "STAGE_1"}, {"x": 1}),
            {},
            lambda r: (
                r[0]["difference"] == 5
                and not r[0]["accounting_value_used_in_regulatory_calculation"]
            ),
        ),
        "get_schema": (("instruments",), {}, lambda r: "instrument_id" in r["columns"]),
        "get_policy": ((), {}, field("past_due_sicr_days", 30)),
        "get_parameters": ((), {}, field("default_backstop_days", 90)),
        "get_formula": (("F-ECL-001",), {}, field("id", "F-ECL-001")),
        "get_sources": (
            (),
            {},
            lambda r: len(r) == 12 and all(x["redistributed"] is False for x in r),
        ),
        "list_profiles": ((), {}, lambda r: r == ("MID_SIZE_UNIVERSAL_FIA", "SMALL_SA_RETAIL_FIA")),
        "load_reference_data": (
            ("SMALL_SA_RETAIL_FIA",),
            {},
            lambda r: len(r) == 19 and len(r["instruments"]) == 5,
        ),
        "validate_dataset": ((data,), {}, lambda r: len(r["instruments"]) == 21),
        "select_snapshot": (
            ({"instruments": [inst]}, "2026-12-31", "2026-09-02T12:00:00+02:00"),
            {},
            lambda r: r["instruments"][0]["instrument_id"] == "U_MORT_01",
        ),
        "run_dataset": (
            (data,),
            {},
            lambda r: (
                r.status == "APPROVED_REFERENCE" and r.metrics["opening_gross_exposure"] == 5072000
            ),
        ),
        "get_metrics": ((result,), {}, field("opening_gross_exposure", 5072000)),
        "get_controls": (
            (result,),
            {},
            lambda r: len(r) == 28 and all(x["status"] == "PASS" for x in r),
        ),
        "get_table": ((result, "STAGING"), {}, lambda r: len(r) == 21),
        "get_lineage": ((result,), {}, field("contract_version", "1.1.0")),
        "export_profile": (
            ("SMALL_SA_RETAIL_FIA", workspace / "profile"),
            {},
            lambda r: len(list(r.glob("*.xlsx"))) == 19,
        ),
        "export_results": (
            (result, workspace / "results"),
            {},
            lambda r: len(list(r.glob("*.xlsx"))) == 7,
        ),
    }
    for name, kind in [
        ("backtest_pd", "PD"),
        ("backtest_lgd", "LGD"),
        ("backtest_ead", "EAD"),
        ("backtest_staging", "STAGING"),
    ]:
        obs = [
            dict(
                model_type=kind,
                model_version_id="v1",
                predicted_value=0.2,
                actual_value=0.1,
                model_owner="Risk",
                validation_status="VALIDATED",
                approval_id="A",
                exposure_weight=1,
                segment="X",
                outcome_flag=False,
            )
        ]
        c[name] = (
            (obs,),
            {},
            lambda r: (
                close(0.1)(r[0]["mean_absolute_error"]) and close(0.5)(r[0]["calibration_ratio"])
            ),
        )
    c["backtest_models"] = (
        (
            [
                dict(
                    model_type="CCF",
                    model_version_id="v1",
                    predicted_value=0.2,
                    actual_value=0.1,
                    model_owner="Risk",
                    validation_status="VALIDATED",
                    approval_id="A",
                    exposure_weight=1,
                    segment="X",
                )
            ],
        ),
        {},
        lambda r: close(0.1)(r[0]["mean_absolute_error"]),
    )
    c["assess_ibor_relief"] = (
        (False, "IBOR_PHASE2_POLICY_V1", "CASE_APPROVAL_1"),
        {},
        field("status", "CONTROLLED_INTERFACE"),
    )
    c["benchmark_ecl"] = (
        (10,),
        {},
        lambda r: close(7619.047619047619)(r["checksum"]) and r["peak_bytes"] > 0,
    )
    return c


def run_examples(workspace: Path):
    outputs = {}
    for name, (args, kwargs, check) in cases(workspace).items():
        value = getattr(f, name)(*args, **kwargs)
        assert check(value), (name, value)
        outputs[name] = value
    return outputs


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("workspace", type=Path)
    args = parser.parse_args()
    print(f"{len(run_examples(args.workspace))} checked analyst examples passed")
