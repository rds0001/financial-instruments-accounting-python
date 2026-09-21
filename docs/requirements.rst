Requirement coverage
====================

Mapping of all 60 frozen accounting requirements. IMPLEMENTED denotes generic
reference functionality, not institutionally approved accounting.

.. list-table::
   :header-rows: 1

   * - Requirement
     - Public calls
     - Status
   * - FR-001
     - assess_scope, classify_instrument
     - IMPLEMENTED
   * - FR-002
     - classify_instrument, ead_profile, build_journals
     - IMPLEMENTED
   * - FR-003
     - assess_scope
     - IMPLEMENTED
   * - FR-004
     - assess_scope
     - CONTROLLED_INTERFACE
   * - FR-005
     - assess_recognition
     - IMPLEMENTED
   * - FR-006
     - assess_recognition
     - IMPLEMENTED
   * - FR-007
     - classify_instrument
     - IMPLEMENTED
   * - FR-008
     - assess_business_model, assess_reclassification
     - IMPLEMENTED
   * - FR-009
     - assess_sppi
     - IMPLEMENTED
   * - FR-010
     - assess_sppi
     - IMPLEMENTED
   * - FR-011
     - assess_sppi
     - IMPLEMENTED
   * - FR-012
     - assess_sppi
     - CONTROLLED_INTERFACE
   * - FR-013
     - assess_sppi
     - IMPLEMENTED
   * - FR-014
     - classify_instrument
     - IMPLEMENTED
   * - FR-015
     - classify_instrument
     - IMPLEMENTED
   * - FR-016
     - split_own_credit, build_journals
     - IMPLEMENTED
   * - FR-017
     - initial_measurement
     - IMPLEMENTED
   * - FR-018
     - present_fair_value
     - CONTROLLED_INTERFACE
   * - FR-019
     - run_dataset, disclosure_facts
     - IMPLEMENTED
   * - FR-020
     - effective_interest_rate, discount_factor
     - IMPLEMENTED
   * - FR-021
     - amortised_cost_step, amortisation_schedule, run_dataset
     - IMPLEMENTED
   * - FR-022
     - interest_revenue
     - IMPLEMENTED
   * - FR-023
     - modification_gain_loss, process_modification
     - IMPLEMENTED
   * - FR-024
     - liability_modification_test, process_modification
     - IMPLEMENTED
   * - FR-025
     - assess_derecognition, continuing_involvement
     - CONTROLLED_INTERFACE
   * - FR-026
     - process_writeoff, process_recovery
     - IMPLEMENTED
   * - FR-027
     - impairment_scope
     - IMPLEMENTED
   * - FR-028
     - assess_stage
     - IMPLEMENTED
   * - FR-029
     - assess_sicr
     - IMPLEMENTED
   * - FR-030
     - assess_sicr
     - IMPLEMENTED
   * - FR-031
     - assess_stage
     - IMPLEMENTED
   * - FR-032
     - assess_stage, stage_movements
     - IMPLEMENTED
   * - FR-033
     - component_ecl, scenario_ecl
     - IMPLEMENTED
   * - FR-034
     - cash_shortfall_ecl
     - IMPLEMENTED
   * - FR-035
     - survival_from_pd, marginal_pd_from_cumulative, cumulative_pd_from_conditional, scenario_ecl
     - IMPLEMENTED
   * - FR-036
     - ead_profile
     - CONTROLLED_INTERFACE
   * - FR-037
     - recovery_present_value, lgd_from_recoveries
     - CONTROLLED_INTERFACE
   * - FR-038
     - allocate_credit_enhancements
     - IMPLEMENTED
   * - FR-039
     - weighted_ecl, scenario_sensitivity
     - IMPLEMENTED
   * - FR-040
     - provision_matrix_ecl
     - IMPLEMENTED
   * - FR-041
     - poci_allowance_change, scenario_ecl
     - IMPLEMENTED
   * - FR-042
     - validate_overlay, allocate_overlay, reconcile_overlay
     - IMPLEMENTED
   * - FR-043
     - backtest_models, backtest_pd, backtest_lgd, backtest_ead, backtest_staging, compare_challenger
     - IMPLEMENTED
   * - FR-044
     - validate_hedge_designation
     - IMPLEMENTED
   * - FR-045
     - measure_hedge
     - IMPLEMENTED
   * - FR-046
     - assess_hedge_effectiveness
     - IMPLEMENTED
   * - FR-047
     - measure_hedge, hedge_reserve_rollforward
     - IMPLEMENTED
   * - FR-048
     - hedge_reserve_rollforward, build_journals
     - IMPLEMENTED
   * - FR-049
     - measure_hedge
     - IMPLEMENTED
   * - FR-050
     - assess_ibor_relief
     - CONTROLLED_INTERFACE
   * - FR-051
     - None
     - NOT_APPLICABLE in frozen knowledge baseline; no final DRM model implemented
   * - FR-052
     - build_journals
     - IMPLEMENTED
   * - FR-053
     - allowance_rollforward, gross_rollforward
     - IMPLEMENTED
   * - FR-054
     - disclosure_facts, aggregate_disclosures, coverage_ratio
     - IMPLEMENTED
   * - FR-055
     - oci_rollforward, hedge_reserve_rollforward
     - IMPLEMENTED
   * - FR-056
     - reconcile_ledger, get_controls
     - CONTROLLED_INTERFACE
   * - FR-057
     - regulatory_bridge
     - IMPLEMENTED
   * - FR-058
     - validate_dataset, select_snapshot, get_lineage
     - IMPLEMENTED
   * - FR-059
     - run_dataset, export_results
     - CLI/shared workflow implemented; browser app is a separate optional integration
   * - FR-060
     - benchmark_ecl
     - IMPLEMENTED
