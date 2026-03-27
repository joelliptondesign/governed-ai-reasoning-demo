"""CLI utility for inspecting a persisted run.

Usage:
python scripts/test_run_aggregator.py --run_id <RUN_ID>
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from service.run_aggregator import build_run_summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Print aggregated summary for a completed run.")
    parser.add_argument("--run_id", required=True, help="Run identifier under runs/<run_id>/")
    args = parser.parse_args()

    summary = build_run_summary(args.run_id)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
