"""`s1flow feedback record` (the base install) and `s1flow feedback measure` (s1flow[eval])."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .common import POLICY, Parser, command, label, load_env, policy_client, policy_root, project, project_root


def feedback_record(a: argparse.Namespace) -> int:
    from .. import policies

    load_env(project_root(a))
    policies.load(a.policy, client=policy_client(a), path=a.path, root=policy_root(a), log=a.log).feedback(a.decision_id, label(a.label))
    return 0


def feedback_measure(a: argparse.Namespace) -> int:
    """Each policy in production, from the feedback in its logs; with --add, the cases with a kept state added as
    labelled cases."""
    from ..eval import feedback as fb  # s1flow[eval]: the task, its cases and objectives
    from ..eval.task import load

    task = load(project(a), a.task)
    found = fb.read([Path(x) for x in a.logs])
    cs = fb.cases(task, found)
    prod = fb.production(task, cs, found.failed)
    added = fb.add(task, cs, write=a.add)
    if a.json:
        print(json.dumps({"production": [x.model_dump(mode="json") for x in prod], "added": added.model_dump(mode="json"), "issues": found.issues.model_dump(mode="json")}))
    else:
        print(fb.markdown(task, prod, added, issues=found.issues))
    return 1 if any(v.below for v in prod) else 0


def add(sub: Any) -> None:
    group = sub.add_parser("feedback", context=("project", "connections"), help="record the right answer for a case a policy decided (record), or measure policies in production (measure)").add_subparsers(
        dest="action", required=True, parser_class=Parser)
    f = command(group, "record", feedback_record, context=("project", "connections"), help="record the right answer for a case a policy decided",
                description="Record the right answer for a case, joined to its answer by decision_id (what `s1flow feedback measure` measures from).")
    f.add_argument("policy", metavar=POLICY, help="the policy that decided it (its id in the log, or the task: the current version)")
    f.add_argument("decision_id", help="the exact decision_id returned by decide")
    f.add_argument("label", help="the right answer: a class key, or true / false")
    f.add_argument("--log", required=True, help="the log to append to (JSONL)")
    f.add_argument("--path", help="a policy file, or a policy set from `s1flow export` (policies.json), instead of policies/ (as decide --path)")
    m = command(group, "measure", feedback_measure, context=("project", "connections"), help="measure each policy in production from the feedback in its logs (needs s1flow[eval])",
                description="Measure each policy in production from the feedback in its logs; with --add, also add the cases with a "
                            "kept state as labelled cases. Exit 1 when production is shown below. Needs s1flow[eval].")
    m.add_argument("task")
    m.add_argument("logs", nargs="+", help="SDK logs (JSONL) or OpenTelemetry JSON exports")
    m.add_argument("--add", action="store_true", help="also add the cases with a kept state and a valid label to tasks/<task>/feedback.jsonl")
    m.add_argument("--json", action="store_true")
