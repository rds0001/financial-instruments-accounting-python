assess_ibor_relief
==================

.. autofunction:: financial_accounting_engine.assess_ibor_relief

Accounting/API contract
-----------------------

Requirements: FR-050.
Reference basis: frozen policy/rules 2026_V1, input contract 1.1.0.
Source paragraphs are retained in decision outputs and the formula registry;
see the requirement mapping and correction notes for controlled judgements.

Parameters
----------

``applicable``
   Explicit externally reviewed IBOR-relief applicability boolean.

``policy_reference``
   Nonempty institution-specific policy/reform-phase reference for the controlled interface.

``approval_reference``
   Nonempty institutional case approval reference; no approval is inferred.

Return schema
-------------

Representative field/type schema (conditional decision fields may be absent;
table columns and optional values are listed in :doc:`../schemas`)::

   {
     "applicable": "bool",
     "policy_reference": "str",
     "approval_reference": "str",
     "status": "str",
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

``examples/analyst_workbook.py`` case ``assess_ibor_relief`` supplies the arguments and an
independent expected-result assertion. Its function call is::

   import financial_accounting_engine as fae
   actual = fae.assess_ibor_relief(*args, **kwargs)
   assert check(actual)

Executed pytest ID: ``tests/test_api.py::test_api_example[assess_ibor_relief]``.
