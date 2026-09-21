measure_hedge
=============

.. autofunction:: financial_accounting_engine.measure_hedge

Accounting/API contract
-----------------------

Requirements: FR-045, FR-047, FR-049.
Reference basis: frozen policy/rules 2026_V1, input contract 1.1.0.
Source paragraphs are retained in decision outputs and the formula registry;
see the requirement mapping and correction notes for controlled judgements.

Parameters
----------

``relationship``
   Canonical hedges row with documented eligibility, ratios and cumulative designated changes.

Return schema
-------------

Representative field/type schema (conditional decision fields may be absent;
table columns and optional values are listed in :doc:`../schemas`)::

   {
     "relationship_id": "str",
     "hedge_type": "str",
     "status": "str",
     "nature_dependent_electricity_hedge": "bool",
     "ineffectiveness_pnl": "float",
     "oci_effective": "float",
     "cost_of_hedging_reserve": "float",
     "recycle_amount": "float",
     "basis_adjustment": "float",
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

``examples/analyst_workbook.py`` case ``measure_hedge`` supplies the arguments and an
independent expected-result assertion. Its function call is::

   import financial_accounting_engine as fae
   actual = fae.measure_hedge(*args, **kwargs)
   assert check(actual)

Executed pytest ID: ``tests/test_api.py::test_api_example[measure_hedge]``.
