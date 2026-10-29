"""Write plugin/skills/ from skills/ (the Skill's source), so the plugin carries the same Skill as the package.

    uv run python scripts/sync_plugin.py           write it
    uv run python scripts/sync_plugin.py --check   exit 1 when plugin/skills/ differs (tests/test_skill.py runs this)
"""

from __future__ import annotations

import filecmp
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills"
COPY = ROOT / "plugin" / "skills"


def differences() -> list[str]:
    def files(d: Path) -> set[str]:
        return {p.relative_to(d).as_posix() for p in d.rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.suffix not in (".pyc", ".pyo")} if d.is_dir() else set()

    src, copy = files(SOURCE), files(COPY)
    out = [f"missing {f}" for f in sorted(src - copy)] + [f"extra {f}" for f in sorted(copy - src)]
    out += [f"differs {f}" for f in sorted(src & copy) if not filecmp.cmp(SOURCE / f, COPY / f, shallow=False)]
    return out


def main(argv: list[str]) -> int:
    diff = differences()
    if "--check" in argv:
        for line in diff:
            print(f"plugin/skills: {line}", file=sys.stderr)
        if diff:
            print("run: uv run python scripts/sync_plugin.py", file=sys.stderr)
        return 1 if diff else 0
    if COPY.exists():
        shutil.rmtree(COPY)
    shutil.copytree(SOURCE, COPY, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"))
    print(f"wrote plugin/skills/ from skills/ ({len(diff)} changed)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
