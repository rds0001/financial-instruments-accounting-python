"""Typed value, table and result contracts for the public accounting API."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence, TypeAlias

Scalar: TypeAlias = str | int | float | bool | None
Row: TypeAlias = Mapping[str, Scalar]
Table: TypeAlias = Sequence[Row]
Dataset: TypeAlias = Mapping[str, Table]
JSONValue: TypeAlias = "Scalar | list[JSONValue] | dict[str, JSONValue]"


class AccountingError(ValueError):
    """A rejected input or accounting judgement; no partial result is approved."""


class ValidationError(AccountingError):
    """Dataset rejection with machine-readable issues (severity/code/object/message)."""

    def __init__(self, issues: Table):
        self.issues = tuple(dict(r) for r in issues)
        super().__init__("; ".join(str(r.get("message")) for r in issues))


class ResourceError(AccountingError):
    """An unknown or damaged packaged resource or an unsafe export target."""


@dataclass(frozen=True)
class AnalysisResult:
    """Result with named tables, metrics, audit lineage and reference-only status.

    ``tables`` uses workbook/sheet keys; ``metrics`` contains scalar totals and
    category distributions; ``lineage`` records input, code and policy hashes.
    Accessors return copies. ``official`` is always False for this library.
    """

    tables: Mapping[str, Table]
    metrics: Mapping[str, JSONValue]
    lineage: Mapping[str, JSONValue]
    status: str
    official: bool = False

    def __post_init__(self) -> None:
        if self.official or self.status not in {"APPROVED_REFERENCE", "REVIEW_REQUIRED"}:
            raise AccountingError("Library results cannot be official or use an unknown status")
