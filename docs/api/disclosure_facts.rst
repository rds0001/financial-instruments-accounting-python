disclosure_facts
================

.. autofunction:: financial_accounting_engine.disclosure_facts

Accounting/API contract
-----------------------

Requirements: FR-019, FR-054.
Reference basis: frozen policy/rules 2026_V1, input contract 1.1.0.
Source paragraphs are retained in decision outputs and the formula registry;
see the requirement mapping and correction notes for controlled judgements.

Parameters
----------

``instruments``
   Sequence of canonical instrument rows with unique instrument IDs.

``ecl_results``
   Instrument summary rows with instrument_id, stage and final_ecl; use presentation money for disclosures.

``classifications``
   Instrument-ID to canonical classification mapping.

``stages``
   Instrument-ID to stage mapping, separate from regulatory default classification.

``fx``
   Instrument-ID to positive local-to-presentation FX multiplier mapping.

``presentation_currency``
   Declared common currency code for all monetary disclosure facts.

Return schema
-------------

Representative field/type schema (conditional decision fields may be absent;
table columns and optional values are listed in :doc:`../schemas`)::

   {
     "type": "table",
     "fields": {
       "allowance": [
         "float"
       ],
       "classification": [
         "str"
       ],
       "currency": [
         "str"
       ],
       "entity_id": [
         "str"
       ],
       "fx_rate": [
         "float"
       ],
       "gross_carrying_amount": [
         "float"
       ],
       "instrument_id": [
         "str"
       ],
       "net_carrying_amount": [
         "float"
       ],
       "portfolio": [
         "str"
       ],
       "presentation_currency": [
         "str"
       ],
       "stage": [
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

``examples/analyst_workbook.py`` case ``disclosure_facts`` supplies the arguments and an
independent expected-result assertion. Its function call is::

   import financial_accounting_engine as fae
   actual = fae.disclosure_facts(*args, **kwargs)
   assert check(actual)

Executed pytest ID: ``tests/test_api.py::test_api_example[disclosure_facts]``.
