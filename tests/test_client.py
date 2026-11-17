"""The model-calling layer (s1flow.client): Client, AsyncClient, decisions.create, the line-up; the base-install CLI."""

import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path

import httpx
import pytest
import respx
from conftest import PROJECT, s1flow, ship

from s1flow import AsyncClient, Client
from s1flow.client import ModelSpec, Refusal
from s1flow.core.errors import ConfigError, DataError, ProviderError
from s1flow.questions import Boolean, Box, Choice, Score

HERE = Path(__file__).parent
TOML = 'default = ["toy"]\n[models.toy]\nprovider = "toy_provider:build"\nid = "t1"\n[models.later]\nprovider = "llm"\nid = "openai/gpt-5-mini"\n'
QS = {
    "bug": Boolean(instructions="Is it a bug report?"),
    "area": Choice(instructions="Which area?", criteria={"linter": None, "formatter": "how code looks", "server": None}),
    "severity": Score(instructions="How stuck is the reporter?", criteria=["not", "has a workaround", "blocked"]),
    "where": Box(instructions="the error dialog"),
}


@pytest.fixture
def toml(tmp_path, monkeypatch):
    monkeypatch.syspath_prepend(str(HERE))
    path = tmp_path / "s1flow.toml"
    path.write_text(TOML)
    return path


def test_four_types_and_several_questions_in_one_call(toml):
    client = Client(toml)
    d = client.responses.create(model="toy", state={"title": "formatter bug"}, questions=QS)
    a = d.answers
    assert a["bug"].probability == 0.9 and a["area"].choice == "formatter" and a["area"].probabilities["formatter"] == 0.8
    assert a["severity"].score == pytest.approx(1.5) and a["where"].box.right == 0.6 and a["where"].confidence == 0.95
    assert d.answered_by == "toy:t1-1" and d.usage.cost_usd == 0.00001 and d.latency_ms == 5.0
    assert client.responses._inner._built["name:toy"].calls == 1  # one request for the four questions


def test_the_async_client_and_questions_as_json(toml):
    raw = {k: q.model_dump() for k, q in QS.items()}
    d = asyncio.run(AsyncClient(toml).responses.create(model="toy", state="a bug in the server", questions=raw))
    assert d.answers["area"].choice == "server"
    with pytest.raises(DataError, match="questions"):
        asyncio.run(AsyncClient(toml).responses.create(model="toy", state="x", questions={"q": {"type": "colour"}}))


def test_a_refusal_is_one_questions_answer(toml):
    d = Client(toml).responses.create(model="toy", state="bug", questions={"a": Boolean(instructions="refuse this"), "b": QS["bug"]})
    assert isinstance(d.answers["a"], Refusal) and d.answers["b"].probability == 0.9


def test_a_spec_needs_no_lineup(tmp_path, monkeypatch):
    monkeypatch.syspath_prepend(str(HERE))
    monkeypatch.chdir(tmp_path)  # a direct ModelSpec needs no connection configuration
    d = Client().responses.create(model=ModelSpec(provider="toy_provider:build", id="t9"), state="bug", questions={"bug": QS["bug"]})
    assert d.answered_by == "toy:t9-1"


def test_the_lineup_is_read_by_shape_and_checked_apart(toml):
    """An `llm` entry is listed and reads without LiteLLM being touched; check() builds every one."""
    client = Client(toml)
    assert [(m.name, m.default, m.spec.provider) for m in client.connections.list()] == [("toy", True, "toy_provider:build"), ("later", False, "llm")]
    assert [m.name for m in client.connections.list(default_only=True)] == ["toy"]
    assert client.connections.retrieve("toy").spec.id == "t1" and client.connections.build("toy").id == "toy:t1"
    client.connections.check()  # LiteLLM is installed in the development environment
    toml.write_text(TOML + '[models.bad]\nprovider = "nope"\nid = "m"\n')
    with pytest.raises(ConfigError, match="unknown provider"):
        Client(toml).connections.check()


def test_an_answer_missing_a_question_is_the_providers_failure(toml):
    from s1flow.client import BooleanAnswer, Response

    class Short:
        id, concurrency = "short", 1
        capabilities = Client(toml).connections.build("toy").capabilities

        async def decide(self, state, questions, *, options=None):
            return Response(answers={"bug": BooleanAnswer(probability=0.5)}, answered_by="short-1")

    with pytest.raises(ProviderError, match="answered without area"):
        Client(toml).responses.create(model=Short(), state="x", questions={"bug": QS["bug"], "area": QS["area"]})


def test_an_answer_cannot_be_changed_past_validation(toml):
    """Answers and responses are frozen, so a value set after construction cannot skip pydantic: a provider
    that tries fails as a ProviderError, not later as a bug in s1flow."""
    from pydantic import ValidationError

    from s1flow.client import BooleanAnswer, Box, BoxAnswer, BoxEdges, Capabilities, Response

    class Mutated:
        id, concurrency = "mutated", 1
        capabilities = Client(toml).connections.build("toy").capabilities

        async def decide(self, state, questions, *, options=None):
            answer = BooleanAnswer(probability=0.5)
            answer.probability = "high"  # type: ignore[misc]
            return Response(answers={"bug": answer}, answered_by="mutated-1")

    with pytest.raises(ProviderError, match="malformed response outside the contract"):
        Client(toml).responses.create(model=Mutated(), state="x", questions={"bug": QS["bug"]})
    class Constructed(Mutated):
        capabilities = Capabilities(question_types=frozenset({"box"}))

        async def decide(self, state, questions, *, options=None):  # model_construct skips validation and frozen
            return Response(answers={"spot": BoxAnswer.model_construct(box={"top": 5})}, answered_by="constructed-1")

    with pytest.raises(ProviderError, match="malformed response outside the contract"):
        Client(toml).responses.create(model=Constructed(), state="x", questions={"spot": Box(instructions="the cat")})
    box = BoxAnswer(box=BoxEdges(top=0, bottom=1, left=0, right=1))
    for model, field in ((box, "box"), (Response(answers={"b": box}, answered_by="m"), "answered_by")):
        with pytest.raises(ValidationError, match="frozen"):
            setattr(model, field, None)


@pytest.mark.parametrize(
    ("qid", "question", "answer_kind", "detail"),
    [
        ("bug", QS["bug"], "probability", "probability"),
        ("bug", QS["bug"], "nan_probability", "probability"),
        ("area", QS["area"], "choice", "option"),
        ("area", QS["area"], "distribution", "probability"),
        ("area", QS["area"], "type", "type"),
        ("severity", QS["severity"], "inf_score", "score must be finite"),
    ],
)
def test_a_provider_answer_stays_inside_the_question_contract(toml, qid, question, answer_kind, detail):
    from s1flow.client import BooleanAnswer, ChoiceAnswer, Response, ScoreAnswer

    class Broken:
        id, concurrency = "broken", 1
        capabilities = Client(toml).connections.build("toy").capabilities

        async def decide(self, state, questions, *, options=None):
            answer = {
                "probability": BooleanAnswer(probability=2),
                "nan_probability": BooleanAnswer(probability=float("nan")),
                "choice": ChoiceAnswer(choice="bogus"),
                "distribution": ChoiceAnswer(choice="formatter", probabilities={"formatter": 2}),
                "type": BooleanAnswer(probability=0.5),
                "inf_score": ScoreAnswer(score=float("inf")),
            }[answer_kind]
            return Response(answers={qid: answer}, answered_by="broken-1")

    with pytest.raises(ProviderError, match=detail):
        Client(toml).responses.create(model=Broken(), state="x", questions={qid: question})


def test_a_sparse_choice_distribution_is_still_a_valid_provider_answer(toml):
    from s1flow.client import ChoiceAnswer, Response

    class Sparse:
        id, concurrency = "sparse", 1
        capabilities = Client(toml).connections.build("toy").capabilities

        async def decide(self, state, questions, *, options=None):
            return Response(answers={"area": ChoiceAnswer(choice="formatter", probabilities={"formatter": 0.8})}, answered_by="sparse-1")

    d = Client(toml).responses.create(model=Sparse(), state="x", questions={"area": QS["area"]})
    assert d.answers["area"].probabilities == {"formatter": 0.8}


@pytest.mark.parametrize("probabilities", [{"billing": 0.0, "support": 0.0}, {"bogus": 1.0}])
def test_a_choice_distribution_needs_positive_mass_on_an_option(toml, probabilities):
    from s1flow.client import ChoiceAnswer, Response

    route = Choice(instructions="Which route?", criteria={"billing": None, "support": None})

    class Degenerate:
        id, concurrency = "degenerate", 1
        capabilities = Client(toml).connections.build("toy").capabilities

        async def decide(self, state, questions, *, options=None):
            return Response(
                answers={"route": ChoiceAnswer(choice="billing", probabilities=probabilities)},
                answered_by="degenerate-1",
            )

    with pytest.raises(ProviderError, match="positive mass"):
        Client(toml).responses.create(model=Degenerate(), state="x", questions={"route": route})


def test_a_malformed_provider_response_is_a_provider_failure(toml):
    class Malformed:
        id, concurrency = "malformed", 1
        capabilities = Client(toml).connections.build("toy").capabilities

        async def decide(self, state, questions, *, options=None):
            return {"answers": {"bug": {"type": "boolean", "probability": 0.5}}}

    with pytest.raises(ProviderError, match="malformed response"):
        Client(toml).responses.create(model=Malformed(), state="x", questions={"bug": QS["bug"]})


def test_an_extra_provider_answer_is_a_provider_failure(toml):
    from s1flow.client import BooleanAnswer, Response

    class Extra:
        id, concurrency = "extra", 1
        capabilities = Client(toml).connections.build("toy").capabilities

        async def decide(self, state, questions, *, options=None):
            return Response(
                answers={"bug": BooleanAnswer(probability=0.5), "other": BooleanAnswer(probability=0.5)},
                answered_by="extra-1",
            )

    with pytest.raises(ProviderError, match="extra"):
        Client(toml).responses.create(model=Extra(), state="x", questions={"bug": QS["bug"]})


# ---------- the base-install CLI ----------


def test_decide_with_a_model(toml):
    cwd = toml.parent
    which = json.dumps({"q": {"type": "choice", "instructions": "Which?", "criteria": {"linter": None, "server": "the LSP"}}})
    done = s1flow("decide", "--model", "toy", "--state", '{"title": "server bug"}', "--questions", which, cwd=cwd)
    assert done.returncode == 0, done.stderr
    assert done.stdout.splitlines()[0] == "q: server  (server 0.800 · linter 0.200)"
    (cwd / "qs.json").write_text(json.dumps({k: q.model_dump() for k, q in QS.items()}))
    (cwd / "s.json").write_text('"a bug"')
    done = s1flow("decide", "--model", "toy", "--state", "@s.json", "--questions", "@qs.json", "--json", cwd=cwd)
    assert done.returncode == 0, done.stderr
    assert set(json.loads(done.stdout)["answers"]) == set(QS)
    done = s1flow("decide", "--model", "toy", "--state", '"x"', "--choice", "Which?", cwd=cwd)  # one spelling: --questions
    assert done.returncode == 2 and "unrecognized arguments: --choice" in done.stderr
    assert s1flow("decide", "--state", "{}", "--boolean", "?", cwd=cwd).returncode == 2  # neither --model nor --policy


@respx.mock
def test_decide_tries_a_model_no_s1flow_toml_names(tmp_path, toml):
    """`--model provider:id` calls a built-in provider's model with no project, and beside a line-up that lacks it.
    Nothing is declared for it, so a box question goes to the model unchecked."""
    from s1flow.client.providers.liquid import BASE_URL

    reply = {"model": "d1.2", "usage": {"input_tokens": 9, "output_tokens": 0, "cost": 0.000001}, "answers": {
        "q": {"type": "noul", "noul": 0.9}, "where": {"type": "box", "box": {"top": 0.1, "bottom": 0.5, "left": 0.2, "right": 0.6}}}}
    route = respx.post(f"{BASE_URL}/systemone").mock(return_value=httpx.Response(200, json=reply))
    qs = json.dumps({"q": {"type": "boolean", "instructions": "A bug?"}, "where": {"type": "box", "instructions": "the dialog"}})
    bare = tmp_path / "bare"
    bare.mkdir()
    for cwd in (bare, toml.parent):  # no project; a project whose line-up has no liquid
        done = s1flow("decide", "--model", "liquid:d1.2", "--state", '"a crash"', "--questions", qs, cwd=cwd, env={"LIQUID_API_KEY": "k"})
        assert done.returncode == 0, done.stderr
        assert done.stdout.splitlines()[0] == "q: P(true) 0.900"
        assert json.loads(route.calls[-1].request.read())["model"] == "d1.2"
    done = s1flow("decide", "--model", "nope", "--state", '"x"', "--boolean", "?", cwd=bare)
    assert done.returncode == 2 and "no s1flow.toml here" in done.stderr and "provider:id (liquid:d1.2)" in done.stderr
    done = s1flow("decide", "--model", "nope:1", "--state", '"x"', "--boolean", "?", cwd=toml.parent)
    assert done.returncode != 0 and "names: toy, later" in done.stderr and "provider:id" in done.stderr
    done = s1flow("decide", "--model", "liquid:d1.2", "--state", '"x"', "--boolean", "?", "--connections", str(toml), cwd=bare)
    assert done.returncode != 0 and "--connections" in done.stderr and len(route.calls) == 2  # the file lists every model allowed


def test_the_client_loads_no_evaluation_stack(toml):
    """Asking a provider of your own four types in one call loads none of numpy, scipy, sklearn, litellm, dotenv."""
    code = (
        "import sys\n"
        "from s1flow import Client\n"
        "from s1flow.questions import Boolean, Box, Choice, Score\n"
        f"d = Client({str(toml)!r}).responses.create(model='toy', state='a bug', questions={{"
        "'b': Boolean(instructions='?'), 'c': Choice(instructions='?', criteria={'x': None, 'y': None}),"
        "'s': Score(instructions='?', criteria=['a', 'b', 'c']), 'x': Box(instructions='?')})\n"
        "print(sorted(d.answers), sorted(m for m in ('numpy', 'scipy', 'sklearn', 'litellm', 'dotenv', 'PIL') if m in sys.modules))\n"
    )
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True, env={"PYTHONPATH": str(HERE), "PATH": ""}).stdout
    assert out.strip() == "['b', 'c', 's', 'x'] []"


def test_decide_with_a_policy_and_record_feedback(tmp_path, monkeypatch):
    """What the decide Action runs: the policy's model, the outputs, the log; then the feedback a person gives."""
    import shutil

    from s1flow.policies import Policies, PolicySpec
    # Make a runtime-only copy, binding its model through a trusted application connection.
    legacy = json.loads((PROJECT / "policies/gh-ruff-area/v1.json").read_text())
    questions = legacy["questions"]
    spec = PolicySpec(task="gh-ruff-area", version=1, connection="toy", model_id="t1", questions=questions,
                      state_schema={"type": "object", "properties": {"title": {"type": "string"}, "body": {"type": "string"}}, "required": ["title", "body"]})
    store = Policies(tmp_path / "policies")
    ship(store, spec)
    (tmp_path / "s1flow.toml").write_text(TOML)
    models = str(tmp_path / "s1flow.toml")
    out, log = tmp_path / "out.txt", tmp_path / "log.jsonl"
    out.write_text("")
    done = s1flow("decide", "--policy", "gh-ruff-area", "--state", '{"title": "the formatter", "body": "x"}', "--case-id", "#1",
                 "--log", str(log), "--github-output", "--connections", models, cwd=tmp_path, env={"GITHUB_OUTPUT": str(out)})
    assert done.returncode == 0, done.stderr
    outputs = dict(line.split("=", 1) for line in out.read_text().splitlines())
    decision_id = outputs.pop("decision_id")
    assert outputs == {"answer": "formatter", "probability": "0.8000", "below_min_probability": "true", "policy": "gh-ruff-area@v1"}
    assert decision_id == json.loads(log.read_text().splitlines()[0])["decision"]["decision_id"]
    done = s1flow("feedback", "record", "gh-ruff-area", decision_id, "formater", "--log", str(log), cwd=tmp_path)
    assert done.returncode == 2 and "one of: linter, formatter, server, configuration" in done.stderr
    done = s1flow("feedback", "record", "gh-ruff-area", decision_id, "formatter", "--log", str(log), cwd=tmp_path)  # no model: no connections
    assert done.returncode == 0, done.stderr
    assert [json.loads(x)["type"] for x in log.read_text().splitlines()] == ["answered", "feedback"]
    assert json.loads(log.read_text().splitlines()[0])["state"] is None  # not kept unless asked
    state = '{"title": "the formatter", "body": "x"}'
    done = s1flow("decide", "--policy", "gh-ruff-area", "--state", state, "--keep-state", "--connections", models, cwd=tmp_path)
    assert done.returncode == 2 and "--keep-state keeps the state in the log: give --log too" in done.stderr
    done = s1flow("decide", "--policy", "gh-ruff-area", "--state", state, "--case-id", "#2", "--log", str(log), "--keep-state", "--connections", models, cwd=tmp_path)
    assert done.returncode == 0, done.stderr
    assert json.loads(log.read_text().splitlines()[-1])["state"] == json.loads(state)  # what `feedback measure` adds as a case
    app = tmp_path / "app"  # an app that ships one policy file, no policies/: feedback names it as decide does
    app.mkdir()
    shutil.copy(tmp_path / "policies" / "gh-ruff-area" / "v1.json", app / "policy.json")
    second_id = json.loads(log.read_text().splitlines()[-1])["decision"]["decision_id"]
    done = s1flow("feedback", "record", "gh-ruff-area", second_id, "linter", "--log", str(log), "--path", str(app / "policy.json"), cwd=app)
    assert done.returncode == 0, done.stderr
    assert json.loads(log.read_text().splitlines()[-1])["type"] == "feedback"
    done = s1flow("feedback", "record", "gh-ruff-area", second_id, "linter", "--log", str(log), "--path", str(app / "policy.json"), "--connections", models, cwd=app)
    assert done.returncode == 2 and "--connections does not apply to s1flow feedback record" in done.stderr


def test_decide_reads_the_projects_env_file(toml):
    """The base install reads .env without python-dotenv (core/envfile.py): the key reaches the provider."""
    cwd = toml.parent
    toml.write_text(TOML + '[models.keyed]\nprovider = "toy_provider:build"\nid = "t1"\noptions = { key = "TOY_API_KEY" }\n')
    (cwd / ".git").mkdir()
    ask = ("decide", "--model", "keyed", "--state", '"a bug"', "--boolean", "A bug?")
    done = s1flow(*ask, cwd=cwd)
    assert done.returncode == 2 and "TOY_API_KEY is not set" in done.stderr
    (cwd / ".env").write_text("# keys\nexport TOY_API_KEY='k1'  \n")
    done = s1flow(*ask, cwd=cwd)
    assert done.returncode == 0, done.stderr


def test_env_files_are_read_nearest_first_and_never_over_the_environment(tmp_path, monkeypatch):
    from s1flow.core import envfile

    assert envfile.parse('A=1\nexport B = "x\\ny" \nC=plain # note\nD=\'#kept\'\n# E=no\nnot a line\nF=\n') == {
        "A": "1", "B": "x\ny", "C": "plain", "D": "#kept", "F": ""}
    assert envfile.parse('A="a b" # note\nB=\'k#1\' # note\nC="say \\"hi\\" # in" # out\nD="open # note\n') == {
        "A": "a b", "B": "k#1", "C": 'say "hi" # in', "D": '"open'}  # a comment after the closing quote is not the value
    repo = tmp_path / "repo"
    (repo / ".git").mkdir(parents=True)
    (tmp_path / ".env").write_text("S1FLOW_T_D=above the git root\n")
    (repo / ".env").write_text("S1FLOW_T_A=root\nS1FLOW_T_B=root\n")
    (repo / "p").mkdir()
    (repo / "p" / ".env").write_text("S1FLOW_T_A=project\nS1FLOW_T_C=project\n")
    for k in ("S1FLOW_T_A", "S1FLOW_T_B", "S1FLOW_T_D"):
        monkeypatch.setenv(k, "")
        monkeypatch.delenv(k)  # restored (removed) after the test, whatever load sets
    monkeypatch.setenv("S1FLOW_T_C", "set")
    envfile.load(repo / "p")
    assert [os.environ.get(k) for k in ("S1FLOW_T_A", "S1FLOW_T_B", "S1FLOW_T_C", "S1FLOW_T_D")] == ["project", "root", "set", None]


def test_help_on_the_base_install_lists_what_it_runs():
    """Without s1flow[eval] (numpy missing), `s1flow --help` lists decide and feedback; another command names the extra."""
    run = lambda *a: subprocess.run([sys.executable, "-c", "import sys; sys.modules['numpy'] = None; from s1flow.cli import main; main()", *a],
                                    capture_output=True, text=True)
    for args, code in (((), 2), (("--help",), 0)):  # no command is a usage error, its help printed
        done = run(*args)
        assert done.returncode == code and "decide" in done.stdout and "feedback" in done.stdout and "s1flow[eval]" in done.stdout
    done = run("report", "x")
    assert done.returncode == 2 and done.stdout == "" and done.stderr.count("\n") == 1
    assert "needs s1flow[eval]" in done.stderr and "need only s1flow" in done.stderr


def test_a_spec_that_is_not_utf8_is_a_clean_cli_error(tmp_path):
    source = tmp_path / 'invalid.json'
    source.write_bytes(b'\xff\xfeinvalid')
    done = s1flow('adopt', '--spec', str(source), '--validate', '--json', cwd=tmp_path)
    assert done.returncode == 2
    assert 'Traceback' not in done.stderr and 'Traceback' not in done.stdout
    assert 'not a v2 policy' in done.stderr + done.stdout


def test_a_state_is_sent_with_its_keys_sorted_as_its_identity_hashes_it(toml):
    """request_digest treats key order as no difference, so every model receives one order: an evaluation
    case and a production call that differ only in key order send the same bytes."""
    from s1flow.client.identity import request_digest

    class Recorder:
        def __init__(self, inner):
            self.inner, self.sent = inner, []
            self.id, self.concurrency, self.capabilities = inner.id, inner.concurrency, inner.capabilities

        async def decide(self, state, questions, *, options=None):
            self.sent.append(json.dumps(state, ensure_ascii=False))
            return await self.inner.decide(state, questions, options=options)

    client = Client(toml)
    model = Recorder(client.connections.build("toy"))
    a = {"title": "bug", "meta": {"z": 1, "a": [{"y": 2, "b": 3}]}}
    b = {"meta": {"a": [{"b": 3, "y": 2}], "z": 1}, "title": "bug"}
    qs = {"bug": QS["bug"]}
    spec = client.connections.resolved("toy")
    assert request_digest(spec, a, qs) == request_digest(spec, b, qs)
    for state in (a, b):
        client.responses.create(model=model, state=state, questions=qs)
    assert model.sent[0] == model.sent[1] == '{"meta": {"a": [{"b": 3, "y": 2}], "z": 1}, "title": "bug"}'
    assert list(a) == ["title", "meta"]  # the caller's value is not changed


def test_feedback_import_records_every_label_in_a_file_or_none(tmp_path):
    """Labels a person corrected, many at once: a CSV (or JSON Lines) of decision_id and label, checked whole first."""
    from s1flow.policies import Policies, PolicySpec

    legacy = json.loads((PROJECT / "policies/gh-ruff-area/v1.json").read_text())
    spec = PolicySpec(task="gh-ruff-area", version=1, connection="toy", model_id="t1", questions=legacy["questions"])
    ship(Policies(tmp_path / "policies"), spec)
    (tmp_path / "s1flow.toml").write_text(TOML)
    log = tmp_path / "log.jsonl"
    ids = []
    for n in range(3):
        done = s1flow("decide", "--policy", "gh-ruff-area", "--state", f'{{"title": "t{n}", "body": "x"}}', "--log", str(log),
                      "--json", "--connections", str(tmp_path / "s1flow.toml"), cwd=tmp_path)
        assert done.returncode == 0, done.stderr
        ids.append(json.loads(done.stdout)["decision_id"])
    lines = lambda: [json.loads(x) for x in log.read_text().splitlines()]  # noqa: E731
    bad = tmp_path / "bad.csv"
    bad.write_text(f"decision_id,label,note\n{ids[0]},linter,ok\n{ids[1]},formater,typo\n{ids[2]},server,\n{ids[0]},server,again\n")
    done = s1flow("feedback", "import", "gh-ruff-area", str(bad), "--log", str(log), cwd=tmp_path)
    assert done.returncode == 2 and "nothing recorded" in done.stderr
    assert "line 3: gh-ruff-area@v1: label 'formater' is not an answer" in done.stderr
    assert f"line 5: decision {ids[0]} already has the label 'linter'" in done.stderr
    assert [x["type"] for x in lines()] == ["answered"] * 3  # one wrong row, nothing written
    good = tmp_path / "labels.csv"
    good.write_text(f"decision_id,label\n{ids[0]},linter\n{ids[1]},formatter\n{ids[0]},linter\n")
    done = s1flow("feedback", "import", "gh-ruff-area", str(good), "--log", str(log), cwd=tmp_path)
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip() == f"recorded 2 labels for gh-ruff-area@v1 in {log}" and done.stderr == ""
    assert [(x["decision_id"], x["label"]) for x in lines()[3:]] == [(ids[0], "linter"), (ids[1], "formatter")]
    jsonl = tmp_path / "more.jsonl"
    jsonl.write_text(json.dumps({"decision_id": ids[2], "label": "server"}) + "\n\n" + json.dumps({"decision_id": "typo-id", "label": "server"}) + "\n")
    done = s1flow("feedback", "import", "gh-ruff-area", str(jsonl), "--log", str(log), cwd=tmp_path)
    assert done.returncode == 0, done.stderr
    assert "notice: 1 of the 2 decision ids are not in" in done.stderr and "(first: typo-id)" in done.stderr
    # a decision another version made is that version's to label
    other = lines()[0]
    other["decision"]["decision_id"], other["decision"]["policy"] = "by-v2", "gh-ruff-area@v2"
    log.write_text(log.read_text() + json.dumps(other) + "\n")
    jsonl.write_text(json.dumps({"decision_id": "by-v2", "label": "server"}) + "\n")
    done = s1flow("feedback", "import", "gh-ruff-area", str(jsonl), "--log", str(log), cwd=tmp_path)
    assert done.returncode == 2 and "decision by-v2 was made by gh-ruff-area@v2, not gh-ruff-area@v1" in done.stderr
    spread = tmp_path / "spread.csv"  # a quoted note over three lines, and a spreadsheet's trailing empty row
    spread.write_text(f'decision_id,label,note\n{ids[0]},formater,"a\nb\nc"\n,,\n')
    done = s1flow("feedback", "import", "gh-ruff-area", str(spread), "--log", str(log), cwd=tmp_path)
    assert done.returncode == 2 and "line 2: gh-ruff-area@v1: label 'formater'" in done.stderr and "line 5" not in done.stderr
    changed = lines()[0]
    changed["decision"]["decision_id"], changed["decision"]["policy_digest"] = "other-file", "0" * 64
    log.write_text(log.read_text() + json.dumps(changed) + "\n")
    jsonl.write_text(json.dumps({"decision_id": "other-file", "label": "server"}) + "\n")
    done = s1flow("feedback", "import", "gh-ruff-area", str(jsonl), "--log", str(log), cwd=tmp_path)
    assert done.returncode == 2 and "was made by another gh-ruff-area@v1 than this one (its digest differs)" in done.stderr
    elsewhere = tmp_path / "labels-only.jsonl"  # labels sent to a log with no decisions in it: say they can't join yet
    jsonl.write_text(json.dumps({"decision_id": ids[0], "label": "server"}) + "\n")
    done = s1flow("feedback", "import", "gh-ruff-area", str(jsonl), "--log", str(elsewhere), cwd=tmp_path)
    assert done.returncode == 0 and "notice: 1 of the 1 decision ids are not in" in done.stderr
    no_header = tmp_path / "plain.csv"
    no_header.write_text(f"{ids[0]},linter\n")
    done = s1flow("feedback", "import", "gh-ruff-area", str(no_header), "--log", str(log), cwd=tmp_path)
    assert done.returncode == 2 and "the header needs the columns decision_id and label" in done.stderr
    (tmp_path / "empty.csv").write_text("decision_id,label\n")
    done = s1flow("feedback", "import", "gh-ruff-area", str(tmp_path / "empty.csv"), "--log", str(log), cwd=tmp_path)
    assert done.returncode == 2 and "no labels in it" in done.stderr
    (tmp_path / "sjis.csv").write_bytes("decision_id,label,メモ\n".encode("shift_jis"))
    done = s1flow("feedback", "import", "gh-ruff-area", str(tmp_path / "sjis.csv"), "--log", str(log), cwd=tmp_path)
    assert done.returncode == 2 and "not UTF-8 text" in done.stderr


def test_decide_without_a_log_says_nothing_is_recorded(tmp_path):
    from s1flow.policies import Policies, PolicySpec

    legacy = json.loads((PROJECT / "policies/gh-ruff-area/v1.json").read_text())
    ship(Policies(tmp_path / "policies"), PolicySpec(task="gh-ruff-area", version=1, connection="toy", model_id="t1", questions=legacy["questions"]))
    (tmp_path / "s1flow.toml").write_text(TOML)
    done = s1flow("decide", "--policy", "gh-ruff-area", "--state", '{"title": "t", "body": "x"}', "--connections", str(tmp_path / "s1flow.toml"), cwd=tmp_path)
    assert done.returncode == 0, done.stderr
    assert done.stderr == "notice: gh-ruff-area@v1: decisions are not recorded: no log= and no OpenTelemetry tracer provider, so no right answer can be joined to them and production can't be measured; pass log=PATH (decide --log FILE)\n"
