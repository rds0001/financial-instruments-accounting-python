"""Verify that the publishable source tree is complete and contains no local debris."""

from __future__ import annotations

import inspect
import json
import re
from pathlib import Path

import financial_accounting_engine as fae
from financial_accounting_engine._resources import verify_resources

ROOT = Path(__file__).resolve().parents[1]
IGNORED = {
    ".git",
    ".hypothesis",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".work",
    "__pycache__",
    "build",
    "dist",
}
REQUIRED = {
    "CHANGELOG.md",
    "CITATION.cff",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "DISCLAIMER.md",
    "LICENSE",
    "MANIFEST.in",
    "NOTICE",
    "README.md",
    "SECURITY.md",
    "THIRD_PARTY_NOTICES.md",
    "pyproject.toml",
    ".github/CODEOWNERS",
    ".github/dependabot.yml",
    ".github/workflows/ci.yml",
    ".github/workflows/publish.yml",
    "src/financial_accounting_engine/__init__.py",
    "src/financial_accounting_engine/py.typed",
    "tests/golden_cases.json",
    "tools/api_inventory.json",
}
TEXT_SUFFIXES = {".cff", ".in", ".json", ".md", ".py", ".rst", ".toml", ".yaml", ".yml"}
SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{30,}\b"),
    "AWS access key": re.compile(r"\bAKIA[A-Z0-9]{16}\b"),
}


def publishable_files() -> list[Path]:
    files = []
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if any(part in IGNORED or part.endswith(".egg-info") for part in relative.parts):
            continue
        if path.is_symlink():
            raise AssertionError(f"Symlink is not allowed in the release tree: {relative}")
        if path.is_file():
            files.append(path)
    return files


def main() -> None:
    files = publishable_files()
    names = {path.relative_to(ROOT).as_posix() for path in files}
    missing = REQUIRED - names
    assert not missing, f"Missing release files: {sorted(missing)}"
    assert not any("scaffold" in name.lower() for name in names)
    assert not any(name.lower().endswith((".pdf", ".doc", ".docx")) for name in names)
    assert len(list((ROOT / "docs/api").glob("*.rst"))) == 80

    inventory = json.loads((ROOT / "tools/api_inventory.json").read_text(encoding="utf-8"))
    assert len(inventory["functions"]) == 80
    assert len([name for name in fae.__all__ if inspect.isfunction(getattr(fae, name))]) == 80

    for path in files:
        if path == Path(__file__) or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        content = path.read_text(encoding="utf-8")
        for label, pattern in SECRET_PATTERNS.items():
            assert pattern.search(content) is None, f"Possible {label} in {path.relative_to(ROOT)}"

    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'name = "financial-instruments-accounting"' in pyproject
    assert 'license = "Apache-2.0"' in pyproject
    assert "financial-instruments-accounting-python" in pyproject
    assert "riskdatascience@web.de" in pyproject

    source_metadata = json.loads(
        (ROOT / "src/financial_accounting_engine/resources/sources.json").read_text(encoding="utf-8")
    )
    assert source_metadata["distribution_policy"] == "EXTERNAL_REFERENCES_ONLY"
    assert all(source["redistributed"] is False for source in source_metadata["sources"])
    assert fae.list_profiles() == ("MID_SIZE_UNIVERSAL_FIA", "SMALL_SA_RETAIL_FIA")
    assert len(verify_resources()) >= 50
    for profile in fae.list_profiles():
        profile_dir = ROOT / "src/financial_accounting_engine/resources/profiles" / profile / "1.0.0"
        assert len(list(profile_dir.glob("*.xlsx"))) == 19

    print(f"PASS: {len(files)} publishable files; 80 APIs; sealed resources verified")


if __name__ == "__main__":
    main()
