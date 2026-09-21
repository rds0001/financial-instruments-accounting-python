component_ecl
=============

.. autofunction:: financial_accounting_engine.component_ecl

Accounting/API contract
-----------------------

Requirements: FR-033.
Reference basis: frozen policy/rules 2026_V1, input contract 1.1.0.
Source paragraphs are retained in decision outputs and the formula registry;
see the requirement mapping and correction notes for controlled judgements.

Parameters
----------

``marginal_pd``
   Unconditional default probability mass for the supplied period in [0,1].

``ead``
   Nonnegative exposure at default in one currency; LGD derivation requires positive exposure.

``lgd``
   Conditional loss severity in [0,1], with recovery timing already valued relative to default.

``eir``
   Annual effective interest rate as a decimal greater than -1; credit-adjusted where POCI applies.

``year``
   Nonnegative discount time to default in years; recovery timing is already incorporated in LGD.

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

``examples/analyst_workbook.py`` case ``component_ecl`` supplies the arguments and an
independent expected-result assertion. Its function call is::

   import financial_accounting_engine as fae
   actual = fae.component_ecl(*args, **kwargs)
   assert check(actual)

Executed pytest ID: ``tests/test_api.py::test_api_example[component_ecl]``.
