# Develop s1flow

The checks below run offline and need no API keys. To call real models from the bench project, put its keys in
`apps/bench/.env` (ignored by Git) and run `uv run s1flow doctor --project apps/bench` to check the connections.

```bash
uv sync --frozen
uv run pytest -q
uv run mypy src/s1flow
uv run lint-imports --no-cache
uv run python scripts/write_schemas.py --check
uv run python scripts/sync_plugin.py --check
uv build --wheel
```

`apps/bench` is this repository's own evaluation project, separate from the package you install. Its past reports
are not a measure of any provider's current accuracy.
