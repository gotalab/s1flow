"""Connection ownership and path resolution are stable across application and CLI contexts."""
from __future__ import annotations

import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from s1flow import AsyncClient, Client, ConfigError, policies
from s1flow.client import ModelSpec
from s1flow.core import place
from s1flow.questions import Boolean

HERE = Path(__file__).parent
QUESTION = {"bug": Boolean(instructions="Is this a bug?")}


def connections(path: Path, model_id: str = "one") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f'default = ["toy"]\n[models.toy]\nprovider = "toy_provider:build"\nid = "{model_id}"\n')
    return path


def cli(*args: str, cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    clean = {k: v for k, v in os.environ.items() if not k.startswith("S1FLOW_")}
    return subprocess.run([sys.executable, "-c", "from s1flow.cli import main; main()", *args], cwd=cwd,
                          env={**clean, "PYTHONPATH": str(HERE), **(env or {})}, capture_output=True, text=True)


@pytest.mark.parametrize("client_type", [Client, AsyncClient])
def test_relative_connections_are_fixed_before_first_read(tmp_path, monkeypatch, client_type):
    connections(tmp_path / "a" / "connections.toml", "a")
    connections(tmp_path / "b" / "connections.toml", "b")
    monkeypatch.chdir(tmp_path / "a")
    client = client_type(connections="connections.toml")
    monkeypatch.chdir(tmp_path / "b")
    assert client.connections.resolved("toy").id == "a"
    assert client.connections.path == tmp_path / "a" / "connections.toml"


def test_sdk_does_not_discover_connections_or_read_env_files(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.syspath_prepend(str(HERE))
    connections(tmp_path / "s1flow.toml")
    monkeypatch.setenv("S1FLOW_CONNECTIONS", str(tmp_path / "s1flow.toml"))
    (tmp_path / ".env").write_text("S1FLOW_CONNECTIONS=unrelated.toml\n")
    monkeypatch.setattr(place, "find", lambda *args, **kwargs: pytest.fail("SDK searched for a project"))
    for client in [Client(), AsyncClient()]:
        with pytest.raises(ConfigError, match="connections="):
            client.connections.resolved("toy")
        response = client.responses.create(model=ModelSpec(provider="toy_provider:build", id="direct"),
                                           state="bug", questions=QUESTION)
        if isinstance(client, AsyncClient):
            response = asyncio.run(response)
        assert response.answered_by == "toy:direct-1"


def test_sdk_policy_requires_an_explicit_location(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    connections(tmp_path / "s1flow.toml")
    with pytest.raises(ConfigError, match="path=.*root="):
        policies.load("ticket", client=Client(connections=tmp_path / "s1flow.toml"))


def test_missing_connection_file_names_absolute_location_and_remedy(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with pytest.raises(ConfigError) as error:
        Client(connections="missing.toml").connections.list()
    assert str(tmp_path / "missing.toml") in str(error.value)
    assert "connections" in str(error.value)


def test_loaded_policy_and_log_keep_their_application_paths(tmp_path, monkeypatch):
    from test_runtime import client as fake_client, policy as specification

    a, b = tmp_path / "a", tmp_path / "b"
    a.mkdir(); b.mkdir()
    store = policies.Policies(a / "policies")
    store.write_new(specification())
    client, calls = fake_client(monkeypatch)
    monkeypatch.chdir(a)
    runtime = policies.load("ticket@v1", root=Path("policies"), client=client, log="logs/decisions.jsonl")
    monkeypatch.chdir(b)
    decision = runtime.decide("bug")
    runtime.feedback(decision.decision_id, True)
    records = [json.loads(line) for line in (a / "logs/decisions.jsonl").read_text().splitlines()]
    assert [r["type"] for r in records] == ["answered", "feedback"]
    assert not (b / "logs").exists()
    assert len(calls) == 2


def test_provider_cache_path_is_fixed_before_model_construction(tmp_path, monkeypatch):
    from s1flow.client import _client
    from toy_provider import build
    from s1flow.client.models import ModelBuild

    a, b = tmp_path / "a", tmp_path / "b"
    a.mkdir(); b.mkdir()
    seen = []

    def build_one(name, spec, cache_dir):
        seen.append(cache_dir)
        return build(ModelBuild(name, spec, cache_dir))

    monkeypatch.setattr(_client, "build_one", build_one)
    monkeypatch.chdir(a)
    client = Client(cache_dir=Path("cache"))
    monkeypatch.chdir(b)
    client.responses.create(model=ModelSpec(provider="toy_provider:build", id="direct"), state="bug", questions=QUESTION)
    assert seen == [a / "cache"]


def test_model_passed_to_connections_has_an_actionable_error():
    with pytest.raises(ConfigError, match=r"responses.create\(model="):
        Client(connections=ModelSpec(provider="typesafe", id="direct"))


def test_invalid_path_is_a_setup_error():
    with pytest.raises(ConfigError, match="cannot resolve connections path"):
        Client(connections="bad\x00.toml")


def test_project_search_stops_at_git_boundary(tmp_path):
    connections(tmp_path / "s1flow.toml", "outside")
    repository = tmp_path / "repository"
    (repository / ".git").mkdir(parents=True)
    nested = repository / "src" / "feature"
    nested.mkdir(parents=True)
    assert place.root(nested) is None
    connections(repository / "s1flow" / "s1flow.toml", "inside")
    assert place.root(nested) == repository / "s1flow"


def test_without_git_discovery_does_not_take_parent_settings(tmp_path):
    connections(tmp_path / "s1flow.toml")
    child = tmp_path / "another-app"
    child.mkdir()
    assert place.root(child) is None


@pytest.mark.parametrize("prefix", [True, False])
def test_cli_explicit_project_and_relative_connection_path(tmp_path, prefix):
    project = tmp_path / "repository" / "s1flow"
    connections(project / "s1flow.toml", "project")
    config = connections(tmp_path / "chosen.toml", "chosen")
    flags = ["--project", str(project.parent), "--connections", config.name]
    command = ["decide", "--model", "toy", "--boolean", "Is this a bug?", "--state", '"bug"', "--json"]
    done = cli(*(flags + command if prefix else command + flags), cwd=tmp_path)
    assert done.returncode == 0, done.stderr
    assert json.loads(done.stdout)["answered_by"] == "toy:chosen-1"


def test_missing_project_error_has_search_location_and_next_step(tmp_path):
    (tmp_path / ".git").mkdir()
    done = cli("tasks", cwd=tmp_path)
    assert done.returncode == 2 and "Traceback" not in done.stderr
    assert str(tmp_path) in done.stderr and "--project" in done.stderr and "s1flow init" in done.stderr


def test_cli_connections_environment_is_supported_but_explicit_path_wins(tmp_path):
    first = connections(tmp_path / "first.toml", "first")
    second = connections(tmp_path / "second.toml", "second")
    command = ["decide", "--model", "toy", "--boolean", "Is this a bug?", "--state", '"bug"', "--json"]
    env = {"S1FLOW_CONNECTIONS": str(first)}
    done = cli(*command, cwd=tmp_path, env=env)
    assert done.returncode == 0, done.stderr
    assert json.loads(done.stdout)["answered_by"] == "toy:first-1"
    done = cli(*command, "--connections", str(second), cwd=tmp_path, env=env)
    assert done.returncode == 0, done.stderr
    assert json.loads(done.stdout)["answered_by"] == "toy:second-1"


def test_nested_cli_options_and_missing_policy_authorization(tmp_path):
    from test_runtime import policy as specification

    config = connections(tmp_path / "s1flow.toml")
    source = tmp_path / "policy.json"
    source.write_text(specification().dump())
    # A connection grant before a nested subcommand is retained, and binding errors stay readable.
    done = cli("--connections", str(config), "policy", "create", str(source), "--check", cwd=tmp_path)
    assert done.returncode == 2 and "unknown connection 'trusted'" in done.stderr
    assert "toy" in done.stderr and str(config) in done.stderr and "Traceback" not in done.stderr
    done = cli("decide", "--policy", "ticket@v1", "--path", str(source), "--state", '"bug"',
               cwd=tmp_path, env={"S1FLOW_CONNECTIONS": str(config)})
    assert done.returncode == 2 and "needs --connections PATH" in done.stderr


def test_explicit_missing_project_never_falls_back(tmp_path):
    connections(tmp_path / "s1flow.toml")
    missing = tmp_path / "wrong"
    done = cli("tasks", "--project", str(missing), cwd=tmp_path)
    assert done.returncode == 2 and str(missing) in done.stderr and "--project" in done.stderr


def test_old_cli_names_explain_the_replacement(tmp_path):
    done = cli("decide", "--models-file", "connections.toml", cwd=tmp_path)
    assert done.returncode == 2 and "--connections" in done.stderr


def test_adoption_identity_comes_from_selected_repository(tmp_path, monkeypatch):
    from s1flow.integrations import git

    a, b = tmp_path / "a", tmp_path / "b"
    for directory, name in [(a, "Application A"), (b, "Application B")]:
        subprocess.run(["git", "init", "-q", str(directory)], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(directory), "config", "user.name", name], check=True)
    monkeypatch.chdir(b)
    assert git.user(a) == "Application A"


def test_invalid_encoding_in_connection_file_is_a_setup_error(tmp_path):
    config = tmp_path / "connections.toml"
    config.write_bytes(b"\xff")
    done = cli("doctor", "--connections", str(config), cwd=tmp_path)
    assert done.returncode == 2 and "Traceback" not in done.stderr
    assert str(config) in done.stderr and "--connections" in done.stderr


@pytest.mark.parametrize("contents, hint", [(b"\xff", "UTF-8"), (b"BROKEN=a\x00b", "NUL")])
def test_invalid_dotenv_is_a_readable_setup_error(tmp_path, contents, hint):
    connections(tmp_path / "s1flow.toml")
    dotenv = tmp_path / ".env"
    dotenv.write_bytes(contents)
    done = cli("doctor", cwd=tmp_path)
    assert done.returncode == 2 and "Traceback" not in done.stderr
    assert str(dotenv) in done.stderr and hint in done.stderr


def test_supplied_lineup_uses_each_clients_fixed_cache_path(tmp_path, monkeypatch):
    from s1flow.client import lineup as connection_files
    from s1flow.client import providers
    from toy_provider import build

    a, b = tmp_path / "a", tmp_path / "b"
    a.mkdir(); b.mkdir()
    seen = []

    def factory(request):
        seen.append(request.cache_dir)
        return build(request)

    monkeypatch.setattr(providers, "build_model", factory)
    supplied = connection_files.Lineup(default=["toy"], models={"toy": ModelSpec(provider="toy_provider:build", id="one")})
    monkeypatch.chdir(a)
    first = Client(connections=supplied, cache_dir=Path("cache"))
    monkeypatch.chdir(b)
    second = Client(connections=supplied, cache_dir=Path("cache"))
    for client in [first, second]:
        client.responses.create(model="toy", state="bug", questions=QUESTION)
    first.connections.check()
    assert seen == [a / "cache", b / "cache", a / "cache"]
    assert supplied.models["toy"].id == "one"  # the caller's declaration is unchanged


def test_preloaded_lineup_is_data_and_client_alone_selects_cache(tmp_path, monkeypatch):
    from s1flow.client import lineup as connection_files
    from s1flow.client import providers
    from toy_provider import build

    a, b = tmp_path / "a", tmp_path / "b"
    config = connections(a / "connections.toml")
    b.mkdir()
    seen = []

    def factory(request):
        seen.append(request.cache_dir)
        return build(request)

    monkeypatch.setattr(providers, "build_model", factory)
    monkeypatch.chdir(a)
    supplied = connection_files.Lineup.read(config)
    monkeypatch.chdir(b)
    for client in [Client(connections=supplied), Client(connections=supplied, cache_dir=Path("override-cache"))]:
        client.responses.create(model="toy", state="bug", questions=QUESTION)
    assert seen == [None, b / "override-cache"]
    assert supplied.models["toy"].id == "one"



def test_an_app_without_a_project_adopts_and_rolls_back_with_root(tmp_path):
    from test_runtime import policy as specification

    app = tmp_path / "app"
    config = app / "connections.toml"
    config.parent.mkdir()
    config.write_text('default = []\n[models.trusted]\nprovider = "toy_provider:build"\nid = "fixed-v1"\n')
    git = {"GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "user.name", "GIT_CONFIG_VALUE_0": "App owner"}
    for v in (1, 2):
        (app / f"v{v}.json").write_text(specification(version=v).dump())
        done = cli("adopt", "--spec", f"v{v}.json", "--root", "policies", "--connections", "connections.toml", "--reason", f"rule {v}", cwd=app, env=git)
        assert done.returncode == 0, done.stderr
    done = cli("adopt", "ticket@v1", "--root", "policies", "--reason", "back", cwd=app, env=git)
    assert done.returncode == 0, done.stderr
    store = policies.Policies(app / "policies")
    assert store.current("ticket") == 1 and [(h.action, h.version, h.by) for h in store.history("ticket")] == [
        ("spec", 1, "App owner"), ("spec", 2, "App owner"), ("rollback", 1, "App owner")]
    for reason in ("", "  "):
        done = cli("adopt", "ticket@v2", "--root", "policies", "--reason", reason, cwd=app, env=git)
        assert done.returncode == 2 and "give --reason a sentence" in done.stderr and "Traceback" not in done.stderr


def test_a_switch_refused_for_a_stale_current_writes_nothing(tmp_path):
    from test_runtime import policy as specification
    from s1flow.policies.history import Switch

    store = policies.Policies(tmp_path)
    store.write_new(specification(), adopted=Switch(action="spec", version=1, previous=None, by="t", reason="t"))
    with pytest.raises(ConfigError, match="current changed while adopting"):
        store.write_new(specification(version=2), adopted=Switch(action="spec", version=2, previous=None, by="t", reason="t"))
    assert store.versions("ticket") == [1] and len(store.history("ticket")) == 1  # adopting again can still save v2
