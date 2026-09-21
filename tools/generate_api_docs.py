"""Regenerate the public API inventory and schema reference from executable examples."""

import importlib.util
import inspect
import json
import uuid
from pathlib import Path

import financial_accounting_engine as fae

ROOT = Path(__file__).resolve().parents[1]
PARAMETERS = {
    "actual": "Independently supplied actual ledger/control amount, in the same unit as expected.",
    "adjustment": "Signed within-period carrying amount adjustment in the input currency; default zero.",
    "allocation_weights": "Population-keyed allocation fractions, nonnegative and summing to one.",
    "allocations": "Population-keyed signed overlay allocations in the approved amount currency.",
    "allowance": "Signed allowance in instrument local currency; POCI changes may be negative.",
    "amount": "Signed overlay amount in one currency; allocation does not itself approve the overlay.",
    "applicable": "Explicit externally reviewed IBOR-relief applicability boolean.",
    "approval_reference": "Nonempty institutional case approval reference; no approval is inferred.",
    "basis_adjustment": "Signed amount removed from OCI into the nonfinancial asset basis.",
    "cash_received": "Nonnegative period receipts in the opening balance currency.",
    "cashflows": "Ordered (cumulative years, nonnegative receipt amount) pairs; EIR requires future receipts.",
    "category": "Canonical measurement classification, e.g. AMORTISED_COST, FVOCI_DEBT or FVTPL_LIABILITY.",
    "ccf": "Period conversion factors in [0,1], with the same vector length as drawn/undrawn.",
    "challenger": "Monitoring result rows keyed by model_type/segment, with MAE and bias.",
    "classifications": "Instrument-ID to canonical classification mapping.",
    "collateral": "Canonical collateral rows: ID, instrument, fair_value, haircut, cost, allocation, recovery timing.",
    "conditional": "Conditional default probability per period in [0,1], conditional on survival to that period.",
    "contractual": "Nonempty (years, contractual receipt) pairs in one currency.",
    "costs": "Discounted cost cashflow pairs for LGD, or signed reserve movement for OCI; see function type.",
    "cumulative": "Nondecreasing unconditional cumulative default probabilities in [0,1].",
    "current_lifetime_ecl": "Current nonnegative lifetime expected loss in the initial baseline currency.",
    "dataset": "Complete canonical Dataset mapping or input-directory path; file/in-memory paths use one core.",
    "destination": "New writable user-directory path. Existing destinations reject; package resources are read-only.",
    "drawn": "Nonnegative drawn exposure for each period, before the supplied period prepayment adjustment.",
    "ead": "Nonnegative exposure at default in one currency; LGD derivation requires positive exposure.",
    "ead_profiles": "Rows keyed by scenario_id/year with nonnegative ead, compatible with the PD/LGD grid.",
    "ecl_results": "Instrument summary rows with instrument_id, stage and final_ecl; use presentation money for disclosures.",
    "effective_hedge_movement": "Signed effective hedge gain/loss for the reporting period credited to the OCI reserve.",
    "eir": "Annual effective interest rate as a decimal greater than -1; credit-adjusted where POCI applies.",
    "event": "Canonical approved event facts, including matching instrument_id, type, reason and relevant amounts.",
    "expected": "Independent expected control amount, or expected recovery cashflow pairs for direct shortfall; see type.",
    "exposure": "Nonnegative segment exposure in one currency.",
    "facts": "Canonical staging facts or atomic disclosure rows, according to the function.",
    "fair_value_movement": "Signed period fair-value movement recognized in OCI.",
    "features": "Reviewed SPPI/classification_inputs fields; missing basic-lending facts reject.",
    "formula_id": "Exact registered formula ID such as F-ECL-001.",
    "fx": "Instrument-ID to positive local-to-presentation FX multiplier mapping.",
    "gross_before": "Gross carrying amount before modification, in the modified cashflow currency.",
    "gross_exposure": "Nonnegative gross exposure; coverage returns None when it is zero.",
    "hedge_results": "Measured hedge rows containing period effective OCI, costs, recycling and basis amounts.",
    "hedged_change": "Signed cumulative change of the hedged item attributable to designated risk; gains positive.",
    "hedging_change": "Signed cumulative designated hedging instrument change; gains positive.",
    "initial_lifetime_ecl": "Nonnegative initial POCI lifetime ECL baseline, same currency as current ECL.",
    "initial_net": "Positive initial carrying amount matched to the receipt currency.",
    "instrument": "Canonical instruments row, restricted to the fields required for the targeted calculation.",
    "instruments": "Sequence of canonical instrument rows with unique instrument IDs.",
    "iterations": "Positive integer number of fixed golden-vector evaluations; capped at 1,000,000.",
    "knowledge_time": "ISO knowledge timestamp including explicit timezone offset; inclusive known-time intervals.",
    "lgd": "Conditional loss severity in [0,1], with recovery timing already valued relative to default.",
    "lgd_profiles": "Rows keyed by scenario_id/year with lgd in [0,1], matching PD/EAD keys.",
    "loss_rate": "Lifetime provision matrix segment rate in [0,1], supplied rather than estimated.",
    "losses": "Scenario-ID keyed nonnegative standalone losses, calculated before weighting.",
    "marginal": "Unconditional period default masses in [0,1]; cumulative sum must not exceed one.",
    "marginal_pd": "Unconditional default probability mass for the supplied period in [0,1].",
    "market": "Canonical market_data row with controlled fair value, changes, model/level and own-credit facts.",
    "model": "Approved business-model label HOLD_TO_COLLECT, HOLD_TO_COLLECT_AND_SELL or OTHER.",
    "modified_cashflows": "Nonempty revised (years, receipt) pairs discounted at the original effective rate.",
    "modified_present_value": "PV of revised liability cashflows including eligible fees at original EIR.",
    "name": "Exact workbook/sheet key or an unambiguous sheet name from AnalysisResult.tables.",
    "observations": "Canonical monitoring rows with model, owner, approval, prediction, outcome and positive exposure weight.",
    "opening": "Opening monetary balance (or instrument-ID keyed opening balances for table rollforwards).",
    "opening_allowances": "Instrument-ID keyed opening allowances in the journal currency.",
    "original_eir": "Original annual effective interest rate, retained through non-derecognizing modification.",
    "original_present_value": "Positive PV of original liability cashflows at original EIR.",
    "overlay": "Amount plus ID, owner, approval, expiry, thesis and double-count-review facts.",
    "own_credit_results": "Own-credit split rows; only classifications marked FVTPL_LIABILITY produce own-credit journals.",
    "pd_curves": "Rows keyed by scenario_id/year with unconditional marginal_pd; annual years start at one.",
    "policy": "Complete explicit versioned policy; None selects the frozen EU_FINANCIAL_INSTRUMENTS_2026_V1.",
    "policy_id": "Exact packaged policy ID, default EU_FINANCIAL_INSTRUMENTS_2026_V1.",
    "policy_reference": "Nonempty institution-specific policy/reform-phase reference for the controlled interface.",
    "prepayment": "Period prepayment fractions in [0,1], applied to drawn exposure; equal vector lengths required.",
    "presentation_currency": "Declared common currency code for all monetary disclosure facts.",
    "probabilities": "Scenario-ID keyed weights in [0,1], summing to one within 1e-9.",
    "processed_events": "Approved process_* outputs; use the same currency as the surrounding journal/rollforward.",
    "profile_id": "Exact profile identifier from list_profiles(); resources are version 1.0.0.",
    "qualitative_substantial": "Externally approved qualitative-substantial-change boolean, additional to the quantitative test.",
    "rate": "Annual decimal discount rate greater than -1.",
    "recoveries": "Nonnegative recovery receipt (years from valuation date, amount) pairs.",
    "recycling": "Signed reserve amount removed to profit/loss; positive reduces a positive reserve.",
    "reference": "Reference monitoring rows keyed uniquely by model_type/segment.",
    "relationship": "Canonical hedges row with documented eligibility, ratios and cumulative designated changes.",
    "reporting_date": "ISO YYYY-MM-DD reporting cutoff; also used to check approval/overlay expiry.",
    "result": "AnalysisResult returned by run_dataset; accessors return independent copies.",
    "rule_set_id": "Exact packaged rule-set ID; default FIA_RULES_2026_V1.",
    "scenario_losses": "Scenario-ID keyed nonnegative separately calculated losses; exact probability-key match required.",
    "scope_decision": "Explicit IN_IFRS9_SCOPE or NO_IFRS9_SCOPE decision; default in-scope requires caller judgement.",
    "stage": "Canonical STAGE_1/STAGE_2/STAGE_3/POCI/SIMPLIFIED_LIFETIME/NO_IMPAIRMENT_SCOPE label.",
    "stage_results": "Rows with prior_stage and current stage; movement counts do not infer missing population.",
    "stages": "Instrument-ID to stage mapping, separate from regulatory default classification.",
    "table": "Optional exact canonical input table name; None returns the complete input schema.",
    "tables": "Mapping of table names to bitemporal canonical rows.",
    "threshold": "Explicit absolute relative-PV-change threshold in [0,1]; default 0.10, equality qualifies.",
    "time": "Nonnegative period length in years for simple within-period accrual.",
    "tolerance": "Positive EIR relative-PV/absolute-rate convergence threshold, or nonnegative absolute control tolerance; see function.",
    "undrawn": "Nonnegative undrawn commitment by period, converted using the corresponding CCF.",
    "year": "Nonnegative discount time to default in years; recovery timing is already incorporated in LGD.",
    "year_fraction": "Nonnegative time from valuation date in years.",
}

# Exhaustive many-to-many mapping of the frozen requirement register.
FR = {
    1: ["assess_scope", "classify_instrument"],
    2: ["classify_instrument", "ead_profile", "build_journals"],
    3: ["assess_scope"],
    4: ["assess_scope"],
    5: ["assess_recognition"],
    6: ["assess_recognition"],
    7: ["classify_instrument"],
    8: ["assess_business_model", "assess_reclassification"],
    9: ["assess_sppi"],
    10: ["assess_sppi"],
    11: ["assess_sppi"],
    12: ["assess_sppi"],
    13: ["assess_sppi"],
    14: ["classify_instrument"],
    15: ["classify_instrument"],
    16: ["split_own_credit", "build_journals"],
    17: ["initial_measurement"],
    18: ["present_fair_value"],
    19: ["run_dataset", "disclosure_facts"],
    20: ["effective_interest_rate", "discount_factor"],
    21: ["amortised_cost_step", "amortisation_schedule", "run_dataset"],
    22: ["interest_revenue"],
    23: ["modification_gain_loss", "process_modification"],
    24: ["liability_modification_test", "process_modification"],
    25: ["assess_derecognition", "continuing_involvement"],
    26: ["process_writeoff", "process_recovery"],
    27: ["impairment_scope"],
    28: ["assess_stage"],
    29: ["assess_sicr"],
    30: ["assess_sicr"],
    31: ["assess_stage"],
    32: ["assess_stage", "stage_movements"],
    33: ["component_ecl", "scenario_ecl"],
    34: ["cash_shortfall_ecl"],
    35: [
        "survival_from_pd",
        "marginal_pd_from_cumulative",
        "cumulative_pd_from_conditional",
        "scenario_ecl",
    ],
    36: ["ead_profile"],
    37: ["recovery_present_value", "lgd_from_recoveries"],
    38: ["allocate_credit_enhancements"],
    39: ["weighted_ecl", "scenario_sensitivity"],
    40: ["provision_matrix_ecl"],
    41: ["poci_allowance_change", "scenario_ecl"],
    42: ["validate_overlay", "allocate_overlay", "reconcile_overlay"],
    43: [
        "backtest_models",
        "backtest_pd",
        "backtest_lgd",
        "backtest_ead",
        "backtest_staging",
        "compare_challenger",
    ],
    44: ["validate_hedge_designation"],
    45: ["measure_hedge"],
    46: ["assess_hedge_effectiveness"],
    47: ["measure_hedge", "hedge_reserve_rollforward"],
    48: ["hedge_reserve_rollforward", "build_journals"],
    49: ["measure_hedge"],
    50: ["assess_ibor_relief"],
    51: [],
    52: ["build_journals"],
    53: ["allowance_rollforward", "gross_rollforward"],
    54: ["disclosure_facts", "aggregate_disclosures", "coverage_ratio"],
    55: ["oci_rollforward", "hedge_reserve_rollforward"],
    56: ["reconcile_ledger", "get_controls"],
    57: ["regulatory_bridge"],
    58: ["validate_dataset", "select_snapshot", "get_lineage"],
    59: ["run_dataset", "export_results"],
    60: ["benchmark_ecl"],
}


def describe(value):
    if isinstance(value, fae.AnalysisResult):
        return {
            "type": "AnalysisResult",
            "fields": ["tables", "metrics", "lineage", "status", "official"],
        }
    if isinstance(value, Path):
        return {"type": "Path", "meaning": "new export directory"}
    if isinstance(value, dict):
        return {str(k): describe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        if all(isinstance(r, dict) for r in value):
            return {
                "type": "table",
                "fields": {
                    k: sorted({type(r[k]).__name__ for r in value if k in r})
                    for k in sorted({k for r in value for k in r})
                },
            }
        return {"type": type(value).__name__, "items": [describe(v) for v in value[:3]]}
    return type(value).__name__


def main():
    spec = importlib.util.spec_from_file_location(
        "analyst_workbook", ROOT / "examples/analyst_workbook.py"
    )
    examples = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(examples)
    sample = examples.cases(ROOT / ".work" / ("doc-examples-" + uuid.uuid4().hex[:8]))
    inventory = []
    toc = [
        "API reference",
        "=============",
        "",
        "See :doc:`contract` for shared conventions, rejection semantics and purity.",
        "",
        ".. toctree::",
        "   :maxdepth: 1",
        "",
    ]
    for name in sorted(sample):
        func = getattr(fae, name)
        args, kwargs, check = sample[name]
        value = func(*args, **kwargs)
        assert check(value), name
        refs = [f"FR-{n:03d}" for n, names in FR.items() if name in names]
        page = ROOT / "docs/api" / f"{name}.rst"
        text = [
            name,
            "=" * len(name),
            "",
            f".. autofunction:: financial_accounting_engine.{name}",
            "",
            "Accounting/API contract",
            "-----------------------",
            "",
            f"Requirements: {', '.join(refs) or 'Library access/governance contract'}.",
            "Reference basis: frozen policy/rules 2026_V1, input contract 1.1.0.",
            "Source paragraphs are retained in decision outputs and the formula registry;",
            "see the requirement mapping and correction notes for controlled judgements.",
            "",
            "Parameters",
            "----------",
            "",
        ]
        for parameter in inspect.signature(func).parameters:
            text += [f"``{parameter}``", f"   {PARAMETERS[parameter]}", ""]
        schema = describe(value)
        text += [
            "Return schema",
            "-------------",
            "",
            "Representative field/type schema (conditional decision fields may be absent;",
            "table columns and optional values are listed in :doc:`../schemas`)::",
            "",
        ]
        text += ["   " + line for line in json.dumps(schema, indent=2).splitlines()]
        text += [
            "",
            "Errors and effects",
            "------------------",
            "",
            "See :doc:`../contract` for finite-value, missing-data and timezone rules.",
            "Invalid domain inputs raise AccountingError; dataset issues use ValidationError;",
            "unknown/damaged resources and conflicting export targets use ResourceError.",
            "Only export_profile and export_results create files. run_dataset may read XLSX;",
            "benchmark_ecl briefly measures time/memory. Other calls are in-memory or read",
            "immutable package resources. No call contacts external services.",
            "",
            "Executable example and direct test",
            "----------------------------------",
            "",
            f"``examples/analyst_workbook.py`` case ``{name}`` supplies the arguments and an",
            "independent expected-result assertion. Its function call is::",
            "",
            "   import financial_accounting_engine as fae",
            f"   actual = fae.{name}(*args, **kwargs)",
            "   assert check(actual)",
            "",
            f"Executed pytest ID: ``tests/test_api.py::test_api_example[{name}]``.",
            "",
        ]
        page.write_text("\n".join(text), encoding="utf-8")
        toc.append(f"   api/{name}")
        inventory.append(
            dict(
                name=name,
                module=func.__module__,
                signature=str(inspect.signature(func)),
                requirements=refs,
                documentation=f"docs/api/{name}.rst",
                example="examples/analyst_workbook.py",
                example_key=name,
                tests=[f"tests/test_api.py::test_api_example[{name}]"],
                return_schema=schema,
                status="IMPLEMENTED",
            )
        )
    (ROOT / "docs/api.rst").write_text("\n".join(toc) + "\n")
    (ROOT / "tools/api_inventory.json").write_text(
        json.dumps(
            {
                "status": "IMPLEMENTED",
                "functions": inventory,
                "classes": [
                    "AccountingError",
                    "AnalysisResult",
                    "ResourceError",
                    "ValidationError",
                ],
                "constants": ["__version__"],
            },
            indent=2,
        )
        + "\n"
    )
    req = [
        "Requirement coverage",
        "====================",
        "",
        "Mapping of all 60 frozen accounting requirements. IMPLEMENTED denotes generic",
        "reference functionality, not institutionally approved accounting.",
        "",
        ".. list-table::",
        "   :header-rows: 1",
        "",
        "   * - Requirement",
        "     - Public calls",
        "     - Status",
    ]
    for number, names in FR.items():
        status = (
            "CONTROLLED_INTERFACE" if number in (4, 12, 18, 25, 36, 37, 50, 56) else "IMPLEMENTED"
        )
        if number == 51:
            status = "NOT_APPLICABLE in frozen knowledge baseline; no final DRM model implemented"
        if number == 59:
            status = (
                "CLI/shared workflow implemented; browser app is a separate optional integration"
            )
        req += [
            f"   * - FR-{number:03d}",
            f"     - {', '.join(names) or 'None'}",
            f"     - {status}",
        ]
    (ROOT / "docs/requirements.rst").write_text("\n".join(req) + "\n")
    schemas = [
        "Schemas",
        "=======",
        "",
        "Input fields",
        "------------",
        "",
        "All tables include canonical record/version/valid/known-time fields.",
        "The following dictionary is preserved from the 1.1.0 input contract. Numeric",
        "currency is instrument-local unless the field explicitly names presentation.",
        "Conditional nullability depends on the selected approach. Runtime validation",
        "adds strict numeric/boolean checks described in :doc:`contract`.",
        "",
    ]
    for table, desc in fae.get_schema().items():
        schemas += [
            table,
            "~" * len(table),
            "",
            f"Workbook: ``{desc['workbook']}``.",
            "",
            ".. list-table::",
            "   :header-rows: 1",
            "",
            "   * - Field",
            "     - Declared type",
            "     - Nullable / unit",
        ]
        for field in desc["fields"]:
            schemas += [
                f"   * - {field['field']}",
                f"     - {field['type']}",
                f"     - {field['nullable']}; {field['unit']}",
            ]
        schemas.append("")
    schemas += [
        "Output tables",
        "-------------",
        "",
        "All domain tables carry object IDs, formula/rule references and run lineage where applicable.",
        "",
    ]
    results = [fae.run_dataset(fae.load_reference_data(p)) for p in fae.list_profiles()]
    for key in sorted({k for r in results for k in r.tables}):
        fields = describe([row for r in results for row in r.tables.get(key, ())])
        schemas += (
            [key, "~" * len(key), "", "Field names and observed types::", ""]
            + ["   " + line for line in json.dumps(fields, indent=2).splitlines()]
            + [""]
        )
    (ROOT / "docs/schemas.rst").write_text("\n".join(schemas) + "\n")
    print(f"{len(inventory)} API pages, input/output schemas and 60 requirement mappings generated")


if __name__ == "__main__":
    main()
