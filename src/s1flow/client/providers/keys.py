"""API keys come from the environment only (the CLI also loads the project's .env files into it)."""

from __future__ import annotations

import os

from ...core.errors import ConfigError
from .needs import where_to_get


def key(env: str) -> str:
    value = os.environ.get(env)
    if not value:
        raise ConfigError(f"{env} is not set: {how_to_set(env)}")
    return value


def how_to_set(env: str) -> str:
    get = where_to_get(env)
    return (f"{get + ', then ' if get else ''}set it in the environment or in a .env in the project "
            "or above it (s1flow doctor lists what each model needs)")
