gross_rollforward
=================

.. autofunction:: financial_accounting_engine.gross_rollforward

Accounting/API contract
-----------------------

Requirements: FR-053.
Reference basis: frozen policy/rules 2026_V1, input contract 1.1.0.
Source paragraphs are retained in decision outputs and the formula registry;
see the requirement mapping and correction notes for controlled judgements.

Parameters
----------

``instruments``
   Sequence of canonical instrument rows with unique instrument IDs.

``opening``
   Opening monetary balance (or instrument-ID keyed opening balances for table rollforwards).

``processed_events``
   Approved process_* outputs; use the same currency as the surrounding journal/rollforward.

``fx``
   Instrument-ID to positive local-to-presentation FX multiplier mapping.

Return schema
-------------

Representative field/type schema (conditional decision fields may be absent;
table columns and optional values are listed in :doc:`../schemas`)::

   {
     "type": "table",
     "fields": {
       "closing_gross": [
         "float"
       ],
       "derecognition": [
         "int"
       ],
       "formula_id": [
         "str"
       ],
       "instrument_id": [
         "str"
       ],
       "modification": [
         "int"
       ],
       "opening_gross": [
         "float"
       ],
       "other_contractual_and_fx_movements": [
         "float"
       ],
       "writeoff": [
         "int"
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

``examples/analyst_workbook.py`` case ``gross_rollforward`` supplies the arguments and an
independent expected-result assertion. Its function call is::

   import financial_accounting_engine as fae
   actual = fae.gross_rollforward(*args, **kwargs)
   assert check(actual)

Executed pytest ID: ``tests/test_api.py::test_api_example[gross_rollforward]``.
