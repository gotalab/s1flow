"""Score questions in the evaluation: MAE, QWK, the ordinal AUROC and Brier, end to end (no network)."""

import asyncio
import json

import numpy as np
import pytest

from conftest import attach, make_project

from s1flow.client import Capabilities, Response, Score, ScoreAnswer
from s1flow.core.errors import ConfigError
from s1flow.eval import Task, comparison, metrics, report
from s1flow.eval import run as running
from s1flow.eval.kinds import kind_of
from s1flow.eval.objectives import measure
from s1flow.objectives import MAE, QWK, Accuracy, MacroF1
from s1flow.policies import DecisionRule
from s1flow.policies.kinds import Average

Q = Score(instructions="How helpful is the response?", criteria=["not", "slightly", "partly", "mostly", "fully"])


def _pairs(labels, dists):
    kind = kind_of(Q)
    readings = [kind.reading(Average(distributed=True, distribution=list(d), expected=float(np.dot(range(5), d))), DecisionRule()) for d in dists]
    return kind, measure.pairs(kind, labels, readings)


def test_mae_qwk_and_level_accuracy_match_sklearn():
    from sklearn.metrics import cohen_kappa_score

    rng = np.random.default_rng(3)
    labels = [int(x) for x in rng.integers(0, 5, 150)]
    _, p = _pairs(labels, rng.dirichlet(np.ones(5), 150))
    said = p.value.astype(int)
    assert measure.measure("mae", p) == pytest.approx(np.mean(np.abs(p.expected - np.array(labels))))
    assert measure.measure("qwk", p) == pytest.approx(cohen_kappa_score(labels, said, weights="quadratic", labels=range(5)))
    assert measure.bound(Accuracy(), kind_of(Q)).value(p) == np.mean(said == np.array(labels))


def test_a_level_is_the_expected_level_rounded():
    kind, p = _pairs([2, 2], [[0, 0, 0.5, 0.5, 0], [0.5, 0, 0, 0, 0.5]])  # expected 2.5 and 2.0
    assert list(p.value) == [3, 2] and list(p.correct) == [False, True]


def test_ordinal_brier_is_the_ranked_probability_score():
    kind, p = _pairs([0, 4], [[1, 0, 0, 0, 0], [1, 0, 0, 0, 0]])  # sure and right, sure and as wrong as can be
    assert measure.measure("brier", p) == pytest.approx(0.5)
    assert kind.brier(0, kind.reading(Average(distributed=True, distribution=[1, 0, 0, 0, 0], expected=0.0), DecisionRule())) == 0.0


def test_equal_tails_tie_in_the_ordinal_auroc():
    _, p = _pairs([3, 2], [[0.1, 0.2, 0.3, 0.4, 0], [0.3, 0.3, 0, 0.4, 0]])  # P(level >= 3) is 0.4 for both: a tie
    assert measure.measure("auroc", p) == 0.5  # the only cut with both sides is 3


def test_ordinal_auroc_ranks_each_cut():
    near = lambda level: [0.9 if j == level else 0.1 / 4 for j in range(5)]
    _, p = _pairs([0, 1, 2, 3, 4], [near(j) for j in range(5)])
    assert measure.measure("auroc", p) == 1.0


def test_a_failed_call_is_as_far_off_as_its_label_can_be():
    kind = kind_of(Q)
    sure = kind.reading(Average(distributed=True, distribution=[0, 0, 0, 0, 1], expected=4.0), DecisionRule())
    p = measure.pairs(kind, [4, 1], [sure, None])
    assert measure.measure("mae", p) == pytest.approx(1.5)  # 0 and 3 levels off


def test_score_objectives_are_declared_for_score_only(tmp_path):
    task = Task(id="s", cases="d.jsonl", state=lambda r: r["t"], question=Q, label=lambda r: r["y"], tiebreak=[QWK()])
    assert task.primary == MAE() and task.kind.objectives[0] == "mae"
    with pytest.raises(ConfigError, match="two levels"):
        Task(id="s", cases="d.jsonl", state=lambda r: r["t"], question=Score(instructions="?", criteria=["only"]), label=lambda r: r["y"])
    with pytest.raises(ConfigError, match="does not apply to a score"):
        Task(id="s", cases="d.jsonl", state=lambda r: r["t"], question=Q, label=lambda r: r["y"], objective=MacroF1())


class Rater:
    """Says the level the text names, sure, except on every fourth case, where it is one level high and unsure."""

    id, model_id, concurrency = "fake:rater", "fake-rater", 4
    capabilities = Capabilities(question_types={"score"})

    def __init__(self, b=None):
        pass

    async def decide(self, state, questions, *, options=None):
        n, level = map(int, state.split())
        off = n % 4 == 0
        said = min(4, level + 1) if off else level
        probs = {str(j): (0.6 if j == said else 0.1) if off else (0.96 if j == said else 0.01) for j in range(5)}
        return Response(answers={"q": ScoreAnswer(score=sum(int(k) * v for k, v in probs.items()), probabilities=probs)},
                        answered_by=self.model_id)


def test_a_score_task_runs_reports_and_compares(tmp_path):
    p = make_project(tmp_path, {"rater": Rater})
    rows = [{"id": str(i), "n": i, "y": i % 5} for i in range(60)]
    (tmp_path / "data.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    task = attach(Task(id="score-test", cases="data.jsonl", dir=tmp_path, state=lambda r: f"{r['n']} {r['y']}",
                       question=Q, label=lambda r: r["y"]), p)
    asyncio.run(running.run_model(task, "rater", limit=None, variant="base"))
    pr = metrics.load(task, "base", "rater")
    assert pr.probabilities
    e = metrics.evaluate(task, pr)
    assert e.objective and e.objective.objective == MAE() and 0 < e.objective.value < 0.5
    assert e.measures["qwk"].value and e.measures["qwk"].value > 0.8
    assert e.selective[0].accuracy == 1.0  # the unsure fourth is left out at the chosen min probability
    md = report.render(task, "base", [e], {"rater": pr})
    assert "| MAE |" in md
    c = comparison.collect(task)
    row = next(r for r in c.candidates if r.model == "rater")
    assert row.value == e.objective.value and {"mae", "qwk", "brier"} <= set(row.metrics)
    assert row.adoption_blocked == ["score questions are comparable but cannot be adopted as runtime policies"]
