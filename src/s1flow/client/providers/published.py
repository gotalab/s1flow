"""Where a model's list price can be read: a provider may say, next to its factory, as it says what it needs.

    def published(spec: ModelSpec, cache_dir: Path | None) -> Price | None:
        ...  # read the provider's price list (a network call); None: the model is not on it

    @publishes(published)
    @declares(needs)
    def build(b: ModelBuild) -> MyModel: ...

`s1flow models --verify` compares s1flow.toml's `price` with it (project/verify.py). The declaration is optional:
for a provider without one, --verify says the price cannot be checked. Nothing here runs on a call.
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path
from typing import Any, Callable, Protocol, TypeVar, runtime_checkable

from ..models import ModelSpec, Price

PublishedOf = Callable[[ModelSpec, Path | None], Price | None]
F = TypeVar("F", bound=Callable[..., Any])


@runtime_checkable
class Publishing(Protocol):
    published: PublishedOf


def publishes(published: PublishedOf) -> Callable[[F], F]:
    """Mark a provider factory with where its models' list prices can be read."""

    def mark(factory: F) -> F:
        setattr(factory, "published", published)
        return factory

    return mark


def published_of(factory: object) -> PublishedOf | None:
    return factory.published if isinstance(factory, Publishing) else None


def per_token(input_usd: Any, output_usd: Any, source: str, request_usd: Any = 0, image_usd: Any = 0) -> Price:
    """A price list's per-token prices (as most lists give them) as a `Price`, read today."""
    return Price(
        input_per_mtok=float(input_usd or 0) * 1_000_000, output_per_mtok=float(output_usd or 0) * 1_000_000,
        per_request=float(request_usd or 0), per_image=float(image_usd or 0), as_of=dt.date.today().isoformat(), source=source,
    )
