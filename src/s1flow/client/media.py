"""Media in a state (SPEC §4, §6): images, audio, video and PDFs, prepared once, translated per provider.

A task writes media as a top-level item of a list state, by path (relative to the task dir) or URL:

    state = ["A voicemail:", {"type": "audio", "path": row["call"]}]

That is the only placement every media-taking provider can express (OpenRouter's parts in the
state array, TypeSafe `assets`, OpenAI `input_image`, Google's content blocks, Workers AI's own arrays), so media elsewhere
in a state are a task error.

Images are resized and re-encoded (images.prepare). Audio, video and PDFs are sent as the file's
own bytes, never transcoded, in the formats every model that reads them takes (2026-11-11:
Gemini Decision 1, Clef Omni, ScaleDown Classify 1): WAV or MP3, MP4, PDF. s1flow checks the format,
because it must name it on the wire, and nothing else: how many and how large is each model's own
limit, and a model that refuses an input says so (Rejected), which an evaluation counts as refused.
"""

import base64
import functools
import hashlib
import json
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from ..core.errors import DataError, Unsupported
from . import images
from .state import Image, kinds_in, Media, MediaKind, MediaRef, Part, State, is_media_dict

def _sniff(kind: MediaKind, raw: bytes) -> str | None:
    """The media type the bytes are, among those `kind` accepts; None when they are none of them."""
    if kind == "audio":
        if raw[:4] == b"RIFF" and raw[8:12] == b"WAVE":
            return "audio/wav"
        if raw[:3] == b"ID3" or (len(raw) > 1 and raw[0] == 0xFF and raw[1] & 0xE6 == 0xE2):  # an MPEG Layer III frame
            return "audio/mpeg"
    elif kind == "video":
        if raw[4:8] == b"ftyp":
            return "video/mp4"
    elif kind == "pdf":
        if raw[:5] == b"%PDF-":
            return "application/pdf"
    return None


ACCEPTED = {"audio": "WAV or MP3", "video": "MP4", "pdf": "PDF"}


def prepare(kind: MediaKind, raw: bytes) -> Image | Media:
    """Raw bytes -> what every provider receives. Images are resized and re-encoded; the rest are checked, not changed."""
    if kind == "image":
        return images.prepare(raw)
    media_type = _sniff(kind, raw)
    if media_type is None:
        raise DataError(f"not {ACCEPTED[kind]}: {kind} is sent as the file's own bytes, so only the formats every model takes are accepted")
    return Media.model_validate({"type": kind, "media_type": media_type, "data": base64.b64encode(raw).decode(),
                                 "sha256": hashlib.sha256(raw).hexdigest()})


@functools.lru_cache(maxsize=256)
def _prepare_file(kind: MediaKind, path: str, mtime_ns: int) -> Image | Media:
    return prepare(kind, Path(path).read_bytes())


@functools.lru_cache(maxsize=256)
def _prepare_url(kind: MediaKind, url: str) -> Image | Media:
    import httpx

    try:
        r = httpx.get(url, follow_redirects=True, timeout=60)
        r.raise_for_status()
    except httpx.HTTPError as e:
        raise DataError(f"cannot fetch {kind} {url}: {e}") from e
    return prepare(kind, r.content)


def _is_ref(x: Any) -> bool:
    return isinstance(x, (Image, Media, MediaRef)) or is_media_dict(x)


def _load(item: Any, base_dir: Path) -> Image | Media:
    if isinstance(item, (Image, Media)):
        return item
    try:
        ref = item if isinstance(item, MediaRef) else MediaRef.model_validate(item)
    except ValidationError as e:
        raise DataError(f"bad media reference {item!r}: {e.errors()[0]['msg']}") from e
    if ref.path is not None:
        p = (base_dir / ref.path).resolve()
        if not p.is_file():
            raise DataError(f"{ref.type} file not found: {p}")
        return _prepare_file(ref.type, str(p), p.stat().st_mtime_ns)
    assert ref.url is not None
    return _prepare_url(ref.type, ref.url)


def _nested(x: Any) -> bool:
    if _is_ref(x):
        return True
    if isinstance(x, dict):
        return any(_nested(v) for v in x.values())
    if isinstance(x, list):
        return any(_nested(v) for v in x)
    return False


def materialize(state: Any, base_dir: Path) -> State:
    """Load and prepare the media of a state. A state without media comes back unchanged.
    Raises DataError for media in the wrong place, in a format s1flow does not send, or that cannot be loaded."""
    if not isinstance(state, list):
        if _nested(state):
            raise DataError("media go as top-level items of a list state, e.g. ['text', {'type': 'audio', 'path': ...}]")
        return state  # type: ignore[no-any-return]
    if any(not _is_ref(x) and _nested(x) for x in state):
        raise DataError("media go as top-level items of a list state, not inside other items")
    if not any(_is_ref(x) for x in state):
        return state
    return [_load(x, base_dir) if _is_ref(x) else x for x in state]


# Translations. Each takes a state that has_media() narrowed to a list of parts.


def images_only(state: State, provider: str) -> None:
    """For a provider whose API carries images and no other media: audio, video or a PDF is refused before the call,
    not serialized into a request it cannot express."""
    other = kinds_in(state) - {"image"}
    if other:
        raise Unsupported(f"{provider} cannot send {', '.join(sorted(other))}")


def data_url(x: Image | Media) -> str:
    return f"data:{x.media_type};base64,{x.data}"


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


def chat_parts(state: list[Part]) -> list[Part]:
    """OpenRouter (documented) and AI Gateway's d1 (images only; works, undocumented): Chat Completions'
    content parts in the state array. Audio is raw base64 with a format; video and PDFs are data URLs."""
    out: list[Part] = []
    for x in state:
        if isinstance(x, Image):
            out.append({"type": "image_url", "image_url": {"url": data_url(x)}})
        elif isinstance(x, Media) and x.type == "audio":
            out.append({"type": "input_audio", "input_audio": {"data": x.data, "format": "wav" if x.media_type == "audio/wav" else "mp3"}})
        elif isinstance(x, Media) and x.type == "video":
            out.append({"type": "video_url", "video_url": {"url": data_url(x)}})
        elif isinstance(x, Media):
            out.append({"type": "file", "file": {"file_data": data_url(x)}})
        else:
            out.append(x)
    return out


GEMINI_BLOCKS = {"image": "image", "audio": "audio", "video": "video", "pdf": "document"}


def gemini_blocks(state: list[Part]) -> list[dict[str, str]]:
    """Google's Decisions API: content blocks (`text`, `image`, `audio`, `video`, `document`) with base64 `data`.
    It joins adjacent text blocks with no separator, so adjacent text parts go as one block, a newline between."""
    out: list[dict[str, str]] = []
    for x in state:
        if isinstance(x, (Image, Media)):
            out.append({"type": GEMINI_BLOCKS[x.type], "data": x.data, "mime_type": x.media_type})
        elif out and out[-1]["type"] == "text":
            out[-1]["text"] += "\n" + text_of(x)
        else:
            out.append({"type": "text", "text": text_of(x)})
    return out
