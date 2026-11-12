"""What a decision model reads: a state of text, JSON, or a list of parts whose media are prepared."""

from typing import Any, Literal, TypeGuard

from pydantic import BaseModel, ConfigDict, model_validator


MediaKind = Literal["image", "audio", "video", "pdf"]
MEDIA_KINDS: tuple[MediaKind, ...] = ("image", "audio", "video", "pdf")


class MediaRef(BaseModel):
    """Media as a task writes it: `{"type": "audio", "path": "calls/a.mp3"}` (relative to the task dir)
    or `{"type": "image", "url": ...}`. It is turned into an `Image` or `Media` (media.materialize) before any call."""

    model_config = ConfigDict(extra="forbid")
    type: MediaKind
    path: str | None = None
    url: str | None = None

    @model_validator(mode="after")
    def _one_source(self) -> "MediaRef":
        if (self.path is None) == (self.url is None):
            raise ValueError(f"{self.type} needs exactly one of path or url")
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


class Media(BaseModel):
    """Prepared audio, video or PDF (media.prepare): the file's own bytes, unchanged, go to every model."""

    model_config = ConfigDict(frozen=True, extra="forbid")
    type: Literal["audio", "video", "pdf"]
    media_type: Literal["audio/wav", "audio/mpeg", "video/mp4", "application/pdf"]
    data: str  # base64
    sha256: str


# A state is text, JSON, or a list of parts. Media are only top-level parts of a list
# (the one placement every provider can express); `Image` and `Media` are not JSON-serializable,
# so a provider that forgets to translate one fails before sending it as text.
Part = str | dict[str, Any] | list[Any] | int | float | bool | None | Image | Media
State = str | dict[str, Any] | list[Part]


def sorted_keys(state: State) -> State:
    """The state with every object's keys in sorted order, as every model receives it. Key order is no
    difference to the request identity (identity.digest sorts keys), so it is none to what is sent either:
    an evaluation case and a production call that differ only in key order send the same request."""
    sent: State = _sorted(state)
    return sent


def _sorted(x: Any) -> Any:
    if isinstance(x, dict):
        return {k: _sorted(x[k]) for k in sorted(x, key=str)}  # by the key as JSON writes it, as identity.digest
    if isinstance(x, (list, tuple)):
        return [_sorted(v) for v in x]
    return x


def has_image(state: State) -> TypeGuard[list[Part]]:
    return isinstance(state, list) and any(isinstance(x, Image) for x in state)


def has_media(state: State) -> TypeGuard[list[Part]]:
    """Any prepared image, audio, video or PDF in the state."""
    return bool(kinds_in(state))


def kinds_in(state: State) -> set[MediaKind]:
    """The kinds of prepared media in a state: what a model must declare it takes."""
    if not isinstance(state, list):
        return set()
    return {x.type for x in state if isinstance(x, (Image, Media))}


# The exact key sets that make a dict audio, video or a PDF: a reference, or a prepared one read back from JSON.
# An app's own `{"type": "video", "url": ..., "title": ...}` has other keys too, so it stays data.
_MEDIA_KEYS = ({"type", "path"}, {"type", "url"}, {"type", "media_type", "data", "sha256"})


def is_media_dict(x: Any) -> bool:
    """A dict that stands for media. Any `{"type": "image", ...}` is an image (as before audio, video and PDFs came),
    so a mistyped image reference is an error; audio, video and PDFs need one of the exact shapes above."""
    if not isinstance(x, dict):
        return False
    if x.get("type") == "image":
        return True
    return x.get("type") in MEDIA_KINDS and set(x) in _MEDIA_KEYS


def has_unprepared_media(x: Any) -> bool:
    """A media reference anywhere that was never turned into an `Image` or `Media` (media.materialize does that)."""
    if isinstance(x, MediaRef) or is_media_dict(x):
        return True
    if isinstance(x, dict):
        return any(has_unprepared_media(v) for v in x.values())
    if isinstance(x, list):
        return any(has_unprepared_media(v) for v in x)
    return False
