# Data Contracts

## Evaluation Run Artifacts

Path:
`runs/{run_id}/scored_results.json`

Structure:

```json
{
  "results": []
}
```

Each result item is a scored evaluation case. The aggregator reads this artifact.

## Service Runtime Artifacts

Path:
`data/runs.jsonl`

Structure:

Append-only JSON Lines storage for API runtime records. Each line is one run record containing lifecycle state and any persisted execution fields available for that run.

## Note

These are intentionally separate systems:

- evaluation pipeline (offline)
- service runtime (API)

They are not unified in this repo.
