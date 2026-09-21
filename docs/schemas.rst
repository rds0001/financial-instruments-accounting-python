Schemas
*******

Input fields
------------

All tables include canonical record/version/valid/known-time fields.
The following dictionary is preserved from the 1.1.0 input contract. Numeric
currency is instrument-local unless the field explicitly names presentation.
Conditional nullability depends on the selected approach. Runtime validation
adds strict numeric/boolean checks described in :doc:`contract`.

run_control
~~~~~~~~~~~

Workbook: ``FIA_IN_00_Run_Control.xlsx``.

.. list-table::
   :header-rows: 1

   * - Field
     - Declared type
     - Nullable / unit
   * - record_id
     - string/date
     - no; decimal/EUR as applicable
   * - business_key
     - string/date
     - no; decimal/EUR as applicable
   * - version_no
     - number
     - no; decimal/EUR as applicable
   * - as_of_date
     - string/date
     - no; decimal/EUR as applicable
   * - valid_from
     - string/date
     - conditional; decimal/EUR as applicable
   * - valid_to
     - string/date
     - conditional; decimal/EUR as applicable
   * - known_from
     - string/date
     - conditional; decimal/EUR as applicable
   * - known_to
     - string/date
     - conditional; decimal/EUR as applicable
   * - is_official
     - boolean
     - conditional; decimal/EUR as applicable
   * - record_status
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_system
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_record_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - run_key
     - string/date
     - conditional; decimal/EUR as applicable
   * - profile_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - policy_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - rule_set_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - contract_version
     - string/date
     - conditional; decimal/EUR as applicable
   * - reporting_date
     - string/date
     - conditional; decimal/EUR as applicable
   * - knowledge_time
     - string/date
     - conditional; decimal/EUR as applicable
   * - view
     - string/date
     - conditional; decimal/EUR as applicable

entities
~~~~~~~~

Workbook: ``FIA_IN_01_Entities_Scopes.xlsx``.

.. list-table::
   :header-rows: 1

   * - Field
     - Declared type
     - Nullable / unit
   * - record_id
     - string/date
     - no; decimal/EUR as applicable
   * - business_key
     - string/date
     - no; decimal/EUR as applicable
   * - version_no
     - number
     - no; decimal/EUR as applicable
   * - as_of_date
     - string/date
     - no; decimal/EUR as applicable
   * - valid_from
     - string/date
     - conditional; decimal/EUR as applicable
   * - valid_to
     - string/date
     - conditional; decimal/EUR as applicable
   * - known_from
     - string/date
     - conditional; decimal/EUR as applicable
   * - known_to
     - string/date
     - conditional; decimal/EUR as applicable
   * - is_official
     - boolean
     - conditional; decimal/EUR as applicable
   * - record_status
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_system
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_record_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - entity_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - entity_name
     - string/date
     - conditional; decimal/EUR as applicable
   * - functional_currency
     - string/date
     - conditional; decimal/EUR as applicable
   * - consolidation_scope
     - string/date
     - conditional; decimal/EUR as applicable

parties
~~~~~~~

Workbook: ``FIA_IN_02_Parties_Credit_Status.xlsx``.

.. list-table::
   :header-rows: 1

   * - Field
     - Declared type
     - Nullable / unit
   * - record_id
     - string/date
     - no; decimal/EUR as applicable
   * - business_key
     - string/date
     - no; decimal/EUR as applicable
   * - version_no
     - number
     - no; decimal/EUR as applicable
   * - as_of_date
     - string/date
     - no; decimal/EUR as applicable
   * - valid_from
     - string/date
     - conditional; decimal/EUR as applicable
   * - valid_to
     - string/date
     - conditional; decimal/EUR as applicable
   * - known_from
     - string/date
     - conditional; decimal/EUR as applicable
   * - known_to
     - string/date
     - conditional; decimal/EUR as applicable
   * - is_official
     - boolean
     - conditional; decimal/EUR as applicable
   * - record_status
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_system
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_record_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - party_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - rating_orig
     - string/date
     - conditional; decimal/EUR as applicable
   * - rating_current
     - string/date
     - conditional; decimal/EUR as applicable
   * - default_flag
     - string/date
     - conditional; decimal/EUR as applicable
   * - watchlist
     - boolean
     - conditional; decimal/EUR as applicable
   * - forbearance
     - boolean
     - conditional; decimal/EUR as applicable

instruments
~~~~~~~~~~~

Workbook: ``FIA_IN_03_Instruments_Contracts.xlsx``.

.. list-table::
   :header-rows: 1

   * - Field
     - Declared type
     - Nullable / unit
   * - record_id
     - string/date
     - no; decimal/EUR as applicable
   * - business_key
     - string/date
     - no; decimal/EUR as applicable
   * - version_no
     - number
     - no; decimal/EUR as applicable
   * - as_of_date
     - string/date
     - no; decimal/EUR as applicable
   * - valid_from
     - string/date
     - conditional; decimal/EUR as applicable
   * - valid_to
     - string/date
     - conditional; decimal/EUR as applicable
   * - known_from
     - string/date
     - conditional; decimal/EUR as applicable
   * - known_to
     - string/date
     - conditional; decimal/EUR as applicable
   * - is_official
     - boolean
     - conditional; decimal/EUR as applicable
   * - record_status
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_system
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_record_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - entity_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - instrument_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - instrument_type
     - string/date
     - conditional; decimal/EUR as applicable
   * - portfolio
     - string/date
     - conditional; decimal/EUR as applicable
   * - currency
     - string/date
     - conditional; decimal/EUR as applicable
   * - transaction_price
     - number
     - conditional; decimal/EUR as applicable
   * - gross_amount
     - number
     - conditional; decimal/EUR as applicable
   * - fair_value
     - number
     - conditional; decimal/EUR as applicable
   * - transaction_costs
     - number
     - conditional; decimal/EUR as applicable
   * - business_model
     - string/date
     - conditional; decimal/EUR as applicable
   * - liability
     - boolean
     - conditional; decimal/EUR as applicable
   * - equity
     - boolean
     - conditional; decimal/EUR as applicable
   * - held_for_trading
     - boolean
     - conditional; decimal/EUR as applicable
   * - fair_value_option
     - boolean
     - conditional; decimal/EUR as applicable
   * - fvoci_equity_election
     - boolean
     - conditional; decimal/EUR as applicable
   * - designation_approval_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - hybrid_contract
     - boolean
     - conditional; decimal/EUR as applicable
   * - host_contract_type
     - string/date
     - conditional; decimal/EUR as applicable
   * - embedded_derivative_separated
     - boolean
     - conditional; decimal/EUR as applicable
   * - contingent_feature
     - string/date
     - conditional; decimal/EUR as applicable
   * - simplified
     - boolean
     - conditional; decimal/EUR as applicable
   * - poci
     - boolean
     - conditional; decimal/EUR as applicable
   * - impairment_scope
     - string/date
     - conditional; decimal/EUR as applicable
   * - ecl_method
     - string/date
     - conditional; decimal/EUR as applicable
   * - provision_rate
     - number
     - conditional; decimal/EUR as applicable
   * - poci_initial_lifetime_ecl
     - number
     - conditional; decimal/EUR as applicable
   * - eir
     - number
     - conditional; decimal/EUR as applicable
   * - credit_adjusted_eir
     - number
     - conditional; decimal/EUR as applicable
   * - rate_type
     - string/date
     - conditional; decimal/EUR as applicable
   * - reset_rate
     - number
     - conditional; decimal/EUR as applicable
   * - undrawn
     - number
     - conditional; decimal/EUR as applicable
   * - guarantee_amount
     - number
     - conditional; decimal/EUR as applicable
   * - overlay
     - number
     - conditional; decimal/EUR as applicable
   * - overlay_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - overlay_owner
     - string/date
     - conditional; decimal/EUR as applicable
   * - overlay_approved
     - boolean
     - conditional; decimal/EUR as applicable
   * - overlay_expiry
     - string/date
     - conditional; decimal/EUR as applicable
   * - overlay_thesis
     - string/date
     - conditional; decimal/EUR as applicable
   * - overlay_double_count_checked
     - boolean
     - conditional; decimal/EUR as applicable
   * - initial_recognition_date
     - string/date
     - conditional; decimal/EUR as applicable
   * - maturity_date
     - string/date
     - conditional; decimal/EUR as applicable
   * - regular_way
     - boolean
     - conditional; decimal/EUR as applicable
   * - trade_date_policy
     - string/date
     - conditional; decimal/EUR as applicable
   * - electronic_payment_election
     - boolean
     - conditional; decimal/EUR as applicable
   * - payment_irrevocable
     - boolean
     - conditional; decimal/EUR as applicable
   * - withdrawal_access_practical
     - boolean
     - conditional; decimal/EUR as applicable
   * - settlement_risk_insignificant
     - boolean
     - conditional; decimal/EUR as applicable
   * - settlement_short_period
     - boolean
     - conditional; decimal/EUR as applicable
   * - scope_assessment
     - string/date
     - conditional; decimal/EUR as applicable
   * - recognition_status
     - string/date
     - conditional; decimal/EUR as applicable
   * - own_use
     - boolean
     - conditional; decimal/EUR as applicable
   * - nature_dependent_contract
     - boolean
     - conditional; decimal/EUR as applicable
   * - purchaser_net_buyer
     - boolean
     - conditional; decimal/EUR as applicable
   * - quantity_consistent_expected_usage
     - boolean
     - conditional; decimal/EUR as applicable
   * - sale_timing_uncontrollable
     - boolean
     - conditional; decimal/EUR as applicable
   * - repurchase_within_reasonable_time
     - boolean
     - conditional; decimal/EUR as applicable
   * - interface_standard
     - string/date
     - conditional; decimal/EUR as applicable
   * - interface_decision_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - interface_approved
     - boolean
     - conditional; decimal/EUR as applicable
   * - regulatory_approach
     - string/date
     - conditional; decimal/EUR as applicable
   * - regulatory_default_flag
     - boolean
     - conditional; decimal/EUR as applicable
   * - regulatory_expected_loss
     - number
     - conditional; decimal/EUR as applicable

cashflows
~~~~~~~~~

Workbook: ``FIA_IN_04_Cashflows_Fees_EIR.xlsx``.

.. list-table::
   :header-rows: 1

   * - Field
     - Declared type
     - Nullable / unit
   * - record_id
     - string/date
     - no; decimal/EUR as applicable
   * - business_key
     - string/date
     - no; decimal/EUR as applicable
   * - version_no
     - number
     - no; decimal/EUR as applicable
   * - as_of_date
     - string/date
     - no; decimal/EUR as applicable
   * - valid_from
     - string/date
     - conditional; decimal/EUR as applicable
   * - valid_to
     - string/date
     - conditional; decimal/EUR as applicable
   * - known_from
     - string/date
     - conditional; decimal/EUR as applicable
   * - known_to
     - string/date
     - conditional; decimal/EUR as applicable
   * - is_official
     - boolean
     - conditional; decimal/EUR as applicable
   * - record_status
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_system
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_record_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - cashflow_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - instrument_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - scenario_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - year_fraction
     - number
     - conditional; decimal/EUR as applicable
   * - amount
     - number
     - conditional; decimal/EUR as applicable
   * - cashflow_type
     - string/date
     - conditional; decimal/EUR as applicable
   * - contractual
     - boolean
     - conditional; decimal/EUR as applicable
   * - expected
     - boolean
     - conditional; decimal/EUR as applicable
   * - include_in_eir
     - boolean
     - conditional; decimal/EUR as applicable

opening_balances
~~~~~~~~~~~~~~~~

Workbook: ``FIA_IN_05_Accounting_Balances.xlsx``.

.. list-table::
   :header-rows: 1

   * - Field
     - Declared type
     - Nullable / unit
   * - record_id
     - string/date
     - no; decimal/EUR as applicable
   * - business_key
     - string/date
     - no; decimal/EUR as applicable
   * - version_no
     - number
     - no; decimal/EUR as applicable
   * - as_of_date
     - string/date
     - no; decimal/EUR as applicable
   * - valid_from
     - string/date
     - conditional; decimal/EUR as applicable
   * - valid_to
     - string/date
     - conditional; decimal/EUR as applicable
   * - known_from
     - string/date
     - conditional; decimal/EUR as applicable
   * - known_to
     - string/date
     - conditional; decimal/EUR as applicable
   * - is_official
     - boolean
     - conditional; decimal/EUR as applicable
   * - record_status
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_system
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_record_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - instrument_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - opening_gross
     - string/date
     - conditional; decimal/EUR as applicable
   * - opening_allowance
     - string/date
     - conditional; decimal/EUR as applicable
   * - opening_fvoci_reserve
     - string/date
     - conditional; decimal/EUR as applicable
   * - opening_hedge_reserve
     - string/date
     - conditional; decimal/EUR as applicable
   * - ledger_gross
     - string/date
     - conditional; decimal/EUR as applicable
   * - ledger_allowance
     - string/date
     - conditional; decimal/EUR as applicable

classification_inputs
~~~~~~~~~~~~~~~~~~~~~

Workbook: ``FIA_IN_06_Classification_SPPI.xlsx``.

.. list-table::
   :header-rows: 1

   * - Field
     - Declared type
     - Nullable / unit
   * - record_id
     - string/date
     - no; decimal/EUR as applicable
   * - business_key
     - string/date
     - no; decimal/EUR as applicable
   * - version_no
     - number
     - no; decimal/EUR as applicable
   * - as_of_date
     - string/date
     - no; decimal/EUR as applicable
   * - valid_from
     - string/date
     - conditional; decimal/EUR as applicable
   * - valid_to
     - string/date
     - conditional; decimal/EUR as applicable
   * - known_from
     - string/date
     - conditional; decimal/EUR as applicable
   * - known_to
     - string/date
     - conditional; decimal/EUR as applicable
   * - is_official
     - boolean
     - conditional; decimal/EUR as applicable
   * - record_status
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_system
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_record_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - instrument_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - business_model
     - string/date
     - conditional; decimal/EUR as applicable
   * - principal_consistent
     - boolean
     - conditional; decimal/EUR as applicable
   * - basic_interest
     - boolean
     - conditional; decimal/EUR as applicable
   * - leverage
     - boolean
     - conditional; decimal/EUR as applicable
   * - modified_time_value_pass
     - boolean
     - conditional; decimal/EUR as applicable
   * - prepayment_compensation_reasonable
     - boolean
     - conditional; decimal/EUR as applicable
   * - extension_basic
     - boolean
     - conditional; decimal/EUR as applicable
   * - non_recourse_pass
     - boolean
     - conditional; decimal/EUR as applicable
   * - cli_lookthrough_pass
     - boolean
     - conditional; decimal/EUR as applicable
   * - contingent_feature_basic
     - boolean
     - conditional; decimal/EUR as applicable
   * - de_minimis_or_non_genuine
     - boolean
     - conditional; decimal/EUR as applicable
   * - sppi_override
     - string/date
     - conditional; decimal/EUR as applicable
   * - designation
     - string/date
     - conditional; decimal/EUR as applicable
   * - approval_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - business_model_change
     - boolean
     - conditional; decimal/EUR as applicable

collateral
~~~~~~~~~~

Workbook: ``FIA_IN_07_Collateral_Recoveries.xlsx``.

.. list-table::
   :header-rows: 1

   * - Field
     - Declared type
     - Nullable / unit
   * - record_id
     - string/date
     - no; decimal/EUR as applicable
   * - business_key
     - string/date
     - no; decimal/EUR as applicable
   * - version_no
     - number
     - no; decimal/EUR as applicable
   * - as_of_date
     - string/date
     - no; decimal/EUR as applicable
   * - valid_from
     - string/date
     - conditional; decimal/EUR as applicable
   * - valid_to
     - string/date
     - conditional; decimal/EUR as applicable
   * - known_from
     - string/date
     - conditional; decimal/EUR as applicable
   * - known_to
     - string/date
     - conditional; decimal/EUR as applicable
   * - is_official
     - boolean
     - conditional; decimal/EUR as applicable
   * - record_status
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_system
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_record_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - collateral_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - instrument_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - collateral_type
     - string/date
     - conditional; decimal/EUR as applicable
   * - fair_value
     - number
     - conditional; decimal/EUR as applicable
   * - haircut
     - number
     - conditional; decimal/EUR as applicable
   * - cost
     - number
     - conditional; decimal/EUR as applicable
   * - recovery_year
     - number
     - conditional; decimal/EUR as applicable
   * - allocated_amount
     - number
     - conditional; decimal/EUR as applicable
   * - separately_recognised
     - boolean
     - conditional; decimal/EUR as applicable

staging_inputs
~~~~~~~~~~~~~~

Workbook: ``FIA_IN_08_Staging_SICR.xlsx``.

.. list-table::
   :header-rows: 1

   * - Field
     - Declared type
     - Nullable / unit
   * - record_id
     - string/date
     - no; decimal/EUR as applicable
   * - business_key
     - string/date
     - no; decimal/EUR as applicable
   * - version_no
     - number
     - no; decimal/EUR as applicable
   * - as_of_date
     - string/date
     - no; decimal/EUR as applicable
   * - valid_from
     - string/date
     - conditional; decimal/EUR as applicable
   * - valid_to
     - string/date
     - conditional; decimal/EUR as applicable
   * - known_from
     - string/date
     - conditional; decimal/EUR as applicable
   * - known_to
     - string/date
     - conditional; decimal/EUR as applicable
   * - is_official
     - boolean
     - conditional; decimal/EUR as applicable
   * - record_status
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_system
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_record_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - instrument_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - impairment_scope
     - string/date
     - conditional; decimal/EUR as applicable
   * - prior_stage
     - string/date
     - conditional; decimal/EUR as applicable
   * - days_past_due
     - number
     - conditional; decimal/EUR as applicable
   * - rating_orig
     - string/date
     - conditional; decimal/EUR as applicable
   * - rating_current
     - string/date
     - conditional; decimal/EUR as applicable
   * - lifetime_pd_orig
     - number
     - conditional; decimal/EUR as applicable
   * - lifetime_pd_current
     - number
     - conditional; decimal/EUR as applicable
   * - watchlist
     - boolean
     - conditional; decimal/EUR as applicable
   * - forbearance
     - boolean
     - conditional; decimal/EUR as applicable
   * - unlikely_to_pay
     - boolean
     - conditional; decimal/EUR as applicable
   * - forward_looking_sicr
     - boolean
     - conditional; decimal/EUR as applicable
   * - credit_impaired
     - boolean
     - conditional; decimal/EUR as applicable
   * - simplified
     - boolean
     - conditional; decimal/EUR as applicable
   * - poci
     - boolean
     - conditional; decimal/EUR as applicable
   * - low_credit_risk
     - boolean
     - conditional; decimal/EUR as applicable
   * - collective_assessment
     - boolean
     - conditional; decimal/EUR as applicable
   * - sicr_rebuttal
     - boolean
     - conditional; decimal/EUR as applicable
   * - sicr_override
     - string/date
     - conditional; decimal/EUR as applicable
   * - override_reason
     - string/date
     - conditional; decimal/EUR as applicable
   * - override_approved
     - boolean
     - conditional; decimal/EUR as applicable
   * - override_expiry
     - string/date
     - conditional; decimal/EUR as applicable
   * - months_since_cure
     - number
     - conditional; decimal/EUR as applicable
   * - months_since_forbearance
     - number
     - conditional; decimal/EUR as applicable

pd_curves
~~~~~~~~~

Workbook: ``FIA_IN_09_PD_Models_Curves.xlsx``.

.. list-table::
   :header-rows: 1

   * - Field
     - Declared type
     - Nullable / unit
   * - record_id
     - string/date
     - no; decimal/EUR as applicable
   * - business_key
     - string/date
     - no; decimal/EUR as applicable
   * - version_no
     - number
     - no; decimal/EUR as applicable
   * - as_of_date
     - string/date
     - no; decimal/EUR as applicable
   * - valid_from
     - string/date
     - conditional; decimal/EUR as applicable
   * - valid_to
     - string/date
     - conditional; decimal/EUR as applicable
   * - known_from
     - string/date
     - conditional; decimal/EUR as applicable
   * - known_to
     - string/date
     - conditional; decimal/EUR as applicable
   * - is_official
     - boolean
     - conditional; decimal/EUR as applicable
   * - record_status
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_system
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_record_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - instrument_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - scenario_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - year
     - number
     - conditional; decimal/EUR as applicable
   * - marginal_pd
     - number
     - conditional; decimal/EUR as applicable
   * - model_version_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - model_owner
     - string/date
     - conditional; decimal/EUR as applicable
   * - validation_status
     - string/date
     - conditional; decimal/EUR as applicable
   * - approval_id
     - string/date
     - conditional; decimal/EUR as applicable

lgd_profiles
~~~~~~~~~~~~

Workbook: ``FIA_IN_10_LGD_Models.xlsx``.

.. list-table::
   :header-rows: 1

   * - Field
     - Declared type
     - Nullable / unit
   * - record_id
     - string/date
     - no; decimal/EUR as applicable
   * - business_key
     - string/date
     - no; decimal/EUR as applicable
   * - version_no
     - number
     - no; decimal/EUR as applicable
   * - as_of_date
     - string/date
     - no; decimal/EUR as applicable
   * - valid_from
     - string/date
     - conditional; decimal/EUR as applicable
   * - valid_to
     - string/date
     - conditional; decimal/EUR as applicable
   * - known_from
     - string/date
     - conditional; decimal/EUR as applicable
   * - known_to
     - string/date
     - conditional; decimal/EUR as applicable
   * - is_official
     - boolean
     - conditional; decimal/EUR as applicable
   * - record_status
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_system
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_record_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - instrument_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - scenario_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - year
     - number
     - conditional; decimal/EUR as applicable
   * - resolution_path
     - string/date
     - conditional; decimal/EUR as applicable
   * - lgd
     - number
     - conditional; decimal/EUR as applicable
   * - recovery_present_value
     - string/date
     - conditional; decimal/EUR as applicable
   * - workout_cost
     - string/date
     - conditional; decimal/EUR as applicable
   * - model_version_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - model_owner
     - string/date
     - conditional; decimal/EUR as applicable
   * - validation_status
     - string/date
     - conditional; decimal/EUR as applicable
   * - approval_id
     - string/date
     - conditional; decimal/EUR as applicable

ead_profiles
~~~~~~~~~~~~

Workbook: ``FIA_IN_11_EAD_CCF_Profiles.xlsx``.

.. list-table::
   :header-rows: 1

   * - Field
     - Declared type
     - Nullable / unit
   * - record_id
     - string/date
     - no; decimal/EUR as applicable
   * - business_key
     - string/date
     - no; decimal/EUR as applicable
   * - version_no
     - number
     - no; decimal/EUR as applicable
   * - as_of_date
     - string/date
     - no; decimal/EUR as applicable
   * - valid_from
     - string/date
     - conditional; decimal/EUR as applicable
   * - valid_to
     - string/date
     - conditional; decimal/EUR as applicable
   * - known_from
     - string/date
     - conditional; decimal/EUR as applicable
   * - known_to
     - string/date
     - conditional; decimal/EUR as applicable
   * - is_official
     - boolean
     - conditional; decimal/EUR as applicable
   * - record_status
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_system
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_record_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - instrument_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - scenario_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - year
     - number
     - conditional; decimal/EUR as applicable
   * - ead
     - number
     - conditional; decimal/EUR as applicable
   * - ccf
     - number
     - conditional; decimal/EUR as applicable
   * - prepayment_rate
     - string/date
     - conditional; decimal/EUR as applicable
   * - behavioural_horizon_years
     - string/date
     - conditional; decimal/EUR as applicable
   * - model_version_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - model_owner
     - string/date
     - conditional; decimal/EUR as applicable
   * - validation_status
     - string/date
     - conditional; decimal/EUR as applicable
   * - approval_id
     - string/date
     - conditional; decimal/EUR as applicable

scenarios
~~~~~~~~~

Workbook: ``FIA_IN_12_Macro_Scenarios.xlsx``.

.. list-table::
   :header-rows: 1

   * - Field
     - Declared type
     - Nullable / unit
   * - record_id
     - string/date
     - no; decimal/EUR as applicable
   * - business_key
     - string/date
     - no; decimal/EUR as applicable
   * - version_no
     - number
     - no; decimal/EUR as applicable
   * - as_of_date
     - string/date
     - no; decimal/EUR as applicable
   * - valid_from
     - string/date
     - conditional; decimal/EUR as applicable
   * - valid_to
     - string/date
     - conditional; decimal/EUR as applicable
   * - known_from
     - string/date
     - conditional; decimal/EUR as applicable
   * - known_to
     - string/date
     - conditional; decimal/EUR as applicable
   * - is_official
     - boolean
     - conditional; decimal/EUR as applicable
   * - record_status
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_system
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_record_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - scenario_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - probability
     - number
     - conditional; decimal/EUR as applicable
   * - scenario_version
     - string/date
     - conditional; decimal/EUR as applicable
   * - forecast_horizon_years
     - string/date
     - conditional; decimal/EUR as applicable
   * - mean_reversion_method
     - string/date
     - conditional; decimal/EUR as applicable
   * - approved_by
     - string/date
     - conditional; decimal/EUR as applicable
   * - approved_at
     - string/date
     - conditional; decimal/EUR as applicable

events
~~~~~~

Workbook: ``FIA_IN_13_Modifications_Writeoffs.xlsx``.

.. list-table::
   :header-rows: 1

   * - Field
     - Declared type
     - Nullable / unit
   * - record_id
     - string/date
     - no; decimal/EUR as applicable
   * - business_key
     - string/date
     - no; decimal/EUR as applicable
   * - version_no
     - number
     - no; decimal/EUR as applicable
   * - as_of_date
     - string/date
     - no; decimal/EUR as applicable
   * - valid_from
     - string/date
     - conditional; decimal/EUR as applicable
   * - valid_to
     - string/date
     - conditional; decimal/EUR as applicable
   * - known_from
     - string/date
     - conditional; decimal/EUR as applicable
   * - known_to
     - string/date
     - conditional; decimal/EUR as applicable
   * - is_official
     - boolean
     - conditional; decimal/EUR as applicable
   * - record_status
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_system
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_record_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - event_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - instrument_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - event_type
     - string/date
     - conditional; decimal/EUR as applicable
   * - amount
     - number
     - conditional; decimal/EUR as applicable
   * - event_date
     - string/date
     - conditional; decimal/EUR as applicable
   * - approved
     - boolean
     - conditional; decimal/EUR as applicable
   * - qualitative_substantial
     - boolean
     - conditional; decimal/EUR as applicable
   * - ten_percent_ratio
     - number
     - conditional; decimal/EUR as applicable
   * - modified_present_value
     - number
     - conditional; decimal/EUR as applicable
   * - derecognition_approved
     - boolean
     - conditional; decimal/EUR as applicable
   * - risks_rewards_transferred
     - boolean
     - conditional; decimal/EUR as applicable
   * - risks_rewards_retained
     - boolean
     - conditional; decimal/EUR as applicable
   * - control_retained
     - boolean
     - conditional; decimal/EUR as applicable
   * - pass_through_arrangement
     - boolean
     - conditional; decimal/EUR as applicable
   * - partial_transfer
     - boolean
     - conditional; decimal/EUR as applicable
   * - continuing_involvement_amount
     - number
     - conditional; decimal/EUR as applicable
   * - reason_code
     - string/date
     - conditional; decimal/EUR as applicable

market_data
~~~~~~~~~~~

Workbook: ``FIA_IN_14_Fair_Value_Market_Data.xlsx``.

.. list-table::
   :header-rows: 1

   * - Field
     - Declared type
     - Nullable / unit
   * - record_id
     - string/date
     - no; decimal/EUR as applicable
   * - business_key
     - string/date
     - no; decimal/EUR as applicable
   * - version_no
     - number
     - no; decimal/EUR as applicable
   * - as_of_date
     - string/date
     - no; decimal/EUR as applicable
   * - valid_from
     - string/date
     - conditional; decimal/EUR as applicable
   * - valid_to
     - string/date
     - conditional; decimal/EUR as applicable
   * - known_from
     - string/date
     - conditional; decimal/EUR as applicable
   * - known_to
     - string/date
     - conditional; decimal/EUR as applicable
   * - is_official
     - boolean
     - conditional; decimal/EUR as applicable
   * - record_status
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_system
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_record_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - market_data_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - instrument_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - fair_value
     - number
     - conditional; decimal/EUR as applicable
   * - fx_rate
     - number
     - conditional; decimal/EUR as applicable
   * - ifrs13_level
     - string/date
     - conditional; decimal/EUR as applicable
   * - valuation_model
     - string/date
     - conditional; decimal/EUR as applicable
   * - valuation_status
     - string/date
     - conditional; decimal/EUR as applicable
   * - total_fv_change
     - number
     - conditional; decimal/EUR as applicable
   * - own_credit_change
     - number
     - conditional; decimal/EUR as applicable
   * - own_credit_oci_mismatch
     - string/date
     - conditional; decimal/EUR as applicable
   * - day_one_difference
     - number
     - conditional; decimal/EUR as applicable

hedges
~~~~~~

Workbook: ``FIA_IN_15_Hedge_Accounting.xlsx``.

.. list-table::
   :header-rows: 1

   * - Field
     - Declared type
     - Nullable / unit
   * - record_id
     - string/date
     - no; decimal/EUR as applicable
   * - business_key
     - string/date
     - no; decimal/EUR as applicable
   * - version_no
     - number
     - no; decimal/EUR as applicable
   * - as_of_date
     - string/date
     - no; decimal/EUR as applicable
   * - valid_from
     - string/date
     - conditional; decimal/EUR as applicable
   * - valid_to
     - string/date
     - conditional; decimal/EUR as applicable
   * - known_from
     - string/date
     - conditional; decimal/EUR as applicable
   * - known_to
     - string/date
     - conditional; decimal/EUR as applicable
   * - is_official
     - boolean
     - conditional; decimal/EUR as applicable
   * - record_status
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_system
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_record_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - relationship_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - hedge_type
     - string/date
     - conditional; decimal/EUR as applicable
   * - hedging_instrument_eligible
     - boolean
     - conditional; decimal/EUR as applicable
   * - hedged_item_eligible
     - boolean
     - conditional; decimal/EUR as applicable
   * - risk_component_eligible
     - boolean
     - conditional; decimal/EUR as applicable
   * - designation_documented
     - boolean
     - conditional; decimal/EUR as applicable
   * - risk_management_objective
     - string/date
     - conditional; decimal/EUR as applicable
   * - hedging_change
     - number
     - conditional; decimal/EUR as applicable
   * - hedged_change
     - number
     - conditional; decimal/EUR as applicable
   * - designated
     - boolean
     - conditional; decimal/EUR as applicable
   * - economic_relationship
     - boolean
     - conditional; decimal/EUR as applicable
   * - credit_risk_dominates
     - boolean
     - conditional; decimal/EUR as applicable
   * - hedge_ratio
     - number
     - conditional; decimal/EUR as applicable
   * - target_hedge_ratio
     - number
     - conditional; decimal/EUR as applicable
   * - rebalancing_required
     - boolean
     - conditional; decimal/EUR as applicable
   * - discontinue
     - boolean
     - conditional; decimal/EUR as applicable
   * - forecast_transaction_expected
     - boolean
     - conditional; decimal/EUR as applicable
   * - nature_dependent_electricity_hedge
     - boolean
     - conditional; decimal/EUR as applicable
   * - variable_nominal_volume
     - boolean
     - conditional; decimal/EUR as applicable
   * - volume_assumptions_documented
     - boolean
     - conditional; decimal/EUR as applicable
   * - option_time_value_change
     - number
     - conditional; decimal/EUR as applicable
   * - forward_element_change
     - number
     - conditional; decimal/EUR as applicable
   * - basis_spread_change
     - number
     - conditional; decimal/EUR as applicable
   * - recycle_amount
     - number
     - conditional; decimal/EUR as applicable
   * - basis_adjustment
     - number
     - conditional; decimal/EUR as applicable

parameters
~~~~~~~~~~

Workbook: ``FIA_IN_16_Rules_Parameters.xlsx``.

.. list-table::
   :header-rows: 1

   * - Field
     - Declared type
     - Nullable / unit
   * - record_id
     - string/date
     - no; decimal/EUR as applicable
   * - business_key
     - string/date
     - no; decimal/EUR as applicable
   * - version_no
     - number
     - no; decimal/EUR as applicable
   * - as_of_date
     - string/date
     - no; decimal/EUR as applicable
   * - valid_from
     - string/date
     - conditional; decimal/EUR as applicable
   * - valid_to
     - string/date
     - conditional; decimal/EUR as applicable
   * - known_from
     - string/date
     - conditional; decimal/EUR as applicable
   * - known_to
     - string/date
     - conditional; decimal/EUR as applicable
   * - is_official
     - boolean
     - conditional; decimal/EUR as applicable
   * - record_status
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_system
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_record_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - parameter_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - parameter_value
     - string/date
     - conditional; decimal/EUR as applicable
   * - unit
     - string/date
     - conditional; decimal/EUR as applicable
   * - policy_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - rule_set_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_reference
     - string/date
     - conditional; decimal/EUR as applicable

mappings
~~~~~~~~

Workbook: ``FIA_IN_17_Bank_Mappings.xlsx``.

.. list-table::
   :header-rows: 1

   * - Field
     - Declared type
     - Nullable / unit
   * - record_id
     - string/date
     - no; decimal/EUR as applicable
   * - business_key
     - string/date
     - no; decimal/EUR as applicable
   * - version_no
     - number
     - no; decimal/EUR as applicable
   * - as_of_date
     - string/date
     - no; decimal/EUR as applicable
   * - valid_from
     - string/date
     - conditional; decimal/EUR as applicable
   * - valid_to
     - string/date
     - conditional; decimal/EUR as applicable
   * - known_from
     - string/date
     - conditional; decimal/EUR as applicable
   * - known_to
     - string/date
     - conditional; decimal/EUR as applicable
   * - is_official
     - boolean
     - conditional; decimal/EUR as applicable
   * - record_status
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_system
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_record_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - mapping_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - mapping_type
     - string/date
     - conditional; decimal/EUR as applicable
   * - external_value
     - string/date
     - conditional; decimal/EUR as applicable
   * - canonical_value
     - string/date
     - conditional; decimal/EUR as applicable

backtesting
~~~~~~~~~~~

Workbook: ``FIA_IN_18_Backtesting_Observations.xlsx``.

.. list-table::
   :header-rows: 1

   * - Field
     - Declared type
     - Nullable / unit
   * - record_id
     - string/date
     - no; decimal/EUR as applicable
   * - business_key
     - string/date
     - no; decimal/EUR as applicable
   * - version_no
     - number
     - no; decimal/EUR as applicable
   * - as_of_date
     - string/date
     - no; decimal/EUR as applicable
   * - valid_from
     - string/date
     - conditional; decimal/EUR as applicable
   * - valid_to
     - string/date
     - conditional; decimal/EUR as applicable
   * - known_from
     - string/date
     - conditional; decimal/EUR as applicable
   * - known_to
     - string/date
     - conditional; decimal/EUR as applicable
   * - is_official
     - boolean
     - conditional; decimal/EUR as applicable
   * - record_status
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_system
     - string/date
     - conditional; decimal/EUR as applicable
   * - source_record_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - observation_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - model_type
     - string/date
     - conditional; decimal/EUR as applicable
   * - model_version_id
     - string/date
     - conditional; decimal/EUR as applicable
   * - challenger_flag
     - boolean
     - conditional; decimal/EUR as applicable
   * - segment
     - string/date
     - conditional; decimal/EUR as applicable
   * - observation_date
     - string/date
     - conditional; decimal/EUR as applicable
   * - predicted_value
     - number
     - conditional; decimal/EUR as applicable
   * - actual_value
     - number
     - conditional; decimal/EUR as applicable
   * - exposure_weight
     - number
     - conditional; decimal/EUR as applicable
   * - outcome_flag
     - boolean
     - conditional; decimal/EUR as applicable
   * - release_amount
     - number
     - conditional; decimal/EUR as applicable
   * - model_owner
     - string/date
     - conditional; decimal/EUR as applicable
   * - validation_status
     - string/date
     - conditional; decimal/EUR as applicable
   * - approval_id
     - string/date
     - conditional; decimal/EUR as applicable

Output tables
-------------

All domain tables carry object IDs, formula/rule references and run lineage where applicable.

00_Summary/CONTROLS
~~~~~~~~~~~~~~~~~~~

Field names and observed types::

   {
     "type": "table",
     "fields": {
       "actual": [
         "bool",
         "float",
         "int"
       ],
       "control_id": [
         "str"
       ],
       "expected": [
         "bool",
         "float",
         "int"
       ],
       "explanation": [
         "str"
       ],
       "status": [
         "str"
       ],
       "tolerance": [
         "float"
       ]
     }
   }

00_Summary/SUMMARY
~~~~~~~~~~~~~~~~~~

Field names and observed types::

   {
     "type": "table",
     "fields": {
       "metric": [
         "str"
       ],
       "value": [
         "float",
         "int"
       ]
     }
   }

01_Classification/CLASSIFICATION_SPPI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Field names and observed types::

   {
     "type": "table",
     "fields": {
       "accounting_policy_id": [
         "str"
       ],
       "as_of_date": [
         "str"
       ],
       "classification": [
         "str"
       ],
       "decision_rule_id": [
         "str"
       ],
       "formula_id": [
         "NoneType"
       ],
       "instrument_id": [
         "str"
       ],
       "knowledge_time": [
         "str"
       ],
       "official_flag": [
         "bool"
       ],
       "reclassification_status": [
         "str"
       ],
       "result_version": [
         "str"
       ],
       "rule_set_id": [
         "str"
       ],
       "run_id": [
         "str"
       ],
       "source_object_id": [
         "str"
       ],
       "source_reference": [
         "str"
       ],
       "sppi_reason": [
         "str"
       ],
       "sppi_result": [
         "str"
       ],
       "view": [
         "str"
       ]
     }
   }

01_Classification/DERECOGNITION
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Field names and observed types::

   {
     "type": "table",
     "fields": {
       "accounting_policy_id": [
         "str"
       ],
       "amount": [
         "float"
       ],
       "as_of_date": [
         "str"
       ],
       "continuing_involvement": [
         "float"
       ],
       "derecognition_result": [
         "str"
       ],
       "event_id": [
         "str"
       ],
       "event_type": [
         "str"
       ],
       "formula_id": [
         "str"
       ],
       "instrument_id": [
         "str"
       ],
       "knowledge_time": [
         "str"
       ],
       "modification_result": [
         "float"
       ],
       "official_flag": [
         "bool"
       ],
       "pnl_effect": [
         "float"
       ],
       "reason_code": [
         "str"
       ],
       "result_version": [
         "str"
       ],
       "rule_set_id": [
         "str"
       ],
       "run_id": [
         "str"
       ],
       "source_object_id": [
         "str"
       ],
       "view": [
         "str"
       ]
     }
   }

01_Classification/SCOPE_RECOGNITION
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Field names and observed types::

   {
     "type": "table",
     "fields": {
       "accounting_policy_id": [
         "str"
       ],
       "as_of_date": [
         "str"
       ],
       "controlled_interface": [
         "str"
       ],
       "decision_rule_id": [
         "str"
       ],
       "electronic_payment_result": [
         "str"
       ],
       "formula_id": [
         "NoneType"
       ],
       "instrument_id": [
         "str"
       ],
       "interface_decision_id": [
         "NoneType"
       ],
       "knowledge_time": [
         "str"
       ],
       "official_flag": [
         "bool"
       ],
       "recognition_event": [
         "str"
       ],
       "regular_way_policy": [
         "str"
       ],
       "result_version": [
         "str"
       ],
       "rule_set_id": [
         "str"
       ],
       "run_id": [
         "str"
       ],
       "scope_decision": [
         "str"
       ],
       "source_object_id": [
         "str"
       ],
       "source_reference": [
         "str"
       ],
       "view": [
         "str"
       ]
     }
   }

02_Measurement_EIR/AMORTISED_COST
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Field names and observed types::

   {
     "type": "table",
     "fields": {
       "accounting_policy_id": [
         "str"
       ],
       "applied_rate": [
         "float"
       ],
       "as_of_date": [
         "str"
       ],
       "cash_received": [
         "float",
         "int"
       ],
       "closing_gross": [
         "float"
       ],
       "formula_id": [
         "str"
       ],
       "instrument_id": [
         "str"
       ],
       "interest": [
         "float"
       ],
       "knowledge_time": [
         "str"
       ],
       "official_flag": [
         "bool"
       ],
       "opening_gross": [
         "float"
       ],
       "original_eir": [
         "float"
       ],
       "rate_method": [
         "str"
       ],
       "result_version": [
         "str"
       ],
       "rule_set_id": [
         "str"
       ],
       "run_id": [
         "str"
       ],
       "source_object_id": [
         "str"
       ],
       "source_reference": [
         "str"
       ],
       "view": [
         "str"
       ]
     }
   }

02_Measurement_EIR/EIR
~~~~~~~~~~~~~~~~~~~~~~

Field names and observed types::

   {
     "type": "table",
     "fields": {
       "accounting_policy_id": [
         "str"
       ],
       "as_of_date": [
         "str"
       ],
       "calculated_eir": [
         "NoneType",
         "float"
       ],
       "contractual_eir": [
         "float",
         "int"
       ],
       "eir_method": [
         "str"
       ],
       "formula_id": [
         "str"
       ],
       "instrument_id": [
         "str"
       ],
       "knowledge_time": [
         "str"
       ],
       "official_flag": [
         "bool"
       ],
       "result_version": [
         "str"
       ],
       "rule_set_id": [
         "str"
       ],
       "run_id": [
         "str"
       ],
       "source_object_id": [
         "str"
       ],
       "source_reference": [
         "str"
       ],
       "view": [
         "str"
       ]
     }
   }

02_Measurement_EIR/FAIR_VALUE
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Field names and observed types::

   {
     "type": "table",
     "fields": {
       "accounting_policy_id": [
         "str"
       ],
       "as_of_date": [
         "str"
       ],
       "classification": [
         "str"
       ],
       "fair_value": [
         "float"
       ],
       "formula_id": [
         "str"
       ],
       "ifrs13_level": [
         "int"
       ],
       "instrument_id": [
         "str"
       ],
       "knowledge_time": [
         "str"
       ],
       "oci_fv_change": [
         "float"
       ],
       "official_flag": [
         "bool"
       ],
       "pnl_fv_change": [
         "float"
       ],
       "recycling_policy": [
         "str"
       ],
       "result_version": [
         "str"
       ],
       "rule_set_id": [
         "str"
       ],
       "run_id": [
         "str"
       ],
       "source_object_id": [
         "str"
       ],
       "source_reference": [
         "str"
       ],
       "total_fv_change": [
         "float"
       ],
       "valuation_model": [
         "str"
       ],
       "valuation_status": [
         "str"
       ],
       "view": [
         "str"
       ]
     }
   }

02_Measurement_EIR/INITIAL_MEASUREMENT
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Field names and observed types::

   {
     "type": "table",
     "fields": {
       "accounting_policy_id": [
         "str"
       ],
       "as_of_date": [
         "str"
       ],
       "day_one_difference": [
         "float"
       ],
       "formula_id": [
         "str"
       ],
       "initial_carrying_amount": [
         "float"
       ],
       "instrument_id": [
         "str"
       ],
       "knowledge_time": [
         "str"
       ],
       "official_flag": [
         "bool"
       ],
       "result_version": [
         "str"
       ],
       "rule_set_id": [
         "str"
       ],
       "run_id": [
         "str"
       ],
       "source_object_id": [
         "str"
       ],
       "source_reference": [
         "str"
       ],
       "transaction_cost_treatment": [
         "str"
       ],
       "view": [
         "str"
       ]
     }
   }

02_Measurement_EIR/INTEREST_REVENUE
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Field names and observed types::

   {
     "type": "table",
     "fields": {
       "accounting_policy_id": [
         "str"
       ],
       "as_of_date": [
         "str"
       ],
       "formula_id": [
         "str"
       ],
       "instrument_id": [
         "str"
       ],
       "interest_basis": [
         "float"
       ],
       "interest_method": [
         "str"
       ],
       "interest_rate": [
         "float"
       ],
       "interest_revenue": [
         "float"
       ],
       "knowledge_time": [
         "str"
       ],
       "official_flag": [
         "bool"
       ],
       "result_version": [
         "str"
       ],
       "rule_set_id": [
         "str"
       ],
       "run_id": [
         "str"
       ],
       "source_object_id": [
         "str"
       ],
       "source_reference": [
         "str"
       ],
       "view": [
         "str"
       ]
     }
   }

02_Measurement_EIR/MODIFICATIONS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Field names and observed types::

   {
     "type": "table",
     "fields": {
       "accounting_policy_id": [
         "str"
       ],
       "amount": [
         "float"
       ],
       "as_of_date": [
         "str"
       ],
       "continuing_involvement": [
         "float"
       ],
       "derecognition_result": [
         "str"
       ],
       "event_id": [
         "str"
       ],
       "event_type": [
         "str"
       ],
       "formula_id": [
         "str"
       ],
       "instrument_id": [
         "str"
       ],
       "knowledge_time": [
         "str"
       ],
       "modification_result": [
         "float"
       ],
       "official_flag": [
         "bool"
       ],
       "pnl_effect": [
         "float"
       ],
       "reason_code": [
         "str"
       ],
       "result_version": [
         "str"
       ],
       "rule_set_id": [
         "str"
       ],
       "run_id": [
         "str"
       ],
       "source_object_id": [
         "str"
       ],
       "view": [
         "str"
       ]
     }
   }

02_Measurement_EIR/OWN_CREDIT
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Field names and observed types::

   {
     "type": "table",
     "fields": {
       "accounting_policy_id": [
         "str"
       ],
       "as_of_date": [
         "str"
       ],
       "formula_id": [
         "str"
       ],
       "instrument_id": [
         "str"
       ],
       "knowledge_time": [
         "str"
       ],
       "official_flag": [
         "bool"
       ],
       "other_fv_change_pnl": [
         "float"
       ],
       "own_credit_oci": [
         "float"
       ],
       "own_credit_pnl_due_to_mismatch": [
         "float"
       ],
       "result_version": [
         "str"
       ],
       "rule_set_id": [
         "str"
       ],
       "run_id": [
         "str"
       ],
       "source_object_id": [
         "str"
       ],
       "source_reference": [
         "str"
       ],
       "total_fv_change": [
         "float"
       ],
       "view": [
         "str"
       ]
     }
   }

03_Impairment_ECL/CREDIT_ENHANCEMENTS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Field names and observed types::

   {
     "type": "table",
     "fields": {
       "accounting_policy_id": [
         "str"
       ],
       "allocated_amount": [
         "float"
       ],
       "as_of_date": [
         "str"
       ],
       "available_protection": [
         "float"
       ],
       "collateral_id": [
         "str"
       ],
       "formula_id": [
         "str"
       ],
       "included_in_ecl": [
         "bool"
       ],
       "instrument_id": [
         "str"
       ],
       "knowledge_time": [
         "str"
       ],
       "official_flag": [
         "bool"
       ],
       "recovery_year": [
         "int"
       ],
       "result_version": [
         "str"
       ],
       "rule_set_id": [
         "str"
       ],
       "run_id": [
         "str"
       ],
       "source_object_id": [
         "str"
       ],
       "source_reference": [
         "str"
       ],
       "view": [
         "str"
       ]
     }
   }

03_Impairment_ECL/ECL_COMPONENTS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Field names and observed types::

   {
     "type": "table",
     "fields": {
       "accounting_policy_id": [
         "str"
       ],
       "as_of_date": [
         "str"
       ],
       "discounted_ecl": [
         "float"
       ],
       "discounted_ecl_local": [
         "float"
       ],
       "ead": [
         "NoneType",
         "float",
         "int"
       ],
       "formula_id": [
         "str"
       ],
       "fx_rate": [
         "float"
       ],
       "instrument_id": [
         "str"
       ],
       "knowledge_time": [
         "str"
       ],
       "lgd": [
         "NoneType",
         "float"
       ],
       "marginal_pd": [
         "NoneType",
         "float"
       ],
       "official_flag": [
         "bool"
       ],
       "result_version": [
         "str"
       ],
       "rule_set_id": [
         "str"
       ],
       "run_id": [
         "str"
       ],
       "scenario_id": [
         "str"
       ],
       "source_object_id": [
         "str"
       ],
       "view": [
         "str"
       ],
       "year": [
         "int"
       ]
     }
   }

03_Impairment_ECL/ECL_RESULTS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Field names and observed types::

   {
     "type": "table",
     "fields": {
       "accounting_policy_id": [
         "str"
       ],
       "as_of_date": [
         "str"
       ],
       "ecl_method": [
         "str"
       ],
       "final_ecl": [
         "float"
       ],
       "final_ecl_local": [
         "float"
       ],
       "formula_id": [
         "str"
       ],
       "fx_rate": [
         "float"
       ],
       "instrument_id": [
         "str"
       ],
       "knowledge_time": [
         "str"
       ],
       "model_version_id": [
         "str"
       ],
       "official_flag": [
         "bool"
       ],
       "overlay": [
         "float"
       ],
       "poci_initial_lifetime_ecl": [
         "float"
       ],
       "prior_stage": [
         "str"
       ],
       "result_version": [
         "str"
       ],
       "rule_set_id": [
         "str"
       ],
       "run_id": [
         "str"
       ],
       "source_object_id": [
         "str"
       ],
       "stage": [
         "str"
       ],
       "stage_movement": [
         "str"
       ],
       "view": [
         "str"
       ],
       "weighted_ecl": [
         "float"
       ],
       "weighted_ecl_local": [
         "float"
       ]
     }
   }

03_Impairment_ECL/STAGING
~~~~~~~~~~~~~~~~~~~~~~~~~

Field names and observed types::

   {
     "type": "table",
     "fields": {
       "accounting_policy_id": [
         "str"
       ],
       "as_of_date": [
         "str"
       ],
       "decision_rule_id": [
         "str"
       ],
       "formula_id": [
         "NoneType"
       ],
       "instrument_id": [
         "str"
       ],
       "knowledge_time": [
         "str"
       ],
       "official_flag": [
         "bool"
       ],
       "prior_stage": [
         "str"
       ],
       "result_version": [
         "str"
       ],
       "rule_set_id": [
         "str"
       ],
       "run_id": [
         "str"
       ],
       "source_object_id": [
         "str"
       ],
       "source_reference": [
         "str"
       ],
       "stage": [
         "str"
       ],
       "stage_movement": [
         "str"
       ],
       "stage_reason": [
         "str"
       ],
       "view": [
         "str"
       ]
     }
   }

04_Hedge_Accounting/HEDGES
~~~~~~~~~~~~~~~~~~~~~~~~~~

Field names and observed types::

   {
     "type": "table",
     "fields": {
       "accounting_policy_id": [
         "str"
       ],
       "as_of_date": [
         "str"
       ],
       "basis_adjustment": [
         "float"
       ],
       "cost_of_hedging_reserve": [
         "float"
       ],
       "formula_id": [
         "str"
       ],
       "hedge_type": [
         "str"
       ],
       "ineffectiveness_pnl": [
         "float"
       ],
       "knowledge_time": [
         "str"
       ],
       "nature_dependent_electricity_hedge": [
         "bool"
       ],
       "oci_effective": [
         "float"
       ],
       "official_flag": [
         "bool"
       ],
       "recycle_amount": [
         "float"
       ],
       "relationship_id": [
         "str"
       ],
       "result_version": [
         "str"
       ],
       "rule_set_id": [
         "str"
       ],
       "run_id": [
         "str"
       ],
       "source_object_id": [
         "str"
       ],
       "source_reference": [
         "str"
       ],
       "status": [
         "str"
       ],
       "view": [
         "str"
       ]
     }
   }

04_Hedge_Accounting/NOT_APPLICABLE
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Field names and observed types::

   {
     "type": "table",
     "fields": {
       "reason": [
         "str"
       ],
       "status": [
         "str"
       ]
     }
   }

04_Hedge_Accounting/OCI_ROLLFORWARD
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Field names and observed types::

   {
     "type": "table",
     "fields": {
       "accounting_policy_id": [
         "str"
       ],
       "as_of_date": [
         "str"
       ],
       "basis_adjustment": [
         "float",
         "int"
       ],
       "closing_reserve": [
         "float"
       ],
       "cost_of_hedging_movement": [
         "float",
         "int"
       ],
       "effective_hedge_movement": [
         "float",
         "int"
       ],
       "fair_value_movement": [
         "float",
         "int"
       ],
       "formula_id": [
         "str"
       ],
       "knowledge_time": [
         "str"
       ],
       "official_flag": [
         "bool"
       ],
       "opening_reserve": [
         "float"
       ],
       "recycling": [
         "float",
         "int"
       ],
       "reserve_type": [
         "str"
       ],
       "result_version": [
         "str"
       ],
       "rule_set_id": [
         "str"
       ],
       "run_id": [
         "str"
       ],
       "source_object_id": [
         "NoneType"
       ],
       "view": [
         "str"
       ]
     }
   }

05_Journals_Disclosures/ALLOWANCE_ROLLFORWARD
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Field names and observed types::

   {
     "type": "table",
     "fields": {
       "accounting_policy_id": [
         "str"
       ],
       "as_of_date": [
         "str"
       ],
       "closing_allowance": [
         "float"
       ],
       "current_stage": [
         "str"
       ],
       "ecl_remeasurement": [
         "float"
       ],
       "formula_id": [
         "str"
       ],
       "instrument_id": [
         "str"
       ],
       "knowledge_time": [
         "str"
       ],
       "official_flag": [
         "bool"
       ],
       "opening_allowance": [
         "float"
       ],
       "prior_stage": [
         "str"
       ],
       "result_version": [
         "str"
       ],
       "rule_set_id": [
         "str"
       ],
       "run_id": [
         "str"
       ],
       "source_object_id": [
         "str"
       ],
       "view": [
         "str"
       ],
       "writeoff": [
         "float",
         "int"
       ]
     }
   }

05_Journals_Disclosures/DISCLOSURE_AGGREGATES
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Field names and observed types::

   {
     "type": "table",
     "fields": {
       "accounting_policy_id": [
         "str"
       ],
       "aggregation_level": [
         "str"
       ],
       "allowance": [
         "float"
       ],
       "as_of_date": [
         "str"
       ],
       "coverage_ratio": [
         "NoneType",
         "float"
       ],
       "dimension_key": [
         "str"
       ],
       "formula_id": [
         "str"
       ],
       "gross_carrying_amount": [
         "float"
       ],
       "instrument_count": [
         "int"
       ],
       "knowledge_time": [
         "str"
       ],
       "net_carrying_amount": [
         "float"
       ],
       "official_flag": [
         "bool"
       ],
       "result_version": [
         "str"
       ],
       "rule_set_id": [
         "str"
       ],
       "run_id": [
         "str"
       ],
       "source_object_id": [
         "NoneType"
       ],
       "view": [
         "str"
       ]
     }
   }

05_Journals_Disclosures/DISCLOSURE_FACTS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Field names and observed types::

   {
     "type": "table",
     "fields": {
       "accounting_policy_id": [
         "str"
       ],
       "allowance": [
         "float"
       ],
       "as_of_date": [
         "str"
       ],
       "classification": [
         "str"
       ],
       "currency": [
         "str"
       ],
       "disclosure_class": [
         "str"
       ],
       "entity_id": [
         "str"
       ],
       "formula_id": [
         "str"
       ],
       "fx_rate": [
         "float"
       ],
       "gross_carrying_amount": [
         "float"
       ],
       "gross_carrying_amount_local": [
         "float"
       ],
       "instrument_id": [
         "str"
       ],
       "knowledge_time": [
         "str"
       ],
       "net_carrying_amount": [
         "float"
       ],
       "official_flag": [
         "bool"
       ],
       "portfolio": [
         "str"
       ],
       "presentation_currency": [
         "str"
       ],
       "result_version": [
         "str"
       ],
       "rule_set_id": [
         "str"
       ],
       "run_id": [
         "str"
       ],
       "source_object_id": [
         "str"
       ],
       "stage": [
         "str"
       ],
       "view": [
         "str"
       ]
     }
   }

05_Journals_Disclosures/EVENTS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Field names and observed types::

   {
     "type": "table",
     "fields": {
       "accounting_policy_id": [
         "str"
       ],
       "amount": [
         "float"
       ],
       "as_of_date": [
         "str"
       ],
       "continuing_involvement": [
         "float"
       ],
       "derecognition_result": [
         "str"
       ],
       "event_id": [
         "str"
       ],
       "event_type": [
         "str"
       ],
       "formula_id": [
         "str"
       ],
       "instrument_id": [
         "str"
       ],
       "knowledge_time": [
         "str"
       ],
       "modification_result": [
         "float"
       ],
       "official_flag": [
         "bool"
       ],
       "pnl_effect": [
         "float"
       ],
       "reason_code": [
         "str"
       ],
       "result_version": [
         "str"
       ],
       "rule_set_id": [
         "str"
       ],
       "run_id": [
         "str"
       ],
       "source_object_id": [
         "str"
       ],
       "view": [
         "str"
       ]
     }
   }

05_Journals_Disclosures/GROSS_ROLLFORWARD
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Field names and observed types::

   {
     "type": "table",
     "fields": {
       "accounting_policy_id": [
         "str"
       ],
       "as_of_date": [
         "str"
       ],
       "closing_gross": [
         "float"
       ],
       "derecognition": [
         "float",
         "int"
       ],
       "formula_id": [
         "str"
       ],
       "instrument_id": [
         "str"
       ],
       "knowledge_time": [
         "str"
       ],
       "modification": [
         "float",
         "int"
       ],
       "official_flag": [
         "bool"
       ],
       "opening_gross": [
         "float"
       ],
       "other_contractual_and_fx_movements": [
         "float"
       ],
       "result_version": [
         "str"
       ],
       "rule_set_id": [
         "str"
       ],
       "run_id": [
         "str"
       ],
       "source_object_id": [
         "str"
       ],
       "view": [
         "str"
       ],
       "writeoff": [
         "float",
         "int"
       ]
     }
   }

05_Journals_Disclosures/JOURNALS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Field names and observed types::

   {
     "type": "table",
     "fields": {
       "account": [
         "str"
       ],
       "accounting_policy_id": [
         "str"
       ],
       "as_of_date": [
         "str"
       ],
       "credit": [
         "float",
         "int"
       ],
       "debit": [
         "float",
         "int"
       ],
       "formula_id": [
         "str"
       ],
       "instrument_id": [
         "str"
       ],
       "journal_batch_id": [
         "str"
       ],
       "knowledge_time": [
         "str"
       ],
       "movement_type": [
         "str"
       ],
       "official_flag": [
         "bool"
       ],
       "result_version": [
         "str"
       ],
       "rule_set_id": [
         "str"
       ],
       "run_id": [
         "str"
       ],
       "source_object_id": [
         "str"
       ],
       "view": [
         "str"
       ]
     }
   }

05_Journals_Disclosures/OCI_ROLLFORWARD
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Field names and observed types::

   {
     "type": "table",
     "fields": {
       "accounting_policy_id": [
         "str"
       ],
       "as_of_date": [
         "str"
       ],
       "basis_adjustment": [
         "float",
         "int"
       ],
       "closing_reserve": [
         "float"
       ],
       "cost_of_hedging_movement": [
         "float",
         "int"
       ],
       "effective_hedge_movement": [
         "float",
         "int"
       ],
       "fair_value_movement": [
         "float",
         "int"
       ],
       "formula_id": [
         "str"
       ],
       "knowledge_time": [
         "str"
       ],
       "official_flag": [
         "bool"
       ],
       "opening_reserve": [
         "float"
       ],
       "recycling": [
         "float",
         "int"
       ],
       "reserve_type": [
         "str"
       ],
       "result_version": [
         "str"
       ],
       "rule_set_id": [
         "str"
       ],
       "run_id": [
         "str"
       ],
       "source_object_id": [
         "NoneType"
       ],
       "view": [
         "str"
       ]
     }
   }

06_Audit/BACKTESTING
~~~~~~~~~~~~~~~~~~~~

Field names and observed types::

   {
     "type": "table",
     "fields": {
       "accounting_policy_id": [
         "str"
       ],
       "approval_id": [
         "str"
       ],
       "as_of_date": [
         "str"
       ],
       "auc": [
         "NoneType",
         "float"
       ],
       "bias": [
         "float"
       ],
       "calibration_ratio": [
         "float"
       ],
       "challenger_flag": [
         "bool"
       ],
       "formula_id": [
         "str"
       ],
       "knowledge_time": [
         "str"
       ],
       "mean_absolute_error": [
         "float"
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
       "observations": [
         "int"
       ],
       "official_flag": [
         "bool"
       ],
       "release_amount": [
         "float"
       ],
       "result_version": [
         "str"
       ],
       "rule_set_id": [
         "str"
       ],
       "run_id": [
         "str"
       ],
       "segment": [
         "str"
       ],
       "source_object_id": [
         "str"
       ],
       "validation_status": [
         "str"
       ],
       "view": [
         "str"
       ],
       "weighted_actual": [
         "float"
       ],
       "weighted_prediction": [
         "float"
       ]
     }
   }

06_Audit/CONTROLS
~~~~~~~~~~~~~~~~~

Field names and observed types::

   {
     "type": "table",
     "fields": {
       "actual": [
         "bool",
         "float",
         "int"
       ],
       "control_id": [
         "str"
       ],
       "expected": [
         "bool",
         "float",
         "int"
       ],
       "explanation": [
         "str"
       ],
       "status": [
         "str"
       ],
       "tolerance": [
         "float"
       ]
     }
   }

06_Audit/REGULATORY_BRIDGE
~~~~~~~~~~~~~~~~~~~~~~~~~~

Field names and observed types::

   {
     "type": "table",
     "fields": {
       "accounting_policy_id": [
         "str"
       ],
       "accounting_value_used_in_regulatory_calculation": [
         "bool"
       ],
       "as_of_date": [
         "str"
       ],
       "difference": [
         "float"
       ],
       "formula_id": [
         "str"
       ],
       "ifrs9_ecl": [
         "float"
       ],
       "ifrs9_stage": [
         "str"
       ],
       "instrument_id": [
         "str"
       ],
       "knowledge_time": [
         "str"
       ],
       "official_flag": [
         "bool"
       ],
       "regulatory_approach": [
         "str"
       ],
       "regulatory_default_flag": [
         "bool"
       ],
       "regulatory_expected_loss": [
         "float"
       ],
       "result_version": [
         "str"
       ],
       "rule_set_id": [
         "str"
       ],
       "run_id": [
         "str"
       ],
       "source_object_id": [
         "str"
       ],
       "view": [
         "str"
       ]
     }
   }

06_Audit/SCENARIO_SENSITIVITY
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Field names and observed types::

   {
     "type": "table",
     "fields": {
       "accounting_policy_id": [
         "str"
       ],
       "as_of_date": [
         "str"
       ],
       "formula_id": [
         "str"
       ],
       "knowledge_time": [
         "str"
       ],
       "official_flag": [
         "bool"
       ],
       "probability": [
         "float"
       ],
       "result_version": [
         "str"
       ],
       "rule_set_id": [
         "str"
       ],
       "run_id": [
         "str"
       ],
       "scenario_id": [
         "str"
       ],
       "source_object_id": [
         "NoneType"
       ],
       "standalone_ecl": [
         "float"
       ],
       "view": [
         "str"
       ],
       "weighted_contribution": [
         "float"
       ]
     }
   }

06_Audit/VALIDATION
~~~~~~~~~~~~~~~~~~~

Field names and observed types::

   {
     "type": "table",
     "fields": {
       "code": [
         "str"
       ],
       "message": [
         "str"
       ],
       "severity": [
         "str"
       ]
     }
   }
