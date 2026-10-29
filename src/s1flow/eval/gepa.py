"""Question optimization with GEPA, for `s1flow optimize` (install `s1flow[optimize]`).

The candidate is the question itself: its instructions and every option's
description, as one text block. DSPy's GEPA mutates a signature's
instructions, which DSPy's System One translation places in the *state*; the
question and criteria jev reads come from field descriptions and the type, out
of GEPA's reach. So this drives the `gepa` engine that dspy.GEPA wraps with an
adapter over s1flow's own (cached) providers, which also lets any model be
optimized.

GEPA sees the dev share only (train to read errors from, val to select on). The test share is
saved with the result; `optimize` checks the new question on it.

Two optional inputs give the reflection LM more than right and wrong answers:
`tasks/<id>/context.md` (how the team decides: a triage policy, CONTRIBUTING, a bot's
prompt) and a `rationale` field on a row (why that case got its label, e.g. the
maintainers' comments around the labelling; `s1flow github rationale` adds them). Neither reaches the
model being optimized.
"""

from __future__ import annotations

import asyncio
import re
from dataclasses import dataclass
from typing import Any, Callable, Coroutine

from ..client import AsyncClient, cost
from ..core import clock
from ..client.answers import BooleanAnswer, ChoiceAnswer, Usage
from ..client.models import DecisionModel, ModelSpec, Price
from ..client.questions import Boolean, Choice, Question
from ..core.errors import ConfigError, ProviderError, Rejected, S1flowError
from ..policies.rule import DecisionRule
from . import evalset
from .run import call
from .cases import Case
from .task import Optimized, Task

# The reflection LM when `--reflection` names no `llm` model of s1flow.toml: OpenAI's own API with OPENAI_API_KEY,
# the key luna@decisions reads, so OpenAI bills it and its credit (ChatGPT Pro's API credits included) applies.
# Its list price is declared (free allowance not deducted). Earlier artifacts used it through the AI Gateway
# ("vercel_ai_gateway/openai/gpt-6.1-sol") and before that "vercel_ai_gateway/anthropic/claude-sonnet-5.5".
REFLECTION = ModelSpec(
    provider="llm", id="openai/gpt-6.1-sol",
    price=Price(input_per_mtok=2.00, output_per_mtok=10.00, as_of="2026-10-03", source="OpenAI's list price for gpt-6.1-sol"),
)
# Length limits on the rewritten question, in characters, where s1flow.toml declares none
# (`max_instructions_chars` / `max_description_chars`; Laya's are 300 / 60).
DEFAULT_LIMITS = (600, 300)


def limits(model: DecisionModel) -> tuple[int, int]:
    caps = model.capabilities
    return caps.max_instructions_chars or DEFAULT_LIMITS[0], caps.max_description_chars or DEFAULT_LIMITS[1]

TEMPLATE = """I want to improve the question given to a decision model: a model that reads a text and returns a probability for each option, and writes no text of its own.

The current question:
```
<curr_param>
```

<context>Cases this question was asked about, with feedback on each answer:
```
<side_info>
```

From the cases the model got wrong, and the ones it got right with low confidence, work out which criteria the model misread, and rewrite the question. Where a case comes with the reason for its label, take the criteria from that reason.

Rules:
- Keep the current format. The first line starts with "INSTRUCTIONS: ", then a "CRITERIA:" line, then one line per option as "- key: description".
- Keep the option keys (left of the colon) exactly as they are: add none, remove none, and keep their order.
- Keep INSTRUCTIONS within {max_instructions} characters and each option's description within {max_description}. Some decision models reject longer text.
- Don't copy wording from the cases. Write criteria that hold for every case, not for particular ones.
- Decision models often misread negation and numeric comparisons. Say what does apply rather than what doesn't.
- Write in the same language as the current question.

Output only the rewritten question, wrapped in ```."""


# ---------- the question as one text component ----------


def to_text(q: Question) -> str:
    lines = [f"INSTRUCTIONS: {q.instructions}", "CRITERIA:"]
    if isinstance(q, Choice):
        lines += [f"- {k}: {v or ''}".rstrip() for k, v in q.criteria.items()]
    elif isinstance(q, Boolean):
        crit = q.criteria or {"true": "", "false": ""}
        lines += [f"- {k}: {crit.get(k, '')}".rstrip() for k in ("true", "false")]
    else:
        raise S1flowError("score questions are not optimized yet")
    return "\n".join(lines)


def from_text(text: str, like: Question) -> Question:
    """Parse a candidate back into a question of the same type and keys; ValueError if it drifted."""
    text = text.strip().strip("`").strip()
    m = re.search(r"INSTRUCTIONS:\s*(.*?)\n\s*CRITERIA:\s*\n(.*)", text, re.S)
    if not m:
        raise ValueError("expected 'INSTRUCTIONS: ...' then 'CRITERIA:' lines")
    instructions = " ".join(m.group(1).split())
    crit: dict[str, str] = {}
    for line in m.group(2).splitlines():
        lm = re.match(r"\s*-\s*([^:：]+?)\s*[:：]\s*(.*)$", line)
        if lm:
            crit[lm.group(1).strip()] = lm.group(2).strip()
    keys = list(like.criteria) if isinstance(like, Choice) else ["true", "false"]
    if list(crit) != keys:
        missing, extra = set(keys) - set(crit), set(crit) - set(keys)
        raise ValueError(f"option keys changed (missing {sorted(missing)[:5]}, extra {sorted(extra)[:5]})")
    if isinstance(like, Choice):
        return Choice(instructions=instructions, criteria={k: crit[k] or None for k in keys})
    return Boolean(instructions=instructions, criteria={k: crit[k] for k in keys if crit[k]} or None)


# ---------- scoring one answer ----------


@dataclass(frozen=True)
class Outcome:
    """One case, as GEPA scores it and the reflection LM reads it."""

    label: Any
    predicted: Any
    probability: float  # of `predicted`
    correct: bool
    brier: float
    top: list[tuple[str, float]] | None = None  # many classes: the three most probable


def outcome(task: Task, case: Case, answer: BooleanAnswer | ChoiceAnswer) -> Outcome:
    """Correctness, a proper score, and what the model said, for one case (read as a policy reads it)."""
    label, kind = case.label, task.kind
    r = kind.read([answer], DecisionRule())
    assert r.probability is not None
    top = sorted(zip(kind.options, r.distribution), key=lambda kv: -kv[1])[:3] if r.distribution is not None else None
    return Outcome(label, r.value, r.probability, kind.correct(label, r), kind.brier(label, r), top)


def score(o: Outcome) -> float:
    """Prompt-search surrogate: half correctness, half (1 - Brier), not the Task's objective."""
    return 0.5 * float(o.correct) + 0.5 * (1.0 - o.brier)


# ---------- GEPA adapter ----------


@dataclass
class Inst:
    case: Case


@dataclass
class Trace:
    case: Case
    outcome: Outcome | None = None
    error: str | None = None


class QuestionAdapter:
    propose_new_texts = None  # use GEPA's reflective proposer with our template

    def __init__(self, task: Task, client: AsyncClient, model: DecisionModel, *, spec: ModelSpec, concurrency: int = 8):
        self.task = task
        self.client = client
        self.model = model
        self.spec = spec
        self.cache_dir = task.where.cache_dir
        self.concurrency = concurrency
        self.calls = 0

    async def _answers(self, batch: list[Inst], q: Question) -> list[tuple[BooleanAnswer | ChoiceAnswer | None, str | None]]:
        sem = asyncio.Semaphore(self.concurrency)

        async def one(inst: Inst) -> tuple[BooleanAnswer | ChoiceAnswer | None, str | None]:
            async with sem:
                try:
                    got, hit = await call(self.cache_dir, self.client, self.model, self.task.model_state(inst.case), {self.task.question_id: q}, concurrency=self.concurrency, spec=self.spec)
                    if not hit:
                        self.calls += 1
                    answer = got.response.answers[self.task.question_id]
                    if not isinstance(answer, (BooleanAnswer, ChoiceAnswer)):
                        raise Rejected(f"the model refused to answer {self.task.question_id}")
                    return answer, None
                except ProviderError as e:  # scored as a failure, shown to the reflection LM
                    return None, f"{type(e).__name__}: {str(e)[:200]}"

        return await asyncio.gather(*(one(i) for i in batch))

    def evaluate(self, batch: list[Inst], candidate: dict[str, str], capture_traces: bool = False) -> Any:
        from gepa.core.adapter import EvaluationBatch

        try:
            q = from_text(candidate["question"], self.task.question)
        except ValueError as e:
            broken = [Trace(i.case, error=f"the question is malformed: {e}") for i in batch]
            return EvaluationBatch(outputs=[None] * len(batch), scores=[0.0] * len(batch), trajectories=broken if capture_traces else None)
        answers = asyncio.run(self._answers(batch, q))
        outputs: list[Outcome | None] = []
        scores: list[float] = []
        traces: list[Trace] = []
        for inst, (answer, err) in zip(batch, answers):
            if answer is None:
                outputs.append(None)
                scores.append(0.0)
                traces.append(Trace(inst.case, error=err))
                continue
            o = outcome(self.task, inst.case, answer)
            outputs.append(o)
            scores.append(score(o))
            traces.append(Trace(inst.case, o))
        return EvaluationBatch(outputs=outputs, scores=scores, trajectories=traces if capture_traces else None)

    def make_reflective_dataset(self, candidate: dict[str, str], eval_batch: Any, components_to_update: list[str]) -> dict[str, list[dict[str, str]]]:
        """GEPA's reflective dataset: per component, records of Inputs / Generated Outputs / Feedback."""
        recs = []
        crit = self.task.question.criteria if isinstance(self.task.question, Choice) else {}
        t: Trace
        for t in eval_batch.trajectories or []:
            case = t.case.text
            if t.outcome is None:
                recs.append({"Inputs": case, "Generated Outputs": "(no answer)", "Feedback": t.error or ""})
                continue
            o = t.outcome
            said = f"Answer: {o.predicted} (probability {o.probability:.2f})"
            if o.top:
                said += ". Top: " + ", ".join(f"{k} {v:.2f}" for k, v in o.top)
            if o.correct:
                fb = "Correct." + (" But the probability is low: criteria that make the choice clear would help." if o.probability < 0.8 else "")
            else:
                gold = o.label
                hint = f" ({crit.get(gold)})" if crit.get(gold) else ""
                fb = f"Wrong. The right answer is {gold}{hint}. Fix the ambiguity in the criteria that led the model to choose {o.predicted}."
            if t.case.rationale:
                fb += f"\nWhy this case got its label: {t.case.rationale}"
            recs.append({"Inputs": case, "Generated Outputs": said, "Feedback": fb})
        recs.sort(key=lambda r: not r["Feedback"].startswith("Wrong"))  # errors first
        return {c: recs for c in components_to_update}


class ReflectionLM:
    """GEPA's reflection LM: an `llm` model of the line-up (`name`; default REFLECTION), called through the client.
    A callable that also counts its calls and what they cost."""

    def __init__(self, client: AsyncClient, name: str | None = None):
        spec = REFLECTION if name is None else client.connections.resolved(name)
        model = client.connections.build(REFLECTION) if name is None else client.connections.build(name)
        write = getattr(model, "write", None)  # an `llm` model (client/providers/llm.py), maybe priced (cost.Listed)
        if write is None:
            raise ConfigError(f"the reflection LM writes text, so it is an `llm` model of s1flow.toml; {name} is {spec.provider}")
        self.name = name or REFLECTION.id
        self.write: Callable[..., Coroutine[Any, Any, tuple[str, Usage]]] = write
        self.price = spec.price
        self.cost = 0.0
        self.calls = 0

    def __call__(self, prompt: str | list[dict[str, Any]]) -> str:
        messages = prompt if isinstance(prompt, list) else [{"role": "user", "content": prompt}]
        text, usage = asyncio.run(self.write(messages, temperature=1))
        self.cost += cost.estimate(usage, self.price).cost_usd or 0.0
        self.calls += 1
        return text


# ---------- the run ----------


def splits(task: Task, cases: list[Case]) -> dict[evalset.Role, list[str]]:
    """test (kept from GEPA) / train / val: the task's fixed evaluation set (evalset.py), over these cases."""
    sf, _ = evalset.ensure(task)
    have = {c.id for c in cases}
    roles: tuple[evalset.Role, ...] = ("train", "val", "test")
    return {role: [i for i in sf.ids(role) if i in have] for role in roles}


def optimize(
    task: Task,
    model_name: str,
    *,
    budget: int,
    seed: int = 1,
    reflection: str | None = None,
    minibatch: int = 8,
    start: str = "base",
    merge: bool = False,
    patience: int | None = None,
    max_cost: float | None = None,
    name: str | None = None,
) -> Optimized:
    """`start` picks the question GEPA begins from: the task's own, or one of its variants.

    The budget (`max_metric_calls`) bounds the loop. `patience` stops after that many proposals
    without a new best on val, `max_cost` once the reflection LM has cost that much (USD, list
    price). `merge` lets GEPA combine candidates that won on different cases.
    """
    import gepa
    from gepa.utils.stop_condition import NoImprovementStopper

    cases = task.load_cases().all()
    by_id = {c.id: c for c in cases}
    sp = splits(task, cases)
    client = task.where.client()
    model = client.connections.build(model_name)
    adapter = QuestionAdapter(task, client, model, spec=client.connections.resolved(model_name))
    lm = ReflectionLM(client, reflection)
    seed_q = task.question if start == "base" else task.variants[start]
    seed_text = to_text(seed_q)
    max_ins, max_desc = limits(model)
    ctx_path = task.dir / "context.md"
    context = f"How this team decides (for reference):\n```\n{ctx_path.read_text().strip()}\n```\n\n" if ctx_path.exists() else ""
    template = (
        TEMPLATE.replace("{max_instructions}", str(max_ins)).replace("{max_description}", str(max_desc)).replace("<context>", context)
    )
    stoppers: list[Any] = []
    if patience:
        stoppers.append(NoImprovementStopper(patience))
    if max_cost:
        stoppers.append(lambda state: lm.cost >= max_cost)
    result: Any = gepa.optimize(
        seed_candidate={"question": seed_text},
        trainset=[Inst(by_id[i]) for i in sp["train"]],
        valset=[Inst(by_id[i]) for i in sp["val"]],
        adapter=adapter,  # type: ignore[arg-type]  # a structural GEPAAdapter; gepa's generics cannot infer Inst
        reflection_lm=lm,
        reflection_prompt_template=template,
        reflection_minibatch_size=minibatch,
        max_metric_calls=budget,
        seed=seed,
        display_progress_bar=False,
        raise_on_exception=False,
        use_merge=merge,
        stop_callbacks=stoppers or None,
    )
    best = from_text(result.best_candidate["question"], task.question)
    name = name or (f"gepa-{model_name}" if start == "base" else f"gepa-{model_name}-from-{start}")
    artifact = Optimized(
        variant=name, model=model_name, method="gepa", at=clock.now(), question=best, seed_question=seed_q, start=start,
        context=ctx_path.name if ctx_path.exists() else None,
        rationales=sum(1 for i in sp["train"] + sp["val"] if by_id[i].rationale),
        split=sp, seed=seed, budget=budget, merge=merge, patience=patience, max_cost=max_cost, reflection_lm=lm.name,
        reflection_calls=lm.calls, reflection_cost_usd=round(lm.cost, 4), model_calls=adapter.calls, candidates=len(result.candidates),
        val_scores=[round(s, 4) for s in result.val_aggregate_scores], best_index=result.best_idx,
    )
    out = task.dir / "optimized" / f"{name}.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(artifact.model_dump_json(exclude_none=True, indent=1))
    task.add_optimized(artifact)
    return artifact
