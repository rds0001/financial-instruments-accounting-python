API and data contract
=====================

Versioning and imports
----------------------

The standalone library starts at 1.0.0; its ancestor is the reference application
engine 1.2.0. These are separate version sequences. The canonical input contract
remains 1.1.0. Historical FIA workbook/profile identifiers are deliberately retained
so sealed input bytes and their provenance remain valid. Public symbols are exported
at ``financial_accounting_engine`` and their documented submodules. Names beginning
with an underscore are internal and may change without compatibility guarantees.

The old imports ``ifrs9_engine`` and ``financial_instruments_engine`` are not aliases.
Distribution name: ``financial-instruments-accounting``; CLI:
``financial-instruments-accounting``. The Python import namespace is
``financial_accounting_engine``.
There is no package import-time data download or calculation.

Types and errors
----------------

``Row`` means a mapping from field name to str/int/float/bool/None. ``Table`` is an
ordered sequence of rows. ``Dataset`` maps the 19 canonical input table names to
tables. Field schemas are listed in :doc:`schemas` and available through get_schema.
Nested configuration/metric structures use the recursive JSONValue type, not Any.
Functions do not mutate caller-supplied rows or policies. Accessors return copies.
AnalysisResult's frozen attributes contain caller-readable table/metric mappings;
those nested mappings are not an immutable database or a signed approval artifact.

AccountingError is the stable ValueError subclass for invalid domain inputs.
ValidationError includes ``issues`` with severity, code, object and message fields.
ResourceError indicates an unknown/damaged resource or a refused export target.
Filesystem errors may additionally raise OSError. No exception is interpreted as
an approved accounting result. Imported scalar formulas reject booleans, numeric
strings, None, NaN and infinity. Conditional null fields in canonical records remain
None; a missing required value is not zero. Empty risk vectors return empty vectors;
empty EIR/direct-shortfall/scenario populations reject. Empty monitoring populations
return no result rows; missing monitoring outcomes are not inferred.

Units, timing and precision
---------------------------

Rates, PDs, LGDs, CCFs, haircuts and scenario weights are decimal fractions, not
percentages. Times are year fractions supplied by the caller. Annual PD curve years
are positive integers. Scalar money has no implicit currency conversion; every
operand in one calculation uses the same currency. The pipeline explicitly converts
local ECL/event amounts to the configured presentation currency. Interest outputs
remain local-currency annual amounts. Hedge inputs use presentation currency because
the historical hedge contract has no independent FX column.

Discounting compounds annually. The inherited amortised-cost step uses simple
accrual within the caller's period: opening * EIR * year_fraction. A fractional-year
schedule using this step is therefore not an effective compounding schedule. Select
periods and convention deliberately; the library does not infer contractual day count.

Calculations retain binary64 precision. No intermediate rounding or automatic
journal rounding is applied. The policy describes reporting rounding; institutional
posting precision is an integration responsibility. Formula tests use separate
rate/probability and monetary tolerances. Golden comparisons use
abs(actual-expected) <= abs_tol + rel_tol*abs(expected); NaN/Inf never pass.

Lifetime ECL and recoveries
---------------------------

Component ECL uses unconditional marginal PD. LGD incorporates recovery timing
relative to default; component discounting is then from default to reporting date.
The Stage-1 limit selects defaults in the next 12 months, not recoveries in that year.
Direct-shortfall input must already represent the intended default-event population;
it can retain later recoveries. Provision rates are supplied lifetime segment rates.
The library does not fit models or infer incomplete lifetime tails.

POCI allowance is represented as a signed change from initial lifetime ECL. A
favourable change can be negative. POCI uses the credit-adjusted rate. Net-interest
presentation uses gross less the signed allowance under this explicit convention.

Policies and controlled judgements
----------------------------------

The default selects EU_FINANCIAL_INSTRUMENTS_2026_V1 and FIA_RULES_2026_V1, with the
reference knowledge timestamp 2026-09-02T12:00:00+02:00 and reporting date 2026-12-31.
It never means the latest law or an automatically approved institutional policy.
Complete policy overrides are accepted; missing required thresholds reject.
Run-control dates/IDs must agree with the selected policy and rule set.

Scope, SPPI features, business model, fairness of prepayment compensation, model
approvals, fair values and transfer judgements are controlled supplied facts. A
boolean decision is not an automated contract/legal interpretation. IBOR relief is
only a recorded approved applicability interface; automatic reform relief is outside
this generic library. R implementation/parity and institutional OFFICIAL approval
remain pending and are never implied by Python reference approval.

I/O, resources and lineage
--------------------------

Pure formulas and domain functions need no Excel files, complete run or web app.
load_reference_data returns offline synthetic tables. export_profile creates a new
user directory containing the 19 sealed inputs and their manifest. run_dataset accepts
those files or in-memory tables and writes nothing. export_results creates a new
directory with seven workbooks, neutral JSON and hashed manifest. Existing export
directories are refused, preserving earlier artifacts. Interrupted filesystem exports
may leave a partial new directory; their missing manifest must not be treated as valid.

Dataset fingerprints cover canonical tables, policy, rules, packaged resources and
Python source. Numeric equality is independent of XLSX ZIP timestamps and language-
specific code/run hashes. Bitemporal valid/known intervals are inclusive; knowledge
timestamps require an explicit offset. Historical official input flags select the
snapshot; they do not authorize OFFICIAL library outputs.

.. autoclass:: financial_accounting_engine.AnalysisResult
   :members:

.. autoexception:: financial_accounting_engine.AccountingError
.. autoexception:: financial_accounting_engine.ValidationError
.. autoexception:: financial_accounting_engine.ResourceError
