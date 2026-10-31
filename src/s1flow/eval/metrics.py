"""Metrics over cached answers: the one place that turns runs into an `Evaluation`. No model calls.

One path for every number: the answers to a case are averaged and read by the question's
kind (policies/kinds.py), as a policy reads them in production, and each label with its reading
makes the pairs every measure reads (objectives/measure.py). An objective that sets a rule has it
chosen on each fold's fit side (`search`) and is measured on the eval side read at it; the rule a
policy uses is chosen on all the dev cases. One bootstrap of the cases per evaluation gives every
interval, and the held-out test share is read at the rules chosen on the rest.

    the rule search  with a constraint (the objective's own, and the task's floors on the primary's threshold):
                        the observed probabilities are the candidates, the best value among those that keep
                        every one, the lower on a tie. Without: a grid (5 points under 50 dev cases, else 19),
                        the best, the nearer 0.5 on a tie. None keeps them: that fold answers nothing, and the
                        policy has no rule (None).
"""

from __future__ import annotations

import json
from collections.abc import Sequence
from dataclasses import dataclass, field, replace
from typing import Any, Literal, cast

import numpy as np

from ..client import cost
from ..client.answers import CostSource
from ..client.identity import request_digest, require_provider_revision, model_digest
from ..client.models import ModelSpec, Price
from ..core.errors import NotFound
from ..policies.kinds import Reading
from ..policies.rule import DecisionRule
from .candidate import Candidate
from . import evalset, records
from . import split as splitting
from .evaluation import (
    Calls, ErrorLossThreshold, Estimate, Evaluation, Failures, Floor, HighConfidenceError, Latency, ObjectiveScore, Selective, SweepRow,
    TestResult, Throughput, ChartData, ThresholdPoint, ProbabilityBin, CalibrationPoint, SelectionPoint, DistributionEvidence,
)
from .objectives import measure
from .objectives.declare import AUROC, Accuracy, Coverage, ExpectedLoss
from .objectives.measure import BOOTSTRAP, HEAVY, Bound, Constraint, Pairs, bound, cp_lower, finite
from .records import PredictionRecord
from .policy import TestVerdict
from .run import prompt_hash, run_path
from .task import Task

HIGH_CONF = 0.9
TEST_BOOTSTRAP = 500
PLAIN = DecisionRule()  # what the cases are read at before a rule is chosen
GRID = np.round(np.arange(0.05, 0.96, 0.05), 2)
SMALL_GRID = np.array([0.1, 0.3, 0.5, 0.7, 0.9])  # under splitting.SMALL dev cases

# ---------- loading ----------


@dataclass
class Preds:
    model: str
    ids: list[str]
    pairs: Pairs  # each scored case's label and the reading of its answer, at the plain rule
    probabilities: bool  # False when the model returned single answers only
    distribution: DistributionEvidence | None = None  # actual current answer evidence
    latency_ms: np.ndarray = field(default_factory=lambda: np.array([]))
    case_latency_ms: np.ndarray = field(default_factory=lambda: np.array([]))  # per scored case (as ids): its call's latency, nan unrecorded
    retries: list[int | None] = field(default_factory=list)  # per answered record, like latency_ms
    concurrency: list[int | None] = field(default_factory=list)
    spend: cost.Spend = field(default_factory=cost.Spend)  # the answered calls' API cost
    call_ids: list[str] = field(default_factory=list)  # answered records, aligned with call timing/usage
    call_costs: list[tuple[float | None, CostSource | None]] = field(default_factory=list)
    price: Price | None = None  # the model's list price, when a cost was estimated from it
    input_tokens: np.ndarray = field(default_factory=lambda: np.array([]))
    calls: int = 0
    failed: int = 0
    unsupported: int = 0  # refused before or by the provider (records.REFUSED)
    data_errors: int = 0  # the task's own errors (records: data_error)
    unlabeled: int = 0
    never_asked: list[str] = field(default_factory=list)  # labelled cases with no record under this question
    failed_cases: list[str] = field(default_factory=list)  # labelled cases asked, no answer: every call failed (like never asked)
    refused_cases: list[str] = field(default_factory=list)  # labelled cases refused or unsupported: the model's limit, not scored
    measured: dict[str, int] | None = None  # wall time of the last uncached run (run.py)
    version: str | None = None  # the answering model scored here (Response.answered_by)
    versions: list[str] = field(default_factory=list)  # every answering model on file, latest first

    @property
    def y(self) -> np.ndarray:
        return self.pairs.y


def select(lines: list[PredictionRecord], prompt: str, version: str | None = None) -> tuple[list[PredictionRecord], str | None, list[str]]:
    """The records to score: lines for this prompt, from one answering model (default: the one
    that answered last), the latest line per case. A case that model never answered
    keeps its latest refusal or failure, so it still counts as unsupported or failed."""
    lines = [r for r in lines if r.prompt == prompt]
    answered = sorted((r for r in lines if r.answered), key=lambda r: r.at)
    versions = list(dict.fromkeys(r.answered_by for r in reversed(answered) if r.answered_by))
    chosen = version or (versions[0] if versions else None)
    if version and version not in versions:
        raise NotFound(f"no answers from {version}; answered by: {', '.join(versions) or 'none'}")
    best: dict[str, PredictionRecord] = {}
    for r in sorted(lines, key=lambda r: r.at):
        k = r.id
        if r.answered:
            if r.answered_by == chosen:
                best[k] = r
        elif k not in best or not best[k].answered:
            best[k] = r
    return list(best.values()), chosen, versions


def _spec(task: Task, name: str) -> ModelSpec | None:
    """The model's entry in the project's s1flow.toml; None for a task outside a project or a name no longer there."""
    if task.project is None:
        return None
    return task.project.lineup().models.get(name.partition(":")[0])


def load(task: Task, variant: str, model: str, *, include_test: bool = False) -> Preds:
    """The run of `model` (`jev`, or `jev:1.14` for a version run of its own), scored on its latest answering model."""
    path = run_path(task, variant, model)
    if not path.exists():
        raise NotFound(f"no run for {model} on {task.id}/{variant}; s1flow run it first")
    prompt = prompt_hash(task.questions(variant))
    sf = evalset.current(task)
    cases = [c for c in task.load_cases().all() if include_test or sf.assign.get(c.id) != "test"]
    # Never bless historical answers using today's identity. A record must carry
    # the identity measured at the call, and match the current materialized input.
    effective = task.where.lineup().resolved(model)
    require_provider_revision(effective)
    expected: dict[str, str] = {}
    for c in cases:
        try:
            expected[c.id] = request_digest(effective, task.model_state(c), task.questions(variant))
        except Exception:
            continue  # unmaterializable input has no reusable answer
    lines = [r for r in records.read(path) if r.request_digest and r.request_digest == expected.get(r.id)]
    meta_path = path.with_suffix(".meta.json")
    meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}
    requested = meta.get("requested", {})
    expected_concurrency = effective.concurrency
    if requested.get("model_digest") == model_digest(effective) and requested.get("declared_concurrency") == effective.concurrency:
        expected_concurrency = requested.get("concurrency")
    # Reuse a genuine raw answer while refusing to carry its timing into a
    # different measurement configuration. Only --fresh can measure that width.
    if expected_concurrency is not None:
        lines = [r if r.concurrency == expected_concurrency else r.model_copy(update={"latency_ms": None, "retries": None, "concurrency": None})
                 for r in lines]
    recs, chosen, versions = select(lines, prompt)
    asked = {r.id for r in lines if r.prompt == prompt}
    ok = [r for r in recs if r.answered]
    kind = task.kind
    spec = _spec(task, model)
    price = spec.price if spec else None
    # A list cost is worked out here from the tokens, with s1flow.toml's price as it is now: a corrected price needs no call.
    spend = cost.Spend()
    for r in ok:
        spend.add(*cost.recorded(r.usage, price))
    pr = Preds(
        model=model, ids=[], pairs=measure.pairs(kind, [], []), probabilities=False,
        latency_ms=np.array([np.nan if r.latency_ms is None else r.latency_ms for r in ok]),
        retries=[r.retries for r in ok],
        concurrency=[r.concurrency for r in ok],
        spend=spend, call_ids=[r.id for r in ok], call_costs=[cost.recorded(r.usage, price) for r in ok],
        price=price if "list" in spend.sources else None,
        input_tokens=np.array([r.usage.input_tokens if r.usage else 0 for r in ok]),
        calls=len(recs),
        failed=sum(r.outcome == "failed" for r in recs),
        unsupported=sum(r.outcome in records.REFUSED for r in recs),
        data_errors=sum(r.outcome == "data_error" for r in recs),
        version=chosen,
        versions=versions,
    )
    if include_test and meta.get("measured"):
        measured = meta["measured"]
        if expected_concurrency is None or measured.get("concurrency") == expected_concurrency:
            pr.measured = measured
    labels: list[Any] = []
    readings: list[Reading] = []
    dist_seen: list[bool] = []
    latency: list[float] = []
    # Scored against the task's labels as they are now (corrections and edits included), not the label a record
    # was written with; a case no longer in the task is left out.
    current = {c.id: c.label for c in cases}
    pr.never_asked = [cid for cid, label in current.items() if label is not None and cid not in asked]
    for r in recs:
        cid = r.id
        if cid not in current:
            continue
        label = current[cid]
        if label is None:
            pr.unlabeled += 1
            continue
        if (a := r.given) is None:
            if r.outcome in records.REFUSED:
                pr.refused_cases.append(cid)
            elif r.outcome == "failed":
                pr.failed_cases.append(cid)
            continue
        avg = kind.average([a])
        readings.append(kind.reading(avg, PLAIN))
        dist_seen.append(avg.distributed)
        labels.append(label)
        pr.ids.append(cid)
        latency.append(np.nan if r.latency_ms is None else float(r.latency_ms))
    pr.pairs = measure.pairs(kind, labels, readings)
    pr.case_latency_ms = np.array(latency, dtype=float)
    recorded_distributions = {r.distribution for r in ok}
    declared = recorded_distributions - {None}
    genuine = bool(dist_seen) and all(dist_seen) and None not in recorded_distributions and declared <= {"native", "sampled"}
    pr.probabilities = genuine
    if ok:
        if genuine and declared:
            pr.distribution = next(iter(declared)) if len(declared) == 1 else "mixed"
        else:
            pr.distribution = "none"
    return pr


# ---------- primitives ----------


def labels_needed(correct: int, n: int, coverage: float, target: float) -> int | None:
    """Labels still needed (at the current error rate and coverage) before cp_lower reaches the target."""
    if n == 0 or coverage == 0:
        return None
    err = 1 - correct / n
    if err >= 1 - target:
        return None
    if cp_lower(correct, n) >= target:
        return 0
    N = n
    while N < 1_000_000:
        N = int(N * 1.1) + 1
        if cp_lower(N - round(err * N), N) >= target:
            break
    else:
        return None
    lo, hi = n, N  # binary search the smallest N
    while lo < hi:
        mid = (lo + hi) // 2
        if cp_lower(mid - round(err * mid), mid) >= target:
            hi = mid
        else:
            lo = mid + 1
    return int(np.ceil((lo - n) / coverage))


def ece(conf: np.ndarray, correct: np.ndarray, bins: int = 10) -> float:
    edges = np.linspace(0, 1, bins + 1)
    total = 0.0
    for i in range(bins):
        m = (conf > edges[i]) & (conf <= edges[i + 1]) if i else (conf >= 0) & (conf <= edges[1])
        if m.any():
            total += m.mean() * abs(conf[m].mean() - correct[m].mean())
    return float(total)


def _better(b: Bound, v: float | None, than: float | None) -> bool:
    if v is None:
        return False
    return than is None or (v > than if b.objective.maximize else v < than)


def search(b: Bound, p: Pairs, grid: np.ndarray = GRID, floors: Sequence[Constraint] = ()) -> float:
    """The rule field the objective sets (`objective.sets`), chosen on these cases: inf when no value keeps
    its constraint and the `floors` (read at inf, nothing is answered)."""
    at = b.objective.sets
    assert at is not None  # only an objective that sets a rule field is searched
    keeps = [c for c in (b.constraint, *floors) if c is not None]
    if not keeps:
        values = [b.value(p.at(**{at: t})) for t in grid]
        known = [v for v in values if v is not None]
        best = (max(known) if b.objective.maximize else min(known)) if known else None
        ties = [t for t, v in zip(grid, values) if v == best]
        return float(min(ties, key=lambda t: abs(t - 0.5)))
    cut, value = np.inf, None
    for t in np.unique(p.reads(at)):  # ascending: a tie keeps the lower
        q = p.at(**{at: t})
        if any(c.holds(*c.count(q)) is False for c in keeps):
            continue
        v = b.value(q)
        if cut == np.inf or _better(b, v, value):
            cut, value = float(t), v
    return float(cut)


SWEEP = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]  # the miss / false-alarm table's thresholds, the chosen one added


def sweep(y: np.ndarray, p: np.ndarray, thresholds: list[float]) -> list[SweepRow]:
    """nod's table: a positive whose P(positive) is below t is a miss, a negative at or above t a false alarm."""
    pos, neg = p[y], p[~y]
    return [
        SweepRow(threshold=t, misses=int((pos < t).sum()), positives=int(pos.size), false_alarms=int((neg >= t).sum()), negatives=int(neg.size))
        for t in thresholds
    ]


def _strata(y: np.ndarray) -> np.ndarray:
    """The folds keep the label's shares (an option, a level); labels that are not one value each (a box) are not
    stratified, so every model gets the same folds."""
    if y.dtype == object and not all(isinstance(v, (str, int)) and not isinstance(v, bool) for v in y):
        return np.zeros(len(y), dtype=int).astype(str)
    return y.astype(str)


# ---------- the whole picture for one candidate ----------


@dataclass
class _Read:
    """One objective, read out of fold: the cases read at the rule each fold chose on its fit side."""

    bound: Bound
    pairs: Pairs  # every case; the dev ones at their fold's rule
    cuts: list[float]  # per fold
    dev: float | None  # chosen on all the dev cases (inf: none keeps the constraint); None: it sets nothing


def _read(b: Bound, p: Pairs, plan: splitting.Plan, folds: list[tuple[np.ndarray, np.ndarray]], floors: Sequence[Constraint] = ()) -> _Read:
    """The objective read out of fold (`search` on each fold's fit side, `floors` kept), and its rule chosen on all the dev cases."""
    at = b.objective.sets
    if at is None:
        return _Read(b, p, [], None)
    grid = SMALL_GRID if len(plan.dev) < splitting.SMALL else GRID
    cut = np.full(len(p), np.nan)
    cuts = []
    for fit, ev in folds:
        cuts.append(search(b, p[fit], grid, floors))
        cut[ev] = cuts[-1]
    return _Read(b, p.at(**{at: cut}), cuts, search(b, p[plan.dev], grid, floors))


def _resamples(n: int, dev: np.ndarray, seed: int) -> tuple[list[np.ndarray], list[np.ndarray]]:
    """One bootstrap over the cases, BOOTSTRAP draws: each a resample of all n (the plain numbers) and one of the
    dev cases `dev` (the objectives, and the calls' latency)."""
    rng = np.random.default_rng(seed)
    whole, of_dev = [], []
    for _ in range(BOOTSTRAP):
        whole.append(rng.integers(0, n, n))
        of_dev.append(rng.choice(dev, len(dev)))
    return whole, of_dev


def _intervals(bounds: Sequence[Bound], p: Pairs, resamples: list[np.ndarray]) -> list[tuple[float, float] | None]:
    """Each measure's 95% interval over these resamples of the cases `p` (a heavy one's over the first HEAVY);
    the measures read on the same cases share each resample."""
    draws: list[list[float]] = [[] for _ in bounds]
    for i, idx in enumerate(resamples):
        q = p[idx]
        for b, d in zip(bounds, draws):
            if (not b.heavy or i < HEAVY) and (v := b.value(q)) is not None:
                d.append(v)
    return [measure.interval(d) for d in draws]


def _score(r: _Read, dev: np.ndarray, interval: tuple[float, float] | None) -> ObjectiveScore:
    """The objective on the dev cases `dev`, each read at its fold's rule, with the rule chosen on all of them."""
    on = r.pairs[dev]
    o, chosen = r.bound.objective, None if r.dev is None else finite(r.dev)
    return ObjectiveScore(
        objective=o, value=r.bound.value(on), interval=interval,
        rule=None if o.sets is None or chosen is None else DecisionRule.model_validate({o.sets: min(1.0, chosen)}),
        constraint=r.bound.constraint.rate(on) if r.bound.constraint else None,
    )


def evaluate(task: Task, pr: Preds, target: float | None = None, variant: str = "base", *, include_test: bool = False) -> Evaluation:
    """`target` overrides the accuracy the first selective answer keeps (default: the task's)."""
    target = target or task.coverage_target
    kind = task.kind
    p0 = pr.pairs
    n = len(p0)
    sf = evalset.current(task)
    plan = splitting.plan(n, np.flatnonzero([sf.assign.get(i) == "test" for i in pr.ids]))
    dev = plan.dev
    base = dict(
        candidate=Candidate(model=pr.model, variant=variant), answered_by=pr.version, answered_by_all=pr.versions, n=len(dev),
        answered_ids=sorted(pr.ids[i] for i in dev),
        probabilities=pr.probabilities,
        failures=Failures(calls=pr.calls, failed=pr.failed, unsupported=pr.unsupported, data_errors=pr.data_errors, unlabeled=pr.unlabeled,
                          never_asked=len(pr.never_asked), failed_cases=len(pr.failed_cases), refused_cases=len(pr.refused_cases)),
    )
    if len(dev) < 2:
        return Evaluation(**base)  # type: ignore[arg-type]
    folds = list(splitting.folds(plan, _strata(p0.y), task.split))
    seen = np.zeros(n, dtype=bool)
    for _, ev in folds:
        seen[ev] = True
    idx_m = np.flatnonzero(seen)
    custom = task.custom_measures

    # the primary, read with the task's floors on the threshold it sets, the one a policy reads with (Task checks it
    # sets one); Coverage at each target the report shows; the error losses' cut, the report's table, read apart
    floors = measure.floors(task.constraints)
    primary = _read(bound(task.primary, kind, custom), p0, plan, folds, floors)
    targets = list(dict.fromkeys([target] + [cast(float, o.params["target_accuracy"]) for o in task.objectives if o.name == "coverage"]))
    covered = [primary if Coverage(t).key == task.primary.key else _read(bound(Coverage(t), kind, custom), p0, plan, folds) for t in targets]
    tuned = _read(bound(ExpectedLoss(*task.error_losses), kind), p0, plan, folds) if "threshold" in kind.sets else None
    # `tiebreak` is measured at the primary's rule, the one a policy reads with: it chooses none of its own
    later = [_Read(bound(o, kind, custom), primary.pairs, [], None) for o in task.objectives[1:]]

    # Every ordinary number and its interval uses the same dev population.
    _, of_dev = _resamples(n, idx_m, task.split.seed)
    accuracy, auroc = bound(Accuracy(), kind), bound(AUROC(), kind)
    acc_i, au_i = _intervals([accuracy, auroc], p0, of_dev)
    primary_i, *later_i = _intervals([primary.bound, *(r.bound for r in later)], primary.pairs, of_dev)
    covered_i = [primary_i if r is primary else _intervals([r.bound], r.pairs, of_dev)[0] for r in covered]

    selective = []
    for t, r, interval in zip(targets, covered, covered_i):
        sc = _score(r, idx_m, interval)
        assert r.bound.constraint is not None and r.dev is not None
        a_ok, a_n = r.bound.constraint.count(r.pairs[idx_m])
        cov = sc.value or 0.0
        selective.append(Selective(
            target_accuracy=t, coverage=Estimate(value=sc.value, interval=sc.interval), accuracy=a_ok / a_n if a_n else None,
            n=a_n, errors=a_n - a_ok, lower=cp_lower(a_ok, a_n), labels_needed=labels_needed(a_ok, a_n, cov, t), min_probability=finite(r.dev),
        ))

    threshold = None
    if tuned is not None:
        assert tuned.dev is not None
        on = tuned.pairs[idx_m]
        threshold = ErrorLossThreshold(
            accuracy=float(on.correct.mean()), misses=int((on.y & ~on.said).sum()), false_alarms=int((~on.y & on.said).sum()),
            median=float(np.median(tuned.cuts)), chosen=tuned.dev,
        )

    test = None
    if include_test and len(plan.test):
        te = plan.test
        held = p0[te]
        sure = held.at(min_probability=covered[0].dev).sure
        on_test, counts = _on_test(primary, te, task.split.seed + 1)
        test = TestResult(
            n=len(te), accuracy=float(held.correct.mean()), coverage=float(sure.mean()),
            sure_accuracy=float(held.correct[sure].mean()) if sure.any() else None,
            tuned_accuracy=float(held.at(threshold=threshold.chosen).correct.mean()) if threshold else None,
            primary=on_test, constraint=counts,
        )

    floor_rows = []
    if floors:
        at_test = None if test is None or primary.dev is None or primary.dev == np.inf else primary.pairs.at(threshold=primary.dev)[plan.test]
        floor_rows = [Floor(what=c.what, bound=c.bound, rate=c.rate(primary.pairs[idx_m]), test=None if at_test is None else c.count(at_test))
                      for c in floors]

    reported = {name: measure.measure(name, p0[dev]) for name in kind.report}
    conf, correct = p0.probability, p0.correct
    high = [
        HighConfidenceError(id=pr.ids[i], label=label, predicted=said, probability=float(conf[i]))
        for i in dev[np.argsort(-conf[dev])]
        if conf[i] >= HIGH_CONF and not correct[i]
        for label, said in [measure.shown(p0, int(i))]
    ]
    return Evaluation(
        **base,  # type: ignore[arg-type]
        split=splitting.describe(plan), split_method=str(plan.method),
        accuracy=Estimate(value=accuracy.value(p0[dev]), interval=acc_i), measures={k: Estimate(value=v) for k, v in reported.items()},
        auroc=Estimate(value=auroc.value(p0[dev]), interval=au_i),
        brier=measure.measure("brier", p0[dev]), ece=ece(conf[dev], correct[dev]),
        selective=selective, error_loss_threshold=threshold, floors=floor_rows,
        sweep=sweep(p0.y[dev], p0.p_positive[dev], sorted({*SWEEP, threshold.chosen})) if threshold else None,
        objective=_score(primary, idx_m, primary_i), tiebreak=[_score(r, idx_m, i) for r, i in zip(later, later_i)],
        test=test, high_confidence_errors=high, calls=calls(pr, idx_m, of_dev),
    )


def calls(pr: Preds, dev: np.ndarray, resamples: list[np.ndarray]) -> Calls:
    """What the calls took, from their records alone, apart from the answers: the latency of each call, the p90 over
    the dev cases `dev` of each one's slowest call (its interval over the evaluation's `resamples` of them, the
    ones that give the objectives theirs), the throughput and the API cost."""
    n = len(pr.pairs)
    lat = pr.case_latency_ms if len(pr.case_latency_ms) == n else np.full(n, np.nan)  # Preds made by hand: not recorded
    p90 = _percentile(lat[dev], 90)
    timing = pr
    spend = pr.spend
    if pr.call_ids:
        allowed = {pr.ids[i] for i in dev}
        indices = [i for i, cid in enumerate(pr.call_ids) if cid in allowed]
        spend = cost.Spend()
        for i in indices:
            spend.add(*pr.call_costs[i])
        timing = replace(pr, latency_ms=pr.latency_ms[indices], retries=[pr.retries[i] for i in indices],
                         concurrency=[pr.concurrency[i] for i in indices], input_tokens=pr.input_tokens[indices],
                         measured=pr.measured if len(indices) == len(pr.call_ids) else None)
    costs = np.array(spend.costs)
    return Calls(
        latency=latency(timing), throughput=_throughput(timing),
        case_latency_p90_ms=None if p90 is None else Estimate(
            value=p90, interval=measure.interval([v for bm in resamples if (v := _percentile(lat[bm], 90)) is not None])),
        cost_per_10k_usd=float(costs.mean() * 10_000) if costs.size else None, cost_total_usd=float(costs.sum()) if costs.size else None,
        cost_source=spend.source, cost_unknown=spend.unknown, price=pr.price,
    )


def _on_test(r: _Read, te: np.ndarray, seed: int) -> tuple[Estimate, tuple[int, int] | None]:
    """The primary objective on the test share, at the rule chosen on the rest, with a bootstrap interval,
    and the share its constraint keeps there."""
    b, at = r.bound, r.bound.objective.sets
    if r.dev is None or at is None:
        q = r.pairs
    elif r.dev == np.inf and at == "threshold":
        return Estimate(value=None), None  # no P(positive) cut keeps the constraint: no policy to read the test share with
    else:
        q = r.pairs.at(**{at: r.dev})  # a min probability none keeps: every case unsure
    rng = np.random.default_rng(seed)
    draws = [v for _ in range(TEST_BOOTSTRAP) if (v := b.value(q[rng.choice(te, len(te))])) is not None]
    return Estimate(value=b.value(q[te]), interval=measure.interval(draws)), b.constraint.count(q[te]) if b.constraint else None


def test_verdict(task: Task, e: Evaluation) -> TestVerdict | None:
    """The held-out share's verdict (`_verdict`), `below` too when it shows one of the task's floors broken, and
    `kept` only when its point values keep them all."""
    verdict = _verdict(task, e)
    if verdict is None or not e.floors:
        return verdict
    pairs = list(zip(measure.floors(task.constraints), e.floors))
    if any(f.test is not None and c.broken(*f.test) for c, f in pairs):
        return "below"
    if verdict == "kept" and not all(f.test is not None and c.holds(*f.test) for c, f in pairs):  # nothing read positive: not kept
        return "inconclusive"
    return verdict


def _verdict(task: Task, e: Evaluation) -> TestVerdict | None:
    """The held-out share's verdict on the primary objective.

    With a constraint: `below` when the test share shows it broken (one-sided 95% Clopper-Pearson),
    `kept` when its point value keeps it. Without: `below` when the test interval lies wholly on the
    worse side of the interval measured on the rest, `kept` when the test value reaches that interval.
    Otherwise `inconclusive`.
    """
    t = e.test
    if t is None:
        return None
    b = bound(task.primary, task.kind, task.custom_measures)
    if b.constraint is not None:
        if t.constraint is None:
            return "inconclusive"
        if b.constraint.broken(*t.constraint):
            return "below"
        return "kept" if b.constraint.holds(*t.constraint) else "inconclusive"
    rest, held = e.objective, t.primary
    assert rest is not None
    if held.value is None or rest.interval is None:
        return "inconclusive"
    lo, hi = rest.interval
    if b.objective.maximize:
        if held.interval and held.interval[1] < lo:
            return "below"
        return "kept" if held.value >= lo else "inconclusive"
    if held.interval and held.interval[0] > hi:
        return "below"
    return "kept" if held.value <= hi else "inconclusive"


def _percentile(ms: np.ndarray, at: float) -> float | None:
    """The latency at percentile `at` of these cases, each its slowest answered call; None when none was recorded."""
    known = ms[~np.isnan(ms)]
    return float(np.percentile(known, at)) if known.size else None


def latency(pr: Preds) -> Latency | None:
    """Per answered call: the answering attempt alone (retries left out). The tail (p99, max) and the
    spread are what decide whether a model fits a time budget."""
    ms = pr.latency_ms
    if not ms.size or not np.isfinite(ms).all():
        return None
    q = {k: float(np.percentile(ms, k)) for k in (50, 90, 95, 99)}
    known = [c for c in pr.concurrency if c is not None]
    return Latency(
        n=int(ms.size), p50_ms=q[50], p90_ms=q[90], p95_ms=q[95], p99_ms=q[99], max_ms=float(ms.max()),
        spread=q[99] / q[50] if q[50] > 0 else None, retried=sum(1 for r in pr.retries if r),
        unrecorded=sum(1 for r in pr.retries if r is None), concurrency=sorted(set(known)),
        concurrency_unknown=len(pr.concurrency) - len(known),
    )


def _throughput(pr: Preds) -> Throughput | None:
    """Calls per minute: measured when a run made all its calls, else latency summed over the
    concurrency the calls were made at (the most common one recorded; none recorded, no estimate)."""
    if pr.measured and pr.measured.get("seconds"):
        mm = pr.measured
        return Throughput(per_min=mm["calls"] / max(mm["seconds"], 1) * 60, seconds=mm["seconds"], calls=mm["calls"], concurrency=mm["concurrency"], measured=True)
    if not pr.latency_ms.size or not np.isfinite(pr.latency_ms).all():
        return None
    known = [c for c in pr.concurrency if c is not None]
    if not known:  # calls saved before the concurrency was recorded: no basis for an estimate
        return None
    c = max(set(known), key=known.count)
    seconds = float(pr.latency_ms.sum()) / 1000 / c
    return Throughput(per_min=pr.latency_ms.size / max(seconds, 1e-9) * 60, seconds=seconds, calls=int(pr.latency_ms.size), concurrency=c, measured=False)


def chart_data(task: Task, pr: Preds, evaluation: Evaluation) -> ChartData:
    """Compute charts with the same dev population and shared reading/scoring code.

    The raw threshold sweep is exploratory; only cv_value is the out-of-fold
    estimate of the selected rule. JavaScript renders these values unchanged.
    """
    sf = evalset.current(task)
    dev = np.array([i for i, cid in enumerate(pr.ids) if sf.assign.get(cid) != "test"], dtype=int)
    pairs = pr.pairs[dev]
    objective = bound(task.primary, task.kind, task.custom_measures)
    raw_value = objective.value(pairs) if len(dev) else None
    cv_value = None if evaluation.objective is None else evaluation.objective.value

    # Selection is meaningful for all question kinds that returned a genuine
    # distribution/confidence.  Build it before the binary-only charts return
    # below so Choice and Box comparisons retain their useful curve too.
    selection_basis: Literal["selected-answer probability", "box confidence"] = "box confidence" if task.kind.type == "box" else "selected-answer probability"
    selected = None
    if evaluation.objective is not None and evaluation.objective.rule is not None:
        selected = evaluation.objective.rule.min_probability
    # A Boolean (including a positive Choice) has two independent controls:
    # the final selected P(positive) threshold and the acceptance probability
    # cut.  The curve must keep the former fixed while varying the latter.
    selection_pairs = pairs
    selection_threshold = 0.5
    if task.kind.binary:
        if evaluation.objective is not None and evaluation.objective.rule is not None and evaluation.objective.rule.threshold is not None:
            selection_threshold = evaluation.objective.rule.threshold
        selection_pairs = pairs.at(threshold=selection_threshold)
    if not len(dev):
        selection_unavailable = "Selection requires answered dev cases with a distribution or box confidence."
        selection: list[SelectionPoint] = []
    elif not pr.probabilities:
        selection_unavailable = "Selection probability is unavailable: the answered dev cases have no genuine distribution or box confidence."
        selection = []
    else:
        selection_unavailable = None
        thresholds = sorted({float(t) for t in np.linspace(0, 1, 101)} | ({float(selected)} if selected is not None else set()))
        selection = []
        for threshold in thresholds:
            accepted_mask = selection_pairs.ok & (selection_pairs.probability >= threshold)
            accepted = int(accepted_mask.sum())
            correct = int((accepted_mask & selection_pairs.correct).sum())
            selection.append(SelectionPoint(
                min_probability=float(threshold),
                coverage=accepted / len(pairs),
                sure_accuracy=correct / accepted if accepted else None,
                accepted=accepted,
                correct=correct,
                total=len(pairs),
            ))

    if not task.kind.binary or not pr.probabilities or not len(dev):
        return ChartData(
            n=len(dev), raw_value=raw_value, cv_value=cv_value,
            selection_sweep=selection, selection_basis=selection_basis,
            selection_unavailable=selection_unavailable,
            unavailable="Binary diagnostics require answered dev cases with a distribution." if task.kind.binary else None,
        )
    threshold_points = []
    chosen = evaluation.objective.rule.threshold if evaluation.objective and evaluation.objective.rule else None
    thresholds = sorted({float(t) for t in np.linspace(0, 1, 101)} | ({chosen} if chosen is not None else set()))
    for threshold in thresholds:
        p = pairs.at(threshold=float(threshold))
        threshold_points.append(ThresholdPoint(threshold=float(threshold), objective=objective.value(p),
                                             precision=_share(*measure.FLOOR_COUNTS["precision"](p)), recall=_share(*measure.FLOOR_COUNTS["recall"](p)),
                                             misses=int((p.y & ~p.said).sum()), false_alarms=int((~p.y & p.said).sum())))
    distribution = []
    calibration = []
    probability = pairs.p_positive
    for index in range(20):
        lower, upper = index / 20, (index + 1) / 20
        mask = (probability >= lower) & ((probability < upper) if index < 19 else (probability <= upper))
        distribution.append(ProbabilityBin(lower=lower, upper=upper, positives=int(pairs.y[mask].sum()),
                                           negatives=int((~pairs.y[mask]).sum())))
    for index in range(10):
        mask = np.minimum(9, (probability * 10).astype(int)) == index
        n = int(mask.sum())
        if n >= 5:
            calibration.append(CalibrationPoint(probability=float(probability[mask].mean()), observed=float(pairs.y[mask].mean()), n=n))
    return ChartData(
        n=len(dev), raw_value=raw_value, cv_value=cv_value,
        threshold_sweep=threshold_points, distribution=distribution, calibration=calibration,
        selection_sweep=selection, selection_basis=selection_basis,
        selection_unavailable=selection_unavailable,
    )


def _share(numerator: int, denominator: int) -> float | None:
    return numerator / denominator if denominator else None
