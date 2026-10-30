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

## Release

1. Set the version in `pyproject.toml` and merge it to main.
2. Run the publish workflow (Actions → publish → Run workflow) on that commit.
3. Tag the same commit `v<version>` and push the tag (`git tag -a v0.1.0a1 <sha> && git push origin v0.1.0a1`).
   `s1flow init --ci` writes `gotalab/s1flow@v<version>` of the CLI that ran it, so a release without its tag
   gives new projects a workflow that cannot find its Action.
4. Point `examples/` at the new tag.
