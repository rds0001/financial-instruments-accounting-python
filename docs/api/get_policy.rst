get_policy
==========

.. autofunction:: financial_accounting_engine.get_policy

Accounting/API contract
-----------------------

Requirements: Library access/governance contract.
Reference basis: frozen policy/rules 2026_V1, input contract 1.1.0.
Source paragraphs are retained in decision outputs and the formula registry;
see the requirement mapping and correction notes for controlled judgements.

Parameters
----------

``policy_id``
   Exact packaged policy ID, default EU_FINANCIAL_INSTRUMENTS_2026_V1.

Return schema
-------------

Representative field/type schema (conditional decision fields may be absent;
table columns and optional values are listed in :doc:`../schemas`)::

   {
     "policy_id": "str",
     "version": "str",
     "reporting_date": "str",
     "knowledge_time": "str",
     "jurisdiction": "str",
     "reporting_scope": "str",
     "presentation_currency": "str",
     "regular_way_policy": "str",
     "electronic_payment_derecognition_election": "bool",
     "hedge_accounting_policy": "str",
     "low_credit_risk_relief": "bool",
     "past_due_sicr_days": "int",
     "default_backstop_days": "int",
     "rating_notch_sicr": "int",
     "absolute_lifetime_pd_sicr": "float",
     "relative_lifetime_pd_sicr": "float",
     "cure_months": "int",
     "probation_months": "int",
     "scenario_weight_tolerance": "float",
     "money_rounding": "str",
     "money_decimals": "int",
     "day_count": "str",
     "official_status_limit": "str",
     "source_rule_set": "str"
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

``examples/analyst_workbook.py`` case ``get_policy`` supplies the arguments and an
independent expected-result assertion. Its function call is::

   import financial_accounting_engine as fae
   actual = fae.get_policy(*args, **kwargs)
   assert check(actual)

Executed pytest ID: ``tests/test_api.py::test_api_example[get_policy]``.
