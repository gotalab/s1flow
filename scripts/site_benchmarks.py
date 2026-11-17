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

s1flow's own bench: every Decision Model in its line-up, asked the same labeled cases on ten public tasks. Each
task is measured by the objective its use calls for, so there is no score across tasks: a model is chosen for one
decision, by what that decision needs.

Read these as an example of what a comparison gives you, not as a ranking of providers. The same model does well
on one task and poorly on another, which is why you measure on your own cases.

- **A snapshot.** Measured {measured}. Models and their versions change; so would these numbers.
- **Development cases only.** The held-out test share of each task is not scored here.
- **Intervals.** Every value has a 95% confidence interval. Candidates whose intervals overlap are not told apart.
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
        return "—"
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
    """Candidates asked every case. A row the model could not reach the objective on stays, with no value."""
    rows = [c for c in data["candidates"] if c["n"] and not c["excluded"]]
    sign = -1 if data["objective"]["direction"] == "max" else 1
    return sorted(rows, key=lambda c: (c["value"] is None, sign * (c["value"] or 0), c["candidate"]))


def question_block(data: dict[str, Any]) -> str:
    question = next(c["question"] for c in data["candidates"] if c["variant"] == "base")
    lines = [f'??? note "The question asked ({data["question_type"]})"', "", f"    {question['instructions']}", ""]
    criteria = question.get("criteria") or {}
    options = criteria.items() if isinstance(criteria, dict) else enumerate(criteria)  # a score's levels are a list
    lines += [f"    - **{option}**: {meaning}" for option, meaning in options]
    return "\n".join(lines).rstrip() + "\n"


def task_page(data: dict[str, Any], use: dict[str, str]) -> str:
    task, objective = data["task"], data["objective"]
    unit = objective["unit"]
    rows = scored(data)
    table = [f"| Candidate | {objective['label']} | accuracy (all) | p50 latency | API cost / 10k |",
             "|---|---|---|---|---|"]
    for c in rows:
        acc = c["metrics"].get("accuracy", {})
        table.append(f"| {c['candidate']} | {fmt(c['value'], unit)} {fmt_interval(c['interval'], unit)} | "
                     f"{fmt(acc.get('value'), 'share')} | {latency(c['calls'])} | {cost(c['calls'])} |")
    unreached = any(c["value"] is None for c in rows)
    return "\n".join([
        "---", "hide:", "  - toc", "description: " + json.dumps(f"{task}: the answer is used to {use['use']}; measured by {use['objective']}."), "---",
        "",
        f"# {task}", "",
        f"The answer is used to **{use['use']}**. Objective: **{use['objective']}**, because {use['why']}.", "",
        f"Measured {data['at'][:10]} on {data['n']} labeled development cases. Source: {data['source']}.", "",
        question_block(data),
        "\n".join(table), "",
        *(["— : no threshold reaches the objective's target on these cases.", ""] if unreached else []),
        f"[Open the full comparison]({task}/comparison.html){{ .md-button }} with every metric, the probability curves "
        f"and a trade-off chart, or download [comparison.json]({task}/comparison.json).", "",
    ])


def index_page(tasks: list[tuple[dict[str, Any], dict[str, str]]]) -> str:
    table = ["| Task | The answer is used to | Objective | Cases | Best · median · worst |",
             "|---|---|---|---|---|"]
    for data, use in tasks:
        unit = data["objective"]["unit"]
        values = [c["value"] for c in scored(data) if c["value"] is not None]
        best, worst = (max, min) if data["objective"]["direction"] == "max" else (min, max)
        spread = " · ".join(fmt(f(values), unit) for f in (best, median, worst))
        table.append(f"| [{data['task']}]({data['task']}.md) | {use['use']} | {use['objective']} | {data['n']} | "
                     f"{spread} |")
    dates = sorted({data["at"][:10] for data, _ in tasks})
    measured = f"on {dates[0]}" if len(dates) == 1 else f"between {dates[0]} and {dates[-1]}; each task page has its date"
    return PREFACE.replace("{measured}", measured) + "\n".join(table) + "\n"


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
