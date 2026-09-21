"""Shared strict boundary checks; booleans are never monetary numbers."""

from __future__ import annotations

from functools import lru_cache, wraps
from math import isfinite
from typing import Callable, Mapping, ParamSpec, TypeVar

from ._resources import read_json
from .models import AccountingError, Row, Scalar


def number(
    value: object, name: str, minimum: float | None = None, maximum: float | None = None
) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value):
        raise AccountingError(f"{name}: finite numeric value required")
    result = float(value)
    if minimum is not None and result < minimum or maximum is not None and result > maximum:
        raise AccountingError(f"{name}: outside [{minimum}, {maximum}]")
    return result


@lru_cache(maxsize=1)
def _field_types() -> dict[str, str]:
    schema = read_json("schema.json")
    types: dict[str, str] = {}
    for table in schema.values():
        if not isinstance(table, dict):
            continue
        fields = table.get("fields", [])
        if not isinstance(fields, list):
            continue
        for field in fields:
            if isinstance(field, dict):
                types[str(field["field"])] = str(field["type"])
    for key in ("sicr_override", "sppi_override", "own_credit_oci_mismatch"):
        types[key] = "boolean"
    for key in (
        "rating_orig",
        "rating_current",
        "opening_gross",
        "opening_allowance",
        "opening_fvoci_reserve",
        "opening_hedge_reserve",
        "ledger_gross",
        "ledger_allowance",
        "prepayment_rate",
        "behavioural_horizon_years",
        "recovery_present_value",
        "workout_cost",
    ):
        types[key] = "number"
    return types


def row(value: Row, required: tuple[str, ...] = ()) -> dict[str, Scalar]:
    for key in required:
        if key not in value or value[key] is None or value[key] == "":
            raise AccountingError(f"Missing required field: {key}")
    for key, val in value.items():
        kind = _field_types().get(key)
        if val is not None and (isinstance(val, float) or kind == "number"):
            number(val, key)
        if val is not None and kind == "boolean" and type(val) is not bool:
            raise AccountingError(f"{key}: boolean required")
    return dict(value)


def weights(values: Mapping[str, float]) -> dict[str, float]:
    result = {key: number(val, key, 0, 1) for key, val in values.items()}
    if not result or abs(sum(result.values()) - 1) > 1e-9:
        raise AccountingError("Scenario probabilities must sum to one (absolute tolerance 1e-9)")
    return result


P = ParamSpec("P")
T = TypeVar("T")


def guard(function: Callable[P, T]) -> Callable[P, T]:
    @wraps(function)
    def wrapped(*args: P.args, **kwargs: P.kwargs) -> T:
        try:
            return function(*args, **kwargs)
        except AccountingError:
            raise
        except (KeyError, TypeError, ValueError, ArithmeticError) as exc:
            raise AccountingError(str(exc)) from exc

    return wrapped
