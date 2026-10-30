"""vN.evaluation.json as s1flow wrote it before @3 (schema/policy-evaluation-2.json is generated from these types).
Read only: eval/policy.py upgrades it to @3; nothing writes it."""
from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, ConfigDict, Field
from .candidate import Candidate
from .evaluation import Evaluation

TestVerdict = Literal['kept', 'below', 'inconclusive']


class Evidence(BaseModel):
    model_config = ConfigDict(extra='forbid')
    data_sha256: str
    execution_digest: str | None
    input_adapter_digest: str = ''
    evaluation_contract_digest: str | None = None  # unknown for historical evidence; never inferred
    git_sha: str | None = None
    evaluation: Evaluation
    test: TestVerdict | None
    test_uses: int = Field(ge=0)  # dropped in @3: counted only where it ran, and lost in CI
    compared: list[str]


class Selection(BaseModel):
    model_config = ConfigDict(extra='forbid')
    by: str
    reason: str
    recommended: str  # dropped in @3: s1flow no longer recommends
    tied: list[str]


class EvaluationRecord(BaseModel):
    """vN.evaluation.json; never embeds or redefines the runtime specification."""
    model_config = ConfigDict(extra='forbid', populate_by_name=True, serialize_by_alias=True)
    schema_: Literal['s1flow/policy-evaluation@2'] = Field(default='s1flow/policy-evaluation@2', alias='schema')
    policy_digest: str
    candidate: Candidate
    selection: Selection
    evidence: Evidence
    answered_by: str
