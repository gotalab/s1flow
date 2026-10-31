"""`s1flow models`: the line-up in s1flow.toml, and what --verify found each model takes."""

from __future__ import annotations

import argparse
import json
from typing import Any

from .common import command, project


def models(a: argparse.Namespace) -> int:
    """The line-up: what each model declares (s1flow.toml) next to what --verify found (models.verified.json)."""
    from ..eval import verify as verifying

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


def add(sub: Any) -> None:
    p = command(sub, "models", models, context=("project", "connections"))
    p.add_argument("--verify", action="store_true", help="ask each model plain questions and check every claim in s1flow.toml")
    p.add_argument("--models", help="with --verify: these only (default: the whole line-up and its versions)")
    p.add_argument("--json", action="store_true")
