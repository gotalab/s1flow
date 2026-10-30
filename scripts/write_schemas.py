"""Write schema/*.json, the JSON Schemas of what s1flow stores and prints, from the pydantic types that read them.

    uv run python scripts/write_schemas.py           # write
    uv run python scripts/write_schemas.py --check   # exit 1 when a schema differs from its type (a test runs this)

A format change edits the type, its schema (this script) and its fixtures (schema/fixtures/) in one commit.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

from pydantic import BaseModel, TypeAdapter

from s1flow.client.answers import Response
from s1flow.eval.cases import Correction, FeedbackCase
from s1flow.eval.evalset import SplitFile, SplitFileV1
from s1flow.eval.comparison import Comparison
from s1flow.eval.policy import EvaluatedPolicy, EvaluationRecord
from s1flow.eval import policy_v2
from s1flow.eval.records import PredictionRecord
from s1flow.policies.policy_set import PolicySet
from s1flow.policies.log import Decision, Log
from s1flow.policies.file import PolicySpec
from s1flow.policies.history import Switch

OUT = Path(__file__).resolve().parents[1] / "schema"
BASE = "https://github.com/gotalab/s1flow/blob/main/schema/"


def of(t: type[BaseModel]) -> dict[str, Any]:
    return t.model_json_schema(by_alias=True)


def case() -> dict[str, Any]:
    """A row of a task's data (data.jsonl, or a .json array): the task's own fields. s1flow itself reads only
    `id` (the row's index when absent) and `rationale`; task.py reads the rest. feedback.jsonl and
    corrections.jsonl lines, which s1flow writes, are in $defs."""
    return {
        "title": "Case",
        "description": case.__doc__.replace("\n    ", " ") if case.__doc__ else "",
        "type": "object",
        "properties": {
            "id": {"type": ["string", "integer"], "description": "the case's id, unique in the task"},
            "rationale": {"type": "string", "description": "why it got its label (shown to GEPA's reflection LM, never to the model)"},
        },
        "$defs": lifted({"feedback": FeedbackCase, "correction": Correction}),
    }


def lifted(types: dict[str, type[BaseModel]]) -> dict[str, Any]:
    """Types' schemas to place under another's $defs, with the types they refer to beside them: their refs
    ("#/$defs/...") point at the outer $defs."""
    out: dict[str, Any] = {}
    for name, t in types.items():
        s = of(t)
        out |= s.pop("$defs", {})
        out[name] = s
    return out


SCHEMAS: dict[str, Callable[[], dict[str, Any]]] = {
    "case-1": case,
    "split-1": lambda: of(SplitFileV1),  # still read (as @2), no longer written
    "split-2": lambda: of(SplitFile),
    "comparison-2": lambda: of(Comparison),
    "policy-2": lambda: of(PolicySpec) | {"title": "Policy"},  # what a policy file holds
    "evaluated-policy-3": lambda: of(EvaluatedPolicy),
    "log-2": lambda: {"title": "Log", **TypeAdapter(Log).json_schema(by_alias=True)},
    "policy-evaluation-3": lambda: of(EvaluationRecord),
    "policy-evaluation-2": lambda: of(policy_v2.EvaluationRecord),  # still read (upgraded to @3), no longer written
    "history-1": lambda: of(Switch) | {"title": "History", "description": "One line of policies/<task>/history.jsonl: " + (Switch.__doc__ or "")},
    "run-2": lambda: of(PredictionRecord),
    "response-1": lambda: of(Response),
    "decision-2": lambda: of(Decision),
    "policy-set-2": lambda: of(PolicySet),
}


def schema(name: str) -> dict[str, Any]:
    return {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": f"{BASE}{name}.json", **SCHEMAS[name]()}


def text(name: str) -> str:
    return json.dumps(schema(name), ensure_ascii=False, indent=1) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="write nothing; exit 1 when a schema is not what its type gives")
    a = ap.parse_args()
    differ = [n for n in SCHEMAS if not (OUT / f"{n}.json").is_file() or (OUT / f"{n}.json").read_text() != text(n)]
    if a.check:
        for n in differ:
            print(f"schema/{n}.json differs from its type: run scripts/write_schemas.py", file=sys.stderr)
        return 1 if differ else 0
    OUT.mkdir(exist_ok=True)
    for n in SCHEMAS:
        (OUT / f"{n}.json").write_text(text(n))
    print(f"wrote {len(SCHEMAS)} schemas in {OUT}" + (f" ({', '.join(differ)} changed)" if differ else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
