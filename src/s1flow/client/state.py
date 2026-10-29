"""What a decision model reads: a state of text, JSON, or a list of parts whose images are prepared."""

from __future__ import annotations

from typing import Any, Literal, TypeGuard

from pydantic import BaseModel, ConfigDict, model_validator


class ImageRef(BaseModel):
    """An image as a task writes it: `{"type": "image", "path": "shots/a.png"}` (relative to the
    task dir) or `{"type": "image", "url": ...}`. It is turned into an `Image` (images.materialize) before any call."""

    model_config = ConfigDict(extra="forbid")
    type: Literal["image"] = "image"
    path: str | None = None
    url: str | None = None

    @model_validator(mode="after")
    def _one_source(self) -> ImageRef:
        if (self.path is None) == (self.url is None):
            raise ValueError("an image needs exactly one of path or url")
        return self


class Image(BaseModel):
    """A prepared image (images.prepare): the same bytes go to every model."""

    model_config = ConfigDict(frozen=True, extra="forbid")
    type: Literal["image"] = "image"
    media_type: Literal["image/png", "image/jpeg"]
    data: str  # base64
    sha256: str
    width: int
    height: int


# A state is text, JSON, or a list of parts. Images are only top-level parts of a list
# (the one placement every provider can express); `Image` is not JSON-serializable, so a
# provider that forgets to translate one fails before sending it as text.
Part = str | dict[str, Any] | list[Any] | int | float | bool | None | Image
State = str | dict[str, Any] | list[Part]


def has_image(state: State) -> TypeGuard[list[Part]]:
    return isinstance(state, list) and any(isinstance(x, Image) for x in state)


def has_unprepared_image(x: Any) -> bool:
    """An image reference anywhere that was never turned into an `Image` (images.materialize does that)."""
    if isinstance(x, ImageRef) or (isinstance(x, dict) and x.get("type") == "image"):
        return True
    if isinstance(x, dict):
        return any(has_unprepared_image(v) for v in x.values())
    if isinstance(x, list):
        return any(has_unprepared_image(v) for v in x)
    return False
