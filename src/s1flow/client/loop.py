"""The one event loop the blocking calls run on (`Client`, and a policy's `decide`).

It runs in a background thread that every caller shares, so a blocking call works from any thread (or
under a running loop), keeps the HTTP connections between calls, and carries the caller's context (an
OTel parent span).
"""

from __future__ import annotations

import asyncio
import contextvars
import threading
from collections.abc import Coroutine
from typing import Any, TypeVar

T = TypeVar("T")
_loop: asyncio.AbstractEventLoop | None = None
_loop_lock = threading.Lock()


def _background_loop() -> asyncio.AbstractEventLoop:
    global _loop
    with _loop_lock:
        if _loop is None:
            _loop = asyncio.new_event_loop()
            threading.Thread(target=_loop.run_forever, name="s1flow-client", daemon=True).start()
        return _loop


def run(coro: Coroutine[Any, Any, T]) -> T:
    """Run a coroutine on the background loop, in a copy of the caller's context, and wait for it."""
    ctx = contextvars.copy_context()

    async def in_context() -> T:
        return await asyncio.get_running_loop().create_task(coro, context=ctx)

    return asyncio.run_coroutine_threadsafe(in_context(), _background_loop()).result()
