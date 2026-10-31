"""Versioned decision and label events, shared with evaluation readers."""
from __future__ import annotations

import json
from typing import Annotated, Any, Literal, Union
from pydantic import BaseModel, ConfigDict, Field
from ..client.answers import Response
from .kinds import Label, Reading


class Decision(Reading):
    """One successful call. case_id may repeat; decision_id identifies this judgment."""
    model_config = ConfigDict(extra='forbid')
    decision_id: str = Field(min_length=1)
    policy: str
    policy_digest: str
    answered_by: str
    latency_ms: float
    execution_digest: str
    response: Response | None = None


LOG: Literal['s1flow/log@2'] = 's1flow/log@2'


class AnsweredLog(BaseModel):
    model_config = ConfigDict(extra='forbid', populate_by_name=True, serialize_by_alias=True)
    schema_: Literal['s1flow/log@2'] = Field(default=LOG, alias='schema')
    type: Literal['answered'] = 'answered'
    at: str
    case_id: str | None = None
    state_sha256: str
    state: Any = None
    decision: Decision


class FailedLog(BaseModel):
    model_config = ConfigDict(extra='forbid', populate_by_name=True, serialize_by_alias=True)
    schema_: Literal['s1flow/log@2'] = Field(default=LOG, alias='schema')
    type: Literal['failed'] = 'failed'
    at: str
    case_id: str | None = None
    state_sha256: str
    policy: str
    policy_digest: str
    error: str


class FeedbackLog(BaseModel):
    model_config = ConfigDict(extra='forbid', populate_by_name=True, serialize_by_alias=True)
    schema_: Literal['s1flow/log@2'] = Field(default=LOG, alias='schema')
    type: Literal['feedback'] = 'feedback'
    at: str
    decision_id: str = Field(min_length=1)
    policy: str
    policy_digest: str
    label: Label


Log = Annotated[Union[AnsweredLog, FailedLog, FeedbackLog], Field(discriminator='type')]
DECIDE, FEEDBACK = 's1flow.decide', 's1flow.feedback'


def span(rec: AnsweredLog | FailedLog | FeedbackLog, provider: str | None = None, requested: str | None = None) -> tuple[str, dict[str, Any]]:
    if isinstance(rec, FeedbackLog):
        return FEEDBACK, {'s1flow.policy': rec.policy, 's1flow.policy_digest': rec.policy_digest,
                          's1flow.decision_id': rec.decision_id, 's1flow.label': json.dumps(rec.label)}
    if isinstance(rec, FailedLog):
        attrs: dict[str, Any] = {'s1flow.policy': rec.policy, 's1flow.policy_digest': rec.policy_digest, 's1flow.case_id': rec.case_id,
                 's1flow.state_sha256': rec.state_sha256, 'error.type': rec.error.partition(':')[0]}
    else:
        d = rec.decision
        attrs = {
            'gen_ai.operation.name': 'decide', 'gen_ai.provider.name': provider, 'gen_ai.request.model': requested,
            'gen_ai.response.model': d.answered_by, 's1flow.policy': d.policy, 's1flow.policy_digest': d.policy_digest,
            's1flow.execution_digest': d.execution_digest, 's1flow.decision_id': d.decision_id, 's1flow.case_id': rec.case_id,
            's1flow.answer': json.dumps(d.model_dump(mode='json')['value']), 's1flow.probability': d.probability,
            's1flow.p_positive': d.p_positive, 's1flow.below_min_probability': d.below_min_probability,
            's1flow.latency_ms': d.latency_ms, 's1flow.state_sha256': rec.state_sha256,
        }
    return DECIDE, {k: v for k, v in attrs.items() if v is not None}


def from_span(name: str, at: str, attrs: dict[str, Any]) -> AnsweredLog | FailedLog | FeedbackLog | None:
    """The record a span() span was written from; None for any other span."""
    a = attrs
    if 's1flow.policy_digest' not in a:
        return None
    if name == FEEDBACK:
        return FeedbackLog(at=at, decision_id=a['s1flow.decision_id'], policy=a['s1flow.policy'],
                           policy_digest=a['s1flow.policy_digest'], label=json.loads(a['s1flow.label']))
    if name != DECIDE:
        return None
    if 'error.type' in a:
        return FailedLog(at=at, case_id=a.get('s1flow.case_id'), state_sha256=a['s1flow.state_sha256'],
                         policy=a['s1flow.policy'], policy_digest=a['s1flow.policy_digest'], error=a['error.type'])
    return AnsweredLog(at=at, case_id=a.get('s1flow.case_id'), state_sha256=a['s1flow.state_sha256'], decision=Decision(
        value=json.loads(a['s1flow.answer']), probability=a.get('s1flow.probability'), p_positive=a.get('s1flow.p_positive'),
        below_min_probability=a.get('s1flow.below_min_probability'), decision_id=a['s1flow.decision_id'],
        policy=a['s1flow.policy'], policy_digest=a['s1flow.policy_digest'], execution_digest=a['s1flow.execution_digest'],
        answered_by=a['gen_ai.response.model'], latency_ms=a['s1flow.latency_ms'],
    ))
