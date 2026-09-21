amortised_cost_step
===================

.. autofunction:: financial_accounting_engine.amortised_cost_step

Accounting/API contract
-----------------------

Requirements: FR-021.
Reference basis: frozen policy/rules 2026_V1, input contract 1.1.0.
Source paragraphs are retained in decision outputs and the formula registry;
see the requirement mapping and correction notes for controlled judgements.

Parameters
----------

``opening``
   Opening monetary balance (or instrument-ID keyed opening balances for table rollforwards).

``eir``
   Annual effective interest rate as a decimal greater than -1; credit-adjusted where POCI applies.

``time``
   Nonnegative period length in years for simple within-period accrual.

``cash_received``
   Nonnegative period receipts in the opening balance currency.

``adjustment``
   Signed within-period carrying amount adjustment in the input currency; default zero.

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

``examples/analyst_workbook.py`` case ``amortised_cost_step`` supplies the arguments and an
independent expected-result assertion. Its function call is::

   import financial_accounting_engine as fae
   actual = fae.amortised_cost_step(*args, **kwargs)
   assert check(actual)

Executed pytest ID: ``tests/test_api.py::test_api_example[amortised_cost_step]``.
