"""Choosing among candidates by the task's objectives and constraints.

Objectives are never summed with weights (there is no basis for the weights): a candidate is
chosen on the objective among those that meet the constraints, and only candidates whose
intervals overlap the best are compared on `tiebreak`'s objectives, in its order.

What the calls took (Evaluation.calls) is used in two places only, both here: the constraints on
latency and API cost, and the fixed order after `tiebreak` among the still tied, latency (p90 per
case) and then API cost per 10,000 cases (unknown last). Latency orders candidates only when they
were all measured alike: at one concurrency, with their retries recorded (a call saved before
2026-10-16 may include the backoff). Otherwise it is skipped and `unlike` says why;
`s1flow run --fresh --concurrency N` with one N for every candidate measures them again.
Candidates whose latency intervals overlap the fastest's are not told apart by it.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel, Field

from .evaluation import Estimate, Evaluation, ObjectiveScore
from .objectives.declare import Constraints, Objective
from .shown import pct, usd


class Ranked(BaseModel):
    candidate: str  # Candidate.name
    scores: list[ObjectiveScore]  # one per objective, in the task's order
    excluded: list[str] = Field(default_factory=list)  # constraints it breaks, in words
    tied_with_best: bool = False


def violations(c: Constraints, e: Evaluation) -> list[str]:
    out = []
    p99, cost = (e.calls.latency.p99_ms if e.calls.latency else None), e.calls.cost_per_10k_usd
    if c.latency_p99_ms is not None:
        if p99 is None:
            out.append("p99 latency unknown; constraint cannot be verified")
        elif p99 > c.latency_p99_ms:
            out.append(f"p99 {p99:.0f}ms > {c.latency_p99_ms:.0f}ms")
    if c.cost_per_10k_usd is not None:
        if cost is None or e.calls.cost_unknown:
            out.append("API cost unknown for some calls; constraint cannot be verified")
        elif cost > c.cost_per_10k_usd:
            out.append(f"API cost {usd(cost, 2)} per 10k > {usd(c.cost_per_10k_usd, 2)}")
    if c.min_labels is not None and e.n < c.min_labels:
        out.append(f"{e.n} labels < {c.min_labels}")
    if c.floors and e.objective is not None and e.objective.rule is None:
        out.append("no threshold keeps " + " and ".join(f"{k} ≥ {pct(v)}" for k, v in c.floors.items()) + " on the dev cases")
    return out


def _overlaps(o: Objective, best: ObjectiveScore, other: ObjectiveScore) -> bool:
    """Conservative interval-overlap grouping heuristic, not an equivalence test."""
    if best.interval is None or other.interval is None:
        return best.value == other.value
    lo, hi = best.interval
    olo, ohi = other.interval
    return ohi >= lo if o.maximize else olo <= hi


@dataclass(frozen=True)
class Unlike:
    """Why the candidates' latencies cannot be compared."""

    concurrencies: list[int]  # every concurrency they were measured at
    unknown: list[str]  # candidates with calls whose concurrency was not recorded (or no latency at all)
    unrecorded: list[str]  # candidates with calls saved before retries were recorded

    def en(self, task: str) -> str:
        why = [f"concurrency {', '.join(map(str, self.concurrencies))}"] if len(self.concurrencies) > 1 else []
        why += [f"{len(self.unknown)} with no concurrency recorded"] if self.unknown else []
        why += [f"{len(self.unrecorded)} with no retries recorded"] if self.unrecorded else []
        return (f"latency not compared ({'; '.join(why)}): measure every candidate again at one concurrency, "
                f"s1flow run {task} --fresh --concurrency N (the same N for all)")


def unlike(evaluations: list[Evaluation]) -> Unlike | None:
    """None when the latencies of these candidates can be compared (or there is one); else why not."""
    if len(evaluations) < 2:
        return None
    seen: set[int] = set()
    unknown, unrecorded = [], []
    for e in evaluations:
        lat, name = e.calls.latency, e.candidate.name
        if lat is None or lat.concurrency_unknown:
            unknown.append(name)
        if lat is not None:
            seen |= set(lat.concurrency)
            if lat.unrecorded:
                unrecorded.append(name)
    if len(seen) <= 1 and not unknown and not unrecorded:
        return None
    return Unlike(sorted(seen), unknown, unrecorded)


def _latency(group: list[Evaluation]) -> dict[str, float]:
    """Each candidate's place on latency within `group`: 0 for the fastest and those whose intervals overlap it,
    else its value (inf: not measured); 0 for all when they were not measured alike."""
    if unlike(group) is not None:
        return {e.candidate.name: 0.0 for e in group}
    of = {e.candidate.name: e.calls.case_latency_p90_ms or Estimate(value=None) for e in group}
    known = [s for s in of.values() if s.value is not None]
    if not known:
        return {n: 0.0 for n in of}
    best = min(known, key=lambda s: s.value or 0.0)

    def overlaps(s: Estimate) -> bool:
        if best.interval is None or s.interval is None:
            return s.value == best.value
        return s.interval[0] <= best.interval[1]

    return {n: float("inf") if s.value is None else 0.0 if overlaps(s) else s.value for n, s in of.items()}


def rank(objective: Objective, then: list[Objective], constraints: Constraints, evaluations: list[Evaluation]) -> list[Ranked]:
    """Every scored candidate, best first: those within the constraints, then the excluded ones.
    `tied_with_best` marks the candidates the objective cannot tell from the best; `tiebreak`, then latency and
    API cost order them."""
    scored = [e for e in evaluations if e.n and e.objective is not None]
    ranked = [Ranked(candidate=e.candidate.name, scores=e.scores, excluded=violations(constraints, e)) for e in scored]
    populations = {tuple(sorted(e.answered_ids)) for e in scored}
    for item, e in zip(ranked, scored):
        if not e.answered_ids:
            item.excluded.append("answered population unverified")
        elif len(populations) > 1:
            item.excluded.append("different answered dev cases; automatic comparison refused")
    by = {e.candidate.name: e for e in scored}

    def by_value(o: Objective, s: ObjectiveScore) -> float:
        return float("inf") if s.value is None else (-s.value if o.maximize else s.value)

    def values(group: list[Ranked]) -> dict[str, list[float]]:
        """Each candidate's keys within `group`: `tiebreak`'s objectives in its order, then its place on latency
        among the group, then its API cost."""
        placed = _latency([by[x.candidate] for x in group])
        out: dict[str, list[float]] = {}
        for x in group:
            cost = by[x.candidate].calls.cost_per_10k_usd
            out[x.candidate] = [*(by_value(t, next(s for s in x.scores if s.objective.key == t.key)) for t in then),
                           placed[x.candidate], float("inf") if cost is None else cost]
        return out

    every = values(ranked)

    def key(i: int) -> tuple[Any, ...]:
        """Sorts ascending: excluded last; then the objective and each of `tiebreak`, best first."""
        x = ranked[i]
        return (bool(x.excluded), by_value(objective, x.scores[0]), *every[x.candidate])

    order = sorted(range(len(ranked)), key=key)
    ranked = [ranked[i] for i in order]
    fits = [x for x in ranked if not x.excluded and x.scores[0].value is not None]
    if not fits:
        return ranked
    top = fits[0]
    tied = [x for x in fits if x is top or _overlaps(objective, top.scores[0], x.scores[0])]
    among = values(tied)

    # Interval overlap groups these conservatively; this is not evidence of equivalence.
    def tie_key(x: Ranked) -> tuple[Any, ...]:
        return (*among[x.candidate], by_value(objective, x.scores[0]))

    tied_sorted = sorted(tied, key=tie_key)
    for x in tied_sorted:
        x.tied_with_best = True
    return tied_sorted + [x for x in ranked if x not in tied_sorted]


def unlike_among_tied(ranked: list[Ranked], evaluations: list[Evaluation]) -> Unlike | None:
    """Why latency did not order the tied candidates: they were not measured alike."""
    by = {e.candidate.name: e for e in evaluations}
    return unlike([by[x.candidate] for x in ranked if x.tied_with_best])
