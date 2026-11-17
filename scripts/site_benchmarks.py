"""Write the site's Benchmarks pages from the bench reports, before `zensical build`.

    python scripts/site_benchmarks.py [--out docs/benchmarks]

Reads apps/bench/reports: README.md (what each task's answer is used for, and why its objective) and each
TASK/comparison.json. Writes OUT/index.md, OUT/TASK.md, and OUT/TASK/comparison.html and .json (the interactive
page the Skill's charts.py draws). Standard library only: no model calls, no rescoring. OUT is generated; it is
not committed.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import re
import shutil
from statistics import median
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "apps" / "bench" / "reports"
CHARTS = ROOT / "plugin" / "skills" / "s1flow" / "scripts" / "charts.py"
PREFACE = """\
---
description: A dated snapshot of Decision Models on ten public tasks, each measured by what its answer is used for.
hide:
  - toc
---

# Benchmarks

s1flow's own bench: the Decision Models in its line-up, asked the same labeled cases on ten public tasks. Each
task is measured by the objective its use calls for, so there is no score across tasks: a model is chosen for one
decision, by what that decision needs.

Read these as an example of what a comparison gives you, not as a ranking of providers. The same model does well
on one task and poorly on another, which is why you measure on your own cases.

- **A snapshot.** Measured {measured}. Models and their versions change; so would these numbers.
- **Development cases only.** The held-out test share of each task is not scored here.
- **Intervals.** Each value comes with a 95% confidence interval. Candidates whose interval reaches the best one's
  are marked `=` on the task page: the objective cannot tell them apart.
- **Latency** is the time for one request, sent from US East (Ashburn, Virginia), four requests at a time. Yours
  depends on where you call from.
- **API cost** is per 10,000 decisions: billed by the provider, or marked ~ when estimated from a list price.

"""


def task_uses() -> dict[str, dict[str, str]]:
    """The task table in the reports README: what each answer is used to do, the objective, and why."""
    uses = {}
    for line in (REPORTS / "README.md").read_text(encoding="utf-8").splitlines():
        row = re.fullmatch(r"\| \[([\w-]+)\]\([^)]*\) \| (.+?) \| (.+?) \| (.+?) \|", line)
        if row:
            task, use, objective, why = row.groups()
            uses[task] = {"use": use, "objective": objective, "why": why}
    return uses


def fmt(value: float | None, unit: str) -> str:
    if value is None:
        return "not reached"
    return f"{value:.0%}" if unit == "share" else f"{value:.3f}"


def fmt_interval(interval: list[float] | None, unit: str) -> str:
    if not interval:
        return ""
    lo, hi = interval
    return f"[{lo * 100:.0f}, {hi * 100:.0f}]" if unit == "share" else f"[{lo:.3f}, {hi:.3f}]"


def cost(calls: dict[str, Any]) -> str:
    usd = calls.get("cost_per_10k_usd")
    if usd is None:
        return "unknown"
    return ("" if calls.get("cost_source") == "billed" else "~") + f"${usd:.2f}"


def latency(calls: dict[str, Any]) -> str:
    p50 = (calls.get("latency") or {}).get("p50_ms")
    return "unknown" if p50 is None else f"{p50:,.0f} ms"


def scored(data: dict[str, Any]) -> list[dict[str, Any]]:
    """Candidates asked every case, best first, then faster, then cheaper; one that reaches no value comes last."""
    rows = [c for c in data["candidates"] if c["n"] and not c["excluded"]]
    sign = -1 if data["objective"]["direction"] == "max" else 1

    def key(c: dict[str, Any]) -> tuple:
        p50 = (c["calls"].get("latency") or {}).get("p50_ms")
        usd = c["calls"].get("cost_per_10k_usd")
        return (c["value"] is None, sign * (c["value"] or 0), p50 is None, p50 or 0, usd is None, usd or 0, c["candidate"])

    return sorted(rows, key=key)


def tied_with_best(data: dict[str, Any], rows: list[dict[str, Any]]) -> set[str]:
    """The candidates `s1flow report` marks `=`: their interval reaches the best one's (s1flow.eval.select._overlaps)."""
    if not rows or rows[0]["value"] is None:
        return set()
    best, maximize = rows[0], data["objective"]["direction"] == "max"

    def overlaps(c: dict[str, Any]) -> bool:
        if c["value"] is None:
            return False
        if not best["interval"] or not c["interval"]:
            return c["value"] == best["value"]
        return c["interval"][1] >= best["interval"][0] if maximize else c["interval"][0] <= best["interval"][1]

    return {c["candidate"] for c in rows if overlaps(c)}


def false_alarms(task: str) -> dict[str, float]:
    """For a Recall objective: each candidate's false-alarm share at its chosen threshold, out of fold, from the
    report's per-variant JSON (it can pass the cap a little)."""
    out = {}
    for path in (REPORTS / task / "questions").glob("*.json"):
        for e in json.loads(path.read_text(encoding="utf-8"))["evaluations"]:
            name = e["candidate"]["model"] + ("" if e["candidate"]["variant"] == "base" else "/" + e["candidate"]["variant"])
            constraint = (e.get("objective") or {}).get("constraint")
            if constraint is not None:
                out[name] = constraint
    return out


def question_block(data: dict[str, Any]) -> str:
    question = next(c["question"] for c in data["candidates"] if c["variant"] == "base")
    lines = [f'??? note "The question asked ({data["question_type"]})"', "", f"    {question['instructions']}", ""]
    criteria = question.get("criteria") or {}
    options = criteria.items() if isinstance(criteria, dict) else enumerate(criteria)  # a score's levels are a list
    lines += [f"    - **{option}**: {meaning}" for option, meaning in options]
    return "\n".join(lines).rstrip() + "\n"


def metric_columns(data: dict[str, Any]) -> list[tuple[str, str, str, str]]:
    """Every metric the comparison holds besides the objective, once each: (key, column label, unit, direction).
    Accuracy under the task's threshold rule is kept beside plain accuracy when they differ, as the HTML page does."""
    objective = data["objective"]
    rows = [c for c in data["candidates"] if c["n"] and not c["excluded"]]
    seen, out = {objective["label"]}, []
    for d in data["metric_definitions"]:
        key, label = d["key"], d["label"]
        if key.startswith("coverage:"):
            if objective["name"] == "coverage":
                continue  # the objective itself
            label = f"coverage at {float(key.split(':')[1]):.0%} accuracy"
        elif key.startswith("accepted_accuracy:"):
            label = "accepted accuracy"
        elif key == "objective:accuracy{}" and any(
                c["metrics"][key]["value"] != c["metrics"]["accuracy"]["value"] for c in rows):
            label = "accuracy (task rule)"
        if label in seen:
            continue
        seen.add(label)
        out.append((key, label, d["unit"], d["direction"]))
    return out


def bench_div(table: list[str], lower: list[int], text: list[int]) -> str:
    """A table the site's script can sort: which columns are lower-is-better, and which sort as text."""
    attrs = f' data-lower="{" ".join(map(str, lower))}" data-text="{" ".join(map(str, text))}"'
    return f'<div class="bench" markdown{attrs}>\n\n' + "\n".join(table) + "\n\n</div>\n"


def task_page(data: dict[str, Any], use: dict[str, str]) -> str:
    task, objective = data["task"], data["objective"]
    unit = objective["unit"]
    rows = scored(data)
    tied = tied_with_best(data, rows)
    rows = [c for c in rows if c["candidate"] in tied] + [c for c in rows if c["candidate"] not in tied]
    alarms = false_alarms(task) if objective["name"] == "recall" else {}
    metrics = metric_columns(data)
    refused = any(c["failures"]["refused_cases"] for c in rows)
    head = ["Candidate", objective["label"]] + (["false alarms"] if alarms else []) + [label for _, label, _, _ in metrics]
    head += ["p50 latency", "p90 latency", "API cost / 10k"] + (["refused"] if refused else [])
    lower = ([1] if objective["direction"] == "min" else []) + ([2] if alarms else [])
    lower += [2 + bool(alarms) + i for i, (*_, direction) in enumerate(metrics) if direction == "min"]
    lower += list(range(len(head) - 3 - refused, len(head)))
    table = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for c in rows:
        cells = [c["candidate"] + (" =" if c["candidate"] in tied else ""),
                 f"{fmt(c['value'], unit)} {fmt_interval(c['interval'], unit)}".rstrip()]
        if alarms:
            cells.append(f"{alarms[c['candidate']]:.1%}" if c["candidate"] in alarms else "")
        cells += [fmt(c["metrics"][key]["value"], u) if c["metrics"][key]["value"] is not None else "" for key, _, u, _ in metrics]
        p90 = (c["calls"].get("latency") or {}).get("p90_ms")
        cells += [latency(c["calls"]), "unknown" if p90 is None else f"{p90:,.0f} ms", cost(c["calls"])]
        if refused:
            cells.append(f"{c['failures']['refused_cases'] / c['n']:.0%}")
        table.append("| " + " | ".join(cells) + " |")
    unreached = any(c["value"] is None for c in rows)
    notes = ["`=` marks the candidates whose interval reaches the best one's: the objective cannot tell them apart, "
             "so they are not ranked against each other. Rows start best first, then faster, then cheaper; select a "
             "column heading to sort by it."]
    if alarms:
        notes.append("False alarms are measured out of fold at each candidate's threshold, so they can pass the cap "
                     "a little.")
    if unreached:
        notes.append("Not reached: no threshold meets the objective's target on these cases.")
    notes.append("Accuracy (all) reads every answer at its most likely option, without the objective's threshold; "
                 "accuracy (task rule) reads them with the objective's threshold. Accepted accuracy is the accuracy of the "
                 "answers above the coverage threshold. Lower is better for "
                 "latency, cost, ECE, Brier score, MAE, loss, false alarms and refusals.")
    return "\n".join([
        "---", "hide:", "  - toc", "description: " + json.dumps(f"{task}: the answer is used to {use['use']}; measured by {use['objective']}."), "---",
        "",
        f"# {task}", "",
        f"The answer is used to **{use['use']}**. Objective: **{use['objective']}**, because {use['why']}.", "",
        f"Measured {data['at'][:10]} on {data['n']} labeled development cases. Source: {data['source']}.", "",
        question_block(data),
        bench_div(table, lower, [0]),
        " ".join(notes), "",
        f"[Open the full comparison]({task}/comparison.html){{ .md-button }} with the probability curves "
        f"and a trade-off chart, or download [comparison.json]({task}/comparison.json).", "",
    ])


def matrix(tasks: list[tuple[dict[str, Any], dict[str, str]]]) -> str:
    """Each candidate's objective value on each task, `=` where it is among the best, as the bench overview shows."""
    cells: dict[str, dict[str, str]] = {}
    for data, _ in tasks:
        rows = scored(data)
        tied = tied_with_best(data, rows)
        for c in rows:
            cells.setdefault(c["candidate"], {})[data["task"]] = (
                fmt(c["value"], data["objective"]["unit"]) + (" =" if c["candidate"] in tied else ""))
    best = {name: sum(v.endswith(" =") for v in row.values()) for name, row in cells.items()}
    order = sorted(cells, key=lambda name: (-best[name], name))
    names = [data["task"] for data, _ in tasks]
    table = ["| Candidate | Among the best | " + " | ".join(names) + " |",
             "|" + "---|" * (len(names) + 2)]
    for name in order:
        table.append(f"| {name} | {best[name]} of {len(cells[name])} | "
                     + " | ".join(cells[name].get(t, "") for t in names) + " |")
    lower = [i + 2 for i, (data, _) in enumerate(tasks) if data["objective"]["direction"] == "min"]
    return bench_div(table, lower, [0])


def index_page(tasks: list[tuple[dict[str, Any], dict[str, str]]]) -> str:
    table = ["| Task | The answer is used to | Objective | Cases | Best · median · worst |",
             "|---|---|---|---|---|"]
    for data, use in tasks:
        unit = data["objective"]["unit"]
        rows = scored(data)
        values = [c["value"] for c in rows if c["value"] is not None]
        best, worst = (max, min) if data["objective"]["direction"] == "max" else (min, max)
        spread = " · ".join(fmt(f(values), unit) for f in (best, median))
        spread += " · " + ("not reached" if len(values) < len(rows) else fmt(worst(values), unit))
        table.append(f"| [{data['task']}]({data['task']}.md) | {use['use']} | {use['objective']} | {data['n']} | "
                     f"{spread} |")
    dates = sorted({data["at"][:10] for data, _ in tasks})
    measured = f"on {dates[0]}" if len(dates) == 1 else f"between {dates[0]} and {dates[-1]}; each task page has its date"
    bench = bench_div(table, [], [0, 1, 2])
    by_model = ("\n## By model\n\nEach candidate's value on each task's own objective. `=` marks a value among the "
                "best on that task, and *Among the best* counts those tasks. The units differ by task, so read a column, "
                "not a row; the task pages have every other metric.\n\n" + matrix(tasks))
    return PREFACE.replace("{measured}", measured) + "## By task\n\n" + bench + by_model


def load_charts():
    spec = importlib.util.spec_from_file_location("charts", CHARTS)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build(out: Path) -> list[str]:
    charts = load_charts()
    uses = task_uses()
    reports = sorted(p.parent.name for p in REPORTS.glob("*/comparison.json"))
    if missing := set(reports) ^ set(uses):
        raise SystemExit(f"apps/bench/reports/README.md and the reports disagree on: {', '.join(sorted(missing))}")
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    tasks = []
    for task in sorted(reports, key=list(uses).index):  # the README's order
        snapshot = REPORTS / task / "comparison.json"
        data = charts.read_snapshot(snapshot)
        (out / task).mkdir()
        shutil.copyfile(snapshot, out / task / "comparison.json")
        (out / task / "comparison.html").write_text(charts.render(data), encoding="utf-8")
        (out / f"{task}.md").write_text(task_page(data, uses[task]), encoding="utf-8")
        tasks.append((data, uses[task]))
    (out / "index.md").write_text(index_page(tasks), encoding="utf-8")
    return reports


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--out", type=Path, default=ROOT / "docs" / "benchmarks")
    args = parser.parse_args()
    print(f"wrote {len(build(args.out))} task pages to {args.out}")


if __name__ == "__main__":
    main()
