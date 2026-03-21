# MED-SCRIBE — Governed Diagnostic Evaluation System

## Thesis

AI reliability is not a model problem — it is a system design problem.

This project demonstrates how a probabilistic reasoning system can be transformed into a measurable, governable, and auditable decision system through structured evaluation and deterministic policy enforcement.

---

## Why This Exists

Most AI systems appear to work because their outputs look plausible.

They fail when:

• outputs are ambiguous  
• reasoning is inconsistent  
• confidence is unjustified  

This project builds a system that:

• measures those failures  
• enforces constraints  
• routes uncertainty explicitly  

---

## What This System Does

Given a clinical-style input, the system:

1. Generates structured diagnostic reasoning  
2. Produces ICD mappings  
3. Scores output quality across multiple dimensions  
4. Applies deterministic governance  
5. Produces a final decision:

• PASS → high-confidence, consistent output  
• REVISE → structured but ambiguous / incomplete  
• FAIL → invalid or contradictory  

---

## Architecture Overview

Pipeline:

Input → Parser → Diagnosis Engine → ICD Mapper → Critic → Policy → Final Decision

Key components:

• LLM reasoning layer → generates candidate outputs  
• Critic layer → scores output across multiple dimensions  
• Policy layer → deterministically maps scores → decision  
• Evaluation layer → measures system behavior across scenarios  

---

## Governance Model

The system enforces:

PASS     → high confidence + full consistency  
REVISE   → ambiguity or partial completeness  
FAIL     → contradiction, invalid structure, or low evidence  

Governance ensures:

• no silent failures  
• no unjustified confidence  
• explicit escalation of uncertainty  

---

## Evaluation Design

Dataset:

• 15 cases  
• balanced across:
  - valid (PASS)
  - ambiguous (REVISE)
  - invalid (FAIL)

Evaluation measures:

• behavior_accuracy  
• pass / revise / fail distribution  
• governance impact  
• score distributions  

---

## Results (Final System)

| Metric | Value |
|---|---:|
| PASS rate | 0.33 |
| REVISE rate | 0.47 |
| FAIL rate | 0.13 |
| Behavior Accuracy | 0.80 |
| Average Score | ~5.9 |
| Incorrect PASS cases | 0 |

---

## System Evolution

The system was developed through four stages:

1. Baseline  
   • pipeline runs, but outputs are unvalidated

2. Governance  
   • system enforces correctness  
   • initially over-constrained (100% FAIL)

3. Calibration + Precision  
   • PASS emerges  
   • scoring aligns with real output quality

4. Robustness Layer  
   • ambiguity handled explicitly  
   • FAIL reduced  
   • accuracy increased

---

## Example Decision Behavior

• Clean, consistent case → PASS  
• Ambiguous symptom pattern → REVISE  
• Contradictory / invalid input → FAIL  

---

## What This Proves

This system demonstrates:

• AI outputs must be measured, not assumed correct  
• governance can enforce reliability  
• structured evaluation enables systematic improvement  
• ambiguity can be handled without collapsing into failure  

---

## Repo Structure

evaluation/
  dataset.json
  eval_runner.py
  score_runner.py
  aggregate_runner.py
  raw_results.json
  scored_results.json
  eval_summary.json

pipeline/
  intake_parser.py
  diagnosis_engine.py
  icd_mapper.py
  critic.py

telemetry/
  executor_heartbeat.jsonl

---

## How to Run

python evaluation/eval_runner.py
python evaluation/score_runner.py
python evaluation/aggregate_runner.py

Outputs:

• evaluation/raw_results.json  
• evaluation/scored_results.json  
• evaluation/eval_summary.json  

---

## Limitations

• Not a clinical system  
• Does not claim medical accuracy  
• Small dataset (designed for behavior testing, not benchmarking)  

---

## Key Insight

The goal is not to make AI smarter.

The goal is to make AI:

• observable  
• controllable  
• accountable  

---

## Author Note

This project focuses on system design, not model training.

It demonstrates how to turn a generative model into a governed decision system with measurable behavior.

---

## What Makes This Different

This is not a prompt engineering demo or a model showcase.

This system introduces a governed architecture around a probabilistic model:

• outputs are scored across multiple dimensions  
• decisions are enforced deterministically  
• ambiguity is explicitly handled (REVISE instead of silent failure)  
• invalid outputs are rejected  

The focus is on:

• measurement over intuition  
• system behavior over single outputs  
• reliability through design, not model tuning  

This demonstrates how AI systems can be made observable, controllable, and accountable.
