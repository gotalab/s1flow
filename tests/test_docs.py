"""What the repository tells people to run is what this version has: the commands its docs name, and the release
its examples and the Skill pin."""

import re
import tomllib
from pathlib import Path

from conftest import cli

ROOT = Path(__file__).resolve().parents[1]
DOCS = [ROOT / "README.md", ROOT / "action.yml", ROOT / "decide" / "action.yml",
        *sorted(ROOT.glob("docs/*.md")), *sorted(ROOT.glob("plugin/skills/**/*.md")), *sorted(ROOT.glob("examples/*"))]
VERSION = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]["version"]

# A command as docs write one: `s1flow X`, uv run / uvx [options] s1flow X, or a code-block line starting s1flow X.
# Prose ("s1flow measures ...") is not read; neither is plain text in YAML, which mixes the two.
RUNNER = r"(?:uv run|uvx)(?: --?[\w-]+(?:[ =]\S+)?)* "
INLINE = re.compile(rf"(?:`|{RUNNER})s1flow ([a-z][a-z-]*)(?: ([a-z][a-z-]*))?")
FENCE = re.compile(r"^```.*?^```", re.M | re.S)
LINE = re.compile(r"^\s*(?:\$ )?s1flow ([a-z][a-z-]*)(?: ([a-z][a-z-]*))?", re.M)
PINS = {f"v{VERSION}": re.compile(r"gotalab/s1flow(?:/decide)?@([\w.-]+)(?![\w.<-])"),  # the Action; not prose naming @v<version>
        VERSION: re.compile(r"\bs1flow(?:\[[\w,]+\])?==([\w.]+)")}  # the package


def named(text: str) -> list[tuple[str, str]]:
    return INLINE.findall(text) + [c for block in FENCE.findall(text) for c in LINE.findall(block)]


def choices(*command: str) -> set[str]:
    """The names `s1flow COMMAND --help` lists: the commands, or a command's sub-commands ({a,b} in its usage)."""
    shown = cli(*command, "--help").output
    if not command:
        return set(re.findall(r"^  ([a-z][a-z-]*)  ", shown.partition("Commands:")[2].partition("\n\n")[0], re.M))
    return {c for group in re.findall(r"\{([a-z,-]+)\}", shown.partition("\n\n")[0]) for c in group.split(",")}


def test_the_docs_name_only_commands_the_cli_has():
    commands = choices()
    assert {"init", "run", "report", "adopt", "check", "decide"} <= commands  # the parse found the list
    subcommands = {c: choices(c) for c in commands}
    assert subcommands["feedback"] == {"record", "measure"}  # and finds a command's sub-commands
    unknown = [f"{p.relative_to(ROOT)}: s1flow {c} {sub}".rstrip() for p in DOCS for c, sub in named(p.read_text())
               if c not in commands or (sub and subcommands[c] and sub not in subcommands[c])]
    assert not unknown, f"no such command (s1flow --help lists {', '.join(sorted(commands))}): {unknown}"


def test_the_examples_and_the_skill_pin_the_release_of_this_version():
    """`s1flow init --ci` writes gotalab/s1flow@v<version>; what people copy pins the same release (the Release steps
    in docs/development.md: the PR that sets the version sets these, and publish runs from that tag)."""
    pins = [(p.relative_to(ROOT), want, ref) for p in DOCS for want, pin in PINS.items() for ref in pin.findall(p.read_text())]
    assert {want for _, want, _ in pins} == set(PINS)  # both kinds are there to check
    stale = [f"{p}: {ref}" for p, want, ref in pins if ref != want]
    assert not stale, f"pyproject.toml's version is {VERSION}: pin the Action at v{VERSION} and the package at =={VERSION} in {stale}"
