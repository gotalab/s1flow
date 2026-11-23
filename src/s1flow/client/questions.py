"""The questions a decision model answers: yes / no, one of N, a level, a box, a value read from the state,
an estimate in a range.

Vocabulary follows the decision-model APIs (TypeSafe, OpenRouter, Workers AI): a map of
typed `questions`, keyed by name. Every provider translates these into its own wire format (yes / no
is `noul` on TypeSafe's, `predicate` on OpenAI's; a value or an estimate is a `field` on OpenRouter's
Extractions route).
"""

from typing import Annotated, Literal, Union

from pydantic import BaseModel, ConfigDict, Field, model_validator

QuestionType = Literal["boolean", "choice", "score", "box", "text", "number", "date", "estimate"]
STRICT = ConfigDict(extra="forbid")  # a misspelt key in a question (and so in a policy's digest) is an error, not dropped
TEXT_TYPES: frozenset[QuestionType] = frozenset({"boolean", "choice", "score"})
# Read from the state or estimated, not decided: OpenRouter serves these on its Extractions route (extractions.py).
FIELD_TYPES: frozenset[QuestionType] = frozenset({"text", "number", "date", "estimate"})


class Boolean(BaseModel):
    model_config = STRICT
    type: Literal["boolean"] = "boolean"
    instructions: str
    # Keys "true" / "false", as on the wire.
    criteria: dict[str, str] | None = None


class Choice(BaseModel):
    model_config = STRICT
    type: Literal["choice"] = "choice"
    instructions: str
    criteria: dict[str, str | None]


class Score(BaseModel):
    """Levels 0..L-1, described in order by `criteria`."""

    model_config = STRICT
    type: Literal["score"] = "score"
    instructions: str
    criteria: list[str]


class Box(BaseModel):
    """One bounding box of the target described in `instructions` (jev 1.14, 2026-10-15).

    There is no "not found" answer: ask a Boolean alongside when the target may be absent.
    """

    model_config = STRICT
    type: Literal["box"] = "box"
    instructions: str


class Text(BaseModel):
    """A passage read from the state as it is written (an invoice number, a name). The answer's value is None
    when the state holds nothing for it."""

    model_config = STRICT
    type: Literal["text"] = "text"
    instructions: str


class Number(BaseModel):
    """A number read from the state, None when the state holds none. `unit` names what it is counted in (USD, kg)."""

    model_config = STRICT
    type: Literal["number"] = "number"
    instructions: str
    unit: str | None = None


class Date(BaseModel):
    """A calendar date read from the state, None when the state holds none."""

    model_config = STRICT
    type: Literal["date"] = "date"
    instructions: str


class RangeEstimate(BaseModel):
    """A number between `min` and `max` the state does not state: the model's estimate, with the p10 - p90 interval
    of its distribution. `step` is the spacing of the values it may take (1 for a count)."""

    model_config = STRICT
    type: Literal["estimate"] = "estimate"
    instructions: str
    min: float
    max: float
    step: float | None = Field(default=None, gt=0)
    unit: str | None = None

    @model_validator(mode="after")
    def _ordered(self) -> "RangeEstimate":
        if not self.min < self.max:
            raise ValueError(f"an estimate's min is under its max, got {self.min:g} and {self.max:g}")
        return self


def no_fields(questions: "Questions", who: str) -> None:
    """Refuse the questions `who` has no way to ask, before any call: it would send a text question in a shape
    the model reads as something else."""
    from ..core.errors import Unsupported

    if field := [f"{q.type} ({k})" for k, q in questions.items() if q.type in FIELD_TYPES]:
        raise Unsupported(f"{who} has no {', '.join(sorted(FIELD_TYPES))} questions: {', '.join(field)}")


Question = Annotated[Union[Boolean, Choice, Score, Box, Text, Number, Date, RangeEstimate], Field(discriminator="type")]
Questions = dict[str, Question]


def has_box(questions: Questions) -> bool:
    return any(q.type == "box" for q in questions.values())

