"""A task's cases, read from two places in one shape (`Case`):

    tasks/<id>/<data>          the task's own rows (any JSON / JSONL shape), read by its `state` and `label`
    tasks/<id>/feedback.jsonl  cases from production, already in Case form (eval/feedback.py writes them)

and `tasks/<id>/corrections.jsonl` (`s1flow cases correct`) says what someone decided about a case's
label after reading it, kept apart so the collected label and the reason it changed both stay.
Everything downstream (runs, metrics, the evaluation set) sees cases only, with corrections applied.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any, Callable, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from ..client.state import State
from ..core.errors import DataError, invalid
from ..policies.kinds import Label

Row = dict[str, Any]
FEEDBACK = "feedback.jsonl"
CORRECTIONS = "corrections.jsonl"
SAMPLED = "review-sample.json"  # the cases `cases review --sample` drew, so a correction knows it read one
Verdict = Literal["relabel", "keep", "unclear", "missing"]
VERDICTS: dict[str, str] = {
    "relabel": "the question's criteria, as written, give another option",
    "keep": "the label is right; the models are wrong",
    "unclear": "the criteria do not settle it (two options fit, or none): not scored",
    "missing": "what decides it is not in the state (a linked PR, the code, a later event): not scored",
}


class Correction(BaseModel):
    """One line of corrections.jsonl: a decision about one case's label, by someone who read it. Appended; the
    latest line per id wins. `unclear` and `missing` leave the case out and are evidence about the task itself."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True, serialize_by_alias=True)
    schema_: Literal["s1flow/correction@1"] = Field(default="s1flow/correction@1", alias="schema")
    id: str
    verdict: Verdict
    label: Any = None  # relabel only: the new label
    was: Any  # the label as collected, when the decision was made
    reason: str
    by: str  # who decided
    at: str
    sampled: bool = False  # drawn by `s1flow cases review --sample` (review-sample.json), not read because it looked wrong

    @model_validator(mode="after")
    def _label_for_relabel(self) -> "Correction":
        if (self.verdict == "relabel") != (self.label is not None):
            raise ValueError("a relabel needs the new label, and only a relabel has one")
        return self


class ReviewSample(BaseModel):
    """tasks/<id>/review-sample.json: every case `cases review --sample` has drawn, so `cases correct` knows a
    correction of one counts toward the label error rate."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True, serialize_by_alias=True)
    schema_: Literal["s1flow/review-sample@1"] = Field(default="s1flow/review-sample@1", alias="schema")
    ids: list[str]


class FeedbackCase(BaseModel):
    """One line of feedback.jsonl: a state the app sent and the answer that turned out right."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True, serialize_by_alias=True)
    schema_: Literal["s1flow/feedback-case@1"] = Field(default="s1flow/feedback-case@1", alias="schema")
    id: str  # "prod:<case_id>"
    state: Any
    label: Label  # as the task labels it
    source: Literal["feedback"] = "feedback"
    at: str  # when the right answer was recorded
    policy: str  # the policy that answered it, its id <task>@vN


@dataclass(frozen=True)
class Case:
    id: str
    state: State  # as the task writes it (images not yet prepared)
    label: Any  # None: not scored
    source: Literal["data", "feedback"] = "data"
    text: str = ""  # one line in reports
    rationale: str | None = None  # why it got its label (shown to GEPA's reflection LM, never to the model)


@dataclass
class Cases:
    """Reads a task's cases as its task.py declares them (`Task.load_cases()` makes one)."""

    task_id: str
    dir: Path
    file: str  # the cases file, relative to dir; .json (array) or .jsonl
    state: Callable[[Row], State]
    label: Callable[[Row], Any]  # None excludes the row from scoring
    show: Callable[[Row], str] | None = None
    _all: list[Case] | None = field(default=None, init=False, repr=False)

    def all(self) -> list[Case]:
        """Every case, the task's rows first, then production's feedback, with corrections applied. Read once."""
        if self._all is None:
            fixes = self.corrections()
            self._all = [_corrected(c, fixes.get(c.id)) for c in self.collected()]
        return self._all

    def collected(self) -> list[Case]:
        """The cases as collected, before corrections."""
        return [*self._from_rows(), *self._from_feedback()]

    def corrections(self) -> dict[str, Correction]:
        """The latest correction per case id."""
        path = self.dir / CORRECTIONS
        if not path.exists():
            return {}
        out: dict[str, Correction] = {}
        for n, line in enumerate(path.read_text().splitlines(), 1):
            if line.strip():
                try:
                    c = Correction.model_validate_json(line)
                except ValidationError as e:
                    raise DataError(f"{self.task_id}: {CORRECTIONS} line {n}: {invalid(e)}") from None
                out[c.id] = c
        return out

    def labelled(self) -> list[Case]:
        return [c for c in self.all() if c.label is not None]

    def by_id(self) -> dict[str, Case]:
        return {c.id: c for c in self.all()}

    def data_sha256(self) -> str:
        """The task's data, its feedback and its corrections: what a policy was chosen on."""
        h = hashlib.sha256((self.dir / self.file).read_bytes())
        for extra in (self.dir / FEEDBACK, self.dir / CORRECTIONS):
            if extra.exists():
                h.update(extra.read_bytes())
        return h.hexdigest()

    def forget(self) -> None:
        """After feedback is added: read the cases again on next use."""
        self._all = None

    def _from_rows(self) -> list[Case]:
        path = (self.dir / self.file).resolve()
        try:
            text = path.read_text()
            rows = json.loads(text) if path.suffix == ".json" else [json.loads(l) for l in text.split("\n") if l.strip()]
        except (OSError, json.JSONDecodeError) as e:
            raise DataError(f"{self.task_id}: cannot read {path}: {e}") from None
        out = []
        for i, r in enumerate(rows):
            r["id"] = str(r.get("id", i))  # records and caches key on the string form
            try:
                out.append(Case(
                    id=r["id"], state=self.state(r), label=self.label(r),
                    text=self.show(r) if self.show else json.dumps(self.state(r), ensure_ascii=False),
                    rationale=r.get("rationale"),
                ))
            except KeyError as e:
                raise DataError(f"{self.task_id}: the case with id {r['id']!r} has no field {e.args[0]!r}, which task.py reads "
                                f"(in state, label or show); its fields: {', '.join(r)}") from None
            except (TypeError, ValueError) as e:
                raise DataError(f"{self.task_id}: the case with id {r['id']!r}: {type(e).__name__}: {e}") from None
        return out

    def _from_feedback(self) -> list[Case]:
        path = self.dir / FEEDBACK
        if not path.exists():
            return []
        out = []
        for line in path.read_text().splitlines():
            if line.strip():
                f = FeedbackCase.model_validate_json(line)
                out.append(Case(id=f.id, state=f.state, label=f.label, source="feedback",
                                text=json.dumps(f.state, ensure_ascii=False)[:120]))
        return out


def _corrected(c: Case, fix: Correction | None) -> Case:
    if fix is None or fix.verdict == "keep":
        return c
    return replace(c, label=fix.label if fix.verdict == "relabel" else None)
