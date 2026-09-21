get_metrics
===========

.. autofunction:: financial_accounting_engine.get_metrics

Accounting/API contract
-----------------------

Requirements: Library access/governance contract.
Reference basis: frozen policy/rules 2026_V1, input contract 1.1.0.
Source paragraphs are retained in decision outputs and the formula registry;
see the requirement mapping and correction notes for controlled judgements.

Parameters
----------

``result``
   AnalysisResult returned by run_dataset; accessors return independent copies.

Return schema
-------------

Representative field/type schema (conditional decision fields may be absent;
table columns and optional values are listed in :doc:`../schemas`)::

   {
     "opening_gross_exposure": "float",
     "closing_gross_exposure": "float",
     "final_ecl_before_writeoff": "float",
     "closing_allowance": "float",
     "net_carrying_amount": "float",
     "classification_distribution": {
       "AC_HOST_PLUS_SEPARATE_DERIVATIVE": "int",
       "AMORTISED_COST": "int",
       "AMORTISED_COST_LIABILITY": "int",
       "FINANCIAL_GUARANTEE": "int",
       "FVOCI_DEBT": "int",
       "FVOCI_EQUITY": "int",
       "FVTPL": "int",
       "FVTPL_LIABILITY": "int",
       "LOAN_COMMITMENT": "int",
       "NO_IFRS9_SCOPE": "int"
     },
     "stage_distribution": {
       "NO_IMPAIRMENT_SCOPE": "int",
       "POCI": "int",
       "SIMPLIFIED_LIFETIME": "int",
       "STAGE_1": "int",
       "STAGE_2": "int",
       "STAGE_3": "int"
     },
     "hedge_status_distribution": {
       "DISCONTINUED": "int",
       "ELIGIBLE": "int",
       "REBALANCE_REQUIRED": "int"
     },
     "fvoci_oci_movement": "float",
     "hedge_reserve_movement": "float",
     "journal_batches": "int",
     "backtesting_result_sets": "int"
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

``examples/analyst_workbook.py`` case ``get_metrics`` supplies the arguments and an
independent expected-result assertion. Its function call is::

   import financial_accounting_engine as fae
   actual = fae.get_metrics(*args, **kwargs)
   assert check(actual)

Executed pytest ID: ``tests/test_api.py::test_api_example[get_metrics]``.
