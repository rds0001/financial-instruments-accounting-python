recovery_present_value
======================

.. autofunction:: financial_accounting_engine.recovery_present_value

Accounting/API contract
-----------------------

Requirements: FR-037.
Reference basis: frozen policy/rules 2026_V1, input contract 1.1.0.
Source paragraphs are retained in decision outputs and the formula registry;
see the requirement mapping and correction notes for controlled judgements.

Parameters
----------

``recoveries``
   Nonnegative recovery receipt (years from valuation date, amount) pairs.

``eir``
   Annual effective interest rate as a decimal greater than -1; credit-adjusted where POCI applies.

Return schema
-------------

Representative field/type schema (conditional decision fields may be absent;
table columns and optional values are listed in :doc:`../schemas`)::

   "float"

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

``examples/analyst_workbook.py`` case ``recovery_present_value`` supplies the arguments and an
independent expected-result assertion. Its function call is::

   import financial_accounting_engine as fae
   actual = fae.recovery_present_value(*args, **kwargs)
   assert check(actual)

Executed pytest ID: ``tests/test_api.py::test_api_example[recovery_present_value]``.
