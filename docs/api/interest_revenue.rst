interest_revenue
================

.. autofunction:: financial_accounting_engine.interest_revenue

Accounting/API contract
-----------------------

Requirements: FR-022.
Reference basis: frozen policy/rules 2026_V1, input contract 1.1.0.
Source paragraphs are retained in decision outputs and the formula registry;
see the requirement mapping and correction notes for controlled judgements.

Parameters
----------

``instrument``
   Canonical instruments row, restricted to the fields required for the targeted calculation.

``stage``
   Canonical STAGE_1/STAGE_2/STAGE_3/POCI/SIMPLIFIED_LIFETIME/NO_IMPAIRMENT_SCOPE label.

``allowance``
   Signed allowance in instrument local currency; POCI changes may be negative.

Return schema
-------------

Representative field/type schema (conditional decision fields may be absent;
table columns and optional values are listed in :doc:`../schemas`)::

   {
     "instrument_id": "str",
     "interest_basis": "float",
     "interest_rate": "float",
     "interest_revenue": "float",
     "interest_method": "str",
     "formula_id": "str",
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

``examples/analyst_workbook.py`` case ``interest_revenue`` supplies the arguments and an
independent expected-result assertion. Its function call is::

   import financial_accounting_engine as fae
   actual = fae.interest_revenue(*args, **kwargs)
   assert check(actual)

Executed pytest ID: ``tests/test_api.py::test_api_example[interest_revenue]``.
