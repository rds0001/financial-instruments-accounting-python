"""Inspect wheel and sdist contents without installing or extracting them."""

from __future__ import annotations

import argparse
import tarfile
import zipfile
from email.parser import BytesParser
from pathlib import Path, PurePosixPath

DIST_NAME = "financial-instruments-accounting"
VERSION = "1.0.0"
PACKAGE = "financial_accounting_engine"


def safe_names(names: list[str]) -> None:
    for name in names:
        path = PurePosixPath(name)
        assert not path.is_absolute() and ".." not in path.parts, f"Unsafe archive path: {name}"
        lowered = name.lower()
        assert "/.work/" not in f"/{lowered}" and "__pycache__" not in lowered
        assert not lowered.endswith((".pyc", ".pyo"))
        assert "scaffold" not in lowered


def check_metadata(raw: bytes) -> None:
    metadata = BytesParser().parsebytes(raw)
    assert metadata["Name"] == DIST_NAME
    assert metadata["Version"] == VERSION
    assert metadata["License-Expression"] == "Apache-2.0"
    assert "RiskDataScience GmbH" in metadata["Author"]
    assert "riskdatascience@web.de" in metadata["Maintainer-email"]
    urls = "\n".join(metadata.get_all("Project-URL", []))
    assert "financial-instruments-accounting-python" in urls
    assert "riskdatascience.net/impressum/" in urls
    assert "riskdatascience.net/datenschutzerklaerung/" in urls


def validate_wheel(path: Path) -> None:
    assert path.stat().st_size < 10_000_000, "Wheel unexpectedly large"
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        safe_names(names)
        metadata_name = next(name for name in names if name.endswith(".dist-info/METADATA"))
        check_metadata(archive.read(metadata_name))
        assert f"{PACKAGE}/__init__.py" in names
        assert f"{PACKAGE}/py.typed" in names
        assert sum(name.endswith(".xlsx") for name in names) == 38
        entry_name = next(name for name in names if name.endswith(".dist-info/entry_points.txt"))
        assert (
            b"financial-instruments-accounting = financial_accounting_engine._cli:main"
            in archive.read(entry_name)
        )
        assert any(name.endswith(".dist-info/licenses/LICENSE") for name in names)
        assert any(name.endswith(".dist-info/licenses/NOTICE") for name in names)
        assert not any("/tests/" in f"/{name}" or "/docs/" in f"/{name}" for name in names)


def validate_sdist(path: Path) -> None:
    assert path.stat().st_size < 10_000_000, "sdist unexpectedly large"
    with tarfile.open(path, "r:gz") as archive:
        members = [member for member in archive.getmembers() if member.isfile()]
        names = [member.name for member in members]
        safe_names(names)
        metadata_member = next(member for member in members if member.name.endswith("/PKG-INFO"))
        extracted = archive.extractfile(metadata_member)
        assert extracted is not None
        check_metadata(extracted.read())
        for suffix in ("/pyproject.toml", "/LICENSE", "/NOTICE", "/README.md"):
            assert any(name.endswith(suffix) for name in names), suffix
        assert any(name.endswith("/tests/golden_cases.json") for name in names)
        assert any(name.endswith("/tools/verify_source_tree.py") for name in names)
        assert any(name.endswith("/docs/corrections.rst") for name in names)
        assert sum(name.endswith(".xlsx") for name in names) == 38


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    wheels = sorted(args.directory.glob("*.whl"))
    sdists = sorted(args.directory.glob("*.tar.gz"))
    assert len(wheels) == 1, f"Expected one wheel, found {wheels}"
    assert len(sdists) == 1, f"Expected one sdist, found {sdists}"
    validate_wheel(wheels[0])
    validate_sdist(sdists[0])
    print(f"PASS: {wheels[0].name} and {sdists[0].name}")


if __name__ == "__main__":
    main()
