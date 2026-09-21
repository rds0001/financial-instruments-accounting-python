# financial-instruments-accounting

`financial-instruments-accounting` is an auditable, offline-capable Python
library for granular financial instrument accounting calculations and reference
workflows. It provides typed building blocks for classification, measurement,
impairment, hedge accounting, journal preparation, disclosures and model
monitoring in one reproducible package.

The methodology is designed around financial instrument accounting concepts in
IFRS 9 and related presentation and disclosure interfaces. The project name is
independent of the standard. The library is not affiliated with, endorsed by or
certified by the IFRS Foundation or any standard setter.

## Capabilities

The package exposes 80 documented public functions across five stable modules:
`formulas`, `domains`, `data`, `workflow` and `models`.

- Scope, recognition, derecognition and continuing involvement
- Business-model and contractual-cash-flow characteristic assessments
- Classification and reclassification reference decisions
- Initial measurement, effective interest rates, amortised cost and interest
  revenue, including purchased or originated credit-impaired instruments
- Multi-scenario expected credit losses using PD/LGD/EAD components, discounted
  cash shortfalls or provision matrices
- Staging, significant-increase-in-credit-risk assessment, overlays, collateral
  allocation, modifications, write-offs and recoveries
- Fair-value presentation, own-credit separation and OCI rollforwards
- Hedge eligibility, effectiveness, lower-of measurement, reserve movements,
  recycling and basis adjustments
- Journal preparation, allowance and gross-carrying-amount rollforwards,
  disclosure facts and regulatory bridges
- PD, LGD, EAD and staging backtesting, challenger comparison, scenario
  sensitivity and audit controls
- Bitemporal input selection, strict validation, resource hashes and result
  lineage

## Installation and first run

```bash
python -m pip install financial-instruments-accounting
```

The distribution name uses hyphens; the Python import namespace is
`financial_accounting_engine`.

```python
import financial_accounting_engine as fae

eir = fae.effective_interest_rate(1000, [(1, 1100)])
assert abs(eir - 0.1) < 1e-9

dataset = fae.load_reference_data("SMALL_SA_RETAIL_FIA")
result = fae.run_dataset(dataset)
assert result.status == "APPROVED_REFERENCE"
print(fae.get_metrics(result))
```

The command-line interface uses the same public workflow:

```bash
financial-instruments-accounting doctor
financial-instruments-accounting profiles
financial-instruments-accounting reference SMALL_SA_RETAIL_FIA --output ./results
```

## Reference data and reproducibility

Two complete synthetic profiles are bundled for offline examples, integration
tests and cross-implementation comparison. Each profile contains 19 sealed XLSX
input workbooks plus canonical JSON data. No client, bank or personal data are
included.

Reference calculations are checked against independently specified formula
cases and frozen full-profile results. The repository also contains API-contract
tests, property tests, correction evidence, resource manifests and installed
wheel/sdist smoke tests. GitHub Actions verifies Python 3.10 through 3.13.

## Scope and legal notice

`APPROVED_REFERENCE` means that the package's automated reference controls have
passed. It is not an institutional approval, an audit opinion or an accounting
conclusion. Users remain responsible for contract interpretation, accounting
policy choices, approved models and parameters, market data, materiality,
governance, ledger integration and financial-statement review.

The software does not implement every requirement, exception or disclosure in
IFRS Accounting Standards and is not a substitute for the standards or for
professional accounting, audit, legal or risk advice. Official source metadata
and links are provided for traceability; standard texts and other third-party
materials are not redistributed. Obtain authoritative, current materials from
their publishers and observe their terms.

The Apache License 2.0 applies to this software and its synthetic project data.
It does not grant rights in third-party standards, publications or trademarks.
See `DISCLAIMER.md`, `THIRD_PARTY_NOTICES.md` and `NOTICE` in the source
repository.

## Documentation and project links

- [Source repository](https://github.com/rds0001/financial-instruments-accounting-python)
- [API documentation and tutorials](https://github.com/rds0001/financial-instruments-accounting-python/tree/main/docs)
- [Issue tracker](https://github.com/rds0001/financial-instruments-accounting-python/issues)
- [Security policy](https://github.com/rds0001/financial-instruments-accounting-python/security/policy)
- [Imprint](https://riskdatascience.net/impressum/)
- [Privacy policy](https://riskdatascience.net/datenschutzerklaerung/)

Copyright 2026 RiskDataScience GmbH. Maintainer contact:
riskdatascience@web.de.
