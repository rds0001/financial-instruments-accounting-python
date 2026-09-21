hedge_reserve_rollforward
=========================

.. autofunction:: financial_accounting_engine.hedge_reserve_rollforward

Accounting/API contract
-----------------------

Requirements: FR-047, FR-048, FR-055.
Reference basis: frozen policy/rules 2026_V1, input contract 1.1.0.
Source paragraphs are retained in decision outputs and the formula registry;
see the requirement mapping and correction notes for controlled judgements.

Parameters
----------

``opening``
   Opening monetary balance (or instrument-ID keyed opening balances for table rollforwards).

``hedge_results``
   Measured hedge rows containing period effective OCI, costs, recycling and basis amounts.

Return schema
-------------

Representative field/type schema (conditional decision fields may be absent;
table columns and optional values are listed in :doc:`../schemas`)::

   {
     "opening_reserve": "float",
     "fair_value_movement": "float",
     "effective_hedge_movement": "float",
     "cost_of_hedging_movement": "float",
     "recycling": "float",
     "basis_adjustment": "float",
     "closing_reserve": "float"
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

``examples/analyst_workbook.py`` case ``hedge_reserve_rollforward`` supplies the arguments and an
independent expected-result assertion. Its function call is::

   import financial_accounting_engine as fae
   actual = fae.hedge_reserve_rollforward(*args, **kwargs)
   assert check(actual)

Executed pytest ID: ``tests/test_api.py::test_api_example[hedge_reserve_rollforward]``.
