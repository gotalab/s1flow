"""Rules for reading validated model answers; independent of evaluation."""
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

RuleField = Literal['min_probability', 'threshold']


class DecisionRule(BaseModel):
    """Binary threshold and optional lower bound on the chosen value's probability."""
    model_config = ConfigDict(extra='forbid', frozen=True)
    threshold: float | None = Field(default=None, ge=0, le=1, allow_inf_nan=False)
    min_probability: float | None = Field(default=None, ge=0, le=1, allow_inf_nan=False)
