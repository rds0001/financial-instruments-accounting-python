split_own_credit
================

.. autofunction:: financial_accounting_engine.split_own_credit

Accounting/API contract
-----------------------

Requirements: FR-016.
Reference basis: frozen policy/rules 2026_V1, input contract 1.1.0.
Source paragraphs are retained in decision outputs and the formula registry;
see the requirement mapping and correction notes for controlled judgements.

Parameters
----------

``market``
   Canonical market_data row with controlled fair value, changes, model/level and own-credit facts.

``category``
   Canonical measurement classification, e.g. AMORTISED_COST, FVOCI_DEBT or FVTPL_LIABILITY.

Return schema
-------------

Representative field/type schema (conditional decision fields may be absent;
table columns and optional values are listed in :doc:`../schemas`)::

   {
     "instrument_id": "str",
     "total_fv_change": "float",
     "own_credit_oci": "float",
     "own_credit_pnl_due_to_mismatch": "float",
     "other_fv_change_pnl": "float",
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

``examples/analyst_workbook.py`` case ``split_own_credit`` supplies the arguments and an
independent expected-result assertion. Its function call is::

   import financial_accounting_engine as fae
   actual = fae.split_own_credit(*args, **kwargs)
   assert check(actual)

Executed pytest ID: ``tests/test_api.py::test_api_example[split_own_credit]``.
