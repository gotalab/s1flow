"""Policies: the stored version, the rule, the state's shape, deciding, logs and spans (no network)."""

import asyncio
import json
import sys

import pytest
from conftest import attach, make_project, ship

from s1flow import policies
from s1flow.core.errors import ConfigError, DataError, NotFound, ProviderError, S1flowError
from s1flow.core import place
from s1flow.eval.evaluation import Evaluation, Failures
from s1flow.eval.policy import EvaluatedPolicy, Evidence, Selection, Store
from s1flow.project import Project
from s1flow.eval.candidate import Candidate
from s1flow.eval.kinds import kind_of
from s1flow.policies import DecisionRule
from s1flow.policies import policy as loading
from s1flow.policies import log as logs
from s1flow.eval.candidate import variant_name
from s1flow.policies.file import PolicySpec, asked
from s1flow.client import Client
from s1flow.client.lineup import Lineup
from s1flow.client.identity import execution_digest
from s1flow.policies.state_shape import mismatch, schema_of
from s1flow.client import Boolean, BooleanAnswer, Capabilities, Choice, ChoiceAnswer, Response, ModelBuild, ModelSpec, Usage
from s1flow.policies.kinds import KindParams

STATE = {"title": "Crash on start", "body": "It crashes."}
CLASSES = ["kind/bug", "kind/question", "kind/enhancement"]


class Fake:
    """Answers `kind/bug` with the probability set on the class; fails when it is None."""

    p: float | None = 0.9
    calls = 0

    def __init__(self, b: ModelBuild):
        self.id, self.capabilities, self.concurrency = f"fake:{b.spec.id}", b.spec.capabilities, 1

    async def decide(self, state, questions, *, options=None):
        Fake.calls += 1
        if Fake.p is None:
            raise ProviderError("down", status=503)
        q = next(iter(questions))
        rest = (1 - Fake.p) / 2
        return Response(answers={q: ChoiceAnswer(choice="kind/bug", probabilities={"kind/bug": Fake.p, "kind/question": rest, "kind/enhancement": rest})}, answered_by="fake-1")


def fake(b: ModelBuild) -> Fake:
    return Fake(b)


def evaluation(model: str = "fake") -> Evaluation:
    return Evaluation(candidate=Candidate(model=model), answered_by="fake-1", answered_by_all=["fake-1"], n=10, probabilities=True,
                      failures=Failures(calls=10, failed=0, unsupported=0, data_errors=0, unlabeled=0))


def policy_client():
    return Client(connections=Lineup(default=[], models={"fake": ModelSpec(provider="test_policy:fake", id="fake-1")}))


def policy(task="t", version=1, rule=DecisionRule(min_probability=0.8), test=None) -> EvaluatedPolicy:
    spec = PolicySpec(
        s1flow_version="0", task=task, version=version, at="2026-10-16T00:00:00Z",
        connection="fake", model_id="fake-1",
        questions={"kind": asked(Choice(instructions="What kind?", criteria={c: None for c in CLASSES}), rule)},
        state_schema=schema_of([STATE]),
    )
    return EvaluatedPolicy(
        spec=spec, candidate=Candidate(model="fake"), answered_by="fake-1",
        selection=Selection(by="t", reason="t", tied=["fake"]),
        evidence=Evidence(data_sha256="0", execution_digest=execution_digest(policy_client().connections.resolved("fake"), spec.digest),
                          evaluation=evaluation(), test=test, compared=["fake"]),
    )


@pytest.fixture
def store(tmp_path):
    Fake.p, Fake.calls = 0.9, 0
    return Store(tmp_path / "policies")


def test_versions_are_never_rewritten_and_current_moves(store, tmp_path):
    store.write_new(policy())
    with pytest.raises(ConfigError, match="already has v1"):
        store.write_new(policy())
    assert store.current("t") is None
    ship(store, policy(version=2))
    assert store.current("t") == 2 and store.read("t").spec.version == 2
    raw = json.loads((tmp_path / "policies" / "t" / "v1.json").read_text())
    assert raw["schema"] == "s1flow/policy@2" and "api_key" not in json.dumps(raw)


def test_current_is_the_one_channel(store, tmp_path):
    store.write_new(policy())
    (tmp_path / "policies" / "t" / "channels.json").write_text('{"schema": "s1flow/channels@1", "channels": {"current": 1, "next": 1}}')
    with pytest.raises(ConfigError, match="the one channel is `current`"):
        store.current("t")
    for name in ("t@next", "t@current"):
        with pytest.raises(ConfigError, match=r"TASK \(its current version\) or TASK@vN"):
            runtime_load(name, root=tmp_path / "policies")


def test_a_broken_policy_file_is_a_config_error(store, tmp_path):
    (tmp_path / "policies" / "t").mkdir(parents=True)
    (tmp_path / "policies" / "t" / "v1.json").write_text('{"schema": "s1flow/decision@1"}')
    (tmp_path / "policies" / "t" / "channels.json").write_text('{"current": 1}')
    with pytest.raises(ConfigError):
        store.read("t")


def test_the_rule():
    yes = BooleanAnswer(probability=0.7)
    b = kind_of(Boolean(instructions="?"))
    assert b.read([yes], DecisionRule()).value is True
    r = b.read([yes], DecisionRule(threshold=0.8))
    assert (r.value, r.probability, r.p_positive) == (False, pytest.approx(0.3), 0.7)
    assert b.read([yes], DecisionRule(min_probability=0.75)).below_min_probability
    c = Choice(instructions="?", criteria={k: None for k in CLASSES})
    a = ChoiceAnswer(choice="kind/bug", probabilities={"kind/bug": 0.5, "kind/question": 0.3, "kind/enhancement": 0.2})
    r = kind_of(c).read([a, a], DecisionRule())
    assert (r.value, r.probability, r.below_min_probability) == ("kind/bug", 0.5, None) and r.distribution == [0.5, 0.3, 0.2]
    r = kind_of(c, KindParams(positive="kind/question")).read([a], DecisionRule(threshold=0.25))
    assert (r.value, r.p_positive, r.distribution) == (True, pytest.approx(0.3), None)
    with pytest.raises(ProviderError, match="outside the contract"):
        kind_of(c).read([yes], DecisionRule())


def test_the_state_shape():
    s = schema_of([STATE, {"title": "x", "body": "y", "labels": ["a"]}])
    assert mismatch(s, STATE) == []
    assert mismatch(s, {"title": "x"}) == ["state.body: missing"]
    assert mismatch(s, {"title": 3, "body": "y", "extra": 1}) == ["state.title: expected string, got number", "state.extra: not permitted by the input shape"]
    assert mismatch(schema_of(["text"]), {"a": 1}) == ["state: expected string, got object"]


def runtime_load(*args, **kw):
    return policies.load(*args, client=policy_client(), **kw)


def decide(r, state=STATE, **kw):
    return policies.DecisionPolicy(r.spec, client=policy_client(), **kw).decide(state, case_id="c1")


def test_the_answer_comes_with_its_probability(store):
    d = decide(policy())
    assert (d.value, d.below_min_probability, d.policy) == ("kind/bug", False, "t@v1") and d.probability == pytest.approx(0.9)
    Fake.p = 0.6
    assert decide(policy()).below_min_probability  # under the min probability: still an answer; what to do is the caller's
    assert not decide(policy(rule=DecisionRule())).below_min_probability


def test_a_failed_call_raises_and_is_logged(store, tmp_path):
    Fake.p = None
    log = tmp_path / "log.jsonl"
    with pytest.raises(ProviderError, match="down"):
        decide(policy(), log=log)
    line = json.loads(log.read_text())
    assert line["type"] == "failed" and "down" in line["error"]


def test_an_answer_without_the_question_is_a_logged_provider_error(store, tmp_path, monkeypatch):
    async def other(self, state, questions, *, options=None):
        return Response(answers={"other": ChoiceAnswer(choice="kind/bug")}, answered_by="fake-1")

    monkeypatch.setattr(Fake, "decide", other)
    log = tmp_path / "log.jsonl"
    with pytest.raises(ProviderError, match="outside the contract"):
        decide(policy(), log=log)
    assert json.loads(log.read_text())["type"] == "failed"


def test_a_state_of_another_shape_is_rejected(store):
    with pytest.raises(DataError, match="state.body: missing"):
        decide(policy(), {"title": "x"})
    assert Fake.calls == 0


def test_development_discovery_and_explicit_runtime_store(tmp_path, monkeypatch):
    """CLI/development discovery stays within Git; the runtime requires its store explicitly."""
    (tmp_path / ".git").mkdir()
    (tmp_path / "policies").mkdir()  # unrelated repository content
    (tmp_path / "s1flow").mkdir()
    (tmp_path / "s1flow" / "s1flow.toml").write_text("default = []\n[models]\n")
    store = Store(tmp_path / "s1flow" / "policies")
    ship(store, policy())
    (tmp_path / "app" / "src").mkdir(parents=True)
    monkeypatch.chdir(tmp_path / "app" / "src")
    with pytest.raises(ConfigError, match="path=.*root="):
        runtime_load("t")
    assert runtime_load("t", root=store.root).spec.ref == "t@v1"
    with pytest.raises(ConfigError, match="next"):
        runtime_load("t@next", root=store.root)
    assert place.project(None) == tmp_path / "s1flow"


def test_project_configuration_is_explicit_not_environment_owned(tmp_path, monkeypatch):
    home = tmp_path / "app"
    home.mkdir()
    (home / "s1flow.toml").write_text("default = []\n[models]\n")
    monkeypatch.chdir(home)
    project = Project(place.project(None, required=True))
    assert place.root() == project.root == home.resolve()
    assert project.config == home / "s1flow.toml"
    assert project.policies_dir == home / "policies"
    assert project.cache_dir == home / ".cache"
    chosen = tmp_path / "chosen.toml"
    assert Project(home, connections=chosen).config == chosen


def test_without_an_s1flow_toml_there_is_no_project(tmp_path, monkeypatch):
    (tmp_path / "policies").mkdir()
    monkeypatch.chdir(tmp_path)
    with pytest.raises(ConfigError, match="no s1flow project.*--project.*s1flow init"):
        place.project(None, required=True)


def test_feedback_and_spans(store, tmp_path):
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    old = loading._tracer
    loading._tracer = provider.get_tracer("s1flow")
    try:
        log = tmp_path / "log.jsonl"
        d = policies.DecisionPolicy(policy().spec, client=policy_client(), log=log)
        with provider.get_tracer("app").start_as_current_span("request") as parent:
            result = d.decide(STATE, case_id="c1")  # on the background loop, under the caller's span
        d.feedback(result.decision_id, "kind/question")
    finally:
        loading._tracer = old
    finished = {s.name: s for s in exporter.get_finished_spans()}
    assert finished["s1flow.decide"].parent.span_id == parent.get_span_context().span_id
    spans = {name: s.attributes for name, s in finished.items()}
    assert spans["s1flow.decide"]["s1flow.policy"] == "t@v1" and spans["s1flow.decide"]["gen_ai.operation.name"] == "decide"
    assert spans["s1flow.decide"]["s1flow.case_id"] == "c1" and spans["s1flow.feedback"]["s1flow.label"] == '"kind/question"'
    lines = [json.loads(x) for x in log.read_text().splitlines()]
    assert [x["type"] for x in lines] == ["answered", "feedback"] and lines[0]["state"] is None  # the state is kept only on request


def test_decide_and_adecide_answer_alike(store):
    """decide blocks (from any thread, even under a running loop); adecide is the same call awaited."""
    import threading

    d = policies.DecisionPolicy(policy().spec, client=policy_client())
    assert d.decide(STATE).value == "kind/bug"
    assert asyncio.run(d.adecide(STATE)).value == "kind/bug"

    async def inside_a_loop():
        return d.decide(STATE)

    assert asyncio.run(inside_a_loop()).value == "kind/bug"
    got = []
    threads = [threading.Thread(target=lambda: got.append(d.decide(STATE).value)) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert got == ["kind/bug"] * 4


def test_policies_stay_light():
    """What an app ships loads none of the evaluation stack, nor the evaluation's own shapes."""
    import subprocess

    code = ("import sys, s1flow.policies; print(sorted(m for m in ('numpy', 'litellm', 'sklearn', 'scipy', 'PIL', 's1flow.eval',"
            " 's1flow.project') if m in sys.modules))")
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True).stdout.strip()
    assert out == "[]"


def test_a_policy_decides_without_reading_why_it_was_chosen(store, tmp_path):
    """Runtime specs have no evaluation fields, and runtime never reads an evaluation sidecar."""
    path = tmp_path / "v1.json"
    path.write_text(policy().spec.dump())
    (tmp_path / "v1.evaluation.json").write_text('{"invalid": "evaluation is not loaded"}')
    d = runtime_load(path=path)
    assert d.decide(STATE).value == "kind/bug"
    raw = json.loads(path.read_text())
    for field in ("evidence", "selection", "unknown"):
        path.write_text(json.dumps({**raw, field: {}}))
        with pytest.raises(ConfigError, match=field):
            runtime_load(path=path)


def test_a_span_reads_back_as_the_record_it_was_written_from(store, tmp_path):
    log = tmp_path / "log.jsonl"
    d = policies.DecisionPolicy(policy().spec, client=policy_client(), log=log)
    result = d.decide(STATE, case_id="c1")
    d.feedback(result.decision_id, "kind/question")
    Fake.p = None
    with pytest.raises(ProviderError):
        d.decide(STATE, case_id="c2")
    for line in log.read_text().splitlines():
        rec = logs.AnsweredLog.model_validate_json(line) if '"answered"' in line else (
            logs.FeedbackLog.model_validate_json(line) if '"feedback"' in line else logs.FailedLog.model_validate_json(line))
        name, attrs = logs.span(rec, "p", "m")
        back = logs.from_span(name, rec.at, attrs)
        if isinstance(rec, logs.AnsweredLog):
            rec.decision.response, rec.decision.distribution = None, None  # what a span leaves out
        if isinstance(rec, logs.FailedLog):
            rec.error = rec.error.partition(":")[0]  # a span keeps the kind
        assert back == rec


def test_the_packages_depend_downward_only():
    """pyproject.toml's import-linter contracts: core <- client <- policies <- project <- eval <- integrations <- cli."""
    import subprocess
    from pathlib import Path

    lint = Path(sys.executable).with_name("lint-imports")
    done = subprocess.run([str(lint)], cwd=Path(__file__).parents[1], capture_output=True, text=True)
    assert done.returncode == 0, done.stdout[-2000:]


class Sharp:
    """Right on every case, with the probability it was made with."""

    def __init__(self, b: ModelBuild):
        self.sure = {"good": 0.97, "vague": 0.6}[b.name]
        self.id, self.concurrency, self.capabilities = f"sharp:{self.sure}", 4, Capabilities()

    async def decide(self, state, questions, *, options=None):
        p = self.sure if state["y"] else 1 - self.sure
        return Response(answers={"q": BooleanAnswer(probability=p)}, answered_by=f"{self.id}-v2", usage=Usage(cost_usd=0.0001))


def test_the_first_run_fixes_the_test_share_and_rank_and_report_write_nothing(tmp_path):
    from s1flow.objectives import Coverage
    from s1flow.eval import Task, adopt, evalset, report
    from s1flow.eval import run as running

    p = make_project(tmp_path, {"good": Sharp, "vague": Sharp})
    rows = [{"id": str(i), "y": i % 2 == 0} for i in range(60)]  # under 200 cases: the same 30% test share
    (tmp_path / "data.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    task = attach(Task(id="toy", cases="data.jsonl", dir=tmp_path, state=lambda r: {"y": r["y"]}, question=Boolean(instructions="?"),
                       label=lambda r: r["y"], objective=Coverage()), p)
    for name in ("good", "vague"):
        asyncio.run(running.run_model(task, name, limit=None, variant="base"))
    fixed = evalset.path(task).read_text()
    assert len(evalset.read(task).ids("test")) == 18  # the first run fixed it
    ranked = adopt.shortlist(task).evaluations  # train/val only: the test share is never shown to a ranking
    assert ranked["good"].test is None
    report.write(task, "base", task.where.root / "out")
    assert evalset.path(task).read_text() == fixed and adopt.shortlist(task).evaluations == ranked
    one = attach(Task(id="one", cases="data.jsonl", dir=tmp_path / "one", state=lambda r: {"y": r["y"]}, question=Boolean(instructions="?"),
                      label=lambda r: r["y"]), p)
    (tmp_path / "one").mkdir()
    (tmp_path / "one" / "data.jsonl").write_text(json.dumps(rows[0]) + "\n")
    with pytest.raises(DataError, match="one: 1 labelled cases; holding out a test share and cross-validating the rest needs 3 or more"):
        evalset.current(one)
    assert "not fixed yet" in (evalset.fix(one) or "") and not evalset.path(one).exists()  # run still asks the models
    asyncio.run(running.run_model(one, "good", limit=None, variant="base"))
    assert not evalset.path(one).exists()


def test_adopt_chooses_from_the_runs_and_names_the_version(tmp_path):
    from s1flow.objectives import Coverage
    from s1flow.eval import Task, adopt, evalset
    from s1flow.eval import run as running

    # good's `model` is none of its versions: an alias, which runs and compares but cannot be released
    p = make_project(tmp_path, {"good": Sharp, "vague": Sharp}, versions={"good": {"2": "good-2"}})
    rows = [{"id": str(i), "y": i % 2 == 0} for i in range(60)]
    (tmp_path / "data.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    task = attach(Task(id="toy", cases="data.jsonl", dir=tmp_path, state=lambda r: {"y": r["y"]}, question=Boolean(instructions="?"),
                       label=lambda r: r["y"], objective=Coverage()), p)
    for name in ("good", "good:2", "vague"):
        asyncio.run(running.run_model(task, name, limit=None, variant="base"))
    listed = adopt.shortlist(task)
    fixed = evalset.path(task).read_text()  # the first run fixed the evaluation set
    assert listed.fits[0].candidate == "good" and task.policies.versions("toy") == []  # listing writes nothing
    assert {r.candidate: r.pin for r in listed.rows()} == {"good": "alias", "good:2": "yes", "vague": "no"}
    with pytest.raises(S1flowError, match="good is an alias .*good:2"):
        adopt.adopt(task, "good", "you", "sure more often", listed=listed)
    assert task.policies.versions("toy") == [] and evalset.path(task).read_text() == fixed
    r = adopt.adopt(task, "good:2", "you", "sure more often", listed=listed)
    assert r.candidate.model == "good:2" and r.spec.model_id == "good-2" and r.spec.connection == "good:2"  # the id, not what the runs say
    assert r.answered_by == "sharp:0.97-v2" and task.where.client().connections.build(r.spec.connection).id == "sharp:0.97"
    assert r.spec.rule.min_probability == pytest.approx(0.97) and r.evidence.compared == ["good", "good:2", "vague"]
    assert r.selection.by == "you" and not r.selection.forced and r.spec.s1flow_version
    assert task.policies.current("toy") == 1 and r.spec.state_schema == {"type": "object", "properties": {"y": {"type": "boolean"}}, "required": ["y"], "additionalProperties": False}
    assert r.evidence.evaluation.objective and r.evidence.evaluation.objective.objective == Coverage()


def test_a_person_picks_another_candidate_and_the_policy_says_so(tmp_path):
    from s1flow.objectives import Accuracy, Constraints
    from s1flow.eval import Task, adopt
    from s1flow.eval import run as running

    p = make_project(tmp_path, {"good": Sharp, "vague": Sharp})
    rows = [{"id": str(i), "y": i % 2 == 0} for i in range(60)]
    (tmp_path / "data.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    task = attach(Task(id="toy", cases="data.jsonl", dir=tmp_path, state=lambda r: {"y": r["y"]}, question=Boolean(instructions="?"),
                       label=lambda r: r["y"], objective=Accuracy()), p)
    for name in ("good", "vague"):
        asyncio.run(running.run_model(task, name, limit=None, variant="base"))
    listed = adopt.shortlist(task)
    rows_ = {r.candidate: r for r in listed.rows()}
    assert rows_["good"].tied and not hasattr(rows_["good"], "recommended")  # the list marks no pick
    assert {r.pin for r in rows_.values()} == {"no"}  # neither declares versions: each serves one
    r = adopt.adopt(task, "vague", "you", "free tier", listed=listed)
    assert r.candidate.model == "vague" and r.selection.tied == listed.tied
    with pytest.raises(S1flowError, match="cannot be picked.*pick one of"):
        adopt.adopt(task, "nope", "you", "x", listed=listed)
    with pytest.raises(S1flowError, match="who adopted it and why"):
        adopt.adopt(task, "good", "you", " ", listed=listed)
    task.constraints = Constraints(min_labels=1000)
    with pytest.raises(S1flowError, match="cannot be picked"):
        adopt.adopt(task, "good", "you", "x")


def test_a_policy_dumps_the_same_bytes_whatever_the_hash_seed(tmp_path):
    import subprocess

    code = ("from s1flow.client import Capabilities; "
            "print(Capabilities(question_types=frozenset({'boolean', 'choice', 'score', 'box'})).model_dump_json())")
    outs = {subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True,
                           env={"PYTHONHASHSEED": str(seed), "PATH": ""}).stdout for seed in range(6)}
    assert len(outs) == 1 and '"question_types":["boolean","box","choice","score"]' in outs.pop()





def test_a_decision_names_the_content_that_made_it(store, tmp_path):
    ship(store, policy())
    path = tmp_path / "policies" / "t" / "v1.json"
    raw = json.loads(path.read_text())
    want = policies.file.policy_digest(raw)
    log = tmp_path / "log.jsonl"
    d = runtime_load("t", root=tmp_path / "policies", log=log).decide(STATE, case_id="c1")
    assert d.policy == "t@v1" and d.policy_digest == want and len(want) == 64
    assert json.loads(log.read_text().splitlines()[0])["decision"]["policy_digest"] == want
    copied = tmp_path / "elsewhere.json"
    copied.write_text(json.dumps(raw, indent=4, sort_keys=True))  # the same content, written another way
    assert runtime_load(path=copied).spec.digest == want
    raw["questions"]["kind"]["rule"]["min_probability"] = 0.5
    copied.write_text(json.dumps(raw))
    assert runtime_load(path=copied).spec.digest != want  # other content, another digest
    r = store.read("t")
    assert r.spec.digest == want and r.spec.with_question(Choice(instructions="Other?", criteria={c: None for c in CLASSES})).digest != want


def test_a_question_keeps_what_its_type_leaves_open_in_a_task_and_a_policy():
    from s1flow.client import Box
    from s1flow.eval import Task

    params = KindParams(iou=0.7)
    box_task = Task(id="box", cases="x", state=lambda row: row, question=Box(instructions="?"),
                    label=lambda row: row, kind_params=params)
    assert json.loads(params.model_dump_json()) == {"iou": 0.7}
    assert box_task.kind.iou == 0.7
    with pytest.raises(ValueError, match="boolean and choice"):
        asked(Box(instructions="?"), DecisionRule(), params)
    assert json.loads(asked(Boolean(instructions="?"), DecisionRule()).model_dump_json())["kind"] == {}  # unset, left out: digests stay
    with pytest.raises(ConfigError, match="kind_params: positive 'c' is not an option"):
        Task(id="t", cases="x", state=lambda r: r, question=Choice(instructions="?", criteria={"a": None, "b": None}),
             label=lambda r: r, kind_params=KindParams(positive="c"))


def test_a_policy_asks_its_questions_by_id(tmp_path):
    raw = json.loads(policy().spec.dump())
    assert list(raw["questions"]) == ["kind"] and raw["questions"]["kind"]["kind"] == {} and "question_id" not in raw
    path = tmp_path / "v1.json"
    raw["questions"]["kind"]["kind"] = {"threshold": 0.5}
    path.write_text(json.dumps(raw))
    with pytest.raises(ConfigError, match="kind.threshold: Extra inputs are not permitted"):
        runtime_load(path=path)
    raw["questions"]["kind"]["question"]["criterion"] = {}  # misspelt: refused, not dropped from what the digest names
    path.write_text(json.dumps(raw))
    with pytest.raises(ConfigError, match="criterion: Extra inputs are not permitted"):
        runtime_load(path=path)
    del raw["questions"]["kind"]["question"]["criterion"]
    raw["questions"]["kind"]["kind"] = {"iou": 0.7}
    path.write_text(json.dumps(raw))
    with pytest.raises(ConfigError, match="iou is a box question's bar for a hit; this one is choice"):
        runtime_load(path=path)
    raw["questions"]["kind"]["kind"] = {}
    raw["questions"]["other"] = raw["questions"]["kind"]
    path.write_text(json.dumps(raw))
    with pytest.raises(ConfigError, match="questions: Dictionary should have at most 1 item"):
        runtime_load(path=path)


def test_every_stored_policy_reads_with_the_policy_layer_alone(tmp_path):
    from pathlib import Path
    import shutil
    from s1flow.policies.file import read_file

    root = Path(__file__).resolve().parents[1]
    copied = tmp_path / "project"
    shutil.copytree(root / "apps/bench/policies", copied / "policies")
    found = sorted((copied / "policies").glob("*/v[0-9].json"))
    assert len(found) == 5
    for path in found:
        spec = read_file(path)
        assert spec.question_id in spec.questions and spec.kind and spec.rule
        assert Store(copied / "policies").read(spec.task, version=spec.version).spec == spec


def test_a_name_that_is_not_there_lists_the_ones_that_are(store, tmp_path):
    store.write_new(policy())
    with pytest.raises(NotFound, match=r"t has no current version"):
        store.read("t")
    ship(store, policy(version=2))
    with pytest.raises(NotFound, match=r"no policy of 'x'; tasks with policies: t"):
        store.read("x")
    with pytest.raises(NotFound, match="no policy .*v9.json"):
        store.read("t", version=9)
    log = tmp_path / "log.jsonl"
    d = policies.DecisionPolicy(policy().spec, client=policy_client(), log=log)
    with pytest.raises(ConfigError, match="label 'kind/nope' is not an answer to its question"):
        d.feedback("c1", "kind/nope")
    with pytest.raises(ConfigError, match="not an answer"):
        d.feedback("c1", True)  # a choice that is not binary takes its options only
    assert not log.exists()
    d.feedback("c1", "kind/bug")
    assert log.exists()
    # logged as the task labels it: a choice scored as binary logs whether the answer is the positive option
    p = policy().spec.model_copy(update={"questions": {"kind": asked(policy().spec.question, DecisionRule(threshold=0.5), KindParams(positive="kind/bug"))}})
    policies.DecisionPolicy(p, client=policy_client(), log=log).feedback("c2", "kind/question")
    assert [json.loads(x)["label"] for x in log.read_text().splitlines()] == ["kind/bug", False]


def test_one_candidate_grammar():
    assert Candidate(model="jev:1.14").name == "jev:1.14"
    assert Candidate(model="d1@vercel", variant="policy").name == "d1@vercel/policy"
    for name in ("jev:1.14", "d1@vercel/policy", "jev@openrouter:2026-10-17/gepa-jev"):
        assert Candidate.parse(name).name == name
    assert Candidate.parse("jev/base") == Candidate(model="jev")
    for bad in ("", "/policy", "jev/", "jev/a/b", "d1@vercel · policy", "jev :1.14"):
        with pytest.raises(ConfigError, match=r"model\[:version\]\[/variant\]"):
            Candidate.parse(bad)
    with pytest.raises(ConfigError, match="variant 'a b'"):
        variant_name("a b")
    with pytest.raises(ValueError, match="no whitespace, ':', '/' or ','"):
        ModelSpec(provider="x", id="m", versions={"a/b": {"id": "m"}})


def test_only_adopt_switches_current():
    """channels.json has one writer (Policies._switch), reached only from what `s1flow adopt` runs."""
    import re
    from pathlib import Path

    src = Path(__file__).resolve().parents[1] / "src" / "s1flow"
    callers = sorted(f"{p.relative_to(src)}" for p in src.rglob("*.py")
                     if re.search(r"adopted=|\.switch\(|\._switch\(", p.read_text()) and p.name != "history.py")
    assert callers == ["cli/adopt.py", "eval/adopt.py", "eval/policy.py", "policies/file.py"]
