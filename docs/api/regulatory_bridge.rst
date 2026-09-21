regulatory_bridge
=================

.. autofunction:: financial_accounting_engine.regulatory_bridge

Accounting/API contract
-----------------------

Requirements: FR-057.
Reference basis: frozen policy/rules 2026_V1, input contract 1.1.0.
Source paragraphs are retained in decision outputs and the formula registry;
see the requirement mapping and correction notes for controlled judgements.

Parameters
----------

``instruments``
   Sequence of canonical instrument rows with unique instrument IDs.

``ecl_results``
   Instrument summary rows with instrument_id, stage and final_ecl; use presentation money for disclosures.

``stages``
   Instrument-ID to stage mapping, separate from regulatory default classification.

``fx``
   Instrument-ID to positive local-to-presentation FX multiplier mapping.

Return schema
-------------

Representative field/type schema (conditional decision fields may be absent;
table columns and optional values are listed in :doc:`../schemas`)::

   {
     "type": "table",
     "fields": {
       "accounting_value_used_in_regulatory_calculation": [
         "bool"
       ],
       "difference": [
         "float"
       ],
       "formula_id": [
         "str"
       ],
       "ifrs9_ecl": [
         "float"
       ],
       "ifrs9_stage": [
         "str"
       ],
       "instrument_id": [
         "str"
       ],
       "regulatory_approach": [
         "NoneType"
       ],
       "regulatory_default_flag": [
         "bool"
       ],
       "regulatory_expected_loss": [
         "float"
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

``examples/analyst_workbook.py`` case ``regulatory_bridge`` supplies the arguments and an
independent expected-result assertion. Its function call is::

   import financial_accounting_engine as fae
   actual = fae.regulatory_bridge(*args, **kwargs)
   assert check(actual)

Executed pytest ID: ``tests/test_api.py::test_api_example[regulatory_bridge]``.
