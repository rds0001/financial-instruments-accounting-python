Corrections and baseline comparison
===================================

Baseline and method
-------------------

The migration baseline is application engine 1.2.0, input contract 1.1.0,
two complete synthetic profiles, 19 input workbooks, seven output workbooks
and 87 passing historical tests.  The baseline source and outputs were frozen
before implementation.  The new public API then added independent formula
vectors and explicit boundary tests.  It did not treat byte-identical XLSX
files or copied algorithms as proof of accounting correctness.

``tools/freeze_reference.py`` compares stable business keys, decisions,
atomic table fields, controls and aggregate values.  It ignores only the
language/run-specific ``run_id`` and normalises an empty spreadsheet
``explanation`` cell to null.  Any new unclassified difference aborts the
maintenance command.  The reviewed field-level ledger is stored in
``docs/correction_ledger.json``.  The corrected cross-language reference is
``resources/golden.json``; the independent hand-calculated cases are
``tests/golden_cases.json``.

Reviewed changes
----------------

The comparison records 203 field changes, including dependent atomic and
aggregate results:

.. list-table::
   :header-rows: 1

   * - Classification
     - Fields
     - Accounting effect
   * - POCI credit-adjusted rate and net interest
     - 83
     - Uses 7.5% credit-adjusted EIR instead of the ordinary 7% EIR; retains a signed change from the initial lifetime-ECL baseline and calculates POCI interest on the explicit net basis.
   * - Hedge gain sign and reserve release
     - 108
     - Applies the cash-flow/net-investment lower-of amount, credits signed gains, and records recycling and basis adjustment as separate reserve removals.
   * - Explicit zero for nonapplicable movement
     - 5
     - Makes a previously absent, nonapplicable zero visible in stable result schemas.
   * - Modification journal sign
     - 4
     - Credits gains and debits losses using nonnegative debit/credit columns.
   * - Write-off allowance utilisation
     - 3
     - Avoids a second profit-or-loss charge when the reference event consumes an existing allowance.

For ``MID_SIZE_UNIVERSAL_FIA``, total ECL changes from
372,972.0342412043 to 372,727.1317328072, a decrease of
244.9025083971.  The POCI instrument's weighted lifetime ECL is
28,446.65099334865; against an initial baseline of 15,000 its signed
allowance change is 13,446.650993348649.  Annual POCI interest is
4,991.501175498851 on the explicit net basis.  The small profile ECL remains
92,039.1234660137.

Other corrected boundaries do not necessarily alter the bundled profiles:

* zero cure/probation months are valid values rather than missing data;
* approved past-due rebuttals and overrides are expiry checked;
* absolute SICR change works when original lifetime PD is zero, while the
  relative test does not divide by zero;
* a de-minimis contingent feature does not bypass principal, interest or
  leverage facts, and trading equity cannot elect FVOCI;
* component and direct-cash-shortfall POCI calculations use the
  credit-adjusted rate and permit favourable signed changes;
* own-credit journals apply only to FVTPL liabilities and no journal contains
  negative debit or credit values;
* local-currency allowance is used for net interest before presentation FX;
* opening allowance is not added twice; signed POCI allowance is retained;
* monitoring weight zero, duplicate/missing curves, shared-collateral
  over-allocation, invalid seals and policy/input conflicts reject.

Independent references and limits
---------------------------------

The POCI correction follows IFRS 9 paragraphs 5.5.13--5.5.14: a favourable
change in lifetime expected losses is an impairment gain even below the amount
included at initial recognition.  The hedge correction follows the lower-of
mechanism referenced by paragraphs 6.5.11 and 6.5.13.  Official-source metadata
and URLs are available through :func:`financial_accounting_engine.get_sources`;
the external standards are not redistributed.

This is a frozen generic reference implementation, not a new assertion that
every current or institution-specific requirement has been independently
certified.  Business model, SPPI contract facts, fair values, models,
counterparty status, mappings and approvals remain controlled inputs.  Gross
rollforward ``other_contractual_and_fx_movements`` is an explicit residual and
is not independent ledger evidence.  R implementation and Python/R parity
remain pending until the separately authorised native R package is built.
