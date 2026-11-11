# Develop s1flow

The checks below run offline and need no API keys. To call real models from the bench project, put its keys in
`apps/bench/.env` (ignored by Git) and run `uv run s1flow doctor --project apps/bench` to check the connections.

```bash
uv sync --frozen
uv run pytest -q -n auto --dist worksteal   # also checks schema/, the import contracts and the wheel
uv run ruff check          # pyflakes: unused imports and variables, undefined names
uv run mypy src/s1flow
```

CI (`.github/workflows/tests.yml`) runs the same commands on every pull request and on main.

Some tests are properties checked on generated cases (Hypothesis): the measures against their definitions or
scikit-learn, the evaluation's reading of a case against production's, the rule search against its constraints, and
the policy store under any order of writes. With `CI` set they draw the same cases every run; locally they draw new
ones each time, and a failure prints the case that broke it.

`apps/bench` is this repository's own evaluation project, separate from the package you install. Its past reports
are not a measure of any provider's current accuracy. Tests of the package read `tests/fixtures/project`, a frozen
copy of the bench's line-up and policies, so re-running or adopting in the bench changes no test. A few also take
real input from the bench: `make_project(copy_tasks=...)` in `tests/conftest.py` copies the `nod-wake` and
`gh-ruff-area` tasks and reads their cases, `tests/test_optimize.py` reads `massive-ja-intent`'s question, and
`tests/test_schemas.py` checks every bench task's cases and every saved policy against the schemas. Editing those
tasks or their data can change these tests. `tests/test_bench.py` checks only that the bench's committed tasks,
policies and reports still read: when a change makes them unreadable, rewrite them to the current shape in the same
change.

## Release

A pull request that changes what users see (the CLI, the Python API, the Action, the Skill, file formats) adds a
line under the changelog's `## Unreleased` heading (creating it at the top when it is missing) and keeps the
version. Merging it releases nothing: main can hold several such changes before they ship.

A release is a pull request of its own, opened when main has an `Unreleased` section. It raises the alpha number in
`pyproject.toml` (`0.1.0a3` → `0.1.0a4`) and `uv.lock`, renames `Unreleased` to that version and date, and pins the
Action at `v<version>` and the package at `==<version>` in `examples/` and the Skill's `references/app.md`
(`tests/test_docs.py` fails until they agree). It changes nothing else: outside the changelog, every line it changes
names the old or the new version, and `.github/workflows/release-only.yml` fails a pull request that changes the
version and more. What ships is main at the moment it merges, so changes merged while it is open ship in it too; put
their changelog lines under its version.

Merging it releases: the publish workflow sees the version change on main, runs the package checks on that commit,
tags it `v<version>` (`s1flow init --ci` writes `gotalab/s1flow@v<version>` of the CLI that ran it, so every release
needs its tag) and publishes to PyPI. Nothing runs on a local machine. Only a commit that changes the version
releases, so a later merge never ships in its place. If a job fails for a reason outside the code (a runner or PyPI
outage), use "Re-run failed jobs" on that run; if the code needs a fix, merge it, then run the publish workflow from
main (Actions → publish → Run workflow), which releases main's version when it has no tag yet.
