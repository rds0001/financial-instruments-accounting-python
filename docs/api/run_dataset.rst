run_dataset
===========

.. autofunction:: financial_accounting_engine.run_dataset

Accounting/API contract
-----------------------

Requirements: FR-019, FR-021, FR-059.
Reference basis: frozen policy/rules 2026_V1, input contract 1.1.0.
Source paragraphs are retained in decision outputs and the formula registry;
see the requirement mapping and correction notes for controlled judgements.

Parameters
----------

``dataset``
   Complete canonical Dataset mapping or input-directory path; file/in-memory paths use one core.

``policy``
   Complete explicit versioned policy; None selects the frozen EU_FINANCIAL_INSTRUMENTS_2026_V1.

Return schema
-------------

Representative field/type schema (conditional decision fields may be absent;
table columns and optional values are listed in :doc:`../schemas`)::

   {
     "type": "AnalysisResult",
     "fields": [
       "tables",
       "metrics",
       "lineage",
       "status",
       "official"
     ]
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

``examples/analyst_workbook.py`` case ``run_dataset`` supplies the arguments and an
independent expected-result assertion. Its function call is::

   import financial_accounting_engine as fae
   actual = fae.run_dataset(*args, **kwargs)
   assert check(actual)

Executed pytest ID: ``tests/test_api.py::test_api_example[run_dataset]``.
