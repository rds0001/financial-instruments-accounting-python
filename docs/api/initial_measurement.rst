initial_measurement
===================

.. autofunction:: financial_accounting_engine.initial_measurement

Accounting/API contract
-----------------------

Requirements: FR-017.
Reference basis: frozen policy/rules 2026_V1, input contract 1.1.0.
Source paragraphs are retained in decision outputs and the formula registry;
see the requirement mapping and correction notes for controlled judgements.

Parameters
----------

``instrument``
   Canonical instruments row, restricted to the fields required for the targeted calculation.

``category``
   Canonical measurement classification, e.g. AMORTISED_COST, FVOCI_DEBT or FVTPL_LIABILITY.

Return schema
-------------

Representative field/type schema (conditional decision fields may be absent;
table columns and optional values are listed in :doc:`../schemas`)::

   {
     "instrument_id": "str",
     "initial_carrying_amount": "float",
     "transaction_cost_treatment": "str",
     "day_one_difference": "float",
     "formula_id": "str",
     "source_reference": "str"
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

``examples/analyst_workbook.py`` case ``initial_measurement`` supplies the arguments and an
independent expected-result assertion. Its function call is::

   import financial_accounting_engine as fae
   actual = fae.initial_measurement(*args, **kwargs)
   assert check(actual)

Executed pytest ID: ``tests/test_api.py::test_api_example[initial_measurement]``.
