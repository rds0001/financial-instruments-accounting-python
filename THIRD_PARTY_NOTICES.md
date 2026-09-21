<!-- Copyright 2026 RiskDataScience GmbH -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Third-party notices

No third-party libraries or external standards documents are vendored in this repository.

Runtime dependencies installed by users:

| Package | Version constraint | Licence | Project |
|---|---|---|---|
| openpyxl | 3.1.5 | MIT | <https://openpyxl.readthedocs.io/> |
| PyYAML | 6.0.2 | MIT | <https://pyyaml.org/> |

Development and build dependencies installed by users:

| Package | Version constraint | Licence | Project |
|---|---|---|---|
| pytest | >=8 | MIT | <https://pytest.org/> |
| setuptools | >=77.0.3 | MIT | <https://setuptools.pypa.io/> |

Transitive dependencies are resolved by the user's Python package installer and remain governed by their own licences. Distributors of binary bundles must generate and review a dependency inventory for the exact resolved environment.

External accounting standards, legislation, supervisory publications, and other source materials are not distributed. Their metadata and official locations are listed in `financial_accounting_engine/resources/sources.json` (also exposed through `get_sources()`); the repository licence does not apply to them.

Additional development tools (not runtime dependencies or vendored code): Hypothesis (MPL-2.0), Ruff (MIT), mypy (MIT), Sphinx (BSD-2-Clause), build (MIT), Twine (Apache-2.0), wheel (MIT), types-PyYAML (Apache-2.0). See the installed tool metadata for exact resolved versions.
