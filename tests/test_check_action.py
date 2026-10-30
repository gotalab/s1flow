"""The `s1flow check` Action's step (action.yml), run with stand-ins for `gh` and the s1flow CLI."""

import json
import os
import shlex
import shutil
import subprocess
from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml")  # a dependency of the eval extra's, not s1flow's own

ROOT = Path(__file__).resolve().parents[1]
pytestmark = pytest.mark.skipif(shutil.which("jq") is None or shutil.which("bash") is None, reason="the Action's step needs bash and jq")


def step() -> str:
    return next(s["run"] for s in yaml.safe_load((ROOT / "action.yml").read_text())["runs"]["steps"] if s.get("name") == "Check")


def run(tmp_path: Path, verdict: str, code: int, *, on_pending: str = "fail", changed: str = "", base_history: str = "") -> tuple[subprocess.CompletedProcess[str], Path]:
    work, stubs, temp = tmp_path / "s1flow", tmp_path / "bin", tmp_path / "temp"
    for d in (work / "policies" / "toy", stubs, temp):
        d.mkdir(parents=True, exist_ok=True)
    (work / "policies" / "toy" / "channels.json").write_text(json.dumps({"channels": {"current": 2}}))
    # gh: the base commit's channels.json and history.jsonl, and the pull request's files
    (stubs / "gh").write_text(f"""#!/usr/bin/env bash
case "$*" in
  *channels.json*) echo '{{"channels": {{"current": 1}}}}';;
  *history.jsonl*) printf '%s' {shlex.quote(base_history)};;
  *pulls/7/files*) printf '%s\\n' {shlex.quote(changed)};;
  *) echo "unexpected gh $*" >&2; exit 1;;
esac
""")
    # the CLI: records its arguments, writes the comment, prints the verdict
    (stubs / "uvx").write_text(f"""#!/usr/bin/env bash
echo "$@" > "{tmp_path}/args"
md=""; prev=""; for a in "$@"; do [ "$prev" = --markdown ] && md="$a"; prev="$a"; done
echo "### s1flow check · toy" > "$md"
echo '{{"verdict": "{verdict}"}}'
exit {code}
""")
    for f in stubs.iterdir():
        f.chmod(0o755)
    env = {**os.environ, "PATH": f"{stubs}:{os.environ['PATH']}", "RUNNER_TEMP": str(temp), "GITHUB_STEP_SUMMARY": str(temp / "summary"),
           "GITHUB_REPOSITORY": "o/r", "TASKS": "", "AGAINST": "", "CANDIDATE": "", "SAMPLE": "", "CACHED_ONLY": "true",
           "ON_PENDING": on_pending, "COMMENT": "false", "FORK": "true", "PR": "7", "BASE": "a" * 40, "WORKDIR": "s1flow",
           "PACKAGE": "s1flow[eval]", "ACTION_PATH": str(ROOT), "GH_TOKEN": "x"}
    return subprocess.run(["bash", "-c", step()], cwd=work, env=env, capture_output=True, text=True), temp


def test_a_pending_check_fails_unless_the_workflow_says_warn(tmp_path):
    ran, _ = run(tmp_path, "pending", 2)
    assert ran.returncode == 1 and "on-pending: fail" in ran.stdout
    ran, _ = run(tmp_path / "warn", "pending", 2, on_pending="warn")
    assert ran.returncode == 0 and "::warning title=s1flow check::toy is pending" in ran.stdout
    ran, _ = run(tmp_path / "maybe", "pending", 2, on_pending="maybe")
    assert ran.returncode == 1 and "on-pending is fail or warn" in ran.stdout


def test_the_base_commits_history_tells_a_rollback(tmp_path):
    entry = '{"schema": "s1flow/history@1"}\n'
    ran, temp = run(tmp_path, "rollback", 0, base_history=entry)
    args = (tmp_path / "args").read_text()
    assert ran.returncode == 0 and "check toy --against v1 --history " in args
    assert (temp / "s1flow-toy-history.jsonl").read_text() == entry  # the base commit's, not the change's own


def test_a_change_to_the_rules_is_flagged(tmp_path):
    changed = "modified s1flow/tasks/toy/task.py\nmodified s1flow/tasks/toy/corrections.jsonl\nmodified README.md\nmodified s1flow/tasks/other/task.py"
    ran, temp = run(tmp_path, "no_difference", 0, changed=changed)
    md = (temp / "summary").read_text()
    assert ran.returncode == 0 and "This change edits `s1flow/tasks/toy/task.py`, `s1flow/tasks/toy/corrections.jsonl`, which set the rules or the cases" in md
    assert "other" not in md and "::warning title=s1flow check::toy: this change edits" in ran.stdout
    ran, temp = run(tmp_path / "again", "no_difference", 0, changed="modified README.md\nadded s1flow/policies/toy/v3.json")
    assert ran.returncode == 0 and "WARNING" not in (temp / "summary").read_text()  # adopt adds a version: nothing to flag


def test_rewriting_a_saved_version_fails(tmp_path):
    ran, temp = run(tmp_path, "rollback", 0, changed="modified s1flow/policies/toy/v1.json\nadded s1flow/policies/toy/v3.json")
    assert ran.returncode == 1 and "this change rewrites `s1flow/policies/toy/v1.json`" in ran.stdout
    assert "A saved version is never rewritten" in (temp / "summary").read_text()
    ran, _ = run(tmp_path / "record", "pass", 0, changed="removed s1flow/policies/toy/v2.evaluation.json")
    assert ran.returncode == 1
