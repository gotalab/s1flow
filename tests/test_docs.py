"""What the repository tells people to run is what this version has: the commands its docs name, the release its
examples and the Skill pin, and Japanese pages that translate the English ones as they are now."""

import hashlib
import re
import tomllib
from pathlib import Path

from conftest import cli

ROOT = Path(__file__).resolve().parents[1]
DOCS = [ROOT / "README.md", ROOT / "AGENTS.md", ROOT / "decide" / "action.yml",
        *sorted(ROOT.glob("docs/*.md")), *sorted(ROOT.glob("docs-ja/*.md")), *sorted(ROOT.glob("plugin/skills/**/*.md")),
        *sorted(ROOT.glob("examples/*"))]
ENGLISH_ONLY = {"development.md"}  # for contributors; the Japanese site links to the English page
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
    """The names `s1flow COMMAND --help` lists: the commands, or a command's sub-commands ({a,b} in its usage, not an
    option's choices: --split {train,val})."""
    shown = cli(*command, "--help").output
    if not command:
        return set(re.findall(r"^  ([a-z][a-z-]*)  ", shown.partition("Commands:")[2].partition("\n\n")[0], re.M))
    return {c for group in re.findall(r"(?<!\w )\{([a-z,-]+)\}", shown.partition("\n\n")[0]) for c in group.split(",")}


def test_the_docs_name_only_commands_the_cli_has():
    commands = choices()
    assert {"init", "run", "report", "adopt", "decide"} <= commands  # the parse found the list
    subcommands = {c: choices(c) for c in commands}
    assert subcommands["feedback"] == {"record", "import", "measure"}  # and finds a command's sub-commands
    unknown = [f"{p.relative_to(ROOT)}: s1flow {c} {sub}".rstrip() for p in DOCS for c, sub in named(p.read_text())
               if c not in commands or (sub and subcommands[c] and sub not in subcommands[c])]
    assert not unknown, f"no such command (s1flow --help lists {', '.join(sorted(commands))}): {unknown}"


def test_the_examples_and_the_skill_pin_the_release_of_this_version():
    """What people copy pins the release of this version (the Release steps
    in docs/development.md: the PR that sets the version sets these, and merging it tags and publishes that commit)."""
    pins = [(p.relative_to(ROOT), want, ref) for p in DOCS for want, pin in PINS.items() for ref in pin.findall(p.read_text())]
    assert {want for _, want, _ in pins} == set(PINS)  # both kinds are there to check
    stale = [f"{p}: {ref}" for p, want, ref in pins if ref != want]
    assert not stale, f"pyproject.toml's version is {VERSION}: pin the Action at v{VERSION} and the package at =={VERSION} in {stale}"


def source_hash(english: Path) -> str:
    return hashlib.sha256(english.read_bytes()).hexdigest()[:12]


def test_each_japanese_page_translates_the_english_page_as_it_is_now():
    """docs-ja/X.md translates docs/X.md, and says which text it translated (translated_from: the English file's
    hash). An English change without its translation fails here: update docs-ja/X.md, then its translated_from."""
    english = {p.name for p in ROOT.glob("docs/*.md")} - ENGLISH_ONLY
    japanese = {p.name for p in ROOT.glob("docs-ja/*.md")}
    assert english == japanese, f"docs/ and docs-ja/ should hold the same pages: only in docs/ {sorted(english - japanese)}, only in docs-ja/ {sorted(japanese - english)}"
    stale = []
    for name in sorted(english):
        stamp = re.search(r"^translated_from: (\S+)$", (ROOT / "docs-ja" / name).read_text(), re.M)
        if not stamp or stamp[1] != source_hash(ROOT / "docs" / name):
            stale.append(f"docs-ja/{name} (translated_from: {source_hash(ROOT / 'docs' / name)} once it matches docs/{name})")
    assert not stale, f"these translations are behind their English page: {stale}"
