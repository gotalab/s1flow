"""`s1flow report`: every candidate on the saved runs by the task's objective; with no task, every task's current
version and why."""

from __future__ import annotations

import argparse
import json
import sys
import unicodedata
from pathlib import Path
from typing import Any, Callable

from ..core.errors import ConfigError, S1flowError
from .common import command, positive, project, shown


def report(a: argparse.Namespace) -> int:
    """Read the saved runs by the task's objective: every candidate on every question variant, best first, those the
    objective cannot tell apart marked (no pick: a person or an agent picks). No model is called and nothing is written
    but, with --out DIR, the comparison snapshot and a Markdown report per question. --from reads a saved snapshot
    offline. With no TASK, every task: its current version and why."""
    from ..eval import adopt as adopting
    from ..eval import comparison
    from ..eval import report as reporting
    from ..eval.task import load

    if a.offset < 0:
        raise ConfigError("--offset is 0 or more")
    if a.from_path and a.task:
        raise ConfigError("report takes TASK or --from PATH, not both")
    snapshot = Path(a.from_path) if a.from_path else None
    task, listed, unranked = None, None, None
    if snapshot is not None:
        for option in ("project", "connections"):
            if getattr(a, option, None) is not None:
                raise ConfigError(f"--{option} does not apply with --from; the saved snapshot is self-contained")
        if a.out:
            raise ConfigError("--out writes a report of the current runs; with --from the snapshot is already saved")
    else:
        if not a.task:  # every task: what runs, and why
            from ..eval.policy import overview

            if a.candidate or a.out:
                raise ConfigError("--candidate and --out take a TASK")
            return _print_tasks(overview(project(a)), a.json)
        task = load(project(a), a.task)
        if a.candidate is None:
            try:
                listed = adopting.shortlist(task)
            except ConfigError:
                raise
            except S1flowError as e:  # nothing to rank yet (no complete runs, a question no policy ships): still show what there is
                unranked = str(e.args[0] if e.args else e)
    snapshot_name = str(snapshot) if snapshot else None
    result = None
    if snapshot is not None:
        result = comparison.read(snapshot)
    else:
        assert task is not None
        result = comparison.collect(task, include_charts=bool(a.out))

    if a.out:
        assert task is not None and result is not None
        out = Path(a.out)
        if out.exists() and not out.is_dir():
            raise ConfigError(f"--out takes a directory; {out} is a file")
        out.mkdir(parents=True, exist_ok=True)
        (out / "comparison.json").write_text(result.model_dump_json(by_alias=True, indent=1) + "\n")
        wrote = [out / "comparison.json"]
        for variant in ["base", *task.variants]:
            if reporting.available_models(task, variant):
                reporting.write(task, variant, out / "questions")  # apart from comparison.json, whatever a variant is named
                wrote += [out / "questions" / f"{variant}.md", out / "questions" / f"{variant}.json"]
        print("wrote " + ", ".join(shown(p) for p in wrote), file=sys.stderr)

    if a.candidate:
        assert result is not None
        if a.json:
            print(json.dumps(comparison.summary(result, candidate=a.candidate, snapshot=snapshot_name), ensure_ascii=False, indent=1))
        else:
            print(comparison.text(result, candidate=a.candidate, snapshot=snapshot_name))
        return 0
    if a.json:
        assert result is not None
        payload = comparison.summary(result, offset=a.offset, limit=a.limit, snapshot=snapshot_name)
        if task is not None:  # the ranking: the candidates ordered by the task's objectives and constraints
            payload["ranking"] = None if listed is None else [r.model_dump(mode="json") for r in listed.rows()[a.offset:a.offset + a.limit]]
            if listed is not None:  # what orders the `tied` rows; with nothing in `by` their order says nothing
                payload["order"] = listed.order().model_dump(mode="json")
            if unranked:
                payload["unranked"] = unranked
        print(json.dumps(payload, ensure_ascii=False, indent=1))
        return 0
    if listed is not None:
        assert task is not None and result is not None
        rows = listed.rows()
        _print_shortlist(task.id, rows[a.offset:a.offset + a.limit], listed.order())
        if len(rows) > a.offset + a.limit:
            print(f"  … {len(rows) - a.offset - a.limit} more: --offset {a.offset + a.limit}")
        ranked = {r.candidate for r in rows}
        if left := [f"{r.candidate} ({', '.join(r.excluded) or 'incomplete'})" for r in result.candidates if r.candidate not in ranked]:
            print(f"not ranked: {'; '.join(left)}")
        if outside := [f"{r.candidate} ({', '.join(r.excluded)})" for r in rows if r.excluded]:
            print(f"outside the constraints: {'; '.join(outside)}")
        _print_weights(listed)
        print(f"Every metric of each candidate: s1flow report {task.id} --json, or --candidate NAME; "
              f"the snapshot and a Markdown report: s1flow report {task.id} --out DIR")
        return 0
    assert result is not None
    print(comparison.text(result, offset=a.offset, limit=a.limit, snapshot=snapshot_name))
    if unranked:
        print(f"not ranked: {unranked}")
    return 0


def _print_tasks(found: list[Any], as_json: bool) -> int:
    if as_json:
        print(json.dumps([t.model_dump(mode="json") for t in found], indent=1))
        return 0
    table = [["task", "current", "candidate", "model version", "answered by", "pin"]]
    for t in found:
        rows = [[t.task, r.policy, r.candidate or "-", r.model_version or "-", r.answered_by or "-", r.pin or "?"]
                for r in t.policies if r.current]
        table += rows or [[t.task, "-", "-", "-", "-", "-"]]
    widths = [max(len(row[i]) for row in table) for i in range(len(table[0]))]
    for row in table:
        print("  ".join(x.ljust(w) for x, w in zip(row, widths)).rstrip())
    for t in found:
        if t.why is not None:
            w = t.why
            print(f"{t.task}: v{w.version} by {w.by}, {w.at[:10]} ({w.action}"
                  + (f" from v{w.previous}" if w.previous else "") + f"): {w.reason}")
    print("pin: yes the policy sends a version by its name; no its model serves one version; alias the model's version "
          "can change; ? s1flow.toml no longer has the model. Every version, its date and digest, and why current is what it "
          "is: --json; every switch: policies/<task>/history.jsonl.")
    return 0


def _print_shortlist(task_id: str, rows: list[Any], order: Any) -> None:
    from ..eval.shown import ms, pct, usd

    def score(s: Any) -> str:
        if s.value is None:
            return "-"
        f: Callable[[float], str] = (lambda v: pct(v, 1, sign="")) if s.objective.unit == "share" else (lambda v: f"{v:.3g}")
        return f(s.value) if s.interval is None else f"{f(s.value)} [{f(s.interval[0])}, {f(s.interval[1])}]"

    def cost(v: float | None, source: str | None) -> str:
        return "-" if v is None else "free" if v == 0 else ("~" if source in ("list", "mixed") else "") + usd(v, 2)

    tied = [r for r in rows if r.tied]
    labels = [s.objective.label for s in rows[0].scores] if rows else []
    # the objectives (measured on the answers) | what the calls took | the model
    head = ["", "candidate", "n", *labels, "|", "p50", "p90", "p99", "API $/10k", "|", "pin", "limit"]
    table = [head]
    for r in rows:
        if r.excluded:
            continue
        lat = r.calls.latency
        table.append(["=" if r.tied else "", r.candidate, str(r.n), *(score(s) for s in r.scores), "|",
                      ms(lat and lat.p50_ms), ms(lat and lat.p90_ms), ms(lat and lat.p99_ms), cost(r.calls.cost_per_10k_usd, r.calls.cost_source), "|",
                      r.pin, "" if r.per_minute is None else f"{r.per_minute}/min"])

    def width(c: str) -> int:  # a CJK character takes two columns
        return sum(2 if unicodedata.east_asian_width(ch) in "WF" else 1 for ch in c)

    widths = [max(width(row[i]) for row in table) for i in range(len(head))]
    print(f"{task_id}: {len(table) - 1} candidates within the constraints, {len(tied)} the primary objective cannot tell apart at the top (=), "
          + (f"ordered by task.py's tiebreak: {', then '.join(order.by)}" if order.by else
             "listed by name, unordered: task.py's tiebreak would order them" if not order.skipped else
             "in the primary objective's order: task.py's tiebreak was skipped")
          + (f" ({order.why})" if order.why else ""))
    for row in table:
        print("  " + "  ".join(c + " " * (w - width(c)) for c, w in zip(row, widths)).rstrip())
    for r in rows:
        if r.excluded:
            print(f"  excluded: {r.candidate} ({', '.join(r.excluded)})")
    print("Measured on train + val; the held-out test is read only for the one you pick. Left of the first |: the objectives, "
          "measured on the answers (n: the labelled train + val cases it answered); then latency per call and API cost per 10,000 cases, measured on the calls. "
          "pin: yes a version, no a model that serves one, alias a model whose version can change (not adoptable: run name:<version>).")
    if refused := [r for r in rows if r.refused]:
        print("refused: " + ", ".join(f"{r.candidate} {r.refused} cases" for r in refused)
              + ": the model's limit (a refusal or an input it does not take), not a failed call; left out of its n.")
    if any(r.calls.cost_source in ("list", "mixed") for r in rows):
        print("~$: an estimated API cost, recorded tokens times s1flow.toml's list price, not a bill"
              + ("; billed API costs are listed beside them, so compare with care." if any(r.calls.cost_source == "billed" for r in rows) else "."))
    print(f'Adopt one: s1flow adopt {task_id} <candidate> --reason "..."')


def _print_weights(listed: Any) -> None:
    """ExpectedLoss or a loss table as the objective: the candidates tied at the top with its weights halved and doubled."""
    from ..eval.weights import decides

    if not listed.reweighted:
        return
    now = sorted(listed.tied)
    for r in listed.reweighted:
        print(f"weights x{r.factor:g} ({r.objective.label}): tied at the top {', '.join(r.tied) or '-'}")
    print("The candidates tied at the top change with the weights: they decide the choice, and they are yours to set." if decides(now, listed.reweighted)
          else "Halving or doubling the weights leaves the candidates tied at the top as they are.")


def add(sub: Any) -> None:
    p = command(sub, "report", report, context=("project", "connections"))
    p.add_argument("task", nargs="?", help="the task (or --from PATH); none: every task, its current version and why")
    p.add_argument("--json", action="store_true", help="every metric of each candidate, and the ranking, as JSON")
    p.add_argument("--limit", type=positive, default=12, help="candidates shown, in the ranking and the list (default: 12)")
    p.add_argument("--offset", type=int, default=0, help="candidates to skip (default: 0)")
    p.add_argument("--candidate", help="one candidate in full: model[:version][/variant]")
    p.add_argument("--out", type=Path, metavar="DIR", help="write comparison.json (with the chart series) and questions/<variant>.md / .json for each question")
    p.add_argument("--from", dest="from_path", type=Path, metavar="PATH", help="read a saved comparison.json offline")
