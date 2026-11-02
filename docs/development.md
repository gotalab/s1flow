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

`apps/bench` is this repository's own evaluation project, separate from the package you install. Its past reports
are not a measure of any provider's current accuracy. Tests of the package read `tests/fixtures/project`, a frozen
copy of the bench's line-up and policies, so re-running or adopting in the bench changes no test.
`tests/test_bench.py` checks only that the bench's committed tasks, policies and reports still read: when a change
makes them unreadable, rewrite them to the current shape in the same change.

## Release

In one pull request, set the version in `pyproject.toml`, and pin the Action at `v<version>` and the package at
`==<version>` in `examples/` and the Skill's `references/app.md` (`tests/test_docs.py` fails until they agree).
Merging it is the release: the publish workflow sees the new version on main, tags the merge commit `v<version>`
(`s1flow init --ci` writes `gotalab/s1flow@v<version>` of the CLI that ran it, so every release needs its tag), runs
the package checks on it and publishes to PyPI. Nothing runs on a local machine. If a job fails after the tag is made,
re-run the failed jobs of that run.
