"""Independent hand calculations and complete corrected profile regression."""

from __future__ import annotations

import json
import math
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest

import financial_accounting_engine as fae
from financial_accounting_engine._resources import read_json

ROOT = Path(__file__).resolve().parents[1]
CASES = json.loads((ROOT / "tests/golden_cases.json").read_text(encoding="utf-8"))["cases"]


def _float(value: str) -> float:
    return float(Decimal(value))


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["id"])
def test_independent_formula_golden(case: dict[str, Any]) -> None:
    inputs = case["inputs"]
    if case["function"] == "effective_interest_rate":
        actual = fae.effective_interest_rate(
            _float(inputs["initial_net"]),
            [(_float(t), _float(v)) for t, v in inputs["cashflows"]],
        )
    elif case["function"] == "component_ecl":
        actual = fae.component_ecl(**{key: _float(value) for key, value in inputs.items()})
    elif case["function"] == "cumulative_pd_from_conditional":
        actual = fae.cumulative_pd_from_conditional(
            [_float(value) for value in inputs["conditional"]]
        )
    elif case["function"] == "lgd_from_recoveries":
        actual = fae.lgd_from_recoveries(
            _float(inputs["ead"]),
            [(_float(t), _float(v)) for t, v in inputs["recoveries"]],
            _float(inputs["eir"]),
        )
    elif case["function"] == "weighted_ecl":
        actual = fae.weighted_ecl(
            {key: _float(value) for key, value in inputs["scenario_losses"].items()},
            {key: _float(value) for key, value in inputs["probabilities"].items()},
        )
    elif case["function"] == "poci_allowance_change":
        actual = fae.poci_allowance_change(**{key: _float(value) for key, value in inputs.items()})
    elif case["function"] == "measure_hedge":
        profile = fae.load_reference_data("MID_SIZE_UNIVERSAL_FIA")
        relationship = {
            **profile["hedges"][0],
            "hedge_type": "CASH_FLOW",
            "hedging_change": _float(inputs["hedging_change"]),
            "hedged_change": _float(inputs["hedged_change"]),
        }
        actual = fae.measure_hedge(relationship)
    elif case["function"] == "liability_modification_test":
        actual = fae.liability_modification_test(
            _float(inputs["original_present_value"]),
            _float(inputs["modified_present_value"]),
            threshold=_float(inputs["threshold"]),
        )
    else:  # pragma: no cover - the JSON schema is intentionally closed
        raise AssertionError(case["function"])

    expected = case["expected"]
    if isinstance(expected, str):
        assert actual == pytest.approx(_float(expected), abs=1e-12, rel=1e-12)
    elif isinstance(expected, list):
        assert actual == pytest.approx([_float(value) for value in expected], abs=1e-12, rel=1e-12)
    else:
        for key, value in expected.items():
            if isinstance(value, str):
                assert actual[key] == pytest.approx(_float(value), abs=1e-12, rel=1e-12)
            else:
                assert actual[key] is value


def _decode(value: Any) -> Any:
    if isinstance(value, dict) and set(value) == {"decimal"}:
        return float(Decimal(value["decimal"]))
    if isinstance(value, dict):
        return {key: _decode(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_decode(item) for item in value]
    return value


def _assert_equal(actual: Any, expected: Any, path: str = "root") -> None:
    if isinstance(expected, float):
        assert isinstance(actual, (int, float)) and not isinstance(actual, bool), path
        assert math.isfinite(actual), path
        assert math.isclose(actual, expected, abs_tol=1e-8, rel_tol=1e-10), path
    elif isinstance(expected, dict):
        assert isinstance(actual, dict) and set(actual) == set(expected), path
        for key in expected:
            _assert_equal(actual[key], expected[key], f"{path}.{key}")
    elif isinstance(expected, list):
        assert isinstance(actual, (list, tuple)) and len(actual) == len(expected), path
        for index, (left, right) in enumerate(zip(actual, expected)):
            _assert_equal(left, right, f"{path}[{index}]")
    else:
        assert actual == expected, path


@pytest.mark.parametrize("profile_id", fae.list_profiles())
def test_complete_corrected_profile_golden(profile_id: str) -> None:
    golden = _decode(read_json("golden.json"))["profiles"][profile_id]
    result = fae.run_dataset(fae.load_reference_data(profile_id))
    actual_tables = {
        key: [
            {
                field: (None if field == "explanation" and value == "" else value)
                for field, value in row.items()
                if field != "run_id"
            }
            for row in rows
        ]
        for key, rows in result.tables.items()
    }
    _assert_equal(result.status, golden["status"], f"{profile_id}.status")
    _assert_equal(dict(result.metrics), golden["metrics"], f"{profile_id}.metrics")
    _assert_equal(actual_tables, golden["tables"], f"{profile_id}.tables")
