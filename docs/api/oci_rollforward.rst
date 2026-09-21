oci_rollforward
===============

.. autofunction:: financial_accounting_engine.oci_rollforward

Accounting/API contract
-----------------------

Requirements: FR-055.
Reference basis: frozen policy/rules 2026_V1, input contract 1.1.0.
Source paragraphs are retained in decision outputs and the formula registry;
see the requirement mapping and correction notes for controlled judgements.

Parameters
----------

``opening``
   Opening monetary balance (or instrument-ID keyed opening balances for table rollforwards).

``fair_value_movement``
   Signed period fair-value movement recognized in OCI.

``effective_hedge_movement``
   Signed effective hedge gain/loss for the reporting period credited to the OCI reserve.

``costs``
   Discounted cost cashflow pairs for LGD, or signed reserve movement for OCI; see function type.

``recycling``
   Signed reserve amount removed to profit/loss; positive reduces a positive reserve.

``basis_adjustment``
   Signed amount removed from OCI into the nonfinancial asset basis.

Return schema
-------------

Representative field/type schema (conditional decision fields may be absent;
table columns and optional values are listed in :doc:`../schemas`)::

   {
     "opening_reserve": "float",
     "fair_value_movement": "float",
     "effective_hedge_movement": "float",
     "cost_of_hedging_movement": "float",
     "recycling": "float",
     "basis_adjustment": "float",
     "closing_reserve": "float"
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

``examples/analyst_workbook.py`` case ``oci_rollforward`` supplies the arguments and an
independent expected-result assertion. Its function call is::

   import financial_accounting_engine as fae
   actual = fae.oci_rollforward(*args, **kwargs)
   assert check(actual)

Executed pytest ID: ``tests/test_api.py::test_api_example[oci_rollforward]``.
