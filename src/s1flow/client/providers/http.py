"""The one HTTP path every decision-model provider uses: retries, then one of two outcomes.

- a JSON body, with how long the attempt that answered took and how many retries came before it, or
- `Rejected` (the provider refused the input as outside its limits: 413, 422, or a 400 that
  says a part is not accepted) or `ProviderError` (anything else), both carrying the status.

A key that is not set is left out rather than stopping the call: a sandbox's proxy may add it on the way
(a network secret). If the provider then answers 401 or 403, the error is the missing key's, as before.
A 401 with every key set says the key was not accepted.

408 / 409 / 429 / 5xx and timeouts are retried with exponential backoff first. The latency is
that of the answering attempt alone: failed attempts and the backoff between them are not the
model's speed, and are counted in `retries` instead.
"""

from __future__ import annotations

import asyncio
import os
import time
from dataclasses import dataclass, field
from typing import Any

import httpx

from ...core.errors import ConfigError, ProviderError, Rejected
from .keys import how_to_set

RETRY_STATUS = frozenset({408, 409, 429, 500, 502, 503, 504})
AUTH_STATUS = frozenset({401, 403})
REFUSAL_STATUS = frozenset({413, 422})
# 400s that name a refused part (OpenRouter: 'Phala does not accept "image_url" parts in state',
# 'Inception does not accept box questions', 2026-10-16). A bare 400 stays a failure: it is
# more often our request than the model's limit.
REFUSAL_HINTS = ("does not accept", "too large", "exceeds the maximum")

_clients: dict[int, httpx.AsyncClient] = {}


def client() -> httpx.AsyncClient:
    """One client per event loop: the optimizer runs each evaluation in a fresh loop."""
    loop = id(asyncio.get_running_loop())
    if loop not in _clients:
        _clients.clear()
        _clients[loop] = httpx.AsyncClient(timeout=httpx.Timeout(60.0, connect=10.0))
    return _clients[loop]


@dataclass(frozen=True)
class Request:
    """One call as it goes on the wire, built before any key is read. A provider's `request` builds it and its
    `decide` sends it (`send`)."""

    url: str
    body: dict[str, Any]
    headers: dict[str, str] = field(default_factory=dict)  # none of them secret
    keys: dict[str, tuple[str, str]] = field(default_factory=dict)  # header -> (prefix, environment variable), filled when sent
    method: str = "POST"

    def unset_keys(self) -> list[str]:
        return [env for _, env in self.keys.values() if not os.environ.get(env)]

    def sent_headers(self) -> dict[str, str]:
        """The headers with each key that is set; an unset one is left out for a proxy to add."""
        return {**self.headers, **{h: prefix + value for h, (prefix, env) in self.keys.items() if (value := os.environ.get(env))}}


@dataclass(frozen=True)
class Posted:
    data: dict[str, Any]
    latency_ms: float  # request sent to response read, for the attempt that answered
    retries: int  # attempts before it that were throttled, failed on the server, or timed out


def retryable(status: int | None) -> bool:
    return status in RETRY_STATUS


def classify(status: int, text: str) -> Rejected | ProviderError:
    if status in REFUSAL_STATUS or (status == 400 and any(h in text.lower() for h in REFUSAL_HINTS)):
        return Rejected(f"rejected by the provider ({status}): {text[:200]}", status)
    return ProviderError(f"{status}: {text[:500]}", status)


async def post_json(url: str, body: dict[str, Any], headers: dict[str, str], attempts: int = 4) -> Posted:
    """POST with exponential backoff on throttling, server errors and timeouts."""
    for attempt in range(attempts):
        last = attempt == attempts - 1
        t0 = time.perf_counter()
        try:
            r = await client().post(url, json=body, headers=headers)
        except (httpx.TimeoutException, httpx.TransportError) as e:
            if last:
                raise ProviderError(f"{type(e).__name__}: {e}") from e
        else:
            latency = (time.perf_counter() - t0) * 1000
            if r.status_code < 400:
                try:
                    data = r.json()
                except ValueError as e:
                    raise ProviderError(f"unreadable response ({r.status_code}): {r.text[:200]}", r.status_code) from e
                if not isinstance(data, dict):
                    raise ProviderError(f"unexpected response ({r.status_code}): {r.text[:200]}", r.status_code)
                return Posted(data, latency, attempt)
            if not retryable(r.status_code) or last:
                raise classify(r.status_code, r.text)
        await asyncio.sleep(0.5 * 2**attempt)
    raise AssertionError("unreachable")


def refused_without(env: str, e: ProviderError) -> ConfigError:
    """A call sent without `env` (not set, for a proxy to add) and refused for it: the missing key's error."""
    return ConfigError(f"{env} is not set and the provider refused the call without it ({e}): {how_to_set(env)}")


async def send(req: Request) -> Posted:
    """A built request, with its keys read from the environment now. Refused for want of a key that was not set:
    the error says to set it."""
    unset = req.unset_keys()
    try:
        return await post_json(req.url, req.body, req.sent_headers())
    except ProviderError as e:
        if e.status in AUTH_STATUS and unset:
            raise refused_without(unset[0], e) from e
        if e.status == 401 and req.keys:  # 403 with a key can be the provider's own refusal (OpenRouter's moderation)
            names = ", ".join(env for _, env in req.keys.values())
            raise ProviderError(f"the provider did not accept {names} ({e}): check the key", e.status) from e
        raise
