"""The `s1flow` console script: every command, in the standard library's argparse.

Each command imports what it needs when it runs, so the base install (pydantic and httpx) runs init, decide,
feedback record, policy, doctor, skill, guide, and adopt TASK@vN and adopt --spec: an app or a workflow decides and
records feedback, and an agent makes a project and gets the Skill, without the evaluation stack. The other commands need s1flow[eval]; on the base
install they end in one line saying what to install, not a traceback. `s1flow --help` lists every command in one
table (HELP), and a command that does not exist is one line naming the closest.

    s1flow decide --model jev --state @issue.json --questions @qs.json        call a model (s1flow.client)
    s1flow decide --model jev --state @issue.json --boolean "Is it a bug report?"   one yes / no question
    s1flow decide --policy gh-ruff-area[@v3] --state @issue.json [--path policies.json] [--case-id] [--log [--keep-state]] [--github-output]
    s1flow feedback record gh-ruff-area@v3 DECISION_ID formatter --log log.jsonl   the right answer, once known
    s1flow feedback measure gh-ruff-area log.jsonl [--dry-run]               production from the logs (s1flow[eval])
    s1flow policy create spec.json --reason "..." [--root policies] [--connections PATH] [--check]   adopt --spec, with --root (--check: validate only)
    s1flow policy export [gh-ruff-area ...] --out policies.json        each task's current policy in one file, for an app to vendor
    s1flow doctor [--models jev,d1@vercel | --policy gh-ruff-area[@…]] [--reach] [--json]   the keys and hosts they need
    s1flow skill install [--dir PATH ...] [--user] [--force]    write the Agent Skill where agents read it (skill.py)
    s1flow skill path                                           the package's own copy
    s1flow guide [topic]                                        print the Skill's routing table, or one reference

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
import json
import os
import sys
import traceback
import unicodedata
import warnings
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, NoReturn, TypeVar, cast

from .core import envfile, place
from .core.errors import ConfigError, NotFound, S1flowError

if TYPE_CHECKING:
    from .client import Client, Response
    from .client.answers import Answer
    from .client.state import State
    from .policies import Policies
    from .policies.file import PolicySpec
    from .project import Project

EXITS = "Exit codes: 0 done; 1 a gate failed or something was found (check fails, doctor or models --verify finds a problem); 2 usage, configuration, could not run, or check pending."
BASE = ("init", "decide", "feedback", "policy", "doctor", "skill", "guide")  # what the base install runs (feedback record)
# Every command, as `s1flow --help` lists it.
TABLE = (
    ("init", "make a project in ./s1flow: s1flow.toml, a task with --task, the CI workflow with --ci"),
    ("tasks", "every task: its current policy, its candidate, the model id that answers, pinned or not"),
    ("models", "the line-up in s1flow.toml, and what --verify found each model takes"),
    ("run", "ask the models about a task's cases (cached): runs/<task>/"),
    ("report", "every model and question variant on the saved runs, best first by the task's objective; --out DIR writes it"),
    ("adopt", "write a candidate as the task's current policy, with why (merging the change ships it)"),
    ("check", "compare two versions on today's test cases, case by case (the CI gate)"),
    ("optimize", "optimize the current policy's question into a new candidate; it ships nothing (s1flow[optimize])"),
    ("cases", "check a task's cases; review and correct their labels"),
    ("decide", "call a model (--model), or decide with a task's policy (--policy)"),
    ("feedback", "record the right answer for a case a policy decided (record); measure policies in production (measure, s1flow[eval])"),
    ("policy", "runtime specifications: check and save one (create), the ones an app uses in one file (export)"),
    ("doctor", "the keys and hosts the models need, and whether they are there"),
    ("skill", "write the Agent Skill where agents read it (install), or print where the package's copy is (path)"),
    ("guide", "print the Skill's routing table, or one topic (s1flow guide cli: exit codes, --json, names)"),
)
HELP = "\n".join([
    "usage: s1flow [--project PATH] [--connections PATH] COMMAND [ARGS]   (s1flow COMMAND --help for its arguments)", "",
    "--project PATH selects a project without changing cwd; --connections PATH selects one trusted connection file.",
    "Use these options only where listed by COMMAND --help; they also work before the command. SDK calls do not discover projects.", "", "Commands:",
    *(f"  {name:<16} {what}" for name, what in TABLE), "",
    "init, decide, feedback record, policy, doctor, skill and guide run on the base install; "
    "the others need the eval extra: install s1flow[eval].",
    EXITS,
])


GITHUB_SCRIPT = "the Skill's script, python .agents/skills/s1flow/scripts/github.py (s1flow skill install writes it)"
RENAMED = {  # commands renamed or removed: none runs under its old name, the error names what replaces it
    "propose": "`report` (the list) or `adopt` (write the one picked)", "improve": "`optimize TASK`", "gh": GITHUB_SCRIPT,
    "github": GITHUB_SCRIPT, "compare": "`report`", "rank": "`report`",
    "promote": "`adopt` (it makes the version current; merging that change ships it)",
    "data": "`cases`", "release": "`policy`", "record-feedback": "`feedback record`",
}

REMOVED_ACTIONS = {  # subcommands removed after 0.1.0a1, by what replaces them
    ("policy", "validate"): "`s1flow policy create FILE --check` (with --connections to check the binding)",
    ("optimize", "prompt"): "`s1flow optimize TASK`",
}

T = TypeVar("T")


# ---------- the frame every command runs in ----------


def unknown_command(name: str) -> NoReturn:
    """`s1flow polciy`: one line naming the closest command, exit 2 (a renamed one: its new name, never a near spelling)."""
    if name in RENAMED:
        usage_error(f"no command {name!r}: it is now {RENAMED[name]}", "s1flow")
    close = difflib.get_close_matches(name, [n for n, _ in TABLE], n=1)
    usage_error(f"no command {name!r}" + (f"; did you mean {close[0]!r}?" if close else ""), "s1flow")


def usage_error(message: str, command: str) -> NoReturn:
    print(f"error: {message} (see {command} --help)", file=sys.stderr)
    sys.exit(2)


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


class Parser(argparse.ArgumentParser):
    """argparse with a usage error as one `error:` line (exit 2) and the exit codes in every --help."""

    def __init__(self, *args: Any, **kw: Any) -> None:
        context: tuple[str, ...] = kw.pop("context", ())
        kw.setdefault("epilog", EXITS)
        super().__init__(*args, **kw)
        if "project" in context:
            self.add_argument("--project", type=Path, default=argparse.SUPPRESS, metavar="PATH",
                              help="use this project directory (or its s1flow/ child); other relative paths stay relative to the invocation directory")
        if "connections" in context:
            self.add_argument("--connections", type=Path, default=argparse.SUPPRESS, metavar="PATH",
                              help="trusted connection configuration; required explicitly for policy execution")
        self.set_defaults(prog_=self.prog, context_options=context)  # the innermost command parsed, for the hint

    def parse_args(self, args: Any = None, namespace: Any = None) -> Any:
        a, extra = self.parse_known_args(args, namespace)
        if any(value == "--models-file" or value.startswith("--models-file=") for value in extra):
            usage_error("--models-file was renamed to --connections PATH", a.prog_)
        for name in ("project", "connections"):
            option = f"--{name}"
            supplied = hasattr(a, name) or any(value == option or value.startswith(option + "=") for value in extra)
            if supplied and name not in a.context_options:
                usage_error(f"{option} does not apply to {a.prog_}; remove this option", a.prog_)
        if extra:
            usage_error(f"unrecognized arguments: {' '.join(extra)}", a.prog_)
        return a

    def error(self, message: str) -> NoReturn:
        usage_error(message, self.prog)


def missing_extra(e: ModuleNotFoundError) -> str | None:
    """The one-line hint for an import an extra would have installed, else None."""
    from .doctor import EXTRAS

    extra = EXTRAS.get((e.name or "").partition(".")[0])
    if extra is None:
        return None
    return f"error: this needs s1flow[{extra}] ({e}): install s1flow with the {extra} extra"


POLICY = "TASK[@vN]"  # how a command names a policy (policies.file.Ref)


def positive(text: str) -> int:
    n = int(text)
    if n < 1:
        raise argparse.ArgumentTypeError(f"{n} is not 1 or more")
    return n


def _command_words(args: list[str]) -> list[str]:
    """The command, its subcommand and the next word as typed, past the options that may come before them
    (--project, --connections)."""
    words: list[str] = []
    i = 0
    while i < len(args) and len(words) < 3:
        x = args[i]
        if x in ("--project", "--connections"):
            i += 2
            continue
        if x.startswith("-"):
            if words:  # an option of the command itself: what follows is its value or its arguments
                break
            i += 1
            continue
        words.append(x)
        i += 1
    return words


def main(argv: list[str] | None = None) -> None:
    args = sys.argv[1:] if argv is None else argv
    first = args[0] if args else None
    if first in (None, "-h", "--help"):
        print(HELP)
        sys.exit(0 if first else 2)
    assert first is not None
    words = _command_words(args)
    if words and words[0] not in {name for name, _ in TABLE}:
        unknown_command(words[0])
    # `optimize prompt` alone optimizes a task named prompt; only `optimize prompt TASK` is the removed form
    removed = len(words) == 3 if words[:2] == ["optimize", "prompt"] else True
    if removed and (gone := REMOVED_ACTIONS.get(tuple(words[:2]))) is not None:  # type: ignore[arg-type]
        usage_error(f"no command {' '.join(words[:2])}: it is now {gone}", f"s1flow {words[0]}")
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


# ---------- what the commands share ----------


def project(a: argparse.Namespace) -> Project:
    from .project import Project

    root = _project_root(a, required=True)
    assert root is not None
    _load_env(root)
    return Project(root, connections=_connections_path(a) if "connections" in a.context_options else None)


def _json(arg: str, what: str) -> Any:
    """JSON as given, or `@file.json`."""
    try:
        return json.loads(Path(arg[1:]).read_text() if arg.startswith("@") else arg)
    except (OSError, ValueError) as e:
        raise ConfigError(f"{what}: {e}") from None


def _load_env(root: Path | None) -> None:
    """Keys from the project's .env files (core/envfile.py), as the evaluation commands read them."""
    envfile.load(root or Path.cwd())


def _project_root(a: argparse.Namespace, *, required: bool = False) -> Path | None:
    return place.project(getattr(a, "project", None), required=required)


def _connections_path(a: argparse.Namespace) -> Path | None:
    value = getattr(a, "connections", None)
    if value is not None:
        return place.absolute(value, "connections")
    if value := os.environ.get("S1FLOW_CONNECTIONS"):
        return place.absolute(value, "S1FLOW_CONNECTIONS")
    return None


def _client(a: argparse.Namespace, root: Path | None) -> Client:
    from .client import Client

    config = _connections_path(a)
    if config is None and root is not None:
        config = root / place.CONFIG
    if config is None:
        raise ConfigError(f"no connections configured in {Path.cwd()}; use --connections PATH, S1FLOW_CONNECTIONS, "
                          "or --project PATH; run s1flow init to create a project")
    return Client(connections=config)


def _policy_client(a: argparse.Namespace) -> Client:
    """Policy execution explicitly grants the connections in this invocation's file."""
    from .client import Client

    if not getattr(a, "connections", None):
        raise ConfigError("policy execution needs --connections PATH: a trusted file listing only the allowed connections; "
                          "S1FLOW_CONNECTIONS does not grant policy execution")
    return Client(connections=a.connections)


def _policy_root(a: argparse.Namespace) -> Path | None:
    if getattr(a, "path", None) is not None:
        return None
    explicit = getattr(a, "root", None)
    if explicit is not None:
        return place.absolute(explicit, "policy root")
    root = _project_root(a, required=True)
    assert root is not None
    return root / "policies"


def _guard(f: Callable[[], T], on_error: Callable[[str], None]) -> T:
    """Run f; on an S1flowError, let `on_error` record why (e.g. for the PR) before it exits 2."""
    try:
        return f()
    except S1flowError as e:
        on_error(str(e.args[0] if e.args else e))
        raise


def _shown(path: Path) -> str:
    """A path from where the command ran, when it is below it."""
    return str(path.relative_to(Path.cwd())) if path.is_relative_to(Path.cwd()) else str(path)


def _questions(a: argparse.Namespace) -> dict[str, Any] | None:
    """--questions JSON, or the one yes / no question --boolean asks (named q)."""
    from .client.questions import Boolean

    if a.boolean is not None and a.questions:
        raise ConfigError("give the questions once: --questions, or --boolean")
    if a.boolean is not None:
        return {"q": Boolean(instructions=a.boolean)}
    return _json(a.questions, "--questions") if a.questions else None


def _state(a: argparse.Namespace) -> State:
    from .client import images
    from .client.state import has_unprepared_image
    from .core.errors import DataError

    state: Any = _json(a.state, "--state") if a.state is not None else None
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
    from .client.answers import BooleanAnswer, BoxAnswer, ChoiceAnswer, ScoreAnswer

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


# ---------- decide, feedback, policy, doctor, skill, guide (the base install) ----------


def decide(a: argparse.Namespace) -> int:
    if a.policy is not None and not a.policy.strip():
        raise ConfigError(f"--policy is empty: name a policy, {POLICY}")
    if (a.model is None) == (a.policy is None):
        raise ConfigError("decide takes --model (call a model) or --policy (decide with a policy), one of them")
    root = _project_root(a)
    _load_env(root)
    if a.policy:
        return _decide_policy(a)
    state = _state(a)
    qs = _questions(a)
    if not qs:
        raise ConfigError('decide --model needs questions: --questions @qs.json ({"area": {"type": "choice", ...}}), or --boolean TEXT')
    client = _policy_client(a) if a.connections else _client(a, root)
    client.connections.resolved(a.model)  # a wrong name or version lists the right ones before a key is read
    d = client.responses.create(model=a.model, state=state, questions=qs)
    if a.json:
        print(d.model_dump_json(indent=1))
    else:
        _print_response(d)
    return 0


def _decide_policy(a: argparse.Namespace) -> int:
    from . import policies

    if a.questions or a.boolean is not None:
        raise ConfigError("a policy asks its own question: leave out --questions and --boolean")
    out = os.environ.get("GITHUB_OUTPUT")
    if a.github_output and not out:
        raise S1flowError("--github-output needs $GITHUB_OUTPUT (set by GitHub Actions)")
    if a.keep_state and not a.log:
        raise ConfigError("--keep-state keeps the state in the log: give --log too")
    r = policies.load(a.policy, client=_policy_client(a), path=a.path, root=_policy_root(a), log=a.log, keep_state=a.keep_state).decide(_state(a), case_id=a.case_id)
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


def feedback_record(a: argparse.Namespace) -> int:
    from . import policies

    _load_env(_project_root(a))
    value: Any = {"true": True, "false": False}.get(a.label.lower(), a.label)
    policies.load(a.policy, client=_policy_client(a), path=a.path, root=_policy_root(a), log=a.log).feedback(a.decision_id, value)
    return 0


def feedback_measure(a: argparse.Namespace) -> int:
    """Each policy in production, from the feedback in its logs; the cases with a kept state added as labelled cases."""
    from .eval import feedback as fb  # s1flow[eval]: the task, its cases and objectives
    from .eval.task import load

    task = load(project(a), a.task)
    found = fb.read([Path(x) for x in a.logs])
    cs = fb.cases(task, found)
    prod = fb.production(task, cs, found.failed)
    added = fb.add(task, cs, a.dry_run)
    if a.json:
        print(json.dumps({"production": [x.model_dump(mode="json") for x in prod], "added": added.model_dump(mode="json"), "issues": found.issues.model_dump(mode="json")}))
    else:
        print(fb.markdown(task, prod, added, issues=found.issues))
    return 1 if any(v.below for v in prod) else 0



def policy_create(a: argparse.Namespace) -> int:
    """Validate a runtime specification and save it as the task's current version (never overwriting a version);
    --check validates only. With --connections, also check that it binds to a model in that file (no model is called)."""
    from .integrations import git
    from .policies import DecisionPolicy, Policies
    from .policies.file import read_file

    spec = read_file(a.file)
    if a.connections:
        DecisionPolicy(spec, client=_policy_client(a))
    if a.check:
        result = {"status": "valid", "policy": spec.ref, "policy_digest": spec.digest, "binding_checked": bool(a.connections)}
        print(json.dumps(result) if a.json else f"valid {spec.ref}; connection {'checked' if a.connections else 'not checked'}")
        return 0
    if not a.reason:
        raise S1flowError("policy create makes the version current: give --reason (it is adopt --spec FILE --reason)")
    store = Policies(a.root)
    _adopt_spec(store, spec, git.user(Path.cwd()) or "s1flow policy create", a.reason)
    path = store.dir(spec.task) / f"v{spec.version}.json"
    result = {"status": "created", "policy": spec.ref, "policy_digest": spec.digest, "path": str(path), "current": True}
    print(json.dumps(result) if a.json else f"created {spec.ref}: {path} (not evaluated), now current")
    return 0


def policy_export(a: argparse.Namespace) -> int:
    from . import policies
    from .policies import policy_set
    from .policies.file import policy_id

    root = _policy_root(a)
    assert root is not None
    b = policy_set.export(root, a.tasks or None)
    Path(a.out).write_text(b.dump())
    for task, e in b.policies.items():
        print(f"{policy_id(task, e.version)} (current) sha256:{e.digest[:12]}")
    print(f"wrote {a.out}: load with policies.load(<task>, path={a.out!r})")
    return 0


def doctor(a: argparse.Namespace) -> int:
    from . import doctor as checking
    from . import policies, skill

    if a.models and a.policy:
        raise ConfigError("doctor takes --models or --policy, not both")
    root = _project_root(a)
    before = {k for k, v in os.environ.items() if v}
    _load_env(root)
    from_dotenv = {k for k, v in os.environ.items() if v and k not in before}
    if a.policy:
        runtime = policies.load(a.policy, client=_policy_client(a), root=_policy_root(a))
        r = runtime.spec
        report = checking.check(f"policy {r.ref}", [(r.connection, runtime.model_spec)],
                                env=dict(os.environ), from_dotenv=from_dotenv, probe=a.reach)
    else:
        models = _client(a, root).connections
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


def skill_install(a: argparse.Namespace) -> int:
    from . import skill

    dirs = [Path(d) for d in a.dir or []]
    for target in skill.targets(dirs, a.user):
        for line in skill.lines(skill.install(target, force=a.force)):
            print(line)
    return 0


def skill_path(a: argparse.Namespace) -> int:
    from . import skill

    print(skill.source())
    return 0


def guide(a: argparse.Namespace) -> int:
    from . import skill

    print(skill.guide(a.topic), end="")
    return 0


# ---------- the evaluation (s1flow[eval]) ----------


def init(a: argparse.Namespace) -> int:
    """Make a project in ./s1flow: s1flow.toml, a task, .gitignore, and with --ci the CI workflow. Nothing outside the
    project unless asked: the Agent Skill comes from the plugin, or `s1flow skill install`."""
    from .project import scaffold

    for line in scaffold.init(Path.cwd() / a.dir, a.task, workflow=a.ci):
        print(line)
    return 0


def tasks(a: argparse.Namespace) -> int:
    """Every task and what runs in production: its current policy, its candidate (model[:version][/variant]), the
    model id that answers, and whether that version is pinned."""
    from .eval.policy import overview

    found = overview(project(a), a.tasks or None)
    if a.json:
        print(json.dumps([t.model_dump(mode="json") for t in found], indent=1))
        return 0
    table = [["task", "current", "candidate", "model version", "answered by", "pin"]]
    for t in found:
        rows = [[t.task, r.policy, r.candidate or "-", r.model_version or "-", r.answered_by or "-", r.pin or "?"]
                for r in t.policies if r.current]
        table += rows or [[t.task, "-", "-", "-", "-", "-"]]
    widths = [max(len(row[i]) for row in table) for i in range(len(table[0]))]
    for row in table:
        print("  ".join(x.ljust(w) for x, w in zip(row, widths)).rstrip())
    print("pin: yes the policy sends a version by its name; no its model serves one version; alias the model's version "
          "can change; ? s1flow.toml no longer has the model. Every version, its date and digest: s1flow tasks --json.")
    return 0


def models(a: argparse.Namespace) -> int:
    """The line-up: what each model declares (s1flow.toml) next to what --verify found (models.verified.json)."""
    from .eval import verify as verifying

    p = project(a)
    if a.verify:
        names, unset = verifying.asked(p, a.models.split(",") if a.models else None)
        for u in unset:  # a missing key says nothing about the model: nothing is recorded
            print(f"{u.name}  not checked (no {', '.join(u.keys)})" + (f": {u.get}" if u.get else ""))
        found = verifying.verify(p, names)
        if not found:
            print("nothing checked: set the keys above (s1flow doctor), then run it again")
            return 2
        for f in found:
            print(f"{f.name}  ({f.answered_by or 'no answer'})")
            for c, mark, detail in f.checks:
                print(f"  {c:<8} {mark:<20} {detail}")
            if f.price is not None:
                print(f"  {'price':<8} {f.price[0]:<20} {f.price[1]}")
        print(f"saved to {verifying.verified_path(p)}" + (f" ({len(unset)} not checked)" if unset else ""))
        return 1 if any(f.failed for f in found) else 0
    rows = verifying.lineup(p)
    if a.json:
        print(json.dumps(rows, ensure_ascii=False, indent=1))
        return 0
    cols = list(rows[0])
    width = {c: max(len(c), *(len(r[c]) for r in rows)) for c in cols}
    print("  ".join(c.ljust(width[c]) for c in cols))
    for row in rows:
        print("  ".join(row[c].ljust(width[c]) for c in cols))
    print("\n✓ declared, verified   ✓? declared, not verified yet   ✗! declared, verification failed   + works, not declared   · not taken")
    print(f"declared in {p.config}, verified in {verifying.verified_path(p)}")
    return 0


def run(a: argparse.Namespace) -> int:
    """Ask the candidates about a task's cases (cached) and write runs/<task>/<variant>/<model[:version]>.jsonl; the first
    run on a task also fixes its held-out test share (tasks/<task>/split.json), the one command that writes it."""
    import asyncio

    from .eval import evalset
    from .eval import run as running
    from .eval.task import load

    p = project(a)
    names = a.models.split(",") if a.models else [m.name for m in p.client().connections.list(default_only=True)]
    task = load(p, a.task)
    running.candidates(task, names)  # every name checked before the split is written
    if note := evalset.fix(task):
        print(f"notice: {note}", file=sys.stderr)
    stats = asyncio.run(running.run(task, names, fresh=a.fresh, concurrency=a.concurrency))
    print(json.dumps(stats, indent=1))
    return 0


def report(a: argparse.Namespace) -> int:
    """Read the saved runs by the task's objective: every candidate on every question variant, best first, the
    ranking's pick marked. No model is called and nothing is written but, with --out DIR, the comparison snapshot and a
    Markdown report per question. --from reads a saved snapshot offline."""
    from .eval import adopt as adopting
    from .eval import comparison
    from .eval import report as reporting
    from .eval.task import load

    if a.offset < 0:
        raise ConfigError("--offset is 0 or more")
    if a.from_path and a.task:
        raise ConfigError("report takes TASK or --from PATH, not both")
    snapshot = Path(a.from_path) if a.from_path else None
    task, listed, unranked = None, None, None
    if snapshot is not None:
        for option in ("project", "connections"):
            if getattr(a, option, None) is not None:
                raise ConfigError(f"--{option} does not apply with --from; the saved snapshot is self-contained")
        if a.out:
            raise ConfigError("--out writes a report of the current runs; with --from the snapshot is already saved")
    else:
        if not a.task:
            raise ConfigError("report needs TASK, or --from PATH")
        task = load(project(a), a.task)
        if a.candidate is None:
            try:
                listed = adopting.shortlist(task)
            except ConfigError:
                raise
            except S1flowError as e:  # nothing to rank yet (no complete runs, a question no policy ships): still show what there is
                unranked = str(e.args[0] if e.args else e)
    shown = str(snapshot) if snapshot else None
    result = None
    if snapshot is not None:
        result = comparison.read(snapshot)
    else:
        assert task is not None
        result = comparison.collect(task, include_charts=bool(a.out))

    if a.out:
        assert task is not None and result is not None
        out = Path(a.out)
        if out.exists() and not out.is_dir():
            raise ConfigError(f"--out takes a directory; {out} is a file")
        out.mkdir(parents=True, exist_ok=True)
        (out / "comparison.json").write_text(result.model_dump_json(by_alias=True, indent=1) + "\n")
        wrote = [out / "comparison.json"]
        for variant in ["base", *task.variants]:
            if reporting.available_models(task, variant):
                reporting.write(task, variant, out / "questions")  # apart from comparison.json, whatever a variant is named
                wrote += [out / "questions" / f"{variant}.md", out / "questions" / f"{variant}.json"]
        print("wrote " + ", ".join(_shown(p) for p in wrote), file=sys.stderr)

    if a.candidate:
        assert result is not None
        if a.json:
            print(json.dumps(comparison.summary(result, candidate=a.candidate, snapshot=shown), ensure_ascii=False, indent=1))
        else:
            print(comparison.text(result, candidate=a.candidate, snapshot=shown))
        return 0
    if a.json:
        assert result is not None
        payload = comparison.summary(result, offset=a.offset, limit=a.limit, snapshot=shown)
        if task is not None:  # the ranking: the candidates ordered by the task's objectives and constraints
            payload["ranking"] = None if listed is None else [r.model_dump(mode="json") for r in listed.rows()[a.offset:a.offset + a.limit]]
            if unranked:
                payload["unranked"] = unranked
        print(json.dumps(payload, ensure_ascii=False, indent=1))
        return 0
    if listed is not None:
        assert task is not None and result is not None
        rows = listed.rows()
        _print_shortlist(task.id, rows[a.offset:a.offset + a.limit])
        if len(rows) > a.offset + a.limit:
            print(f"  … {len(rows) - a.offset - a.limit} more: --offset {a.offset + a.limit}")
        ranked = {r.candidate for r in rows}
        if left := [f"{r.candidate} ({', '.join(r.excluded) or 'incomplete'})" for r in result.candidates if r.candidate not in ranked]:
            print(f"not ranked: {'; '.join(left)}")
        if outside := [f"{r.candidate} ({', '.join(r.excluded)})" for r in rows if r.excluded]:
            print(f"outside the constraints: {'; '.join(outside)}")
        _print_weights(listed)
        print(f"Every metric of each candidate: s1flow report {task.id} --json, or --candidate NAME; "
              f"the snapshot and a Markdown report: s1flow report {task.id} --out DIR")
        return 0
    assert result is not None
    print(comparison.text(result, offset=a.offset, limit=a.limit, snapshot=shown))
    if unranked:
        print(f"not ranked: {unranked}")
    return 0


def _print_shortlist(task_id: str, rows: list[Any]) -> None:
    from .eval.shown import ms, pct, usd

    def score(s: Any) -> str:
        if s.value is None:
            return "-"
        f: Callable[[float], str] = (lambda v: pct(v, 1, sign="")) if s.objective.unit == "share" else (lambda v: f"{v:.3g}")
        return f(s.value) if s.interval is None else f"{f(s.value)} [{f(s.interval[0])}, {f(s.interval[1])}]"

    def cost(v: float | None, source: str | None) -> str:
        return "-" if v is None else "free" if v == 0 else ("~" if source in ("list", "mixed") else "") + usd(v, 2)

    tied = [r for r in rows if r.tied]
    labels = [s.objective.label for s in rows[0].scores] if rows else []
    # the objectives (measured on the answers) | what the calls took | the model
    head = ["", "candidate", "n", *labels, "|", "p50", "p90", "p99", "API $/10k", "|", "pin", "limit"]
    table = [head]
    for r in rows:
        if r.excluded:
            continue
        lat = r.calls.latency
        table.append(["*" if r.recommended else "=" if r.tied else "", r.candidate, str(r.n), *(score(s) for s in r.scores), "|",
                      ms(lat and lat.p50_ms), ms(lat and lat.p90_ms), ms(lat and lat.p99_ms), cost(r.calls.cost_per_10k_usd, r.calls.cost_source), "|",
                      r.pin, "" if r.per_minute is None else f"{r.per_minute}/min"])
    def width(c: str) -> int:  # a CJK character takes two columns
        return sum(2 if unicodedata.east_asian_width(ch) in "WF" else 1 for ch in c)

    widths = [max(width(row[i]) for row in table) for i in range(len(head))]
    print(f"{task_id}: {len(table) - 1} candidates within the constraints, {len(tied)} tied on the primary objective (=), the ranking's pick (*)")
    for row in table:
        print("  " + "  ".join(c + " " * (w - width(c)) for c, w in zip(row, widths)).rstrip())
    for r in rows:
        if r.excluded:
            print(f"  excluded: {r.candidate} ({', '.join(r.excluded)})")
    print("Measured on train + val; the held-out test is read only for the one you pick. Left of the first |: the objectives, "
          "measured on the answers (n: the labelled train + val cases it answered); then latency per call and API cost per 10,000 cases, measured on the calls. "
          "pin: yes a version, no a model that serves one, alias a model whose version can change (not adoptable: run name:<version>).")
    if refused := [r for r in rows if r.refused]:
        print("refused: " + ", ".join(f"{r.candidate} {r.refused} cases" for r in refused)
              + ": the model's limit (a refusal or an input it does not take), not a failed call; left out of its n.")
    if any(r.calls.cost_source in ("list", "mixed") for r in rows):
        print("~$: an estimated API cost, recorded tokens times s1flow.toml's list price, not a bill"
              + ("; billed API costs are listed beside them, so compare with care." if any(r.calls.cost_source == "billed" for r in rows) else "."))
    print(f'Adopt one: s1flow adopt {task_id} <candidate> --reason "..."')


def _print_weights(listed: Any) -> None:
    """ExpectedLoss or a loss table as the objective: the pick with its weights halved and doubled."""
    from .eval.weights import decides

    if not listed.reweighted:
        return
    now = listed.recommended if listed.fits else None
    for r in listed.reweighted:
        print(f"weights x{r.factor:g} ({r.objective.label}): the ranking's pick {r.recommended or '-'}, tied {', '.join(r.tied) or '-'}")
    print("The pick moves with the weights: they decide it, and they are yours to set." if decides(now, listed.reweighted)
          else "Halving or doubling the weights leaves the pick as it is.")


def _adopt_spec(store: Policies, spec: PolicySpec, by: str, reason: str) -> int | None:
    """Save a runtime spec as its task's next version, unevaluated, and make it current (adopt --spec, policy
    create); returns the version current pointed at before."""
    from .policies.history import Switch

    previous = store.current(spec.task)
    store.write_new(spec, adopted=Switch(action="spec", version=spec.version, previous=previous, by=by, reason=reason))
    return previous


def _adopt_without_evaluation(a: argparse.Namespace) -> int:
    """adopt TASK@vN (point current at a saved version) or adopt --spec FILE (save a runtime spec as the next
    version, unevaluated, and point current at it): no model is called and nothing is measured."""
    from .integrations import git
    from .policies import DecisionPolicy, Policies
    from .policies.file import Ref, read_file
    from .policies.history import Switch

    if a.candidate or a.force:
        raise S1flowError("adopt TASK@vN and adopt --spec take no candidate and no --force: nothing is measured")
    # In an s1flow project its policies/ and s1flow.toml; in an app's repository, --root and --connections.
    proj = None if a.root else project(a)
    store = Policies(place.absolute(a.root, "policy root") if a.root else proj.policies_dir)  # type: ignore[union-attr]
    user = git.user(proj.root if proj else Path.cwd())
    if not user:
        raise S1flowError("adopt records who switched current: set git config user.name")
    if a.spec:
        if a.task:
            raise S1flowError("adopt --spec FILE takes no TASK: the spec names its task and version")
        spec = read_file(a.spec)
        DecisionPolicy(spec, client=proj.client() if proj else _policy_client(a))  # it binds to an allowed model
        previous = _adopt_spec(store, spec, user, a.reason)
        path = store.dir(spec.task) / f"v{spec.version}.json"
        out = {"policy": spec.ref, "previous": previous, "evaluated": False, "path": str(path)}
        print(json.dumps(out) if a.json else f"{spec.ref} (current, not evaluated): wrote {_shown(path)}, channels.json, history.jsonl")
        return 0
    ref = Ref.parse(a.task)
    if ref.version is None:
        raise S1flowError(f"a rollback names the version: adopt {ref.task}@vN --reason \"...\"")
    previous = store.current(ref.task)
    if previous == ref.version:
        raise S1flowError(f"{ref.task}@v{ref.version} is already current")
    store.switch(ref.task, Switch(action="rollback", version=ref.version, previous=previous, by=user, reason=a.reason))
    out = {"policy": f"{ref.task}@v{ref.version}", "previous": previous, "evaluated": None, "path": None}
    print(json.dumps(out) if a.json else f"{ref.task}@v{ref.version} (current, from v{previous}): wrote channels.json, history.jsonl")
    return 0


def adopt(a: argparse.Namespace) -> int:
    """Switch the task's current policy, with why (who: git config user.name; history.jsonl keeps each switch): to a
    measured candidate (TASK CANDIDATE), to an older version (TASK@vN, a rollback), or to a runtime spec saved
    unevaluated (--spec FILE; these two need only the base install). The pull request that carries it ships it when
    it merges. A candidate the held-out test shows below is not written (exit 1) unless --force."""
    a.reason = a.reason.strip()
    if not a.reason:
        raise S1flowError("adopt records why: give --reason a sentence")
    if a.spec or "@" in (a.task or "") or a.root:
        return _adopt_without_evaluation(a)
    if not a.task or not a.candidate:
        raise S1flowError("adopt takes TASK CANDIDATE, TASK@vN (a rollback) or --spec FILE")
    from .eval import adopt as adopting
    from .eval.task import load
    from .integrations import git

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
             + _shown(d / "history.jsonl") + " (the refusal)" if held else
             "wrote " + ", ".join(_shown(f) for f in (d / f"v{r.spec.version}.json", d / "channels.json", d / "history.jsonl"))
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
    print(f"{r.spec.ref}{'' if held else ' (current)'}: {r.candidate.name}, answered by {r.answered_by}; adopted by {r.selection.by}"
          + ("" if r.candidate.name == listed.recommended else f" (the ranking recommended {listed.recommended})"))
    if r.candidate.name not in r.selection.tied:
        print(f"  note: not tied with {listed.recommended}: measured worse on {p0.objective.label}")
    print("  rule: " + (", ".join(f"{k} {v:.3f}" for k, v in (("threshold", rd.threshold), ("min probability", rd.min_probability)) if v is not None) or "the plain argmax"))
    print(f"  {p0.objective.label}: {p0.value}  interval {p0.interval}  (n {e.n})")
    if e.test:
        print(f"  held-out test: n {e.test.n}, primary {e.test.primary.value}  -> {r.evidence.test}"
              + (" (written with --force; the reason is recorded as why)" if r.selection.forced else ""))
    print(wrote)
    if check_it:
        print(check_it)
    return 1 if held else 0


def check(a: argparse.Namespace) -> int:
    """Ask both versions about today's test cases and compare them case by case. Exit 0 pass, 1 worse, 2 could not run or pending."""
    from .eval import check as checking
    from .eval.check import comment
    from .eval.task import load

    task_id, markdown = a.task, a.markdown

    def write(text: str) -> None:
        if markdown:
            markdown.parent.mkdir(parents=True, exist_ok=True)
            markdown.write_text(text)

    def failed(message: str) -> None:  # the PR still hears why
        write(comment.error_markdown(task_id, message))

    task = _guard(lambda: load(project(a), task_id), failed)
    r = _guard(lambda: checking.check(task, a.against, a.candidate, a.sample, a.cached_only), failed)
    md = comment.markdown(task, r)
    write(md)
    print(r.model_dump_json(indent=1) if a.json else md)
    return r.exit


def optimize(a: argparse.Namespace) -> int:
    """Optimize current's question for a model into a new candidate (needs s1flow[optimize]); it ships nothing:
    report compares it with the others, adopt makes it current when a person picks it."""
    from .eval import optimize as optimizing
    from .eval.task import load

    task = load(project(a), a.task)
    r = optimizing.optimize(task, a.budget, model=a.model, reflection=a.reflection, patience=a.patience, max_cost=a.max_cost)
    if a.json:
        print(r.model_dump_json(indent=1))
        return 0
    o = r.optimization
    print(f"{r.task}: candidate {r.candidate}  (from {r.start}; {o.candidates} questions tried, reflection ${o.reflection_cost_usd}, val {o.val_scores[0]} -> {o.val_scores[o.best_index]})")
    print(f"compare it: s1flow report {r.task}; adopt it: s1flow adopt {r.task} {r.candidate} --reason \"...\"")
    return 0


def cases_check(a: argparse.Namespace) -> int:
    """Check a task's cases before running it: states build, labels fit the question, duplicates, balance, the split.
    Exit 1 when a case is wrong."""
    from .eval import data as checking
    from .eval.task import load

    task = load(project(a), a.task)
    r = checking.check(task)
    print(checking.markdown(task, r))
    return 1 if r.errors else 0


def cases_review(a: argparse.Namespace) -> int:
    """The cases whose label is worth reading again (models disagreeing at a high probability, the same state with
    another label), a random sample, and what the corrections so far say about the task."""
    from .eval import review as reviewing
    from .eval.task import load

    task = load(project(a), a.task)
    r = reviewing.review(task, min_probability=a.min_probability, limit=a.limit, sample=a.sample, include_read=a.include_read)
    print(r.model_dump_json(indent=1) if a.json else reviewing.markdown(task, r))
    return 0


def cases_correct(a: argparse.Namespace) -> int:
    """Record a decision about one case's label in corrections.jsonl (the collected data stays as it is)."""
    from .eval import review as reviewing
    from .eval.cases import VERDICTS, Verdict
    from .eval.task import load
    from .integrations import git

    if a.verdict not in VERDICTS:
        raise ConfigError(f"verdict is one of {', '.join(VERDICTS)}, got {a.verdict!r}")
    value: Any = None if a.label is None else {"true": True, "false": False}.get(a.label.lower(), a.label)
    task = load(project(a), a.task)
    by = a.by or git.user(task.where.root)
    if not by:
        raise ConfigError("a correction records who decided: give --by or set git config user.name")
    fix = reviewing.correct(task, a.case_id, cast(Verdict, a.verdict), reason=a.reason, by=by, label=value)
    print(f"{fix.id}: {fix.verdict}" + (f" {fix.was!r} -> {fix.label!r}" if fix.verdict == "relabel" else "") + f" ({VERDICTS[fix.verdict]})")
    return 0


# ---------- the parser ----------


def _command(sub: Any, name: str, run: Callable[[argparse.Namespace], int], help: str | None = None, **kw: Any) -> argparse.ArgumentParser:
    """A command whose --help says what its function's docstring does (`help` in its group's list: the first line)."""
    doc = " ".join((run.__doc__ or "").split())
    p: argparse.ArgumentParser = sub.add_parser(name, help=help or doc.partition(". ")[0], description=kw.pop("description", doc or None), **kw)
    p.set_defaults(run=run)
    return p


def parser() -> argparse.ArgumentParser:
    from . import skill

    ap = Parser(prog="s1flow", context=("project", "connections"), description="Run small model-backed decisions in your app and CI, then evaluate and improve them on your own data.")
    sub = ap.add_subparsers(dest="command", required=True, parser_class=Parser)

    p = _command(sub, "init", init)
    p.add_argument("--task", help="also write tasks/<id>/task.py to fill in")
    p.add_argument("dir", nargs="?", default="s1flow", help="the project directory, made here; everything s1flow writes goes in it (default: s1flow)")
    p.add_argument("--ci", action="store_true", help="also write .github/workflows/s1flow-check.yml at the git root")

    p = _command(sub, "tasks", tasks, context=("project", "connections"))
    p.add_argument("tasks", nargs="*", help="these only (default: every task)")
    p.add_argument("--json", action="store_true", help="every version too, with its date and digest")

    p = _command(sub, "models", models, context=("project", "connections"))
    p.add_argument("--verify", action="store_true", help="ask each model plain questions and check every claim in s1flow.toml")
    p.add_argument("--models", help="with --verify: these only (default: the whole line-up and its versions)")
    p.add_argument("--json", action="store_true")

    p = _command(sub, "run", run, context=("project", "connections"))
    p.add_argument("task")
    p.add_argument("--models", help="comma-separated candidates, model[:version][/variant]: jev:1.14, d1@vercel/policy (default: s1flow.toml's `default`, on the task's own question)")
    p.add_argument("--fresh", action="store_true", help="call again instead of reading the cache (to measure latency and wall time)")
    p.add_argument("--concurrency", type=positive, help="calls in flight per model (default: the model's own); with it, models run one after another. 1 times each call alone")

    p = _command(sub, "report", report, context=("project", "connections"))
    p.add_argument("task", nargs="?", help="the task (or --from PATH)")
    p.add_argument("--json", action="store_true", help="every metric of each candidate, and the ranking, as JSON")
    p.add_argument("--limit", type=positive, default=12, help="candidates shown, in the ranking and the list (default: 12)")
    p.add_argument("--offset", type=int, default=0, help="candidates to skip (default: 0)")
    p.add_argument("--candidate", help="one candidate in full: model[:version][/variant]")
    p.add_argument("--out", type=Path, metavar="DIR", help="write comparison.json (with the chart series) and questions/<variant>.md / .json for each question")
    p.add_argument("--from", dest="from_path", type=Path, metavar="PATH", help="read a saved comparison.json offline")

    p = _command(sub, "adopt", adopt, context=("project", "connections"))
    p.add_argument("task", nargs="?", help="the task, or TASK@vN to roll back to a saved version")
    p.add_argument("candidate", nargs="?", help="the candidate, model[:version][/variant] as `s1flow report` names it")
    p.add_argument("--spec", type=Path, metavar="FILE", help="save this runtime spec as the next version, unevaluated, and make it current")
    p.add_argument("--root", type=Path, help="the policies directory, outside an s1flow project (an app's repository; with --connections for --spec)")
    p.add_argument("--reason", required=True, help="why (kept in the policy and in history.jsonl)")
    p.add_argument("--force", action="store_true", help="write it even when the held-out test shows it below")
    p.add_argument("--json", action="store_true")

    p = _command(sub, "check", check, context=("project", "connections"))
    p.add_argument("task")
    p.add_argument("--against", default="current", help="the version to compare with: vN (on a pull request, the base branch's current) or current")
    p.add_argument("--candidate", help="current, vN, or `draft` (the task's current question); default: current when --against names another version, else the edited question")
    p.add_argument("--sample", type=positive, help="check this many test cases only (a cheap PR check)")
    p.add_argument("--cached-only", action="store_true", help="make no calls (no keys, e.g. a PR from a fork); pending when some are needed")
    p.add_argument("--json", action="store_true")
    p.add_argument("--markdown", type=Path, help="also write the PR comment here")

    p = _command(sub, "optimize", optimize, context=("project", "connections"))
    p.add_argument("task")
    p.add_argument("--json", action="store_true")
    p.add_argument("--budget", type=int, default=300, help="GEPA metric calls (model calls on train/val)")
    p.add_argument("--model", help="model whose question is optimized (default: current's)")
    p.add_argument("--reflection", help="the reflection LM, an `llm` model of s1flow.toml (default: gpt-6.1-sol on OpenAI's API, OPENAI_API_KEY)")
    p.add_argument("--patience", type=int, help="stop after this many proposals without a new best on val")
    p.add_argument("--max-cost", type=float, help="stop once the reflection LM has cost this much (USD)")

    group = sub.add_parser("cases", context=("project", "connections"), help="check a task's cases; review and correct their labels",
                           description="Check a task's cases, and review and correct their labels.").add_subparsers(dest="action", required=True, parser_class=Parser)
    p = _command(group, "check", cases_check, context=("project",))
    p.add_argument("task")
    p = _command(group, "review", cases_review, context=("project", "connections"))
    p.add_argument("task")
    p.add_argument("--min-probability", type=float, default=0.9, help="list a case when a model answered something else at this probability or more")
    p.add_argument("--limit", type=int, default=30)
    p.add_argument("--sample", type=int, default=0, help="cases drawn at random from the rest, to estimate the label error rate (how many: see the Skill)")
    p.add_argument("--all", action="store_true", dest="include_read", help="also list cases already corrected")
    p.add_argument("--json", action="store_true")
    p = _command(group, "correct", cases_correct, context=("project",))
    p.add_argument("task")
    p.add_argument("case_id")
    p.add_argument("--verdict", required=True, help="relabel | keep | unclear | missing")
    p.add_argument("--reason", required=True, help="the criterion that decides it, or what the state lacks")
    p.add_argument("--by", help="who decided (default: git config user.name)")
    p.add_argument("--label", help="relabel only: the new label (a class key, or true / false)")

    d = _command(sub, "decide", decide, context=("project", "connections"), help="call a model (--model) or decide with a policy (--policy)",
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
    rel.add_argument("--path", help="a policy file, or a policy set from `policy export` (policies.json), instead of policies/")
    rel.add_argument("--case-id", help="the case's id in your app, kept in the log for context (it may repeat; feedback record joins by decision_id)")
    rel.add_argument("--log", help="append the log here (JSONL)")
    rel.add_argument("--keep-state", action="store_true", help="keep the state in the log, so `feedback measure` can add the case as a labelled one")
    rel.add_argument("--github-output", action="store_true", help="also write answer, probability, below_min_probability, decision_id, policy to $GITHUB_OUTPUT")
    d.add_argument("--json", action="store_true", help="print the Response (with --policy, the Decision) as JSON")

    group = sub.add_parser("feedback", context=("project", "connections"), help="record the right answer for a case a policy decided (record), or measure policies in production (measure)").add_subparsers(
        dest="action", required=True, parser_class=Parser)
    f = _command(group, "record", feedback_record, context=("project", "connections"), help="record the right answer for a case a policy decided",
                 description="Record the right answer for a case, joined to its answer by decision_id (what `s1flow feedback measure` measures from).")
    f.add_argument("policy", metavar=POLICY, help="the policy that decided it (its id in the log, or the task: the current version)")
    f.add_argument("decision_id", help="the exact decision_id returned by decide")
    f.add_argument("label", help="the right answer: a class key, or true / false")
    f.add_argument("--log", required=True, help="the log to append to (JSONL)")
    f.add_argument("--path", help="a policy file, or a policy set from `policy export` (policies.json), instead of policies/ (as decide --path)")
    m = _command(group, "measure", feedback_measure, context=("project", "connections"), help="measure each policy in production from the feedback in its logs (needs s1flow[eval])",
                 description="Measure each policy in production from the feedback in its logs, and add the cases with a kept state "
                             "as labelled cases. Exit 1 when production is shown below. Needs s1flow[eval].")
    m.add_argument("task")
    m.add_argument("logs", nargs="+", help="SDK logs (JSONL) or OpenTelemetry JSON exports")
    m.add_argument("--dry-run", action="store_true", help="measure only; add no cases")
    m.add_argument("--json", action="store_true")

    group = sub.add_parser("policy", context=("project", "connections"), help="runtime specifications: check and save one (create), the ones an app uses in one file (export)").add_subparsers(
        dest="action", required=True, parser_class=Parser)
    create = _command(group, "create", policy_create, context=("connections",), help="validate and save an unevaluated runtime specification")
    create.add_argument("file", type=Path, help="PolicySpec JSON file")
    create.add_argument("--root", type=Path, default=Path("policies"), help="directory for immutable policy versions")
    create.add_argument("--check", action="store_true", help="validate only; save nothing")
    create.add_argument("--reason", help="why it becomes current (needed unless --check); the same as adopt --spec FILE --reason")
    create.add_argument("--json", action="store_true")
    ex = _command(group, "export", policy_export, context=("project",), help="write the policies an app uses into one file (policies.json)",
                  description="One file with each task's current policy and its digest, for an app in another repository or "
                              "language to vendor and review in its own pull requests. policies.load(task, path=FILE) reads it.")
    ex.add_argument("tasks", nargs="*", help="the tasks (default: every task with a current version)")
    ex.add_argument("--out", default="policies.json")

    doc = _command(sub, "doctor", doctor, context=("project", "connections"), help="the keys and hosts the models need, and whether they are there",
                   description="For each model, the environment variables its provider reads (set or not; never a value) and the hosts "
                               "it calls (for a sandbox's allow-list). Exit 0 when everything needed is there, 1 otherwise, one line per problem.")
    doc.add_argument("--models", help="comma-separated names from s1flow.toml (default: its `default`)")
    doc.add_argument("--policy", metavar=POLICY, help="the model of this policy (the current version when no @ is given)")
    doc.add_argument("--reach", action="store_true", help="also send one plain HTTPS request per host, without a key (no model is called)")
    doc.add_argument("--json", action="store_true")

    group = sub.add_parser("skill", help="write the Agent Skill where agents read it, or print where it is").add_subparsers(dest="action", required=True, parser_class=Parser)
    si = _command(group, "install", skill_install, help="write the Skill into .agents/skills/s1flow/ and .claude/skills/s1flow/",
                  description="Write the Skill this s1flow carries into <git root or cwd>/.agents/skills/s1flow/ and .claude/skills/s1flow/, "
                              "or where --dir and --user say. A file changed there since s1flow wrote it is kept (and named) unless --force.")
    si.add_argument("--dir", action="append", metavar="PATH", help="a skills directory to write s1flow/ into; repeatable")
    si.add_argument("--user", action="store_true", help="~/.agents/skills/ and ~/.claude/skills/")
    si.add_argument("--force", action="store_true", help="overwrite files changed there")

    _command(group, "path", skill_path, help="print the package's own copy of the Skill (to link to)")

    g = _command(sub, "guide", guide, help="print the Skill's routing table, or one of its references",
                 description="Print the Skill this s1flow carries: SKILL.md (which job reads which reference), or references/<topic>.md.")
    g.add_argument("topic", nargs="?", help=", ".join(skill.topics()))
    return ap
