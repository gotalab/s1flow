"""Call the models and append to runs/<task>/<variant>/<model>.jsonl.

The file is append-only: one `PredictionRecord` per case asked (records.py), stamped with the
prompt hash, the model that actually answered (`answered_by`) and the time. A version asked for by
name (`jev:1.14`) is a run of its own, `jev:1.14.jsonl`: under an alias (`jev`) the answering version can
change between lines. Readers pick the lines for the current prompt and one answering model
(metrics.load), so nothing is ever overwritten
and a failed run only adds failure lines. A ConfigError (a missing key) stops the run instead:
it is not the case's outcome.

Every call goes through the model-calling layer (`AsyncClient.responses.create`), wrapped in a cache:
the `Response` is kept under sha256(model id, request) in .cache/answers/, so a rerun
with the same settings costs nothing. Whatever a call ends with is recorded as its outcome, never raised.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import sys
import time
from collections.abc import Mapping
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from ..client import AsyncClient
from ..client._client import AsyncResponses, ModelRef, validate_questions
from ..client.answers import Response
from ..client.identity import request_digest, require_provider_revision, model_digest
from ..client.models import DecisionModel, ModelSpec
from ..client.questions import Question, Questions
from ..client.state import State
from ..core import clock
from ..core.errors import ConfigError, NotFound
from .candidate import Candidate
from . import records
from .records import PredictionRecord
from .cases import Case
from .task import Task


def cache_key(spec: ModelSpec, state: State, questions: Questions) -> str:
    """The effective binding and actual input, with the request implementation revision."""
    require_provider_revision(spec)
    return request_digest(spec, state, questions)


def prompt_hash(questions: Questions) -> str:
    """The prompt as the model sees it: questions, options, instructions."""
    payload = json.dumps({k: q.model_dump() for k, q in questions.items()}, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(payload.encode()).hexdigest()[:12]


class Cached(BaseModel):
    """One cached call (.cache/answers/): the Response, and how many calls were in flight to the model when it was made."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    schema_: Literal["s1flow/cached@1"] = Field(default="s1flow/cached@1", alias="schema")
    response: Response
    concurrency: int | None = None

    def dump(self) -> str:
        return self.model_dump_json(by_alias=True)


def cache_path(cache_dir: Path, key: str) -> Path:
    return cache_dir / "answers" / key[:2] / f"{key}.json"


def cached(cache_dir: Path, spec: ModelSpec, state: State, questions: Questions) -> bool:
    """Whether the cache holds the answer `call` would read for this call (no call is made)."""
    return cache_path(cache_dir, cache_key(spec, state, questions)).exists()


async def call(
    cache_dir: Path, client: AsyncClient, model: DecisionModel, state: State, questions: Questions, fresh: bool = False,
    concurrency: int | None = None, *, spec: ModelSpec,
) -> tuple[Cached, bool]:
    """A cached call keeps the latency and concurrency of the call that made it."""
    key = cache_key(spec, state, questions)
    path = cache_path(cache_dir, key)
    if path.exists() and not fresh:
        try:
            return Cached.model_validate_json(path.read_text()), True
        except ValidationError:  # not a failed call: recorded as one, it would stay failed until --fresh
            raise ConfigError(f"{path}: an answer cached in an older shape; rewrite the cache entry "
                              "by rerunning with --fresh, or explicitly remove this entry before rerunning") from None
    d = await client.responses.create(model=model, state=state, questions=questions)
    got = Cached(response=d, concurrency=concurrency or model.concurrency)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(got.dump())
    return got, False


class CachedResponses(AsyncResponses):
    """`responses.create` answered from the cache first (`call`). Counts, per decision returned, whether the
    cache answered it (`hit`), and the calls made and the ones the cache answered."""

    def __init__(self, inner: AsyncClient, cache_dir: Path):
        super().__init__(inner.connections)
        self._inner, self._cache_dir = inner, cache_dir
        self.calls = self.cached = 0
        self._hits: dict[int, bool] = {}
        self._timing_current: dict[int, bool] = {}

    async def create(
        self, *, model: ModelRef, state: State, questions: Mapping[str, Question | dict[str, Any]], options: dict[str, Any] | None = None,
    ) -> Response:
        if options:
            raise ConfigError("the evaluation's cache keys no per-call options")
        if isinstance(model, str):
            spec = self._connections.resolved(model)
        elif isinstance(model, ModelSpec):
            spec = model.resolved()
        else:
            # A free-standing object has no verified effective binding. Calling it is
            # supported, but it cannot safely share a persistent answer cache.
            d = await self._inner.responses.create(model=model, state=state, questions=questions)
            self.calls += 1
            self._hits[id(d)] = False
            self._timing_current[id(d)] = True
            return d
        built = self._model(model)
        got, hit = await call(self._cache_dir, self._inner, built, state, validate_questions(questions), spec=spec)
        self.cached += hit
        self.calls += not hit
        self._hits[id(got.response)] = hit
        self._timing_current[id(got.response)] = got.concurrency == built.concurrency
        return got.response

    def hit(self, d: Response) -> bool:
        """Whether the cache answered this decision (one this object returned)."""
        return self._hits[id(d)]

    def timing_current(self, response: Response) -> bool:
        """Whether this raw response's measured concurrency matches this execution."""
        return self._timing_current[id(response)]


class CachedClient(AsyncClient):
    """An `AsyncClient` whose decisions come from the evaluation's cache first: what `check` passes to
    `policies.load`, so a policy decides there as it does in production, and unchanged answers cost nothing."""

    def __init__(self, inner: AsyncClient, cache_dir: Path):
        self.connections = inner.connections
        self.responses: CachedResponses = CachedResponses(inner, cache_dir)


def run_path(task: Task, variant: str, model_name: str) -> Path:
    return task.where.runs_dir / task.id / variant / f"{model_name}.jsonl"


def ask_again(task: Task, missing: list[tuple[str, str]]) -> str:
    """The command that asks (model, variant) pairs the cases they have no answer to: a run skips the answered and refused."""
    names = dict.fromkeys(Candidate(model=m, variant=v).name for m, v in missing)
    return f"s1flow run {task.id} --models {','.join(names)}"


async def run_model(
    task: Task, model_name: str, *, limit: int | None, variant: str, fresh: bool = False,
    concurrency: int | None = None,
) -> dict[str, int]:
    """`concurrency` overrides the model's own: 1 times each call alone, with nothing else in flight to it."""
    spec = task.where.lineup().resolved(model_name)
    require_provider_revision(spec)
    client = task.where.client()
    model = client.connections.build(spec, name=model_name)
    cache_dir = task.where.cache_dir
    width = concurrency or model.concurrency
    questions = task.questions(variant)
    prompt = prompt_hash(questions)
    out = run_path(task, variant, model_name)
    cases = task.load_cases().all()[:limit] if limit else task.load_cases().all()
    previous = records.read(out) if not fresh else []
    # Identity is checked per materialized input. An unchanged id/prompt alone is
    # insufficient, and legacy history without an identity never becomes current.
    inputs: dict[str, State] = {}
    identities: dict[str, str] = {}
    for case in cases:
        try:
            inputs[case.id] = task.model_state(case)
            identities[case.id] = request_digest(spec, inputs[case.id], questions)
        except ConfigError:
            raise
        except Exception:
            pass  # one() records the input error using the normal outcome path
    done_before = {r.id for r in previous if r.request_digest and r.request_digest == identities.get(r.id)
                   and (r.answered or r.outcome in records.REFUSED)}
    todo = [c for c in cases if c.id not in done_before]
    sem = asyncio.Semaphore(width)
    stats = {"calls": 0, "cached": 0, "skipped": len(cases) - len(todo), "unsupported": 0, "rejected": 0, "errors": 0, "data_errors": 0}
    done = 0

    async def one(case: Case) -> PredictionRecord:
        nonlocal done
        base: dict[str, Any] = {
            "id": case.id, "label": case.label, "model": model_name, "variant": variant,
            "prompt": prompt, "distribution": model.capabilities.distribution,
            "request_digest": identities.get(case.id),
        }
        now = clock.now  # stamped when the call ends
        async with sem:
            try:
                state = inputs[case.id] if case.id in inputs else task.model_state(case)
                got, hit = await call(cache_dir, client, model, state, questions, fresh, width, spec=spec)
                rec = records.from_response(base | {"at": now()}, got.response, task.question_id, hit, got.concurrency)
                stats["cached" if hit else "calls"] += 1
            except ConfigError:
                raise
            except Exception as e:  # every outcome is recorded (records.from_exception), none is raised
                rec = records.from_exception(base | {"at": now()}, e)
                stats[{"unsupported": "unsupported", "rejected": "rejected", "data_error": "data_errors"}.get(rec.outcome, "errors")] += 1
        done += 1
        if done % 25 == 0:
            print(f"  {model_name}: {done}/{len(todo)}", file=sys.stderr)
        return rec

    t0 = time.perf_counter()
    recs = await asyncio.gather(*(one(c) for c in todo))
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("a") as f:
        f.writelines(r.line() + "\n" for r in recs)
    stats["seconds"] = round(time.perf_counter() - t0)
    _write_meta(out.with_suffix(".meta.json"), stats, width, spec)
    return stats


META = "s1flow/run-meta@1"  # runs/<task>/<variant>/<model>.meta.json


def _write_meta(path: Path, stats: dict[str, int], concurrency: int, spec: ModelSpec) -> None:
    """Wall time of the last run that made every call itself; cached reruns keep the earlier one."""
    meta = json.loads(path.read_text()) if path.exists() else {"schema": META}
    meta["last"] = stats
    meta["requested"] = {"concurrency": concurrency, "declared_concurrency": spec.concurrency, "model_digest": model_digest(spec)}
    if stats["calls"] and not stats["cached"]:
        meta["measured"] = {"seconds": stats["seconds"], "calls": stats["calls"], "concurrency": concurrency}
    path.write_text(json.dumps(meta))


def candidates(task: Task, names: list[str]) -> list[Candidate]:
    """Candidate names (`jev:1.14`, `d1@vercel/policy`) checked before any call: the model and its version in the
    line-up, the variant in the task. A wrong one is a NotFound listing what there is."""
    models = task.where.lineup()
    out = []
    for name in names:
        c = Candidate.parse(name)
        require_provider_revision(models.resolved(c.model))
        if c.variant != "base" and c.variant not in task.variants:
            raise NotFound(f"{task.id} has no variant {c.variant!r}; variants: {', '.join(task.variants) or 'none'}")
        out.append(c)
    return out


async def run(
    task: Task, names: list[str], *, limit: int | None = None, fresh: bool = False, concurrency: int | None = None,
) -> dict[str, dict[str, int]]:
    """The candidates run side by side; with `concurrency`, one after another, so no call shares the machine's network.
    Every name is checked before any call (`candidates`)."""
    cands = candidates(task, names)
    one = lambda c: run_model(task, c.model, limit=limit, variant=c.variant, fresh=fresh, concurrency=concurrency)
    if concurrency:
        return {c.name: await one(c) for c in cands}
    return dict(zip((c.name for c in cands), await asyncio.gather(*(one(c) for c in cands))))
