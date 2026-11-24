"""OpenAI Decisions API (`POST /v1/decisions`, public beta 2026-10-06): gpt-6-luna.

The wire format is OpenAI's own: questions are a list with a `name`; yes/no is a
`predicate`, a score has `levels` indexed from 0, and answers come back as a list.
Billing is input tokens only. The AI Gateway (gateway.py) speaks the same format on its
own `/v1/decisions`, plus a `box` question OpenAI does not take.

Images go as `input_image` parts (base64 data URL) in a user message, so a state
with images is sent as one message whose content alternates text and images.
"""

import json
from typing import Any

from ...core.errors import Unsupported
from ..answers import Answer, BooleanAnswer, BoxAnswer, BoxEdges, ChoiceAnswer, Response, ScoreAnswer, Usage
from ..media import openai_content, images_only
from ..models import Capabilities, ModelBuild, ModelSpec, check_supported
from ..questions import Questions
from ..state import State, has_image
from .build import NoOptions, options
from .contract import outside_contract, refusal
from .http import Request, send
from .needs import Needs, declares, origin

BASE_URL = "https://api.openai.com/v1"


def decisions_questions(questions: Questions, *, box: bool = False) -> list[dict[str, Any]]:
    """`box`: the wire takes a `box` question (the AI Gateway's does, OpenAI's does not)."""
    out: list[dict[str, Any]] = []
    for name, q in questions.items():
        if q.type == "boolean":
            text = q.instructions
            if q.criteria:  # no field for per-answer criteria, so they go into the instructions
                text += "\n" + "\n".join(f"- {k}: {v}" for k, v in q.criteria.items())
            out.append({"type": "predicate", "name": name, "instructions": text})
        elif q.type == "choice":
            choices = [{"value": k, "description": v} if v else {"value": k} for k, v in q.criteria.items()]
            out.append({"type": "choice", "name": name, "instructions": q.instructions, "choices": choices})
        elif q.type == "score":
            levels = [{"label": str(i), "description": d} for i, d in enumerate(q.criteria)]
            out.append({"type": "score", "name": name, "instructions": q.instructions, "levels": levels})
        elif q.type == "box" and box:
            out.append({"type": "box", "name": name, "instructions": q.instructions})
        else:
            raise Unsupported(f"the Decisions API has no {q.type} questions ({name})")
    return out


def decisions_input(state: State) -> Any:
    """Text as it is; a state with images as one user message whose content alternates text and images."""
    if has_image(state):
        return [{"role": "user", "content": openai_content(state)}]
    return state if isinstance(state, str) else json.dumps(state, ensure_ascii=False, indent=1)


def parse_decisions(raw: list[dict[str, Any]]) -> dict[str, Answer]:
    out: dict[str, Answer] = {}
    for a in raw:
        with outside_contract(a.get("name", "?")):
            out[a["name"]] = refusal(a) or _answer(a)
    return out


def _answer(a: dict[str, Any]) -> Answer:
    if a["type"] == "predicate":
        return BooleanAnswer(probability=a["probability"])
    if a["type"] == "choice":
        probs = {p["value"]: p["probability"] for p in a.get("probabilities") or []}
        return ChoiceAnswer(choice=a["choice"], probabilities=probs or None, confidence=a.get("confidence"))
    if a["type"] == "box":
        b = a["box"]
        return BoxAnswer(box=BoxEdges.clipped(b["top"], b["bottom"], b["left"], b["right"]), confidence=a.get("confidence"))
    probs = {str(p["value"]): p["probability"] for p in a.get("probabilities") or []}
    return ScoreAnswer(score=a["score"], probabilities=probs or None, confidence=a.get("confidence"))


class DecisionsModel:
    def __init__(self, model_id: str, *, concurrency: int = 8, capabilities: Capabilities | None = None):
        self.model_id = model_id
        self.id = f"openai-decisions:{model_id}"
        self.concurrency = concurrency
        self.capabilities = capabilities or Capabilities()

    def request(self, state: State, questions: Questions, *, options: dict[str, Any] | None = None) -> Request:
        images_only(state, self.id)
        body: dict[str, Any] = {"model": self.model_id, "input": decisions_input(state), "questions": decisions_questions(questions)}
        if options:
            body.update(options)
        return Request(f"{BASE_URL}/decisions", body, keys={"Authorization": ("Bearer ", "OPENAI_API_KEY")})

    async def decide(self, state: State, questions: Questions, *, options: dict[str, Any] | None = None) -> Response:
        check_supported(self, state, questions)
        posted = await send(self.request(state, questions, options=options))
        data = posted.data
        usage = data.get("usage") or {}
        return Response(
            answers=parse_decisions(data["answers"]),
            answered_by=data.get("model", self.model_id),
            usage=Usage(input_tokens=usage.get("input_tokens") or 0, raw=usage or None),  # priced from s1flow.toml's list, if any
            latency_ms=posted.latency_ms,
            retries=posted.retries,
        )


def needs(spec: ModelSpec) -> Needs:
    return Needs(keys=("OPENAI_API_KEY",), hosts=(origin(BASE_URL),))


@declares(needs)
def build(b: ModelBuild) -> DecisionsModel:
    options(NoOptions, b)
    return DecisionsModel(b.spec.id, concurrency=b.spec.concurrency or 8, capabilities=b.spec.capabilities)
