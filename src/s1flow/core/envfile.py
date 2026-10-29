"""The project's .env files, read into the environment by the `s1flow` command only: the library takes keys
from the environment and never reads a file. The standard library alone, so the base install reads them too.

The common form: `KEY=value` or `export KEY=value`, one per line; `'...'` taken as is, `"..."` with the
escapes \\n \\t \\" \\\\; after an unquoted value, ` #` starts a comment. No `${VAR}` expansion, no value
over several lines.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

from . import place
from .errors import ConfigError

_LINE = re.compile(r"(?:export\s+)?([A-Za-z_][A-Za-z0-9_.-]*)\s*=\s*(.*)")
_ESCAPES = {"n": "\n", "t": "\t", '"': '"', "\\": "\\"}


def parse(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or not (m := _LINE.fullmatch(line)):
            continue
        key, value = m.group(1), m.group(2)
        if len(value) >= 2 and value[0] == value[-1] == "'":
            value = value[1:-1]
        elif len(value) >= 2 and value[0] == value[-1] == '"':
            value = re.sub(r"\\(.)", lambda e: _ESCAPES.get(e.group(1), e.group(0)), value[1:-1])
        else:
            value = re.split(r"\s+#", value, maxsplit=1)[0].rstrip()
        out[key] = value
    return out


def load(root: Path) -> None:
    """The .env files of `root` and its parents up to the git root, nearest first; what is already set wins."""
    for d in place.search_dirs(place.absolute(root, "dotenv root")):
        path = d / ".env"
        if path.is_file():
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as e:
                raise ConfigError(f"cannot read dotenv file {path}: {e}; check its permissions and UTF-8 encoding") from None
            if "\x00" in text:
                raise ConfigError(f"invalid dotenv file {path}: remove NUL bytes before loading it")
            for k, v in parse(text).items():
                os.environ.setdefault(k, v)
        if (d / ".git").exists():
            break
