"""The base install is the client and policies alone: what an extra would have installed is named when missing."""

import subprocess
import sys
from pathlib import Path
from textwrap import dedent


def run(code: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)


def test_the_cli_without_eval_says_what_to_install():
    done = run("import sys; sys.modules['numpy'] = None; sys.argv = ['s1flow', 'report', 'x']; from s1flow.cli import main; main()")
    assert done.returncode == 2 and done.stdout == ""
    assert done.stderr.count("\n") == 1 and "s1flow[eval]" in done.stderr


def test_an_llm_model_without_litellm_is_a_config_error():
    done = run(
        "import sys; sys.modules['litellm'] = None\n"
        "from s1flow.core.errors import ConfigError\n"
        "from s1flow.client import ModelSpec\n"
        "from s1flow.client.providers import build_one\n"
        "try:\n"
        "    build_one('m', ModelSpec(provider='llm', id='openai/gpt-5-mini'))\n"
        "except ConfigError as e:\n"
        "    print(e)\n"
    )
    assert done.returncode == 0, done.stderr
    assert done.stdout.splitlines() == ["the llm provider needs LiteLLM: install s1flow[llm]"]


def test_decision_model_providers_build_without_litellm():
    done = run(
        "import sys; sys.modules['litellm'] = sys.modules['numpy'] = None\n"
        "from s1flow.client import ModelSpec\n"
        "from s1flow.client.providers import build_one\n"
        "for p, m in [('typesafe', 'jev'), ('gateway', 'd1'), ('openrouter', 'clef'), ('cloudflare', 'kev'), ('openai-decisions', 'gpt-5-mini')]:\n"
        "    build_one('m', ModelSpec(provider=p, id=m))\n"
        "print('ok')\n"
    )
    assert done.returncode == 0 and done.stdout.strip() == "ok", done.stderr


def test_runtime_calls_and_logs_without_a_project_or_evaluation(tmp_path):
    """Both runtime entry points work even when evaluation and every extra are unavailable."""
    code = dedent('''\
        import importlib.abc
        import json
        import sys
        from pathlib import Path

        forbidden = ("s1flow.eval", "s1flow.project", "numpy", "scipy", "sklearn", "litellm", "gepa", "PIL", "opentelemetry")
        class NoExtras(importlib.abc.MetaPathFinder):
            def find_spec(self, fullname, path=None, target=None):
                if any(fullname == p or fullname.startswith(p + ".") for p in forbidden):
                    raise ModuleNotFoundError(fullname, name=fullname)
        sys.meta_path.insert(0, NoExtras())
        sys.path.insert(0, sys.argv[1])

        from s1flow import Client, policies
        from s1flow.client import ModelSpec
        from s1flow.client.lineup import Lineup
        from s1flow.questions import Boolean

        model = ModelSpec(provider="toy_provider:build", id="standalone")
        question = Boolean(instructions="Is this a bug?")
        client = Client(connections=Lineup(default=[], models={"standalone": model}))
        result = client.responses.create(model=model, state="a bug", questions={"bug": question})
        assert result.answers["bug"].probability == 0.9

        file = policies.PolicySpec(
            s1flow_version="0.1.0", task="bug", version=1, at="2026-10-24",
            connection="standalone", model_id=model.id,
            questions={"bug": policies.asked(question, policies.DecisionRule(threshold=0.5))},
            state_schema={"type": "string"},
        )
        assert "evidence" not in file.model_dump() and "selection" not in file.model_dump()
        Path("policy.json").write_text(file.dump())
        runtime = policies.load(path="policy.json", client=client, log="decisions.jsonl", keep_state=True)
        decision = runtime.decide("a bug", case_id="ticket-1")
        assert decision.value is True and not decision.below_min_probability
        runtime.feedback(decision.decision_id, True)
        logs = [json.loads(line) for line in Path("decisions.jsonl").read_text().splitlines()]
        assert [row["type"] for row in logs] == ["answered", "feedback"]
        assert logs[0]["state"] == "a bug"
        assert not any(name == p or name.startswith(p + ".") for name in sys.modules for p in forbidden)
        print("standalone runtime ok")
    ''')
    done = subprocess.run(
        [sys.executable, "-c", code, str(Path(__file__).parent.resolve())],
        cwd=tmp_path, capture_output=True, text=True,
    )
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip() == "standalone runtime ok"
