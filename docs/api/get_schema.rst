get_schema
==========

.. autofunction:: financial_accounting_engine.get_schema

Accounting/API contract
-----------------------

Requirements: Library access/governance contract.
Reference basis: frozen policy/rules 2026_V1, input contract 1.1.0.
Source paragraphs are retained in decision outputs and the formula registry;
see the requirement mapping and correction notes for controlled judgements.

Parameters
----------

``table``
   Optional exact canonical input table name; None returns the complete input schema.

Return schema
-------------

Representative field/type schema (conditional decision fields may be absent;
table columns and optional values are listed in :doc:`../schemas`)::

   {
     "workbook": "str",
     "columns": {
       "type": "list",
       "items": [
         "str",
         "str",
         "str"
       ]
     },
     "fields": {
       "type": "table",
       "fields": {
         "description": [
           "str"
         ],
         "domain": [
           "NoneType",
           "str"
         ],
         "field": [
           "str"
         ],
         "key": [
           "NoneType",
           "str"
         ],
         "nullable": [
           "str"
         ],
         "origin": [
           "str"
         ],
         "time_reference": [
           "str"
         ],
         "type": [
           "str"
         ],
         "unit": [
           "str"
         ]
       }
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

``examples/analyst_workbook.py`` case ``get_schema`` supplies the arguments and an
independent expected-result assertion. Its function call is::

   import financial_accounting_engine as fae
   actual = fae.get_schema(*args, **kwargs)
   assert check(actual)

Executed pytest ID: ``tests/test_api.py::test_api_example[get_schema]``.
