"""Granular accounting decisions over canonical row/table mappings.

Input fields follow get_schema(). Output schemas are documented in docs/schemas.
Monetary inputs within one call use one currency unless explicit FX is supplied.
Approved judgements remain caller inputs; these functions do not infer approvals.
"""

from __future__ import annotations

from collections import Counter
from typing import Mapping, cast

from ._checks import guard, number, row, weights
from ._engine import (
    accounting,
    backtesting,
    classification,
    ecl,
    enhancements,
    events,
    hedge_accounting,
    measurement,
    reporting,
    scope,
    staging,
)
from .data import get_policy
from .models import AccountingError, JSONValue, Row, Table

__all__ = [
    "assess_scope",
    "assess_recognition",
    "assess_derecognition",
    "assess_business_model",
    "assess_sppi",
    "classify_instrument",
    "assess_reclassification",
    "initial_measurement",
    "present_fair_value",
    "split_own_credit",
    "interest_revenue",
    "impairment_scope",
    "assess_sicr",
    "assess_stage",
    "stage_movements",
    "allocate_credit_enhancements",
    "scenario_ecl",
    "validate_overlay",
    "allocate_overlay",
    "reconcile_overlay",
    "process_modification",
    "process_writeoff",
    "process_recovery",
    "continuing_involvement",
    "validate_hedge_designation",
    "assess_hedge_effectiveness",
    "measure_hedge",
    "hedge_reserve_rollforward",
    "build_journals",
    "allowance_rollforward",
    "gross_rollforward",
    "oci_rollforward",
    "reconcile_ledger",
    "disclosure_facts",
    "aggregate_disclosures",
    "backtest_pd",
    "backtest_lgd",
    "backtest_ead",
    "backtest_staging",
    "scenario_sensitivity",
    "compare_challenger",
    "regulatory_bridge",
]


def _rows(values: Table) -> list[dict[str, object]]:
    return [dict(row(v)) for v in values]


@guard
def assess_scope(instrument: Row) -> Row:
    """Scope/own-use/interface decision from approved canonical instrument facts."""
    return cast(
        Row,
        scope.assess_scope_and_recognition(
            row(
                instrument,
                ("instrument_id", "scope_assessment", "recognition_status", "trade_date_policy"),
            )
        ),
    )


@guard
def assess_recognition(instrument: Row) -> Row:
    """Recognition, regular-way policy and electronic-payment criteria decision."""
    return assess_scope(instrument)


@guard
def assess_business_model(model: str) -> Row:
    """Validate supplied portfolio judgement HTC/HTC&S/OTHER; no statistical inference."""
    if model not in {"HOLD_TO_COLLECT", "HOLD_TO_COLLECT_AND_SELL", "OTHER"}:
        raise AccountingError("Unknown business model")
    return dict(
        business_model=model, judgement_required=True, source_reference="IFRS9.4.1.1-B4.1.2"
    )


@guard
def assess_sppi(features: Row) -> Row:
    """SPPI decision from documented features; approved override requires approval_id."""
    result, reason = classification.assess_sppi(row(features))
    return dict(sppi_pass=bool(result), reason=str(reason), source_reference="IFRS9.4.1.2_B4.1")


@guard
def classify_instrument(
    instrument: Row, features: Row, scope_decision: str = "IN_IFRS9_SCOPE"
) -> Row:
    """Classify debt/equity/liabilities, hybrids, commitments and guarantees."""
    return cast(
        Row,
        classification.classify(
            row(instrument, ("instrument_id", "instrument_type")), row(features), scope_decision
        ),
    )


@guard
def assess_reclassification(instrument: Row, features: Row) -> Row:
    """Prospective reclassification flag; disallow liability/equity business-model changes."""
    result = classify_instrument(instrument, features)
    return {
        k: result[k]
        for k in ("instrument_id", "classification", "reclassification_status", "source_reference")
    }


@guard
def initial_measurement(instrument: Row, category: str) -> Row:
    """FV +/- transaction costs, or FV with costs expensed for FVTPL; local money."""
    return cast(
        Row,
        measurement.initial_measurement(
            row(
                instrument,
                ("instrument_id", "fair_value", "transaction_costs", "transaction_price"),
            ),
            category,
        ),
    )


@guard
def present_fair_value(instrument: Row, market: Row, category: str) -> Row:
    """Present supplied FV movement in profit/loss or OCI; valuation is a controlled input."""
    return cast(
        Row,
        measurement.fair_value_presentation(
            row(instrument, ("instrument_id",)),
            row(market, ("fair_value", "ifrs13_level", "valuation_model", "valuation_status")),
            category,
        ),
    )


@guard
def split_own_credit(market: Row, category: str) -> Row:
    """Split designated FVTPL liability change between OCI and P&L, including mismatch."""
    return cast(
        Row,
        measurement.own_credit(
            row(market, ("instrument_id", "total_fv_change", "own_credit_change")), category
        ),
    )


@guard
def interest_revenue(instrument: Row, stage: str, allowance: float) -> Row:
    """One-year interest: gross stage1/2, net stage3, credit-adjusted net POCI.

    Allowance must use the instrument's local currency; signed POCI changes allowed.
    """
    number(allowance, "allowance")
    return cast(
        Row,
        measurement.interest_revenue(
            row(instrument, ("instrument_id", "gross_amount", "eir")), stage, allowance
        ),
    )


@guard
def impairment_scope(instrument: Row) -> Row:
    """Explicit impairment approach; liabilities/equity are outside impairment scope."""
    i = row(instrument, ("instrument_id", "impairment_scope"))
    approach = (
        "NO_IMPAIRMENT_SCOPE"
        if i.get("liability") or i.get("equity") or i["impairment_scope"] == "NO_IMPAIRMENT_SCOPE"
        else "POCI"
        if i.get("poci")
        else "SIMPLIFIED_LIFETIME"
        if i.get("simplified")
        else "GENERAL"
    )
    return dict(instrument_id=i["instrument_id"], approach=approach)


@guard
def assess_stage(facts: Row, policy: Mapping[str, JSONValue] | None = None) -> Row:
    """Stage/POCI/simplified decision, prior movement and reasons using explicit policy.

    Default selects EU_FINANCIAL_INSTRUMENTS_2026_V1, never a floating latest policy.
    """
    p = dict(get_policy() if policy is None else policy)
    for key in (
        "reporting_date",
        "default_backstop_days",
        "past_due_sicr_days",
        "rating_notch_sicr",
        "absolute_lifetime_pd_sicr",
        "relative_lifetime_pd_sicr",
        "cure_months",
        "probation_months",
    ):
        if key not in p:
            raise AccountingError(f"Missing policy parameter: {key}")
    return cast(
        Row,
        staging.assess_stage(
            row(
                facts,
                (
                    "instrument_id",
                    "impairment_scope",
                    "days_past_due",
                    "rating_orig",
                    "rating_current",
                ),
            ),
            p,
        ),
    )


@guard
def assess_sicr(facts: Row, policy: Mapping[str, JSONValue] | None = None) -> Row:
    """SICR decision plus stage reason; credit impairment takes precedence over SICR."""
    result = assess_stage(facts, policy)
    return dict(
        instrument_id=result["instrument_id"],
        sicr=result["stage"] == "STAGE_2",
        stage=result["stage"],
        reason=result["stage_reason"],
    )


@guard
def stage_movements(stage_results: Table) -> list[Row]:
    """Count observed prior->current movements; no inference for absent instruments."""
    counts = Counter((str(r["prior_stage"]), str(r["stage"])) for r in stage_results)
    return [dict(prior_stage=a, stage=b, instruments=n) for (a, b), n in sorted(counts.items())]


@guard
def allocate_credit_enhancements(collateral: Table, instruments: Table) -> list[Row]:
    """Available protection after haircut/costs; reject over-allocation including pooled IDs."""
    index = {str(i["instrument_id"]): row(i) for i in instruments}
    totals: dict[str, float] = {}
    limits: dict[str, float] = {}
    for record in collateral:
        r = row(
            record,
            (
                "collateral_id",
                "instrument_id",
                "fair_value",
                "haircut",
                "cost",
                "allocated_amount",
                "recovery_year",
            ),
        )
        if str(r["instrument_id"]) not in index:
            raise AccountingError("Unknown collateral instrument")
        cid = str(r["collateral_id"])
        limit = max(
            number(r["fair_value"], "fair_value", 0) * (1 - number(r["haircut"], "haircut", 0, 1))
            - number(r["cost"], "cost", 0),
            0,
        )
        if cid in limits and limits[cid] != limit:
            raise AccountingError("Inconsistent shared collateral capacity")
        limits[cid] = limit
        totals[cid] = totals.get(cid, 0) + number(r["allocated_amount"], "allocated", 0)
        if totals[cid] > limit + 1e-9:
            raise AccountingError("Shared collateral over-allocation")
    return cast(list[Row], enhancements.assess_allocations(_rows(collateral), index))


@guard
def scenario_ecl(
    instrument: Row,
    stage: str,
    pd_curves: Table,
    lgd_profiles: Table,
    ead_profiles: Table,
    probabilities: Mapping[str, float],
    cashflows: Table = (),
    reporting_date: str | None = None,
) -> tuple[list[Row], Row]:
    """Scenario component/direct/provision ECL: (component rows, instrument summary).

    Curves need scenario_id/year keys and PD/LGD/EAD values; Stage1 selects default
    year1, lifetime selects every supplied year. Recovery timing belongs in LGD.
    POCI uses credit-adjusted EIR and signed change against initial lifetime ECL.
    """
    i = row(instrument, ("instrument_id", "impairment_scope"))
    if i.get("overlay") and reporting_date is None:
        raise AccountingError("Overlay requires reporting date")
    try:
        details, summary = ecl.calculate_ecl(
            i,
            stage,
            _rows(pd_curves),
            _rows(lgd_profiles),
            _rows(ead_profiles),
            weights(probabilities),
            _rows(cashflows),
            reporting_date,
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise AccountingError(str(exc)) from exc
    return cast(list[Row], details), cast(Row, summary)


@guard
def validate_overlay(overlay: Row, reporting_date: str) -> Row:
    """Check ownership, approval, thesis, expiry and double-count review for an overlay."""
    from datetime import date

    o = row(
        overlay,
        (
            "overlay_id",
            "overlay_owner",
            "overlay_approved",
            "overlay_expiry",
            "overlay_thesis",
            "overlay_double_count_checked",
            "overlay",
        ),
    )
    number(o["overlay"], "overlay")
    if (
        o["overlay_approved"] is not True
        or o["overlay_double_count_checked"] is not True
        or date.fromisoformat(str(o["overlay_expiry"])) < date.fromisoformat(reporting_date)
    ):
        raise AccountingError("Overlay not approved/current or double-count review missing")
    return dict(overlay_id=o["overlay_id"], amount=o["overlay"], status="VALID")


@guard
def allocate_overlay(amount: float, allocation_weights: Mapping[str, float]) -> dict[str, float]:
    """Allocate a governed signed amount to explicit population weights summing to one."""
    a = number(amount, "amount")
    w = weights(allocation_weights)
    return {k: a * v for k, v in w.items()}


@guard
def reconcile_overlay(
    amount: float, allocations: Mapping[str, float], tolerance: float = 1e-9
) -> Row:
    """Control signed overlay allocation total against approved amount; no mutation."""
    return reconcile_ledger(
        number(amount, "amount"), sum(number(v, k) for k, v in allocations.items()), tolerance
    )


def _event(event: Row, instrument: Row, kinds: set[str]) -> Row:
    e = row(event, ("event_id", "instrument_id", "event_type", "approved", "reason_code"))
    if e["event_type"] not in kinds:
        raise AccountingError("Wrong event type for this function")
    if e["instrument_id"] != instrument.get("instrument_id"):
        raise AccountingError("Event/instrument key mismatch")
    return cast(Row, events.process_event(e, row(instrument, ("instrument_id", "gross_amount"))))


@guard
def assess_derecognition(event: Row, instrument: Row) -> Row:
    """Risk/reward/control transfer decision from approved contract-specific facts."""
    return _event(event, instrument, {"ASSET_TRANSFER"})


@guard
def continuing_involvement(event: Row, instrument: Row) -> Row:
    """Transfer decision with continuing-involvement amount, bounded by transferred amount."""
    r = assess_derecognition(event, instrument)
    if (
        not 0
        <= number(r["continuing_involvement"], "continuing involvement")
        <= number(r["amount"], "amount", 0)
    ):
        raise AccountingError("Continuing involvement outside transferred amount")
    return r


@guard
def process_modification(event: Row, instrument: Row) -> Row:
    """Approved asset/liability modification; PV inputs are supplied in local currency."""
    return _event(
        event,
        instrument,
        {
            "ASSET_MODIFICATION_NO_DERECOGNITION",
            "ASSET_MODIFICATION_DERECOGNITION",
            "LIABILITY_MODIFICATION_NO_DERECOGNITION",
            "LIABILITY_MODIFICATION_DERECOGNITION",
        },
    )


@guard
def process_writeoff(event: Row, instrument: Row) -> Row:
    """Approved writeoff of a nonnegative amount not exceeding gross carrying amount."""
    number(event.get("amount"), "amount", 0, number(instrument.get("gross_amount"), "gross", 0))
    return _event(event, instrument, {"WRITEOFF"})


@guard
def process_recovery(event: Row, instrument: Row) -> Row:
    """Approved post-writeoff recovery; positive recovery income, not new allowance."""
    number(event.get("amount"), "amount", 0)
    return _event(event, instrument, {"RECOVERY"})


@guard
def measure_hedge(relationship: Row) -> Row:
    """FV hedge residual or CF/NI lesser-of cumulative effective gain and P&L residual.

    Changes are cumulative since designation. Returns lifecycle status, OCI,
    ineffectiveness, costs, recycling and basis adjustment in one currency.
    """
    return cast(
        Row,
        hedge_accounting.measure(
            row(
                relationship,
                (
                    "relationship_id",
                    "hedge_type",
                    "hedging_change",
                    "hedged_change",
                    "hedge_ratio",
                    "target_hedge_ratio",
                ),
            )
        ),
    )


@guard
def validate_hedge_designation(relationship: Row) -> Row:
    """Return designation eligibility and lifecycle status from documented hedge facts."""
    r = measure_hedge(relationship)
    return dict(
        relationship_id=r["relationship_id"], eligible=r["status"] != "REJECTED", status=r["status"]
    )


@guard
def assess_hedge_effectiveness(relationship: Row) -> Row:
    """Economic relationship, credit dominance and ratio assessment plus measured residual."""
    return measure_hedge(relationship)


@guard
def oci_rollforward(
    opening: float,
    fair_value_movement: float = 0,
    effective_hedge_movement: float = 0,
    costs: float = 0,
    recycling: float = 0,
    basis_adjustment: float = 0,
) -> Row:
    """Signed OCI reserve: opening + FV + effective hedge + costs - recycling - basis."""
    values = [
        number(v, k)
        for k, v in [
            ("opening", opening),
            ("fair_value", fair_value_movement),
            ("hedge", effective_hedge_movement),
            ("costs", costs),
            ("recycling", recycling),
            ("basis", basis_adjustment),
        ]
    ]
    a, b, c, d, e, f = values
    return dict(
        opening_reserve=a,
        fair_value_movement=b,
        effective_hedge_movement=c,
        cost_of_hedging_movement=d,
        recycling=e,
        basis_adjustment=f,
        closing_reserve=a + b + c + d - e - f,
    )


@guard
def hedge_reserve_rollforward(opening: float, hedge_results: Table) -> Row:
    """Roll signed period hedge reserve movements including costs, recycling and basis adjustment."""

    def total(key: str) -> float:
        return sum(number(r.get(key), key) for r in hedge_results)

    return oci_rollforward(
        opening,
        effective_hedge_movement=total("oci_effective"),
        costs=total("cost_of_hedging_reserve"),
        recycling=total("recycle_amount"),
        basis_adjustment=total("basis_adjustment"),
    )


@guard
def build_journals(
    ecl_results: Table,
    opening_allowances: Mapping[str, float],
    classifications: Mapping[str, str],
    instruments: Table,
    processed_events: Table = (),
    own_credit_results: Table = (),
    hedge_results: Table = (),
) -> list[Row]:
    """Balanced ECL/event/own-credit/hedge reference journals; amounts in one currency.

    Own-credit rows are only booked for FVTPL liabilities. Institutional account
    mappings and posting approvals remain external; this never posts to a ledger.
    """
    idx = {str(i["instrument_id"]): row(i) for i in instruments}
    result = (
        accounting.allowance_journals(
            _rows(ecl_results), dict(opening_allowances), dict(classifications), idx
        )
        + accounting.event_journals(_rows(processed_events))
        + accounting.own_credit_journals(
            _rows(
                [
                    r
                    for r in own_credit_results
                    if classifications.get(str(r["instrument_id"])) == "FVTPL_LIABILITY"
                ]
            )
        )
        + accounting.hedge_journals(_rows(hedge_results))
    )
    for r in result:
        number(r["debit"], "debit", 0)
        number(r["credit"], "credit", 0)
    for key in {r["journal_batch_id"] for r in result}:
        if (
            abs(sum(r["debit"] - r["credit"] for r in result if r["journal_batch_id"] == key))
            > 1e-9
        ):
            raise AccountingError("Unbalanced journal batch")
    return cast(list[Row], result)


@guard
def allowance_rollforward(
    instruments: Table,
    opening: Mapping[str, float],
    ecl_results: Table,
    processed_events: Table,
    fx: Mapping[str, float],
) -> list[Row]:
    """Opening + target-minus-opening - writeoffs; signed POCI changes retained."""
    return cast(
        list[Row],
        reporting.allowance_rollforward(
            _rows(instruments),
            dict(opening),
            {str(r["instrument_id"]): row(r) for r in ecl_results},
            _rows(processed_events),
            dict(fx),
        ),
    )


@guard
def gross_rollforward(
    instruments: Table,
    opening: Mapping[str, float],
    processed_events: Table,
    fx: Mapping[str, float],
) -> list[Row]:
    """Gross movement bridge; other_contractual_and_fx_movements is an explicit residual.

    This explanatory bridge alone is not an independent ledger reconciliation.
    """
    return cast(
        list[Row],
        reporting.gross_rollforward(
            _rows(instruments), dict(opening), _rows(processed_events), dict(fx)
        ),
    )


@guard
def reconcile_ledger(expected: float, actual: float, tolerance: float = 1e-9) -> Row:
    """Independent scalar reconciliation in one unit; FAIL if absolute difference > tolerance."""
    e = number(expected, "expected")
    a = number(actual, "actual")
    t = number(tolerance, "tolerance", 0)
    return dict(
        expected=e,
        actual=a,
        difference=a - e,
        tolerance=t,
        status="PASS" if abs(a - e) <= t else "FAIL",
    )


@guard
def disclosure_facts(
    instruments: Table,
    ecl_results: Table,
    classifications: Mapping[str, str],
    stages: Mapping[str, str],
    fx: Mapping[str, float],
    presentation_currency: str,
) -> list[Row]:
    """Atomic gross/allowance/net disclosures; ECL inputs already in presentation currency."""
    index = {str(r["instrument_id"]): r for r in ecl_results}
    result: list[Row] = []
    for i in instruments:
        iid = str(i["instrument_id"])
        rate = number(fx[iid], "fx", 0)
        g = number(i["gross_amount"], "gross", 0) * rate
        a = number(index[iid]["final_ecl"], "ECL")
        result.append(
            dict(
                instrument_id=iid,
                entity_id=i["entity_id"],
                portfolio=i["portfolio"],
                classification=classifications[iid],
                stage=stages[iid],
                gross_carrying_amount=g,
                allowance=a,
                net_carrying_amount=g - a,
                currency=i["currency"],
                presentation_currency=presentation_currency,
                fx_rate=rate,
            )
        )
    return result


@guard
def aggregate_disclosures(facts: Table) -> list[Row]:
    """Group by entity/portfolio/category/stage/currency and combined dimensions.

    Coverage is sum(allowance)/sum(gross), never the sum of instrument ratios.
    All monetary facts must share one presentation currency.
    """
    if len({r.get("presentation_currency") for r in facts}) > 1:
        raise AccountingError("Mixed presentation currencies")
    return cast(list[Row], reporting.aggregate_disclosures(_rows(facts)))


def _backtest(observations: Table, model_type: str) -> list[Row]:
    return cast(
        list[Row],
        backtesting.evaluate(_rows([r for r in observations if r.get("model_type") == model_type])),
    )


@guard
def backtest_pd(observations: Table) -> list[Row]:
    """Approved PD observations: weighted calibration/bias/MAE and unweighted pairwise AUC."""
    return _backtest(observations, "PD")


@guard
def backtest_lgd(observations: Table) -> list[Row]:
    """Approved LGD observations: weighted predictions/outcomes, bias and MAE."""
    return _backtest(observations, "LGD")


@guard
def backtest_ead(observations: Table) -> list[Row]:
    """Approved EAD observations: exposure-weighted predictions/outcomes in money units."""
    return _backtest(observations, "EAD")


@guard
def backtest_staging(observations: Table) -> list[Row]:
    """Approved staging outcome monitoring, separate from accounting posting effects."""
    return _backtest(observations, "STAGING")


@guard
def scenario_sensitivity(
    losses: Mapping[str, float], probabilities: Mapping[str, float]
) -> list[Row]:
    """Standalone scenario losses and weighted contributions; management view only."""
    w = weights(probabilities)
    if set(w) != set(losses):
        raise AccountingError("Scenario keys differ")
    return [
        dict(
            scenario_id=k,
            standalone_ecl=number(losses[k], k, 0),
            probability=v,
            weighted_contribution=losses[k] * v,
            view="MANAGEMENT",
        )
        for k, v in w.items()
    ]


@guard
def compare_challenger(reference: Table, challenger: Table) -> list[Row]:
    """Match monitoring rows on model_type/segment and compare MAE and bias; no posting."""
    index = {(r["model_type"], r["segment"]): r for r in reference}
    result: list[Row] = []
    if len(index) != len(reference):
        raise AccountingError("Ambiguous reference model/segment")
    for r in challenger:
        key = (r["model_type"], r["segment"])
        if key not in index:
            raise AccountingError("Missing reference comparison group")
        result.append(
            dict(
                model_type=r["model_type"],
                segment=r["segment"],
                mae_difference=number(r["mean_absolute_error"], "MAE")
                - number(index[key]["mean_absolute_error"], "MAE"),
                bias_difference=number(r["bias"], "bias") - number(index[key]["bias"], "bias"),
                view="MANAGEMENT",
            )
        )
    return result


@guard
def regulatory_bridge(
    instruments: Table, ecl_results: Table, stages: Mapping[str, str], fx: Mapping[str, float]
) -> list[Row]:
    """Accounting ECL versus supplied regulatory EL, no capital calculation or feedback."""
    return cast(
        list[Row],
        reporting.regulatory_bridge(
            _rows(instruments),
            {str(r["instrument_id"]): row(r) for r in ecl_results},
            dict(stages),
            dict(fx),
        ),
    )


@guard
def backtest_models(observations: Table) -> list[Row]:
    """Monitor PD/LGD/EAD/CCF/STAGING/SCENARIO/OVERLAY including challengers.

    Positive exposure weights, owner, validation status and approval are required.
    This management analysis does not alter accounting estimates or post journals.
    """
    for r in observations:
        if r.get("model_type") not in {"PD", "LGD", "EAD", "CCF", "STAGING", "SCENARIO", "OVERLAY"}:
            raise AccountingError("Unknown monitoring model type")
    return cast(list[Row], backtesting.evaluate(_rows(observations)))


@guard
def assess_ibor_relief(applicable: bool, policy_reference: str, approval_reference: str) -> Row:
    """Record an externally approved IBOR applicability judgement (controlled interface).

    No automatic relief, EIR reset or hedge continuation is inferred. The institution
    supplies the applicable reform phase, policy and case approval in the references.
    Returns applicability, references and CONTROLLED_INTERFACE status.
    """
    if (
        type(applicable) is not bool
        or not policy_reference.strip()
        or not approval_reference.strip()
    ):
        raise AccountingError("Explicit applicability, policy and approval required")
    return dict(
        applicable=applicable,
        policy_reference=policy_reference,
        approval_reference=approval_reference,
        status="CONTROLLED_INTERFACE",
        source_reference="IFRS9.6.8-6.9_5.4.5-5.4.9",
    )


__all__ += ["backtest_models", "assess_ibor_relief"]
