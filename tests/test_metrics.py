import numpy as np
import pytest
from hypothesis import given
from hypothesis import strategies as st

from conftest import binary_preds, task

from s1flow.eval import metrics, split
from s1flow.eval.evaluation import Estimate, Floor, ObjectiveScore
from s1flow.eval.objectives import measure
from s1flow.eval.objectives.measure import bound
from s1flow.eval.task import Split
from s1flow.objectives import AUROC, Constraints, Coverage, ExpectedLoss, Recall
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


def verdict(objectives, rest, held=None, constraint=None, floor=None, **constraints):
    """The held-out verdict of a task with these objectives: the rest's interval `rest`, the test share's (value,
    interval) `held`, its primary constraint's (k, n) `constraint`, and its floor's (k, n) `floor`."""
    from conftest import ev  # here: the folds test names its eval side `ev`

    from s1flow.eval.evaluation import TestResult  # here: pytest would try to collect it as a test class

    t = task(objectives, constraints=Constraints(**constraints))
    value, interval = held or (None, None)
    test = TestResult(n=10, accuracy=0.9, coverage=1.0, sure_accuracy=None, tuned_accuracy=None,
                      primary=Estimate(value=value, interval=interval), constraint=constraint)
    floors = [Floor(what=name, bound=bound, rate=bound, test=floor) for name, bound in Constraints(**constraints).floors.items()]
    e = ev("m", [ObjectiveScore(objective=t.primary, value=0.5, interval=rest)])
    return metrics.test_verdict(t, e.model_copy(update={"test": test, "floors": floors}))


def test_the_held_out_verdict_at_its_edges():
    # no constraint: kept when the test value reaches the rest's interval, below only when its interval lies wholly past it
    assert verdict([AUROC()], (0.7, 0.9), (0.7, (0.6, 0.8))) == "kept"
    assert verdict([AUROC()], (0.7, 0.9), (0.69, (0.6, 0.7))) == "inconclusive"  # its interval touches: not shown below
    assert verdict([AUROC()], (0.7, 0.9), (0.69, (0.6, 0.6999))) == "below"
    assert verdict([ExpectedLoss()], (0.1, 0.3), (0.3, (0.2, 0.4))) == "kept"
    assert verdict([ExpectedLoss()], (0.1, 0.3), (0.31, (0.3, 0.4))) == "inconclusive"
    assert verdict([ExpectedLoss()], (0.1, 0.3), (0.31, (0.3001, 0.4))) == "below"
    # a constraint: kept at its bound exactly; past it but not shown broken (one-sided 95%), inconclusive
    assert verdict([Coverage(target_accuracy=0.9)], None, constraint=(9, 10)) == "kept"
    assert verdict([Coverage(target_accuracy=0.9)], None, constraint=(8, 10)) == "inconclusive"
    assert verdict([Coverage(target_accuracy=0.9)], None, constraint=(10, 20)) == "below"
    assert verdict([Recall(max_false_alarm=0.1)], None, constraint=(1, 10)) == "kept"
    assert verdict([Recall(max_false_alarm=0.1)], None, constraint=(2, 10)) == "inconclusive"
    assert verdict([Recall(max_false_alarm=0.1)], None, constraint=(10, 20)) == "below"
    assert verdict([Coverage(target_accuracy=0.9)], None, constraint=(0, 0)) == "inconclusive"  # nothing answered
    # a floor: kept at it exactly, inconclusive under it, below when shown broken, and nothing read positive is not kept
    kept = (0.5, (0.4, 0.6))
    assert verdict([ExpectedLoss()], (0.1, 0.9), kept, floor=(8, 10), min_precision=0.8) == "kept"
    assert verdict([ExpectedLoss()], (0.1, 0.9), kept, floor=(7, 10), min_precision=0.8) == "inconclusive"
    assert verdict([ExpectedLoss()], (0.1, 0.9), kept, floor=(2, 10), min_precision=0.8) == "below"
    assert verdict([ExpectedLoss()], (0.1, 0.9), kept, floor=(0, 0), min_precision=0.8) == "inconclusive"


# ---------- properties over generated cases (Hypothesis): each measure against an independent oracle ----------

PROBABILITY = st.one_of(st.integers(0, 20).map(lambda i: i / 20), st.floats(0, 1))  # coarse values tie, exact edges included


@st.composite
def binary_cases(draw, min_size=1):
    n = draw(st.integers(min_size, 40))
    return np.array(draw(st.lists(PROBABILITY, min_size=n, max_size=n))), np.array(draw(st.lists(st.booleans(), min_size=n, max_size=n)))


def ece(conf, correct, bins=10):
    """Expected calibration error, by its definition: bins (e_i, e_i+1] over the probability, the first closed at 0."""
    edges = np.linspace(0, 1, bins + 1)
    at = np.clip(np.searchsorted(edges, conf, side="left") - 1, 0, bins - 1)
    return sum((at == i).mean() * abs(conf[at == i].mean() - correct[at == i].mean()) for i in range(bins) if (at == i).any())


@given(binary_cases(), st.data())
def test_binary_measures_are_their_definitions(cases, data):
    """A failed call (no reading) counts as wrong, raises no alarm, and has P(positive) 0.5 and probability 0."""
    from sklearn.metrics import brier_score_loss, f1_score, precision_score, recall_score, roc_auc_score

    p, y = cases
    ok = np.array(data.draw(st.lists(st.booleans(), min_size=len(p), max_size=len(p))))
    kind = BooleanKind()
    pairs = measure.pairs(kind, [bool(v) for v in y], [kind.reading(Average(distributed=True, p_positive=float(x)), DecisionRule()) if answered else None
                                          for x, answered in zip(p, ok)])
    p, said = np.where(ok, p, 0.5), ok & (p >= 0.5)
    right = ok & (said == y)
    assert measure.measure("brier", pairs) == pytest.approx(brier_score_loss(y, p, labels=[False, True]))
    assert measure.measure("auroc", pairs) == (pytest.approx(roc_auc_score(y, p)) if 0 < y.sum() < len(y) else None)
    assert measure.measure("accuracy", pairs) == pytest.approx(right.mean())
    assert measure.measure("ece", pairs) == pytest.approx(ece(np.where(ok, np.where(said, p, 1 - p), 0.0), right))
    assert measure.measure("f1", pairs) == pytest.approx(f1_score(y, said, zero_division=0))
    assert measure.measure("recall", pairs) == (pytest.approx(recall_score(y, said)) if y.any() else None)
    assert measure.measure("precision", pairs) == (pytest.approx(precision_score(y, said)) if said.any() else None)


KEYS = ["a", "b", "c", "d"]


@st.composite
def choice_cases(draw):
    k, n = draw(st.integers(2, 4)), draw(st.integers(1, 30))
    weights = draw(st.lists(st.lists(st.integers(0, 6), min_size=k, max_size=k).filter(any), min_size=n, max_size=n))
    dist = np.array(weights, dtype=float)
    return KEYS[:k], dist / dist.sum(axis=1, keepdims=True), np.array(draw(st.lists(st.sampled_from(KEYS[:k]), min_size=n, max_size=n)))


@given(choice_cases())
def test_choice_measures_are_their_definitions(cases):
    from sklearn.metrics import roc_auc_score

    from s1flow.client import Choice
    from s1flow.eval.kinds import kind_of

    keys, dist, y = cases
    kind = kind_of(Choice(instructions="?", criteria={k: None for k in keys}))
    pairs = measure.pairs(kind, list(y), [kind.reading(Average(distributed=True, distribution=list(d)), DecisionRule()) for d in dist])
    onehot = np.array([[label == k for k in keys] for label in y], dtype=float)
    said = np.array(keys)[[max(range(len(keys)), key=lambda j: d[j]) for d in dist]]  # the first of the most probable
    assert measure.measure("brier", pairs) == pytest.approx(np.mean(((dist - onehot) ** 2).sum(axis=1)))
    aucs = [roc_auc_score(y == k, dist[:, j]) for j, k in enumerate(keys) if 0 < (y == k).sum() < len(y)]
    assert measure.measure("auroc", pairs) == (pytest.approx(np.mean(aucs)) if aucs else None)
    assert measure.measure("accuracy", pairs) == pytest.approx(np.mean(said == y))
    assert measure.measure("ece", pairs) == pytest.approx(ece(dist.max(axis=1), said == y))


@given(st.integers(2, 5).flatmap(lambda levels: st.tuples(
    st.just(levels),
    st.lists(st.tuples(st.lists(st.integers(0, 6), min_size=levels, max_size=levels).filter(any), st.integers(0, levels - 1)), min_size=1, max_size=30))))
def test_score_measures_are_their_definitions(cases):
    from sklearn.metrics import cohen_kappa_score

    from s1flow.client import Score
    from s1flow.eval.kinds import kind_of

    levels, rows = cases
    kind = kind_of(Score(instructions="?", criteria=[str(i) for i in range(levels)]))
    dist = np.array([w for w, _ in rows], dtype=float)
    dist /= dist.sum(axis=1, keepdims=True)
    expected, y = dist @ np.arange(levels), np.array([label for _, label in rows])
    readings = [kind.reading(Average(distributed=True, distribution=list(d), expected=float(e)), DecisionRule()) for d, e in zip(dist, expected)]
    pairs = measure.pairs(kind, list(y), readings)
    said = np.array([r.value for r in readings])
    assert measure.measure("mae", pairs) == pytest.approx(np.mean(np.abs(expected - y)))
    chance = len(set(y)) == 1 and set(y) == set(said)  # every label and every answer one level: nothing to explain
    assert measure.measure("qwk", pairs) == (None if chance else pytest.approx(cohen_kappa_score(y, said, weights="quadratic", labels=range(levels))))


# ---------- properties: the evaluation reads a case as production does, and searches within its constraints ----------


@given(st.data())
def test_reading_again_at_any_rule_is_what_production_reads(data):
    """Pairs.at (the evaluation) and BooleanKind.reading (a policy in production) agree at any rule, at its edges too."""
    p, y = data.draw(binary_cases())
    edges = st.sampled_from(sorted({*p, *(1 - p)}))  # a rule exactly at a case's probability
    rule = DecisionRule(threshold=data.draw(st.none() | edges | PROBABILITY), min_probability=data.draw(st.none() | edges | PROBABILITY))
    kind = BooleanKind()
    production = measure.pairs(kind, [bool(v) for v in y], [kind.reading(Average(distributed=True, p_positive=float(x)), rule) for x in p])
    evaluation = binary_preds(p, y).pairs.at(threshold=rule.threshold, min_probability=rule.min_probability)
    for col in ("value", "probability", "unsure", "correct"):
        assert (np.asarray(getattr(evaluation, col), dtype=object) == getattr(production, col)).all(), col


def chosen(cuts, keeps, value, maximize):
    """The rule search's choice by its definition: of the cuts that keep every constraint, the best value (known
    values first), the lower on a tie; inf when none keeps them."""
    kept = [t for t in cuts if keeps(t)]
    known = [v for t in kept if (v := value(t)) is not None]
    if not kept:
        return np.inf
    if not known:
        return kept[0]
    best = max(known) if maximize else min(known)
    return next(t for t in kept if value(t) == best)


def share_keeps(k, n, bound, at_least):
    return n == 0 or (k / n >= bound if at_least else k / n <= bound)


@given(binary_cases(), st.sampled_from([0.5, 0.8, 0.9, 1.0]))
def test_coverage_chooses_the_widest_min_probability_that_keeps_its_target(cases, target):
    p, y = cases
    said = p >= 0.5
    prob = np.where(said, p, 1 - p)

    def sure(t):
        return prob >= t

    want = chosen(sorted(set(prob)), lambda t: share_keeps(int((sure(t) & (said == y)).sum()), int(sure(t).sum()), target, True),
                  lambda t: float(sure(t).mean()), maximize=True)
    assert metrics.search(bound(Coverage(target_accuracy=target), BooleanKind()), binary_preds(p, y).pairs) == want


@given(binary_cases(), st.sampled_from([0.05, 0.1, 0.25, 0.5]))
def test_recall_chooses_the_threshold_that_keeps_its_false_alarm_cap(cases, cap):
    p, y = cases
    want = chosen(sorted(set(p)), lambda t: share_keeps(int(((p >= t) & ~y).sum()), int((~y).sum()), cap, False),
                  lambda t: float((p >= t)[y].mean()) if y.any() else None, maximize=True)
    assert metrics.search(bound(Recall(max_false_alarm=cap), BooleanKind()), binary_preds(p, y).pairs) == want


FLOORS = [(0.5, None), (0.8, None), (None, 0.5), (None, 0.8), (0.5, 0.5), (0.8, 0.8), (0.5, 0.8)]  # (min_precision, min_recall)


@given(binary_cases(), st.integers(1, 5), st.integers(1, 5), st.sampled_from(FLOORS))
def test_expected_loss_chooses_within_the_floors(cases, fn, fp, floors):
    p, y = cases
    min_precision, min_recall = floors
    constraints = Constraints(min_precision=min_precision, min_recall=min_recall)

    def keeps(t):
        said = p >= t
        tp = int((said & y).sum())
        return ((min_precision is None or share_keeps(tp, int(said.sum()), min_precision, True))
                and (min_recall is None or share_keeps(tp, int(y.sum()), min_recall, True)))

    def loss(t):  # whole losses: summed exactly, so a tie is a tie in either order
        said = p >= t
        return (fn * int((y & ~said).sum()) + fp * int((~y & said).sum())) / len(p)

    got = metrics.search(bound(ExpectedLoss(fn=fn, fp=fp), BooleanKind()), binary_preds(p, y).pairs, floors=measure.floors(constraints))
    assert got == chosen(sorted(set(p)), keeps, loss, maximize=False)


# ---------- properties: the Clopper-Pearson bounds a constraint is judged by ----------


@given(st.integers(1, 2000).flatmap(lambda n: st.tuples(st.integers(0, n), st.just(n))), st.floats(0.01, 0.99))
def test_clopper_pearson_brackets_the_share_and_broken_is_never_kept(kn, bound_):
    from scipy.stats import beta

    k, n = kn
    lo, hi = metrics.cp_lower(k, n), measure.cp_upper(k, n)
    assert 0 <= lo <= k / n <= hi <= 1
    assert lo == (0.0 if k == 0 else pytest.approx(beta.ppf(0.05, k, n - k + 1)))
    if k < n:
        assert metrics.cp_lower(k + 1, n) >= lo
    for at_least in (True, False):
        c = measure.Constraint(count=lambda p: (k, n), bound=bound_, at_least=at_least, what="", limit="", excuse="", beside=None)
        assert not (c.broken(k, n) and c.holds(k, n))
