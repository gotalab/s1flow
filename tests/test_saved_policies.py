"""The saved-policies workflow's step, run on a small Git history: a change that rewrites a saved version fails."""

import subprocess
from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml")

ROOT = Path(__file__).resolve().parents[1]
POLICIES = "apps/bench/policies/toy"


def step() -> str:
    jobs = yaml.safe_load((ROOT / ".github" / "workflows" / "saved-policies.yml").read_text())["jobs"]
    return next(s["run"] for s in jobs["saved-policies"]["steps"] if "run" in s)


def git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@example.com", *args], cwd=repo, check=True, capture_output=True)


@pytest.fixture
def repo(tmp_path):
    git(tmp_path, "init", "-q")
    d = tmp_path / POLICIES
    d.mkdir(parents=True)
    for name in ("v1.json", "v1.evaluation.json", "channels.json", "history.jsonl"):
        (d / name).write_text(f"{name} as saved, long enough that a rename would be detected as one\n")
    git(tmp_path, "add", ".")
    git(tmp_path, "commit", "-q", "-m", "base")
    return tmp_path


def run(repo: Path) -> subprocess.CompletedProcess[str]:
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "change")
    return subprocess.run(["bash", "-c", step()], cwd=repo, capture_output=True, text=True)


def test_adopting_a_new_version_passes(repo):
    (repo / POLICIES / "v2.json").write_text("new\n")
    (repo / POLICIES / "v2.evaluation.json").write_text("new\n")
    (repo / POLICIES / "channels.json").write_text("current is v2\n")
    (repo / POLICIES / "history.jsonl").write_text("why\n")
    done = run(repo)
    assert done.returncode == 0 and "No saved policy version is rewritten" in done.stdout


@pytest.mark.parametrize("rewrite", [
    lambda d: (d / "v1.json").write_text("edited\n"),
    lambda d: (d / "v1.evaluation.json").write_text("edited\n"),
    lambda d: (d / "v1.json").unlink(),
    lambda d: (d / "v1.json").rename(d / "v3.json"),
    lambda d: ((d / "v1.json").unlink(), (d / "v1.json").symlink_to("channels.json")),
], ids=["edited", "evidence edited", "removed", "renamed", "replaced by a link"])
def test_rewriting_a_saved_version_fails(repo, rewrite):
    rewrite(repo / POLICIES)
    done = run(repo)
    assert done.returncode == 1 and "::error::this pull request rewrites saved policy versions" in done.stdout
    assert f"{POLICIES}/v1." in done.stdout


def test_a_diff_that_cannot_be_read_fails(tmp_path):
    git(tmp_path, "init", "-q")
    (tmp_path / "a").write_text("a\n")
    git(tmp_path, "add", ".")
    git(tmp_path, "commit", "-q", "-m", "the only commit: no HEAD^1")
    done = subprocess.run(["bash", "-c", step()], cwd=tmp_path, capture_output=True, text=True)
    assert done.returncode != 0 and "No saved policy version is rewritten" not in done.stdout
