# Med Scribe — Governed AI Decision System

A production-adjacent AI system that separates **probabilistic reasoning** from **deterministic decision enforcement**, with persistent evaluation, observability, and comparative analysis.

---

## Overview

This system implements a structured, multi-stage pipeline for diagnostic reasoning and evaluation, then enforces outcomes through a deterministic policy layer.

Every run is:

- persisted (append-only)
- inspectable (full artifact retrieval)
- observable (latency + execution trace)
- comparable (run-to-run diffing)

---

## Core Architecture

Input  
→ Intake Parser  
→ Diagnosis Engine (LLM)  
→ ICD Mapping  
→ Critic (Scoring)  
→ Policy (Deterministic Decision)  
→ Persisted Run Artifact  
→ API Layer (Evaluate / Replay / Compare)

---

## Key Capabilities

### Deterministic Decision Layer
- PASS / REVISE / FAIL enforcement  
- removes ambiguity from LLM outputs  

### Persistent Run Storage
- append-only JSONL (`data/runs.jsonl`)  
- full historical trace of decisions  

### Artifact Replay (Retrieval-Based)
- GET /run/{run_id}  
- no recomputation, no model invocation  

### Observability
- stage-level latency tracking  
- execution trace per run  

### Run Comparison
- GET /compare  
- decision + score-level diffs  

---

## API

### POST /evaluate
Input:
{
  "input_text": "..."
}

Returns:
{
  "run_id": "...",
  "decision": "PASS",
  "scores": {...},
  "timing": {...},
  "trace": [...]
}

---

### GET /run/{run_id}
Returns full stored artifact.

---

### GET /runs
Lists previous runs.

---

### GET /compare
Compare two runs by ID.

---

## Tech Stack

- Python  
- FastAPI (service layer)  
- LangChain (LLM orchestration within structured pipeline)  
- JSONL (append-only storage)

---

## Running the System

pip install -r requirements.txt  
uvicorn service.main:app --reload  

Docs: http://localhost:8000/docs

---

## Design Principles

- separation of reasoning and decision enforcement  
- append-only state for auditability  
- minimal, explicit system boundaries  
- observability by default  

---

## Positioning

This project demonstrates:

- applied AI system design  
- evaluation and governance patterns  
- operational thinking (state, latency, traceability)  
- building production-adjacent systems without overengineering  
