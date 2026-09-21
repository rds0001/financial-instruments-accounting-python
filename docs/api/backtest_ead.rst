backtest_ead
============

.. autofunction:: financial_accounting_engine.backtest_ead

Accounting/API contract
-----------------------

Requirements: FR-043.
Reference basis: frozen policy/rules 2026_V1, input contract 1.1.0.
Source paragraphs are retained in decision outputs and the formula registry;
see the requirement mapping and correction notes for controlled judgements.

Parameters
----------

``observations``
   Canonical monitoring rows with model, owner, approval, prediction, outcome and positive exposure weight.

Return schema
-------------

Representative field/type schema (conditional decision fields may be absent;
table columns and optional values are listed in :doc:`../schemas`)::

   {
     "type": "table",
     "fields": {
       "approval_id": [
         "str"
       ],
       "auc": [
         "NoneType"
       ],
       "bias": [
         "float"
       ],
       "calibration_ratio": [
         "float"
       ],
       "challenger_flag": [
         "bool"
       ],
       "formula_id": [
         "str"
       ],
       "mean_absolute_error": [
         "float"
       ],
       "model_owner": [
         "str"
       ],
       "model_type": [
         "str"
       ],
       "model_version_id": [
         "str"
       ],
       "observations": [
         "int"
       ],
       "release_amount": [
         "float"
       ],
       "segment": [
         "str"
       ],
       "validation_status": [
         "str"
       ],
       "weighted_actual": [
         "float"
       ],
       "weighted_prediction": [
         "float"
       ]
     }
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

``examples/analyst_workbook.py`` case ``backtest_ead`` supplies the arguments and an
independent expected-result assertion. Its function call is::

   import financial_accounting_engine as fae
   actual = fae.backtest_ead(*args, **kwargs)
   assert check(actual)

Executed pytest ID: ``tests/test_api.py::test_api_example[backtest_ead]``.
