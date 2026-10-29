"""Call a decision model: any model, all four question types, several questions in one call. No policy and
no evaluation stack (pydantic and httpx; Pillow only for a state with images, LiteLLM only for an `llm` model).

    from s1flow import Client
    from s1flow.questions import Boolean, Choice, Score, Box

    d = Client(connections="connections.toml").responses.create(model="jev", state={...}, questions={"bug": Boolean(instructions="...")})
    d.answers["bug"].probability

A policy (s1flow.policies) and the evaluation (s1flow.eval) call models through this layer.
"""

from ._client import AsyncClient, Client, ConnectionInfo
from .answers import Answer, BooleanAnswer, BoxAnswer, BoxEdges, ChoiceAnswer, Response, Given, Refusal, ScoreAnswer, Usage
from .models import Capabilities, DecisionModel, ModelBuild, ModelSpec, Price, ProviderFactory
from .providers.needs import Needs, declares
from .questions import Boolean, Box, Choice, Question, Questions, QuestionType, Score
from .state import Image, ImageRef, State

__all__ = [
    "Answer", "AsyncClient", "Boolean", "BooleanAnswer", "Box", "BoxAnswer", "BoxEdges", "Capabilities", "Choice", "ChoiceAnswer",
    "Client", "Response", "DecisionModel", "Given", "Image", "ImageRef", "ModelBuild", "ConnectionInfo", "ModelSpec", "Needs", "Price", "ProviderFactory",
    "Question", "QuestionType", "Questions", "Refusal", "Score", "ScoreAnswer", "State", "Usage", "declares",
]
