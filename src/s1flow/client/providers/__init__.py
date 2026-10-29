"""Providers: what turns a `ModelSpec` into a `DecisionModel`, and what its models need from where they run.

The built-in ones are imported only when a spec names them, so an app that ships one policy
loads one provider (and not LiteLLM unless that policy is an `llm` one). Each declares the keys and
hosts its models need (needs.py, `s1flow doctor`); a provider of your own may, with `declares`.
"""

from __future__ import annotations

import importlib
from importlib.metadata import entry_points
from pathlib import Path

from ...core.errors import ConfigError
from ..cost import listed
from ..models import DecisionModel, ModelBuild, ModelSpec, ProviderFactory
from .needs import Needs, NeedsOf, declares, needs_of
from .published import PublishedOf, published_of, publishes

__all__ = ["BUILTIN", "Needs", "NeedsOf", "PublishedOf", "build_model", "build_one", "declares", "needs", "published", "publishes", "resolve"]

# The `provider` names s1flow.toml can use without code, as "module:factory" under s1flow.client.providers.
# Your own: "package.module:factory", or an entry point in the `s1flow.providers` group.
BUILTIN: dict[str, str] = {
    "typesafe": "typesafe:build",  # TypeSafe's API, or any server that speaks it (options.base_url)
    "gateway": "gateway:build",  # Vercel AI Gateway /v1/evaluate
    "openrouter": "openrouter:build",  # OpenRouter /systemone
    "cloudflare": "cloudflare:build",  # Workers AI, through clef-proxy/
    "openai-decisions": "openai_decisions:build",  # OpenAI Decisions API
    "llm": "llm:build",  # any LLM LiteLLM reaches, asked for JSON
}


def resolve(kind: str) -> ProviderFactory:
    """A provider named by the application's trusted ModelSpec: built in, "package.module:factory", or an
    entry point in the `s1flow.providers` group."""
    if kind in BUILTIN:
        module, _, attr = BUILTIN[kind].partition(":")
        builtin: ProviderFactory = getattr(importlib.import_module(f"{__name__}.{module}"), attr)
        return builtin
    if ":" in kind:
        module, _, attr = kind.partition(":")
        try:
            factory: ProviderFactory = getattr(importlib.import_module(module), attr)
        except (ImportError, AttributeError) as e:
            raise ConfigError(f"cannot load provider {kind!r}: {e}") from None
        return factory
    found = entry_points(group="s1flow.providers", name=kind)
    if found:
        plugin: ProviderFactory = next(iter(found)).load()
        return plugin
    raise ConfigError(f"unknown provider {kind!r}; built in: {', '.join(BUILTIN)}; or name your own as package.module:factory")


def build_model(b: ModelBuild) -> DecisionModel:
    """The spec's provider builds the model; its calls are priced from the spec's list price, if it has one (client/cost.py)."""
    return listed(resolve(b.spec.provider)(b), b.spec.price)


def build_one(name: str, spec: ModelSpec, cache_dir: Path | None = None) -> DecisionModel:
    """Build the application-supplied model specification without line-up lookup."""
    return build_model(ModelBuild(name, spec.resolved(), cache_dir))


def needs(spec: ModelSpec) -> Needs | None:
    """What a model of this spec needs (keys, hosts, packages), as its provider declares it; None when it declares
    nothing. Nothing is built and no key is read. An unknown provider or options that do not fit are a ConfigError."""
    of = needs_of(resolve(spec.provider))
    return None if of is None else of(spec)


def published(spec: ModelSpec) -> PublishedOf | None:
    """How to read the list price of this spec's model, as its provider declares it (published.py); None when it
    declares none. Nothing is read until it is called."""
    return published_of(resolve(spec.provider))
