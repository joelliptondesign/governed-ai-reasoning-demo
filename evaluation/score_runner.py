"""Scores raw evaluation results and persists run artifacts.

Flow:
raw_results.json -> scored_results.json -> runs/{run_id}/
"""

import json
from datetime import datetime, timezone
from pathlib import Path

INPUT_PATH = Path("evaluation/raw_results.json")
OUTPUT_PATH = Path("evaluation/scored_results.json")
RUNS_ROOT = Path("runs")


def generate_run_id():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z").replace(":", "-")


def persist_run_results(run_id: str, scored_results: dict):
    run_dir = RUNS_ROOT / run_id
    candidate_run_id = run_id
    version = 1

    while run_dir.exists():
        version += 1
        candidate_run_id = f"{run_id}_v{version}"
        run_dir = RUNS_ROOT / candidate_run_id

    run_dir.mkdir(parents=True, exist_ok=False)

    with (run_dir / "scored_results.json").open("w", encoding="utf-8") as f:
        json.dump(scored_results, f, indent=2)

    return candidate_run_id


def compute_total_score(scores):
    numeric_scores = [
        v for v in scores.values()
        if isinstance(v, (int, float))
    ]
    return sum(numeric_scores)


def compute_status(scores):
    total = compute_total_score(scores)

    # Hard fail
    if scores.get("diagnosis_consistency_score", 2) == 0:
        return "FAIL", total

    if total >= 7:
        return "PASS", total
    elif total >= 4:
        return "REVISE", total
    else:
        return "FAIL", total


def extract_scores(pipeline_output):
    # Assumes critic_scores exist in output
    return pipeline_output.get("critic_scores", {})


def extract_final_status(pipeline_output):
    return pipeline_output.get("final_status", "UNKNOWN")


def main():
    with open(INPUT_PATH, "r") as f:
        data = json.load(f)["results"]

    scored = []

    for item in data:
        output = item.get("pipeline_output", {})

        scores = extract_scores(output)

        if not scores:
            scored.append({
                "case_id": item["case_id"],
                "scenario_type": item.get("scenario_type"),
                "expected_behavior": item.get("expected_behavior"),
                "actual_final_status": extract_final_status(output),
                "computed_final_status": "FAIL",
                "total_score": 0,
                "critic_scores": {},
                "error": "missing_critic_scores"
            })
            continue

        computed_status, total_score = compute_status(scores)

        scored.append({
            "case_id": item["case_id"],
            "scenario_type": item["scenario_type"],
            "expected_behavior": item["expected_behavior"],
            "actual_final_status": extract_final_status(output),
            "computed_final_status": computed_status,
            "total_score": total_score,
            "critic_scores": scores
        })

    scored_results = {"results": scored}

    with open(OUTPUT_PATH, "w") as f:
        json.dump(scored_results, f, indent=2)

    try:
        run_id = generate_run_id()
        persisted_run_id = persist_run_results(run_id, scored_results)
        print(f"[RUN SAVED] run_id={persisted_run_id}")
    except Exception as exc:
        print(f"WARNING: failed to persist scored results: {exc}")


if __name__ == "__main__":
    main()
