"""One line of runs/<task>/<variant>/<model>.jsonl: what happened to one case.

Every case ends in exactly one outcome:

| outcome       | raised as                     | in the report                                    |
|---------------|-------------------------------|--------------------------------------------------|
| `answered`    | (a `Response`)                | scored                                           |
| `unsupported` | `Unsupported`, before a call  | refused / unsupported; left out of the denominator |
| `rejected`    | `Rejected`, after a call, or the question's `Refusal` | refused / unsupported; left out of the denominator |
| `failed`      | `ProviderError`, or any other | failed                                           |
| `data_error`  | `DataError`                   | data errors: the task is wrong, not the model    |
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from ..client.answers import Answer, Given, Refusal, Response, Usage
from ..core.errors import DataError, ProviderError, Rejected, Unsupported

Outcome = Literal["answered", "unsupported", "rejected", "failed", "data_error"]
REFUSED: frozenset[Outcome] = frozenset({"unsupported", "rejected"})


class PredictionRecord(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True, serialize_by_alias=True)

    schema_: Literal["s1flow/run@2"] = Field(default="s1flow/run@2", alias="schema")
    request_digest: str | None = None  # absent on a failed call
    id: str
    label: Any = None
    model: str  # the name in s1flow.toml
    variant: str = "base"
    prompt: str  # prompt_hash of the questions asked
    distribution: Literal["native", "sampled", "none"] | None = None
    at: str = ""  # when the call ended (core.clock)
    outcome: Outcome
    # answered
    answer: Answer | None = None
    # what the Response said, by its field names
    answered_by: str | None = None  # the model that actually answered
    # the tokens and API cost (billed / list, client/cost.py; None: not known), and the usage as the model returned
    # it (`raw`). A list cost is worked out again from the tokens when a report reads it (metrics.load), so this one
    # is what the price gave that day.
    usage: Usage | None = None
    latency_ms: float | None = None  # the answering attempt alone (Response.latency_ms)
    retries: int | None = None  # None: not recorded (lines before 2026-10-16)
    concurrency: int | None = None  # calls in flight to the model when this one was made
    cached: bool | None = None
    # anything else
    reason: str | None = None
    status: int | None = None  # HTTP status, when there was one

    @field_validator("id", mode="before")
    @classmethod
    def _id_str(cls, v: Any) -> str:
        return str(v)

    @model_validator(mode="after")
    def _consistent(self) -> PredictionRecord:
        if (self.answered or self.outcome in REFUSED) and not self.request_digest:
            raise ValueError("answered/refused records need request_digest")
        if (self.outcome == "answered") != (self.answer is not None):
            raise ValueError(f"outcome {self.outcome} with answer={self.answer is not None}")
        if isinstance(self.answer, Refusal):
            raise ValueError("a refusal is recorded as rejected, not answered")
        if self.outcome == "answered" and self.answered_by is None:
            raise ValueError("an answered record needs answered_by")
        return self

    @property
    def answered(self) -> bool:
        return self.outcome == "answered"

    @property
    def given(self) -> Given | None:
        """The answer, typed as one that is not a refusal (a record never holds one)."""
        return None if self.answer is None or isinstance(self.answer, Refusal) else self.answer

    def line(self) -> str:
        return json.dumps(self.model_dump(mode="json", exclude_none=True), ensure_ascii=False)


def from_response(base: dict[str, Any], d: Response, question_id: str, cached: bool, concurrency: int | None) -> PredictionRecord:
    """The call's answer to the task's question; a `Refusal` is the model's limit (`rejected`), as a refused call is."""
    answer = d.answers[question_id]
    if isinstance(answer, Refusal):
        return from_exception(base, Rejected(f"the model refused to answer {question_id}" + (f": {answer.reason}" if answer.reason else "")))
    return PredictionRecord.model_validate(base | {
        "outcome": "answered",
        "answer": answer,
        "answered_by": d.answered_by,
        "usage": d.usage,
        "latency_ms": round(d.latency_ms, 1),
        "retries": d.retries,
        "concurrency": concurrency,
        "cached": cached,
    })


def from_exception(base: dict[str, Any], e: Exception) -> PredictionRecord:
    """The exception a call ended with -> its outcome (core/errors.py names the four)."""
    outcome: Outcome
    status: int | None = None
    if isinstance(e, DataError):
        outcome = "data_error"
    elif isinstance(e, Rejected):
        outcome, status = "rejected", e.status
    elif isinstance(e, Unsupported):
        outcome = "unsupported"
    elif isinstance(e, ProviderError):
        outcome, status = "failed", e.status
    else:
        outcome = "failed"
    reason = str(e) if isinstance(e, (Unsupported, ProviderError, DataError)) else f"{type(e).__name__}: {e}"
    return PredictionRecord.model_validate(base | {"outcome": outcome, "reason": reason[:300], "status": status})


def read(path: Path) -> list[PredictionRecord]:
    if not path.exists():
        return []
    return [PredictionRecord.model_validate_json(line) for line in path.read_text().splitlines() if line.strip()]
