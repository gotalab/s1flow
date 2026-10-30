"""Reports: <out>/<variant>.md and <variant>.json (`s1flow report --out DIR` writes them to DIR/questions/), from the evaluations alone. What was measured
on the answers (the comparison, the objectives) and what the calls took (latency, API cost) are separate sections."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from collections import Counter

from ..core import clock
from .kinds import Kind
from .evaluation import ChartData, ChartSummary, Estimate, Evaluation, Floor, ObjectiveScore, cost_note
from .objectives import measure
from .objectives.declare import Objective
from .objectives.measure import bound
from . import evalset, metrics
from .run import ask_again
from .select import Ranked, rank, unlike_among_tied
from .shown import band, num, pct, usd
from .cases import Case
from .task import Task


def esc(s: str) -> str:
    return s.replace("|", "\\|").replace("\n", " ")


def show(case: Case, limit: int = 70) -> str:
    text = esc(case.text)
    return text if len(text) <= limit else text[: limit - 1] + "…"


def available_models(task: Task, variant: str) -> list[str]:
    d = task.where.runs_dir / task.id / variant
    return sorted(p.stem for p in d.glob("*.jsonl")) if d.exists() else []


def fmt(kind: Kind, o: Objective, sc: ObjectiveScore, with_ci: bool = True) -> str:
    """An objective's value as the report writes it (by its unit), with its constraint where that has no column of its own."""
    if sc.value is None:
        return "—"
    if o.unit == "share":
        c = None if o.code_sha256 else bound(o, kind).constraint  # a custom one holds no constraint
        beside = f" ({c.beside} {pct(sc.constraint, 1)})" if c and c.beside and sc.constraint is not None else ""
        return pct(sc.value) + (band(sc.interval) if with_ci and sc.interval else "") + beside
    within = f" [{sc.interval[0]:.3f}, {sc.interval[1]:.3f}]" if with_ci and sc.interval else ""
    return f"{sc.value:.3f}{within}"


def _p99(e: Evaluation) -> float | None:
    return e.calls.latency.p99_ms if e.calls.latency else None


SOURCE = {"billed": "billed", "list": "estimated", "mixed": "billed and estimated", None: "unknown"}  # Calls.cost_source


def compared(evs: list[Evaluation]) -> list[Evaluation]:
    """The candidates the report ranks: those with an answer to every labelled case but the ones they refused. One
    never asked some cases, or whose every call failed on some, is scored on the rest only (rank leaves it out too)."""
    return [e for e in evs if e.n and not e.failures.missing]


def left_out(task: Task, evs: list[Evaluation]) -> list[str]:
    gaps = [e for e in evs if e.n and e.failures.missing]
    if not gaps:
        return []
    why = lambda f: " and ".join(x for x in (f"{f.never_asked} cases never asked" if f.never_asked else "",
                                             f"{f.failed_cases} cases whose every call failed" if f.failed_cases else "") if x)
    return ["", "Not compared: " + "; ".join(f"{e.candidate.name} ({why(e.failures)})" for e in gaps)
            + ". With cases it has no answer to, a candidate is measured on the rest only, not on the cases the others answered,"
            + " so it is neither ranked nor chosen. Ask them again: "
            + f"`{ask_again(task, [(e.candidate.model, e.candidate.variant) for e in gaps])}`"]


def headline(task: Task, evs: list[Evaluation]) -> str:
    """The candidate the task's objectives and constraints choose (select.rank), and why."""
    scored = compared(evs)
    if not scored:
        return "No candidate has an answer to every case." if any(e.n for e in evs) else "No results."
    objs = task.objectives
    o0 = objs[0]
    ranked = rank(task.primary, task.ties, task.constraints, scored)
    by = {e.candidate.name: e for e in scored}
    fits = [x for x in ranked if not x.excluded and x.scores[0].value is not None]
    excluded = [x for x in ranked if x.excluded]
    if not fits:
        return "No model meets the constraints (" + "; ".join(f"{x.candidate}: {', '.join(x.excluded)}" for x in excluded) + ")."
    chosen = fits[0]
    sign = -1.0 if o0.maximize else 1.0
    leader = min(fits, key=lambda x: sign * (x.scores[0].value or 0.0))  # fits all have a value
    tied = [x for x in fits if x.tied_with_best]

    def tail(x: Ranked) -> str:
        e = by[x.candidate]
        bits = [f"API cost {usd(e.calls.cost_per_10k_usd)} per 10k"] if e.calls.cost_per_10k_usd is not None else []
        bits += [f"p99 {_p99(e):.0f}ms"] if _p99(e) else []
        return f" ({', '.join(bits)})" if bits else ""

    limits = [k for k, v in (("p99", task.constraints.latency_p99_ms), ("API cost", task.constraints.cost_per_10k_usd), ("labels", task.constraints.min_labels)) if v is not None]
    pre = f"Among the models within the constraints ({', '.join(limits)}), " if limits else ""
    parts = [f"{pre}**{leader.candidate}** has the {'highest' if o0.maximize else 'lowest'} {o0.label}, {fmt(task.kind, o0, leader.scores[0])}{tail(leader)}."]
    others = [x.candidate for x in tied if x is not leader]
    if others:
        parts.append(f"Its interval overlaps with {', '.join(others)}: the selection heuristic groups them for tiebreaking; interval overlap does not establish equivalence.")
        unlike = unlike_among_tied(ranked, scored) if "latency" in task.ties else None
        if chosen is not leader:
            words = [t.label if not isinstance(t, str) else "API cost" if t == "cost" else "p90 latency"
                     for t in task.ties if not (t == "latency" and unlike)]
            if words == ["API cost"]:
                parts.append(f"Of those, the lowest API cost is chosen: **{chosen.candidate}**{tail(chosen)}.")
            else:
                parts.append(f"Of those, compared by {', then '.join(words)}, **{chosen.candidate}** is chosen{tail(chosen)}.")
        if unlike:
            said = unlike.en(task.id)
            parts.append(said[0].upper() + said[1:] + ".")
    for x in excluded:
        parts.append(f"{x.candidate} breaks a constraint and is left out ({', '.join(x.excluded)}).")
    top_acc = max(scored, key=lambda e: (e.accuracy.value or 0.0) if e.accuracy else 0.0)
    if top_acc.accuracy:
        parts.append(f"The highest raw accuracy (dev) is {top_acc.candidate.name}'s, {pct(top_acc.accuracy.value)}{band(top_acc.accuracy.interval)}.")
    sel = next((s for s in by[chosen.candidate].selective if s.target_accuracy == o0.params.get("target_accuracy")), None)
    if sel is not None:  # the primary keeps an accuracy on what it answers
        target, need = sel.target_accuracy, sel.labels_needed
        if need and need > 5000:
            parts.append(f"Its sure accuracy is close to the target: showing it is {pct(target)} or more takes over 5,000 labels.")
        elif need:
            parts.append(f"Showing its sure accuracy is {pct(target)} or more takes about {need:,} more labels at the same error rate.")
    return " ".join(parts)


def objectives_table(task: Task, evs: list[Evaluation]) -> list[str]:
    """Every objective per candidate, best first, with the constraints."""
    scored = compared(evs)
    if not scored:
        return []
    objs = task.objectives
    ranked = rank(task.primary, task.ties, task.constraints, scored)
    floors = {e.candidate.name: e.floors for e in scored}
    head = "| model | " + " | ".join(o.label for o in objs) + " | rule | constraints |"
    L = ["", "## Objectives and constraints", "", head, "|---|" + "---|" * (len(objs) + 2)]
    for x in ranked:
        thr = x.scores[0].chosen
        L.append(
            f"| {x.candidate}{' ◎' if x is ranked[0] and not x.excluded else ''} | " + " | ".join(fmt(task.kind, o, sc) for o, sc in zip(objs, x.scores))
            + f" | {num(thr) if thr is not None else '—'} | {', '.join(x.excluded) or 'met'}{_floors(floors.get(x.candidate, []))} |"
        )
    L += ["", "◎ is the model the objectives and constraints choose. Every objective is measured on the answers. The models whose "
          "interval on the primary objective (leftmost) overlaps the best one's are compared by the next objectives (read the way "
          "the primary sets); those still tied, by the calls' latency (p90, only when all were measured alike), then API cost "
          "(the Calls section). The threshold is the min probability (Coverage) or P(positive) cut (on a yes/no question, every objective but Coverage and AUROC) the primary objective sets, among those that keep the task's floors (min_precision, "
          "min_recall) where it sets any; their shares are out of fold, so they can pass a floor a little."]
    return L


def _floors(fs: list[Floor]) -> str:
    """The floors' shares out of fold, beside the constraints."""
    return f" ({', '.join(f'{f.what} {pct(f.rate)}' for f in fs)})" if fs else ""


def weights_table(task: Task, evs: list[Evaluation], preds: dict[str, metrics.Preds]) -> list[str]:
    """With ExpectedLoss or a loss table as the objective: the recommendation with its weights halved and doubled."""
    from .weights import decides, sensitivity

    scored = compared(evs)
    moved = sensitivity(task, {e.candidate.name: preds[e.candidate.name] for e in scored if e.candidate.name in preds})
    if not moved:
        return []
    ranked = rank(task.primary, task.ties, task.constraints, scored)
    fits = [x for x in ranked if not x.excluded and x.scores[0].value is not None]
    now = fits[0].candidate if fits else None
    L = ["", "## With other weights", "", "| weights | recommended | tied |", "|---|---|---|",
         f"| as set: {task.primary.label} | {now or '—'} | {', '.join(x.candidate for x in ranked if x.tied_with_best)} |"]
    L += [f"| {'halved' if r.factor < 1 else 'doubled'}: {r.objective.label} | {r.recommended or '—'} | {', '.join(r.tied)} |" for r in moved]
    L += ["", ("**The recommendation moves: these weights decide it.** " if decides(now, moved) else "Halving or doubling the weights leaves the recommendation as it is. ")
          + "The weights are the task owner's to set; s1flow has no default. Re-ranked from the recorded answers, nothing asked again."]
    return L


def pareto(o0: Objective, ranked: list[Ranked], by: dict[str, Evaluation]) -> set[str]:
    """Candidates no other one beats on all of: the primary objective, API cost per 10k, p99."""
    pts: dict[str, tuple[float, float, float]] = {}
    for x in ranked:
        v, e = x.scores[0].value, by[x.candidate]
        if v is None:
            continue
        cost, p99 = e.calls.cost_per_10k_usd, _p99(e)
        pts[x.candidate] = (-v if o0.maximize else v, float("inf") if cost is None else float(cost), float(p99 or float("inf")))
    beats = lambda b, a: all(x <= y for x, y in zip(b, a)) and any(x < y for x, y in zip(b, a))
    return {m for m, a in pts.items() if not any(beats(b, a) for b in pts.values())}


REPORTED = {"f1": "F1", "macro_f1": "macro-F1", "mean_iou": "mean IoU"}  # a kind's own number, as the comparison heads it


def render(task: Task, variant: str, evs: list[Evaluation], preds: dict[str, metrics.Preds]) -> str:
    sf = evalset.current(task)
    cases = {cid: c for cid, c in task.load_cases().by_id().items() if sf.assign.get(cid) != "test"}
    kind = task.kind
    box = kind.type == "box"
    first = next((e for e in evs if e.n), None)
    labelled = [c for c in task.load_cases().labelled() if sf.assign.get(c.id) != "test"]
    labels = Counter(str(c.label) for c in labelled) if not box else Counter()
    sel0 = first.selective[0] if first and first.selective else None
    L: list[str] = [
        f"# {task.id}" + (f" · {variant}" if variant != "base" else ""),
        "",
        f"{dt.date.today()} · {len(labelled)} labelled dev cases"
        + (f" (right at IoU {kind.iou:g} or more)" if box else f" ({', '.join(f'{k} {v}' for k, v in labels.most_common(8))}" + (", more" if len(labels) > 8 else "") + ")")
        + f" · split: {first.split if first else '—'} · source: {task.source}",
        "",
        headline(task, evs),
        "",
        "## Comparison",
        "",
        "| model | scored | accuracy | " + REPORTED[kind.report[0]] + " | AUROC | ECE | coverage | sure accuracy (lower bound) | refused / unsupported | failed |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for e in evs:
        f = e.failures
        if not e.n or not e.selective:
            L.append(f"| {e.candidate.name} | 0 | — | | | | | | {f.unsupported}/{f.calls} | {f.failed}/{f.calls} |")
            continue
        s = e.selective[0]
        flag = "" if e.probabilities else " ※"
        acc = e.accuracy or Estimate(value=None)
        L.append(
            f"| {e.candidate.name}{flag}{' ✕' if f.missing else ''} | {e.n} | {pct(acc.value, 1)}{band(acc.interval)} | {num(e.measures[kind.report[0]].value if kind.report[0] in e.measures else None)} | {num(e.auroc.value if e.auroc else None)} | {num(e.ece)} "
            f"| {pct(s.coverage.value)}{band(s.coverage.interval)} | {pct(s.accuracy, 1)} ({pct(s.lower, 1)}) | {f.unsupported}/{f.calls} | {f.failed}/{f.calls} |"
        )
    L += left_out(task, evs)
    L += ["", "Answered by: " + "; ".join(
        f"{e.candidate.name} = {e.answered_by}" + (f" (also {', '.join(v for v in e.answered_by_all if v != e.answered_by)})" if len(e.answered_by_all) > 1 else "")
        for e in evs if e.answered_by
    ) + ". To compare versions, run each by name: `s1flow run <task> --models jev:1.14`."]
    L += objectives_table(task, evs)
    L += weights_table(task, evs, preds)
    L += calls_table(task, evs)
    L += time_table(evs)
    L += [
        "",
        f"Coverage: answering the most probable first, the largest share whose sure accuracy keeps the target {pct(sel0.target_accuracy) if sel0 else ''}. "
        "The cut is chosen on each CV fold's fit side and measured on its eval side. The lower bound is a one-sided 95% Clopper-Pearson; [ ] is a 95% bootstrap interval.",
        "Scored: answered dev cases only; held-out test results require an explicit final check. Refused / unsupported and failed both count calls.",
    ]
    if any(not e.probabilities for e in evs):
        L.append("※ a model that returns no distribution (one answer): its probability is 1 for every answer, so the coverage is all or nothing.")
    if box:
        L.append(f"Box: right at IoU {kind.iou:g} or more with the label's box. The probability is what jev returns; for an LLM, the agreement (IoU) of its repeated boxes. AUROC and ECE say how well that probability separates right from wrong.")
    if any(e.failures.unsupported for e in evs):
        L.append("Refused / unsupported: inputs the model did not take (question type, image, length limits). The model's limit, "
                 "not a failed call: left out of the denominator, the candidate kept.")
    if any(e.failures.data_errors for e in evs):
        L.append("Data errors: " + ", ".join(f"{e.candidate.name} {e.failures.data_errors}" for e in evs if e.failures.data_errors)
                 + ". The task's, not the model's (a missing image file, a state written wrong): counted neither as scored nor as failed.")

    if any(e.error_loss_threshold for e in evs):
        L += [
            "",
            "## Threshold",
            "",
            f"The threshold with the lowest total loss, chosen by CV, a miss (a positive read as negative) losing {task.error_losses[0]:g} and a false alarm {task.error_losses[1]:g}.",
            "",
            "| model | accuracy at 0.5 | accuracy tuned | misses | false alarms | threshold chosen (median) | threshold chosen on dev |",
            "|---|---|---|---|---|---|---|",
        ]
        for e in evs:
            if e.error_loss_threshold and e.accuracy:
                t = e.error_loss_threshold
                L.append(f"| {e.candidate.name} | {pct(e.accuracy.value, 1)} | {pct(t.accuracy, 1)} | {t.misses} | {t.false_alarms} | {t.median:.2f} | {t.chosen:.2f} |")

    for e in evs:
        if e.sweep:
            L += ["", f"## Misses and false alarms by threshold ({e.candidate.name})", "", "| threshold | misses | false alarms |", "|---|---|---|"]
            for row in e.sweep:
                L.append(f"| {row.threshold:.2f} | {row.misses} ({pct(row.misses / row.positives if row.positives else None)}) | {row.false_alarms} ({pct(row.false_alarms / row.negatives if row.negatives else None)}) |")

    if any(e.test for e in evs):
        L += ["", "## Test (read once, at the end)", "", "| model | cases | accuracy | coverage | sure accuracy | primary objective |", "|---|---|---|---|---|---|"]
        for e in evs:
            if e.test:
                held = e.test
                L.append(f"| {e.candidate.name} | {held.n} | {pct(held.accuracy, 1)} | {pct(held.coverage)} | {pct(held.sure_accuracy, 1)} | {num(held.primary.value, 3)} |")

    L += ["", f"## Wrong at a high probability ({metrics.HIGH_CONF} or more)", ""]
    any_err = False
    for e in evs:
        if not e.high_confidence_errors:
            continue
        any_err = True
        L += [f"**{e.candidate.name}** ({len(e.high_confidence_errors)})", "", "| id | label | answer | probability | case |", "|---|---|---|---|---|"]
        for h in e.high_confidence_errors[:8]:
            L.append(f"| {h.id} | {h.label} | {h.predicted} | {h.probability:.2f} | {show(cases[h.id])} |")
        L.append("")
    if not any_err:
        L.append("None.")

    if not box:
        L += disagreements(task, preds, cases)
    return "\n".join(L) + "\n"


def disagreements(task: Task, preds: dict[str, metrics.Preds], cases: dict[str, Case]) -> list[str]:
    preds = {m: p for m, p in preds.items() if p.ids}  # a model that answered nothing has no verdicts
    if len(preds) < 2:
        return []
    common = set.intersection(*(set(p.ids) for p in preds.values()))
    decided: dict[str, dict[str, tuple[bool | str, float]]] = {}
    for m, p in preds.items():
        for i, cid in enumerate(p.ids):
            if cid in common and cid in cases:
                decided.setdefault(cid, {})[m] = (measure.plain(p.pairs.value[i]), float(p.pairs.probability[i]))
    split = [cid for cid, d in decided.items() if len({v for v, _ in d.values()}) > 1]
    if not split:
        return ["", "## Cases the models disagree on", "", "None."]
    label = {cid: measure.plain(p.y[i]) for p in preds.values() for i, cid in enumerate(p.ids)}
    names = list(preds)
    L = ["", f"## Cases the models disagree on (12 of {len(split)})", "", "| id | label | " + " | ".join(names) + " | case |", "|---|---|" + "---|" * len(names) + "---|"]
    for cid in sorted(split, key=lambda c: -max(cf for _, cf in decided[c].values()))[:12]:
        cells = [f"{decided[cid][m][0]} ({decided[cid][m][1]:.2f})" if m in decided[cid] else "—" for m in names]
        L.append(f"| {cid} | {label[cid]} | " + " | ".join(cells) + f" | {show(cases[cid])} |")
    return L


def _dur(seconds: float) -> str:
    return f"{seconds:.0f} s" if seconds < 90 else f"{seconds / 60:.0f} min" if seconds < 5400 else f"{seconds / 3600:.1f} h"


def calls_table(task: Task, evs: list[Evaluation]) -> list[str]:
    """What the calls took, per candidate: latency per call and API cost per 10,000 cases, with where that cost
    came from, and the frontier of the primary objective against them."""
    rows = [e for e in evs if e.n]
    if not rows:
        return []
    budget = task.constraints.latency_p99_ms
    frontier = pareto(task.primary, rank(task.primary, task.ties, task.constraints, compared(rows)), {e.candidate.name: e for e in rows})
    L = [
        "", "## Calls (latency and API cost)", "",
        "| model | calls | p50 | p90 | p99 | max | spread (p99/p50) | retried | concurrency |" + (f" p99 ≤ {budget:.0f}ms |" if budget is not None else "")
        + " API cost per 10k | source | frontier |",
        "|---|---|---|---|---|---|---|---|---|" + ("---|" if budget is not None else "") + "---|---|---|",
    ]
    caveats: set[str] = set()
    for e in rows:
        c, t = e.calls, e.calls.latency
        spent = f" {usd(c.cost_per_10k_usd)} | {SOURCE[c.cost_source]} | {'○' if e.candidate.name in frontier else ''} |"
        if t is None:
            L.append(f"| {e.candidate.name} | 0 | — | — | — | — | — | — | — |" + (" — |" if budget is not None else "") + spent)
            continue
        conc = ", ".join(map(str, t.concurrency)) or "unknown"
        if t.concurrency_unknown and t.concurrency:
            conc += f" ({t.concurrency_unknown} unknown)"
        retried = "not recorded" if t.unrecorded == t.n else f"{t.retried}" + (f" ({t.unrecorded} not recorded)" if t.unrecorded else "")
        if t.unrecorded:
            caveats.add("unrecorded")
        if t.n < 100:
            caveats.add("few")
        if len(t.concurrency) > 1 or t.concurrency_unknown:
            caveats.add("mixed")
        fit = "" if budget is None else " ✓ |" if t.p99_ms <= budget else " ✗ |"
        L.append(
            f"| {e.candidate.name} | {t.n} | {t.p50_ms:.0f} ms | {t.p90_ms:.0f} ms | {t.p99_ms:.0f} ms | {t.max_ms:.0f} ms "
            f"| {num(t.spread, 1)} | {retried} | {conc} |{fit}{spent}"
        )
    L += ["", "Measured on the calls, not the answers: never an objective, only the constraints and the order of candidates the "
          "objectives tie (the p90 of each case's slowest call, then API cost). Frontier ○: no other model beats it on all three of "
          "the primary objective, API cost per 10k and p99.",
          "Latency is the time from sending to receiving one call that answered (the round trip from here included), without "
          "retries or the wait before them. Many calls at once read slower, from the provider's load and this machine's "
          "connections: to compare models, measure every candidate again at the same concurrency "
          "(`s1flow run <task> --fresh --concurrency N`, the same N for all)."]
    if "few" in caveats:
        L.append("Under 100 calls, a model's p99 means little more than its max.")
    if "mixed" in caveats:
        L.append("Some calls were made at another concurrency, or at one not recorded.")
    if "unrecorded" in caveats:
        L.append("\"not recorded\": calls made before 2026-10-16, whose time may include a retry's wait.")
    if note := cost_note([(e.candidate.name, e.calls.cost_source, e.calls.price.as_of if e.calls.price else None, e.calls.cost_unknown) for e in rows]):
        L.append(note)
    return L


def time_table(evs: list[Evaluation]) -> list[str]:
    rows = [e for e in evs if e.n and e.calls.throughput]
    if not rows:
        return []
    L = ["", "## API cost and time for these cases", "", "| model | API cost, total | time | per 10k (estimate) | concurrency |", "|---|---|---|---|---|"]
    for e in rows:
        t = e.calls.throughput
        assert t is not None
        kind = "measured" if t.measured else "estimated"
        L.append(
            f"| {e.candidate.name} | {usd(e.calls.cost_total_usd)} | {_dur(t.seconds)} ({kind}, {t.calls} calls) "
            f"| {_dur(10_000 / t.per_min * 60)} | {t.concurrency} |"
        )
    L += ["", "Measured: the wall time of a run that called every case. When every answer came from the cache, estimated as the calls' time summed and divided by the concurrency. The time depends more on the concurrency and the provider's rate limit than on the model."]
    return L


REPORT = "s1flow/report@1"  # <out>/<variant>.json


def chart_summary(task: Task, evaluations: list[Evaluation], data: dict[str, ChartData]) -> ChartSummary:
    """Summarize raw/CV change and the 2D cost-quality frontier on dev only.

    The report's other Pareto view includes p99 latency. This explicitly named
    projection ignores latency, so it can answer the cost-versus-quality question.
    """
    compared_evaluations = compared(evaluations)
    eligible = [e for e in compared_evaluations if e.objective and e.objective.rule and e.objective.rule.threshold is not None
                and data[e.candidate.name].raw_value is not None and data[e.candidate.name].cv_value is not None]
    changes = [(e.candidate.name, data[e.candidate.name]) for e in eligible]
    def gain(item: tuple[str, ChartData]) -> float:
        row = item[1]
        assert row.raw_value is not None and row.cv_value is not None
        return (row.cv_value - row.raw_value) * (1 if task.primary.maximize else -1)
    largest = max(changes, key=lambda item: abs(gain(item)), default=None)
    points = [(e.candidate.name, e.calls.cost_per_10k_usd, e.objective.value)
              for e in compared_evaluations if e.objective and e.objective.value is not None
              and e.calls.cost_per_10k_usd is not None and e.calls.cost_per_10k_usd >= 0]
    frontier = []
    for name, price, value in sorted(points, key=lambda point: (point[1], point[0])):
        assert price is not None and value is not None
        quality = -value if task.primary.maximize else value
        if not any(other_price is not None and other_value is not None and other_price <= price
                   and (-other_value if task.primary.maximize else other_value) <= quality
                   and (other_price < price or (-other_value if task.primary.maximize else other_value) < quality)
                   for _, other_price, other_value in points):
            frontier.append(name)
    return ChartSummary(candidate_count=len(changes), improved_count=sum(gain(item) > 1e-9 for item in changes),
                        largest_change_candidate=None if largest is None else largest[0],
                        largest_change_raw=None if largest is None else largest[1].raw_value,
                        largest_change_cv=None if largest is None else largest[1].cv_value,
                        cost_quality_frontier=frontier)


def write(task: Task, variant: str, out: Path) -> str:
    """<out>/<variant>.md and <variant>.json from every run on the variant's question; the Markdown is returned.
    The first report fixes the task's evaluation set (evalset.py)."""
    evalset.ensure(task)
    data_digest = task.data_digest
    contract_digest = task.evaluation_contract_digest
    adapter_digest = task.input_adapter_digest
    names = available_models(task, variant)
    preds = {m: metrics.load(task, variant, m) for m in names}
    evs = [metrics.evaluate(task, preds[m], variant=variant) for m in names]
    md = render(task, variant, evs, preds)
    out.mkdir(parents=True, exist_ok=True)
    charts = {e.candidate.name: metrics.chart_data(task, preds[e.candidate.model], e) for e in evs}
    saved = {"schema": REPORT, "task": task.id, "variant": variant, "at": clock.now(),
             "data_digest": data_digest, "evaluation_contract_digest": contract_digest, "input_adapter_digest": adapter_digest,
             "evaluations": [e.model_dump(mode="json") for e in evs],
             "charts": {name: values.model_dump(mode="json") for name, values in charts.items()},
             "chart_summary": chart_summary(task, evs, charts).model_dump(mode="json")}

    (out / f"{variant}.md").write_text(md)
    (out / f"{variant}.json").write_text(json.dumps(saved, ensure_ascii=False, indent=1))
    return md
