"""Configuration options are advertised and accepted only where they affect the command."""
from __future__ import annotations

from pathlib import Path

import pytest

from conftest import s1flow

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("command, option", [
    (["export"], "--connections"),
    (["init", "new-project"], "--project"),
    (["cases", "check", "ticket"], "--connections"),
    (["cases", "correct", "ticket", "case-1", "--verdict", "keep", "--reason", "checked"], "--connections"),
])
@pytest.mark.parametrize("prefix", [False, True])
def test_unused_context_options_fail_before_work(tmp_path, command, option, prefix):
    flags = [option, str(tmp_path / "unused")]
    done = s1flow(*(flags + command if prefix else command + flags), cwd=tmp_path)
    assert done.returncode == 2 and "Traceback" not in done.stderr
    assert option in done.stderr and "does not apply" in done.stderr
    assert not list(tmp_path.iterdir())


@pytest.mark.parametrize("words, expected", [
    (["export"], {"--project"}),
    (["adopt"], {"--project", "--connections"}),
    (["cases", "check"], {"--project"}),
    (["cases", "review"], {"--project", "--connections"}),
    (["decide"], {"--project", "--connections"}),
    (["init"], set()),
])
def test_help_shows_only_effective_configuration_options(tmp_path, words, expected):
    done = s1flow(*words, "--help", cwd=tmp_path)
    assert done.returncode == 0
    for option in ["--project", "--connections"]:
        assert (option in done.stdout) == (option in expected)


@pytest.mark.parametrize("option", ["--project", "--connections"])
def test_offline_comparison_rejects_live_configuration(tmp_path, option):
    snapshot = ROOT / "schema/fixtures/comparison-2.valid.json"
    done = s1flow("report", "--from", str(snapshot), option, str(tmp_path / "unused"), "--json", cwd=tmp_path)
    assert done.returncode == 2 and "--from" in done.stderr and option in done.stderr
    assert "does not apply" in done.stderr and "Traceback" not in done.stderr


def test_group_prefix_does_not_bypass_leaf_option_scope(tmp_path):
    done = s1flow("cases", "--connections", str(tmp_path / "c.toml"), "check", "ticket", cwd=tmp_path)
    assert done.returncode == 2 and "--connections does not apply" in done.stderr


