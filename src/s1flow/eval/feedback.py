"""Join production labels to unique decisions and measure the observed labelled subset.

A case_id never identifies a call. Only decision_id plus the policy digest can
join feedback; ambiguous references are reported and excluded. Feedback share
measures observation, and cannot establish that labels are unbiased.
"""
from __future__ import annotations

import datetime as dt
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from pydantic import BaseModel, Field, TypeAdapter, ValidationError

from ..client.identity import digest, state_digest
from ..core import clock
from ..core.errors import ConfigError, DataError, NotFound
from ..policies import log
from ..policies.file import Ref
from ..policies.log import AnsweredLog, Decision, FailedLog, FeedbackLog
from . import evalset
from .cases import FEEDBACK, FeedbackCase
from .evaluation import Estimate
from .kinds import kind_of
from .objectives import measure
from .objectives.declare import Objective
from .objectives.measure import bound, cp_lower
from .shown import band, pct
from .task import Task

MIN_FEEDBACK_SHARE = 0.5  # a display threshold, never evidence of unbiased feedback
MISSING = object()


@dataclass
class Answered:
    case_id: str | None
    policy: str
    at: str
    decision: Decision
    state: Any = None
    label: Any = MISSING
    label_at: str | None = None


class JoinIssues(BaseModel):
    duplicates: int = 0
    unknown_feedback: int = 0
    policy_mismatch: int = 0
    conflicting_decisions: int = 0
    ambiguous_feedback: int = 0
    invalid_state: int = 0
    invalid_reference: int = 0


class Logs(BaseModel):
    answered: list[AnsweredLog] = Field(default_factory=list)
    failed: list[FailedLog] = Field(default_factory=list)
    feedback: list[FeedbackLog] = Field(default_factory=list)
    issues: JoinIssues = Field(default_factory=JoinIssues)

    def add(self, rec: AnsweredLog | FailedLog | FeedbackLog) -> None:
        if isinstance(rec, AnsweredLog):
            self.answered.append(rec)
        elif isinstance(rec, FailedLog):
            self.failed.append(rec)
        else:
            self.feedback.append(rec)


_LOG: TypeAdapter[AnsweredLog | FailedLog | FeedbackLog] = TypeAdapter(log.Log)


def _otel_value(v: dict[str, Any]) -> Any:
    for k in ("stringValue", "boolValue", "doubleValue"):
        if k in v:
            return v[k]
    if "intValue" in v:
        return int(v["intValue"])
    return None


def _spans(obj: dict[str, Any]) -> list[tuple[str, str, dict[str, Any]]]:
    out = []
    for rs in obj.get("resourceSpans", []):
        for ss in rs.get("scopeSpans", []):
            for sp in ss.get("spans", []):
                at = clock.stamp(dt.datetime.fromtimestamp(int(sp.get("startTimeUnixNano", 0)) / 1e9, dt.timezone.utc), ms=True)
                out.append((sp.get("name", ""), at, {a["key"]: _otel_value(a["value"]) for a in sp.get("attributes", [])}))
    return out


def read(paths: list[Path]) -> Logs:
    logs = Logs()
    for path in paths:
        for n, line in enumerate(path.read_text().splitlines(), 1):
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
                if "resourceSpans" in obj:
                    for name, at, attrs in _spans(obj):
                        rec = log.from_span(name, at, attrs)
                        if rec is not None:
                            logs.add(rec)
                else:
                    logs.add(_LOG.validate_python(obj))
            except (ValidationError, ValueError, KeyError, TypeError) as e:
                raise DataError(f"{path}:{n}: invalid log record: {e}") from None
    return logs


def _unique(records: list[Any], issues: JoinIssues) -> list[Any]:
    seen: set[str] = set()
    out = []
    for rec in records:
        key = rec.model_dump_json(by_alias=True)
        if key in seen:
            issues.duplicates += 1
        else:
            seen.add(key)
            out.append(rec)
    return out


def cases(task: Task, logs: Logs) -> list[Answered]:
    """One row per unambiguous decision; corrections use the latest label for that exact decision."""
    issues = JoinIssues()
    answers = _unique(logs.answered, issues)
    feedback = _unique(logs.feedback, issues)
    _unique(logs.failed, issues)
    # Keep all IDs for diagnosing a reference to a decision from a different task/policy.
    def belongs(ref: str) -> bool:
        try:
            return Ref.parse(ref).task == task.id
        except ConfigError:
            issues.invalid_reference += 1
            return False

    by_id: dict[str, AnsweredLog] = {}
    signatures: dict[str, str] = {}
    conflicts: set[str] = set()
    for rec in answers:
        d = rec.decision
        key = d.decision_id
        if rec.state is not None and state_digest(rec.state) != rec.state_sha256:
            conflicts.add(key)
            issues.invalid_state += 1
        signature = digest({"policy": d.policy, "policy_digest": d.policy_digest, "execution": d.execution_digest,
                            "state": rec.state_sha256, "reading": d.model_dump(include={"value", "probability", "p_positive", "below_min_probability"})})
        if key in signatures and signatures[key] != signature:
            conflicts.add(key)
        else:
            signatures[key] = signature
            # State from this same unique decision may be retained by JSONL but omitted by OTel.
            if key not in by_id or (by_id[key].state is None and rec.state is not None):
                by_id[key] = rec
    issues.conflicting_decisions = len(conflicts)
    labels: dict[str, FeedbackLog] = {}
    ambiguous: set[str] = set()
    for f in sorted(feedback, key=lambda f: f.at):
        if not belongs(f.policy):
            continue
        rec = by_id.get(f.decision_id)
        if rec is None:
            issues.unknown_feedback += 1
            continue
        if f.decision_id in conflicts:
            continue
        d = rec.decision
        if f.policy != d.policy or f.policy_digest != d.policy_digest:
            issues.policy_mismatch += 1
            continue
        old = labels.get(f.decision_id)
        if old and old.at == f.at and old.label != f.label:
            ambiguous.add(f.decision_id)
        elif old is None or old.at < f.at:
            ambiguous.discard(f.decision_id)
        labels[f.decision_id] = f
    issues.ambiguous_feedback = len(ambiguous)
    logs.issues = issues
    out = []
    for key, rec in by_id.items():
        if key in conflicts or not belongs(rec.decision.policy):
            continue
        c = Answered(rec.case_id, rec.decision.policy, rec.at, rec.decision, state=rec.state)
        if (f := labels.get(key)) is not None and key not in ambiguous:
            c.label, c.label_at = f.label, f.at
        out.append(c)
    return out


def valid(task: Task, label: Any) -> bool:
    return task.kind.label_error(label) is None


class InProduction(BaseModel):
    """Descriptive metrics only on the observed labelled decisions, with the adopted primary objective."""
    policy: str
    answered: int
    failed: int
    with_feedback: int
    feedback_share: float
    accuracy: Estimate
    correct: int
    sure_accuracy: Estimate
    sure_n: int
    primary: Objective | None = None
    objective: Estimate = Estimate(value=None)
    below: bool | None
    comparison_reason: str | None = None
    observed_subset: str = "decisions with valid feedback labels; selection bias is unknown"


def _rate(k: int, n: int, show_interval: bool) -> Estimate:
    if not n:
        return Estimate(value=None)
    ci = (cp_lower(k, n, 0.975), 1 - cp_lower(n - k, n, 0.975)) if show_interval else None
    return Estimate(value=k / n, interval=ci)


def _objective_estimate(b: measure.Bound, pairs: measure.Pairs, show_interval: bool, seed: int) -> Estimate:
    value = b.value(pairs) if len(pairs) else None
    draws: list[float] = []
    if show_interval and value is not None:
        rng = np.random.default_rng(seed)
        for _ in range(measure.HEAVY if b.heavy else measure.BOOTSTRAP):
            v = b.value(pairs[rng.integers(0, len(pairs), len(pairs))])
            if v is not None and np.isfinite(v):
                draws.append(v)
    return Estimate(value=value, interval=measure.interval(draws))


def production(task: Task, cs: list[Answered], failed: list[FailedLog]) -> list[InProduction]:
    """Measure the adopted objective and rule, never substitute accuracy for its comparison."""
    out = []
    failure_events = {f.model_dump_json(): f for f in failed}
    for ref in sorted({c.policy for c in cs} | {f.policy for f in failure_events.values() if Ref.parse(f.policy).task == task.id}):
        rows = [c for c in cs if c.policy == ref]
        primary = None
        objective = Estimate(value=None)
        below = None
        reason = None
        kind = task.kind
        adopted = None
        try:
            adopted = task.policies.get(Ref.parse(ref))
            kind = kind_of(adopted.spec.question, adopted.spec.asked.kind)
        except (ConfigError, NotFound) as e:
            reason = f"adoption evidence unavailable: {e}"
        known = [c for c in rows if c.label is not MISSING and kind.label_error(c.label) is None]
        p = measure.pairs(kind, [c.label for c in known], [c.decision for c in known])
        share = len(known) / len(rows) if rows else 0.0
        show_interval = share >= MIN_FEEDBACK_SHARE
        correct, sure = int(p.correct.sum()), int(p.sure.sum())
        acc = _rate(correct, len(known), show_interval)
        sure_acc = _rate(int((p.sure & p.correct).sum()), sure, show_interval)
        if adopted is not None:
            score = adopted.evidence.evaluation.primary
            primary = score.objective if score is not None else None
            if primary is None:
                reason = "adoption evidence has no primary objective"
            elif any(c.decision.policy_digest != adopted.spec.digest or
                     c.decision.execution_digest != adopted.evidence.execution_digest for c in rows):
                reason = "logged policy or execution identity differs from the adoption evidence"
            elif primary.code_sha256 and (primary.key not in task.custom or
                                          task.custom[primary.key].objective.code_sha256 != primary.code_sha256):
                reason = "adopted custom objective code differs or is unavailable; evidence cannot be reused"
            else:
                b = bound(primary, kind, task.custom_measures)
                objective = _objective_estimate(b, p, show_interval, task.split.seed)
                if b.constraint is not None and show_interval and len(p):
                    k, n = b.constraint.count(p)
                    below = b.constraint.broken(k, n, 0.975) if n else None
                elif objective.interval is not None and score is not None and score.interval is not None:
                    below = (objective.interval[1] < score.interval[0] if primary.maximize
                             else objective.interval[0] > score.interval[1])
        out.append(InProduction(
            policy=ref, answered=len(rows), failed=sum(f.policy == ref for f in failure_events.values()),
            with_feedback=len(known), feedback_share=share, accuracy=acc, correct=correct,
            sure_accuracy=sure_acc, sure_n=sure, primary=primary, objective=objective, below=below,
            comparison_reason=reason,
        ))
    return out


# ---------- new labelled cases ----------


class Added(BaseModel):
    added: int
    no_state: int
    no_label: int
    invalid_label: int
    already: int
    notes: list[str] = []


def add(task: Task, cs: list[Answered], dry_run: bool = False) -> Added:
    """Append verified decision/input/label pairs (each decision_id once)."""
    path = task.dir / FEEDBACK
    have = {FeedbackCase.model_validate_json(l).id for l in path.read_text().splitlines() if l.strip()} if path.exists() else set()
    rows: list[FeedbackCase] = []
    counts = {"no_state": 0, "no_label": 0, "invalid_label": 0, "already": 0}
    for c in cs:
        cid = f"prod:{c.decision.decision_id}"
        if c.label is MISSING:
            counts["no_label"] += 1
        elif not valid(task, c.label):
            counts["invalid_label"] += 1
        elif c.state is None:
            counts["no_state"] += 1
        elif cid in have:
            counts["already"] += 1
        else:
            have.add(cid)
            rows.append(FeedbackCase(id=cid, state=c.state, label=c.label, at=clock.stamp(dt.datetime.fromisoformat(c.label_at or c.at)),
                                     policy=c.policy))
    notes: list[str] = []
    if rows and not dry_run:
        with path.open("a") as f:
            f.writelines(r.model_dump_json() + "\n" for r in rows)
        task.load_cases().forget()
        notes = evalset.ensure(task)[1] if evalset.read(task) else []  # new cases get their share of test
    return Added(added=len(rows), notes=notes, **counts)


def markdown(task: Task, prod: list[InProduction], added: Added, *, issues: JoinIssues | None = None) -> str:
    def shown(e: Estimate) -> str:
        return "—" if e.value is None else f"{e.value:.3f}{band(e.interval) if e.interval else ' (no interval)'}"

    lines = [f"# {task.id} · production", "",
             "Measured only on decisions with observed valid feedback. The feedback share cannot establish absence of selection bias. "
             f"Under {pct(MIN_FEEDBACK_SHARE)} with feedback, intervals are omitted. Intervals describe sampling uncertainty within this subset only.", "",
             "| policy | answered | failed | with feedback | adopted objective | observed value | accuracy |",
             "|---|---|---|---|---|---|---|"]
    for row in prod:
        label = row.primary.label if row.primary else "unavailable"
        lines.append(f"| {row.policy} | {row.answered} | {row.failed} | {pct(row.feedback_share)} ({row.with_feedback}) | {label} | {shown(row.objective)} | {shown(row.accuracy)} |")
        if row.comparison_reason:
            lines.append(f"- {row.policy}: no adoption comparison: {row.comparison_reason}")
        if row.below:
            constraint = bound(row.primary, task.kind, task.custom_measures).constraint if row.primary else None
            why = f" ({constraint.shown_broken})" if constraint is not None else ""
            lines.append(f"- **{row.policy} is below its adopted objective in the observed feedback subset**{why}. Revisit the question or model.")
    lines += ["", f"- Added {added.added} new cases. Not added: no input {added.no_state}, no feedback {added.no_label}, "
              f"invalid label {added.invalid_label}, added before {added.already}", *[f"- {x}" for x in added.notes]]
    if added.no_state:
        lines.append("- To add those, keep the state in the log: `s1flow decide --log FILE --keep-state`, the decide Action's `keep-state: true`, or `DecisionPolicy(..., log=FILE, keep_state=True)`")
    if issues is not None:
        counts = ", ".join(f"{key.replace('_', ' ')} {value}" for key, value in issues.model_dump().items() if value)
        if counts:
            lines += ["", f"- Log join diagnostics (excluded where ambiguous): {counts}"]
    return "\n".join(lines) + "\n"
