"""What the repository tells people to run is what this version has: the commands its docs name, and the Action
release its examples and the Skill pin."""

import re
import tomllib
from pathlib import Path

from conftest import cli

ROOT = Path(__file__).resolve().parents[1]
DOCS = [ROOT / "README.md", ROOT / "action.yml", ROOT / "decide" / "action.yml",
        *sorted(ROOT.glob("docs/*.md")), *sorted(ROOT.glob("skills/**/*.md")), *sorted(ROOT.glob("examples/*"))]
VERSION = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]["version"]

INLINE = re.compile(r"(?:`|(?:uv run|uvx) )s1flow ([a-z][a-z-]*)")  # `s1flow X`, uv run s1flow X
FENCE = re.compile(r"^```.*?^```", re.M | re.S)
LINE = re.compile(r"^\s*(?:\$ )?s1flow ([a-z][a-z-]*)", re.M)  # a line of a code block that runs s1flow
PIN = re.compile(r"gotalab/s1flow(?:/decide)?@([\w.-]+)(?![\w.<-])")  # a ref, not prose naming @v<version>


def named(text: str) -> list[str]:
    return INLINE.findall(text) + [c for block in FENCE.findall(text) for c in LINE.findall(block)]


def test_the_docs_name_only_commands_the_cli_has():
    shown = cli("--help").output
    commands = set(re.findall(r"^  ([a-z][a-z-]*)  ", shown.partition("Commands:")[2].partition("\n\n")[0], re.M))
    assert {"init", "run", "report", "adopt", "check", "decide"} <= commands  # the parse found the list
    unknown = [f"{p.relative_to(ROOT)}: s1flow {c}" for p in DOCS for c in named(p.read_text()) if c not in commands]
    assert not unknown, f"no such command (s1flow --help lists {', '.join(sorted(commands))}): {unknown}"


def test_the_examples_and_the_skill_pin_the_action_this_version_tags():
    """`s1flow init --ci` writes gotalab/s1flow@v<version>; what people copy pins the same release (the Release steps
    in docs/development.md: the PR that sets the version sets these, and publish runs from that tag)."""
    pins = [(p.relative_to(ROOT), ref) for p in DOCS for ref in PIN.findall(p.read_text())]
    assert pins
    stale = [f"{p}: @{ref}" for p, ref in pins if ref != f"v{VERSION}"]
    assert not stale, f"pyproject.toml's version is {VERSION}: pin the Action at v{VERSION} in {stale}"
