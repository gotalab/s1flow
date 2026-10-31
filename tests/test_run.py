import asyncio
import json
import re

import pytest
from conftest import make_project

from s1flow.core.errors import ConfigError, NotFound, Unsupported
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


def ids(lines):
    return sorted((r.id, r.answered_by, r.outcome == "failed") for r in lines)


def test_select_scores_the_latest_answering_model_on_the_current_prompt():
    lines = [line("a"), line("b"), line("a", "jev-1.14.0", at="2026-10-15"), line("c", prompt="old")]
    chosen, version, versions = metrics.select(lines, "p1")
    assert version == "jev-1.14.0" and versions == ["jev-1.14.0", "jev-1.13.0"]
    assert ids(chosen) == [("a", "jev-1.14.0", False)]  # b was never answered by 1.14; c was another prompt


def test_select_a_later_failure_does_not_hide_an_answer():
    lines = [line("a"), line("a", at="2026-10-15", reason="AI_GATEWAY_API_KEY is not set"), line("b", at="2026-10-15", reason="boom")]
    chosen, _, _ = metrics.select(lines, "p1")
    assert ids(chosen) == [("a", "jev-1.13.0", False), ("b", None, True)]


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
    chosen, version, _ = metrics.select(lines, running.prompt_hash(nod.questions("base")))
    assert version == "fake-1" and all(r.answered for r in chosen) and len(chosen) == 5


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
