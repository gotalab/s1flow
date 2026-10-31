import numpy as np
import pytest

from conftest import binary_preds

from s1flow.eval import metrics, split
from s1flow.eval.objectives import measure
from s1flow.eval.objectives.measure import bound
from s1flow.eval.task import Split
from s1flow.objectives import Coverage, ExpectedLoss
from s1flow.policies import DecisionRule
from s1flow.policies.kinds import Average
from s1flow.eval.kinds import BooleanKind
from s1flow.policies.kinds import KindParams


def test_cp_lower_rule_of_three():
    # 30 automated, all correct: only "about 90% or better" at 95% one-sided
    assert metrics.cp_lower(30, 30) == pytest.approx(0.05 ** (1 / 30), abs=1e-9)
    assert metrics.cp_lower(59, 59) >= 0.95 > metrics.cp_lower(58, 58)


def test_labels_needed():
    assert metrics.labels_needed(59, 59, 1.0, 0.95) == 0
    assert metrics.labels_needed(30, 30, 1.0, 0.95) == 29
    assert metrics.labels_needed(30, 30, 0.5, 0.95) == 58  # only half gets automated
    assert metrics.labels_needed(90, 100, 1.0, 0.95) is None  # 10% errors never reach 95%


def test_a_min_probability_cuts_only_between_distinct_probabilities():
    pairs = binary_preds([0.99, 0.01, 0.9, 0.8], [True, True, True, True]).pairs  # probabilities 0.99, 0.99, 0.9, 0.8; the second wrong
    cov = lambda t: bound(Coverage(target_accuracy=t), BooleanKind())
    assert metrics.search(cov(0.5), pairs) == 0.8
    assert metrics.search(cov(0.9), pairs) == np.inf  # none keeps it: nothing is answered


def test_the_sweep_counts_a_positive_below_t_a_miss_and_a_negative_at_or_above_t_a_false_alarm():
    y = np.array([True, True, False, False])
    rows = metrics.sweep(y, np.array([0.4, 0.5, 0.5, 0.6]), [0.5, 0.6])
    assert [(r.threshold, r.misses, r.positives, r.false_alarms, r.negatives) for r in rows] == [(0.5, 1, 2, 2, 2), (0.6, 2, 2, 1, 2)]


def test_a_threshold_prefers_cheaper_errors():
    pairs = binary_preds([0.2, 0.9, 0.4, 0.1], [True, True, False, False]).pairs
    grid = np.array([0.1, 0.3, 0.5])
    assert metrics.search(bound(ExpectedLoss(fn=10, fp=1), BooleanKind()), pairs, grid) == 0.1
    assert metrics.search(bound(ExpectedLoss(fn=1, fp=1), BooleanKind()), pairs, grid) == 0.5


def test_reading_again_at_a_rule_is_what_the_kind_reads():
    kind, rng = BooleanKind(), np.random.default_rng(0)
    ps = np.round(rng.random(50), 2)
    plain = binary_preds(ps, ps > 0.5).pairs
    for rule in (DecisionRule(threshold=0.3), DecisionRule(min_probability=0.7), DecisionRule(threshold=0.6, min_probability=0.8)):
        each = measure.pairs(kind, list(ps > 0.5), [kind.reading(Average(distributed=True, p_positive=float(x)), rule) for x in ps])
        again = plain.at(threshold=rule.threshold, min_probability=rule.min_probability)
        for col in ("value", "probability", "unsure", "correct"):
            assert (np.asarray(getattr(again, col), dtype=object) == getattr(each, col)).all(), (rule, col)


@pytest.mark.parametrize("y", [
    np.array(["a", "b"] * 30),  # stratified k-fold
    np.array(["a"] * 57 + ["b"] * 3),  # a label with fewer than k cases: k-fold
    np.array(["a", "b"] * 20),  # under SMALL: leave-one-out
])
def test_folds_cover_dev_without_leaks(y):
    s = Split(k=5)
    p = split.plan(len(y), np.array([], dtype=int))
    seen = set()
    for fit, ev in split.folds(p, y, s):
        assert not set(fit) & set(ev)
        seen |= set(ev.tolist())
    assert seen == set(p.dev.tolist())


def test_the_plan_switches_on_the_dev_size():
    small = split.plan(60, np.arange(18))
    assert small.method == "loo" and len(small.dev) == 42 and set(small.test) == set(range(18))
    big = split.plan(300, np.arange(90))
    assert big.method == "stratified-kfold" and len(big.dev) == 210


def test_auc_matches_sklearn():
    from sklearn.metrics import roc_auc_score

    rng = np.random.default_rng(0)
    y = rng.random(200) < 0.4
    s = np.round(rng.random(200), 1)  # ties on purpose
    assert measure._auc(y, s) == pytest.approx(roc_auc_score(y, s))


@pytest.mark.parametrize("binary", [True, False])
def test_f1_is_sklearns(binary):
    from sklearn.metrics import f1_score

    from s1flow.client import Choice
    from s1flow.eval.kinds import kind_of

    rng = np.random.default_rng(1)
    keys = ["a", "b", "c", "d"]
    kind = kind_of(Choice(instructions="?", criteria={k: None for k in keys}), KindParams(positive="a" if binary else None))
    dist = rng.dirichlet(np.ones(4), 120)
    labels = [bool(x) for x in rng.random(120) < 0.3] if binary else [keys[i] for i in rng.integers(0, 3, 120)]  # "d" never right
    avgs = [Average(distributed=True, p_positive=float(d[0])) if binary else Average(distributed=True, distribution=list(d)) for d in dist]
    p = measure.pairs(kind, labels, [kind.reading(a, DecisionRule()) for a in avgs])
    want = f1_score(p.y, p.value.astype(bool), average="binary") if binary else f1_score(p.y, p.value, average="macro", labels=keys, zero_division=0)
    assert measure.measure("f1" if binary else "macro_f1", p) == want  # exactly: the baseline holds sklearn's numbers
