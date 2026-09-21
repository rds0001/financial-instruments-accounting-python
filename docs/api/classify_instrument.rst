classify_instrument
===================

.. autofunction:: financial_accounting_engine.classify_instrument

Accounting/API contract
-----------------------

Requirements: FR-001, FR-002, FR-007, FR-014, FR-015.
Reference basis: frozen policy/rules 2026_V1, input contract 1.1.0.
Source paragraphs are retained in decision outputs and the formula registry;
see the requirement mapping and correction notes for controlled judgements.

Parameters
----------

``instrument``
   Canonical instruments row, restricted to the fields required for the targeted calculation.

``features``
   Reviewed SPPI/classification_inputs fields; missing basic-lending facts reject.

``scope_decision``
   Explicit IN_IFRS9_SCOPE or NO_IFRS9_SCOPE decision; default in-scope requires caller judgement.

Return schema
-------------

Representative field/type schema (conditional decision fields may be absent;
table columns and optional values are listed in :doc:`../schemas`)::

   {
     "instrument_id": "str",
     "classification": "str",
     "sppi_result": "str",
     "sppi_reason": "str",
     "reclassification_status": "str",
     "decision_rule_id": "str",
     "source_reference": "str"
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

``examples/analyst_workbook.py`` case ``classify_instrument`` supplies the arguments and an
independent expected-result assertion. Its function call is::

   import financial_accounting_engine as fae
   actual = fae.classify_instrument(*args, **kwargs)
   assert check(actual)

Executed pytest ID: ``tests/test_api.py::test_api_example[classify_instrument]``.
