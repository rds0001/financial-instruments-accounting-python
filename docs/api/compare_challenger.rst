compare_challenger
==================

.. autofunction:: financial_accounting_engine.compare_challenger

Accounting/API contract
-----------------------

Requirements: FR-043.
Reference basis: frozen policy/rules 2026_V1, input contract 1.1.0.
Source paragraphs are retained in decision outputs and the formula registry;
see the requirement mapping and correction notes for controlled judgements.

Parameters
----------

``reference``
   Reference monitoring rows keyed uniquely by model_type/segment.

``challenger``
   Monitoring result rows keyed by model_type/segment, with MAE and bias.

Return schema
-------------

Representative field/type schema (conditional decision fields may be absent;
table columns and optional values are listed in :doc:`../schemas`)::

   {
     "type": "table",
     "fields": {
       "bias_difference": [
         "float"
       ],
       "mae_difference": [
         "float"
       ],
       "model_type": [
         "str"
       ],
       "segment": [
         "str"
       ],
       "view": [
         "str"
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

``examples/analyst_workbook.py`` case ``compare_challenger`` supplies the arguments and an
independent expected-result assertion. Its function call is::

   import financial_accounting_engine as fae
   actual = fae.compare_challenger(*args, **kwargs)
   assert check(actual)

Executed pytest ID: ``tests/test_api.py::test_api_example[compare_challenger]``.
