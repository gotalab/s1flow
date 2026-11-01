"""The `s1flow` console script: every command, in the standard library's argparse, one module per command
(cli/<command>.py: its function and its arguments); common.py is what they share.

Each command imports what it needs when it runs, so the base install (pydantic and httpx) runs init, decide,
feedback record, export, doctor, models and adopt --spec (models --verify draws images: s1flow[images]): an app or a workflow decides and
records feedback, and an agent makes a project and gets the Skill, without the evaluation stack. The other commands need s1flow[eval]; on the base
install they end in one line saying what to install, not a traceback. `s1flow --help` lists every command in one
table (HELP), and a command that does not exist is one line naming the closest.

    s1flow decide --model jev --state @issue.json --questions @qs.json        call a model (s1flow.client)
    s1flow decide --model jev --state @issue.json --boolean "Is it a bug report?"   one yes / no question
    s1flow decide --policy gh-ruff-area[@v3] --state @issue.json [--path policies.json] [--case-id] [--log [--keep-state]] [--github-output]
    s1flow feedback record gh-ruff-area@v3 DECISION_ID formatter --log log.jsonl   the right answer, once known
    s1flow feedback measure gh-ruff-area log.jsonl [--add]                   production from the logs (s1flow[eval])
    s1flow adopt --spec spec.json --reason "..." [--root policies] [--connections PATH]   save a spec as the next version, current
    s1flow adopt --spec spec.json --check [--connections PATH]          validate it (and its binding) only
    s1flow export [gh-ruff-area ...] --out policies.json                each task's current policy in one file, for an app to vendor
    s1flow doctor [--models jev,d1@vercel | --policy gh-ruff-area[@…] [--path policies.json]] [--reach] [--json]   the keys and hosts they need
    s1flow init --skill                                                 write the Agent Skill where agents read it (skill.py)

A policy is named TASK[@vN] wherever a command takes one (the current version when none is given), so its id
in a log (`gh-ruff-area@v3`) is input as it is. channels.json names the current version; the pull request that
changes it ships it when it merges. Only adopt points it (history.jsonl says why, each time).

Exit codes, the same for every command (EXITS), shown in every --help:

    0  done
    1  a gate failed or something was found: check fails, adopt or feedback measure shows the held-out test or
       production below, cases check finds a wrong case, doctor a key or host missing, models --verify a
       declared capability failing
    2  usage (an `error:` line naming the --help to read), configuration, could not run (an S1flowError), or
       check pending (answers needed that only a run with keys can get); a bug in s1flow prints its traceback too
"""

from __future__ import annotations

import argparse
import difflib
import sys
import traceback
import warnings
from typing import Any, NoReturn

from ..core import place
from ..core.errors import S1flowError
from . import adopt, cases, check, decide, doctor, export, feedback, init, models, optimize, report, run
from .common import EXITS, Parser, usage_error

BASE = ("init", "decide", "feedback", "export", "doctor", "models")  # what the base install runs (feedback record; adopt --spec; models without --verify)
# Every command, in the order `s1flow --help` lists it: its module (cli/<name>.py) and its line in that list.
COMMANDS = (
    (init, "init", "make a project in ./s1flow: s1flow.toml, a task with --task, the CI workflow with --ci, the Agent Skill with --skill"),
    (models, "models", "the line-up in s1flow.toml, and what --verify found each model takes"),
    (run, "run", "ask the models about a task's cases (cached): runs/<task>/"),
    (report, "report", "every model and question variant on the saved runs by the task's objective (--out DIR writes it); no TASK: every task's current version and why"),
    (adopt, "adopt", "write a candidate as the task's current policy, with why (merging the change ships it)"),
    (check, "check", "compare two versions on today's test cases, case by case (the CI gate)"),
    (optimize, "optimize", "optimize the current policy's question into a new candidate; it ships nothing (s1flow[optimize])"),
    (cases, "cases", "check a task's cases; review and correct their labels"),
    (decide, "decide", "call a model (--model), or decide with a task's policy (--policy)"),
    (feedback, "feedback", "record the right answer for a case a policy decided (record); measure policies in production (measure, s1flow[eval])"),
    (export, "export", "the policies an app uses, each task's current version, in one file (policies.json)"),
    (doctor, "doctor", "the keys and hosts the models need, and whether they are there"),
)
TABLE = tuple((name, what) for _, name, what in COMMANDS)
HELP = "\n".join([
    "usage: s1flow [--project PATH] [--connections PATH] COMMAND [ARGS]   (s1flow COMMAND --help for its arguments)", "",
    "--project PATH selects a project without changing cwd; --connections PATH selects one trusted connection file.",
    "Use these options only where listed by COMMAND --help; they also work before the command. SDK calls do not discover projects.", "", "Commands:",
    *(f"  {name:<16} {what}" for name, what in TABLE), "",
    "init, decide, feedback record, export, doctor, models and adopt --spec run on the base install (models --verify: s1flow[images]); "
    "the others need the eval extra: install s1flow[eval].",
    EXITS,
])


def unknown_command(name: str) -> NoReturn:
    """`s1flow polciy`: one line naming the closest command, exit 2."""
    close = difflib.get_close_matches(name, [n for n, _ in TABLE], n=1)
    usage_error(f"no command {name!r}" + (f"; did you mean {close[0]!r}?" if close else ""), "s1flow")


def notices() -> None:
    """A warning is one `notice:` line on stderr, without the file and line it was raised at."""
    def show(message: Warning | str, category: type[Warning], filename: str, lineno: int, file: Any = None, line: str | None = None) -> None:
        print(f"notice: {message}", file=sys.stderr)

    warnings.showwarning = show


def bug() -> NoReturn:
    """Anything that is not an S1flowError is a bug in s1flow: its traceback, then exit 2 (it could not run)."""
    traceback.print_exc()
    print("error: a bug in s1flow (the traceback above); please report it", file=sys.stderr)
    sys.exit(2)


def missing_extra(e: ModuleNotFoundError) -> str | None:
    """The one-line hint for an import an extra would have installed, else None."""
    from ..doctor import EXTRAS

    extra = EXTRAS.get((e.name or "").partition(".")[0])
    if extra is None:
        return None
    return f"error: this needs s1flow[{extra}] ({e}): install s1flow with the {extra} extra"


def _command_name(args: list[str]) -> str | None:
    """The command as typed, past the options that may come before it (--project, --connections)."""
    i = 0
    while i < len(args):
        if args[i] in ("--project", "--connections"):
            i += 2
        elif args[i].startswith("-"):
            i += 1
        else:
            return args[i]
    return None


def parser() -> argparse.ArgumentParser:
    ap = Parser(prog="s1flow", context=("project", "connections"), description="Run small model-backed decisions in your app and CI, then evaluate and improve them on your own data.")
    sub = ap.add_subparsers(dest="command", required=True, parser_class=Parser)
    for module, _, _ in COMMANDS:
        module.add(sub)
    return ap


def main(argv: list[str] | None = None) -> None:
    args = sys.argv[1:] if argv is None else argv
    first = args[0] if args else None
    if first in (None, "-h", "--help"):
        print(HELP)
        sys.exit(0 if first else 2)
    assert first is not None
    command = _command_name(args)
    if command is not None and command not in {name for name, _ in TABLE}:
        unknown_command(command)
    notices()
    a = parser().parse_args(args)
    try:
        for name in ("project", "connections"):
            value = getattr(a, name, None)
            setattr(a, name, place.absolute(value, name) if value is not None else None)
        code = a.run(a)
    except S1flowError as e:
        print(f"error: {e.args[0] if e.args else e}", file=sys.stderr)
        sys.exit(2)
    except KeyboardInterrupt:
        print("error: interrupted", file=sys.stderr)
        sys.exit(2)
    except ModuleNotFoundError as e:  # an extra this needs (s1flow[eval], s1flow[images], s1flow[llm], s1flow[optimize])
        if (hint := missing_extra(e)) is None:
            bug()
        print(hint + ("" if a.command in BASE else f"; {', '.join(BASE)} need only s1flow"), file=sys.stderr)
        sys.exit(2)
    except Exception:
        bug()
    sys.exit(code)
