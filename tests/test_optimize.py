"""The question as GEPA edits it, and how one answer is scored (no network)."""

import pytest
from conftest import BENCH

from s1flow.client import Boolean, Choice, ChoiceAnswer
from s1flow.eval import Task
from s1flow.eval.gepa import from_text, outcome, score, to_text
from s1flow.eval.cases import Case
from s1flow.eval.task import load
from s1flow.project import Project


def test_question_text_roundtrip():
    q = Choice(instructions="どうする？", criteria={"wake": "起きる", "stamp": "スタンプ", "ignore": None})
    assert from_text(to_text(q), q) == q
    b = Boolean(instructions="有害か", criteria={"true": "有害", "false": "無害"})
    assert from_text("```\n" + to_text(b) + "\n```", b) == b


def test_changed_keys_are_rejected():
    q = Choice(instructions="x", criteria={"a": "A", "b": "B"})
    with pytest.raises(ValueError):
        from_text("INSTRUCTIONS: x\nCRITERIA:\n- a: A\n- c: C", q)
    with pytest.raises(ValueError):
        from_text("INSTRUCTIONS: x\nCRITERIA:\n- b: B\n- a: A", q)  # order matters


def test_massive_question_roundtrip():
    q = load(Project(BENCH), "massive-ja-intent").question
    assert from_text(to_text(q), q) == q


def test_an_honest_probability_scores_higher():
    t = Task(id="t", cases="x", state=lambda r: r, question=Choice(instructions="?", criteria={"a": None, "b": None}), label=lambda r: r)
    case = Case(id="1", state="s", label="a")
    sure = outcome(t, case, ChoiceAnswer(choice="a", probabilities={"a": 0.9, "b": 0.1}))
    wrong = outcome(t, case, ChoiceAnswer(choice="b", probabilities={"a": 0.1, "b": 0.9}))
    assert sure.correct and not wrong.correct and score(sure) > 0.9 > 0.1 > score(wrong)


def test_the_reflection_lm_is_an_llm_model_called_through_the_client(tmp_path, monkeypatch):
    import types

    import litellm

    from s1flow.client import AsyncClient
    from s1flow.core.errors import ConfigError
    from s1flow.eval.gepa import ReflectionLM

    (tmp_path / "s1flow.toml").write_text(
        'default = []\n[models.writer]\nprovider = "llm"\nid = "openai/w"\n'
        'price = { input_per_mtok = 1.0, output_per_mtok = 2.0, as_of = "2026-10-22", source = "test" }\n'
        '[models.jev]\nprovider = "typesafe"\nid = "jev-1.14.0"\n'
    )
    sent = []

    async def fake(**kw):
        sent.append(kw)
        usage = types.SimpleNamespace(prompt_tokens=1_000, completion_tokens=500)
        return types.SimpleNamespace(choices=[types.SimpleNamespace(message=types.SimpleNamespace(content="new question"))], usage=usage, _hidden_params={})

    monkeypatch.setattr(litellm, "acompletion", fake)
    client = AsyncClient(tmp_path / "s1flow.toml")
    lm = ReflectionLM(client, "writer")
    assert lm("rewrite it") == "new question" and lm.calls == 1 and lm.name == "writer"
    assert sent[0]["model"] == "openai/w" and sent[0]["messages"] == [{"role": "user", "content": "rewrite it"}] and sent[0]["temperature"] == 1
    assert lm.cost == pytest.approx(1_000 * 1e-6 + 500 * 2e-6)  # s1flow.toml's list price
    with pytest.raises(ConfigError, match="llm"):
        ReflectionLM(client, "jev")  # a decision model writes no text
