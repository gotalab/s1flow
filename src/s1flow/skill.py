"""The Agent Skill that travels with the package (`plugin/skills/s1flow/` in the repository, `s1flow/skills/s1flow/` in
the wheel), and writing it where agents read it. Standard library only: it runs on the base install.

    s1flow init --skill                   <git root or cwd>/.agents/skills/s1flow/ and .claude/skills/s1flow/
    (the Claude Code plugin brings the same Skill)

Each written copy holds MARKER: the s1flow version that wrote it and the hash of each file as written. A file whose
content no longer matches its recorded hash was changed here and is kept unless `force`; so is a file the marker
does not know (a copy made by hand).
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass, field
from importlib import metadata
from pathlib import Path

from .core import place
from .core.errors import ConfigError

NAME = "s1flow"
MARKER = ".s1flow-skill.json"
AGENT_DIRS = (".agents/skills", ".claude/skills")  # Codex, Devin and others; Claude Code


def source() -> Path:
    """The Skill this s1flow carries: inside the installed package, or plugin/skills/s1flow/ of a source checkout."""
    here = Path(__file__).resolve().parent
    for d in (here / "skills" / NAME, here.parents[1] / "plugin" / "skills" / NAME):
        if (d / "SKILL.md").is_file():
            return d
    raise ConfigError(f"this s1flow carries no Skill (looked in {here / 'skills' / NAME})")


def version() -> str:
    try:
        return metadata.version("s1flow")
    except metadata.PackageNotFoundError:
        return "0"


def project_root() -> Path:
    """The git root above the working directory, else the working directory."""
    here = Path.cwd().resolve()
    return place.git_root(here) or here


def targets(root: Path | None = None) -> list[Path]:
    """The skills directories to write into (each gets an s1flow/ folder): the project's."""
    return [(root or project_root()) / d for d in AGENT_DIRS]


def _hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _files(d: Path) -> dict[str, bytes]:
    return {
        p.relative_to(d).as_posix(): p.read_bytes()
        for p in sorted(d.rglob("*"))
        if p.is_file() and p.name != MARKER
        and "__pycache__" not in p.parts and p.suffix not in (".pyc", ".pyo")
    }


def marker(d: Path) -> dict[str, object] | None:
    try:
        m = json.loads((d / MARKER).read_text())
    except (OSError, ValueError):
        return None
    return m if isinstance(m, dict) else None


@dataclass
class Installed:
    path: Path
    version: str
    added: list[str] = field(default_factory=list)
    updated: list[str] = field(default_factory=list)
    unchanged: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)  # changed here (or unknown to the marker), kept
    linked: bool = False  # the target is the package's own copy: nothing written


def install(skills_dir: Path, force: bool = False) -> Installed:
    """Write the Skill into `skills_dir`/s1flow/, keeping what was changed there unless `force`."""
    src, dest = source(), Path(skills_dir) / NAME
    done = Installed(dest, version())
    if dest.exists() and dest.resolve() == src.resolve():
        done.linked = True
        return done
    old = marker(dest) or {}
    recorded_files = old.get("files")
    recorded: dict[str, str] = recorded_files if isinstance(recorded_files, dict) else {}
    new = _files(src)
    hashes: dict[str, str] = {}
    for rel, data in new.items():
        path, h = dest / rel, _hash(data)
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            done.added.append(rel)
        elif (now := _hash(path.read_bytes())) == h:
            done.unchanged.append(rel)
        elif force or now == recorded.get(rel):
            path.write_bytes(data)
            done.updated.append(rel)
        else:
            done.skipped.append(rel)
            if rel in recorded:
                hashes[rel] = recorded[rel]  # still what s1flow last wrote: the change here stays protected
            continue
        hashes[rel] = h
    for rel in sorted(set(recorded) - set(new)):  # gone from this version
        path = dest / rel
        if not path.exists():
            continue
        if force or _hash(path.read_bytes()) == recorded[rel]:
            path.unlink()
            done.removed.append(rel)
        else:
            done.skipped.append(rel)
            hashes[rel] = recorded[rel]
    (dest / MARKER).write_text(json.dumps({"schema": "s1flow/skill-marker@1", "s1flow_version": done.version, "files": hashes}, indent=1) + "\n")
    return done


def _show(p: Path) -> str:
    try:
        return os.path.relpath(p) if p.resolve().is_relative_to(Path.cwd().resolve()) else str(p)
    except ValueError:
        return str(p)


def lines(done: Installed) -> list[str]:
    where = _show(done.path)
    if done.linked:
        return [f"kept {where}: it is the package's own copy (a link)"]
    counts = ", ".join(f"{len(v)} {k}" for k, v in (("added", done.added), ("updated", done.updated), ("removed", done.removed),
                                                     ("unchanged", done.unchanged), ("skipped", done.skipped)) if v)
    out = [f"{where} (s1flow {done.version}): {counts or 'nothing to write'}"]
    out += [f"  skipped {rel}: changed there (--force overwrites it)" for rel in done.skipped]
    return out


def _policy(v: str) -> tuple[int, ...]:
    m = re.match(r"\d+(\.\d+)*", v)
    return tuple(int(x) for x in m.group(0).split(".")) if m else ()


def stale(root: Path | None = None) -> list[str]:
    """One line per project copy an older s1flow wrote."""
    out = []
    for d in AGENT_DIRS:
        copy = (root or project_root()) / d / NAME
        m = marker(copy)
        if m is None:
            continue
        was, now = str(m.get("s1flow_version", "?")), version()
        if _policy(was) < _policy(now):
            out.append(f"{_show(copy)} is from s1flow {was}, this is {now}: s1flow init --skill --force updates it")
    return out

