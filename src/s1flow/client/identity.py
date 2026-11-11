"""Content identities shared by the runtime and evaluation; no evaluation imports.

These are equality checks, not signatures. Credentials never contribute to them. Neither the
s1flow version nor its source does: an upgrade that sends the same request and reads the
answer the same way keeps every saved answer, cache entry and adoption. REQUEST and
EXECUTION are bumped by hand when that stops being true; tests/test_wire_format.py fails
when what is sent or how an answer is read changes, so the bump is not forgotten.
"""
from __future__ import annotations

import hashlib
import json
import re
from importlib.metadata import PackageNotFoundError, version
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from pydantic import BaseModel, SecretBytes, SecretStr

from .models import ModelSpec
from .endpoints import cloudflare_relay
from .questions import Questions
from .state import State

_SECRET = re.compile(r"(^|[_-])(api[_-]?key|key|auth|bearer|access[_-]?token|refresh[_-]?token|token|password|passwd|secret|authorization|credential|cookie)($|[_-])", re.I)


def _plain(value: Any) -> Any:
    if isinstance(value, BaseModel):
        return _plain(value.model_dump(mode="json"))
    if isinstance(value, dict):
        return {str(k): _plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(v) for v in value]
    if isinstance(value, (set, frozenset)):
        return sorted(_plain(v) for v in value)
    return value


def digest(value: Any) -> str:
    """Canonical JSON SHA-256 (also used for data and adapter identities)."""
    data = json.dumps(_plain(value), sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(data.encode()).hexdigest()


def _public(value: Any) -> Any:
    if isinstance(value, (SecretStr, SecretBytes)):
        return "<credential>"
    if isinstance(value, dict):
        return {str(k): ("<credential>" if _SECRET.search(str(k)) and not str(k).endswith("_env") else _public(v)) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_public(v) for v in value]
    if isinstance(value, str) and value.startswith(("https://", "http://")):
        u = urlsplit(value)
        host = u.netloc.rsplit("@", 1)[-1]
        query = urlencode([(k, "<credential>" if _SECRET.search(k) else v) for k, v in parse_qsl(u.query, keep_blank_values=True)])
        return urlunsplit((u.scheme, host, u.path, query, u.fragment))
    return value


# Bump when a built-in provider sends different bytes for the same input and question, or reads
# the same reply into a different answer (tests/test_wire_format.py names the change).
REQUEST = "s1flow/request@3"
# Bump when a policy turns the same answers into different decisions. An execution names REQUEST too.
EXECUTION = "s1flow/execution@3"

try:
    SDK_VERSION = version("s1flow")
except PackageNotFoundError:
    SDK_VERSION = "source"


def model_digest(spec: ModelSpec) -> str:
    """Effective provider, concrete id, options and capabilities; no prices or notes."""
    s = spec.resolved()
    return digest({
        "endpoint": _public(cloudflare_relay()) if s.provider == "cloudflare" else None,
        "provider": s.provider,
        "provider_revision": s.provider_revision,
        "id": s.id,
        "options": _public(s.options),
        "capabilities": s.capabilities,
    })


def _dependency_revision(spec: ModelSpec) -> dict[str, str]:
    # LiteLLM owns request construction for the llm provider. Inspect metadata
    # without importing an optional dependency or loading provider code.
    if spec.provider != "llm":
        return {}
    try:
        return {"litellm": version("litellm")}
    except PackageNotFoundError:
        return {"litellm": "unavailable"}


def request_digest(spec: ModelSpec, state: State, questions: Questions) -> str:
    """The actual materialized input, question and effective request implementation."""
    return digest({"schema": REQUEST, "model": model_digest(spec), "state": state,
                   "questions": questions, "dependencies": _dependency_revision(spec)})


def execution_digest(spec: ModelSpec, policy_digest: str) -> str:
    """Shared runtime conditions; evaluation records preprocessing identity separately."""
    return digest({"schema": EXECUTION, "request": REQUEST, "model": model_digest(spec), "policy": policy_digest,
                   "declared_concurrency": spec.concurrency, "dependencies": _dependency_revision(spec)})


def state_digest(state: State) -> str:
    """Hash the materialized input, including the bytes sent for prepared images."""
    return digest(state)


def require_provider_revision(spec: ModelSpec) -> None:
    """Evaluation reuse needs an app-declared revision of custom request code.

    Built-ins are covered by REQUEST and EXECUTION. This guard is not applied
    by direct Client or DecisionPolicy, which support explicitly unassessed use.
    """
    from ..core.errors import ConfigError
    from .providers import BUILTIN

    if spec.provider not in BUILTIN and not spec.provider_revision:
        raise ConfigError(f"custom provider {spec.provider!r} needs provider_revision in the app's model configuration "
                          "before evaluation, caching or adoption; declare its implementation commit or package revision")


# 0.1.0a2 to 0.1.0a5 hashed their version and the source of client/ and policies/ into every identity, so each
# upgrade made every saved answer look unasked. They send what this release sends and read answers as it does,
# except that 0.1.0a2 and 0.1.0a3 sent a state's keys in the order written (0.1.0a4 sorts them): their answers
# stand only for a state whose keys were already sorted, and their policies were measured on such requests.
# Saved runs, cache entries and adoptions keep the identity they were written with, so keep this table. It names
# the formats those releases sent and decided as: a bump of either retires it.
_RELEASED_AS = ("s1flow/request@3", "s1flow/execution@3")
_RELEASED: dict[str, tuple[str, bool]] = {  # version -> (its source revision, whether it sent keys sorted)
    "0.1.0a2": ("be5b78a24f470d18042ddfc443235b0cc990ae21551a4b6d87cb2c7145114b8d", False),
    "0.1.0a3": ("3abe4d1a43437172e57cb9f39ec63198767b0ef4ef3661bf8c5ae7bbc5f6a756", False),
    "0.1.0a4": ("fcdfd90b318c653acaeb3a129f512800707cb2292880f6a69cb3b365f34c2ce7", True),
    "0.1.0a5": ("2a64d762d1cd9a5dc93fcb8cc9ad6a85740a7c4dac9b7bb5915370165c9e7f55", True),
}


def _keys_sorted(x: Any) -> bool:
    if isinstance(x, dict):
        return list(x) == sorted(x, key=str) and all(_keys_sorted(v) for v in x.values())
    if isinstance(x, (list, tuple)):
        return all(_keys_sorted(v) for v in x)
    return True


def request_digests(spec: ModelSpec, state: State, questions: Questions) -> tuple[str, ...]:
    """The request's identity, then the ones the releases above wrote for the same request."""
    if REQUEST != _RELEASED_AS[0]:
        return (request_digest(spec, state, questions),)
    sent_as_now = _keys_sorted(state)
    common = {"model": model_digest(spec), "state": state, "questions": questions, "dependencies": _dependency_revision(spec)}
    return (request_digest(spec, state, questions), *(
        digest(common | {"schema": "s1flow/request@2", "sdk": sdk, "implementation": revision})
        for sdk, (revision, sorted_sent) in _RELEASED.items() if sorted_sent or sent_as_now))


def execution_digests(spec: ModelSpec, policy_digest: str) -> tuple[str, ...]:
    """The execution's identity, then the ones the releases that sent keys sorted wrote for it."""
    if (REQUEST, EXECUTION) != _RELEASED_AS:
        return (execution_digest(spec, policy_digest),)
    common = {"model": model_digest(spec), "policy": policy_digest, "declared_concurrency": spec.concurrency,
              "dependencies": _dependency_revision(spec)}
    return (execution_digest(spec, policy_digest), *(
        digest(common | {"schema": "s1flow/execution@2", "sdk": sdk, "implementation": revision})
        for sdk, (revision, sorted_sent) in _RELEASED.items() if sorted_sent))
