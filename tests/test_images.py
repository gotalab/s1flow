"""Image preparation and each provider's image wire format (no network)."""

import asyncio
import base64
import io
import json

import httpx
import pytest
import respx
from PIL import Image as PILImage

from s1flow.client import Capabilities, Choice, Image, images
from s1flow.client.endpoints import cloudflare_relay
from s1flow.client.providers.cloudflare import CloudflareModel
from s1flow.client.providers.gateway import BASE_URL as GW_URL, GatewayModel
from s1flow.client.providers.llm import user_content
from s1flow.client.providers.openai_decisions import BASE_URL as OPENAI_URL, DecisionsModel
from s1flow.client.providers.openrouter import BASE_URL as OR_URL, OpenRouterModel
from s1flow.client.providers.typesafe import BASE_URL as TS_URL, TypeSafeModel
from s1flow.core.errors import DataError

Q = {"screen": Choice(instructions="どの画面か", criteria={"signin": None, "error": None})}
IMG = Capabilities(image=True)


def png(size, mode="RGB", colour=(200, 0, 0)) -> bytes:
    buf = io.BytesIO()
    PILImage.new(mode, size, colour).save(buf, "PNG")
    return buf.getvalue()


def decoded(img) -> PILImage.Image:
    return PILImage.open(io.BytesIO(base64.b64decode(img.data)))


@pytest.mark.parametrize("size", [(100, 80), (4000, 3000), (3000, 120), (300, 300)])
def test_prepare_fits_every_provider(size):
    img = images.prepare(png(size))
    w, h = decoded(img).size
    assert images.SIDE_MIN <= min(w, h) and max(w, h) <= images.SIDE_MAX
    assert images.PIXELS_MIN <= w * h <= images.PIXELS_MAX
    assert len(base64.b64decode(img.data)) <= images.BYTES_MAX
    assert (img.width, img.height) == (w, h)


def test_prepare_flattens_alpha_and_applies_exif_rotation():
    assert decoded(images.prepare(png((300, 300), "RGBA", (0, 0, 0, 0)))).getpixel((150, 150)) == (255, 255, 255)
    im = PILImage.new("RGB", (400, 300), "red")
    exif = im.getexif()
    exif[0x0112] = 6  # rotate 90° on display
    buf = io.BytesIO()
    im.save(buf, "JPEG", exif=exif)
    assert decoded(images.prepare(buf.getvalue())).size == (300, 400)


def test_materialize_loads_paths_once_and_rejects_bad_placement(tmp_path):
    (tmp_path / "a.png").write_bytes(png((300, 300)))
    state = ["画面", {"type": "image", "path": "a.png"}]
    out = images.materialize(state, tmp_path)
    assert out[0] == "画面" and isinstance(out[1], Image) and out[1].sha256
    assert images.materialize("text only", tmp_path) == "text only"
    with pytest.raises(DataError, match="top-level"):
        images.materialize({"shot": {"type": "image", "path": "a.png"}}, tmp_path)
    with pytest.raises(DataError, match="at most"):
        images.materialize([{"type": "image", "path": "a.png"}] * 5, tmp_path)
    with pytest.raises(DataError, match="not found"):
        images.materialize([{"type": "image", "path": "missing.png"}], tmp_path)
    with pytest.raises(DataError, match="exactly one"):
        images.materialize([{"type": "image", "path": "a.png", "url": "https://x"}], tmp_path)


STATE = ["画面", images.prepare(png((300, 300)))]
CHOICE = {"screen": {"type": "choice", "choice": "error", "probabilities": {"signin": 0.1, "error": 0.9}}}


@respx.mock
def test_typesafe_sends_assets_and_the_danger_zone_header(monkeypatch):
    monkeypatch.setenv("TYPESAFE_API_KEY", "t")
    route = respx.post(f"{TS_URL}/systemone").mock(return_value=httpx.Response(200, json={"model": "jev-1.14.0", "answers": CHOICE}))
    asyncio.run(TypeSafeModel("jev-latest", capabilities=IMG).decide(STATE, Q))
    req = route.calls[0].request
    body = json.loads(req.read())
    assert req.headers["typesafe-danger-zone-images"] == "true"
    assert body["state"] == ["画面", "jevfit-image-1"]
    assert body["assets"]["jevfit-image-1"] == {"type": "image", "data_base64": STATE[1].data, "format": "png"}


@respx.mock
def test_typesafe_text_requests_are_unchanged(monkeypatch):
    monkeypatch.setenv("TYPESAFE_API_KEY", "t")
    route = respx.post(f"{TS_URL}/systemone").mock(return_value=httpx.Response(200, json={"model": "jev-1.14.0", "answers": CHOICE}))
    asyncio.run(TypeSafeModel("jev-latest", capabilities=IMG).decide(["画面"], Q))
    req = route.calls[0].request
    assert "assets" not in json.loads(req.read()) and "typesafe-danger-zone-images" not in req.headers


@respx.mock
def test_openrouter_and_gateway_send_image_url_parts(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "t")
    monkeypatch.setenv("AI_GATEWAY_API_KEY", "t")
    orr = respx.post(f"{OR_URL}/systemone").mock(return_value=httpx.Response(200, json={"answers": CHOICE}))
    gw = respx.post(f"{GW_URL}/evaluate").mock(return_value=httpx.Response(200, json={"answers": CHOICE}))
    asyncio.run(OpenRouterModel("typesafe/jev-1.13", capabilities=IMG).decide(STATE, Q))
    asyncio.run(GatewayModel("liquid/d1", capabilities=IMG).decide(STATE, Q))
    part = {"type": "image_url", "image_url": {"url": images.data_url(STATE[1])}}
    for route in (orr, gw):
        body = json.loads(route.calls[0].request.read())
        assert body["state"] == ["画面", part] and "assets" not in body


@respx.mock
def test_decisions_sends_one_user_message_with_input_image(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "t")
    answers = [{"type": "choice", "name": "screen", "choice": "error", "probabilities": [{"value": "error", "probability": 1}]}]
    route = respx.post(f"{OPENAI_URL}/decisions").mock(return_value=httpx.Response(200, json={"answers": answers}))
    asyncio.run(DecisionsModel("gpt-6-luna", capabilities=IMG).decide(STATE, Q))
    body = json.loads(route.calls[0].request.read())
    assert body["input"] == [{"role": "user", "content": [
        {"type": "input_text", "text": "画面"}, {"type": "input_image", "image_url": images.data_url(STATE[1])},
    ]}]


@respx.mock
def test_clef_sends_images_apart_with_placeholders():
    route = respx.post(f"{cloudflare_relay()}/run/@cf/cloudflare/clef").mock(return_value=httpx.Response(200, json={"result": {"answers": CHOICE}}))
    asyncio.run(CloudflareModel("clef", capabilities=IMG).decide(STATE, Q))
    body = json.loads(route.calls[0].request.read())
    assert body["state"] == ["画面", "[image 1]"] and body["images"] == [images.data_url(STATE[1])]


def test_an_untranslated_image_cannot_be_sent_as_text():
    import json as json_

    with pytest.raises(TypeError):
        json_.dumps({"state": STATE})


def test_llm_puts_images_after_the_prompt():
    content = user_content(STATE, Q)
    assert "[image 1]" in content[0]["text"] and STATE[1].data not in content[0]["text"]
    assert content[1] == {"type": "image_url", "image_url": {"url": images.data_url(STATE[1])}}
    assert isinstance(user_content(["画面"], Q), str)
