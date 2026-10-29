"""M0 acceptance: s1flow's sweep over nod's saved P(wake) gives nod's own table."""

import json
import re
from pathlib import Path

import numpy as np

from conftest import BENCH

from s1flow.eval import metrics
from s1flow.project import Project
from s1flow.eval.task import load

NOD_EVAL = Path(__file__).parent / "fixtures" / "nod"  # nod's saved run and report


def nod_table() -> dict[float, tuple[int, int]]:
    rows = re.findall(r"^\| (0\.\d\d)(?: ←今)? \| (\d+) \(.*?\) \| (\d+) \(.*?\) \|$", (NOD_EVAL / "report-latest.md").read_text(), re.M)
    return {float(t): (int(m), int(w)) for t, m, w in rows}


def test_sweep_matches_nod_report():
    saved = json.loads((NOD_EVAL / "results-latest.json").read_text())
    labelled = [r for r in saved["results"] if r["label"] != "either"]
    y = np.array([r["label"] == "must" for r in labelled])
    runs = np.array([r["pWake"] for r in labelled])
    theirs = nod_table()
    assert theirs, "could not parse nod's report"
    ours = {s.threshold: (s.misses, s.false_alarms) for s in metrics.sweep(y, runs, sorted(theirs))}
    assert ours == theirs


def test_task_state_matches_nod_build_state():
    task = load(Project(BENCH), "nod-wake")
    assert task.load_cases().by_id()["book-yes-un"].state == {
        "earlier": ["ユーザー: 今週末、箱根で一泊できる宿探して。2人で"],
        "agent": "土曜泊で「箱根湯本 翠の宿」が空いています。2名・朝夕食付きで38,000円です。この条件で予約しますか？",
        "user": "うん",
    }
