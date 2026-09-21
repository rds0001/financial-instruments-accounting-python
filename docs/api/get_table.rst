get_table
=========

.. autofunction:: financial_accounting_engine.get_table

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

``name``
   Exact workbook/sheet key or an unambiguous sheet name from AnalysisResult.tables.

Return schema
-------------

Representative field/type schema (conditional decision fields may be absent;
table columns and optional values are listed in :doc:`../schemas`)::

   {
     "type": "table",
     "fields": {
       "accounting_policy_id": [
         "str"
       ],
       "as_of_date": [
         "str"
       ],
       "decision_rule_id": [
         "str"
       ],
       "formula_id": [
         "NoneType"
       ],
       "instrument_id": [
         "str"
       ],
       "knowledge_time": [
         "str"
       ],
       "official_flag": [
         "bool"
       ],
       "prior_stage": [
         "str"
       ],
       "result_version": [
         "str"
       ],
       "rule_set_id": [
         "str"
       ],
       "run_id": [
         "str"
       ],
       "source_object_id": [
         "str"
       ],
       "source_reference": [
         "str"
       ],
       "stage": [
         "str"
       ],
       "stage_movement": [
         "str"
       ],
       "stage_reason": [
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

``examples/analyst_workbook.py`` case ``get_table`` supplies the arguments and an
independent expected-result assertion. Its function call is::

   import financial_accounting_engine as fae
   actual = fae.get_table(*args, **kwargs)
   assert check(actual)

Executed pytest ID: ``tests/test_api.py::test_api_example[get_table]``.
