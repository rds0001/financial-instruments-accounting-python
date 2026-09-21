scenario_ecl
============

.. autofunction:: financial_accounting_engine.scenario_ecl

Accounting/API contract
-----------------------

Requirements: FR-033, FR-035, FR-041.
Reference basis: frozen policy/rules 2026_V1, input contract 1.1.0.
Source paragraphs are retained in decision outputs and the formula registry;
see the requirement mapping and correction notes for controlled judgements.

Parameters
----------

``instrument``
   Canonical instruments row, restricted to the fields required for the targeted calculation.

``stage``
   Canonical STAGE_1/STAGE_2/STAGE_3/POCI/SIMPLIFIED_LIFETIME/NO_IMPAIRMENT_SCOPE label.

``pd_curves``
   Rows keyed by scenario_id/year with unconditional marginal_pd; annual years start at one.

``lgd_profiles``
   Rows keyed by scenario_id/year with lgd in [0,1], matching PD/EAD keys.

``ead_profiles``
   Rows keyed by scenario_id/year with nonnegative ead, compatible with the PD/LGD grid.

``probabilities``
   Scenario-ID keyed weights in [0,1], summing to one within 1e-9.

``cashflows``
   Ordered (cumulative years, nonnegative receipt amount) pairs; EIR requires future receipts.

``reporting_date``
   ISO YYYY-MM-DD reporting cutoff; also used to check approval/overlay expiry.

Return schema
-------------

Representative field/type schema (conditional decision fields may be absent;
table columns and optional values are listed in :doc:`../schemas`)::

   {
     "type": "tuple",
     "items": [
       {
         "type": "table",
         "fields": {
           "discounted_ecl": [
             "float"
           ],
           "ead": [
             "float"
           ],
           "formula_id": [
             "str"
           ],
           "instrument_id": [
             "str"
           ],
           "lgd": [
             "float"
           ],
           "marginal_pd": [
             "float"
           ],
           "scenario_id": [
             "str"
           ],
           "year": [
             "int"
           ]
         }
       },
       {
         "instrument_id": "str",
         "stage": "str",
         "ecl_method": "str",
         "weighted_ecl": "float",
         "poci_initial_lifetime_ecl": "float",
         "overlay": "float",
         "final_ecl": "float",
         "formula_id": "str",
         "model_version_id": "str"
       }
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

``examples/analyst_workbook.py`` case ``scenario_ecl`` supplies the arguments and an
independent expected-result assertion. Its function call is::

   import financial_accounting_engine as fae
   actual = fae.scenario_ecl(*args, **kwargs)
   assert check(actual)

Executed pytest ID: ``tests/test_api.py::test_api_example[scenario_ecl]``.
