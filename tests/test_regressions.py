import copy
import math

import pytest
from hypothesis import given
from hypothesis import strategies as st

import financial_accounting_engine as f


@pytest.fixture
def data():
    return f.load_reference_data("MID_SIZE_UNIVERSAL_FIA")


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), float("-inf"), None, True, "0.05"])
def test_nonfinite_and_wrong_types_rejected(bad):
    with pytest.raises(f.AccountingError):
        f.discount_factor(bad, 1)
    with pytest.raises(f.AccountingError):
        f.component_ecl(0.02, bad, 0.4, 0.05, 1)


@pytest.mark.parametrize("rate", [-0.1, 0, 0.1])
def test_eir_positive_zero_negative(rate):
    assert f.effective_interest_rate(100, [(1, 100 * (1 + rate))]) == pytest.approx(rate, abs=1e-10)


def test_eir_missing_or_unbracketed():
    for flows in ([], [(1, 2000)], [(1, -10)], [(0, 100)]):
        with pytest.raises(f.AccountingError):
            f.effective_interest_rate(100, flows)


@given(
    st.floats(min_value=0, max_value=1),
    st.floats(min_value=0, max_value=1),
    st.floats(min_value=0, max_value=1e8),
)
def test_component_bounds(pd, lgd, ead):
    assert 0 <= f.component_ecl(pd, ead, lgd, 0, 1) <= ead + 1e-7


@given(st.lists(st.floats(min_value=0, max_value=1), max_size=20))
def test_conditional_survival_invariants(curve):
    cumulative = f.cumulative_pd_from_conditional(curve)
    marginal = f.marginal_pd_from_cumulative(cumulative)
    survival = f.survival_from_pd(marginal)
    assert all(a <= b for a, b in zip(cumulative, cumulative[1:]))
    assert all(math.isclose(s, 1 - c, abs_tol=1e-12) for s, c in zip(survival, cumulative))


@pytest.mark.parametrize(
    "days,expected", [(29, "STAGE_1"), (30, "STAGE_2"), (89, "STAGE_2"), (90, "STAGE_3")]
)
def test_stage_boundaries(data, days, expected):
    assert f.assess_stage({**data["staging_inputs"][0], "days_past_due": days})["stage"] == expected


def test_zero_cure_and_expired_rebuttal(data):
    row = data["staging_inputs"][0]
    assert f.assess_stage({**row, "months_since_cure": 0})["stage"] == "STAGE_2"
    assert f.assess_stage({**row, "months_since_forbearance": 0})["stage"] == "STAGE_2"
    with pytest.raises(f.AccountingError):
        f.assess_stage(
            {
                **row,
                "days_past_due": 30,
                "sicr_rebuttal": True,
                "override_approved": True,
                "override_reason": "Approved judgement",
                "override_expiry": "2026-01-01",
            }
        )
    policy = f.get_policy()
    del policy["relative_lifetime_pd_sicr"]
    with pytest.raises(f.AccountingError):
        f.assess_stage(row, policy)


def test_de_minimis_does_not_override_leverage(data):
    assert (
        f.assess_sppi(
            {
                **data["classification_inputs"][0],
                "de_minimis_or_non_genuine": True,
                "leverage": True,
            }
        )["sppi_pass"]
        is False
    )


def test_trading_equity_no_fvoci_election(data):
    with pytest.raises(f.AccountingError):
        f.classify_instrument(
            {
                **data["instruments"][0],
                "equity": True,
                "held_for_trading": True,
                "fvoci_equity_election": True,
                "designation_approval_id": "A",
            },
            data["classification_inputs"][0],
        )


@pytest.mark.parametrize(
    "gain,item,oci,pnl",
    [
        (80, -100, 80, 0),
        (120, -100, 100, 20),
        (-80, 100, -80, 0),
        (-120, 100, -100, -20),
        (80, 100, 0, 80),
    ],
)
@pytest.mark.parametrize("kind", ["CASH_FLOW", "NET_INVESTMENT"])
def test_hedge_lower_of(data, gain, item, oci, pnl, kind):
    r = f.measure_hedge(
        {**data["hedges"][0], "hedge_type": kind, "hedging_change": gain, "hedged_change": item}
    )
    assert r["oci_effective"] == oci
    assert r["ineffectiveness_pnl"] == pnl


def test_poci_negative_change_credit_adjusted_rate(data):
    i = next(x for x in data["instruments"] if x["poci"])
    i = {**i, "poci_initial_lifetime_ecl": 30, "eir": 0.9, "credit_adjusted_eir": 0.1, "overlay": 0}
    details, summary = f.scenario_ecl(
        i,
        "POCI",
        [dict(scenario_id="s", year=1, marginal_pd=0.1)],
        [dict(scenario_id="s", year=1, lgd=1)],
        [dict(scenario_id="s", year=1, ead=110)],
        {"s": 1},
    )
    assert details[0]["discounted_ecl"] == pytest.approx(10)
    assert summary["final_ecl"] == pytest.approx(-20)


def test_default_horizon_not_recovery_horizon():
    assert f.cash_shortfall_ecl([(1, 100)], [(3, 50)], 0) == 50
    assert f.weighted_ecl({"a": 1, "b": 999}, {"a": 1, "b": 0}) == 1
    with pytest.raises(f.AccountingError):
        f.weighted_ecl({"a": 1}, {"a": 0.9})


def test_dataset_mutation_and_official_block(data):
    before = copy.deepcopy(data)
    f.run_dataset(data)
    assert data == before
    data["run_control"][0]["view"] = "OFFICIAL"
    with pytest.raises(f.ValidationError):
        f.run_dataset(data)


def test_snapshot_overlap_and_history(data):
    row = data["instruments"][0]
    later = {
        **row,
        "record_id": "REC-LATER",
        "known_from": "2026-10-01T00:00:00+00:00",
        "gross_amount": 123,
    }
    earlier = {**row, "known_to": "2026-09-30T23:59:59+00:00"}
    assert (
        f.select_snapshot({"i": [earlier, later]}, "2026-12-31", "2026-09-02T12:00:00+02:00")["i"][
            0
        ]["gross_amount"]
        == row["gross_amount"]
    )
    assert (
        f.select_snapshot({"i": [earlier, later]}, "2026-12-31", "2026-10-02T00:00:00+00:00")["i"][
            0
        ]["gross_amount"]
        == 123
    )
    with pytest.raises(f.ValidationError):
        f.select_snapshot({"i": [row, row]}, "2026-12-31", "2026-10-02T00:00:00+00:00")


def test_duplicate_curves_fail(data):
    data["pd_curves"].append({**data["pd_curves"][0], "record_id": "R2", "business_key": "B2"})
    with pytest.raises(f.ValidationError):
        f.run_dataset(data)


@pytest.mark.parametrize("field,value", [("gross_amount", float("nan")), ("liability", "False")])
def test_bad_dataset_cells(data, field, value):
    data["instruments"][0][field] = value
    with pytest.raises(f.ValidationError):
        f.run_dataset(data)


def test_zero_weight_not_silently_one():
    r = dict(
        model_type="PD",
        model_version_id="V",
        model_owner="R",
        approval_id="A",
        validation_status="VALIDATED",
        predicted_value=0.1,
        actual_value=0.2,
        exposure_weight=0,
    )
    with pytest.raises(f.AccountingError):
        f.backtest_pd([r])


def test_export_seal_and_readonly_workflow(tmp_path):
    root = f.export_profile("SMALL_SA_RETAIL_FIA", tmp_path / "inputs")
    before = {p.name: p.read_bytes() for p in root.iterdir()}
    result = f.run_dataset(root)
    assert result.status == "APPROVED_REFERENCE"
    assert before == {p.name: p.read_bytes() for p in root.iterdir()}
    with pytest.raises(f.ResourceError):
        f.export_profile("SMALL_SA_RETAIL_FIA", root)
    path = next(root.glob("*.xlsx"))
    path.write_bytes(path.read_bytes() + b"corruption")
    with pytest.raises(f.ValidationError):
        f.run_dataset(root)


def test_opening_allowance_not_double_counted(data):
    for row in data["opening_balances"]:
        row["opening_allowance"] = 100
    r = f.run_dataset(data)
    assert r.metrics["closing_allowance"] == pytest.approx(
        sum(x["closing_allowance"] for x in f.get_table(r, "ALLOWANCE_ROLLFORWARD"))
    )


def test_fx_net_interest_uses_local_allowance(data):
    i = next(r for r in data["staging_inputs"] if r["credit_impaired"])
    iid = i["instrument_id"]
    next(r for r in data["market_data"] if r["instrument_id"] == iid)["fx_rate"] = 2
    result = f.run_dataset(data)
    interest = next(r for r in f.get_table(result, "INTEREST_REVENUE") if r["instrument_id"] == iid)
    loss = next(r for r in f.get_table(result, "ECL_RESULTS") if r["instrument_id"] == iid)
    inst = next(r for r in data["instruments"] if r["instrument_id"] == iid)
    assert interest["interest_basis"] == pytest.approx(
        max(inst["gross_amount"] - loss["final_ecl_local"], 0)
    )


def test_absolute_sicr_from_zero_baseline(data):
    facts = {**data["staging_inputs"][0], "lifetime_pd_orig": 0, "lifetime_pd_current": 0.06}
    assert f.assess_stage(facts)["stage"] == "STAGE_2"


def test_negative_own_credit_and_offsetting_components():
    inst = [dict(instrument_id="x", instrument_type="BOND")]
    for own, total in [(-4, -10), (4, 0)]:
        split = f.split_own_credit(
            dict(instrument_id="x", own_credit_change=own, total_fv_change=total), "FVTPL_LIABILITY"
        )
        journals = f.build_journals(
            [], {}, {"x": "FVTPL_LIABILITY"}, inst, own_credit_results=[split]
        )
        assert journals and all(r["debit"] >= 0 and r["credit"] >= 0 for r in journals)
        assert sum(r["debit"] - r["credit"] for r in journals) == 0
    assert f.build_journals([], {}, {"x": "FVTPL"}, inst, own_credit_results=[split]) == []


def test_hedge_gain_credit_and_reserve_recycling(data):
    h = f.measure_hedge(
        {
            **data["hedges"][0],
            "hedge_type": "CASH_FLOW",
            "hedging_change": 120,
            "hedged_change": -100,
            "recycle_amount": 10,
            "basis_adjustment": 5,
        }
    )
    rows = f.build_journals([], {}, {}, [], hedge_results=[h])
    gain = next(r for r in rows if r["account"] == "HEDGE_INEFFECTIVENESS_PNL")
    assert gain["credit"] == 20 and gain["debit"] == 0
    assert sum(r["debit"] - r["credit"] for r in rows) == 0
    assert any(r["account"] == "HEDGE_RECYCLING_PNL" and r["credit"] == 10 for r in rows)
    assert any(r["account"] == "NONFINANCIAL_ASSET_BASIS" and r["credit"] == 5 for r in rows)


def test_poci_direct_shortfall_signed():
    i = dict(
        instrument_id="x",
        impairment_scope="GENERAL_ECL",
        ecl_method="DIRECT_CASH_SHORTFALL",
        credit_adjusted_eir=0,
        eir=0.1,
        poci_initial_lifetime_ecl=30,
        overlay=0,
    )
    flows = [
        dict(contractual=True, expected=False, year_fraction=1, amount=100),
        dict(contractual=False, expected=True, scenario_id="s", year_fraction=2, amount=80),
    ]
    _, r = f.scenario_ecl(i, "POCI", [], [], [], {"s": 1}, flows)
    assert r["final_ecl"] == -10


def test_result_cannot_be_official():
    with pytest.raises(f.AccountingError):
        f.AnalysisResult({}, {}, {}, "OFFICIAL", True)


def test_policy_input_parameter_conflict(data):
    next(r for r in data["parameters"] if r["parameter_id"] == "past_due_sicr_days")[
        "parameter_value"
    ] = "29"
    with pytest.raises(f.AccountingError):
        f.run_dataset(data)


def test_zero_weight_negative_or_duplicate_scenarios(data):
    i = data["instruments"][0]
    pd = [dict(scenario_id="s", year=1, marginal_pd=0.1)]
    lgd = [dict(scenario_id="s", year=1, lgd=0.4)]
    ead = [dict(scenario_id="s", year=1, ead=100)]
    with pytest.raises(f.AccountingError):
        f.scenario_ecl(i, "STAGE_1", pd * 2, lgd, ead, {"s": 1})
    with pytest.raises(f.AccountingError):
        f.scenario_ecl(i, "STAGE_1", pd, lgd, [], {"s": 1})
    with pytest.raises(f.AccountingError):
        f.scenario_ecl(i, "STAGE_1", pd, lgd, ead, {"s": -1, "t": 2})


def test_shared_collateral_not_double_allocated():
    collateral = [
        dict(
            collateral_id="same",
            instrument_id=i,
            fair_value=100,
            haircut=0,
            cost=0,
            allocated_amount=60,
            recovery_year=1,
        )
        for i in ("a", "b")
    ]
    with pytest.raises(f.AccountingError):
        f.allocate_credit_enhancements(
            collateral, [dict(instrument_id="a"), dict(instrument_id="b")]
        )


def test_coverage_uses_weighted_population():
    facts = [
        dict(
            entity_id="E",
            portfolio="P",
            classification="AC",
            stage="STAGE_1",
            currency="EUR",
            presentation_currency="EUR",
            gross_carrying_amount=g,
            allowance=a,
        )
        for g, a in [(100, 10), (900, 180)]
    ]
    rows = f.aggregate_disclosures(facts)
    assert all(r["coverage_ratio"] == 0.19 for r in rows)
    assert f.coverage_ratio(0, 0) is None
