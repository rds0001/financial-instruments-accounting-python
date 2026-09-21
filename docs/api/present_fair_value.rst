present_fair_value
==================

.. autofunction:: financial_accounting_engine.present_fair_value

Accounting/API contract
-----------------------

Requirements: FR-018.
Reference basis: frozen policy/rules 2026_V1, input contract 1.1.0.
Source paragraphs are retained in decision outputs and the formula registry;
see the requirement mapping and correction notes for controlled judgements.

Parameters
----------

``instrument``
   Canonical instruments row, restricted to the fields required for the targeted calculation.

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
     "classification": "str",
     "fair_value": "float",
     "total_fv_change": "float",
     "pnl_fv_change": "float",
     "oci_fv_change": "float",
     "recycling_policy": "str",
     "ifrs13_level": "int",
     "valuation_model": "str",
     "valuation_status": "str",
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

``examples/analyst_workbook.py`` case ``present_fair_value`` supplies the arguments and an
independent expected-result assertion. Its function call is::

   import financial_accounting_engine as fae
   actual = fae.present_fair_value(*args, **kwargs)
   assert check(actual)

Executed pytest ID: ``tests/test_api.py::test_api_example[present_fair_value]``.
