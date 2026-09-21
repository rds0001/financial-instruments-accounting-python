load_reference_data
===================

.. autofunction:: financial_accounting_engine.load_reference_data

Accounting/API contract
-----------------------

Requirements: Library access/governance contract.
Reference basis: frozen policy/rules 2026_V1, input contract 1.1.0.
Source paragraphs are retained in decision outputs and the formula registry;
see the requirement mapping and correction notes for controlled judgements.

Parameters
----------

``profile_id``
   Exact profile identifier from list_profiles(); resources are version 1.0.0.

Return schema
-------------

Representative field/type schema (conditional decision fields may be absent;
table columns and optional values are listed in :doc:`../schemas`)::

   {
     "run_control": {
       "type": "table",
       "fields": {
         "as_of_date": [
           "str"
         ],
         "business_key": [
           "str"
         ],
         "contract_version": [
           "str"
         ],
         "is_official": [
           "bool"
         ],
         "knowledge_time": [
           "str"
         ],
         "known_from": [
           "str"
         ],
         "known_to": [
           "str"
         ],
         "policy_id": [
           "str"
         ],
         "profile_id": [
           "str"
         ],
         "record_id": [
           "str"
         ],
         "record_status": [
           "str"
         ],
         "reporting_date": [
           "str"
         ],
         "rule_set_id": [
           "str"
         ],
         "run_key": [
           "str"
         ],
         "source_record_id": [
           "str"
         ],
         "source_system": [
           "str"
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
         "view": [
           "str"
         ]
       }
     },
     "entities": {
       "type": "table",
       "fields": {
         "as_of_date": [
           "str"
         ],
         "business_key": [
           "str"
         ],
         "consolidation_scope": [
           "str"
         ],
         "entity_id": [
           "str"
         ],
         "entity_name": [
           "str"
         ],
         "functional_currency": [
           "str"
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
         "record_id": [
           "str"
         ],
         "record_status": [
           "str"
         ],
         "source_record_id": [
           "str"
         ],
         "source_system": [
           "str"
         ],
         "valid_from": [
           "str"
         ],
         "valid_to": [
           "str"
         ],
         "version_no": [
           "int"
         ]
       }
     },
     "parties": {
       "type": "table",
       "fields": {
         "as_of_date": [
           "str"
         ],
         "business_key": [
           "str"
         ],
         "default_flag": [
           "bool"
         ],
         "forbearance": [
           "bool"
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
         "party_id": [
           "str"
         ],
         "rating_current": [
           "int"
         ],
         "rating_orig": [
           "int"
         ],
         "record_id": [
           "str"
         ],
         "record_status": [
           "str"
         ],
         "source_record_id": [
           "str"
         ],
         "source_system": [
           "str"
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
         "watchlist": [
           "bool"
         ]
       }
     },
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
           "float",
           "int"
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
           "NoneType",
           "str"
         ],
         "overlay_id": [
           "NoneType",
           "str"
         ],
         "overlay_owner": [
           "NoneType",
           "str"
         ],
         "overlay_thesis": [
           "NoneType",
           "str"
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
           "float",
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
           "NoneType",
           "bool"
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
     },
     "cashflows": {
       "type": "table",
       "fields": {
         "amount": [
           "int"
         ],
         "as_of_date": [
           "str"
         ],
         "business_key": [
           "str"
         ],
         "cashflow_id": [
           "str"
         ],
         "cashflow_type": [
           "str"
         ],
         "contractual": [
           "bool"
         ],
         "expected": [
           "bool"
         ],
         "include_in_eir": [
           "bool"
         ],
         "instrument_id": [
           "str"
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
         "record_id": [
           "str"
         ],
         "record_status": [
           "str"
         ],
         "scenario_id": [
           "NoneType"
         ],
         "source_record_id": [
           "str"
         ],
         "source_system": [
           "str"
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
         "year_fraction": [
           "int"
         ]
       }
     },
     "opening_balances": {
       "type": "table",
       "fields": {
         "as_of_date": [
           "str"
         ],
         "business_key": [
           "str"
         ],
         "instrument_id": [
           "str"
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
         "ledger_allowance": [
           "int"
         ],
         "ledger_gross": [
           "int"
         ],
         "opening_allowance": [
           "int"
         ],
         "opening_fvoci_reserve": [
           "int"
         ],
         "opening_gross": [
           "int"
         ],
         "opening_hedge_reserve": [
           "int"
         ],
         "record_id": [
           "str"
         ],
         "record_status": [
           "str"
         ],
         "source_record_id": [
           "str"
         ],
         "source_system": [
           "str"
         ],
         "valid_from": [
           "str"
         ],
         "valid_to": [
           "str"
         ],
         "version_no": [
           "int"
         ]
       }
     },
     "classification_inputs": {
       "type": "table",
       "fields": {
         "approval_id": [
           "str"
         ],
         "as_of_date": [
           "str"
         ],
         "basic_interest": [
           "bool"
         ],
         "business_key": [
           "str"
         ],
         "business_model": [
           "str"
         ],
         "business_model_change": [
           "bool"
         ],
         "cli_lookthrough_pass": [
           "bool"
         ],
         "contingent_feature_basic": [
           "bool"
         ],
         "de_minimis_or_non_genuine": [
           "bool"
         ],
         "designation": [
           "str"
         ],
         "extension_basic": [
           "bool"
         ],
         "instrument_id": [
           "str"
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
         "leverage": [
           "bool"
         ],
         "modified_time_value_pass": [
           "bool"
         ],
         "non_recourse_pass": [
           "bool"
         ],
         "prepayment_compensation_reasonable": [
           "bool"
         ],
         "principal_consistent": [
           "bool"
         ],
         "record_id": [
           "str"
         ],
         "record_status": [
           "str"
         ],
         "source_record_id": [
           "str"
         ],
         "source_system": [
           "str"
         ],
         "sppi_override": [
           "NoneType"
         ],
         "valid_from": [
           "str"
         ],
         "valid_to": [
           "str"
         ],
         "version_no": [
           "int"
         ]
       }
     },
     "collateral": {
       "type": "table",
       "fields": {
         "allocated_amount": [
           "int"
         ],
         "as_of_date": [
           "str"
         ],
         "business_key": [
           "str"
         ],
         "collateral_id": [
           "str"
         ],
         "collateral_type": [
           "str"
         ],
         "cost": [
           "int"
         ],
         "fair_value": [
           "int"
         ],
         "haircut": [
           "float"
         ],
         "instrument_id": [
           "str"
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
         "record_id": [
           "str"
         ],
         "record_status": [
           "str"
         ],
         "recovery_year": [
           "int"
         ],
         "separately_recognised": [
           "bool"
         ],
         "source_record_id": [
           "str"
         ],
         "source_system": [
           "str"
         ],
         "valid_from": [
           "str"
         ],
         "valid_to": [
           "str"
         ],
         "version_no": [
           "int"
         ]
       }
     },
     "staging_inputs": {
       "type": "table",
       "fields": {
         "as_of_date": [
           "str"
         ],
         "business_key": [
           "str"
         ],
         "collective_assessment": [
           "bool"
         ],
         "credit_impaired": [
           "bool"
         ],
         "days_past_due": [
           "int"
         ],
         "forbearance": [
           "bool"
         ],
         "forward_looking_sicr": [
           "bool"
         ],
         "impairment_scope": [
           "str"
         ],
         "instrument_id": [
           "str"
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
         "lifetime_pd_current": [
           "NoneType"
         ],
         "lifetime_pd_orig": [
           "NoneType"
         ],
         "low_credit_risk": [
           "bool"
         ],
         "months_since_cure": [
           "int"
         ],
         "months_since_forbearance": [
           "int"
         ],
         "override_approved": [
           "bool"
         ],
         "override_expiry": [
           "NoneType"
         ],
         "override_reason": [
           "NoneType"
         ],
         "poci": [
           "bool"
         ],
         "prior_stage": [
           "str"
         ],
         "rating_current": [
           "int"
         ],
         "rating_orig": [
           "int"
         ],
         "record_id": [
           "str"
         ],
         "record_status": [
           "str"
         ],
         "sicr_override": [
           "NoneType"
         ],
         "sicr_rebuttal": [
           "bool"
         ],
         "simplified": [
           "bool"
         ],
         "source_record_id": [
           "str"
         ],
         "source_system": [
           "str"
         ],
         "unlikely_to_pay": [
           "bool"
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
         "watchlist": [
           "bool"
         ]
       }
     },
     "pd_curves": {
       "type": "table",
       "fields": {
         "approval_id": [
           "str"
         ],
         "as_of_date": [
           "str"
         ],
         "business_key": [
           "str"
         ],
         "instrument_id": [
           "str"
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
         "marginal_pd": [
           "float"
         ],
         "model_owner": [
           "str"
         ],
         "model_version_id": [
           "str"
         ],
         "record_id": [
           "str"
         ],
         "record_status": [
           "str"
         ],
         "scenario_id": [
           "str"
         ],
         "source_record_id": [
           "str"
         ],
         "source_system": [
           "str"
         ],
         "valid_from": [
           "str"
         ],
         "valid_to": [
           "str"
         ],
         "validation_status": [
           "str"
         ],
         "version_no": [
           "int"
         ],
         "year": [
           "int"
         ]
       }
     },
     "lgd_profiles": {
       "type": "table",
       "fields": {
         "approval_id": [
           "str"
         ],
         "as_of_date": [
           "str"
         ],
         "business_key": [
           "str"
         ],
         "instrument_id": [
           "str"
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
         "lgd": [
           "float"
         ],
         "model_owner": [
           "str"
         ],
         "model_version_id": [
           "str"
         ],
         "record_id": [
           "str"
         ],
         "record_status": [
           "str"
         ],
         "recovery_present_value": [
           "float",
           "int"
         ],
         "resolution_path": [
           "str"
         ],
         "scenario_id": [
           "str"
         ],
         "source_record_id": [
           "str"
         ],
         "source_system": [
           "str"
         ],
         "valid_from": [
           "str"
         ],
         "valid_to": [
           "str"
         ],
         "validation_status": [
           "str"
         ],
         "version_no": [
           "int"
         ],
         "workout_cost": [
           "int"
         ],
         "year": [
           "int"
         ]
       }
     },
     "ead_profiles": {
       "type": "table",
       "fields": {
         "approval_id": [
           "str"
         ],
         "as_of_date": [
           "str"
         ],
         "behavioural_horizon_years": [
           "int"
         ],
         "business_key": [
           "str"
         ],
         "ccf": [
           "float",
           "int"
         ],
         "ead": [
           "int"
         ],
         "instrument_id": [
           "str"
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
         "model_owner": [
           "str"
         ],
         "model_version_id": [
           "str"
         ],
         "prepayment_rate": [
           "int"
         ],
         "record_id": [
           "str"
         ],
         "record_status": [
           "str"
         ],
         "scenario_id": [
           "str"
         ],
         "source_record_id": [
           "str"
         ],
         "source_system": [
           "str"
         ],
         "valid_from": [
           "str"
         ],
         "valid_to": [
           "str"
         ],
         "validation_status": [
           "str"
         ],
         "version_no": [
           "int"
         ],
         "year": [
           "int"
         ]
       }
     },
     "scenarios": {
       "type": "table",
       "fields": {
         "approved_at": [
           "str"
         ],
         "approved_by": [
           "str"
         ],
         "as_of_date": [
           "str"
         ],
         "business_key": [
           "str"
         ],
         "forecast_horizon_years": [
           "int"
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
         "mean_reversion_method": [
           "str"
         ],
         "probability": [
           "float"
         ],
         "record_id": [
           "str"
         ],
         "record_status": [
           "str"
         ],
         "scenario_id": [
           "str"
         ],
         "scenario_version": [
           "str"
         ],
         "source_record_id": [
           "str"
         ],
         "source_system": [
           "str"
         ],
         "valid_from": [
           "str"
         ],
         "valid_to": [
           "str"
         ],
         "version_no": [
           "int"
         ]
       }
     },
     "events": {
       "type": "table",
       "fields": {}
     },
     "market_data": {
       "type": "table",
       "fields": {
         "as_of_date": [
           "str"
         ],
         "business_key": [
           "str"
         ],
         "day_one_difference": [
           "int"
         ],
         "fair_value": [
           "int"
         ],
         "fx_rate": [
           "int"
         ],
         "ifrs13_level": [
           "int"
         ],
         "instrument_id": [
           "str"
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
         "market_data_id": [
           "str"
         ],
         "own_credit_change": [
           "int"
         ],
         "own_credit_oci_mismatch": [
           "bool"
         ],
         "record_id": [
           "str"
         ],
         "record_status": [
           "str"
         ],
         "source_record_id": [
           "str"
         ],
         "source_system": [
           "str"
         ],
         "total_fv_change": [
           "int"
         ],
         "valid_from": [
           "str"
         ],
         "valid_to": [
           "str"
         ],
         "valuation_model": [
           "str"
         ],
         "valuation_status": [
           "str"
         ],
         "version_no": [
           "int"
         ]
       }
     },
     "hedges": {
       "type": "table",
       "fields": {}
     },
     "parameters": {
       "type": "table",
       "fields": {
         "as_of_date": [
           "str"
         ],
         "business_key": [
           "str"
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
         "parameter_id": [
           "str"
         ],
         "parameter_value": [
           "str"
         ],
         "policy_id": [
           "str"
         ],
         "record_id": [
           "str"
         ],
         "record_status": [
           "str"
         ],
         "rule_set_id": [
           "str"
         ],
         "source_record_id": [
           "str"
         ],
         "source_reference": [
           "str"
         ],
         "source_system": [
           "str"
         ],
         "unit": [
           "str"
         ],
         "valid_from": [
           "str"
         ],
         "valid_to": [
           "str"
         ],
         "version_no": [
           "int"
         ]
       }
     },
     "mappings": {
       "type": "table",
       "fields": {}
     },
     "backtesting": {
       "type": "table",
       "fields": {
         "actual_value": [
           "float",
           "int"
         ],
         "approval_id": [
           "str"
         ],
         "as_of_date": [
           "str"
         ],
         "business_key": [
           "str"
         ],
         "challenger_flag": [
           "bool"
         ],
         "exposure_weight": [
           "int"
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
         "model_owner": [
           "str"
         ],
         "model_type": [
           "str"
         ],
         "model_version_id": [
           "str"
         ],
         "observation_date": [
           "str"
         ],
         "observation_id": [
           "str"
         ],
         "outcome_flag": [
           "bool"
         ],
         "predicted_value": [
           "float",
           "int"
         ],
         "record_id": [
           "str"
         ],
         "record_status": [
           "str"
         ],
         "release_amount": [
           "int"
         ],
         "segment": [
           "str"
         ],
         "source_record_id": [
           "str"
         ],
         "source_system": [
           "str"
         ],
         "valid_from": [
           "str"
         ],
         "valid_to": [
           "str"
         ],
         "validation_status": [
           "str"
         ],
         "version_no": [
           "int"
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

``examples/analyst_workbook.py`` case ``load_reference_data`` supplies the arguments and an
independent expected-result assertion. Its function call is::

   import financial_accounting_engine as fae
   actual = fae.load_reference_data(*args, **kwargs)
   assert check(actual)

Executed pytest ID: ``tests/test_api.py::test_api_example[load_reference_data]``.
