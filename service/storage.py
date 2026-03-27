"""Append-only JSONL storage for service run artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


RUNS_PATH = Path(__file__).resolve().parents[1] / "data" / "runs.jsonl"


def _ensure_storage_file() -> None:
    RUNS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RUNS_PATH.touch(exist_ok=True)


def append_run(record: dict[str, Any]) -> None:
    _ensure_storage_file()
    with RUNS_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=True) + "\n")


def get_run(run_id: str) -> dict[str, Any] | None:
    _ensure_storage_file()
    with RUNS_PATH.open("r", encoding="utf-8") as handle:
        for line in handle:
            raw = line.strip()
            if not raw:
                continue
            record = json.loads(raw)
            if record.get("run_id") == run_id:
                return record
    return None


def list_runs() -> list[dict[str, Any]]:
    _ensure_storage_file()
    runs: list[dict[str, Any]] = []
    with RUNS_PATH.open("r", encoding="utf-8") as handle:
        for line in handle:
            raw = line.strip()
            if not raw:
                continue
            record = json.loads(raw)
            runs.append(
                {
                    "run_id": record.get("run_id"),
                    "timestamp": record.get("timestamp"),
                }
            )
    return runs
