"""Images in a state (SPEC §4, §6): one common form, prepared once, translated per provider.

A task writes an image as `{"type": "image", "path": "shots/a.png"}` (relative to the task
dir) or `{"type": "image", "url": "https://..."}`, as a top-level item of a list state:

    state = ["Which screen is this?", {"type": "image", "path": row["shot"]}]

That is the only placement every image-taking provider can express (TypeSafe `assets`,
OpenRouter / AI Gateway `image_url` parts, OpenAI `input_image`, Workers AI `images[]`),
so images elsewhere in a state are a task error.

`materialize` turns each image into the same bytes for every model: EXIF rotation applied,
alpha flattened on white, resized and padded into the limits all providers share, and
encoded as PNG (JPEG when PNG is too large). Different pixels per provider would make a
model comparison an image comparison.
"""

from __future__ import annotations

import base64
import functools
import hashlib
import io
import json
import math
from pathlib import Path
from typing import Any

from typing import TYPE_CHECKING

from pydantic import ValidationError

from ..core.errors import ConfigError, DataError
from .state import Image, ImageRef, Part, State

if TYPE_CHECKING:  # Pillow and httpx load only when an image is prepared: a text-only app never needs them
    from PIL.Image import Image as PILImage

# The intersection of the providers' limits (2026-10-16):
# Jev: 256..1568 px a side, 78,400..2,458,624 px; Clef through OpenRouter: about 300 KB a file,
# and at most 4 images for Clef / Clef-flash.
SIDE_MIN, SIDE_MAX = 256, 1568
PIXELS_MIN, PIXELS_MAX = 78_400, 2_458_624
BYTES_MAX = 300_000
MAX_IMAGES = 4


def _is_ref(x: Any) -> bool:
    return isinstance(x, (Image, ImageRef)) or (isinstance(x, dict) and x.get("type") == "image")


def _fit(im: PILImage) -> PILImage:
    from PIL import Image as PIL

    w, h = im.size
    area = w * h
    up = max(SIDE_MIN / min(w, h), math.sqrt(PIXELS_MIN / area))
    s = up if up > 1 else min(1.0, SIDE_MAX / max(w, h), math.sqrt(PIXELS_MAX / area))
    s = min(s, SIDE_MAX / max(w, h))  # a very long image is padded below instead of overflowing
    if s != 1:
        im = im.resize((max(1, round(w * s)), max(1, round(h * s))), PIL.Resampling.LANCZOS)
    w, h = im.size
    if min(w, h) < SIDE_MIN or w * h < PIXELS_MIN:
        long_ = max(w, h)
        short = max(min(w, h), SIDE_MIN, math.ceil(PIXELS_MIN / long_))
        size = (long_, short) if w >= h else (short, long_)
        canvas = PIL.new("RGB", size, "white")
        canvas.paste(im, ((size[0] - w) // 2, (size[1] - h) // 2))
        im = canvas
    return im


def _encode(im: PILImage) -> tuple[bytes, str]:
    from PIL import Image as PIL

    while True:
        buf = io.BytesIO()
        im.save(buf, "PNG", optimize=True)
        if buf.tell() <= BYTES_MAX:
            return buf.getvalue(), "image/png"
        for quality in (90, 80, 70, 60):
            buf = io.BytesIO()
            im.save(buf, "JPEG", quality=quality)
            if buf.tell() <= BYTES_MAX:
                return buf.getvalue(), "image/jpeg"
        w, h = im.size
        if min(w, h) * 0.8 < SIDE_MIN:
            raise DataError(f"image does not fit in {BYTES_MAX} bytes at the smallest allowed size")
        im = im.resize((round(w * 0.8), round(h * 0.8)), PIL.Resampling.LANCZOS)


def prepare(raw: bytes) -> Image:
    """Raw image bytes -> the prepared image every provider receives."""
    try:
        from PIL import Image as PIL
        from PIL import ImageOps
    except ModuleNotFoundError:
        raise ConfigError("preparing an image needs Pillow: install s1flow[images]") from None

    try:
        src = PIL.open(io.BytesIO(raw))
    except OSError as e:
        raise DataError(f"not an image: {e}") from e
    with src:
        if getattr(src, "is_animated", False):
            raise DataError("animated images are not accepted (Jev rejects animated PNGs)")
        im = ImageOps.exif_transpose(src)
        if im.mode in ("RGBA", "LA", "P"):
            rgba = im.convert("RGBA")
            im = PIL.new("RGB", rgba.size, "white")
            im.paste(rgba, mask=rgba.split()[3])
        else:
            im = im.convert("RGB")
    data, media_type = _encode(_fit(im))
    with PIL.open(io.BytesIO(data)) as out:
        width, height = out.size
    return Image.model_validate({
        "media_type": media_type,
        "data": base64.b64encode(data).decode(),
        "sha256": hashlib.sha256(data).hexdigest(),
        "width": width,
        "height": height,
    })


@functools.lru_cache(maxsize=256)
def _prepare_file(path: str, mtime_ns: int) -> Image:
    return prepare(Path(path).read_bytes())


@functools.lru_cache(maxsize=256)
def _prepare_url(url: str) -> Image:
    import httpx

    try:
        r = httpx.get(url, follow_redirects=True, timeout=60)
        r.raise_for_status()
    except httpx.HTTPError as e:
        raise DataError(f"cannot fetch image {url}: {e}") from e
    return prepare(r.content)


def _load(item: Any, base_dir: Path) -> Image:
    if isinstance(item, Image):
        return item
    try:
        ref = item if isinstance(item, ImageRef) else ImageRef.model_validate(item)
    except ValidationError as e:
        raise DataError(f"bad image reference {item!r}: {e.errors()[0]['msg']}") from e
    if ref.path is not None:
        p = (base_dir / ref.path).resolve()
        if not p.is_file():
            raise DataError(f"image file not found: {p}")
        return _prepare_file(str(p), p.stat().st_mtime_ns)
    assert ref.url is not None
    return _prepare_url(ref.url)


def _nested_image(x: Any) -> bool:
    if _is_ref(x):
        return True
    if isinstance(x, dict):
        return any(_nested_image(v) for v in x.values())
    if isinstance(x, list):
        return any(_nested_image(v) for v in x)
    return False


def materialize(state: Any, base_dir: Path) -> State:
    """Load and prepare the images of a state. A state without images comes back unchanged.
    Raises DataError for images in the wrong place, too many, or that cannot be loaded."""
    if not isinstance(state, list):
        if _nested_image(state):
            raise DataError("images go as top-level items of a list state, e.g. ['text', {'type': 'image', 'path': ...}]")
        return state  # type: ignore[no-any-return]
    if any(not _is_ref(x) and _nested_image(x) for x in state):
        raise DataError("images go as top-level items of a list state, not inside other items")
    n = sum(_is_ref(x) for x in state)
    if n > MAX_IMAGES:
        raise DataError(f"{n} images in one state; at most {MAX_IMAGES} (Clef's limit)")
    return [_load(x, base_dir) if _is_ref(x) else x for x in state] if n else state


# Translations. Each takes a state that has_image() narrowed to a list of parts.


def data_url(img: Image) -> str:
    return f"data:{img.media_type};base64,{img.data}"


def text_of(item: Part) -> str:
    return item if isinstance(item, str) else json.dumps(item, ensure_ascii=False, indent=1)


def typesafe_assets(state: list[Part]) -> tuple[list[Part], dict[str, dict[str, str]]]:
    """TypeSafe: each image becomes a reference string, the bytes go in top-level `assets`."""
    out: list[Part] = []
    assets: dict[str, dict[str, str]] = {}
    for item in state:
        if isinstance(item, Image):
            ref = f"jevfit-image-{len(assets) + 1}"
            fmt = "png" if item.media_type == "image/png" else "jpeg"
            assets[ref] = {"type": "image", "data_base64": item.data, "format": fmt}
            out.append(ref)
        else:
            out.append(item)
    return out, assets


def image_url_parts(state: list[Part]) -> list[Part]:
    """OpenRouter (documented) and AI Gateway's d1 (works, undocumented): `image_url` parts in the state array."""
    return [{"type": "image_url", "image_url": {"url": data_url(x)}} if isinstance(x, Image) else x for x in state]


def openai_content(state: list[Part]) -> list[dict[str, str]]:
    """OpenAI Decisions: one user message whose content alternates `input_text` and `input_image`."""
    return [
        {"type": "input_image", "image_url": data_url(x)} if isinstance(x, Image) else {"type": "input_text", "text": text_of(x)}
        for x in state
    ]


def placeholders(state: list[Part]) -> tuple[list[Part], list[Image]]:
    """Workers AI and the LLM baseline take images apart from the text: `[image n]` marks where each one was."""
    out: list[Part] = []
    imgs: list[Image] = []
    for item in state:
        if isinstance(item, Image):
            imgs.append(item)
            out.append(f"[image {len(imgs)}]")
        else:
            out.append(item)
    return out, imgs
