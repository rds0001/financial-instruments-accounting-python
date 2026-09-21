build_journals
==============

.. autofunction:: financial_accounting_engine.build_journals

Accounting/API contract
-----------------------

Requirements: FR-002, FR-016, FR-048, FR-052.
Reference basis: frozen policy/rules 2026_V1, input contract 1.1.0.
Source paragraphs are retained in decision outputs and the formula registry;
see the requirement mapping and correction notes for controlled judgements.

Parameters
----------

``ecl_results``
   Instrument summary rows with instrument_id, stage and final_ecl; use presentation money for disclosures.

``opening_allowances``
   Instrument-ID keyed opening allowances in the journal currency.

``classifications``
   Instrument-ID to canonical classification mapping.

``instruments``
   Sequence of canonical instrument rows with unique instrument IDs.

``processed_events``
   Approved process_* outputs; use the same currency as the surrounding journal/rollforward.

``own_credit_results``
   Own-credit split rows; only classifications marked FVTPL_LIABILITY produce own-credit journals.

``hedge_results``
   Measured hedge rows containing period effective OCI, costs, recycling and basis amounts.

Return schema
-------------

Representative field/type schema (conditional decision fields may be absent;
table columns and optional values are listed in :doc:`../schemas`)::

   {
     "type": "table",
     "fields": {
       "account": [
         "str"
       ],
       "credit": [
         "float",
         "int"
       ],
       "debit": [
         "float",
         "int"
       ],
       "instrument_id": [
         "str"
       ],
       "journal_batch_id": [
         "str"
       ],
       "movement_type": [
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

``examples/analyst_workbook.py`` case ``build_journals`` supplies the arguments and an
independent expected-result assertion. Its function call is::

   import financial_accounting_engine as fae
   actual = fae.build_journals(*args, **kwargs)
   assert check(actual)

Executed pytest ID: ``tests/test_api.py::test_api_example[build_journals]``.
