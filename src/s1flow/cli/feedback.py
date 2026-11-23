"""`s1flow feedback record` and `feedback import` (the base install), and `s1flow feedback measure` (s1flow[eval])."""

import argparse
import csv
import io
import json
import warnings
from pathlib import Path
from typing import Any

from ..core.errors import ConfigError, DataError
from .common import POLICY, Parser, command, label, policy_root, project


def feedback_record(a: argparse.Namespace) -> int:
    from ..policies.policy import record_feedback, resolve

    record_feedback(resolve(a.policy, path=a.path, root=policy_root(a)), a.decision_id, label(a.label), log=a.log)
    return 0


def feedback_import(a: argparse.Namespace) -> int:
    """Every label in the file, or none: each row is checked against the policy's question (and against the decision
    the log holds under its id) before any is written."""
    from ..policies.log import FeedbackLog
    from ..policies.policy import feedback_event, resolve, write_feedback

    spec = resolve(a.policy, path=a.path, root=policy_root(a))
    rows = _label_rows(Path(a.file))
    if not rows:
        raise DataError(f"{a.file}: no labels in it")
    decided = _decided(Path(a.log))
    events: list[FeedbackLog] = []
    wrong: list[str] = []
    seen: dict[str, FeedbackLog] = {}
    for line, decision_id, value in rows:
        try:
            event = feedback_event(spec, decision_id, value)
        except ConfigError as e:
            wrong.append(f"line {line}: {e}")
            continue
        by = decided.get(decision_id)
        if by is not None and by[0] != spec.ref:
            wrong.append(f"line {line}: decision {decision_id} was made by {by[0]}, not {spec.ref}: import its labels under that policy")
        elif by is not None and by[1] != spec.digest:
            wrong.append(f"line {line}: decision {decision_id} was made by another {spec.ref} than this one (its digest differs): "
                         "name the policy file the app decided with (--path)")
        elif (first := seen.get(decision_id)) is not None:
            if first.label != event.label:
                wrong.append(f"line {line}: decision {decision_id} already has the label {first.label!r} in this file")
        else:
            seen[decision_id] = event
            events.append(event)
    if wrong:
        more = f"; and {len(wrong) - 20} more" if len(wrong) > 20 else ""
        raise DataError(f"{a.file}: nothing recorded; fix these rows: " + "; ".join(wrong[:20]) + more)
    unknown = [e.decision_id for e in events if e.decision_id not in decided]
    if unknown:
        warnings.warn(f"{len(unknown)} of the {len(events)} decision ids are not in {a.log} (first: {unknown[0]}): "
                      "`feedback measure` counts them as unknown unless their decisions are in a log it reads")
    write_feedback(events, log=a.log)
    print(f"recorded {len(events)} labels for {spec.ref} in {a.log}")
    return 0


def _label_rows(path: Path) -> list[tuple[int, str, Any]]:
    """(line, decision_id, label) from a CSV with a header naming decision_id and label (other columns are left
    alone), or JSON Lines of {"decision_id": ..., "label": ...}. A CSV label is read as `feedback record` reads it."""
    try:
        text = path.read_text(encoding="utf-8-sig")
    except OSError as e:
        raise ConfigError(f"{path}: {e.strerror or e}") from None
    except UnicodeDecodeError:
        raise DataError(f"{path}: not UTF-8 text; save it as UTF-8 (CSV UTF-8 in a spreadsheet)") from None
    if path.suffix.lower() == ".csv":
        reader = csv.DictReader(io.StringIO(text, newline=""), strict=True)  # an unclosed quote must not swallow rows
        if not {"decision_id", "label"} <= set(reader.fieldnames or ()):
            raise DataError(f"{path}: the header needs the columns decision_id and label, got {', '.join(reader.fieldnames or ()) or 'none'}")
        rows = []
        start = reader.line_num + 1
        try:
            for r in reader:  # a row's line is the one it starts on (a quoted cell may span lines)
                if any((v or "").strip() for k, v in r.items() if k is not None):  # a spreadsheet's trailing `,,` rows are blank
                    rows.append((start, (r["decision_id"] or "").strip(), label((r["label"] or "").strip())))
                start = reader.line_num + 1
        except csv.Error as e:
            raise DataError(f"{path}: the row from line {start} is not valid CSV ({e}); nothing recorded") from None
        return rows
    if path.suffix.lower() != ".jsonl":
        raise ConfigError(f"{path}: give a .csv (columns decision_id, label) or a .jsonl file")
    out = []
    for n, raw in enumerate(text.splitlines(), 1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except ValueError as e:
            raise DataError(f"{path}:{n}: not JSON: {e}") from None
        if not isinstance(row, dict) or not {"decision_id", "label"} <= row.keys():
            raise DataError(f'{path}:{n}: a line is {{"decision_id": ..., "label": ...}}')
        out.append((n, row["decision_id"], row["label"]))
    return out


def _decided(log: Path) -> dict[str, tuple[str, str]]:
    """The policy (ref, digest) behind each decision the log already holds; empty when it holds none."""
    from ..policies.log import AnsweredLog

    out: dict[str, tuple[str, str]] = {}
    if not log.is_file():
        return out
    with log.open(encoding="utf-8", errors="replace") as lines:
        for raw in lines:
            if '"answered"' not in raw:
                continue
            try:
                d = AnsweredLog.model_validate_json(raw).decision
            except ValueError:
                continue  # `feedback measure` reports a broken line; this only cross-checks
            out[d.decision_id] = (d.policy, d.policy_digest)
    return out


def feedback_measure(a: argparse.Namespace) -> int:
    """Each policy in production, from the feedback in its logs; with --add, the cases with a kept state added as
    labelled cases."""
    from ..eval import feedback as fb  # s1flow[eval]: the task, its cases and objectives
    from ..eval.task import load

    task = load(project(a), a.task)
    found = fb.read([Path(x) for x in a.logs])
    cs = fb.cases(task, found)
    prod = fb.production(task, cs, found.failed)
    added = fb.add(task, cs, write=a.add)
    if a.json:
        print(json.dumps({"production": [x.model_dump(mode="json") for x in prod], "added": added.model_dump(mode="json"), "issues": found.issues.model_dump(mode="json")}))
    else:
        print(fb.markdown(task, prod, added, issues=found.issues))
    return 1 if any(v.below for v in prod) else 0


def add(sub: Any) -> None:
    group = sub.add_parser("feedback", context=("project", "connections"), help="record the right answer for a case a policy decided (record, or import from a file), or measure policies in production (measure)").add_subparsers(
        dest="action", required=True, parser_class=Parser)
    f = command(group, "record", feedback_record, context=("project",), help="record the right answer for a case a policy decided",
                description="Record the right answer for a case, joined to its answer by decision_id (what `s1flow feedback measure` measures from). "
                            "It calls no model, so it takes no connections.")
    f.add_argument("policy", metavar=POLICY, help="the policy that decided it (its id in the log, or the task: the current version)")
    f.add_argument("decision_id", help="the exact decision_id returned by decide")
    f.add_argument("label", help="the right answer: a class key, true / false, a level (2), or a box as JSON")
    f.add_argument("--log", required=True, help="the log to append to (JSONL)")
    f.add_argument("--path", help="a policy file, or a policy set from `s1flow export` (policies.json), instead of policies/ (as decide --path)")
    i = command(group, "import", feedback_import, context=("project",), help="record many right answers at once, from a file of decision ids and labels",
                description="Record the right answers in a file at once: a CSV whose header has decision_id and label (other "
                            "columns are ignored), or JSON Lines of {\"decision_id\": ..., \"label\": ...}. Every row is checked "
                            "first; if one is wrong, nothing is recorded. A decision the log already holds must be this policy's. "
                            "It calls no model, so it takes no connections.")
    i.add_argument("policy", metavar=POLICY, help="the policy that decided them (its id in the log, or the task: the current version)")
    i.add_argument("file", help="the labels: a .csv or .jsonl file")
    i.add_argument("--log", required=True, help="the log to append to (JSONL); the decision log itself keeps them together")
    i.add_argument("--path", help="a policy file, or a policy set from `s1flow export` (policies.json), instead of policies/ (as decide --path)")
    m = command(group, "measure", feedback_measure, context=("project", "connections"), help="measure each policy in production from the feedback in its logs (needs s1flow[eval])",
                description="Measure each policy in production from the feedback in its logs; with --add, also add the cases with a "
                            "kept state as labelled cases. Exit 1 when production is shown below. Needs s1flow[eval].")
    m.add_argument("task")
    m.add_argument("logs", nargs="+", help="SDK logs (JSONL) or OpenTelemetry JSON exports")
    m.add_argument("--add", action="store_true", help="also add the cases with a kept state and a valid label to tasks/<task>/feedback.jsonl")
    m.add_argument("--json", action="store_true")
