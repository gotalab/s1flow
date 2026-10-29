"""The one way s1flow writes a time: UTC, to the second, with a trailing `Z` (`2026-10-22T05:00:00Z`); a log to the
millisecond (`2026-10-22T05:00:00.123Z`). Every file s1flow writes names it `at`. Such strings sort as the times do.
"""

from __future__ import annotations

import datetime as dt


def stamp(t: dt.datetime, ms: bool = False) -> str:
    """`t` (an aware datetime) as s1flow writes it."""
    u = t.astimezone(dt.timezone.utc)
    return u.strftime("%Y-%m-%dT%H:%M:%S") + (f".{u.microsecond // 1000:03d}" if ms else "") + "Z"


def now(ms: bool = False) -> str:
    """The time now, as s1flow writes it (`ms`: to the millisecond, as a log is)."""
    return stamp(dt.datetime.now(dt.timezone.utc), ms)
