# Copyright 2026 RiskDataScience GmbH
# SPDX-License-Identifier: Apache-2.0
"""Deterministic model monitoring for reference and challenger observations."""

from __future__ import annotations

from collections import defaultdict


def _weighted_mean(rows: list[dict], field: str) -> float:
    weight = sum(float(row["exposure_weight"]) for row in rows)
    if weight <= 0:
        raise ValueError("Backtesting weights must be positive")
    return sum(float(row[field]) * float(row["exposure_weight"]) for row in rows) / weight


def _auc(rows: list[dict]) -> float | None:
    positives = [row for row in rows if bool(row.get("outcome_flag"))]
    negatives = [row for row in rows if not bool(row.get("outcome_flag"))]
    if not positives or not negatives:
        return None
    score = 0.0
    for positive in positives:
        for negative in negatives:
            left, right = float(positive["predicted_value"]), float(negative["predicted_value"])
            score += 1.0 if left > right else 0.5 if left == right else 0.0
    return score / (len(positives) * len(negatives))


def evaluate(observations: list[dict]) -> list[dict]:
    """Return model-level calibration, error and discrimination diagnostics."""
    grouped: dict[tuple, list[dict]] = defaultdict(list)
    for row in observations:
        required = (
            "model_type",
            "model_version_id",
            "predicted_value",
            "actual_value",
            "model_owner",
            "validation_status",
            "approval_id",
        )
        missing = [field for field in required if row.get(field) in (None, "")]
        if missing:
            raise ValueError(
                f"Incomplete backtesting observation {row.get('observation_id')}: {missing}"
            )
        if row["validation_status"] not in {"VALIDATED", "CONDITIONALLY_VALIDATED"}:
            raise ValueError(f"Unusable model validation status: {row['model_version_id']}")
        if float(row["exposure_weight"]) <= 0:
            raise ValueError("Observation weights must be positive")
        grouped[
            (
                row["model_type"],
                row["model_version_id"],
                bool(row.get("challenger_flag")),
                row.get("segment") or "ALL",
            )
        ].append(row)
    results = []
    for (model_type, version, challenger, segment), rows in sorted(grouped.items()):
        predicted = _weighted_mean(rows, "predicted_value")
        actual = _weighted_mean(rows, "actual_value")
        mae = _weighted_mean(
            [
                {**r, "absolute_error": abs(float(r["predicted_value"]) - float(r["actual_value"]))}
                for r in rows
            ],
            "absolute_error",
        )
        result = {
            "model_type": model_type,
            "model_version_id": version,
            "challenger_flag": challenger,
            "segment": segment,
            "observations": len(rows),
            "weighted_prediction": predicted,
            "weighted_actual": actual,
            "calibration_ratio": actual / predicted if predicted else None,
            "mean_absolute_error": mae,
            "bias": predicted - actual,
            "auc": _auc(rows) if model_type in {"PD", "STAGING"} else None,
            "release_amount": sum(float(r.get("release_amount") or 0) for r in rows),
            "model_owner": rows[0]["model_owner"],
            "validation_status": rows[0]["validation_status"],
            "approval_id": rows[0]["approval_id"],
            "formula_id": "F-BT-001",
        }
        results.append(result)
    return results
