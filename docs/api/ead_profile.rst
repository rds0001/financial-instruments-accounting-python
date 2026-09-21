ead_profile
===========

.. autofunction:: financial_accounting_engine.ead_profile

Accounting/API contract
-----------------------

Requirements: FR-002, FR-036.
Reference basis: frozen policy/rules 2026_V1, input contract 1.1.0.
Source paragraphs are retained in decision outputs and the formula registry;
see the requirement mapping and correction notes for controlled judgements.

Parameters
----------

``drawn``
   Nonnegative drawn exposure for each period, before the supplied period prepayment adjustment.

``undrawn``
   Nonnegative undrawn commitment by period, converted using the corresponding CCF.

``ccf``
   Period conversion factors in [0,1], with the same vector length as drawn/undrawn.

``prepayment``
   Period prepayment fractions in [0,1], applied to drawn exposure; equal vector lengths required.

Return schema
-------------

Representative field/type schema (conditional decision fields may be absent;
table columns and optional values are listed in :doc:`../schemas`)::

   {
     "type": "list",
     "items": [
       "float"
     ]
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

``examples/analyst_workbook.py`` case ``ead_profile`` supplies the arguments and an
independent expected-result assertion. Its function call is::

   import financial_accounting_engine as fae
   actual = fae.ead_profile(*args, **kwargs)
   assert check(actual)

Executed pytest ID: ``tests/test_api.py::test_api_example[ead_profile]``.
