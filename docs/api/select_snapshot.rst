select_snapshot
===============

.. autofunction:: financial_accounting_engine.select_snapshot

Accounting/API contract
-----------------------

Requirements: FR-058.
Reference basis: frozen policy/rules 2026_V1, input contract 1.1.0.
Source paragraphs are retained in decision outputs and the formula registry;
see the requirement mapping and correction notes for controlled judgements.

Parameters
----------

``tables``
   Mapping of table names to bitemporal canonical rows.

``reporting_date``
   ISO YYYY-MM-DD reporting cutoff; also used to check approval/overlay expiry.

``knowledge_time``
   ISO knowledge timestamp including explicit timezone offset; inclusive known-time intervals.

Return schema
-------------

Representative field/type schema (conditional decision fields may be absent;
table columns and optional values are listed in :doc:`../schemas`)::

   {
     "instruments": {
       "type": "table",
       "fields": {
         "as_of_date": [
           "str"
         ],
         "business_key": [
           "str"
         ],
         "business_model": [
           "str"
         ],
         "contingent_feature": [
           "NoneType"
         ],
         "credit_adjusted_eir": [
           "int"
         ],
         "currency": [
           "str"
         ],
         "designation_approval_id": [
           "str"
         ],
         "ecl_method": [
           "str"
         ],
         "eir": [
           "float"
         ],
         "electronic_payment_election": [
           "bool"
         ],
         "embedded_derivative_separated": [
           "bool"
         ],
         "entity_id": [
           "str"
         ],
         "equity": [
           "NoneType"
         ],
         "fair_value": [
           "int"
         ],
         "fair_value_option": [
           "bool"
         ],
         "fvoci_equity_election": [
           "NoneType"
         ],
         "gross_amount": [
           "int"
         ],
         "guarantee_amount": [
           "int"
         ],
         "held_for_trading": [
           "NoneType"
         ],
         "host_contract_type": [
           "str"
         ],
         "hybrid_contract": [
           "bool"
         ],
         "impairment_scope": [
           "str"
         ],
         "initial_recognition_date": [
           "str"
         ],
         "instrument_id": [
           "str"
         ],
         "instrument_type": [
           "str"
         ],
         "interface_approved": [
           "bool"
         ],
         "interface_decision_id": [
           "NoneType"
         ],
         "interface_standard": [
           "NoneType"
         ],
         "is_official": [
           "bool"
         ],
         "known_from": [
           "str"
         ],
         "known_to": [
           "str"
         ],
         "liability": [
           "NoneType"
         ],
         "maturity_date": [
           "str"
         ],
         "nature_dependent_contract": [
           "bool"
         ],
         "overlay": [
           "int"
         ],
         "overlay_approved": [
           "bool"
         ],
         "overlay_double_count_checked": [
           "bool"
         ],
         "overlay_expiry": [
           "NoneType"
         ],
         "overlay_id": [
           "NoneType"
         ],
         "overlay_owner": [
           "NoneType"
         ],
         "overlay_thesis": [
           "NoneType"
         ],
         "own_use": [
           "bool"
         ],
         "payment_irrevocable": [
           "bool"
         ],
         "poci": [
           "NoneType"
         ],
         "poci_initial_lifetime_ecl": [
           "int"
         ],
         "portfolio": [
           "str"
         ],
         "provision_rate": [
           "int"
         ],
         "purchaser_net_buyer": [
           "bool"
         ],
         "quantity_consistent_expected_usage": [
           "bool"
         ],
         "rate_type": [
           "str"
         ],
         "recognition_status": [
           "str"
         ],
         "record_id": [
           "str"
         ],
         "record_status": [
           "str"
         ],
         "regular_way": [
           "bool"
         ],
         "regulatory_approach": [
           "str"
         ],
         "regulatory_default_flag": [
           "bool"
         ],
         "regulatory_expected_loss": [
           "int"
         ],
         "repurchase_within_reasonable_time": [
           "bool"
         ],
         "reset_rate": [
           "NoneType"
         ],
         "sale_timing_uncontrollable": [
           "bool"
         ],
         "scope_assessment": [
           "str"
         ],
         "settlement_risk_insignificant": [
           "bool"
         ],
         "settlement_short_period": [
           "bool"
         ],
         "simplified": [
           "NoneType"
         ],
         "source_record_id": [
           "str"
         ],
         "source_system": [
           "str"
         ],
         "trade_date_policy": [
           "str"
         ],
         "transaction_costs": [
           "int"
         ],
         "transaction_price": [
           "int"
         ],
         "undrawn": [
           "int"
         ],
         "valid_from": [
           "str"
         ],
         "valid_to": [
           "str"
         ],
         "version_no": [
           "int"
         ],
         "withdrawal_access_practical": [
           "bool"
         ]
       }
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

``examples/analyst_workbook.py`` case ``select_snapshot`` supplies the arguments and an
independent expected-result assertion. Its function call is::

   import financial_accounting_engine as fae
   actual = fae.select_snapshot(*args, **kwargs)
   assert check(actual)

Executed pytest ID: ``tests/test_api.py::test_api_example[select_snapshot]``.
