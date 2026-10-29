"""How a number reads where s1flow shows it (the report, the check's PR comment, production from feedback, the CLI's
tables): a share in percent, its interval, a plain number, an API cost, a latency. Not known is a dash."""

from __future__ import annotations

DASH = "—"


def pct(x: float | None, digits: int = 0, *, none: str = DASH, sign: str = "%") -> str:
    """A share in percent: 0.853 -> 85%."""
    return none if x is None else f"{100 * x:.{digits}f}{sign}"


def band(r: tuple[float, float] | None, digits: int = 0) -> str:
    """A share's interval in percent, after its value: " [80, 90]"; nothing when there is none."""
    return "" if not r else f" [{100 * r[0]:.{digits}f}, {100 * r[1]:.{digits}f}]"


def num(x: float | None, digits: int = 2, *, none: str = DASH) -> str:
    return none if x is None else f"{x:.{digits}f}"


def usd(x: float | None, places: int | None = None, *, none: str = DASH) -> str:
    """An API cost: $0.31, and under a cent to four places ($0.0012) unless `places` fixes them."""
    if x is None:
        return none
    return f"${x:.{places if places is not None else 2 if x >= 0.01 else 4}f}"


def ms(x: float | None, *, none: str = "-") -> str:
    return none if x is None else f"{x:.0f}ms"
