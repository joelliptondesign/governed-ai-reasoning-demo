"""Read-only aggregation utilities for completed run artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


RUNS_ROOT = Path(__file__).resolve().parents[1] / "runs"
VALID_STATUSES = ("PASS", "REVISE", "FAIL")


def _run_scored_results_path(run_id: str) -> Path:
    return RUNS_ROOT / run_id / "scored_results.json"


def _warn(message: str) -> None:
    print(f"WARNING: {message}")


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def load_run_cases(run_id: str) -> list[dict]:
    """Load scored case results for a completed run."""
    if not isinstance(run_id, str) or not run_id.strip():
        raise ValueError("run_id must be a non-empty string")

    path = _run_scored_results_path(run_id.strip())
    if not path.exists():
        raise FileNotFoundError(f"missing scored results for run '{run_id}': {path}")

    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if isinstance(payload, dict):
        cases = payload.get("results")
    elif isinstance(payload, list):
        cases = payload
    else:
        raise ValueError(f"invalid scored results format for run '{run_id}': expected object or list")

    if not isinstance(cases, list):
        raise ValueError(f"invalid scored results format for run '{run_id}': missing results list")

    normalized_cases: list[dict] = []
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            _warn(f"skipping malformed case at index {index} in run '{run_id}'")
            continue
        normalized_cases.append(case)

    return normalized_cases


def compute_status_distribution(cases: list[dict]) -> dict:
    """Count actual final statuses across scored cases."""
    distribution = {status: 0 for status in VALID_STATUSES}
    distribution["total"] = 0

    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            _warn(f"skipping malformed case at index {index} while computing status distribution")
            continue

        distribution["total"] += 1
        status = case.get("actual_final_status")
        if status in VALID_STATUSES:
            distribution[status] += 1
        else:
            case_id = case.get("case_id", f"index {index}")
            _warn(f"case '{case_id}' missing or invalid actual_final_status; excluding from status buckets")

    return distribution


def compute_average_score(cases: list[dict]) -> float:
    """Compute the average total score across valid scored cases."""
    total = 0.0
    count = 0

    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            _warn(f"skipping malformed case at index {index} while computing average score")
            continue

        score = case.get("total_score")
        if not _is_number(score):
            case_id = case.get("case_id", f"index {index}")
            _warn(f"case '{case_id}' missing numeric total_score; excluding from average score")
            continue

        total += float(score)
        count += 1

    if count == 0:
        return 0.0

    return total / count


def compute_critic_averages(cases: list[dict]) -> dict:
    """Compute mean critic scores for every numeric critic key present."""
    totals: dict[str, float] = {}
    counts: dict[str, int] = {}

    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            _warn(f"skipping malformed case at index {index} while computing critic averages")
            continue

        critic_scores = case.get("critic_scores")
        if critic_scores is None:
            continue
        if not isinstance(critic_scores, dict):
            case_id = case.get("case_id", f"index {index}")
            _warn(f"case '{case_id}' has malformed critic_scores; excluding from critic averages")
            continue

        for key, value in critic_scores.items():
            if not _is_number(value):
                continue
            totals[key] = totals.get(key, 0.0) + float(value)
            counts[key] = counts.get(key, 0) + 1

    critic_averages: dict[str, float] = {}
    for key in sorted(totals):
        critic_averages[key] = totals[key] / counts[key]

    return critic_averages


def build_run_summary(run_id: str) -> dict:
    """Build a deterministic read-only summary for a completed run."""
    cases = load_run_cases(run_id)
    status_distribution = compute_status_distribution(cases)

    return {
        "run_id": run_id,
        "num_cases": status_distribution["total"],
        "status_distribution": status_distribution,
        "average_score": compute_average_score(cases),
        "critic_averages": compute_critic_averages(cases),
    }
