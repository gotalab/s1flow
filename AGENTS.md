# Develop s1flow

This file is for people and agents changing this repository. What s1flow does for its users is in the README.

## Check a change

These run offline and need no API keys. CI (`.github/workflows/tests.yml`) runs the same on every pull request.

```bash
uv sync --frozen
uv run pytest -q -n auto --dist worksteal   # also checks schema/, the import contracts and the wheel
uv run ruff check          # pyflakes: unused imports and variables, undefined names
uv run mypy src/s1flow
```

[docs/development.md](docs/development.md) says which tests read the bench project in `apps/bench`, and how a
release works.

## Rules for every change

- Write everything committed here in English: code, comments, messages, docs and pull requests. The repository is
  public and its readers are outside users.
- Change formats and interfaces directly. Add no compatibility layer, deprecation path or migration: s1flow is an
  alpha with almost no users.
- The CLI only measures, records and switches: the same input gives the same output. Ranking, recommending,
  highlighting or ordering things for a reader belongs to the Skill (`plugin/skills/s1flow`) or the agent using it,
  never to a command or the files it writes. A command stretched past this becomes ambiguous to call and turns into
  debt.
- A pull request that changes what users see (the CLI, the Python API, the decide Action, the Skill, file formats)
  adds a line under `## Unreleased` in `CHANGELOG.md` (creating the heading at the top when it is missing) and keeps
  the version. Merging it releases nothing. Only a release pull request raises the version, and it changes nothing
  else ([Release](docs/development.md#release)).
