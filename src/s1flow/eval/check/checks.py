"""reports/<task>/checks.json: the last check of each pair of stored versions, so `promote` can say whether check
has run for the versions it moves between."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from ...core import clock

Verdict = Literal["fail", "better", "no_difference", "pass", "pending"]


class Checked(BaseModel):
    """The last check of a pair of stored versions."""

    verdict: Verdict
    n: int
    sample: int | None
    at: str


class ChecksFile(BaseModel):
    """reports/<task>/checks.json: the last check of each pair of stored versions, by pair (`v1->v2`)."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True, serialize_by_alias=True)
    schema_: Literal["s1flow/checks@1"] = Field(default="s1flow/checks@1", alias="schema")
    checks: dict[str, Checked] = {}


def pair(against: int, candidate: int | None) -> str:
    return f"v{against}" if candidate is None else f"v{against}->v{candidate}"


def _checks(reports_dir: Path, task_id: str) -> Path:
    return reports_dir / task_id / "checks.json"


def _read_checks(path: Path) -> ChecksFile:
    return ChecksFile.model_validate_json(path.read_text()) if path.exists() else ChecksFile()


def record(reports_dir: Path, task_id: str, key: str, verdict: Verdict, n: int, sample: int | None) -> None:
    path = _checks(reports_dir, task_id)
    got = _read_checks(path).checks | {key: Checked(verdict=verdict, n=n, sample=sample, at=clock.now())}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(ChecksFile(checks=dict(sorted(got.items()))).model_dump_json(indent=1) + "\n")


def last(reports_dir: Path, task_id: str, key: str) -> Checked | None:
    return _read_checks(_checks(reports_dir, task_id)).checks.get(key)
