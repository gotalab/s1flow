"""Per-token prices from the AI Gateway model list, fetched once per process (and kept for a day in
the project's cache when there is one)."""

from __future__ import annotations

import json
import os
import time
from pathlib import Path

MODELS_URL = "https://ai-gateway.vercel.sh/v1/models"
_prices: dict[str, tuple[float, float]] | None = None


def _load(cache_dir: Path | None) -> dict[str, tuple[float, float]]:
    global _prices
    if _prices is not None:
        return _prices
    path = cache_dir / "gateway-models.json" if cache_dir else None
    if path and path.exists() and time.time() - path.stat().st_mtime < 86_400:
        text = path.read_text()
    else:
        import httpx

        key = os.environ.get("AI_GATEWAY_API_KEY")  # the list is public; a key, when set, is sent as the calls send it
        r = httpx.get(MODELS_URL, headers={"Authorization": f"Bearer {key}"} if key else {}, timeout=30)
        r.raise_for_status()
        text = r.text
        if path:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
    _prices = {
        m["id"]: (float(m["pricing"].get("input", 0)), float(m["pricing"].get("output", 0)))
        for m in json.loads(text)["data"]
        if m.get("pricing")
    }
    return _prices


def listed(gateway_model_id: str, cache_dir: Path | None = None) -> tuple[float, float] | None:
    """(USD per input token, per output token) on the gateway's list; None when the model is not on it."""
    return _load(cache_dir).get(gateway_model_id)


def cost(gateway_model_id: str, input_tokens: int, output_tokens: int, cache_dir: Path | None = None) -> float | None:
    p = listed(gateway_model_id, cache_dir)
    return None if p is None else p[0] * input_tokens + p[1] * output_tokens
