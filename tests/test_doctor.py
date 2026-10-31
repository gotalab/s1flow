"""What each provider declares it needs (keys, hosts), and `s1flow doctor`, which checks it on the base install."""

import json
from conftest import ship
import os
import subprocess
import sys
from pathlib import Path

import httpx
import pytest

from s1flow import doctor
from s1flow.client import ModelSpec, Needs
from s1flow.client.providers import needs
from s1flow.core.errors import ConfigError

HERE = Path(__file__).parent
KEYS = ("TYPESAFE_API_KEY", "AI_GATEWAY_API_KEY", "OPENROUTER_API_KEY", "OPENAI_API_KEY", "MY_KEY", "CLEF_RELAY_URL")
DECLARED = '''from s1flow.client import Needs, declares


def needs(spec):
    return Needs(keys=("MY_KEY",), hosts=("https://api.example.com",))


@declares(needs)
def build(b):
    raise AssertionError("doctor builds nothing")
'''
TOML = """default = ["jev", "d1@vercel"]
[models.jev]
provider = "typesafe"
id = "jev-latest"
[models."d1@vercel"]
provider = "gateway"
id = "liquid/d1"
[models.toy]
provider = "toy_provider:build"
id = "t1"
[models.mine]
provider = "my_provider:build"
id = "m1"
[models.nope]
provider = "no_such_module:build"
id = "x"
[models.flash]
provider = "llm"
id = "vercel_ai_gateway/google/gemini-3.1-flash-lite"
"""


def spec(provider: str, model: str = "m", **options) -> ModelSpec:
    return ModelSpec(provider=provider, id=model, options=options)


# ---------- the declarations ----------


def test_each_built_in_provider_declares_its_keys_and_hosts(monkeypatch):
    monkeypatch.delenv("CLEF_RELAY_URL", raising=False)
    assert needs(spec("typesafe")) == Needs(keys=("TYPESAFE_API_KEY",), hosts=("https://api.typesafe.ai",))
    assert needs(spec("typesafe", base_url="http://my.host:9000/v1", api_key_env="MINE")) == Needs(keys=("MINE",), hosts=("http://my.host:9000",))
    assert needs(spec("gateway")) == Needs(keys=("AI_GATEWAY_API_KEY",), hosts=("https://ai-gateway.vercel.sh",))
    assert needs(spec("openrouter")) == Needs(keys=("OPENROUTER_API_KEY",), hosts=("https://openrouter.ai",))
    assert needs(spec("openai-decisions")) == Needs(keys=("OPENAI_API_KEY",), hosts=("https://api.openai.com",))
    clef = needs(spec("cloudflare", "clef"))
    assert clef is not None and clef.keys == () and clef.hosts == ("http://localhost:8788",) and "wrangler" in clef.note
    monkeypatch.setenv("CLEF_RELAY_URL", "https://relay.example.com/x")
    assert needs(spec("cloudflare", "clef")).hosts == ("https://relay.example.com",)


def test_an_llm_declares_its_litellm_provider():
    gw = Needs(keys=("AI_GATEWAY_API_KEY",), hosts=("https://ai-gateway.vercel.sh",), packages=("litellm",))
    assert needs(spec("llm", "vercel_ai_gateway/anthropic/claude-haiku-4.5", box_units="pixels")) == gw
    assert needs(spec("llm", "anthropic/claude-haiku-4.5")).keys == ("ANTHROPIC_API_KEY",)
    assert needs(spec("llm", "gpt-5-mini")).hosts == ("https://api.openai.com",)  # a bare id is OpenAI's
    assert needs(spec("llm", "openai/gpt-5-mini", api_key_env="MINE")).keys == ("MINE",)
    unknown = needs(spec("llm", "bedrock/some-model"))
    assert unknown.keys == () and unknown.hosts == () and "not known" in unknown.note


def test_a_declaration_reads_the_spec_alone():
    with pytest.raises(ConfigError, match="options do not fit"):
        needs(spec("typesafe", base_url="x", typo=1))
    with pytest.raises(ConfigError, match="unknown provider"):
        needs(spec("nope"))


def test_a_provider_of_your_own_declares_or_not(tmp_path, monkeypatch):
    (tmp_path / "my_provider.py").write_text(DECLARED)
    monkeypatch.syspath_prepend(str(tmp_path))
    monkeypatch.syspath_prepend(str(HERE))
    assert needs(spec("my_provider:build")) == Needs(keys=("MY_KEY",), hosts=("https://api.example.com",))
    assert needs(spec("toy_provider:build")) is None  # declares nothing


def test_declarations_read_without_litellm():
    code = (
        "import sys; sys.modules['litellm'] = None\n"
        "from s1flow.client import ModelSpec\n"
        "from s1flow.client.providers import needs\n"
        "print(needs(ModelSpec(provider='llm', id='openai/gpt-5-mini')).keys)\n"
    )
    done = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    assert done.returncode == 0 and done.stdout.strip() == "('OPENAI_API_KEY',)", done.stderr


# ---------- reaching the hosts ----------


def test_reach_counts_any_answer_and_asks_each_host_once(monkeypatch):
    asked: list[str] = []

    def get(url, timeout):
        asked.append(url)
        if "typesafe" in url:
            raise httpx.ConnectError("blocked")
        return httpx.Response(404)

    monkeypatch.setattr(doctor.httpx, "get", get)
    models = [("jev", spec("typesafe")), ("d1", spec("gateway")), ("laya", spec("gateway"))]
    r = doctor.check("s1flow.toml", models, env={"TYPESAFE_API_KEY": "k", "AI_GATEWAY_API_KEY": "k"}, probe=True)
    assert sorted(asked) == ["https://ai-gateway.vercel.sh", "https://api.typesafe.ai"]
    assert r.problems == ["api.typesafe.ai is unreachable (jev): ConnectError: blocked"]
    assert r.models[1].hosts[0].status == 404


# ---------- the command ----------


def s1flow(*args, cwd, env=None):
    base = {k: v for k, v in os.environ.items() if not k.startswith("S1FLOW_") and k not in KEYS}
    path = os.pathsep.join([str(HERE), str(cwd)])
    return subprocess.run([sys.executable, "-c", "from s1flow.cli import main; main()", *args], cwd=cwd, capture_output=True, text=True,
                          env=base | {"PYTHONPATH": path} | (env or {}))


@pytest.fixture
def project(tmp_path):
    (tmp_path / "s1flow.toml").write_text(TOML)
    (tmp_path / "my_provider.py").write_text(DECLARED)
    return tmp_path


def test_doctor_names_what_is_missing_and_never_a_value(project):
    done = s1flow("doctor", cwd=project, env={"TYPESAFE_API_KEY": "zq-value-xyz"})
    assert done.returncode == 1
    assert done.stderr.splitlines() == ["problem: AI_GATEWAY_API_KEY is not set (d1@vercel): get one at https://vercel.com/docs/ai-gateway/authentication-and-byok/api-keys"]
    assert "TYPESAFE_API_KEY  set" in done.stdout and "AI_GATEWAY_API_KEY  NOT SET (get one at https://vercel.com/docs/ai-gateway/authentication-and-byok/api-keys)" in done.stdout
    assert "allow-list: ai-gateway.vercel.sh, api.typesafe.ai" in done.stdout
    assert "zq-value" not in done.stdout + done.stderr

    done = s1flow("doctor", "--json", cwd=project, env={"TYPESAFE_API_KEY": "zq-value-xyz", "AI_GATEWAY_API_KEY": "k"})
    assert done.returncode == 0, done.stdout + done.stderr
    report = json.loads(done.stdout)
    assert report["ok"] and report["keys"] == ["AI_GATEWAY_API_KEY", "TYPESAFE_API_KEY"]
    assert report["models"][0]["keys"] == {"TYPESAFE_API_KEY": "environment"}


def test_a_dotenv_fills_in_and_never_overrides(project):
    (project / ".env").write_text("TYPESAFE_API_KEY=from-dotenv\nAI_GATEWAY_API_KEY=from-dotenv\n")
    done = s1flow("doctor", "--json", cwd=project, env={"TYPESAFE_API_KEY": "set"})
    assert done.returncode == 0, done.stderr
    keys = {k: v for m in json.loads(done.stdout)["models"] for k, v in m["keys"].items()}
    assert keys == {"TYPESAFE_API_KEY": "environment", "AI_GATEWAY_API_KEY": ".env"}


def test_doctor_on_named_models(project):
    done = s1flow("doctor", "--models", "toy,mine", cwd=project)
    assert done.returncode == 1 and done.stderr.splitlines() == ["problem: MY_KEY is not set (mine)"]
    assert "provider toy_provider:build declares no keys or hosts: doctor cannot check them" in done.stdout
    assert s1flow("doctor", "--models", "toy", cwd=project).returncode == 0  # nothing declared, nothing missing

    done = s1flow("doctor", "--models", "nope", cwd=project)
    assert done.returncode == 1 and done.stderr.startswith("problem: nope: cannot load provider 'no_such_module:build'")


def test_doctor_on_a_policy(project):
    sys.path.insert(0, str(HERE))
    try:
        from test_policy import policy
    finally:
        sys.path.remove(str(HERE))
    from s1flow.eval.policy import Store

    store = Store(project / "policies")
    r = policy(task="t")
    ship(store, r.model_copy(update={"spec": r.spec.model_copy(update={"model_id": "jaredpalmer/kev-4b"})}))
    with (project / "s1flow.toml").open("a") as f:
        f.write('\n[models.fake]\nprovider = "openrouter"\nid = "jaredpalmer/kev-4b"\n')
    done = s1flow("doctor", "--policy", "t", "--connections", str(project / "s1flow.toml"), cwd=project)
    assert done.returncode == 1 and done.stderr.splitlines() == ["problem: OPENROUTER_API_KEY is not set (fake): get one at https://openrouter.ai/keys"]
    assert done.stdout.startswith("policy t@v1")


def test_doctor_runs_on_the_base_install(project):
    code = ("import sys\nfor m in ('numpy', 'scipy', 'sklearn', 'litellm', 'PIL'): sys.modules[m] = None\n"
            "sys.argv = ['s1flow', 'doctor', '--models', 'jev,flash']\nfrom s1flow.cli import main; main()")
    env = {k: v for k, v in os.environ.items() if not k.startswith("S1FLOW_") and k not in KEYS} | {"TYPESAFE_API_KEY": "k", "AI_GATEWAY_API_KEY": "k"}
    done = subprocess.run([sys.executable, "-c", code], cwd=project, capture_output=True, text=True, env=env)
    assert done.returncode == 1, done.stderr
    assert done.stderr.splitlines() == ["problem: flash needs litellm: install s1flow[llm]"]


def test_doctor_names_a_project_skill_an_older_s1flow_wrote(project, monkeypatch):
    """What skill.stale says (test_skill pins its text), one `skill:` line each."""
    from s1flow import skill

    (project / ".git").mkdir()
    copy = project / ".claude" / "skills" / "s1flow"
    copy.mkdir(parents=True)
    (copy / skill.MARKER).write_text(json.dumps({"schema": "s1flow/skill-marker@1", "s1flow_version": "0.0.1", "files": {}}))
    monkeypatch.chdir(project)
    stale = skill.stale()
    done = s1flow("doctor", "--models", "toy", cwd=project)
    assert done.returncode == 0 and stale
    assert [line for line in done.stdout.splitlines() if line.startswith("skill: ")] == [f"skill: {line}" for line in stale]
    assert json.loads(s1flow("doctor", "--models", "toy", "--json", cwd=project).stdout)["skill"] == stale


def test_a_missing_key_says_where_to_get_it():
    from s1flow.client.providers.needs import how_to_set

    assert how_to_set("OPENROUTER_API_KEY") == ("get one at https://openrouter.ai/keys, then set it in the environment or in a .env "
                                                "in the project or above it (s1flow doctor lists what each model needs)")
    assert how_to_set("MY_KEY").startswith("set it in the environment")
