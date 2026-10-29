"""What a model needs from where it runs: the variables it reads and the hosts it calls (`s1flow doctor`).

A provider declares it next to its factory, so an agent in a sandbox can tell which secrets to set and which
hosts to allow without calling a model:

    def needs(spec: ModelSpec) -> Needs:
        return Needs(keys=("MY_API_KEY",), hosts=("https://api.example.com",))

    @declares(needs)
    def build(b: ModelBuild) -> MyModel: ...

The declaration is optional: for a provider without one, `s1flow doctor` says it cannot tell and checks nothing.
It reads the spec alone and imports nothing the provider calls with, so it runs on the base install.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Protocol, TypeVar, runtime_checkable
from urllib.parse import urlsplit

from ...core.errors import ConfigError
from ..models import ModelSpec


@dataclass(frozen=True)
class Needs:
    keys: tuple[str, ...] = ()  # environment variables the call needs set (API keys); never read here
    hosts: tuple[str, ...] = ()  # origins it calls ("https://api.typesafe.ai"): a sandbox's allow-list
    packages: tuple[str, ...] = ()  # modules beyond the base install it imports ("litellm")
    note: str = ""  # what the declaration cannot tell


NeedsOf = Callable[[ModelSpec], Needs]
F = TypeVar("F", bound=Callable[..., Any])


@runtime_checkable
class Declared(Protocol):
    """A factory that says what its models need: a function marked with `declares`, or an object with `needs`."""

    needs: NeedsOf


def declares(needs: NeedsOf) -> Callable[[F], F]:
    """Mark a provider factory with what its models need."""

    def mark(factory: F) -> F:
        setattr(factory, "needs", needs)
        return factory

    return mark


def needs_of(factory: object) -> NeedsOf | None:
    return factory.needs if isinstance(factory, Declared) else None


def origin(url: str) -> str:
    """"https://api.typesafe.ai/v1" -> "https://api.typesafe.ai"."""
    u = urlsplit(url)
    if not (u.scheme and u.netloc):
        raise ConfigError(f"not a URL: {url!r}")
    return f"{u.scheme}://{u.netloc}"


# Where to get each key the built-in providers read: `s1flow doctor` and a missing key's error name the page.
KEY_PAGES: dict[str, str] = {
    "OPENROUTER_API_KEY": "https://openrouter.ai/keys",
    "AI_GATEWAY_API_KEY": "https://vercel.com/docs/ai-gateway/authentication-and-byok/api-keys",
    "TYPESAFE_API_KEY": "https://console.typesafe.ai/",
    "OPENAI_API_KEY": "https://platform.openai.com/api-keys",
    "ANTHROPIC_API_KEY": "https://console.anthropic.com/settings/keys",
    "GEMINI_API_KEY": "https://aistudio.google.com/apikey",
}


def where_to_get(key: str) -> str:
    """"get one at <page>" for a key s1flow knows, else "" (a provider of your own names its own)."""
    return f"get one at {KEY_PAGES[key]}" if key in KEY_PAGES else ""


# LiteLLM's providers by the id's prefix: the key LiteLLM reads and the host it calls.
LITELLM: dict[str, tuple[str, str]] = {
    "vercel_ai_gateway/": ("AI_GATEWAY_API_KEY", "https://ai-gateway.vercel.sh"),
    "openai/": ("OPENAI_API_KEY", "https://api.openai.com"),
    "anthropic/": ("ANTHROPIC_API_KEY", "https://api.anthropic.com"),
    "gemini/": ("GEMINI_API_KEY", "https://generativelanguage.googleapis.com"),
    "openrouter/": ("OPENROUTER_API_KEY", "https://openrouter.ai"),
    "groq/": ("GROQ_API_KEY", "https://api.groq.com"),
    "mistral/": ("MISTRAL_API_KEY", "https://api.mistral.ai"),
    "deepseek/": ("DEEPSEEK_API_KEY", "https://api.deepseek.com"),
    "xai/": ("XAI_API_KEY", "https://api.x.ai"),
}


def litellm_needs(model: str, api_key_env: str | None = None) -> Needs:
    """An LLM through LiteLLM: the provider LiteLLM reads from the id's prefix, or a bare OpenAI id ("gpt-5-mini"). `api_key_env` replaces the key."""
    prefix = next((p for p in LITELLM if model.startswith(p)), "openai/" if "/" not in model else None)
    if prefix is None:
        keys = (api_key_env,) if api_key_env else ()
        return Needs(keys=keys, packages=("litellm",), note=f"LiteLLM's provider for {model!r} not known to s1flow: see LiteLLM's docs for its key and host")
    env, host = LITELLM[prefix]
    return Needs(keys=(api_key_env or env,), hosts=(host,), packages=("litellm",))
