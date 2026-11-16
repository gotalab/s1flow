"""Call a decision model: any model, every question type, several questions in one call. No policy and
no evaluation stack (pydantic and httpx; Pillow only for a state with images, LiteLLM only for an `llm` model).

    from s1flow import Client
    from s1flow.questions import Boolean, Choice, Score, Box, Text, Number, Date, Estimate

    d = Client(connections="connections.toml").responses.create(model="jev", state={...}, questions={"bug": Boolean(instructions="...")})
    d.answers["bug"].probability

A policy (s1flow.policies) and the evaluation (s1flow.eval) call models through this layer.
"""

from ._client import AsyncClient, Client, ConnectionInfo
from .answers import (
    Answer, BooleanAnswer, BoxAnswer, BoxEdges, ChoiceAnswer, DateAnswer, EstimateAnswer, Given, NumberAnswer, Refusal, Response,
    ScoreAnswer, TextAnswer, Usage,
)
from .models import Capabilities, DecisionModel, ModelBuild, ModelSpec, Price, ProviderFactory
from .providers.needs import Needs, declares
from .questions import Boolean, Box, Choice, Date, Estimate, Number, Question, Questions, QuestionType, Score, Text
from .state import Image, Media, MediaRef, State

__all__ = [
    "Answer", "AsyncClient", "Boolean", "BooleanAnswer", "Box", "BoxAnswer", "BoxEdges", "Capabilities", "Choice", "ChoiceAnswer",
    "Date", "DateAnswer", "Estimate", "EstimateAnswer", "Number", "NumberAnswer", "Text", "TextAnswer",
    "Client", "Response", "DecisionModel", "Given", "Image", "Media", "MediaRef", "ModelBuild", "ConnectionInfo", "ModelSpec", "Needs", "Price", "ProviderFactory",
    "Question", "QuestionType", "Questions", "Refusal", "Score", "ScoreAnswer", "State", "Usage", "declares",
]
