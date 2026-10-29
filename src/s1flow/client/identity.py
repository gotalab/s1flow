"""Content identities shared by the runtime and evaluation; no evaluation imports.

These are equality checks, not signatures. Credentials never contribute to them. A
source revision accompanies the SDK version so editable installs cannot certify old
answers after the request builder or answer interpretation changes.
"""
from __future__ import annotations

import hashlib
import json
import re
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
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


def _revision() -> str:
    root = Path(__file__).parent
    # Include the shared response interpretation too. No config or user inputs are read.
    paths = sorted(root.rglob("*.py")) + sorted((root.parent / "policies").glob("*.py"))
    return digest({str(p.relative_to(root.parent)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})


try:
    SDK_VERSION = version("s1flow")
except PackageNotFoundError:
    SDK_VERSION = "source"
IMPLEMENTATION_REVISION = _revision()


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
    return digest({"schema": "s1flow/request@2", "model": model_digest(spec), "state": state,
                   "questions": questions, "sdk": SDK_VERSION, "implementation": IMPLEMENTATION_REVISION,
                   "dependencies": _dependency_revision(spec)})


def execution_digest(spec: ModelSpec, policy_digest: str) -> str:
    """Shared runtime conditions; evaluation records preprocessing identity separately."""
    return digest({"schema": "s1flow/execution@2", "model": model_digest(spec), "policy": policy_digest,
                   "declared_concurrency": spec.concurrency,
                   "sdk": SDK_VERSION, "implementation": IMPLEMENTATION_REVISION,
                   "dependencies": _dependency_revision(spec)})


def state_digest(state: State) -> str:
    """Hash the materialized input, including the bytes sent for prepared images."""
    return digest(state)


def require_provider_revision(spec: ModelSpec) -> None:
    """Evaluation reuse needs an app-declared revision of custom request code.

    Built-ins are covered by IMPLEMENTATION_REVISION. This guard is not applied
    by direct Client or DecisionPolicy, which support explicitly unassessed use.
    """
    from ..core.errors import ConfigError
    from .providers import BUILTIN

    if spec.provider not in BUILTIN and not spec.provider_revision:
        raise ConfigError(f"custom provider {spec.provider!r} needs provider_revision in the app's model configuration "
                          "before evaluation, caching or adoption; declare its implementation commit or package revision")
