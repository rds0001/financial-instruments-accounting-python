"""Fail closed on missing exports, parameter docs, examples or collected direct tests."""

import inspect
import json
import subprocess
import sys
from pathlib import Path

import financial_accounting_engine as fae

ROOT = Path(__file__).resolve().parents[1]


def main():
    data = json.loads((ROOT / "tools/api_inventory.json").read_text())
    functions = {n for n in fae.__all__ if inspect.isfunction(getattr(fae, n))}
    entries = {r["name"]: r for r in data["functions"]}
    assert functions == entries.keys(), functions ^ entries.keys()
    assert set(fae.__all__) == functions | set(data["classes"]) | set(data["constants"])
    collection = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "--collect-only",
            "-q",
            "-o",
            "cache_dir=.work/pytest-cache",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    for name, entry in entries.items():
        page = (ROOT / entry["documentation"]).read_text()
        assert (ROOT / entry["example"]).is_file()
        assert f"financial_accounting_engine.{name}" in page
        signature = inspect.signature(getattr(fae, name))
        assert str(signature) == entry["signature"]
        assert signature.return_annotation is not inspect.Signature.empty
        for parameter in signature.parameters:
            assert f"``{parameter}``" in page, (name, parameter)
            assert signature.parameters[parameter].annotation is not inspect.Parameter.empty
        for test in entry["tests"]:
            assert test in collection, test
        assert entry["return_schema"]
    requirements = (ROOT / "docs/requirements.rst").read_text()
    assert all(f"FR-{n:03d}" in requirements for n in range(1, 61))
    print(
        f"PASS: {len(functions)} public functions documented, typed and linked to executable direct tests"
    )


if __name__ == "__main__":
    main()
