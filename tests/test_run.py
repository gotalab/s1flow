import asyncio
import json
import re

import pytest
from conftest import make_project

from s1flow.core.errors import ConfigError, DataError, NotFound, Unsupported
from s1flow.client import Capabilities, ChoiceAnswer, Response
from s1flow.eval import data, metrics, records
from s1flow.eval import run as running
from s1flow.eval.records import PredictionRecord
from s1flow.eval.task import load
from s1flow.project import scaffold


def line(id, answered_by="jev-1.13.0", at="2026-10-07", prompt="p1", **kw):
    """A record as written to disk; `reason=` makes a failure line."""
    r = {"schema": "s1flow/run@2", "id": id, "model": "jev", "prompt": prompt, "at": at, **kw}
    if kw:
        r |= {"outcome": "failed"}
    else:
        r |= {"outcome": "answered", "answer": {"type": "choice", "choice": "a"}, "answered_by": answered_by, "request_digest": "d", "retries": 0}
    return PredictionRecord.model_validate(r)


def test_an_answered_line_without_retries_or_answered_by_is_refused():
    """Every answered call records who answered and how many retries it took; a failed one need not."""
    good = line("a").model_dump(mode="json")
    for field in ("retries", "answered_by"):
        with pytest.raises(ValueError, match=f"an answered record needs {field}"):
            PredictionRecord.model_validate({k: v for k, v in good.items() if k != field})
    assert line("b", reason="timeout").retries is None


def ids(lines):
    return sorted((r.id, r.answered_by, r.outcome == "failed") for r in lines)


def test_select_scores_the_latest_answering_model_on_the_current_prompt():
    lines = [line("a"), line("b"), line("a", "jev-1.14.0", at="2026-10-15"), line("c", prompt="old")]
    s = records.select(lines, "p1")
    assert s.answered_by == "jev-1.14.0" and s.versions == ["jev-1.14.0", "jev-1.13.0"]
    assert ids(s.records) == [("a", "jev-1.14.0", False)]  # c was another prompt
    assert s.earlier == ["b"]  # answered by 1.13 only: no answer from 1.14, so a run asks it again


def test_select_a_later_failure_does_not_hide_an_answer():
    lines = [line("a"), line("a", at="2026-10-15", reason="AI_GATEWAY_API_KEY is not set"), line("b", at="2026-10-15", reason="boom")]
    s = records.select(lines, "p1")
    assert ids(s.records) == [("a", "jev-1.13.0", False), ("b", None, True)] and s.earlier == []


def test_select_reads_the_cases_in_id_order_whatever_order_the_calls_ended_in():
    lines = [line("c"), line("a"), line("b")]
    assert [r.id for r in records.select(lines, "p1").records] == ["a", "b", "c"]


class Fake:
    """Answers every case; fails while `broken` (RuntimeError: an unexpected error is the case's outcome)."""

    made: list["Fake"] = []
    broken = False

    def __init__(self, model_id="fake-1"):
        self.id, self.model_id, self.concurrency, self.capabilities = f"fake:{model_id}", model_id, 4, Capabilities()
        self.calls = 0
        Fake.made.append(self)

    async def decide(self, state, questions, *, options=None):
        self.calls += 1
        if Fake.broken:
            raise RuntimeError("down")
        q = next(iter(questions))
        return Response(answers={q: ChoiceAnswer(choice="wake", probabilities={"wake": 1.0})}, answered_by=self.model_id)


@pytest.fixture
def nod(tmp_path):
    Fake.made, Fake.broken = [], False
    p = make_project(tmp_path, {"fake": lambda b: Fake(b.spec.id if b.spec.id != "fake" else "fake-1")}, copy_tasks=("nod-wake",),
                     versions={"fake": {"2": "fake-2"}})
    return load(p, "nod-wake")


def calls(model_id):
    return sum(f.calls for f in Fake.made if f.model_id == model_id)


def test_run_appends_skips_answered_cases_and_keeps_answers_through_failures(nod):
    go = lambda **kw: asyncio.run(running.run_model(nod, "fake", variant="base", **kw))
    path = running.run_path(nod, "base", "fake")
    go(limit=3)
    assert len(records.read(path)) == 3 and calls("fake-1") == 3
    go(limit=5)  # the first 3 are already answered under this prompt
    assert len(records.read(path)) == 5 and calls("fake-1") == 5
    Fake.broken = True
    go(limit=5, fresh=True)  # a run that fails only adds failure lines
    lines = records.read(path)
    assert len(lines) == 10 and sum(r.outcome == "failed" for r in lines) == 5
    s = records.select(lines, running.prompt_hash(nod.questions("base")))
    assert s.answered_by == "fake-1" and all(r.answered for r in s.records) and len(s.records) == 5


def test_a_label_the_question_cannot_score_stops_the_run_before_any_call(nod):
    """A boolean reading of 0/1 or "true" is not a label: run refuses before it spends a call, as report would fail on it."""
    nod.label = lambda r: {"must": 1, "sleep": 0}.get(r["label"])
    nod.load_cases().forget()
    with pytest.raises(DataError, match="labels the question cannot score, so no model is asked: .*true or false, got 1"):
        asyncio.run(running.run(nod, ["fake"]))
    assert calls("fake-1") == 0 and not running.run_path(nod, "base", "fake").exists()


def test_cases_only_an_earlier_answering_model_answered_are_asked_again(nod, monkeypatch):
    """Under an alias the answering model can change between runs: the cases only the earlier one answered have no
    answer from the one scored, so they count as missing and the next run asks them past the cache."""
    go = lambda **kw: asyncio.run(running.run_model(nod, "fake", variant="base", **kw))  # noqa: E731
    go(limit=3)
    first = {r.id for r in records.read(running.run_path(nod, "base", "fake"))}
    monkeypatch.setattr(Fake, "decide", answering_as("fake-1b"))
    go(limit=5)  # the 2 new cases are answered by fake-1b, the one now scored
    pr = metrics.load(nod, "base", "fake", include_test=True)
    assert pr.version == "fake-1b" and len(pr.ids) == 2 and first <= set(pr.never_asked)  # fake-1's 3 count as missing
    asked = calls("fake-1")
    go(limit=5)
    assert calls("fake-1") == asked + 3  # asked again, not read from the cache that holds fake-1's answers
    pr = metrics.load(nod, "base", "fake", include_test=True)
    assert len(pr.ids) == 5 and not first & set(pr.never_asked) and pr.versions == ["fake-1b", "fake-1"]


def test_a_failed_ask_again_does_not_bring_back_the_earlier_answering_model(nod, monkeypatch):
    """The cache holds the earlier model's answers: a case whose ask again failed is asked past it the next time,
    or its cached answer would make the earlier model the scored one again, and the next run swap back."""
    go = lambda **kw: asyncio.run(running.run_model(nod, "fake", variant="base", **kw))  # noqa: E731
    go(limit=3)
    monkeypatch.setattr(Fake, "decide", answering_as("fake-1b"))
    go(limit=5)
    Fake.broken = True
    go(limit=5)  # the 3 asked again fail
    Fake.broken = False
    for _ in range(2):
        go(limit=5)
        assert metrics.load(nod, "base", "fake", include_test=True).version == "fake-1b"
    pr = metrics.load(nod, "base", "fake", include_test=True)
    assert len(pr.ids) == 5 and not pr.failed_cases


def answering_as(version):
    real = Fake.decide

    async def decide(self, state, questions, *, options=None):
        r = await real(self, state, questions, options=options)
        return r.model_copy(update={"answered_by": version})

    return decide


def test_the_scores_do_not_depend_on_the_order_the_calls_ended_in(nod, monkeypatch):
    """The same answers give the same folds, resamples and numbers, whichever call ended first."""
    import hashlib

    async def varied(self, state, questions, *, options=None):
        p = 0.2 + 0.6 * hashlib.sha256(json.dumps(state, sort_keys=True).encode()).digest()[0] / 255
        return Response(answers={next(iter(questions)): ChoiceAnswer(choice="wake" if p >= .5 else "stamp", probabilities={"wake": p, "stamp": 1 - p})},
                        answered_by=self.model_id)

    monkeypatch.setattr(Fake, "decide", varied)
    asyncio.run(running.run_model(nod, "fake", limit=None, variant="base"))
    path = running.run_path(nod, "base", "fake")
    first = metrics.evaluate(nod, metrics.load(nod, "base", "fake"))
    lines = path.read_text().splitlines()
    path.write_text("".join(line + "\n" for line in reversed(lines)))  # the calls ending the other way round
    again = metrics.evaluate(nod, metrics.load(nod, "base", "fake"))
    assert again.objective == first.objective and again.accuracy == first.accuracy and again.tiebreak == first.tiebreak


def test_a_missing_key_stops_the_run_instead_of_filling_it_with_failures(nod, monkeypatch):
    async def no_key(self, state, questions, *, options=None):
        raise ConfigError("AI_GATEWAY_API_KEY is not set")

    monkeypatch.setattr(Fake, "decide", no_key)
    with pytest.raises(ConfigError):
        asyncio.run(running.run_model(nod, "fake", limit=3, variant="base"))
    assert not running.run_path(nod, "base", "fake").exists()


def test_a_cached_answer_that_does_not_parse_stops_the_run_instead_of_failing_the_case(nod):
    go = lambda: asyncio.run(running.run_model(nod, "fake", limit=1, variant="base", fresh=False))  # noqa: E731
    go()
    entry = next((nod.where.cache_dir / "answers").glob("*/*.json"))
    entry.write_text(entry.read_text().replace('"response"', '"decision"'))  # the shape before 2026-10-22
    running.run_path(nod, "base", "fake").unlink()
    with pytest.raises(ConfigError, match="an answer cached in an older shape; rewrite the cache"):
        go()
    assert not running.run_path(nod, "base", "fake").exists()


def test_a_task_id_that_cannot_name_a_policy_is_refused():
    from s1flow.core.place import task_id_error

    assert task_id_error("gh-bug") is None and task_id_error("nod-wake") is None
    assert all(task_id_error(x) for x in ("a@b", "ticket_bug", "Bug", "-x", ""))


def test_a_version_asked_for_by_name_is_a_run_of_its_own(nod):
    go = lambda spec: asyncio.run(running.run_model(nod, spec, limit=3, variant="base"))
    go("fake")
    go("fake:2")  # its own file: what the model answered without a version is not its answers, so all 3 are asked
    go("fake:2")
    base, version = (records.read(running.run_path(nod, "base", n)) for n in ("fake", "fake:2"))
    assert (calls("fake-1"), calls("fake-2")) == (3, 3)
    assert {(r.model, r.answered_by) for r in base} == {("fake", "fake-1")} and {(r.model, r.answered_by) for r in version} == {("fake:2", "fake-2")}
    assert metrics.load(nod, "base", "fake:2").version == "fake-2"
    with pytest.raises(NotFound, match="no version 'fake-2'; versions: 2"):
        go("fake:fake-2")  # the label, not the id


def test_a_version_asked_for_is_asked_what_another_refused(nod, monkeypatch):
    go = lambda spec: asyncio.run(running.run_model(nod, spec, limit=3, variant="base"))
    real = Fake.decide

    async def refuse(self, state, questions, *, options=None):
        raise Unsupported("no images")

    monkeypatch.setattr(Fake, "decide", refuse)
    go("fake")
    go("fake")  # a refusal is final for the same model
    monkeypatch.setattr(Fake, "decide", real)
    assert calls("fake-2") == 0
    go("fake:2")  # the version asked for may answer what the model refused
    assert calls("fake-2") == 3 and [len(records.read(running.run_path(nod, "base", n))) for n in ("fake", "fake:2")] == [3, 3]


def test_numeric_row_ids_are_read_as_strings(tmp_path):
    from s1flow.client import Boolean
    from s1flow.eval import Task

    (tmp_path / "d.jsonl").write_text('{"id": 3, "x": 1}\n{"x": 2}\n')
    t = Task(id="t", cases="d.jsonl", dir=tmp_path, state=lambda r: "s", question=Boolean(instructions="q"), label=lambda r: True)
    assert [c.id for c in t.load_cases().all()] == ["3", "1"]


def test_a_row_without_a_field_task_py_reads_says_which(tmp_path):
    p = make_project(tmp_path / "p")
    d = p.tasks_dir / "t"
    d.mkdir(parents=True)
    (d / "task.py").write_text(scaffold.stub("t", "Bug?"))
    (d / "data.jsonl").write_text(json.dumps({"id": "#7", "title": "x", "label": True}) + "\n")
    got = data.check(load(p, "t"))
    assert got.errors == ["t: the case with id '#7' has no field 'text', which task.py reads (in state, label or show); its fields: id, title, label"]


def test_a_task_whose_id_differs_from_its_directory_is_refused(tmp_path):
    p = make_project(tmp_path / "p")
    d = p.tasks_dir / "t-bug"
    d.mkdir(parents=True)
    (d / "task.py").write_text(scaffold.stub("bug", "Bug?"))  # runs and policies would go to bug/, the lookup to t-bug
    with pytest.raises(ConfigError, match=r"id 'bug' does not match its directory tasks/t-bug: set id='t-bug'"):
        load(p, "t-bug")


def test_the_task_init_writes_spells_out_the_defaults(tmp_path):
    p = make_project(tmp_path / "p", {"fake": lambda b: Fake(b.spec.id)})
    written = scaffold.stub("t", "Bug?")
    bare = re.sub(r"\n    # Every value below.*?\n    optimizer=Gepa\(budget=300, reflection=None\),", "\n    objective=Accuracy(),", written, flags=re.S)
    assert "split=" not in bare and "tiebreak=" not in bare and "optimizer=" not in bare
    rows = "".join(json.dumps({"id": str(i), "text": "x", "label": i % 2 == 0}) + "\n" for i in range(20))
    tasks = []
    for name, text in (("t", written), ("t", bare)):
        d = p.tasks_dir / name
        d.mkdir(parents=True, exist_ok=True)
        (d / "task.py").write_text(text)
        (d / "data.jsonl").write_text(rows)
        tasks.append(load(p, name))
    spelled, default = tasks
    assert spelled.split == default.split and spelled.constraints == default.constraints and spelled.optimizer == default.optimizer
    assert spelled.objectives == default.objectives and spelled.ties == ["latency", "cost"] and default.ties == []  # unordered without one
    ordered = default.copy(tiebreak=["latency", "cost"])
    assert spelled.evaluation_contract_digest == ordered.evaluation_contract_digest  # what was measured is measured alike
    moved = {default.copy(tiebreak=t).evaluation_contract_digest for t in (["cost", "latency"], ["cost"], ["latency"])}
    assert len(moved) == 3 and ordered.evaluation_contract_digest not in moved  # another order is another selection rule
