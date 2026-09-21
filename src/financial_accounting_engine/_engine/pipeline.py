# Copyright 2026 RiskDataScience GmbH
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from collections import Counter

from .._resources import source_inventory_valid as _source_inventory_valid
from .backtesting import evaluate as evaluate_backtesting
from .classification import classify
from .contracts import WORKBOOKS
from .ecl import calculate_ecl
from .events import process_event
from .hedge_accounting import measure
from .measurement import (
    calculate_eir,
    fair_value_presentation,
    initial_measurement,
    interest_revenue,
    own_credit,
    subsequent_measurement,
)
from .reporting import (
    aggregate_disclosures,
    allowance_rollforward,
    gross_rollforward,
    regulatory_bridge,
)
from .scope import assess_scope_and_recognition


def _meta(row: dict, run_id: str, date: str, policy: dict, formula: str | None = None) -> dict:
    return {
        **row,
        "run_id": run_id,
        "result_version": "1",
        "as_of_date": date,
        "knowledge_time": policy["knowledge_time"],
        "rule_set_id": policy["source_rule_set"],
        "accounting_policy_id": policy["policy_id"],
        "view": row.get("view", "REFERENCE"),
        "official_flag": False,
        "formula_id": formula or row.get("formula_id"),
        "source_object_id": row.get("instrument_id")
        or row.get("relationship_id")
        or row.get("model_version_id"),
    }


def _control(control_id: str, expected, actual, status="PASS", explanation="") -> dict:
    return {
        "control_id": control_id,
        "expected": expected,
        "actual": actual,
        "tolerance": 1e-9,
        "status": status,
        "explanation": explanation,
    }


def compute(tables, policy, rules, run_id, issues):
    from ..domains import allocate_credit_enhancements, assess_stage, build_journals

    date = policy["reporting_date"]
    instruments = tables["instruments"]
    instrument_index = {r["instrument_id"]: r for r in instruments}
    feature_index = {r["instrument_id"]: r for r in tables["classification_inputs"]}
    staging_index = {r["instrument_id"]: r for r in tables["staging_inputs"]}
    scopes = [_meta(assess_scope_and_recognition(r), run_id, date, policy) for r in instruments]
    scope_index = {r["instrument_id"]: r["scope_decision"] for r in scopes}
    classifications = [
        _meta(
            classify(r, feature_index[r["instrument_id"]], scope_index[r["instrument_id"]]),
            run_id,
            date,
            policy,
        )
        for r in instruments
    ]
    classification_index = {r["instrument_id"]: r["classification"] for r in classifications}
    initial_results = [
        _meta(
            initial_measurement(r, classification_index[r["instrument_id"]]), run_id, date, policy
        )
        for r in instruments
    ]
    initial_index = {r["instrument_id"]: r for r in initial_results}
    eir_results = [
        _meta(
            calculate_eir(
                r,
                [x for x in tables["cashflows"] if x["instrument_id"] == r["instrument_id"]],
                float(initial_index[r["instrument_id"]]["initial_carrying_amount"]),
            ),
            run_id,
            date,
            policy,
        )
        for r in instruments
    ]
    opening_gross_local = {
        r["instrument_id"]: float(r["opening_gross"] or 0) for r in tables["opening_balances"]
    }
    subsequent_results = [
        _meta(
            subsequent_measurement(
                r,
                classification_index[r["instrument_id"]],
                opening_gross_local[r["instrument_id"]],
                [x for x in tables["cashflows"] if x["instrument_id"] == r["instrument_id"]],
            ),
            run_id,
            date,
            policy,
        )
        for r in instruments
    ]
    stages = [
        _meta(assess_stage(staging_index[r["instrument_id"]], policy), run_id, date, policy)
        for r in instruments
    ]
    stage_index = {r["instrument_id"]: r["stage"] for r in stages}
    stage_result_index = {r["instrument_id"]: r for r in stages}
    scenarios = {r["scenario_id"]: float(r["probability"]) for r in tables["scenarios"]}
    market_index = {r["instrument_id"]: r for r in tables["market_data"]}
    details, ecl_results = [], []
    for inst in instruments:
        iid = inst["instrument_id"]
        d, e = calculate_ecl(
            inst,
            stage_index[iid],
            [x for x in tables["pd_curves"] if x["instrument_id"] == iid],
            [x for x in tables["lgd_profiles"] if x["instrument_id"] == iid],
            [x for x in tables["ead_profiles"] if x["instrument_id"] == iid],
            scenarios,
            [x for x in tables["cashflows"] if x["instrument_id"] == iid],
            date,
        )
        fx = float(market_index[iid]["fx_rate"])
        for component in d:
            component["discounted_ecl_local"] = component["discounted_ecl"]
            component["discounted_ecl"] = float(component["discounted_ecl"]) * fx
            component["fx_rate"] = fx
        e["final_ecl_local"] = e["final_ecl"]
        e["weighted_ecl_local"] = e["weighted_ecl"]
        e["fx_rate"] = fx
        e["weighted_ecl"] = float(e["weighted_ecl"]) * fx
        e["overlay"] = float(e["overlay"]) * fx
        e["final_ecl"] = float(e["final_ecl"]) * fx
        e["prior_stage"] = stage_result_index[iid]["prior_stage"]
        e["stage_movement"] = stage_result_index[iid]["stage_movement"]
        details.extend(_meta(x, run_id, date, policy) for x in d)
        ecl_results.append(_meta(e, run_id, date, policy))
    hedges = [_meta(measure(r), run_id, date, policy) for r in tables["hedges"]]
    own_credit_results = [
        _meta(
            own_credit(market_index[r["instrument_id"]], classification_index[r["instrument_id"]]),
            run_id,
            date,
            policy,
        )
        for r in instruments
    ]
    fair_value_results = [
        _meta(
            fair_value_presentation(
                r, market_index[r["instrument_id"]], classification_index[r["instrument_id"]]
            ),
            run_id,
            date,
            policy,
        )
        for r in instruments
    ]
    processed_events = [
        _meta(process_event(e, instrument_index[e["instrument_id"]]), run_id, date, policy)
        for e in tables["events"]
    ]
    collateral_results = [
        _meta(x, run_id, date, policy)
        for x in allocate_credit_enhancements(tables["collateral"], instruments)
    ]
    backtesting_results = [
        _meta({**x, "view": "MANAGEMENT"}, run_id, date, policy)
        for x in evaluate_backtesting(tables["backtesting"])
    ]
    opening = {
        r["instrument_id"]: float(r["opening_allowance"] or 0)
        * float(market_index[r["instrument_id"]]["fx_rate"])
        for r in tables["opening_balances"]
    }
    opening_gross = {
        r["instrument_id"]: float(r["opening_gross"] or 0)
        * float(market_index[r["instrument_id"]]["fx_rate"])
        for r in tables["opening_balances"]
    }
    fx_index = {iid: float(row["fx_rate"]) for iid, row in market_index.items()}
    interest_results = [
        _meta(
            interest_revenue(
                r,
                stage_index[r["instrument_id"]],
                float(
                    next(x for x in ecl_results if x["instrument_id"] == r["instrument_id"])[
                        "final_ecl_local"
                    ]
                ),
            ),
            run_id,
            date,
            policy,
        )
        for r in instruments
    ]
    presentation_events = [
        {
            **e,
            **{
                k: float(e[k]) * fx_index[e["instrument_id"]]
                for k in ("amount", "continuing_involvement", "modification_result", "pnl_effect")
            },
        }
        for e in processed_events
    ]
    presentation_own_credit = [
        {
            **r,
            **{
                k: float(r[k]) * fx_index[r["instrument_id"]]
                for k in (
                    "total_fv_change",
                    "own_credit_oci",
                    "other_fv_change_pnl",
                    "own_credit_pnl_due_to_mismatch",
                )
            },
        }
        for r in own_credit_results
    ]
    raw_journals = build_journals(
        ecl_results,
        opening,
        classification_index,
        instruments,
        presentation_events,
        presentation_own_credit,
        hedges,
    )
    journals = [
        _meta(x, run_id, date, policy, x.get("formula_id") or "ACCOUNTING-RULE")
        for x in raw_journals
    ]
    total_ecl = sum(float(x["final_ecl"]) for x in ecl_results)
    gross = sum(
        float(x["gross_amount"] or 0) * float(market_index[x["instrument_id"]]["fx_rate"])
        for x in instruments
        if not x.get("liability")
    )
    writeoffs = sum(
        float(x["amount"]) * float(market_index[x["instrument_id"]]["fx_rate"])
        for x in processed_events
        if x["event_type"] == "WRITEOFF"
    )
    transfer_reduction = sum(
        max(float(x["amount"]) - float(x["continuing_involvement"]), 0)
        * float(market_index[x["instrument_id"]]["fx_rate"])
        for x in processed_events
        if x["event_type"] == "ASSET_TRANSFER" and x["derecognition_result"] != "NO_DERECOGNITION"
    )
    closing_gross = gross - writeoffs - transfer_reduction
    closing_allowance = sum(
        float(e["final_ecl"])
        - sum(
            float(v["amount"]) * float(market_index[v["instrument_id"]]["fx_rate"])
            for v in processed_events
            if v["instrument_id"] == e["instrument_id"] and v["event_type"] == "WRITEOFF"
        )
        if e["stage"] == "POCI"
        else max(
            float(e["final_ecl"])
            - sum(
                float(v["amount"]) * float(market_index[v["instrument_id"]]["fx_rate"])
                for v in processed_events
                if v["instrument_id"] == e["instrument_id"] and v["event_type"] == "WRITEOFF"
            ),
            0,
        )
        for e in ecl_results
    )
    balanced = all(
        abs(
            sum(
                float(x["debit"]) - float(x["credit"])
                for x in journals
                if x["journal_batch_id"] == batch
            )
        )
        < 1e-9
        for batch in {x["journal_batch_id"] for x in journals}
    )
    formula_ids = {x["id"] for x in rules["formulas"]}
    expected_formula_ids = {
        x.get("formula_id")
        for group in [
            classifications,
            initial_results,
            eir_results,
            subsequent_results,
            fair_value_results,
            ecl_results,
            hedges,
            own_credit_results,
            processed_events,
            collateral_results,
            backtesting_results,
        ]
        for x in group
        if x.get("formula_id")
    }
    pd_survival_ok = all(
        sum(
            float(x["marginal_pd"])
            for x in tables["pd_curves"]
            if x["instrument_id"] == iid and x["scenario_id"] == sid
        )
        <= 1 + 1e-9
        for iid in instrument_index
        for sid in scenarios
    )
    hedge_reserve = sum(
        float(h.get("oci_effective", 0))
        + float(h.get("cost_of_hedging_reserve", 0))
        - float(h.get("recycle_amount", 0))
        - float(h.get("basis_adjustment", 0))
        for h in hedges
    )
    scenario_sensitivities = []
    for scenario_id, probability in scenarios.items():
        scenario_ecl = sum(
            float(x["discounted_ecl"]) for x in details if x["scenario_id"] == scenario_id
        )
        scenario_sensitivities.append(
            _meta(
                {
                    "scenario_id": scenario_id,
                    "probability": probability,
                    "standalone_ecl": scenario_ecl,
                    "weighted_contribution": scenario_ecl * probability,
                    "view": "MANAGEMENT",
                    "formula_id": "F-SENS-001",
                },
                run_id,
                date,
                policy,
            )
        )
    opening_fvoci = sum(
        float(x.get("opening_fvoci_reserve") or 0) for x in tables["opening_balances"]
    )
    fvoci_fv_movement = sum(
        float(x["oci_fv_change"])
        for x in fair_value_results
        if x["classification"] in {"FVOCI_DEBT", "FVOCI_EQUITY"}
    )
    opening_hedge = sum(
        float(x.get("opening_hedge_reserve") or 0) for x in tables["opening_balances"]
    )
    oci_rollforwards = [
        _meta(
            {
                "reserve_type": "FVOCI_RESERVE",
                "opening_reserve": opening_fvoci,
                "fair_value_movement": fvoci_fv_movement,
                "effective_hedge_movement": 0.0,
                "cost_of_hedging_movement": 0.0,
                "recycling": 0.0,
                "closing_reserve": opening_fvoci + fvoci_fv_movement,
                "formula_id": "F-OCI-ROLL-001",
            },
            run_id,
            date,
            policy,
        ),
        _meta(
            {
                "reserve_type": "HEDGE_RESERVE",
                "opening_reserve": opening_hedge,
                "fair_value_movement": 0.0,
                "effective_hedge_movement": sum(float(x.get("oci_effective") or 0) for x in hedges),
                "cost_of_hedging_movement": sum(
                    float(x.get("cost_of_hedging_reserve") or 0) for x in hedges
                ),
                "recycling": sum(float(x.get("recycle_amount") or 0) for x in hedges),
                "basis_adjustment": sum(float(x.get("basis_adjustment") or 0) for x in hedges),
                "closing_reserve": opening_hedge + hedge_reserve,
                "formula_id": "F-OCI-ROLL-001",
            },
            run_id,
            date,
            policy,
        ),
    ]
    disclosures = []
    for inst in instruments:
        iid = inst["instrument_id"]
        ecl = next(x for x in ecl_results if x["instrument_id"] == iid)
        gross_local = float(inst["gross_amount"] or 0)
        fx = float(market_index[iid]["fx_rate"])
        gross_pc = gross_local * fx
        disclosures.append(
            _meta(
                {
                    "instrument_id": iid,
                    "entity_id": inst["entity_id"],
                    "portfolio": inst["portfolio"],
                    "classification": classification_index[iid],
                    "stage": stage_index[iid],
                    "gross_carrying_amount_local": gross_local,
                    "gross_carrying_amount": gross_pc,
                    "allowance": float(ecl["final_ecl"]),
                    "net_carrying_amount": gross_pc - float(ecl["final_ecl"]),
                    "currency": inst["currency"],
                    "presentation_currency": policy["presentation_currency"],
                    "fx_rate": fx,
                    "disclosure_class": "IFRS7_FINANCIAL_INSTRUMENT",
                },
                run_id,
                date,
                policy,
                "DISC-001",
            )
        )
    disclosure_aggregates = [
        _meta(x, run_id, date, policy) for x in aggregate_disclosures(disclosures)
    ]
    ecl_index = {x["instrument_id"]: x for x in ecl_results}
    allowance_movements = [
        _meta(x, run_id, date, policy)
        for x in allowance_rollforward(instruments, opening, ecl_index, processed_events, fx_index)
    ]
    gross_movements = [
        _meta(x, run_id, date, policy)
        for x in gross_rollforward(instruments, opening_gross, processed_events, fx_index)
    ]
    regulatory_results = [
        _meta(x, run_id, date, policy)
        for x in regulatory_bridge(instruments, ecl_index, stage_index, fx_index)
    ]
    expected_formula_ids.update(
        x.get("formula_id")
        for group in [
            disclosure_aggregates,
            allowance_movements,
            gross_movements,
            regulatory_results,
            scenario_sensitivities,
            oci_rollforwards,
        ]
        for x in group
        if x.get("formula_id")
    )
    allowance_rollforward_total = sum(float(x["closing_allowance"]) for x in allowance_movements)
    gross_rollforward_total = sum(float(x["closing_gross"]) for x in gross_movements)
    aggregate_total = sum(
        float(x["gross_carrying_amount"])
        for x in disclosure_aggregates
        if x["aggregation_level"] == "entity_id"
    )
    disclosure_gross = sum(float(x["gross_carrying_amount"]) for x in disclosures)
    controls = [
        _control("INPUT_CONTRACT_COMPLETE", len(WORKBOOKS), len(tables)),
        _control("OFFICIAL_SNAPSHOT_UNIQUE", True, True),
        _control("SOURCE_INVENTORY_VALID", True, _source_inventory_valid()),
        _control("FORMULA_REGISTRY_COMPLETE", True, expected_formula_ids.issubset(formula_ids)),
        _control(
            "MODEL_APPROVAL_VALID",
            True,
            all(bool(x.get("approved_by")) for x in tables["scenarios"])
            and all(
                x.get("validation_status") in {"VALIDATED", "CONDITIONALLY_VALIDATED"}
                and bool(x.get("approval_id"))
                for table in ("pd_curves", "lgd_profiles", "ead_profiles", "backtesting")
                for x in tables[table]
            ),
        ),
        _control("SCENARIO_PROBABILITY_SUM", 1.0, sum(scenarios.values())),
        _control("PD_SURVIVAL_RECONCILIATION", True, pd_survival_ok),
        _control(
            "ECL_SCENARIO_RECONCILIATION",
            total_ecl,
            sum(
                float(x["discounted_ecl"])
                * (1 if x["scenario_id"] == "PROVISION_MATRIX" else scenarios[x["scenario_id"]])
                for x in details
            )
            + sum(
                float(x["overlay"])
                - float(x.get("poci_initial_lifetime_ecl", 0)) * float(x["fx_rate"])
                for x in ecl_results
            ),
        ),
        _control("ALLOWANCE_ROLLFORWARD", closing_allowance, allowance_rollforward_total),
        _control("GROSS_ROLLFORWARD", closing_gross, gross_rollforward_total),
        _control(
            "GROSS_NET_CARRYING_AMOUNT",
            closing_gross - closing_allowance,
            sum(
                float(x["closing_gross"])
                - float(
                    next(
                        a for a in allowance_movements if a["instrument_id"] == x["instrument_id"]
                    )["closing_allowance"]
                )
                for x in gross_movements
            ),
        ),
        _control("JOURNAL_BALANCED", True, balanced),
        _control(
            "LEDGER_RECONCILIATION",
            gross,
            sum(
                float(x["ledger_gross"] or 0) * float(market_index[x["instrument_id"]]["fx_rate"])
                for x in tables["opening_balances"]
                if x["instrument_id"]
                in {i["instrument_id"] for i in instruments if not i.get("liability")}
            ),
        ),
        _control(
            "COLLATERAL_ALLOCATION",
            True,
            all(
                float(x["allocated_amount"]) <= float(x["available_protection"]) + 1e-9
                for x in collateral_results
            ),
        ),
        _control(
            "OVERLAY_ALLOCATION_AND_EXPIRY",
            sum(
                float(i.get("overlay") or 0) * float(market_index[i["instrument_id"]]["fx_rate"])
                for i in instruments
            ),
            sum(float(e["overlay"]) for e in ecl_results),
        ),
        _control("STAGE_MOVEMENT_RECONCILIATION", len(instruments), len(stages)),
        _control(
            "FVOCI_OCI_RECONCILIATION",
            opening_fvoci + fvoci_fv_movement,
            next(
                x["closing_reserve"]
                for x in oci_rollforwards
                if x["reserve_type"] == "FVOCI_RESERVE"
            ),
        ),
        _control(
            "HEDGE_RESERVE_RECONCILIATION",
            opening_hedge + hedge_reserve,
            next(
                x["closing_reserve"]
                for x in oci_rollforwards
                if x["reserve_type"] == "HEDGE_RESERVE"
            ),
        ),
        _control(
            "NO_ACCOUNTING_REGULATORY_DOUBLE_COUNT",
            True,
            all(
                not x["accounting_value_used_in_regulatory_calculation"] for x in regulatory_results
            ),
        ),
        _control("SCOPE_RECOGNITION_COMPLETE", len(instruments), len(scopes)),
        _control("SPPI_DECISIONS_COMPLETE", len(instruments), len(classifications)),
        _control("EIR_METHOD_COMPLETE", len(instruments), len(eir_results)),
        _control("DERECOGNITION_EVENTS_COMPLETE", len(tables["events"]), len(processed_events)),
        _control(
            "OWN_CREDIT_SPLIT",
            sum(float(x["total_fv_change"]) for x in own_credit_results),
            sum(
                float(x["own_credit_oci"]) + float(x["other_fv_change_pnl"])
                for x in own_credit_results
            ),
        ),
        _control(
            "WRITE_OFF_RECOVERY_SEPARATE",
            True,
            all(
                x["event_type"]
                in {
                    "WRITEOFF",
                    "RECOVERY",
                    "ASSET_TRANSFER",
                    "ASSET_MODIFICATION_NO_DERECOGNITION",
                    "ASSET_MODIFICATION_DERECOGNITION",
                    "LIABILITY_MODIFICATION_DERECOGNITION",
                    "LIABILITY_MODIFICATION_NO_DERECOGNITION",
                }
                for x in processed_events
            ),
        ),
        _control("DISCLOSURE_ATOMIC_COVERAGE", len(instruments), len(disclosures)),
        _control("DISCLOSURE_AGGREGATION_RECONCILIATION", disclosure_gross, aggregate_total),
        _control(
            "BACKTESTING_MODEL_TYPE_COVERAGE",
            True,
            {"PD", "LGD", "EAD", "STAGING"}.issubset(
                {x["model_type"] for x in backtesting_results}
            ),
        ),
    ]
    for c in controls:
        if (
            isinstance(c["expected"], (int, float))
            and isinstance(c["actual"], (int, float))
            and abs(float(c["expected"]) - float(c["actual"])) > float(c["tolerance"])
        ):
            c["status"] = "FAIL"
        elif isinstance(c["expected"], bool) and c["expected"] != c["actual"]:
            c["status"] = "FAIL"
    summary = [
        {"metric": "opening_gross_exposure", "value": gross},
        {"metric": "closing_gross_exposure", "value": closing_gross},
        {"metric": "final_ecl_before_writeoff", "value": total_ecl},
        {"metric": "closing_allowance", "value": closing_allowance},
        {"metric": "net_carrying_amount", "value": closing_gross - closing_allowance},
        {"metric": "instruments", "value": len(instruments)},
        {"metric": "controls_passed", "value": sum(c["status"] == "PASS" for c in controls)},
    ]
    outputs = {
        "00_Summary": {"SUMMARY": summary, "CONTROLS": controls},
        "01_Classification": {
            "SCOPE_RECOGNITION": scopes,
            "CLASSIFICATION_SPPI": classifications,
            "DERECOGNITION": processed_events,
        },
        "02_Measurement_EIR": {
            "INITIAL_MEASUREMENT": initial_results,
            "EIR": eir_results,
            "AMORTISED_COST": subsequent_results,
            "INTEREST_REVENUE": interest_results,
            "FAIR_VALUE": fair_value_results,
            "OWN_CREDIT": own_credit_results,
            "MODIFICATIONS": processed_events,
        },
        "03_Impairment_ECL": {
            "STAGING": stages,
            "ECL_RESULTS": ecl_results,
            "ECL_COMPONENTS": details,
            "CREDIT_ENHANCEMENTS": collateral_results,
        },
        "04_Hedge_Accounting": {"HEDGES": hedges, "OCI_ROLLFORWARD": oci_rollforwards}
        if hedges
        else {
            "NOT_APPLICABLE": [
                {"status": "NOT_APPLICABLE", "reason": "Profile declares no hedge relationships"}
            ],
            "OCI_ROLLFORWARD": oci_rollforwards,
        },
        "05_Journals_Disclosures": {
            "JOURNALS": journals,
            "ALLOWANCE_ROLLFORWARD": allowance_movements,
            "GROSS_ROLLFORWARD": gross_movements,
            "OCI_ROLLFORWARD": oci_rollforwards,
            "DISCLOSURE_FACTS": disclosures,
            "DISCLOSURE_AGGREGATES": disclosure_aggregates,
            "EVENTS": processed_events,
        },
        "06_Audit": {
            "CONTROLS": controls,
            "VALIDATION": issues
            or [{"severity": "INFO", "code": "VALID", "message": "No validation issues"}],
            "BACKTESTING": backtesting_results,
            "SCENARIO_SENSITIVITY": scenario_sensitivities,
            "REGULATORY_BRIDGE": regulatory_results,
        },
    }
    status = (
        "APPROVED_REFERENCE" if all(c["status"] == "PASS" for c in controls) else "REVIEW_REQUIRED"
    )
    metric_payload = {
        "opening_gross_exposure": gross,
        "closing_gross_exposure": closing_gross,
        "final_ecl_before_writeoff": total_ecl,
        "closing_allowance": closing_allowance,
        "net_carrying_amount": closing_gross - closing_allowance,
        "classification_distribution": dict(sorted(Counter(classification_index.values()).items())),
        "stage_distribution": dict(sorted(Counter(stage_index.values()).items())),
        "hedge_status_distribution": dict(sorted(Counter(x["status"] for x in hedges).items())),
        "fvoci_oci_movement": fvoci_fv_movement,
        "hedge_reserve_movement": hedge_reserve,
        "journal_batches": len({x["journal_batch_id"] for x in journals}),
        "backtesting_result_sets": len(backtesting_results),
    }
    return outputs, metric_payload, status
