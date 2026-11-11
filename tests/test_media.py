"""Audio, video and PDFs in a state: preparation, limits, the OpenRouter wire format, declarations and --verify's inputs (no network)."""

import argparse
import asyncio
import base64
import io
import json
import math
import struct
import wave
import zlib

import httpx
import pytest
import respx

from s1flow.cli.decide import _state
from s1flow.client import Capabilities, Choice, Media, media
from s1flow.client.identity import state_digest
from s1flow.client.models import check_supported
from s1flow.client.providers.cloudflare import CloudflareModel
from s1flow.client.providers.gateway import GatewayModel
from s1flow.client.providers.llm import user_content
from s1flow.client.providers.openai_decisions import DecisionsModel
from s1flow.client.providers.openrouter import BASE_URL as OR_URL, OpenRouterModel
from s1flow.client.providers.typesafe import TypeSafeModel
from s1flow.core.errors import DataError, Unsupported
from s1flow.policies.state_shape import mismatch, schema_of
from s1flow.project import verify

def tone(hz: int, rate: int = 16_000) -> bytes:
    """Half a second of a sine tone as a 16-bit mono WAV."""
    frames = [round(12_000 * math.sin(2 * math.pi * hz * i / rate)) for i in range(rate // 2)]
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(struct.pack(f"<{len(frames)}h", *frames))
    return buf.getvalue()


WAV = media.prepare("audio", tone(440))
MP3 = (verify.PROBES / "say-red.mp3").read_bytes()  # an ID3 tag of 35 bytes, then the frames
MP4 = (verify.PROBES / "red-blue.mp4").read_bytes()
PDF = base64.b64decode(verify.invoice(paid=True).data)
Q = {"callback": Choice(instructions="Call back?", criteria={"yes": None, "no": None})}


def raw(x: Media) -> bytes:
    return base64.b64decode(x.data)


@pytest.mark.parametrize("kind, data, media_type", [
    ("audio", raw(WAV), "audio/wav"), ("audio", MP3, "audio/mpeg"), ("audio", MP3[10 + 35:], "audio/mpeg"), ("video", MP4, "video/mp4"), ("pdf", PDF, "application/pdf"),
])
def test_prepare_keeps_the_files_own_bytes(kind, data, media_type):
    x = media.prepare(kind, data)
    assert isinstance(x, Media) and x.type == kind and x.media_type == media_type and raw(x) == data


@pytest.mark.parametrize("kind, data", [
    ("audio", b"OggS" + b"\x00" * 64),  # OGG: OpenRouter takes it, Workers AI's Clef Omni documents only WAV and MP3
    ("audio", b"\xff\xf1" + b"\x00" * 64),  # AAC in ADTS frames, not an MP3 frame
    ("video", b"\x1aE\xdf\xa3" + b"\x00" * 64),  # WebM
    ("pdf", MP4),
])
def test_prepare_refuses_formats_not_every_model_takes(kind, data):
    with pytest.raises(DataError, match="not "):
        media.prepare(kind, data)


def test_materialize_loads_media_and_leaves_counts_and_sizes_to_the_model(tmp_path):
    (tmp_path / "a.wav").write_bytes(raw(WAV))
    (tmp_path / "v.mp4").write_bytes(MP4)
    (tmp_path / "i.pdf").write_bytes(PDF)
    out = media.materialize(["留守電", {"type": "audio", "path": "a.wav"}, {"type": "video", "path": "v.mp4"}, {"type": "pdf", "path": "i.pdf"}], tmp_path)
    assert out[0] == "留守電" and [x.type for x in out[1:]] == ["audio", "video", "pdf"]
    with pytest.raises(DataError, match="top-level"):
        media.materialize({"call": {"type": "audio", "path": "a.wav"}}, tmp_path)
    with pytest.raises(DataError, match="audio file not found"):
        media.materialize([{"type": "audio", "path": "missing.wav"}], tmp_path)
    (tmp_path / "big.mp3").write_bytes(MP3 + b"\x00" * (17 * 1024 * 1024))  # past every model's limit: the model refuses it, not s1flow
    many = media.materialize([{"type": "audio", "path": "big.mp3"}] * 5 + [{"type": "pdf", "path": "i.pdf"}] * 2, tmp_path)
    assert [x.type for x in many] == ["audio"] * 5 + ["pdf"] * 2


def test_the_same_file_is_the_same_input_and_another_file_is_not(tmp_path):
    (tmp_path / "a.wav").write_bytes(raw(WAV))
    (tmp_path / "b.wav").write_bytes(tone(880))
    a = state_digest(media.materialize([{"type": "audio", "path": "a.wav"}], tmp_path))
    assert a == state_digest([media.prepare("audio", raw(WAV))])
    assert a != state_digest(media.materialize([{"type": "audio", "path": "b.wav"}], tmp_path))


@respx.mock
def test_openrouter_sends_chat_completions_parts(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "t")
    answers = {"callback": {"type": "choice", "choice": "yes", "probabilities": {"yes": 0.9, "no": 0.1}}}
    route = respx.post(f"{OR_URL}/systemone").mock(return_value=httpx.Response(200, json={"answers": answers}))
    mp3, video, pdf = media.prepare("audio", MP3), media.prepare("video", MP4), media.prepare("pdf", PDF)
    caps = Capabilities(audio=True, video=True, pdf=True)
    asyncio.run(OpenRouterModel("google/gemini-decision-1", capabilities=caps).decide(["留守電", WAV, mp3, video, pdf], Q))
    assert json.loads(route.calls[0].request.read())["state"] == [
        "留守電",
        {"type": "input_audio", "input_audio": {"data": WAV.data, "format": "wav"}},
        {"type": "input_audio", "input_audio": {"data": mp3.data, "format": "mp3"}},
        {"type": "video_url", "video_url": {"url": f"data:video/mp4;base64,{video.data}"}},
        {"type": "file", "file": {"file_data": f"data:application/pdf;base64,{pdf.data}"}},
    ]


def test_a_model_takes_only_the_kinds_it_declares():
    model = OpenRouterModel("cloudflare/clef-omni", capabilities=Capabilities(image=True, audio=True, video=True))
    check_supported(model, ["x", WAV], Q)
    with pytest.raises(Unsupported, match="does not take pdf"):
        check_supported(model, ["x", media.prepare("pdf", PDF)], Q)
    with pytest.raises(DataError, match="never prepared"):
        check_supported(model, ["x", {"type": "audio", "path": "a.wav"}], Q)


def test_app_data_that_only_mentions_a_kind_is_not_media(tmp_path):
    for state in (
        {"attachment": {"type": "video", "title": "demo"}},
        {"ticket": "refund", "attachments": [{"type": "pdf", "path": "/srv/inv/1.pdf", "name": "inv"}]},
        ["msg", {"type": "video", "url": "https://example.com/v", "title": "t"}],
    ):
        assert media.materialize(state, tmp_path) == state
        check_supported(OpenRouterModel("liquid/d1"), state, Q)


def test_a_mistyped_image_reference_is_still_an_error(tmp_path):
    with pytest.raises(DataError, match="bad media reference"):
        media.materialize(["x", {"type": "image", "file": "a.png"}], tmp_path)


def test_a_policy_shape_names_each_kind():
    shape = schema_of([["text", WAV]])
    assert mismatch(shape, ["text", WAV]) == []
    assert mismatch(shape, ["text", media.prepare("pdf", PDF)]) == ["state[1]: expected audio"]


def test_decide_adds_files_after_the_state(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "a.wav").write_bytes(raw(WAV))
    (tmp_path / "i.pdf").write_bytes(PDF)
    a = argparse.Namespace(state='"留守電"', image=None, audio=["a.wav"], video=None, pdf=["i.pdf"])
    state = _state(a)
    assert state[0] == "留守電" and [x.type for x in state[1:]] == ["audio", "pdf"]
    with pytest.raises(DataError, match="--audio"):
        _state(argparse.Namespace(state='[{"type":"audio","url":"http://127.0.0.1/x"}]', image=None, audio=None, video=None, pdf=None))


def test_verify_inputs_say_what_the_checks_ask():
    assert verify.saying("red").data != verify.saying("blue").data and verify.saying("red").media_type == "audio/mpeg"
    paid, unpaid = (base64.b64decode(verify.invoice(paid=p).data) for p in (True, False))
    assert b"PAID" not in paid  # compressed: the base64 read as text does not say it
    start = paid.index(b"stream\n") + len(b"stream\n")
    assert b"Status: PAID" in zlib.decompress(paid[start:paid.index(b"\nendstream")])
    assert paid != unpaid
    assert verify.clip("red", "blue").data != verify.clip("blue", "red").data


@pytest.mark.parametrize("model", [
    TypeSafeModel("jev-latest"), GatewayModel("liquid/d1"), DecisionsModel("gpt-6-luna"), CloudflareModel("clef"),
])
def test_a_provider_that_carries_only_images_refuses_other_media_before_the_call(model):
    with pytest.raises(Unsupported, match="cannot send audio, pdf"):
        model.request(["x", WAV, media.prepare("pdf", PDF)], Q)
    with pytest.raises(Unsupported, match="cannot send audio"):
        user_content(["x", WAV], Q)
