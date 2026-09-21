process_writeoff
================

.. autofunction:: financial_accounting_engine.process_writeoff

Accounting/API contract
-----------------------

Requirements: FR-026.
Reference basis: frozen policy/rules 2026_V1, input contract 1.1.0.
Source paragraphs are retained in decision outputs and the formula registry;
see the requirement mapping and correction notes for controlled judgements.

Parameters
----------

``event``
   Canonical approved event facts, including matching instrument_id, type, reason and relevant amounts.

``instrument``
   Canonical instruments row, restricted to the fields required for the targeted calculation.

Return schema
-------------

Representative field/type schema (conditional decision fields may be absent;
table columns and optional values are listed in :doc:`../schemas`)::

   {
     "event_id": "str",
     "instrument_id": "str",
     "event_type": "str",
     "amount": "float",
     "derecognition_result": "str",
     "continuing_involvement": "float",
     "modification_result": "float",
     "pnl_effect": "float",
     "reason_code": "str",
     "formula_id": "str"
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

``examples/analyst_workbook.py`` case ``process_writeoff`` supplies the arguments and an
independent expected-result assertion. Its function call is::

   import financial_accounting_engine as fae
   actual = fae.process_writeoff(*args, **kwargs)
   assert check(actual)

Executed pytest ID: ``tests/test_api.py::test_api_example[process_writeoff]``.
