"""The fixed evaluation set and `check` (no network)."""

import json
import math

import pytest
from conftest import attach, cli, labelled, make_project, point

from s1flow.core.errors import ConfigError, DataError, NotFound, ProviderError, S1flowError
from s1flow.eval.candidate import Candidate
from s1flow.eval.evaluation import Evaluation, Failures
from s1flow.client.identity import execution_digest
from s1flow.objectives import Constraints, Coverage, Recall
from s1flow.policies import DecisionPolicy, DecisionRule, PolicySpec
from s1flow.eval.policy import EvaluatedPolicy, Evidence, Selection
from s1flow.policies.file import asked
from s1flow.policies.state_shape import schema_of
from s1flow.client import Choice, ChoiceAnswer, Response, ModelBuild, ModelSpec, Usage
from s1flow.client.models import Price
from s1flow.eval import Task, check, evalset
from s1flow.eval.check import calls, comment
from s1flow.eval.task import Optimized, Split
from s1flow.policies.kinds import KindParams

CLASSES = ["a", "b", "c"]
QUESTION = Choice(instructions="Which?", criteria={c: None for c in CLASSES})


class Fake:
    """`good` answers the label, `bad` the next class, `unsure` the label at a low probability."""

    def __init__(self, b: ModelBuild):
        self.id, self.kind, self.capabilities, self.concurrency = f"fake:{b.spec.id}", b.spec.id, b.spec.capabilities, 4

    async def decide(self, state, questions, *, options=None):
        q = next(iter(questions))
        truth = state["text"]
        pick = CLASSES[(CLASSES.index(truth) + 1) % 3] if self.kind == "bad" else truth
        top = 0.6 if self.kind == "below_min_probability" else 0.97
        probs = {c: top if c == pick else (1 - top) / 2 for c in CLASSES}
        usage = Usage(input_tokens=100) if self.kind == "tokens" else Usage(cost_usd=0.0001)  # tokens: a model that bills nothing back
        return Response(answers={q: ChoiceAnswer(choice=pick, probabilities=probs)}, answered_by=self.id, usage=usage, latency_ms=100.0)


def fake(b: ModelBuild) -> Fake:
    return Fake(b)


@pytest.fixture
def task(tmp_path, no_ci):
    p = make_project(tmp_path)
    rows = [{"id": str(i), "text": CLASSES[i % 3]} for i in range(120)]
    (tmp_path / "data.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    return attach(Task(id="toy", cases="data.jsonl", dir=tmp_path, state=lambda r: {"text": r["text"]}, question=QUESTION,
                       label=lambda r: r["text"], objective=Coverage(target_accuracy=0.9)), p)


def policy(version: int, model: str, question=QUESTION) -> EvaluatedPolicy:
    e = Evaluation(candidate=Candidate(model=model), answered_by=model, answered_by_all=[model], n=120, probabilities=True,
                   failures=Failures(calls=120, failed=0, unsupported=0, data_errors=0, unlabeled=0))
    return EvaluatedPolicy(
        spec=PolicySpec(task="toy", version=version, connection=model, model_id=model,
                        questions={"q": asked(question, DecisionRule(min_probability=0.9))}, state_schema=schema_of([{"text": "a"}])),
        candidate=Candidate(model=model), answered_by=model,
        selection=Selection(by="t", reason="t", tied=[model]),
        evidence=Evidence(data_sha256="0", execution_digest=None, evaluation=e, test=None, compared=[model]),
    )


def ship(task: Task, *rs: EvaluatedPolicy, current: int = 1, candidate: int | None = None) -> None:
    """`current` the version the base branch ships; `candidate` the one a pull request made current (check it
    --against v{current})."""
    store = task.policies
    # Connections are explicitly owned by this application, never embedded in a policy.
    make_project(task.where.root, {r.spec.connection: fake for r in rs})
    for r in rs:
        runtime = DecisionPolicy(r.spec, client=task.where.client())
        r.evidence.execution_digest = runtime.execution_digest
        r.evidence.input_adapter_digest = task.input_adapter_digest
        r.evidence.evaluation_contract_digest = task.evaluation_contract_digest
        r.evidence.data_sha256 = task.data_digest
        store.write_new(r)
    point(store, "toy", candidate or current)
    evalset.fix(task)  # the task's first run fixed the held-out test share


def test_the_split_is_made_once_and_never_moves(task, tmp_path):
    with pytest.raises(DataError, match="the first `s1flow run toy` fixes the held-out test share"):
        evalset.fixed(task)  # adopt, check and optimize refuse to draw one of their own
    planned = evalset.current(task)
    assert not evalset.path(task).exists()  # reading writes nothing
    assert "fixed the evaluation set" in (evalset.fix(task) or "") and evalset.fix(task) is None  # the first run writes it, once
    sf = evalset.fixed(task)
    assert sf.assign == planned.assign and set(sf.assign.values()) == {"train", "val", "test"} and 30 <= len(sf.ids("test")) <= 50
    assert sf.test_share == task.split.test  # later cases are held out at the task's share, whatever rounding made of the first
    written = evalset.path(task).read_text()
    with (tmp_path / "data.jsonl").open("a") as f:
        f.writelines(json.dumps({"id": f"n{i}", "text": "a"}) + "\n" for i in range(40))
    task.load_cases().forget()
    sf2 = evalset.current(task)
    assert {k: sf2.assign[k] for k in sf.assign} == sf.assign and all(f"n{i}" in sf2.assign for i in range(40))
    assert evalset.path(task).read_text() == written  # new cases are placed by their id's hash, never written
    assert 0 < sum(sf2.assign[f"n{i}"] == "test" for i in range(40)) < 40


def test_a_split_from_before_reads_without_its_uses(task):
    evalset.fix(task)
    old = json.loads(evalset.path(task).read_text())
    evalset.path(task).write_text(json.dumps({**old, "schema": "s1flow/split@1", "uses": [{"at": "t", "by": "check", "what": "v1"}]}))
    assert evalset.read(task).assign == old["assign"] and evalset.current(task).assign == evalset.current(task).assign


@pytest.mark.parametrize("labels", [list("aabbcc"), [c for c in "abcde" for _ in range(2)], list("aab")])
def test_a_small_task_still_gets_a_test_share(task, labels):
    labelled(task, labels)  # more labels than test cases, or one case of a label: drawn at random instead of stratified
    sp = evalset.initial(task, task.load_cases().labelled(), 1)
    assert len(sp["test"]) == math.ceil(0.3 * len(labels)) and len(sp["train"]) + len(sp["val"]) >= 2


def test_too_few_cases_for_a_test_share_is_a_data_error(task):
    labelled(task, ["a", "b"])
    with pytest.raises(DataError, match="needs 3 or more"):
        evalset.initial(task, task.load_cases().labelled(), 1)


@pytest.mark.parametrize("share", [None, "auto", 0, 1.0])
def test_a_test_share_outside_0_and_1_is_refused(share):
    with pytest.raises(ConfigError, match="between 0 and 1"):
        Split(test=share)


def test_the_split_starts_from_an_optimization_split(task):
    task.optimized = {"gepa-x": Optimized(
        variant="gepa-x", model="m", optimizer="gepa", settings={}, at="2026-10-16T00:00:00Z", question=QUESTION, seed_question=QUESTION,
        split={"train": ["0", "1"], "val": ["2"], "test": ["3", "4"]}, model_calls=1, cost_usd=0.0,
    )}
    evalset.fix(task)
    sf = evalset.fixed(task)
    assert sf.source == "optimized/gepa-x" and {"3", "4"} <= set(sf.ids("test")) and sf.assign["0"] == "train"


def test_a_worse_candidate_fails(task):
    ship(task, policy(1, "good"), policy(2, "bad"), candidate=2)
    r = check.check(task, against="v1")
    assert (r.verdict, r.exit) == ("fail", 1) and [s.name for s in r.sides] == ["v1", "current"]
    assert r.sides[1].sure_accuracy == 0.0 and r.diff and r.diff.sure_accuracy.interval[1] < 0
    md = comment.markdown(task, r)
    assert md.startswith("<!-- s1flow-check:toy -->") and "❌ fail" in md


def test_a_more_cautious_candidate_is_worse_on_coverage(task):
    ship(task, policy(1, "good"), policy(2, "below_min_probability"), candidate=2)
    r = check.check(task, against="v1")
    assert r.exit == 1 and r.diff and r.diff.primary.diff == pytest.approx(-1.0)


def test_the_same_answers_pass_and_are_cached(task):
    ship(task, policy(1, "good"), policy(2, "good"), candidate=2)
    r = check.check(task, against="v1", sample=20)
    assert (r.verdict, r.exit, r.n) == ("no_difference", 0, 20)
    again = check.check(task, against="v1", sample=20)
    assert again.sides[0].calls == 0 and again.sides[0].cached == 20


def test_a_policy_is_asked_and_cached_under_runs_key(task):
    """check decides through policies.DecisionPolicy: each case is one call and one cache entry, under run's key."""
    ship(task, policy(1, "good"))
    first = check.check(task, sample=10)
    assert (first.sides[0].calls, first.sides[0].cached) == (3, 7)  # 3 distinct states; the rest are the same calls
    _, r = check.pick(task, "current")
    assert calls.missing(task, r, [task.load_cases().by_id()[i] for i in evalset.read(task).ids("test")][:10]) == 0
    again = check.check(task, sample=10, cached_only=True)
    assert (again.verdict, again.sides[0].calls, again.sides[0].cached) == (first.verdict, 0, 10)
    assert len(list((task.where.cache_dir / "answers").glob("*/*.json"))) == 3


def recall_task(task: Task) -> Task:
    """The same cases, scored as P("a") with false alarms held to 10% of the others."""
    t = Task(id="toy", cases="data.jsonl", dir=task.dir, state=lambda r: {"text": r["text"]}, question=QUESTION, kind_params=KindParams(positive="a"),
             label=lambda r: r["text"] == "a", objective=Recall(max_false_alarm=0.1))
    return attach(t, task.where)


def binary(version: int, model: str) -> EvaluatedPolicy:
    base = policy(version, model)
    return base.model_copy(update={"spec": base.spec.model_copy(update={"questions": {"q": asked(QUESTION, DecisionRule(threshold=0.5), KindParams(positive="a"))}})})


def test_recall_is_checked_on_its_false_alarms(task):
    """bad says "a" for every "c": half the negatives are false alarms."""
    t = recall_task(task)
    ship(t, binary(1, "good"), binary(2, "bad"), candidate=2)
    r = check.check(t, against="v1")
    assert r.verdict == "fail" and r.primary_label == "recall at 10% false alarms or fewer"
    assert "current: the false-alarm rate is above the cap 10% (one-sided 95%: its lower bound is over the cap)" in r.reasons
    assert "the false-alarm rate is higher than v1's (the difference's 95% interval is above 0)" in r.reasons


def test_a_floor_broken_on_the_check_cases_fails(task):
    """bad reads every "c" as "a": half of what it reads positive is not."""
    t = recall_task(task).copy(constraints=Constraints(min_precision=0.8))
    ship(t, binary(1, "bad"))
    r = check.check(t)
    assert r.exit == 1 and "current: the precision is below the floor 80% (one-sided 95%: its upper bound is under the target)" in r.reasons


def test_a_candidate_that_keeps_the_bound_is_better_than_one_that_breaks_it(task):
    t = recall_task(task)
    ship(t, binary(1, "bad"), binary(2, "good"), candidate=2)
    r = check.check(t, against="v1")
    assert r.verdict == "better" and not r.reasons
    assert any("on the test cases v1's false-alarm rate exceeds the cap 10%, so current, which keeps the cap even at a lower recall, counts as better" in n for n in r.notes)


def test_an_edited_question_is_checked_as_draft(task):
    ship(task, policy(1, "good", Choice(instructions="Old wording?", criteria={c: None for c in CLASSES})))
    r = check.check(task)
    assert [s.name for s in r.sides] == ["current", "draft"] and r.exit == 0


def test_current_alone_is_held_to_the_target(task):
    ship(task, policy(1, "bad"))
    r = check.check(task)
    assert len(r.sides) == 1 and r.exit == 1 and "the target" in r.reasons[0]


def test_no_policy_leaves_no_split(task):
    with pytest.raises(NotFound):
        check.check(task)
    assert not evalset.path(task).exists()


def test_without_keys_only_the_cache_answers(task):
    ship(task, policy(1, "good"), policy(2, "bad"), candidate=2)
    r = check.check(task, against="v1", cached_only=True)
    assert (r.verdict, r.exit) == ("pending", 2) and set(r.need_calls) == {"v1", "current"}
    assert "⏸ pending" in comment.markdown(task, r)
    check.check(task, against="v1")  # with keys: the answers are cached now
    assert check.check(task, against="v1", cached_only=True).verdict == "fail"


def test_init_makes_a_project(tmp_path):
    from importlib import metadata

    from s1flow.project import scaffold

    (tmp_path / ".git").mkdir()
    proj = tmp_path / "app"
    assert not any(".github" in x for x in scaffold.init(tmp_path / "bare"))  # the workflow only when asked
    done = scaffold.init(proj, "ticket-bug", 'Is it a "bug"?', workflow=True)
    assert (proj / "s1flow.toml").exists() and {".cache/", ".env"} <= set((proj / ".gitignore").read_text().split())
    wf = (tmp_path / ".github" / "workflows" / "s1flow-check.yml").read_text()
    assert '"app/tasks/**"' in wf and 'working-directory: "app"' in wf and "${{ secrets.OPENROUTER_API_KEY }}" in wf
    assert "push:" not in wf and "80 calls" in wf  # pull requests only, and what one costs
    assert f"gotalab/s1flow@v{metadata.version('s1flow')}" in wf  # the Action at the installed release, not main
    src = (proj / "tasks" / "ticket-bug" / "task.py").read_text()
    compile(src, "task.py", "exec")
    assert "id='ticket-bug'" in src and """instructions='Is it a "bug"?'""" in src and len(done) == 4
    assert not (tmp_path / ".claude").exists()  # the Skill is the CLI's to write (skill.py)
    assert all(x.startswith("kept") for x in scaffold.init(proj, "ticket-bug")[:1])


def test_an_adopted_version_wins_over_an_edit(task):
    ship(task, policy(1, "good", Choice(instructions="Old wording?", criteria={c: None for c in CLASSES})), policy(2, "good"), candidate=2)
    assert check.default_candidate(task, check.pick(task, "v1")[1]) == "current"  # the pull request adopted v2
    assert check.default_candidate(task, check.pick(task, "current")[1]) is None  # current, its question as shipped: itself


def test_a_forced_version_fails_like_any_below_and_says_why(task):
    forced = policy(2, "bad")
    forced.evidence.test = "below"
    forced.selection = Selection(by="ana", reason="the old model is retired on Friday", tied=["bad"], forced=True)
    ship(task, policy(1, "good"), forced, candidate=2)
    r = check.check(task, against="v1")
    assert r.verdict == "fail"  # what the evidence says, the pull request could have written: it is asked again
    assert "current (toy@v2) was adopted with --force although the held-out test showed it below, by ana: the old model is retired on Friday" in r.notes
    assert "the old model is retired on Friday" in comment.markdown(task, r)


def test_a_version_adopted_without_an_evaluation_is_checked_like_any_other(task):
    ship(task, policy(1, "good"), policy(2, "bad"), candidate=2)
    (task.policies.dir("toy") / "v2.evaluation.json").unlink()  # what adopt --spec writes: the spec alone
    r = check.check(task, against="v1")
    assert r.verdict == "fail" and r.sides[1].variant is None
    assert "current (toy@v2) was adopted without an evaluation (adopt --spec): this check is its first measurement" in r.notes
    with pytest.raises(S1flowError, match="adopted without an evaluation"):
        check.check(task, candidate="draft")


def test_every_call_failing_is_not_a_pass(task, monkeypatch):
    ship(task, policy(1, "good"))

    async def down(self, state, questions, *, options=None):
        raise ProviderError("503 from the model")

    monkeypatch.setattr(Fake, "decide", down)
    with pytest.raises(ProviderError, match="every call failed"):
        check.check(task)


def test_a_candidate_over_the_latency_budget_fails(task):
    ship(task, policy(1, "good"))
    task.constraints = Constraints(latency_p99_ms=50)  # the fake answers in 100ms
    r = check.check(task)
    assert r.exit == 1 and "p99" in r.reasons[0]


def test_a_cost_not_known_is_not_free_and_a_list_price_estimates_it(task):
    ship(task, policy(1, "tokens"))
    r = check.check(task, sample=20)
    assert r.sides[0].cost_per_10k_usd is None and r.sides[0].cost_unknown == 20
    assert "calls whose API cost is not known" in comment.markdown(task, r)
    priced = policy(2, "tokens")
    price = Price(input_per_mtok=1.0, as_of="2026-10-19", source="t")
    task.policies.write_new(priced)
    path = task.where.root / "s1flow.toml"
    path.write_text(path.read_text() + '\n[models.tokens.price]\ninput_per_mtok = 1.0\nas_of = "2026-10-19"\nsource = "t"\n')
    point(task.policies, "toy", 2)
    task.project = type(task.where)(task.where.root)  # reload the application-owned connection price
    r = check.check(task, sample=20)  # cached answers priced from the current binding
    s = r.sides[0]
    assert s.cached == 20 and s.cost_source == "list" and s.cost_per_10k_usd == pytest.approx(100 * 1.0 / 1_000_000 * 10_000)


def test_a_task_with_no_current_version_checks_the_one_asked_for(task):
    ship(task, policy(1, "good"))
    (task.policies.dir("toy") / "channels.json").unlink()  # 0.1.0a1 left only `next`: no current
    r = check.check(task, against="v1")
    assert [s.name for s in r.sides] == ["v1"] and r.exit == 0


def test_check_writes_no_record(task):
    ship(task, policy(1, "good"), policy(2, "good"), candidate=2)
    assert check.check(task, against="v1").verdict == "no_difference"
    assert not (task.where.root / "reports").exists()  # the pull request's check is the record

