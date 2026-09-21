"""Pure scalar/curve calculations. Rates are decimals and time is in years.

Money values must use one currency throughout each call. No rounding is applied.
All inputs must be finite; None, NaN, infinity and booleans are rejected.
"""

from __future__ import annotations

from math import fsum
from typing import Mapping, Sequence

from ._checks import number, weights
from .models import AccountingError, Row

__all__ = [
    "discount_factor",
    "effective_interest_rate",
    "amortised_cost_step",
    "amortisation_schedule",
    "marginal_pd_from_cumulative",
    "survival_from_pd",
    "cumulative_pd_from_conditional",
    "component_ecl",
    "cash_shortfall_ecl",
    "modification_gain_loss",
    "hedge_ineffectiveness",
    "ead_profile",
    "recovery_present_value",
    "lgd_from_recoveries",
    "provision_matrix_ecl",
    "weighted_ecl",
    "poci_allowance_change",
    "liability_modification_test",
    "coverage_ratio",
]


def discount_factor(rate: float, year_fraction: float) -> float:
    """F-DF-001: annual compound discount factor (1 + rate)^(-years)."""
    r = number(rate, "rate")
    t = number(year_fraction, "year_fraction", 0)
    if r <= -1:
        raise AccountingError("rate must exceed -100%")
    try:
        return number((1 + r) ** (-t), "discount_factor", 0)
    except OverflowError as exc:
        raise AccountingError("Discount factor overflow") from exc


def effective_interest_rate(
    initial_net: float, cashflows: Sequence[tuple[float, float]], tolerance: float = 1e-12
) -> float:
    """F-EIR-001: solve positive receipts PV=initial_net by bracketed bisection.

    Cashflows are (years, receipts). All receipts nonnegative, at least one
    strictly positive after time zero. Root bracket [-0.999999, 10] is explicit;
    unbracketed/ambiguous cashflows raise AccountingError. Tolerance is relative
    PV error or absolute rate interval, with at most 250 iterations.
    """
    initial = number(initial_net, "initial_net", 0)
    tol = number(tolerance, "tolerance", 0, 1e-3)
    flows = [(number(t, "time", 0), number(v, "receipt", 0)) for t, v in cashflows]
    if initial == 0 or tol == 0 or not any(t > 0 and v > 0 for t, v in flows):
        raise AccountingError("Positive initial amount, tolerance and future receipts required")

    def npv(r: float) -> float:
        return fsum(v * discount_factor(r, t) for t, v in flows) - initial

    lo, hi = -0.999999, 10.0
    flo, fhi = npv(lo), npv(hi)
    if flo * fhi > 0:
        raise AccountingError("EIR root outside [-0.999999, 10]")
    for _ in range(250):
        mid = (lo + hi) / 2
        value = npv(mid)
        if abs(value) <= tol * max(1, initial) or hi - lo <= tol:
            return mid
        if flo * value <= 0:
            hi = mid
        else:
            lo, flo = mid, value
    raise AccountingError("EIR failed to converge")


def amortised_cost_step(
    opening: float, eir: float, time: float, cash_received: float, adjustment: float = 0.0
) -> float:
    """F-AC-001: opening + opening*eir*time + adjustment - receipt.

    Simple accrual within each supplied period, no implicit day-count conversion.
    Signed adjustments permitted; opening and receipts must be nonnegative.
    """
    o = number(opening, "opening", 0)
    r = number(eir, "eir")
    t = number(time, "time", 0)
    discount_factor(r, 0)
    return number(
        o
        + o * r * t
        + number(adjustment, "adjustment")
        - number(cash_received, "cash_received", 0),
        "closing",
    )


def amortisation_schedule(
    opening: float, eir: float, cashflows: Sequence[tuple[float, float]]
) -> list[Row]:
    """Apply amortised_cost_step at strictly increasing cumulative year fractions.

    Rows: time, opening, interest, cash_received, closing, in input currency.
    Overpayment leaving a negative closing balance is rejected.
    """
    balance = number(opening, "opening", 0)
    prior = 0.0
    result: list[Row] = []
    for time, cash in cashflows:
        if number(time, "time", 0) <= prior:
            raise AccountingError("Times must increase strictly")
        closing = amortised_cost_step(balance, eir, time - prior, cash)
        if closing < -1e-9:
            raise AccountingError("Schedule overpayment")
        result.append(
            dict(
                time=time,
                opening=balance,
                interest=balance * eir * (time - prior),
                cash_received=cash,
                closing=closing,
            )
        )
        prior, balance = time, max(closing, 0)
    return result


def marginal_pd_from_cumulative(cumulative: Sequence[float]) -> list[float]:
    """Unconditional marginal PDs from a nondecreasing cumulative default curve."""
    result = []
    prior = 0.0
    for value in cumulative:
        current = number(value, "cumulative PD", prior, 1)
        result.append(current - prior)
        prior = current
    return result


def survival_from_pd(marginal: Sequence[float]) -> list[float]:
    """End-period survival = 1 - cumulative unconditional marginal PD; [] -> []."""
    total = 0.0
    result = []
    for value in marginal:
        total += number(value, "marginal PD", 0, 1)
        if total > 1 + 1e-12:
            raise AccountingError("Marginal PD sum exceeds one")
        result.append(max(1 - total, 0))
    return result


def cumulative_pd_from_conditional(conditional: Sequence[float]) -> list[float]:
    """Cumulative PD = 1 - product(1 - conditional period PD)."""
    survival = 1.0
    result = []
    for value in conditional:
        survival *= 1 - number(value, "conditional PD", 0, 1)
        result.append(1 - survival)
    return result


def component_ecl(marginal_pd: float, ead: float, lgd: float, eir: float, year: float) -> float:
    """F-ECL-001: unconditional PD * EAD * LGD discounted to default time.

    LGD must already reflect recovery timing relative to default. Stage 1 limits
    default events to 12 months, not recoveries to 12 months.
    """
    return number(
        number(marginal_pd, "PD", 0, 1)
        * number(ead, "EAD", 0)
        * number(lgd, "LGD", 0, 1)
        * discount_factor(eir, year),
        "ECL",
        0,
    )


def recovery_present_value(recoveries: Sequence[tuple[float, float]], eir: float) -> float:
    """PV of nonnegative (years from valuation date, recovery receipt) pairs."""
    discount_factor(eir, 0)
    return number(
        fsum(number(v, "recovery", 0) * discount_factor(eir, t) for t, v in recoveries),
        "recovery PV",
        0,
    )


def cash_shortfall_ecl(
    contractual: Sequence[tuple[float, float]], expected: Sequence[tuple[float, float]], eir: float
) -> float:
    """F-CS-001: max(PV contractual - PV expected, 0); both sets required."""
    if not contractual or not expected:
        raise AccountingError(
            "Contractual and expected cashflows required; explicit zero recovery permitted"
        )
    return max(recovery_present_value(contractual, eir) - recovery_present_value(expected, eir), 0)


def modification_gain_loss(
    gross_before: float, modified_cashflows: Sequence[tuple[float, float]], original_eir: float
) -> float:
    """F-MOD-001: asset gain positive = revised PV - existing gross amount."""
    if not modified_cashflows:
        raise AccountingError("Modified cashflows required")
    return recovery_present_value(modified_cashflows, original_eir) - number(
        gross_before, "gross_before", 0
    )


def hedge_ineffectiveness(hedging_change: float, hedged_change: float) -> float:
    """F-HDG-001: fair-value hedge offset residual; signed gains are positive."""
    return number(
        number(hedging_change, "hedging_change") + number(hedged_change, "hedged_change"),
        "ineffectiveness",
    )


def ead_profile(
    drawn: Sequence[float],
    undrawn: Sequence[float],
    ccf: Sequence[float],
    prepayment: Sequence[float],
) -> list[float]:
    """Period EAD = drawn*(1-prepayment) + undrawn*CCF; equal vector lengths."""
    if len({len(drawn), len(undrawn), len(ccf), len(prepayment)}) != 1:
        raise AccountingError("EAD vectors must have equal lengths")
    return [
        number(d, "drawn", 0) * (1 - number(p, "prepayment", 0, 1))
        + number(u, "undrawn", 0) * number(c, "CCF", 0, 1)
        for d, u, c, p in zip(drawn, undrawn, ccf, prepayment)
    ]


def lgd_from_recoveries(
    ead: float,
    recoveries: Sequence[tuple[float, float]],
    eir: float,
    costs: Sequence[tuple[float, float]] = (),
) -> float:
    """LGD = clipped (EAD - PV recoveries + PV workout costs)/EAD, in [0,1]."""
    exposure = number(ead, "ead", 0)
    if exposure == 0:
        raise AccountingError("LGD undefined for zero EAD")
    return min(
        max(
            (
                exposure
                - recovery_present_value(recoveries, eir)
                + recovery_present_value(costs, eir)
            )
            / exposure,
            0,
        ),
        1,
    )


def provision_matrix_ecl(exposure: float, loss_rate: float) -> float:
    """F-PM-001: provision for one homogeneous segment, exposure * loss_rate."""
    return number(exposure, "exposure", 0) * number(loss_rate, "loss_rate", 0, 1)


def weighted_ecl(scenario_losses: Mapping[str, float], probabilities: Mapping[str, float]) -> float:
    """Weight separately computed nonnegative scenario losses; keys must match."""
    w = weights(probabilities)
    if set(w) != set(scenario_losses):
        raise AccountingError("Scenario keys differ")
    return number(
        fsum(number(scenario_losses[k], k, 0) * v for k, v in w.items()), "weighted ECL", 0
    )


def poci_allowance_change(current_lifetime_ecl: float, initial_lifetime_ecl: float) -> float:
    """IFRS9.5.5.13–14: signed lifetime ECL change, favourable changes negative."""
    return number(current_lifetime_ecl, "current ECL", 0) - number(
        initial_lifetime_ecl, "initial ECL", 0
    )


def liability_modification_test(
    original_present_value: float,
    modified_present_value: float,
    qualitative_substantial: bool = False,
    threshold: float = 0.10,
) -> Row:
    """IFRS9.B3.3.6: absolute PV difference/original >= threshold, or qualitative.

    Caller supplies PVs at original EIR including eligible lender/borrower fees.
    Result fields: ratio (decimal), substantial (bool), threshold (decimal).
    """
    old = number(original_present_value, "original PV", 0)
    new = number(modified_present_value, "modified PV", 0)
    limit = number(threshold, "threshold", 0, 1)
    if old == 0:
        raise AccountingError("Original PV must be positive")
    if type(qualitative_substantial) is not bool:
        raise AccountingError("Qualitative judgement must be boolean")
    ratio = abs(new - old) / old
    return dict(ratio=ratio, substantial=qualitative_substantial or ratio >= limit, threshold=limit)


def coverage_ratio(allowance: float, gross_exposure: float) -> float | None:
    """Allowance / gross exposure; zero denominator returns None, POCI may be signed."""
    a = number(allowance, "allowance")
    g = number(gross_exposure, "gross exposure", 0)
    return a / g if g else None


def benchmark_ecl(iterations: int = 10000) -> Row:
    """Run the fixed F-ECL-001 golden vector repeatedly; return timing and checksum.

    Iterations 1..1,000,000; elapsed_seconds is observational, not a performance SLA.
    Measures Python traced peak bytes in an isolated tracing session; refuses when
    tracing is already active so callers' profiling state is never disturbed.
    """
    import time
    import tracemalloc

    if type(iterations) is not int or not 1 <= iterations <= 1000000:
        raise AccountingError("iterations must be an integer in [1, 1000000]")
    if tracemalloc.is_tracing():
        raise AccountingError("Another memory tracing session is active")
    tracemalloc.start()
    try:
        start = time.perf_counter()
        checksum = fsum(component_ecl(0.02, 100000, 0.4, 0.05, 1) for _ in range(iterations))
        elapsed = time.perf_counter() - start
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    return dict(
        iterations=iterations,
        checksum=checksum,
        elapsed_seconds=elapsed,
        peak_bytes=peak,
        formula_id="F-ECL-001",
    )


__all__ += ["benchmark_ecl"]
