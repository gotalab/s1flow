"""The CLI as an agent drives it: one exit table, a usage error as one `error:` line, a warning as a `notice:` line."""

from __future__ import annotations


import pytest

from conftest import s1flow

from s1flow.cli import EXITS, HELP, TABLE



@pytest.mark.parametrize("args, said", [
    (("repot",), "error: no command 'repot'; did you mean 'report'? (see s1flow --help)"),
    (("--project", ".", "repot"), "error: no command 'repot'; did you mean 'report'?"),
    (("--connections", "c.toml", "skill", "install"), "error: no command 'skill'"),
    (("run",), "error: the following arguments are required: task (see s1flow run --help)"),
    (("run", "t", "--bogus"), "error: unrecognized arguments: --bogus (see s1flow run --help)"),
    (("check", "t", "--sample", "0"), "error: argument --sample: 0 is not 1 or more (see s1flow check --help)"),
    (("decide", "--bogus"), "error: unrecognized arguments: --bogus (see s1flow decide --help)"),
    (("export", "--bogus"), "error: unrecognized arguments: --bogus (see s1flow export --help)"),
    (("adopt", "t@v1"), "error: adopt records why: give --reason a sentence"),
    (("adopt", "t@v1", "--check", "--reason", "x"), "error: adopt --check validates a spec: adopt --spec FILE --check"),
])
def test_a_usage_error_is_one_line_and_exit_2(tmp_path, args, said):
    done = s1flow(*args, cwd=tmp_path)
    assert done.returncode == 2 and "Traceback" not in done.stderr
    assert done.stderr.strip().splitlines()[-1].startswith("error: ") and said in done.stderr


def test_the_top_help_lists_every_command_and_the_exit_codes():
    from s1flow.cli import parser

    done = s1flow("--help")
    assert done.returncode == 0 and done.stdout.strip() == HELP and EXITS in done.stdout
    commands = set(parser()._subparsers._group_actions[0].choices)  # type: ignore[union-attr]
    assert [name for name, _ in TABLE] and {name for name, _ in TABLE} == commands


def _commands(p, path=()):
    """Every command and subcommand the parser takes, as the words that run it."""
    import argparse

    subs = [a for a in p._actions if isinstance(a, argparse._SubParsersAction)]
    if not subs:
        yield path
    for a in subs:
        for name, child in a.choices.items():
            yield from _commands(child, (*path, name))


def test_every_command_takes_h_and_its_help_ends_with_the_exit_codes():
    from conftest import cli

    from s1flow.cli import parser

    found = list(_commands(parser()))
    assert ("cases", "review") in found and ("export",) in found and ("optimize",) in found and ("report",) in found and len(found) == 15
    for words in found + [("cases",), ("feedback",)]:
        done = cli(*words, "-h")
        assert done.exit_code == 0 and " ".join(EXITS.split()) in " ".join(done.output.split()), words


def test_a_warning_is_a_notice_line(capsys):
    import warnings

    from s1flow.cli import notices

    shown = warnings.showwarning
    try:
        notices()
        warnings.warn("left out until run on every case: x (3 cases never asked)", stacklevel=1)
    finally:
        warnings.showwarning = shown
    assert capsys.readouterr().err == "notice: left out until run on every case: x (3 cases never asked)\n"


def test_names_are_checked_at_the_entry_and_the_right_ones_listed(tmp_path):
    from conftest import make_project
    from s1flow.core.errors import NotFound
    from s1flow.eval import run as running
    from s1flow.eval.task import load

    project = make_project(tmp_path, {"m": lambda b: None}, copy_tasks=("gh-ruff-area",), versions={"m": {"1.0": "m-1.0"}})
    with pytest.raises(NotFound, match="no task 'ruff-area'; the tasks: gh-ruff-area"):
        load(project, "ruff-area")
    task = load(project, "gh-ruff-area")
    assert [c.name for c in running.candidates(task, ["m", "m:1.0"])] == ["m", "m:1.0"]
    for name, said in (("n", "unknown connection 'n'; known: m"), ("m:2.0", "m: no version '2.0'; versions: 1.0"),
                       ("m/policy", "gh-ruff-area has no variant 'policy'; variants: none")):
        with pytest.raises(NotFound, match=said):
            running.candidates(task, [name])
    # the command that asks a candidate again names it the same way
    assert running.ask_again(task, [("m", "base"), ("m:1.0", "policy"), ("m", "base")]) == "s1flow run gh-ruff-area --models m,m:1.0/policy"


def test_report_with_no_task_is_the_overview_of_what_runs(tmp_path):
    """Per task, the current policy: candidate, version, the id that answers, pinned or not, and why."""
    import json
    import shutil

    from conftest import PROJECT

    (tmp_path / "s1flow.toml").write_text((PROJECT / "s1flow.toml").read_text())
    shutil.copytree(PROJECT / "policies", tmp_path / "policies")
    (tmp_path / "policies" / "gh-ruff-area" / "channels.json").write_text('{"schema": "s1flow/channels@1", "channels": {"current": 1}}\n')
    done = s1flow("report", "--json", cwd=tmp_path)
    assert done.returncode == 0, done.stderr
    area = next(t for t in json.loads(done.stdout) if t["task"] == "gh-ruff-area")
    assert area["current"] == 1
    v = {r["version"]: r for r in area["policies"]}
    assert (v[1]["candidate"], v[1]["model_version"], v[1]["answered_by"], v[1]["pin"]) == ("d1@vercel", None, "liquid/d1", "no")
    assert v[3]["candidate"] == "d1@vercel/improve-d1@vercel-20261016-0701" and v[1]["current"] and not v[3]["current"]
    assert (v[2]["candidate"], v[2]["model_version"], v[2]["pin"]) == ("jev", "1.14", "yes")  # an old policy sends jev-1.14.0
    text = s1flow("report", cwd=tmp_path).stdout.splitlines()
    assert text[0].split()[:2] == ["task", "current"]
    assert ["gh-ruff-area", "gh-ruff-area@v1", "d1@vercel", "-", "liquid/d1", "no"] in [t.split() for t in text]
    # why current is what it is: the last switch in history.jsonl
    (tmp_path / "policies" / "gh-ruff-area" / "history.jsonl").write_text(json.dumps(
        {"schema": "s1flow/history@1", "at": "2026-10-30T09:00:00Z", "action": "spec", "version": 1, "previous": 3, "by": "ana", "reason": "v3 times out"}) + "\n")
    shown = s1flow("report", cwd=tmp_path)
    assert shown.returncode == 0 and "gh-ruff-area: v1 by ana, 2026-10-30 (spec from v3): v3 times out" in shown.stdout
    area = next(t for t in json.loads(s1flow("report", "--json", cwd=tmp_path).stdout) if t["task"] == "gh-ruff-area")
    assert area["why"]["reason"] == "v3 times out" and area["current"] == 1


