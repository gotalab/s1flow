"""The questions a decision model answers: yes / no, one of N, a level, a box.

Vocabulary follows the decision-model APIs (TypeSafe, AI Gateway, OpenRouter, Workers AI): a map of
typed `questions`, keyed by name. Every provider translates these into its own wire format (yes / no
is `noul` on TypeSafe's, `predicate` on OpenAI's).
"""

from __future__ import annotations

from typing import Annotated, Literal, Union

from pydantic import BaseModel, ConfigDict, Field

QuestionType = Literal["boolean", "choice", "score", "box"]
STRICT = ConfigDict(extra="forbid")  # a misspelt key in a question (and so in a policy's digest) is an error, not dropped
TEXT_TYPES: frozenset[QuestionType] = frozenset({"boolean", "choice", "score"})


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


Question = Annotated[Union[Boolean, Choice, Score, Box], Field(discriminator="type")]
Questions = dict[str, Question]


def has_box(questions: Questions) -> bool:
    return any(q.type == "box" for q in questions.values())

