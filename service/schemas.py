"""Pydantic request and response schemas for the service API."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class EvaluateRequest(BaseModel):
    input_text: str


class EvaluateResponse(BaseModel):
    run_id: str
    decision: str
    scores: dict[str, Any]
    summary: dict[str, Any] | None
    timing: dict[str, int]
    trace: list[str]
