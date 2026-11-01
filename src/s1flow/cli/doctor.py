"""`s1flow doctor`: the keys and hosts the models need, and whether they are there. The base install runs it."""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

from ..core.errors import ConfigError
from .common import POLICY, client, command, load_env, policy_client, policy_root, project_root


def doctor(a: argparse.Namespace) -> int:
    from .. import doctor as checking
    from .. import policies, skill

    if a.models and a.policy:
        raise ConfigError("doctor takes --models or --policy, not both")
    if a.path and not a.policy:
        raise ConfigError("--path names where --policy is read from: it goes with --policy")
    root = project_root(a)
    before = {k for k, v in os.environ.items() if v}
    load_env(root)
    from_dotenv = {k for k, v in os.environ.items() if v and k not in before}
    if a.policy:
        runtime = policies.load(a.policy, client=policy_client(a), path=a.path, root=policy_root(a))
        r = runtime.spec
        report = checking.check(f"policy {r.ref}", [(r.connection, runtime.model_spec)],
                                env=dict(os.environ), from_dotenv=from_dotenv, probe=a.reach)
    else:
        models = client(a, root).connections
        lineup = models.lineup
        names = [n for n in a.models.split(",") if n] if a.models else lineup.default
        for n in names:
            lineup.resolved(n)
        source = f"{models.path or 's1flow.toml'}" + ("" if a.models else " (its default)")
        report = checking.check(source, [(n, lineup.spec(n.partition(":")[0])) for n in names],
                                env=dict(os.environ), from_dotenv=from_dotenv, probe=a.reach)
    old_skills = skill.stale()
    if a.json:
        print(json.dumps({**report.as_json(), "skill": old_skills}, indent=1))
    else:
        print(checking.render(report), flush=True)
        for line in old_skills:
            print(f"skill: {line}")
        for problem in report.problems:
            print(f"problem: {problem}", file=sys.stderr)
    return 1 if report.problems else 0


def add(sub: Any) -> None:
    doc = command(sub, "doctor", doctor, context=("project", "connections"), help="the keys and hosts the models need, and whether they are there",
                  description="For each model, the environment variables its provider reads (set or not; never a value) and the hosts "
                              "it calls (for a sandbox's allow-list). Exit 0 when everything needed is there, 1 otherwise, one line per problem.")
    doc.add_argument("--models", help="comma-separated names from s1flow.toml (default: its `default`)")
    doc.add_argument("--policy", metavar=POLICY, help="the model of this policy (the current version when no @ is given)")
    doc.add_argument("--path", help="with --policy: a policy file, or a policy set from `s1flow export` (policies.json), instead of policies/ (as decide --path)")
    doc.add_argument("--reach", action="store_true", help="also send one plain HTTPS request per host, without a key (no model is called)")
    doc.add_argument("--json", action="store_true")
