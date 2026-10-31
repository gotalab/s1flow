"""`s1flow decide`: call a model with questions given here (--model), or decide with a task's policy (--policy).
The base install runs it."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

from ..core.errors import ConfigError, S1flowError
from .common import POLICY, client, command, json_arg, load_env, policy_client, policy_root, project_root

if TYPE_CHECKING:
    from ..client import Response
    from ..client.answers import Answer
    from ..client.state import State


def decide(a: argparse.Namespace) -> int:
    if a.policy is not None and not a.policy.strip():
        raise ConfigError(f"--policy is empty: name a policy, {POLICY}")
    if (a.model is None) == (a.policy is None):
        raise ConfigError("decide takes --model (call a model) or --policy (decide with a policy), one of them")
    root = project_root(a)
    load_env(root)
    if a.policy:
        return _decide_policy(a)
    state = _state(a)
    qs = _questions(a)
    if not qs:
        raise ConfigError('decide --model needs questions: --questions @qs.json ({"area": {"type": "choice", ...}}), or --boolean TEXT')
    c = policy_client(a) if a.connections else client(a, root)
    c.connections.resolved(a.model)  # a wrong name or version lists the right ones before a key is read
    d = c.responses.create(model=a.model, state=state, questions=qs)
    if a.json:
        print(d.model_dump_json(indent=1))
    else:
        _print_response(d)
    return 0


def _decide_policy(a: argparse.Namespace) -> int:
    from .. import policies

    if a.questions or a.boolean is not None:
        raise ConfigError("a policy asks its own question: leave out --questions and --boolean")
    out = os.environ.get("GITHUB_OUTPUT")
    if a.github_output and not out:
        raise S1flowError("--github-output needs $GITHUB_OUTPUT (set by GitHub Actions)")
    if a.keep_state and not a.log:
        raise ConfigError("--keep-state keeps the state in the log: give --log too")
    r = policies.load(a.policy, client=policy_client(a), path=a.path, root=policy_root(a), log=a.log, keep_state=a.keep_state).decide(_state(a), case_id=a.case_id)
    if a.github_output and out:
        answer = r.value if isinstance(r.value, str) else json.dumps(r.value)  # a class key as is; true / false
        with open(out, "a") as f:
            for k, v in {"answer": answer, "probability": f"{r.probability:.4f}", "below_min_probability": json.dumps(r.below_min_probability), "decision_id": r.decision_id, "policy": r.policy}.items():
                f.write(f"{k}={v}\n")
    if a.json:
        print(r.model_dump_json(indent=1))
    else:
        print(f"{r.policy}: {json.dumps(r.value, ensure_ascii=False)} (probability {r.probability:.3f}" + (", below minimum probability" if r.below_min_probability else "") + f"; {r.answered_by})")
    return 0


def _questions(a: argparse.Namespace) -> dict[str, Any] | None:
    """--questions JSON, or the one yes / no question --boolean asks (named q)."""
    from ..client.questions import Boolean

    if a.boolean is not None and a.questions:
        raise ConfigError("give the questions once: --questions, or --boolean")
    if a.boolean is not None:
        return {"q": Boolean(instructions=a.boolean)}
    return json_arg(a.questions, "--questions") if a.questions else None


def _state(a: argparse.Namespace) -> State:
    from ..client import images
    from ..client.state import has_unprepared_image
    from ..core.errors import DataError

    state: Any = json_arg(a.state, "--state") if a.state is not None else None
    if has_unprepared_image(state):
        raise DataError("state cannot load files or URLs; use --image PATH for an explicit local image")
    if a.image:
        parts = [] if state is None else state if isinstance(state, list) else [state]
        prepared = [images.prepare(Path(path).read_bytes()) for path in a.image]
        state = [*parts, *prepared]
    if state is None:
        raise ConfigError("decide needs a state: --state JSON, or --state @file.json")
    return cast("State", state)


def _line(qid: str, x: Answer) -> str:
    from ..client.answers import BooleanAnswer, BoxAnswer, ChoiceAnswer, ScoreAnswer

    if isinstance(x, BooleanAnswer):
        return f"{qid}: P(true) {x.probability:.3f}"
    if isinstance(x, ChoiceAnswer):
        probs = sorted((x.probabilities or {}).items(), key=lambda kv: -kv[1])
        dist = " · ".join(f"{k} {p:.3f}" for k, p in probs) if probs else x.choice
        return f"{qid}: {x.choice}" + (f"  ({dist})" if probs else "")
    if isinstance(x, ScoreAnswer):
        dist = " · ".join(f"{k}: {p:.3f}" for k, p in sorted((x.probabilities or {}).items(), key=lambda kv: int(kv[0])))
        return f"{qid}: {x.score:.2f}" + (f"  ({dist})" if dist else "")
    if isinstance(x, BoxAnswer):
        b = x.box
        conf = x.confidence if x.confidence is not None else x.agreement
        return f"{qid}: top {b.top:.3f} bottom {b.bottom:.3f} left {b.left:.3f} right {b.right:.3f}" + ("" if conf is None else f"  (confidence {conf:.2f})")
    return f"{qid}: refused" + (f" ({x.reason})" if x.reason else "")


def _print_response(d: Response) -> None:
    for qid, x in d.answers.items():
        print(_line(qid, x))
    cost = "" if d.usage.cost_usd is None else f" · ${d.usage.cost_usd:.6f}"
    print(f"({d.answered_by} · {d.latency_ms:.0f}ms{cost})")


def add(sub: Any) -> None:
    d = command(sub, "decide", decide, context=("project", "connections"), help="call a model (--model) or decide with a policy (--policy)",
                description="Call a model with the questions given here (--model), or decide with a task's policy (--policy).")
    which = d.add_argument_group("what answers")
    which.add_argument("--model", help="a name in s1flow.toml (jev, or jev:1.14 for a version)")
    which.add_argument("--policy", metavar=POLICY, help="decide with this policy (policies/<task>/; the current version when no @ is given)")
    d.add_argument("--state", help="the state as JSON, or @file.json")
    d.add_argument("--image", action="append", metavar="PATH", help="add an image to the state (needs s1flow[images]); repeatable")
    asked = d.add_argument_group("the questions (--model)")
    asked.add_argument("--questions", help='the questions as JSON {"name": {"type": "choice", "instructions": ..., "criteria": ...}}, or @file.json')
    asked.add_argument("--boolean", metavar="TEXT", help="one yes / no question instead, named q")
    rel = d.add_argument_group("a policy (--policy)")
    rel.add_argument("--path", help="a policy file, or a policy set from `s1flow export` (policies.json), instead of policies/")
    rel.add_argument("--case-id", help="the case's id in your app, kept in the log for context (it may repeat; feedback record joins by decision_id)")
    rel.add_argument("--log", help="append the log here (JSONL)")
    rel.add_argument("--keep-state", action="store_true", help="keep the state in the log, so `feedback measure --add` can add the case as a labelled one")
    rel.add_argument("--github-output", action="store_true", help="also write answer, probability, below_min_probability, decision_id, policy to $GITHUB_OUTPUT")
    d.add_argument("--json", action="store_true", help="print the Response (with --policy, the Decision) as JSON")
