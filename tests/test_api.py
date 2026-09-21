import importlib.util
import inspect
from pathlib import Path

import pytest

import financial_accounting_engine as f

spec = importlib.util.spec_from_file_location(
    "analyst_workbook", Path(__file__).parents[1] / "examples/analyst_workbook.py"
)
examples = importlib.util.module_from_spec(spec)
spec.loader.exec_module(examples)
FUNCTIONS = [n for n in f.__all__ if inspect.isfunction(getattr(f, n))]


@pytest.fixture(scope="module")
def api_cases(tmp_path_factory):
    return examples.cases(tmp_path_factory.mktemp("api"))


@pytest.mark.parametrize("name", FUNCTIONS)
def test_api_example(name, api_cases):
    args, kwargs, check = api_cases[name]
    assert check(getattr(f, name)(*args, **kwargs)), name


def test_export_inventory_matches_examples(api_cases):
    assert set(FUNCTIONS) == set(api_cases)
