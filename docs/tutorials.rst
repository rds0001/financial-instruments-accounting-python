Analyst tutorials
=================

Granular start
--------------

No workbook or complete portfolio is required for a formula:

>>> import financial_accounting_engine as fae
>>> round(fae.component_ecl(.02, 100000, .4, .05, 1), 6)
761.904762
>>> fae.poci_allowance_change(20, 30)
-10.0
>>> fae.cumulative_pd_from_conditional([.1, .2])[-1] == .28
False

The last equality illustrates binary64 representation. Compare numerically:

>>> abs(fae.cumulative_pd_from_conditional([.1, .2])[-1] - .28) < 1e-12
True

Classification and EIR
----------------------

Load one independent synthetic contract, then ask targeted questions:

>>> data = fae.load_reference_data('SMALL_SA_RETAIL_FIA')
>>> fae.assess_sppi(data['classification_inputs'][0])['sppi_pass']
True
>>> fae.classify_instrument(data['instruments'][0], data['classification_inputs'][0])['classification']
'AMORTISED_COST'
>>> round(fae.effective_interest_rate(1000, [(1, 1100)]), 10)
0.1
>>> fae.amortisation_schedule(1000, .1, [(1, 200), (2, 990)])[-1]['closing']
0.0

Classification features express reviewed judgements. They do not parse a contract
or establish SPPI merely because inputs are present. Missing required facts reject.

Staging, scenarios and POCI
---------------------------

>>> facts = dict(data['staging_inputs'][0], days_past_due=30)
>>> fae.assess_stage(facts)['stage']
'STAGE_2'
>>> fae.weighted_ecl({'base': 10, 'stress': 30}, {'base': .75, 'stress': .25})
15.0
>>> fae.poci_allowance_change(40, 30)
10.0
>>> fae.poci_allowance_change(20, 30)
-10.0

Use scenario_ecl for one instrument's curve/component rows and instrument summary.
Use cash_shortfall_ecl when expected receipts already encode the relevant default
population, and provision_matrix_ecl for one homogeneous lifetime-loss-rate segment.
An ECL overlay needs its own ownership, approval, expiry and double-count review;
allocate_overlay only allocates a supplied amount and never creates that approval.

Hedges, journals and reconciliation
-----------------------------------

>>> u = fae.load_reference_data('MID_SIZE_UNIVERSAL_FIA')
>>> hedge = dict(u['hedges'][0], hedge_type='CASH_FLOW', hedging_change=80, hedged_change=-100)
>>> measured = fae.measure_hedge(hedge)
>>> (measured['oci_effective'], measured['ineffectiveness_pnl'])
(80.0, 0.0)
>>> fae.oci_rollforward(10, effective_hedge_movement=5, recycling=2, basis_adjustment=1)['closing_reserve']
12.0
>>> fae.reconcile_ledger(100, 99)['status']
'FAIL'

For CF/NI hedges supply cumulative designated changes; reserve rollforwards consume
period movements. Derive movements from consecutive cumulative valuations when
using more than one reporting period. Rejected designations do not produce new
hedge-accounting entries. Supplied costs-of-hedging and recycling/basis amounts require
separate institutional support. Reference journals are balanced templates, not postings.

Snapshots, lineage and the full workflow
----------------------------------------

>>> result = fae.run_dataset(data)
>>> result.status
'APPROVED_REFERENCE'
>>> result.official
False
>>> len(fae.get_table(result, 'STAGING'))
5
>>> fae.get_lineage(result)['contract_version']
'1.1.0'
>>> all(row['status'] == 'PASS' for row in fae.get_controls(result))
True

To export, supply a new path explicitly::

   source = fae.export_profile('SMALL_SA_RETAIL_FIA', '/your/workspace/inputs')
   result = fae.run_dataset(source)
   fae.export_results(result, '/your/workspace/results')

None of these operations publishes results, downloads standards or contacts the
maintainer. Supply institutional policy/approvals before replacing reference facts.

Complete executable examples
----------------------------

``examples/analyst_workbook.py`` directly invokes every public function and checks
a specified expected result. Run it with a new local workspace path::

   python examples/analyst_workbook.py ./example-results

All tests use the installed public API; examples never import private engine modules.
Each function's reference page links its exact example key and pytest case.
