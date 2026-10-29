"""`s1flow init`: make `s1flow/` (or another directory) a project (core.place finds it by its s1flow.toml).

    s1flow.toml                          the line-up, to edit: three models on one key (OPENROUTER_API_KEY)
    tasks/<dir>/task.py                 a task to fill in, with --task
    .gitignore                          .cache/ and .env (answers and keys, kept out of git)
    <git root>/.github/workflows/s1flow-check.yml   check on PRs that change the project, with the Action; with --ci

Nothing else: the Agent Skill comes from the plugin or `s1flow skill install` (skill.py).
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path

from ..core import place
from ..core.errors import ConfigError
from ..client.lineup import BUILTIN_LINEUP

TEMPLATES = Path(__file__).resolve().parents[1] / "templates"
ACTION = "gotalab/s1flow@main"


def _git_root(d: Path) -> Path | None:
    for p in [d, *d.parents]:
        if (p / ".git").exists():
            return p
    return None


def stub(task_id: str, instructions: str) -> str:
    """The task.py `init --task` writes, to fill in."""
    doc = instructions.replace("\\", "\\\\").replace('"""', "'''")
    text = (TEMPLATES / "task.py.tmpl").read_text().format(
        task_id=task_id, task_id_repr=repr(task_id), doc=doc, instructions=repr(instructions))
    compile(text, "task.py", "exec")  # every value went in through repr(): a failure here is s1flow's bug
    return text


def init(
    project: Path, task_id: str | None = None, instructions: str = "Is this a bug report?", action: str = ACTION, workflow: bool = False,
) -> list[str]:
    """Returns what was written (an existing file is left as it is)."""
    project = project.resolve()
    project.mkdir(parents=True, exist_ok=True)
    done: list[str] = []

    def show(path: Path) -> str:  # from where init ran, so s1flow/ shows
        return os.path.relpath(path) if path.is_relative_to(Path.cwd()) else str(path)

    def write(path: Path, text: str) -> None:
        if path.exists():
            done.append(f"kept {show(path)} (exists)")
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        done.append(f"wrote {show(path)}")

    if not (project / place.CONFIG).exists():
        shutil.copyfile(BUILTIN_LINEUP, project / place.CONFIG)
        done.append(f"wrote {show(project / place.CONFIG)}")
    ignore = project / ".gitignore"
    lines = ignore.read_text().splitlines() if ignore.exists() else []
    missing = [x for x in (".cache/", ".env") if x not in lines]  # answers and keys stay out of git
    if missing:
        ignore.write_text("\n".join([*lines, *missing]) + "\n")
        done.append(f"added {', '.join(missing)} to {show(ignore)}")
    if task_id and (why := place.task_id_error(task_id)):
        raise ConfigError(why)
    if task_id:
        write(project / "tasks" / task_id / "task.py", stub(task_id, instructions))  # its directory is named its id
    root = _git_root(project)
    if workflow and root is not None:
        rel = os.path.relpath(project, root)
        prefix = "" if rel == "." else rel.rstrip("/") + "/"
        wf = (TEMPLATES / "workflow.yml").read_text().format(prefix=prefix, action=action, workdir=rel)
        write(root / ".github" / "workflows" / "s1flow-check.yml", wf)
    return done
