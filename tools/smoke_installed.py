"""Public smoke test intended to run from an isolated installed artifact."""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from importlib.metadata import version
from pathlib import Path

import financial_accounting_engine as fae

EXPECTED_ECL = {
    "MID_SIZE_UNIVERSAL_FIA": 372727.1317328072,
    "SMALL_SA_RETAIL_FIA": 92039.1234660137,
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--forbid-prefix", type=Path)
    args = parser.parse_args()
    workspace = args.workspace.resolve()

    assert version("financial-instruments-accounting") == "1.0.0"
    assert fae.__version__ == "1.0.0"
    if args.forbid_prefix:
        module_path = Path(fae.__file__).resolve()
        assert not module_path.is_relative_to(args.forbid_prefix.resolve()), module_path
    assert math.isclose(fae.effective_interest_rate(1000, [(1, 1100)]), 0.1, abs_tol=1e-10)

    assert fae.list_profiles() == tuple(EXPECTED_ECL)
    for profile, expected_ecl in EXPECTED_ECL.items():
        result = fae.run_dataset(fae.load_reference_data(profile))
        assert result.status == "APPROVED_REFERENCE"
        assert math.isclose(
            float(result.metrics["final_ecl_before_writeoff"]), expected_ecl, abs_tol=1e-8
        )
        assert len(fae.get_controls(result)) == 28

    workspace.mkdir(parents=True, exist_ok=False)
    exported = fae.export_profile("SMALL_SA_RETAIL_FIA", workspace / "profile")
    assert len(list(exported.glob("*.xlsx"))) == 19
    cli = Path(sys.executable).parent / "financial-instruments-accounting"
    assert cli.is_file(), cli
    doctor = subprocess.run(
        [str(cli), "doctor"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert json.loads(doctor.stdout)["status"] == "PASS"
    listed = subprocess.run(
        [str(cli), "profiles"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert tuple(json.loads(listed.stdout)) == fae.list_profiles()
    print("PASS: installed package, CLI, resources and both full profiles")


if __name__ == "__main__":
    main()
