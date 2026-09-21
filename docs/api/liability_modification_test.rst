liability_modification_test
===========================

.. autofunction:: financial_accounting_engine.liability_modification_test

Accounting/API contract
-----------------------

Requirements: FR-024.
Reference basis: frozen policy/rules 2026_V1, input contract 1.1.0.
Source paragraphs are retained in decision outputs and the formula registry;
see the requirement mapping and correction notes for controlled judgements.

Parameters
----------

``original_present_value``
   Positive PV of original liability cashflows at original EIR.

``modified_present_value``
   PV of revised liability cashflows including eligible fees at original EIR.

``qualitative_substantial``
   Externally approved qualitative-substantial-change boolean, additional to the quantitative test.

``threshold``
   Explicit absolute relative-PV-change threshold in [0,1]; default 0.10, equality qualifies.

Return schema
-------------

Representative field/type schema (conditional decision fields may be absent;
table columns and optional values are listed in :doc:`../schemas`)::

   {
     "ratio": "float",
     "substantial": "bool",
     "threshold": "float"
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

``examples/analyst_workbook.py`` case ``liability_modification_test`` supplies the arguments and an
independent expected-result assertion. Its function call is::

   import financial_accounting_engine as fae
   actual = fae.liability_modification_test(*args, **kwargs)
   assert check(actual)

Executed pytest ID: ``tests/test_api.py::test_api_example[liability_modification_test]``.
