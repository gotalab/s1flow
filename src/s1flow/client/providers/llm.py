"""An LLM wrapped as a decision model (the baseline). Any LiteLLM model works.

AI Gateway refuses a language model as a primary decision model, so the LLM
answers through structured output here. One sample gives one answer and no
distribution; `samples=k` estimates the distribution from k answers (k times
the cost).

Images go after the prompt as `image_url` parts; `[image n]` in the STATE marks where
each one was.

Box questions are asked in the model's own units, then turned into fractions: Gemini answers
on a 0-1000 scale, Claude in pixels of the image it sees. Asked the other way, each lands at
IoU 0.01-0.16 instead of 0.92-1.0 (2026-10-16). Pixels are of the first image in the state.

LiteLLM is imported when a model is built, not with this module, so the declaration (`needs`) reads on the
base install.
"""

from __future__ import annotations

import asyncio
import json
import os
import statistics
import time
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from pydantic import Field

from . import pricing
from ...core.errors import ConfigError, ProviderError, Rejected
from ..answers import Answer, BooleanAnswer, BoxAnswer, BoxEdges, ChoiceAnswer, Response, ScoreAnswer, Usage
from ..boxes import iou
from ..images import data_url, placeholders
from ..models import Capabilities, ModelBuild, ModelSpec, Price, check_supported
from ..questions import TEXT_TYPES, Boolean, Choice, Questions, Score
from ..state import Image, State, has_image
from .build import Options, declared, options, spec_options
from .http import AUTH_STATUS, refused_without, retryable
from .needs import Needs, declares, litellm_needs
from .published import per_token, publishes


UNSET_KEY = "s1flow-key-not-set"


def require_litellm() -> None:
    """LiteLLM, or one line saying what to install: the base install is the runtime for decision models alone."""
    try:
        import litellm
    except ModuleNotFoundError as e:
        if e.name != "litellm":
            raise
        raise ConfigError("the llm provider needs LiteLLM: install s1flow[llm]") from None
    litellm.suppress_debug_info = True


SYSTEM = (
    "You are a precise classifier. Read the STATE and answer every QUESTION about it. "
    "Reply with a JSON object that has one field per question id, following the schema."
)
GATEWAY_PREFIX = "vercel_ai_gateway/"
EDGES = ("top", "bottom", "left", "right")

BoxUnits = Literal["k1000", "pixels"]
Size = tuple[int, int]


def box_instruction(units: BoxUnits, size: Size | None) -> str:
    if units == "pixels":
        dims = f"The image is {size[0]}x{size[1]} pixels. " if size else ""
        return f"    {dims}Answer the bounding box of that target in pixels: top, bottom, left, right, from the top-left corner."
    return "    Answer the bounding box of that target: top, bottom, left, right as integers on a 0-1000 scale of the image height and width (0 = top or left edge, 1000 = bottom or right edge)."


def first_size(state: State) -> Size | None:
    if isinstance(state, list):
        for item in state:
            if isinstance(item, Image):
                return item.width, item.height
    return None


def to_fractions(b: dict[str, float], units: BoxUnits, size: Size | None) -> BoxEdges:
    """The model's own units -> fractions, clipped into the image and put in order."""
    w, h = size if units == "pixels" and size else (1000, 1000)
    return BoxEdges.clipped(b["top"] / h, b["bottom"] / h, b["left"] / w, b["right"] / w)


def render_prompt(state: State, questions: Questions, box_units: BoxUnits = "k1000", size: Size | None = None) -> str:
    lines = ["STATE:", state if isinstance(state, str) else json.dumps(state, ensure_ascii=False, indent=1), "", "QUESTIONS:"]
    for qid, q in questions.items():
        lines.append(f"- {qid} ({q.type}): {q.instructions}")
        if isinstance(q, Choice):
            lines += [f"    - {k}: {v}" if v else f"    - {k}" for k, v in q.criteria.items()]
        elif isinstance(q, Boolean) and q.criteria:
            lines += [f"    - {k}: {v}" for k, v in q.criteria.items()]
        elif isinstance(q, Score):
            lines += [f"    - {i}: {v}" for i, v in enumerate(q.criteria)]
        elif q.type == "box":
            lines.append(box_instruction(box_units, size))
    return "\n".join(lines)


def user_content(state: State, questions: Questions, box_units: BoxUnits = "k1000") -> str | list[dict[str, Any]]:
    if not has_image(state):
        return render_prompt(state, questions, box_units)
    text_state, imgs = placeholders(state)
    text: dict[str, Any] = {"type": "text", "text": render_prompt(text_state, questions, box_units, first_size(state))}
    return [text] + [{"type": "image_url", "image_url": {"url": data_url(i)}} for i in imgs]


def json_schema(questions: Questions) -> dict[str, Any]:
    props: dict[str, Any] = {}
    for qid, q in questions.items():
        if isinstance(q, Boolean):
            props[qid] = {"type": "boolean"}
        elif isinstance(q, Choice):
            props[qid] = {"type": "string", "enum": list(q.criteria)}
        elif isinstance(q, Score):
            props[qid] = {"type": "integer", "enum": list(range(len(q.criteria)))}
        else:
            props[qid] = {"type": "object", "properties": {e: {"type": "number"} for e in EDGES}, "required": list(EDGES), "additionalProperties": False}
    return {"type": "object", "properties": props, "required": list(props), "additionalProperties": False}


def box_answer(boxes: list[BoxEdges]) -> BoxAnswer:
    """The edge-wise median of the samples; with k > 1, how well the samples agree is the confidence."""
    med = {e: float(statistics.median([getattr(b, e) for b in boxes])) for e in EDGES}
    answer = BoxEdges(
        top=min(med["top"], med["bottom"]), bottom=max(med["top"], med["bottom"]),
        left=min(med["left"], med["right"]), right=max(med["left"], med["right"]),
    )
    agreement = float(statistics.fmean([iou(b, answer) for b in boxes])) if len(boxes) > 1 else None
    return BoxAnswer(box=answer, agreement=agreement)


def to_answers(
    samples: list[dict[str, Any]], questions: Questions, distribution: bool, box_units: BoxUnits = "k1000", size: Size | None = None
) -> dict[str, Answer]:
    out: dict[str, Answer] = {}
    for qid, q in questions.items():
        values = [s[qid] for s in samples]
        if isinstance(q, Boolean):
            out[qid] = BooleanAnswer(probability=sum(bool(v) for v in values) / len(values))
            continue
        if not isinstance(q, (Choice, Score)):
            out[qid] = box_answer([to_fractions(v, box_units, size) for v in values])
            continue
        keys = list(q.criteria) if isinstance(q, Choice) else [str(i) for i in range(len(q.criteria))]
        counts = Counter(str(v) for v in values)
        probs = {k: counts[k] / len(values) for k in keys}
        top = max(keys, key=lambda k: probs[k])
        if isinstance(q, Choice):
            out[qid] = ChoiceAnswer(choice=top, probabilities=probs if distribution else None)
        else:
            out[qid] = ScoreAnswer(
                score=sum(int(k) * p for k, p in probs.items()),
                probabilities=probs if distribution else None,
            )
    return out


def provider_error(e: Exception) -> Rejected | ProviderError:
    """litellm's exceptions -> the contract's outcomes. Context overflow and content refusals are the model's limits."""
    import litellm

    status = getattr(e, "status_code", None)
    if isinstance(e, (litellm.ContextWindowExceededError, litellm.ContentPolicyViolationError)):
        return Rejected(f"rejected by the provider ({status}): {str(e)[:200]}", status)
    return ProviderError(f"{type(e).__name__}: {str(e)[:500]}", status)


@dataclass(frozen=True)
class Completed:
    response: Any  # litellm's ModelResponse
    latency_ms: float  # the attempt that answered (as http.Posted)
    retries: int


async def complete(model: str, messages: list[dict[str, Any]], api_key_env: str | None = None, attempts: int = 4, **kwargs: Any) -> Completed:
    """One litellm call with this project's key handling, retries and error outcomes (the LLM baseline and
    GEPA's reflection). The retries are ours, not litellm's, so the latency is the answering attempt's alone (http.py)."""
    import litellm

    env = next(iter(litellm_needs(model, api_key_env).keys), None)
    unset = bool(env) and not os.environ.get(env or "")
    if env:  # an unset key goes as a stand-in for a sandbox's proxy to replace (LiteLLM will not send without one)
        kwargs["api_key"] = os.environ.get(env) or UNSET_KEY
    for attempt in range(attempts):
        t0 = time.perf_counter()
        try:
            r = await litellm.acompletion(model=model, messages=messages, num_retries=0, **kwargs)
            return Completed(r, (time.perf_counter() - t0) * 1000, attempt)
        except Exception as e:  # litellm raises its own and openai's exception types
            err = provider_error(e)
            if unset and env and err.status in AUTH_STATUS:
                raise refused_without(env, err) from e
            transient = retryable(err.status) or isinstance(e, (litellm.Timeout, litellm.APIConnectionError))
            if isinstance(err, Rejected) or not transient or attempt == attempts - 1:
                raise err from e
        await asyncio.sleep(0.5 * 2**attempt)
    raise AssertionError("unreachable")


def response_cost(model: str, responses: list[Any], cache_dir: Path | None = None) -> float | None:
    """Gateway models from the gateway's list prices (litellm does not know them), others from litellm."""
    if model.startswith(GATEWAY_PREFIX):
        tin = sum(r.usage.prompt_tokens for r in responses)
        tout = sum(r.usage.completion_tokens for r in responses)
        return pricing.cost(model.removeprefix(GATEWAY_PREFIX), tin, tout, cache_dir)
    return sum((r._hidden_params or {}).get("response_cost") or 0 for r in responses) or None


def _raw(usage: Any) -> Any:
    """LiteLLM's usage of one response, as JSON (None when it cannot be written)."""
    try:
        return usage.model_dump(mode="json")
    except Exception:  # not LiteLLM's pydantic usage (a test's stand-in)
        return None


class LLMModel:
    def __init__(
        self, model: str, *, samples: int = 1, concurrency: int = 8, api_key_env: str | None = None, image: bool = False,
        box_units: BoxUnits | None = None, capabilities: Capabilities | None = None, cache_dir: Path | None = None,
    ):
        self.box_units: BoxUnits = box_units or "k1000"
        self.model = model
        self.samples = samples
        self.id = f"llm:{model}" + (f"#k{samples}" if samples > 1 else "")
        self.concurrency = concurrency
        # An LLM returns no distribution: k samples make one ("sampled"), one sample has none.
        distribution: Literal["sampled", "none"] = "sampled" if samples > 1 else "none"
        self.capabilities = (capabilities or Capabilities(
            context_tokens=128_000, image=image, question_types=TEXT_TYPES | {"box"} if box_units else TEXT_TYPES,
        )).model_copy(update={"distribution": distribution})
        self.api_key_env = api_key_env
        self.cache_dir = cache_dir  # for the gateway's price list

    async def _one(self, messages: list[dict[str, Any]], schema: dict[str, Any]) -> Completed:
        return await complete(
            self.model, messages, self.api_key_env,
            response_format={"type": "json_schema", "json_schema": {"name": "answers", "schema": schema, "strict": True}},
            temperature=0 if self.samples == 1 else 1,
        )

    async def write(self, messages: list[dict[str, Any]], *, temperature: float = 1) -> tuple[str, Usage]:
        """Free text, not a decision (GEPA's reflection LM, eval/gepa.py): what the model wrote, and its usage priced
        as `decide`'s is."""
        done = await complete(self.model, messages, self.api_key_env, temperature=temperature)
        r = done.response
        cost = response_cost(self.model, [r], self.cache_dir)
        usage = Usage(input_tokens=r.usage.prompt_tokens, output_tokens=r.usage.completion_tokens, cost_usd=cost,
                      cost_source="list" if cost is not None else None, raw=_raw(r.usage))
        return str(r.choices[0].message.content), usage

    async def decide(self, state: State, questions: Questions, *, options: dict[str, Any] | None = None) -> Response:
        check_supported(self, state, questions)
        messages: list[dict[str, Any]] = [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user_content(state, questions, self.box_units)},
        ]
        schema = json_schema(questions)
        done = await asyncio.gather(*(self._one(messages, schema) for _ in range(self.samples)))
        responses = [d.response for d in done]
        try:
            samples = [json.loads(r.choices[0].message.content) for r in responses]
        except (TypeError, ValueError) as e:
            raise ProviderError(f"unreadable structured output: {e}") from e
        tin = sum(r.usage.prompt_tokens for r in responses)
        tout = sum(r.usage.completion_tokens for r in responses)
        cost = response_cost(self.model, responses, self.cache_dir)
        return Response(
            answers=to_answers(samples, questions, distribution=self.samples > 1, box_units=self.box_units, size=first_size(state)),
            answered_by=self.model,
            # A list cost: the gateway's or LiteLLM's table times the tokens (pricing.py), not a bill.
            usage=Usage(input_tokens=tin, output_tokens=tout, cost_usd=cost, cost_source="list" if cost is not None else None,
                        raw={"responses": [_raw(r.usage) for r in responses]}),
            latency_ms=max(d.latency_ms for d in done),  # k samples are asked at once: the answer waits for the slowest
            retries=sum(d.retries for d in done),
            provider_metadata={"samples": samples},
        )


class LLMOptions(Options):
    samples: int = Field(default=1, ge=1)  # k > 1 asks k times at temperature 1 and makes a distribution
    box_units: BoxUnits | None = None  # how this LLM states a box; required for Box questions
    api_key_env: str | None = None  # default: litellm's own lookup (the gateway key for vercel_ai_gateway/)


def needs(spec: ModelSpec) -> Needs:
    o = spec_options(LLMOptions, spec)
    return litellm_needs(spec.id, o.api_key_env)


def published(spec: ModelSpec, cache_dir: Path | None) -> Price | None:
    """The list an LLM's cost is estimated from (response_cost): the gateway's for its models, else LiteLLM's table."""
    if spec.id.startswith(GATEWAY_PREFIX):
        p = pricing.listed(spec.id.removeprefix(GATEWAY_PREFIX), cache_dir)
        return None if p is None else per_token(*p, source=pricing.MODELS_URL)
    require_litellm()
    import litellm

    m = litellm.model_cost.get(spec.id) or litellm.model_cost.get(spec.id.partition("/")[2])
    if not m:
        return None
    return per_token(m.get("input_cost_per_token"), m.get("output_cost_per_token"), f"LiteLLM {litellm_version()} model_cost")


def litellm_version() -> str:
    from importlib.metadata import version

    return version("litellm")


@publishes(published)
@declares(needs)
def build(b: ModelBuild) -> LLMModel:
    require_litellm()
    o = options(LLMOptions, b)
    caps = b.spec.capabilities
    if "box" in caps.question_types and o.box_units is None:
        raise ConfigError(f"{b.name}: Box questions need options.box_units (k1000 or pixels), the units this LLM answers in")
    if declared(b) and "distribution" in caps.model_fields_set:
        raise ConfigError(f"{b.name}: an LLM's distribution follows options.samples; leave it out of capabilities")
    return LLMModel(
        b.spec.id, samples=o.samples, concurrency=b.spec.concurrency or 8, api_key_env=o.api_key_env,
        box_units=o.box_units, capabilities=caps, cache_dir=b.cache_dir,
    )
