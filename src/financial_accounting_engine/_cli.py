"""Command line entry point for local reference workflows."""

from __future__ import annotations

import argparse
import json

from . import (
    __version__,
    export_profile,
    export_results,
    list_profiles,
    load_reference_data,
    run_dataset,
)
from ._resources import verify_resources
from .models import AccountingError


def main() -> int:
    parser = argparse.ArgumentParser(
        description="financial-instruments-accounting: local reference accounting"
    )
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("profiles")
    sub.add_parser("doctor")
    export = sub.add_parser("export-profile")
    export.add_argument("profile", choices=list_profiles())
    export.add_argument("destination")
    run = sub.add_parser("run")
    run.add_argument("dataset")
    run.add_argument("--output", required=True)
    ref = sub.add_parser("reference")
    ref.add_argument("profile", choices=list_profiles())
    ref.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        if args.command == "profiles":
            print(json.dumps(list_profiles()))
        elif args.command == "doctor":
            print(
                json.dumps(
                    dict(
                        version=__version__,
                        resources=len(verify_resources()),
                        status="PASS",
                        official=False,
                    )
                )
            )
        elif args.command == "export-profile":
            print(export_profile(args.profile, args.destination))
        else:
            data = (
                load_reference_data(args.profile) if args.command == "reference" else args.dataset
            )
            result = run_dataset(data)
            export_results(result, args.output)
            print(json.dumps(dict(status=result.status, metrics=result.metrics), indent=2))
            return 0 if result.status == "APPROVED_REFERENCE" else 2
    except (AccountingError, OSError) as exc:
        parser.exit(2, f"Rejected: {exc}\n")
    return 0
