modification_gain_loss
======================

.. autofunction:: financial_accounting_engine.modification_gain_loss

Accounting/API contract
-----------------------

Requirements: FR-023.
Reference basis: frozen policy/rules 2026_V1, input contract 1.1.0.
Source paragraphs are retained in decision outputs and the formula registry;
see the requirement mapping and correction notes for controlled judgements.

Parameters
----------

``gross_before``
   Gross carrying amount before modification, in the modified cashflow currency.

``modified_cashflows``
   Nonempty revised (years, receipt) pairs discounted at the original effective rate.

``original_eir``
   Original annual effective interest rate, retained through non-derecognizing modification.

Return schema
-------------

Representative field/type schema (conditional decision fields may be absent;
table columns and optional values are listed in :doc:`../schemas`)::

   "float"

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

``examples/analyst_workbook.py`` case ``modification_gain_loss`` supplies the arguments and an
independent expected-result assertion. Its function call is::

   import financial_accounting_engine as fae
   actual = fae.modification_gain_loss(*args, **kwargs)
   assert check(actual)

Executed pytest ID: ``tests/test_api.py::test_api_example[modification_gain_loss]``.
