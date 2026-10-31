"""The model-calling layer (s1flow.client): Client, AsyncClient, decisions.create, the line-up; the base-install CLI."""

import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
from conftest import PROJECT, ship

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


@pytest.mark.parametrize(
    ("qid", "question", "answer_kind", "detail"),
    [
        ("bug", QS["bug"], "probability", "probability"),
        ("bug", QS["bug"], "nan_probability", "probability"),
        ("area", QS["area"], "choice", "option"),
        ("area", QS["area"], "distribution", "probability"),
        ("area", QS["area"], "type", "type"),
    ],
)
def test_a_provider_answer_stays_inside_the_question_contract(toml, qid, question, answer_kind, detail):
    from s1flow.client import BooleanAnswer, ChoiceAnswer, Response

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


# ---------- the base-install CLI ----------


def s1flow(*args, cwd, env=None):
    import os

    e = {k: v for k, v in os.environ.items() if not k.startswith("S1FLOW_")} | {"PYTHONPATH": str(HERE)} | (env or {})
    return subprocess.run([sys.executable, "-c", "from s1flow.cli import main; main()", *args], cwd=cwd, capture_output=True, text=True, env=e)


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
    done = s1flow("feedback", "record", "gh-ruff-area", decision_id, "formater", "--log", str(log), "--connections", models, cwd=tmp_path)
    assert done.returncode == 2 and "one of: linter, formatter, server, configuration" in done.stderr
    done = s1flow("feedback", "record", "gh-ruff-area", decision_id, "formatter", "--log", str(log), "--connections", models, cwd=tmp_path)
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
    done = s1flow("feedback", "record", "gh-ruff-area", second_id, "linter", "--log", str(log), "--path", str(app / "policy.json"), "--connections", models, cwd=app)
    assert done.returncode == 0, done.stderr
    assert json.loads(log.read_text().splitlines()[-1])["type"] == "feedback"


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
    assert done.returncode == 2 and "needs s1flow[eval]" in done.stderr and "need only s1flow" in done.stderr


@pytest.mark.parametrize('answered_by', ['', ' \t\n'])
def test_blank_answering_model_is_a_provider_failure(toml, answered_by):
    from s1flow.client import BooleanAnswer, Response

    class BlankIdentity:
        id, concurrency = 'blank', 1
        capabilities = Client(toml).connections.build('toy').capabilities
        async def decide(self, state, questions, *, options=None):
            return Response(answers={'bug': BooleanAnswer(probability=.9)}, answered_by=answered_by)
    with pytest.raises(ProviderError, match='answered_by'):
        Client(toml).responses.create(model=BlankIdentity(), state='bug', questions={'bug': QS['bug']})


def test_policy_validate_invalid_utf8_is_clean_cli_error(tmp_path):
    source = tmp_path / 'invalid.json'
    source.write_bytes(b'\xff\xfeinvalid')
    done = s1flow('adopt', '--spec', str(source), '--check', '--json', cwd=tmp_path)
    assert done.returncode == 2
    assert 'Traceback' not in done.stderr and 'Traceback' not in done.stdout
    assert 'not a v2 policy' in done.stderr + done.stdout
