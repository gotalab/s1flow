"""What each objective is on a set of answers: `MEASURES[(objective name, what is measured)]` over `Pairs`,
one label and the reading of its answers (policies/kinds.py) per case. numpy and scipy.

    p = pairs(kind, labels, readings)     # metrics: read from the runs; feedback: the logged Decision
    bound(objective, kind).value(p)       # the objective's value on those cases
    p.at(threshold=t)                     # the same answers read at another rule (metrics, per fold)

What is measured is the question type, except that a choice scored as P(positive) is measured as a
boolean. A measure never chooses a rule and a rule never knows a measure: metrics finds the
rule on a fold's fit side and measures the eval side read at it, feedback measures what
a policy read. The kind's own numbers (`f1`, `mean_iou`, `mae`, `qwk`, `mean_error`, `brier`, `ece`) are measures too.

A constraint is a share an objective keeps on one side of a bound (Coverage: the accuracy of what is
answered; Recall: the false alarms among the negatives). Only the built-ins hold one.
"""

from dataclasses import dataclass, replace
from typing import Any, Callable, Sequence

import numpy as np
from scipy.special import betaincinv

from ...client.answers import BoxEdges
from ...client.boxes import iou
from ...core.errors import ConfigError
from ...policies.kinds import ABSENT

READ = ("text", "number", "date")  # a value read from the state, whose label may be ABSENT
from ..kinds import Kind, Reading
from .declare import Constraints, Objective


def measured_as(kind: Kind) -> str:
    """What a kind is measured as: its question type, a choice scored as P(positive) a boolean."""
    return "boolean" if kind.binary else kind.type


@dataclass(frozen=True)
class Pairs:
    """Cases as columns: each one's label and the reading of its answers (None when there is no answer: the call
    failed, or the model refused the case)."""

    measured: str  # measured_as(kind)
    options: list[str]  # a choice's keys
    y: np.ndarray  # the labels; bool for a binary question
    ok: np.ndarray  # answered (False: the call failed, there is no reading)
    value: np.ndarray  # the reading's value
    unsure: np.ndarray  # under the rule's min_probability (a failed call too)
    min_probability_set: np.ndarray  # distinguishes an unconfigured lower bound from a passed one
    correct: np.ndarray  # kind.correct (a failed call is never right)
    probability: np.ndarray  # of the value, a box's confidence: what min_probability reads (0 when failed)
    p_positive: np.ndarray  # binary: P(positive) (0.5 when failed)
    distribution: np.ndarray | None  # choice and score: (cases, options or levels), uniform when failed
    confidence: np.ndarray  # box (0 when failed)
    expected: np.ndarray  # score: the expected level (nan when failed, and for the other kinds)
    levels: int = 0  # score: L, its levels 0..L-1
    bounds: tuple[float, float] = (0.0, 0.0)  # estimate: the question's range

    def __len__(self) -> int:
        return len(self.y)

    def __getitem__(self, idx: np.ndarray) -> "Pairs":
        return Pairs(  # not dataclasses.replace: a bootstrap takes thousands of these
            measured=self.measured, options=self.options, levels=self.levels, bounds=self.bounds, y=self.y[idx], ok=self.ok[idx], value=self.value[idx], unsure=self.unsure[idx], min_probability_set=self.min_probability_set[idx], correct=self.correct[idx],
            probability=self.probability[idx], p_positive=self.p_positive[idx], confidence=self.confidence[idx],
            distribution=None if self.distribution is None else self.distribution[idx], expected=self.expected[idx],
        )

    @property
    def sure(self) -> np.ndarray:
        return self.ok & ~self.unsure

    @property
    def said(self) -> np.ndarray:
        """Binary: read True (a failed call raises no alarm)."""
        return self.ok & np.asarray(self.value == True, dtype=bool)  # noqa: E712 (an object array)

    def reads(self, field: str) -> np.ndarray:
        """What a rule field is compared with: P(positive) for a threshold, the probability for a min probability."""
        return self.p_positive if field == "threshold" else self.probability

    def at(self, threshold: float | np.ndarray | None = None, min_probability: float | np.ndarray | None = None) -> "Pairs":
        """The answered cases, read at the plain rule, read again at another one (per case, when arrays):
        a threshold makes the value P(positive) at or above it, a min probability marks what is under it unsure.
        inf reads nothing as True, or every case as unsure. A case with no answer has nothing to read again:
        at every rule it stays wrong and unsure."""
        out = self
        if threshold is not None:
            value = self.p_positive >= threshold
            out = replace(out, value=value, probability=np.where(value, self.p_positive, 1 - self.p_positive), correct=self.ok & (value == self.y))
        if min_probability is not None:
            out = replace(out, unsure=~self.ok | (out.probability < min_probability), min_probability_set=np.ones(len(out), dtype=bool))
        return out


def pairs(kind: Kind, labels: Sequence[Any], readings: Sequence[Reading | None]) -> Pairs:
    """Each label with the reading of its case (None: the call failed)."""
    n, options = len(labels), kind.options
    levels = int(getattr(kind, "levels", 0)) if kind.type == "score" else 0
    # A choice with a positive option is measured as a boolean. Normalize its
    # labels once for both metric truth values and correctness.
    normalized = [kind.as_label(label) for label in labels]
    y = np.empty(n, dtype=object)
    for i, v in enumerate(normalized):  # one at a time: a label that is a tuple stays one value
        y[i] = v
    if n and kind.type not in (*READ, "box") and all(isinstance(v, bool) for v in normalized):  # these keep ABSENT as it is
        y = y.astype(bool)
    value = np.empty(n, dtype=object)
    for i, r in enumerate(readings):
        value[i] = None if r is None else r.value
    width = len(options) or levels
    flat = [1 / width] * width if width else []
    has_dist = any(r is not None and r.distribution is not None for r in readings)
    return Pairs(
        measured=measured_as(kind), options=options, y=y, value=value,
        ok=np.array([r is not None for r in readings], dtype=bool),
        unsure=np.array([r is None or r.below_min_probability is True for r in readings], dtype=bool),
        min_probability_set=np.array([r is not None and r.below_min_probability is not None for r in readings], dtype=bool),
        correct=np.array([kind.correct(t, r) for t, r in zip(normalized, readings)], dtype=bool),
        probability=np.array([0.0 if r is None else r.probability if r.probability is not None else (r.confidence or 0.0) for r in readings], dtype=float),
        p_positive=np.array([0.5 if r is None or r.p_positive is None else r.p_positive for r in readings], dtype=float),
        distribution=np.array([flat if r is None or r.distribution is None else r.distribution for r in readings], dtype=float) if has_dist else None,
        confidence=np.array([0.0 if r is None or r.confidence is None else r.confidence for r in readings], dtype=float),
        expected=np.array([np.nan if r is None or r.expected is None else r.expected for r in readings], dtype=float), levels=levels,
        bounds=(float(getattr(kind, "low", 0.0)), float(getattr(kind, "high", 0.0))) if kind.type == "estimate" else (0.0, 0.0),
    )


# ---------- proportions ----------


def cp_lower(k: int, n: int, level: float = 0.95) -> float:
    """One-sided Clopper-Pearson lower bound on a proportion."""
    if n == 0 or k == 0:
        return 0.0
    return float(betaincinv(k, n - k + 1, 1 - level))  # scipy.stats.beta.ppf, without importing scipy.stats (most of a second)


def cp_upper(k: int, n: int, level: float = 0.95) -> float:
    return 1 - cp_lower(n - k, n, level)


def cp_interval(k: int, n: int) -> tuple[float, float]:
    """Two-sided 95% Clopper-Pearson interval on a proportion: each side at 97.5%."""
    return cp_lower(k, n, 0.975), cp_upper(k, n, 0.975)


@dataclass(frozen=True)
class Constraint:
    """A share kept on one side of a bound while the objective's value is made best."""

    count: Callable[[Pairs], tuple[int, int]]  # (cases that count, out of)
    bound: float
    at_least: bool  # the share must reach the bound (else stay at or under it)
    what: str  # the share, in words
    beside: str | None  # its name beside the objective's value in a report (None: Coverage's is a column of its own)

    @property
    def shown_broken(self) -> str:
        """What `broken` found, in words."""
        return "its upper bound is under the target" if self.at_least else "its lower bound is over the cap"

    def rate(self, p: Pairs) -> float | None:
        k, n = self.count(p)
        return k / n if n else None

    def holds(self, k: int, n: int) -> bool | None:
        """At the point value; None with nothing to count."""
        if not n:
            return None
        return k / n >= self.bound if self.at_least else k / n <= self.bound

    def broken(self, k: int, n: int, level: float = 0.95) -> bool:
        """Shown on the wrong side of the bound: the one-sided Clopper-Pearson bound past it."""
        if not n:
            return False
        return cp_upper(k, n, level) < self.bound if self.at_least else cp_lower(k, n, level) > self.bound


# ---------- the measures ----------

Params = dict[str, Any]


@dataclass(frozen=True)
class Measure:
    value: Callable[[Pairs, Params], float | None]
    constraint: Callable[[Params], Constraint] | None = None
    heavy: bool = False  # slow (many options): an interval takes the first HEAVY draws only
    # what it is on, as the comparison defines its metric ({reading}: the plain reading it reads the answers at);
    # None: shown only as an objective
    basis: str | None = None


# One bootstrap draws BOOTSTRAP resamples of the cases (the evaluation's intervals);
# a heavy measure is read on the first HEAVY of them.
BOOTSTRAP = 1000
HEAVY = 200


def interval(draws: Sequence[float]) -> tuple[float, float] | None:
    """A bootstrap's 95% interval: the 2.5th and 97.5th percentiles of its draws (None without any)."""
    return (float(np.quantile(draws, 0.025)), float(np.quantile(draws, 0.975))) if draws else None


def finite(x: float) -> float | None:
    """A value or a rule's cut as an evaluation stores it: None when it is no number (nothing to measure) or infinite
    (no cut keeps the constraint)."""
    return float(x) if np.isfinite(x) else None


def _auc(pos: np.ndarray, score: np.ndarray) -> float | None:
    """Mann-Whitney AUROC with average ranks for ties (same as sklearn, much faster)."""
    n1 = int(pos.sum())
    n0 = len(pos) - n1
    if n1 == 0 or n0 == 0:
        return None
    r = _ranks(score)
    return float((r[pos].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def _ranks(x: np.ndarray) -> np.ndarray:
    """The 1-based ranks of `x`, ties at their average: scipy.stats.rankdata's default, without its per-call checks
    (a bootstrap ranks each of its draws)."""
    order = np.argsort(x, kind="mergesort")
    xs = x[order]
    new = np.concatenate(([True], xs[1:] != xs[:-1]))
    starts = np.concatenate((np.flatnonzero(new), [len(x)]))
    group = np.cumsum(new) - 1
    ranks = np.empty(len(x))
    ranks[order] = (starts[group] + starts[group + 1] + 1) / 2
    return ranks


def _f1(tp: np.ndarray, true: np.ndarray, said: np.ndarray) -> np.ndarray:
    """F1 per class as sklearn computes it (2 tp / (true + predicted), 0 when both are 0)."""
    denom = 1.0 * true.astype(float) + said.astype(float)
    num = 2.0 * tp.astype(float)
    out = num / np.where(denom == 0, 1.0, denom)
    out[denom == 0] = 0.0
    return out


def _ious(p: Pairs) -> np.ndarray:
    """A box task: the IoU of each case's box with its label box (0 when failed). Where the label or the answer is
    no box: 1 when both are, 0 when one is."""
    def one(v: Any, t: Any) -> float:
        if t is ABSENT or v is None:
            return 1.0 if t is ABSENT and v is None else 0.0
        return iou(v, BoxEdges.model_validate(t))

    return np.array([one(v, t) if ok else 0.0 for v, t, ok in zip(p.value, p.y, p.ok)], dtype=float)


# ---------- the loss table (Loss; Accuracy and ExpectedLoss are fixed forms of it) ----------


@dataclass(frozen=True)
class Table:
    """What each answer loses on each label: `loss[label, said]`, 0 on the diagonal. A failed call loses
    `unsure` when the table sets one, else the most its label's row loses; an unsure answer loses `unsure`
    when there is one (the table then chooses a min probability), else it is read as given."""

    keys: list[Any]  # the labels in order: True, False for a binary question, else a choice's options
    loss: np.ndarray  # (len(keys), len(keys))
    unsure: float | None = None

    def total(self, p: Pairs) -> float:
        """The cases' summed loss: each cell's loss times its count, the cells in order (so ExpectedLoss adds its
        misses before its false alarms, as it always has), then the failed and unsure cases."""
        counted = p.ok if self.unsure is None else p.sure
        wrong = counted & ~p.correct
        k, total = len(self.keys), 0.0
        if wrong.any():
            counts = np.bincount(self._codes(p.y[wrong]) * k + self._codes(p.value[wrong]), minlength=k * k).reshape(k, k)
            for a in range(k):
                for b in range(k):
                    if counts[a, b] and self.loss[a, b]:
                        total += float(self.loss[a, b]) * int(counts[a, b])
        rest = ~counted
        if rest.any():
            if self.unsure is not None:
                total += self.unsure * int(rest.sum())
            else:
                for a, c in enumerate(np.bincount(self._codes(p.y[rest]), minlength=k)):
                    if c and self.loss[a].max():
                        total += float(self.loss[a].max()) * int(c)
        return total

    def _codes(self, xs: np.ndarray) -> np.ndarray:
        if self.keys == [True, False]:  # a binary question, in the bootstrap's inner loop: no Python loop
            return np.where(np.asarray(xs == True, dtype=bool), 0, 1)  # noqa: E712 (an object array)
        at = {key: i for i, key in enumerate(self.keys)}
        return np.array([at[bool(x)] if isinstance(x, (bool, np.bool_)) else at[x] for x in xs], dtype=int)


def table(params: Params, keys: list[Any]) -> Table:
    """Loss' params on these labels: `default` for every error, `losses` by label then answer ("true" / "false"
    for a binary question), `unsure`."""
    named = {str(k).lower() if isinstance(k, bool) else k: i for i, k in enumerate(keys)}
    loss = np.full((len(keys), len(keys)), float(params["default"]))
    np.fill_diagonal(loss, 0.0)
    for t, row in params["losses"].items():
        for said, c in row.items():
            loss[named[t], named[said]] = float(c)
    return Table(keys=keys, loss=loss, unsure=None if params["unsure"] is None else float(params["unsure"]))


def _labels(p: Pairs) -> list[Any]:
    return [True, False] if p.measured == "boolean" else list(p.options)


def _loss(p: Pairs, params: Params) -> float | None:
    return table(params, _labels(p)).total(p) / len(p) if len(p) else None


def _accuracy(p: Pairs, _: Params) -> float | None:
    """The share right: the table where every error loses 1 (and a failed call is an error), read as 1 - its
    mean loss. Counted as (n - errors) / n, which is the share right exactly."""
    if not len(p):
        return None
    return (len(p) - float(np.count_nonzero(~p.correct))) / len(p)


def _coverage(p: Pairs, _: Params) -> float | None:
    return float(p.sure.mean()) if len(p) else None


def _sure_accuracy(params: Params) -> Constraint:
    t = float(params["target_accuracy"])
    return Constraint(count=lambda p: (int((p.sure & p.correct).sum()), int(p.sure.sum())), bound=t, at_least=True,
                      what="sure accuracy", beside=None)


def _recall(p: Pairs, _: Params) -> float | None:
    return float(p.said[p.y].mean()) if p.y.any() else None


def _precision(p: Pairs, _: Params) -> float | None:
    said = p.said
    return float((said & p.y).sum() / said.sum()) if said.any() else None


def _false_alarms(params: Params) -> Constraint:
    m = float(params["max_false_alarm"])
    return Constraint(count=lambda p: (int((p.said & ~p.y).sum()), int((~p.y).sum())), bound=m, at_least=False,
                      what="false-alarm rate", beside="false alarms")


FLOOR_COUNTS: dict[str, Callable[[Pairs], tuple[int, int]]] = {
    "precision": lambda p: (int((p.said & p.y).sum()), int(p.said.sum())),
    "recall": lambda p: (int((p.said & p.y).sum()), int(p.y.sum())),
}


def floors(c: Constraints) -> list[Constraint]:
    """The task's floors (Constraints.min_precision, min_recall), each a share kept at or above its bound."""
    return [Constraint(count=FLOOR_COUNTS[name], bound=v, at_least=True, what=name, beside=name) for name, v in c.floors.items()]


def _expected_loss(p: Pairs, params: Params) -> float | None:
    """The binary table with a miss losing fn and a false alarm fp."""
    t = Table(keys=[True, False], loss=np.array([[0.0, float(params["fn"])], [float(params["fp"]), 0.0]]))
    return t.total(p) / len(p) if len(p) else None


def _auroc_binary(p: Pairs, _: Params) -> float | None:
    return _auc(p.y.astype(bool), p.p_positive)


def _auroc_choice(p: Pairs, _: Params) -> float | None:
    assert p.distribution is not None
    scores = [a for j, c in enumerate(p.options) if (a := _auc(p.y == c, p.distribution[:, j])) is not None]
    return float(np.mean(scores)) if scores else None


def _auroc_box(p: Pairs, _: Params) -> float | None:
    return _auc(p.correct, p.confidence)  # does the confidence rank hits above misses


def _auroc_hit(p: Pairs, _: Params) -> float | None:
    return _auc(p.correct, p.probability)  # does what min_probability reads rank the right answers above the wrong


def _brier_hit(p: Pairs, _: Params) -> float | None:
    return float(np.mean((p.probability - p.correct) ** 2))


def _there(p: Pairs) -> np.ndarray:
    """A value read from the state: the cases labelled with a value (the rest are labelled absent)."""
    return np.array([y is not ABSENT for y in p.y], dtype=bool)


def _value_accuracy(p: Pairs, _: Params) -> float | None:
    there = _there(p)
    return float(p.correct[there].mean()) if there.any() else None


def _absent_accuracy(p: Pairs, _: Params) -> float | None:
    there = _there(p)
    return float(p.correct[~there].mean()) if (~there).any() else None


def _options(p: Pairs) -> tuple[int, int, int]:
    """A multichoice, option by option over the cases: chosen and in the label, chosen, in the label. No answer chose nothing."""
    chosen = [set(v) if ok else set() for v, ok in zip(p.value, p.ok)]
    return sum(len(c & set(y)) for c, y in zip(chosen, p.y)), sum(map(len, chosen)), sum(len(y) for y in p.y)


def _option_precision(p: Pairs, _: Params) -> float | None:
    hit, chosen, _labelled = _options(p)
    return hit / chosen if chosen else None


def _option_recall(p: Pairs, _: Params) -> float | None:
    hit, _chosen, labelled = _options(p)
    return hit / labelled if labelled else None


def _option_f1(p: Pairs, _: Params) -> float | None:
    hit, chosen, labelled = _options(p)
    return 2 * hit / (chosen + labelled) if chosen + labelled else None


def _mean_error(p: Pairs, _: Params) -> float | None:
    """An estimate's mean distance from its label; a failed call is as far off as its label can be in the range."""
    if not len(p):
        return None
    y = p.y.astype(float)
    far = np.maximum(y - p.bounds[0], p.bounds[1] - y)
    return float(np.mean(np.where(p.ok, np.abs(np.where(p.ok, p.expected, y) - y), far)))


def _f1_binary(p: Pairs, _: Params) -> float | None:
    said, y = p.said, p.y.astype(bool)
    return float(_f1(np.array([np.sum(y & said)]), np.array([np.sum(y)]), np.array([np.sum(said)]))[0])


def _f1_macro(p: Pairs, _: Params) -> float | None:
    said = [p.ok & (p.value == c) for c in p.options]
    tp = np.array([np.sum((p.y == c) & s) for c, s in zip(p.options, said)])
    f = _f1(tp, np.array([np.sum(p.y == c) for c in p.options]), np.array([np.sum(s) for s in said]))
    return float(np.mean(f))


def _mean_iou(p: Pairs, _: Params) -> float | None:
    return float(_ious(p).mean()) if len(p) else None


def _brier_binary(p: Pairs, _: Params) -> float | None:
    return float(np.mean((p.p_positive - p.y) ** 2))


def _brier_choice(p: Pairs, _: Params) -> float | None:
    assert p.distribution is not None
    onehot = np.array([[1.0 if yi == c else 0.0 for c in p.options] for yi in p.y])
    return float(np.mean(((p.distribution - onehot) ** 2).sum(axis=1)))


def _brier_box(p: Pairs, _: Params) -> float | None:
    return float(np.mean((p.confidence - p.correct) ** 2))


def _gaps(p: Pairs) -> tuple[np.ndarray, np.ndarray]:
    """A score's labels and levels said, as ints; a failed call said the level farthest from its label."""
    y = p.y.astype(int)
    far = np.where(y < (p.levels - 1) / 2, p.levels - 1, 0)
    said = np.where(p.ok, np.array([-1 if v is None else v for v in p.value], dtype=int), far)
    return y, said


def _mae(p: Pairs, _: Params) -> float | None:
    if not len(p):
        return None
    y, said = _gaps(p)
    expected = np.where(p.ok, p.expected, said)
    return float(np.mean(np.abs(expected - y)))


def _qwk(p: Pairs, _: Params) -> float | None:
    """Cohen's kappa with quadratic weights over the levels (as sklearn's cohen_kappa_score(weights="quadratic")).
    None when chance agreement leaves nothing to explain (every label and every answer one level)."""
    if not len(p):
        return None
    y, said = _gaps(p)
    k = p.levels
    observed = np.bincount(y * k + said, minlength=k * k).reshape(k, k).astype(float)
    expected = np.outer(np.bincount(y, minlength=k), np.bincount(said, minlength=k)) / len(p)
    w = (np.subtract.outer(np.arange(k), np.arange(k)) ** 2).astype(float)
    chance = float((w * expected).sum())
    return None if chance == 0 else 1 - float((w * observed).sum()) / chance


def _cumulative(p: Pairs) -> np.ndarray:
    """P(level >= k) for k = 1..L-1, per case: summed from the top, so equal tails stay equal floats (a tie for AUROC)."""
    assert p.distribution is not None
    return np.cumsum(p.distribution[:, ::-1], axis=1)[:, ::-1][:, 1:]


def _auroc_score(p: Pairs, _: Params) -> float | None:
    """The mean over the cuts k = 1..L-1 of AUROC(label >= k, P(level >= k)): does the distribution rank the cases
    above each cut first, the reading a gate on "level k or more" uses."""
    if p.distribution is None:
        return None
    y, above = p.y.astype(int), _cumulative(p)
    scores = [a for k in range(1, p.levels) if (a := _auc(y >= k, above[:, k - 1])) is not None]
    return float(np.mean(scores)) if scores else None


def _brier_score(p: Pairs, _: Params) -> float | None:
    """The ranked probability score (ScoreKind.brier), the mean over the cases."""
    if p.distribution is None or not len(p):
        return None
    y, above = p.y.astype(int), _cumulative(p)
    truth = (y[:, None] >= np.arange(1, p.levels)[None, :]).astype(float)
    return float(np.mean(((above - truth) ** 2).sum(axis=1) / (p.levels - 1)))


def _ece(p: Pairs, _: Params, bins: int = 10) -> float | None:
    """Expected calibration error: the probability against the share right, over equal bins (the first closed at 0)."""
    conf, correct = p.probability, p.correct
    edges = np.linspace(0, 1, bins + 1)
    total = 0.0
    for i in range(bins):
        m = (conf > edges[i]) & (conf <= edges[i + 1]) if i else (conf >= 0) & (conf <= edges[1])
        if m.any():
            total += m.mean() * abs(conf[m].mean() - correct[m].mean())
    return float(total)


_ACCURACY = Measure(_accuracy, basis="{reading}; correct / labelled dev cases")
_COVERAGE = Measure(_coverage, _sure_accuracy)

# What each metric is on each kind (what it is called is METRICS', declare.py). A basis is what the comparison
# says it is measured on: {reading} is the plain reading of the answers it is read at.
MEASURES: dict[tuple[str, str], Measure] = {
    ("accuracy", "boolean"): _ACCURACY,
    ("accuracy", "choice"): _ACCURACY,
    ("accuracy", "box"): _ACCURACY,
    ("accuracy", "score"): _ACCURACY,
    ("coverage", "boolean"): _COVERAGE,
    ("coverage", "choice"): _COVERAGE,
    ("coverage", "box"): _COVERAGE,
    ("coverage", "score"): _COVERAGE,
    ("recall", "boolean"): Measure(_recall, _false_alarms, basis="{reading}; true positives / labelled positives among labelled dev cases"),
    ("precision", "boolean"): Measure(_precision, basis="{reading}; true positives / predicted positives among labelled dev cases"),
    ("expected_loss", "boolean"): Measure(_expected_loss),
    ("loss", "boolean"): Measure(_loss),
    ("loss", "choice"): Measure(_loss),
    ("auroc", "boolean"): Measure(_auroc_binary, basis="genuine model probabilities; binary positive-vs-negative AUROC over labelled dev cases"),
    ("auroc", "choice"): Measure(_auroc_choice, heavy=True,
                                 basis="genuine model probabilities; macro one-v-rest AUROC over options and labelled dev cases"),
    ("auroc", "box"): Measure(_auroc_box, basis="recorded box confidence; hit-ranking AUROC over labelled dev cases"),
    ("auroc", "score"): Measure(_auroc_score, basis="genuine model probabilities; mean over the cuts k of AUROC(label >= k, P(level >= k)) "
                                                    "over labelled dev cases"),
    ("mae", "score"): Measure(_mae, basis="expected level; mean absolute error in levels over labelled dev cases"),
    ("qwk", "score"): Measure(_qwk, basis="{reading}; quadratic weighted kappa over labelled dev cases"),
    ("f1", "boolean"): Measure(_f1_binary, basis="{reading}; harmonic mean of precision and recall over labelled dev cases"),
    ("macro_f1", "choice"): Measure(_f1_macro, basis="{reading}; mean of per-class F1 over labelled dev cases"),
    # the kinds' own numbers (Kind.report), and the calibration every evaluation reports
    ("mean_iou", "box"): Measure(_mean_iou, basis="{reading}; mean IoU over labelled dev cases"),
    ("mean_error", "estimate"): Measure(_mean_error, basis="the estimate; mean distance from the label, in the question's unit, "
                                                             "over labelled dev cases"),
    ("accuracy", "estimate"): _ACCURACY,
    ("coverage", "estimate"): _COVERAGE,
    ("auroc", "estimate"): Measure(_auroc_hit, basis="narrowness of the p10 - p90 interval; hit-ranking AUROC over labelled dev cases"),
    ("brier", "estimate"): Measure(_brier_hit, basis="narrowness of the p10 - p90 interval; Brier score of hit correctness over labelled dev cases"),
    ("ece", "estimate"): Measure(_ece, basis="narrowness of the p10 - p90 interval; calibration of hit correctness over labelled dev cases"),
    ("accuracy", "multichoice"): _ACCURACY,
    ("coverage", "multichoice"): _COVERAGE,
    ("auroc", "multichoice"): Measure(_auroc_hit, basis="probability of the whole set chosen; hit-ranking AUROC over labelled dev cases"),
    ("brier", "multichoice"): Measure(_brier_hit, basis="probability of the whole set chosen; Brier score of answer correctness over labelled dev cases"),
    ("ece", "multichoice"): Measure(_ece, basis="probability of the whole set chosen; calibration of answer correctness over labelled dev cases"),
    ("option_f1", "multichoice"): Measure(_option_f1, basis="{reading}; F1 over every option of every labelled dev case (micro)"),
    ("option_precision", "multichoice"): Measure(_option_precision, basis="{reading}; options chosen that the label has / options chosen"),
    ("option_recall", "multichoice"): Measure(_option_recall, basis="{reading}; options chosen that the label has / options the labels have"),
    **{(name, read): m for read in ("text", "number", "date") for name, m in {
        "accuracy": _ACCURACY,
        "coverage": _COVERAGE,
        "auroc": Measure(_auroc_hit, basis="probability of the value read; hit-ranking AUROC over labelled dev cases"),
        "brier": Measure(_brier_hit, basis="probability of the value read; Brier score of answer correctness over labelled dev cases"),
        "ece": Measure(_ece, basis="probability of the value read; calibration of answer correctness over labelled dev cases"),
        "value_accuracy": Measure(_value_accuracy, basis="{reading}; correct / labelled dev cases whose label is a value"),
        "absent_accuracy": Measure(_absent_accuracy, basis="{reading}; correct / labelled dev cases labelled absent"),
    }.items()},
    ("brier", "boolean"): Measure(_brier_binary, basis="genuine model probabilities; binary Brier score over labelled dev cases"),
    ("brier", "choice"): Measure(_brier_choice, basis="genuine model probabilities; multiclass Brier score over labelled dev cases"),
    ("brier", "box"): Measure(_brier_box, basis="recorded box confidence; Brier score of hit correctness over labelled dev cases"),
    ("brier", "score"): Measure(_brier_score, basis="genuine model probabilities; ranked probability score over (levels - 1), "
                                                    "over labelled dev cases"),
    ("ece", "boolean"): Measure(_ece, basis="genuine model probabilities; calibration of answer correctness over labelled dev cases"),
    ("ece", "choice"): Measure(_ece, basis="genuine model probabilities; calibration of selected-answer correctness over labelled dev cases"),
    ("ece", "box"): Measure(_ece, basis="recorded box confidence; calibration of hit correctness over labelled dev cases"),
    ("ece", "score"): Measure(_ece, basis="genuine model probabilities; calibration of the rounded level's correctness over labelled dev cases"),
}


@dataclass(frozen=True)
class Bound:
    """An objective with what measures it, for one kind."""

    objective: Objective
    measure: Measure
    constraint: Constraint | None

    def value(self, p: Pairs) -> float | None:
        return self.measure.value(p, self.objective.params)

    @property
    def heavy(self) -> bool:
        return self.measure.heavy


def bound(o: Objective, kind: Kind, custom: dict[str, Measure] | None = None) -> Bound:
    """`custom`: what measures the task's custom objectives (Task.custom_measures), by key."""
    if o.code_sha256 is not None:
        if (mine := (custom or {}).get(o.key)) is None:
            raise ConfigError(f"{o.name} is a custom objective, and task.py defines no such function (with these params) to measure it")
        return Bound(o, mine, None)
    m = MEASURES.get((o.name, measured_as(kind)))
    if m is None:
        raise ConfigError(f"nothing measures {o.name} on a {measured_as(kind)} question")
    return Bound(o, m, None if m.constraint is None else m.constraint(o.params))


def measure(name: str, p: Pairs) -> float | None:
    """A measure that takes no params (a kind's own number)."""
    return MEASURES[(name, p.measured)].value(p, {})


# ---------- per case ----------


def shown(p: Pairs, i: int) -> tuple[bool | str, bool | str]:
    """One case's label and reading, as a list of errors writes them."""
    if p.measured == "box":
        if p.y[i] is ABSENT or p.value[i] is None:
            return "absent" if p.y[i] is ABSENT else "box", "absent" if p.value[i] is None else "box"
        return "box", f"IoU {_ious(p[np.array([i])])[0]:.2f}"
    if p.measured == "multichoice":
        return written(p, p.y[i]), written(p, p.value[i])
    if p.measured in READ:
        return "absent" if p.y[i] is ABSENT else str(p.y[i]), "absent" if p.value[i] is None else str(p.value[i])
    return plain(p.y[i]), plain(p.value[i])


def written(p: Pairs, v: Any) -> Any:
    """A label or a reading as a report writes it: a value read that is not there is `absent`."""
    if p.measured == "multichoice" and isinstance(v, (tuple, list)):
        return ", ".join(v) or "none"
    return "absent" if p.measured in READ and (v is ABSENT or v is None) else plain(v)


def plain(v: Any) -> Any:
    return bool(v) if isinstance(v, (bool, np.bool_)) else str(v)
