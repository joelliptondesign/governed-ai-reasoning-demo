# MedScribe — Stateful AI Execution & Evaluation System

## Overview

AI systems are increasingly used in workflows where the cost of being wrong is high.

But most systems still rely on a single model response.
That response can change between runs, ignore constraints, or produce outputs that look correct but aren't.

This creates a gap between what AI can generate and what a system can reliably act on.

## Problem

In high-stakes environments, it's not enough for AI to be helpful — it needs to be consistent and controllable.

Common failure modes:

- outputs vary for the same input
- constraints are applied inconsistently
- there's no clear record of how a result was produced
- it's difficult to compare behavior across runs

These aren't model problems alone. They're system design problems.

## Approach

MedScribe explores how to address this by introducing structure around the model.

The system simulates a clinical-style workflow to make decision quality and failure modes easier to evaluate.

Instead of relying on a single response, the input moves through a defined pipeline:

- intake and parsing
- triage and diagnosis
- structured mapping
- scoring and evaluation
- final outcome enforcement

The model is used within the pipeline, not as the final authority.

## What This Enables

Adding structure changes how the system behaves:

- outputs are consistent across repeated runs
- invalid results are filtered before they surface
- each run produces a complete, inspectable record
- system behavior can be compared across cases and over time

This makes it possible to evaluate the system itself, not just individual outputs.

## Scope

This project is not intended to be a clinical product.

The clinical setting is used to represent a high-stakes environment where incorrect outputs are easy to recognize.

The focus is on system design:
how to control, inspect, and evaluate AI behavior in a structured way.

The sections below describe how the system is implemented.

## Summary

MedScribe is a stateful, API-driven AI system that executes, persists, and analyzes structured runs with full lifecycle visibility. It executes requests asynchronously, records lifecycle state and execution artifacts, and exposes stored runs for inspection, comparison, and retrieval. The repository also includes an offline evaluation pipeline that produces scored run artifacts and a read-only aggregation utility for persisted evaluation runs.

Each run is treated as a persistent artifact, enabling inspection, comparison, and retrieval without re-execution.

## What This System Does

Pipeline:

Input → Intake Parser → Triage Engine → Diagnosis Engine → ICD Mapping → Critic → Governance Policy → Persisted Run

Implemented outputs:

- structured intake data
- triage decision
- diagnosis list
- ICD mappings
- critic scores and recommendation
- governance-enforced final status
- persisted run artifact

## Example Run

Below is a simplified example of a completed run artifact:

```json
{
  "run_id": "example-run",
  "status": "completed",
  "input": "Patient reports fever and sore throat.",
  "diagnosis": {
    "diagnoses": ["Pharyngitis"],
    "triage": {
      "level": "home_care",
      "rationale": "Symptoms fit a simple upper-respiratory pattern."
    }
  },
  "icd_mapping": {
    "mappings": [
      {
        "label": "Pharyngitis",
        "icd_code": "J02.9",
        "icd_label": "Acute pharyngitis, unspecified",
        "status": "OK"
      }
    ]
  },
  "scores": {
    "diagnosis_consistency_score": 1.0,
    "symptom_alignment_score": 1.0,
    "icd_specificity_score": 1.0,
    "recommended_status": "pass",
    "confidence": 1.0
  },
  "decision": "PASS",
  "timing": {
    "total_ms": 1280
  }
}
```

Actual run artifacts include additional fields such as execution traces, fallback diagnostics, and error metadata.

## Core System Properties

- Stateful execution with lifecycle states: `pending`, `running`, `completed`, `degraded`, `failed`
- Deterministic enforcement in the governance policy layer
- Persistent append-only run storage in `data/runs.jsonl`
- Retrieval of stored runs without recomputation through `GET /run/{run_id}`
- Run comparison through `GET /compare`
- Search over persisted runs through `POST /search`

## Evaluation & Analysis

- Offline batch execution from `evaluation/dataset.json` through `evaluation/eval_runner.py`
- Scoring of batch results through `evaluation/score_runner.py`
- Persisted evaluation run artifacts in `runs/{run_id}/scored_results.json`
- Read-only aggregation for persisted evaluation runs through `service/run_aggregator.py`
- CLI inspection of aggregated evaluation summaries through `scripts/test_run_aggregator.py`

## Observability

- Execution trace recorded per service run
- Stage-level latency tracking for parse, diagnosis, mapping, scoring, and total runtime
- Node-level fallback diagnostics for hybrid execution mode
- Stored failure metadata including `failed_stage` and `error`

## API

### `POST /evaluate`

Request:

```json
{
  "input_text": "I have had fever, cough, and sore throat for two days."
}
```

Response:

```json
{
  "run_id": "uuid",
  "status": "pending"
}
```

Behavior:

- creates a pending run record
- starts asynchronous execution

### `GET /run/{run_id}`

Returns the stored run artifact for the requested run ID.

Example fields in the response:

```json
{
  "run_id": "uuid",
  "timestamp": "2026-03-27T00:00:00Z",
  "input": "I have fever and cough.",
  "status": "completed",
  "parsed_input": {},
  "diagnosis": {
    "diagnoses": [],
    "triage": {}
  },
  "icd_mapping": {
    "mappings": []
  },
  "scores": {},
  "decision": "PASS",
  "summary": {},
  "timing": {},
  "trace": [],
  "node_diagnostics": [],
  "fallback_nodes": [],
  "fallback_reasons": {},
  "metadata": {},
  "retry_count": 0,
  "failed_stage": null,
  "fallback_used": false,
  "degraded_mode": false,
  "error": null
}
```

Run lifecycle states:

- `pending`
- `running`
- `completed`
- `degraded`
- `failed`

### `GET /run/{run_id}/status`

Response:

```json
{
  "run_id": "uuid",
  "status": "completed"
}
```

### `GET /runs`

Returns a list of stored runs with summary fields:

```json
[
  {
    "run_id": "uuid",
    "timestamp": "2026-03-27T00:00:00Z",
    "status": "completed"
  }
]
```

### `GET /compare`

Query parameters:

- `run_id_1`
- `run_id_2`

Response:

```json
{
  "run_id_1": "run-a",
  "run_id_2": "run-b",
  "decision_diff": true,
  "score_diff": {
    "confidence": {
      "run_1": 0.85,
      "run_2": 0.62
    }
  }
}
```

### `POST /search`

Request:

```json
{
  "query": "fever cough",
  "top_k": 5
}
```

Response:

```json
{
  "results": [
    {
      "run_id": "uuid",
      "score": 0.91
    }
  ]
}
```

### `POST /tool`

Request:

```json
{
  "tool_name": "parse_input",
  "payload": {
    "raw_input": "I have a headache."
  }
}
```

Response:

```json
{
  "result": {}
}
```

Supported tool names:

- `parse_input`
- `generate_diagnosis`
- `map_icd`
- `score_case`

## Architecture

Primary service boundary:

- FastAPI entry point in `service/main.py`
- Route layer in `service/api.py`
- Execution orchestration in `service/run_manager.py`
- Append-only storage in `service/storage.py`
- Retrieval search in `service/retrieval.py`
- Node dispatch utilities in `service/tools.py`

Pipeline implementation:

- state initialization in `graph/state.py`
- graph definition in `graph/graph_builder.py`
- intake parsing in `graph/nodes/intake_parser.py`
- triage assignment in `graph/nodes/triage_engine.py`
- diagnosis generation in `graph/nodes/diagnosis_engine.py`
- ICD mapping in `graph/nodes/icd_mapper.py`
- critic scoring in `graph/nodes/critic.py`
- governance enforcement in `graph/nodes/governance_policy.py`

Evaluation boundary:

- batch execution in `evaluation/eval_runner.py`
- scored result generation and run artifact persistence in `evaluation/score_runner.py`
- evaluation run aggregation in `service/run_aggregator.py`

Artifact models:

- service runtime artifacts: `data/runs.jsonl`
- evaluation run artifacts: `runs/{run_id}/scored_results.json`

## Tech Stack

- Python
- FastAPI
- Pydantic
- LangGraph
- LangChain OpenAI
- FAISS
- NumPy
- python-dotenv
- JSON / JSONL file storage

## Running the System

```bash
pip install -r requirements.txt
uvicorn service.main:app --reload
```

Optional local verification:

```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/openapi.json
curl -X POST http://127.0.0.1:8000/evaluate \
  -H "Content-Type: application/json" \
  -d '{"input_text":"I have had fever, cough, and sore throat for two days."}'
```

Offline evaluation flow:

```bash
python evaluation/eval_runner.py
python evaluation/score_runner.py
python scripts/test_run_aggregator.py --run_id <RUN_ID>
```

## Design Principles

- stateful execution with explicit lifecycle tracking
- append-only storage for persisted service runs
- inspectable stored artifacts
- explicit boundaries between service runtime and offline evaluation
- deterministic policy enforcement after critic scoring
