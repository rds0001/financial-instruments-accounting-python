benchmark_ecl
=============

.. autofunction:: financial_accounting_engine.benchmark_ecl

Accounting/API contract
-----------------------

Requirements: FR-060.
Reference basis: frozen policy/rules 2026_V1, input contract 1.1.0.
Source paragraphs are retained in decision outputs and the formula registry;
see the requirement mapping and correction notes for controlled judgements.

Parameters
----------

``iterations``
   Positive integer number of fixed golden-vector evaluations; capped at 1,000,000.

Return schema
-------------

Representative field/type schema (conditional decision fields may be absent;
table columns and optional values are listed in :doc:`../schemas`)::

   {
     "iterations": "int",
     "checksum": "float",
     "elapsed_seconds": "float",
     "peak_bytes": "int",
     "formula_id": "str"
   }

Errors and effects
------------------

See :doc:`../contract` for finite-value, missing-data and timezone rules.
Invalid domain inputs raise AccountingError; dataset issues use ValidationError;
unknown/damaged resources and conflicting export targets use ResourceError.
Only export_profile and export_results create files. run_dataset may read XLSX;
benchmark_ecl briefly measures time/memory. Other calls are in-memory or read
immutable package resources. No call contacts external services.

Executable example and direct test
----------------------------------

``examples/analyst_workbook.py`` case ``benchmark_ecl`` supplies the arguments and an
independent expected-result assertion. Its function call is::

   import financial_accounting_engine as fae
   actual = fae.benchmark_ecl(*args, **kwargs)
   assert check(actual)

Executed pytest ID: ``tests/test_api.py::test_api_example[benchmark_ecl]``.
