"""`s1flow doctor`: what the models need from where they run, and whether it is there.

For each model, the keys its provider declares (set or not: never a value or its length), the hosts it calls
(a sandbox's allow-list), and the packages beyond the base install it imports. `reach` adds a plain HTTPS
request per host, without a key: any answer, even a 404, means the host is reachable, and no model is called.
A provider that declares nothing is shown as such and checked no further.
"""

from __future__ import annotations

import importlib.util
from collections.abc import Collection, Iterable
from dataclasses import asdict, dataclass, field
from typing import Any
from urllib.parse import urlsplit

import httpx

from .client import ModelSpec
from .client.providers import needs
from .client.providers.needs import where_to_get
from .core.errors import S1flowError

# The top-level module a missing import names -> the extra that installs it (also the CLI's hint, cli.missing_extra).
EXTRAS = {"numpy": "eval", "scipy": "eval", "sklearn": "eval", "PIL": "images", "litellm": "llm", "gepa": "optimize"}

LOOPBACK = ("localhost", "127.0.0.1", "::1")


@dataclass
class Host:
    url: str  # the origin called
    host: str  # what an allow-list names
    reachable: bool | None = None  # None: not checked (no --reach)
    status: int | None = None
    error: str | None = None


@dataclass
class Checked:
    name: str
    provider: str
    declared: bool  # False: the provider says nothing of its keys and hosts
    keys: dict[str, str | None] = field(default_factory=dict)  # name -> "environment", ".env", or None when not set
    hosts: list[Host] = field(default_factory=list)
    packages: dict[str, bool] = field(default_factory=dict)  # module -> installed
    note: str = ""
    error: str | None = None  # the spec cannot be read (an unknown provider, options that do not fit)


@dataclass
class Report:
    source: str
    models: list[Checked]
    problems: list[str]

    @property
    def keys(self) -> list[str]:
        return sorted({k for m in self.models for k in m.keys})

    @property
    def hosts(self) -> list[str]:
        """The allow-list: every host but this machine's (the clef-proxy relay)."""
        return sorted({h.host for m in self.models for h in m.hosts if urlsplit(h.url).hostname not in LOOPBACK})

    def as_json(self) -> dict[str, Any]:
        return {"source": self.source, "ok": not self.problems, "keys": self.keys, "hosts": self.hosts,
                "models": [asdict(m) for m in self.models], "problems": self.problems}


def reach(url: str, timeout: float = 5.0) -> Host:
    host = Host(url, urlsplit(url).netloc)
    try:
        r = httpx.get(url, timeout=timeout)
    except httpx.HTTPError as e:
        host.reachable, host.error = False, f"{type(e).__name__}: {e}"[:200]
    else:
        host.reachable, host.status = True, r.status_code
    return host


def check_one(name: str, spec: ModelSpec, env: dict[str, str], from_dotenv: Collection[str]) -> Checked:
    c = Checked(name, spec.provider, declared=False)
    try:
        declared = needs(spec)
    except S1flowError as e:
        c.error = str(e.args[0] if e.args else e)
        return c
    if declared is None:
        return c
    c.declared, c.note = True, declared.note
    c.keys = {k: (".env" if k in from_dotenv else "environment") if env.get(k) else None for k in declared.keys}
    c.hosts = [Host(u, urlsplit(u).netloc) for u in declared.hosts]
    c.packages = {p: importlib.util.find_spec(p) is not None for p in declared.packages}
    return c


def check(
    source: str, models: Iterable[tuple[str, ModelSpec]], *,
    env: dict[str, str], from_dotenv: Collection[str] = (), probe: bool = False,
) -> Report:
    """`source` says where the models came from. `from_dotenv`: the variables the CLI read from .env rather than the environment."""
    checked, reached = list[Checked](), dict[str, Host]()
    problems: list[str] = []
    for name, spec in models:
        c = check_one(name, spec, env, from_dotenv)
        if probe:  # each host once, however many models call it
            for h in c.hosts:
                if h.url not in reached:
                    reached[h.url] = reach(h.url)
            c.hosts = [reached[h.url] for h in c.hosts]
        checked.append(c)
        if c.error:
            problems.append(f"{name}: {c.error}")
    missing: dict[str, list[str]] = {}
    for c in checked:
        for k, where in c.keys.items():
            if where is None:
                missing.setdefault(k, []).append(c.name)
    problems += [f"{k} is not set ({', '.join(names)})" + (f": {get}" if (get := where_to_get(k)) else "") for k, names in sorted(missing.items())]
    for c in checked:
        for p, installed in c.packages.items():
            if not installed:
                extra = EXTRAS.get(p)
                problems.append(f"{c.name} needs {p}" + (f": install s1flow[{extra}]" if extra else ""))
    for h in reached.values():
        if h.reachable is False:
            problems.append(f"{h.host} is unreachable ({', '.join(c.name for c in checked if h in c.hosts)}): {h.error}")
    return Report(source, checked, problems)


def render(r: Report) -> str:
    lines = [r.source, ""]
    for c in r.models:
        lines.append(f"{c.name}  ({c.provider})")
        if c.error:
            lines.append(f"  error: {c.error}")
        elif not c.declared:
            lines.append(f"  provider {c.provider} declares no keys or hosts: doctor cannot check them")
        for k, where in c.keys.items():
            lines.append(f"  key   {k}  " + ("set" + (" (.env)" if where == ".env" else "") if where else "NOT SET" + (f" ({get})" if (get := where_to_get(k)) else "")))
        for h in c.hosts:
            state = "" if h.reachable is None else f"  reachable (HTTP {h.status})" if h.reachable else f"  UNREACHABLE: {h.error}"
            lines.append(f"  host  {h.host}{state}")
        for p, installed in c.packages.items():
            lines.append(f"  pkg   {p}  " + ("installed" if installed else "NOT INSTALLED"))
        if c.note:
            lines.append(f"  note  {c.note}")
    lines += ["", f"secrets:    {', '.join(r.keys) or '-'}", f"allow-list: {', '.join(r.hosts) or '-'}"]
    return "\n".join(lines)
