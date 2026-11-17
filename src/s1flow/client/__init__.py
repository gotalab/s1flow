"""Call a decision model: any model, every question type, several questions in one call. No policy and
no evaluation stack (pydantic and httpx; Pillow only for a state with images, LiteLLM only for an `llm` model).

    from s1flow import Client
    from s1flow.questions import Boolean, Choice, Score, Box, Text, Number, Date, RangeEstimate

    d = Client(connections="connections.toml").responses.create(model="jev", state={...}, questions={"bug": Boolean(instructions="...")})
    d.answers["bug"].probability

A policy (s1flow.policies) and the evaluation (s1flow.eval) call models through this layer.
"""

from ._client import AsyncClient, Client, ConnectionInfo
from .answers import (
    Answer, BooleanAnswer, BoxAnswer, BoxEdges, BoxesAnswer, FoundBox, ChoiceAnswer, DateAnswer, EstimateAnswer, Given, MultiChoiceAnswer, NumberAnswer, Refusal, Response,
    ScoreAnswer, TextAnswer, Usage,
)
from .models import Capabilities, DecisionModel, ModelBuild, ModelSpec, Price, ProviderFactory
from .providers.needs import Needs, declares
from .questions import Boolean, Box, Boxes, Choice, Date, MultiChoice, RangeEstimate, Number, Question, Questions, QuestionType, Score, Text
from .state import Image, Media, MediaRef, State

__all__ = [
    "Answer", "AsyncClient", "Boolean", "BooleanAnswer", "Box", "BoxAnswer", "BoxEdges", "Capabilities", "Choice", "ChoiceAnswer",
    "Date", "DateAnswer", "RangeEstimate", "EstimateAnswer", "Number", "NumberAnswer", "Text", "TextAnswer",
    "Client", "Response", "DecisionModel", "Given", "MultiChoice", "MultiChoiceAnswer", "Boxes", "BoxesAnswer", "FoundBox", "Image", "Media", "MediaRef", "ModelBuild", "ConnectionInfo", "ModelSpec", "Needs", "Price", "ProviderFactory",
    "Question", "QuestionType", "Questions", "Refusal", "Score", "ScoreAnswer", "State", "Usage", "declares",
]
