"""`s1flow adopt`: the one command that switches a task's current policy (history.jsonl says why, each time)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from ..core import place
from ..core.errors import ConfigError, S1flowError
from .common import command, policy_client, project, project_root, shown


def adopt(a: argparse.Namespace) -> int:
    """Switch the task's current policy, with why (who: git config user.name; history.jsonl keeps each switch): to a
    measured candidate (TASK CANDIDATE), or to a runtime spec saved unevaluated (--spec FILE; the base install runs
    it). The pull request that carries it ships it when
    it merges. A candidate the held-out test shows below is not written (exit 1) unless --force."""
    a.reason = (a.reason or "").strip()
    if a.check and not a.spec:
        raise S1flowError("adopt --check validates a spec: adopt --spec FILE --check")
    if not a.reason and not a.check:
        raise S1flowError("adopt records why: give --reason a sentence")
    if a.spec:
        return _adopt_spec(a)
    if a.root:
        raise S1flowError("--root is where adopt --spec FILE saves, outside an s1flow project")
    if not a.task or not a.candidate:
        raise S1flowError("adopt takes TASK CANDIDATE or --spec FILE")
    from ..eval import adopt as adopting
    from ..eval.task import load
    from ..integrations import git

    task = load(project(a), a.task)
    listed = adopting.shortlist(task)
    listed.pickable(a.candidate)
    user = git.user(task.where.root)
    if not user:
        raise S1flowError("a policy records who adopted it: set git config user.name")
    previous = task.policies.current(task.id)
    r = adopting.adopt(task, a.candidate, user, a.reason, listed=listed, git_sha=git.sha(task.where.root), force=a.force)
    held = r.evidence.test == "below" and not a.force
    d = task.policies.dir(task.id)
    wrote = ("not written: below on the held-out test (adopt again with --force to ship it anyway); wrote "
             + shown(d / "history.jsonl") + " (the refusal)" if held else
             "wrote " + ", ".join(shown(f) for f in (d / f"v{r.spec.version}.json", d / "channels.json", d / "history.jsonl"))
             + " (the policy, current, why)")
    check_it = None if held or previous is None else f"compare it with v{previous}: s1flow check {task.id} --against v{previous}"
    if a.json:  # stdout is the policy alone
        print(r.model_dump_json(by_alias=True, indent=1))
        print(wrote, file=sys.stderr)
        return 1 if held else 0
    e = r.evidence.evaluation
    p0 = e.objective
    assert p0 is not None
    rd = r.spec.rule
    print(f"{r.spec.ref}{'' if held else ' (current)'}: {r.candidate.name}, answered by {r.answered_by}; adopted by {r.selection.by}")
    if r.candidate.name not in r.selection.tied:
        print(f"  note: measured worse on {p0.objective.label} than the candidates tied at the top ({', '.join(r.selection.tied)})")
    print("  rule: " + (", ".join(f"{k} {v:.3f}" for k, v in (("threshold", rd.threshold), ("min probability", rd.min_probability)) if v is not None) or "the plain argmax"))
    print(f"  {p0.objective.label}: {p0.value}  interval {p0.interval}  (n {e.n})")
    if e.test:
        print(f"  held-out test: n {e.test.n}, primary {e.test.primary.value}  -> {r.evidence.test}"
              + (" (written with --force; the reason is recorded as why)" if r.selection.forced else ""))
    print(wrote)
    if check_it:
        print(check_it)
    return 1 if held else 0


def _adopt_spec(a: argparse.Namespace) -> int:
    """adopt --spec FILE: save a runtime spec as its task's next version, unevaluated, and make it current (with
    --check, validate it only). No model is called and nothing is measured. In an s1flow project, its policies/ and
    s1flow.toml; in an app's repository, --root and --connections."""
    from ..integrations import git
    from ..policies import DecisionPolicy, Policies
    from ..policies.file import read_file
    from ..policies.history import Switch

    if a.task or a.candidate or a.force:
        raise S1flowError("adopt --spec FILE takes no TASK, candidate or --force: the spec names its task and version, and nothing is measured")
    spec = read_file(a.spec)
    # --check with --connections alone, outside a project: the binding only
    found = None if a.root else project_root(a, required=not (a.check and a.connections))
    proj = project(a) if found else None
    DecisionPolicy(spec, client=proj.client() if proj else policy_client(a))  # it binds to an allowed model
    where = place.absolute(a.root, "policy root") if a.root else proj.policies_dir if proj else None
    store = Policies(where) if where else None
    if a.check:
        if store is not None and spec.version <= (latest := max(store.versions(spec.task), default=0)):
            raise ConfigError(f"{spec.task} already has v{latest}; a new policy is v{latest + 1}")
        print(json.dumps({"policy": spec.ref, "valid": True}) if a.json else f"{spec.ref}: valid (binds to {spec.connection}); nothing written")
        return 0
    assert store is not None
    user = git.user(proj.root if proj else Path.cwd())
    if not user:
        raise S1flowError("adopt records who switched current: set git config user.name")
    previous = store.current(spec.task)
    store.write_new(spec, adopted=Switch(action="spec", version=spec.version, previous=previous, by=user, reason=a.reason))
    path = store.dir(spec.task) / f"v{spec.version}.json"
    out = {"policy": spec.ref, "previous": previous, "evaluated": False, "path": str(path)}
    print(json.dumps(out) if a.json else f"{spec.ref} (current, not evaluated): wrote {shown(path)}, channels.json, history.jsonl")
    return 0


def add(sub: Any) -> None:
    p = command(sub, "adopt", adopt, context=("project", "connections"))
    p.add_argument("task", nargs="?", help="the task")
    p.add_argument("candidate", nargs="?", help="the candidate, model[:version][/variant] as `s1flow report` names it")
    p.add_argument("--spec", type=Path, metavar="FILE", help="save this runtime spec as the next version, unevaluated, and make it current")
    p.add_argument("--root", type=Path, help="the policies directory, outside an s1flow project (an app's repository; with --connections for --spec)")
    p.add_argument("--reason", help="why (kept in history.jsonl, and for a candidate in vN.evaluation.json); needed unless --spec FILE --check")
    p.add_argument("--check", action="store_true", help="with --spec: validate the spec only (it binds to an allowed model); write nothing")
    p.add_argument("--force", action="store_true", help="write it even when the held-out test shows it below")
    p.add_argument("--json", action="store_true")
