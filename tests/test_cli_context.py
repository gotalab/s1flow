"""Configuration options are advertised and accepted only where they affect the command."""
from __future__ import annotations

from pathlib import Path

import pytest

from test_connections import cli

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("command, option", [
    (["policy", "create", str(ROOT / "schema/fixtures/policy-2.valid.json"), "--check"], "--project"),
    (["policy", "create", str(ROOT / "schema/fixtures/policy-2.valid.json")], "--project"),
    (["policy", "export"], "--connections"),
    (["init", "new-project"], "--project"),
    (["guide", "cli"], "--connections"),
    (["skill", "path"], "--project"),
    (["cases", "check", "ticket"], "--connections"),
    (["cases", "correct", "ticket", "case-1", "--verdict", "keep", "--reason", "checked"], "--connections"),
])
@pytest.mark.parametrize("prefix", [False, True])
def test_unused_context_options_fail_before_work(tmp_path, command, option, prefix):
    flags = [option, str(tmp_path / "unused")]
    done = cli(*(flags + command if prefix else command + flags), cwd=tmp_path)
    assert done.returncode == 2 and "Traceback" not in done.stderr
    assert option in done.stderr and "does not apply" in done.stderr
    assert not list(tmp_path.iterdir())


@pytest.mark.parametrize("words, expected", [
    (["policy", "create"], {"--connections"}),
    (["policy", "export"], {"--project"}),
    (["cases", "check"], {"--project"}),
    (["cases", "review"], {"--project", "--connections"}),
    (["decide"], {"--project", "--connections"}),
    (["init"], set()),
    (["guide"], set()),
])
def test_help_shows_only_effective_configuration_options(tmp_path, words, expected):
    done = cli(*words, "--help", cwd=tmp_path)
    assert done.returncode == 0
    for option in ["--project", "--connections"]:
        assert (option in done.stdout) == (option in expected)


@pytest.mark.parametrize("option", ["--project", "--connections"])
def test_offline_comparison_rejects_live_configuration(tmp_path, option):
    snapshot = ROOT / "schema/fixtures/comparison-2.valid.json"
    done = cli("report", "--from", str(snapshot), option, str(tmp_path / "unused"), "--json", cwd=tmp_path)
    assert done.returncode == 2 and "--from" in done.stderr and option in done.stderr
    assert "does not apply" in done.stderr and "Traceback" not in done.stderr


def test_group_prefix_does_not_bypass_leaf_option_scope(tmp_path):
    policy = ROOT / "schema/fixtures/policy-2.valid.json"
    done = cli("policy", "--project", str(tmp_path), "create", str(policy), "--check", cwd=tmp_path)
    assert done.returncode == 2 and "--project does not apply" in done.stderr


