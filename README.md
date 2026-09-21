# financial-instruments-accounting

An Apache-2.0 Python reference library for financial instrument classification,
measurement, expected credit losses, hedge accounting, journals and audit controls.
IFRS 9 describes its accounting basis, not a product endorsement or certification.

```python
import financial_accounting_engine as fae
assert abs(fae.effective_interest_rate(1000, [(1, 1100)]) - .1) < 1e-9
result = fae.run_dataset(fae.load_reference_data("SMALL_SA_RETAIL_FIA"))
print(fae.get_metrics(result))
```

Installation from a checked-out source tree: `python -m pip install .`.
CLI: `financial-instruments-accounting --help`.

Python 3.10+ syntax; local verification uses Python 3.10. Broader platform/version
verification is reserved for external CI. Stable public imports are at the package
root and in `formulas`, `domains`, `data`, `workflow` and `models`.
API documentation and tutorials are in `docs/`; executable examples in `examples/`.

Source and issue tracking:
[github.com/rds0001/financial-instruments-accounting-python](https://github.com/rds0001/financial-instruments-accounting-python).

All reference data are synthetic. Outputs are at most APPROVED_REFERENCE, never
institutionally OFFICIAL. Contract judgements, approved models, market valuations
and ledger integration remain caller responsibilities. This library is not a
complete implementation of every IFRS standard. See DISCLAIMER.md.

Copyright 2026 RiskDataScience GmbH. Contact: riskdatascience@web.de.
[Imprint](https://riskdatascience.net/impressum/) ·
[Privacy Policy](https://riskdatascience.net/datenschutzerklaerung/).
