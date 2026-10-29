"""The errors s1flow raises. Every one is an `S1flowError` whose message is one sentence a person can act on.

| error           | means                                                             | CLI exit |
|-----------------|-------------------------------------------------------------------|----------|
| `ConfigError`   | s1flow.toml, a task.py, a policy file or a key is wrong or missing | 2        |
| `DataError`     | a case is wrong (no state, a label outside the options, an image) | 2        |
| `NotFound`      | no such task, run, policy or channel                             | 2        |
| `ProviderError` | the model call failed (auth, 4xx, 5xx, timeouts after retries)    | 2        |
| `Unsupported`   | the model does not take this question type, image or option       | 2        |
| `Rejected`      | the provider refused the input after the call (413, 422, ...)      | 2        |

A check that runs and finds the change worse is a result (exit 1), not an error.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydantic import ValidationError


class S1flowError(Exception):
    """Every error s1flow raises on purpose."""


class ConfigError(S1flowError):
    """A configuration file or a key is wrong or missing."""


class DataError(S1flowError):
    """The case itself is wrong (no state, a label outside the options, a missing image). A task bug."""


class NotFound(S1flowError):
    """No such task, run, policy or channel."""


class ProviderError(S1flowError):
    """The call failed: auth, a 4xx that is not a refusal, 5xx or timeouts after retries, an unreadable response."""

    def __init__(self, message: str, status: int | None = None):
        super().__init__(message)
        self.status = status


class Unsupported(ProviderError):
    """Outside the model's declared capabilities (question type, image, options). Raised before any call."""


class Rejected(Unsupported):
    """The provider refused the input as outside its limits, after the call: 413, 422, or a 400
    that says it does not accept a part of the request. Not counted as a failure."""


def invalid(e: ValidationError, limit: int = 3) -> str:
    """A pydantic error as one line, for an error message: `models.b.colour: Extra inputs are not permitted`."""
    parts = [f"{'.'.join(str(x) for x in err['loc']) or 'value'}: {err['msg']}" for err in e.errors()[:limit]]
    more = f" (and {e.error_count() - limit} more)" if e.error_count() > limit else ""
    return "; ".join(parts) + more
