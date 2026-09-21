get_lineage
===========

.. autofunction:: financial_accounting_engine.get_lineage

Accounting/API contract
-----------------------

Requirements: FR-058.
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
     "input_hash": "str",
     "policy_hash": "str",
     "rule_hash": "str",
     "code_hash": "str",
     "resource_hash": "str",
     "engine_version": "str",
     "contract_version": "str",
     "policy_id": "str",
     "rule_set_id": "str",
     "as_of_date": "str",
     "knowledge_time": "str",
     "official": "bool",
     "run_id": "str"
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

``examples/analyst_workbook.py`` case ``get_lineage`` supplies the arguments and an
independent expected-result assertion. Its function call is::

   import financial_accounting_engine as fae
   actual = fae.get_lineage(*args, **kwargs)
   assert check(actual)

Executed pytest ID: ``tests/test_api.py::test_api_example[get_lineage]``.
