Installation and local verification
===================================

Install the local wheel or source archive with pip. Python 3.10 is locally tested;
syntax supports 3.10 and later, with a broader platform/version matrix pending external
CI. No GitHub/PyPI release or R implementation is part of this local build.

CLI commands::

   financial-instruments-accounting --version
   financial-instruments-accounting doctor
   financial-instruments-accounting profiles
   financial-instruments-accounting export-profile SMALL_SA_RETAIL_FIA ./inputs
   financial-instruments-accounting run ./inputs --output ./results
   financial-instruments-accounting reference MID_SIZE_UNIVERSAL_FIA --output ./universal-results

The optional existing browser application is not bundled in this library release.
Use the public workflow API or CLI; the original application remains a separate
integration consumer. There is no HTTP listener, browser launch or telemetry in the
library. URLs are metadata/legal links and are never fetched by calculations.

Local development checks (from the library root)::

   python -m pytest
   python -m ruff check --no-cache src tests tools examples
   python -m mypy src
   python tools/verify_api_docs.py
   python -m sphinx -W --keep-going -b html docs .work/docs-html
   python -m sphinx -W --keep-going -b doctest docs .work/docs-doctest
   python -m build
   python -m twine check dist/*
   python tools/validate_distribution.py dist

Build from a clean source copy; do not include .work, environments, old source trees,
caches or scaffolds. Verify wheel and source-archive installations in independent
virtual environments and run tools/smoke_installed.py outside the source tree.
The script tests both profiles, scalar formulas, resources, rejected inputs and CLI.

Troubleshooting
---------------

An existing export destination is rejected deliberately: select a new directory.
ValidationError.issues identifies table/key problems. Do not suppress invalid scenario
weights, missing curve rows, expired approvals or failed controls by inserting zeros.
A damaged reference profile should be freshly exported and its input seal verified.
For real datasets, construct a complete canonical Dataset or 19 conformant workbooks;
no synthetic profile seal is required for user-authored datasets.

When a result is REVIEW_REQUIRED, examine get_controls before using any accounting
outputs. APPROVED_REFERENCE only means these automated reference controls passed.
Institutional ledger integration, four-eyes approval, mappings, contract interpretation,
independent model validation and production deployment are separate responsibilities.

The source-inventory archive and local progress records are development evidence and
are intentionally excluded from distributions. Official-source metadata are shipped;
third-party standards, law PDFs and downloaded publications are not.
