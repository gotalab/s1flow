"""Image preparation: one common form for every model (media.py places images in a state and translates them).

`prepare` turns each image into the same bytes for every model: EXIF rotation applied,
alpha flattened on white, resized and padded into the limits all providers share, and
encoded as PNG (JPEG when PNG is too large). Different pixels per provider would make a
model comparison an image comparison.
"""

import base64
import hashlib
import io
import math
from typing import TYPE_CHECKING

from ..core.errors import ConfigError, DataError
from .state import Image

if TYPE_CHECKING:  # Pillow loads only when an image is prepared: a text-only app never needs it
    from PIL.Image import Image as PILImage

# The intersection of the providers' limits (2026-10-16):
# Jev: 256..1568 px a side, 78,400..2,458,624 px; Clef through OpenRouter: about 300 KB a file.
# These keep the pixels the same for every model; how many images a model takes is its own limit.
SIDE_MIN, SIDE_MAX = 256, 1568
PIXELS_MIN, PIXELS_MAX = 78_400, 2_458_624
BYTES_MAX = 300_000


def _fit(im: "PILImage") -> "PILImage":
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


def _encode(im: "PILImage") -> tuple[bytes, str]:
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
