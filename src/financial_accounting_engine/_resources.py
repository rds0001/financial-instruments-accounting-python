"""Offline package resources, independent of repository layout and CWD."""

from __future__ import annotations

import hashlib
import json
from importlib.resources import files
from typing import cast

import yaml

from .models import JSONValue, ResourceError


def read_bytes(relative: str) -> bytes:
    if relative.startswith("/") or ".." in relative.split("/"):
        raise ResourceError("Resource path must be package-relative")
    try:
        return (
            files("financial_accounting_engine")
            .joinpath("resources")
            .joinpath(relative)
            .read_bytes()
        )
    except (FileNotFoundError, IsADirectoryError) as exc:
        raise ResourceError(f"Unknown resource: {relative}") from exc


def read_json(relative: str) -> dict[str, JSONValue]:
    obj = json.loads(read_bytes(relative))
    if not isinstance(obj, dict):
        raise ResourceError("JSON resource must be an object")
    return cast(dict[str, JSONValue], obj)


def configuration(group: str, identifier: str, key: str) -> dict[str, JSONValue]:
    root = (
        files("financial_accounting_engine")
        .joinpath("resources")
        .joinpath("configuration")
        .joinpath(group)
    )
    matches = []
    for path in root.iterdir():
        if path.name.endswith(".yaml"):
            obj = yaml.safe_load(path.read_text(encoding="utf-8"))
            if isinstance(obj, dict) and obj.get(key) == identifier:
                matches.append(obj)
    if len(matches) != 1:
        raise ResourceError(f"Unknown or ambiguous {key}: {identifier}")
    return cast(dict[str, JSONValue], matches[0])


def source_inventory_valid() -> bool:
    sources = read_json("sources.json").get("sources")
    if not isinstance(sources, list) or not sources:
        return False
    required = {"source_id", "title", "issuer", "official_url", "archival_sha256", "redistributed"}
    return all(
        isinstance(s, dict)
        and required <= s.keys()
        and s["redistributed"] is False
        and str(s["official_url"]).startswith("https://")
        and len(str(s["archival_sha256"])) == 64
        for s in sources
    )


def verify_resources() -> dict[str, str]:
    manifest = read_json("manifest.json")
    hashes = {}
    for key, expected in manifest.items():
        actual = hashlib.sha256(read_bytes(key)).hexdigest()
        if actual != expected:
            raise ResourceError(f"Damaged resource: {key}")
        hashes[key] = actual
    return hashes
