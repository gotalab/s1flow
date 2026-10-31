"""What every command module shares: the argparse frame (one `error:` line, the exit codes in every --help) and the
project, client and path helpers. Nothing here imports the evaluation stack."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, NoReturn, TypeVar

from ..core import envfile, place
from ..core.errors import ConfigError, S1flowError

if TYPE_CHECKING:
    from ..client import Client
    from ..project import Project

EXITS = "Exit codes: 0 done; 1 a gate failed or something was found (check fails, doctor or models --verify finds a problem); 2 usage, configuration, could not run, or check pending."
POLICY = "TASK[@vN]"  # how a command names a policy (policies.file.Ref)

T = TypeVar("T")


# ---------- the argparse frame ----------


def usage_error(message: str, command: str) -> NoReturn:
    print(f"error: {message} (see {command} --help)", file=sys.stderr)
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


def command(sub: Any, name: str, run: Callable[[argparse.Namespace], int], help: str | None = None, **kw: Any) -> argparse.ArgumentParser:
    """A command whose --help says what its function's docstring does (`help` in its group's list: the first line)."""
    doc = " ".join((run.__doc__ or "").split())
    p: argparse.ArgumentParser = sub.add_parser(name, help=help or doc.partition(". ")[0], description=kw.pop("description", doc or None), **kw)
    p.set_defaults(run=run)
    return p


def positive(text: str) -> int:
    n = int(text)
    if n < 1:
        raise argparse.ArgumentTypeError(f"{n} is not 1 or more")
    return n


# ---------- the project, its clients and paths ----------


def project(a: argparse.Namespace) -> Project:
    from ..project import Project

    root = project_root(a, required=True)
    assert root is not None
    load_env(root)
    return Project(root, connections=connections_path(a) if "connections" in a.context_options else None)


def json_arg(arg: str, what: str) -> Any:
    """JSON as given, or `@file.json`."""
    try:
        return json.loads(Path(arg[1:]).read_text() if arg.startswith("@") else arg)
    except (OSError, ValueError) as e:
        raise ConfigError(f"{what}: {e}") from None


def load_env(root: Path | None) -> None:
    """Keys from the project's .env files (core/envfile.py), as the evaluation commands read them."""
    envfile.load(root or Path.cwd())


def project_root(a: argparse.Namespace, *, required: bool = False) -> Path | None:
    return place.project(getattr(a, "project", None), required=required)


def connections_path(a: argparse.Namespace) -> Path | None:
    value = getattr(a, "connections", None)
    return place.absolute(value, "connections") if value is not None else None


def client(a: argparse.Namespace, root: Path | None) -> Client:
    from ..client import Client

    config = connections_path(a)
    if config is None and root is not None:
        config = root / place.CONFIG
    if config is None:
        raise ConfigError(f"no connections configured in {Path.cwd()}; use --connections PATH "
                          "or --project PATH; run s1flow init to create a project")
    return Client(connections=config)


def policy_client(a: argparse.Namespace) -> Client:
    """Policy execution explicitly grants the connections in this invocation's file."""
    from ..client import Client

    if not getattr(a, "connections", None):
        raise ConfigError("policy execution needs --connections PATH: a trusted file listing only the allowed connections")
    return Client(connections=a.connections)


def policy_root(a: argparse.Namespace) -> Path | None:
    if getattr(a, "path", None) is not None:
        return None
    explicit = getattr(a, "root", None)
    if explicit is not None:
        return place.absolute(explicit, "policy root")
    root = project_root(a, required=True)
    assert root is not None
    return root / "policies"


def guard(f: Callable[[], T], on_error: Callable[[str], None]) -> T:
    """Run f; on an S1flowError, let `on_error` record why (e.g. for the PR) before it exits 2."""
    try:
        return f()
    except S1flowError as e:
        on_error(str(e.args[0] if e.args else e))
        raise


def shown(path: Path) -> str:
    """A path from where the command ran, when it is below it."""
    return str(path.relative_to(Path.cwd())) if path.is_relative_to(Path.cwd()) else str(path)


def label(text: str) -> Any:
    """A label as typed: true / false (any case) as a boolean, else the text (a class key)."""
    return {"true": True, "false": False}.get(text.lower(), text)
