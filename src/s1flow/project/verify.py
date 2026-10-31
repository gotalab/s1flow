"""`s1flow models --verify`: does a model really take what s1flow.toml declares? (the contract test)

A 200 is not proof: AI Gateway and OpenRouter answered images they never saw, at chance
(2026-10-15). The check asks each model, through its own provider code, questions whose
answer is plain, and checks every claim a `Capabilities` can make:

| check     | asks                                                         | passes when                         |
|-----------|--------------------------------------------------------------|-------------------------------------|
| `boolean` | is the light red? on a red light, then a green one            | P(true) >= PASS, then <= 1 - PASS    |
| `choice`  | the car's colour, on a blue car, then a red one               | the colour, with p >= PASS, twice    |
| `score`   | how many apples (levels 0-3), on three apples, then one       | within 0.5 of the count, twice       |
| `image`   | the disc's colour, on a red disc, then a blue one             | the colour, with p >= PASS, twice    |
| `images`  | both discs in one state, red first                            | both colours in order                |
| `box`     | the box of a disc off-centre in a 4:3 image                   | IoU >= BOX_PASS                      |

Every check runs whatever the model declares, so a claim that fails and a capability nobody
declared both show. `images` and `box` need `image` to pass first. The results go to
models.verified.json beside s1flow.toml, which `s1flow models` shows next to the declarations.
A model whose key is not set is not asked (`unset_keys`): nothing is recorded for it, since a missing
key says nothing about what the model takes.

A model with a `price` in s1flow.toml has it compared with the list its provider says it is published in
(`@publishes`, client/providers/published.py): a price that differs, or one read more than `STALE_DAYS` ago,
is a warning, not a failure. A provider that declares no list cannot have its price checked, and says so.
"""

from __future__ import annotations

import asyncio
import datetime as dt
import io
import json
import math
import os
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Literal, TypeVar

from pydantic import BaseModel, ConfigDict, Field

from ..client import AsyncClient, images
from ..core import clock
from ..client.answers import Answer, BooleanAnswer, BoxAnswer, BoxEdges, ChoiceAnswer, Response, ScoreAnswer
from ..client.boxes import iou
from ..client import providers
from ..client.models import Capabilities, DecisionModel, ModelSpec, Price
from ..client.providers.needs import where_to_get
from ..client.questions import Boolean, Box, Choice, Questions, Score
from ..client.state import Image, Part, State
from ..core.errors import ProviderError, S1flowError
from . import Project

if TYPE_CHECKING:
    from PIL import Image as PILImage

PASS = 0.6
BOX_PASS = 0.5
CheckName = Literal["boolean", "choice", "score", "image", "images", "box"]
EVERYTHING = Capabilities(image=True, question_types=frozenset({"boolean", "choice", "score", "box"}))


class Check(BaseModel):
    model_config = ConfigDict(extra="forbid")
    ok: bool
    detail: str  # what came back, or the error


class Verification(BaseModel):
    """One model's results (models.verified.json)."""

    model_config = ConfigDict(extra="forbid")
    at: str
    answered_by: str | None = None  # the model that answered
    checks: dict[CheckName, Check]


def claims(caps: Capabilities) -> dict[CheckName, bool]:
    """What a declaration says each check should do."""
    return {
        "boolean": "boolean" in caps.question_types,
        "choice": "choice" in caps.question_types,
        "score": "score" in caps.question_types,
        "image": caps.image,
        "images": caps.image,
        "box": caps.image and "box" in caps.question_types,
    }


def disagreements(caps: Capabilities, v: Verification) -> tuple[list[CheckName], list[CheckName]]:
    """(declared but failed, passed but not declared)."""
    said = claims(caps)
    failed = [c for c, r in v.checks.items() if said[c] and not r.ok]
    undeclared = [c for c, r in v.checks.items() if r.ok and not said[c]]
    return failed, undeclared


# ---------- what is asked ----------

COLOURS = {"red": (220, 30, 30), "blue": (30, 60, 220)}
COLOUR: Questions = {
    "colour": Choice(
        instructions="What colour is the disc in the picture?",
        criteria={"red": "The disc is red", "blue": "The disc is blue", "green": "The disc is green"},
    )
}
PAIR: Questions = {
    "first": Choice(instructions="What colour is the disc in the FIRST picture?", criteria={"red": None, "blue": None, "green": None}),
    "second": Choice(instructions="What colour is the disc in the SECOND picture?", criteria={"red": None, "blue": None, "green": None}),
}
LIGHT: Questions = {"red": Boolean(instructions="Is the traffic light in the text red?")}
CAR: Questions = {
    "colour": Choice(
        instructions="What colour is Ken's car?",
        criteria={"red": "The car is red", "blue": "The car is blue", "green": "The car is green"},
    )
}
APPLES: Questions = {
    "apples": Score(
        instructions="How many apples does Mia have?",
        criteria=["Mia has no apples", "Mia has one apple", "Mia has two apples", "Mia has three apples"],
    )
}
# A 400x300 image with a disc at x 40..160, y 40..160: the box as fractions of width and height.
BOX_TRUTH = BoxEdges(top=40 / 300, bottom=160 / 300, left=40 / 400, right=160 / 400)
BOX_Q: Questions = {"disc": Box(instructions="the red disc in the picture")}


def _png(im: PILImage.Image) -> Image:
    buf = io.BytesIO()
    im.save(buf, "PNG")
    return images.prepare(buf.getvalue())


def disc(rgb: tuple[int, int, int]) -> Image:
    from PIL import Image as PILImage, ImageDraw  # s1flow[images], only when a model declares it reads images

    im = PILImage.new("RGB", (320, 320), "white")
    ImageDraw.Draw(im).ellipse((60, 60, 260, 260), fill=rgb)
    return _png(im)


def box_image() -> Image:
    from PIL import Image as PILImage, ImageDraw

    im = PILImage.new("RGB", (400, 300), "white")
    ImageDraw.Draw(im).ellipse((40, 40, 160, 160), fill=COLOURS["red"])
    return _png(im)


# ---------- reading the answers ----------


A = TypeVar("A", BooleanAnswer, ChoiceAnswer, ScoreAnswer, BoxAnswer)


def _as(kind: type[A], a: Answer) -> A:
    if not isinstance(a, kind):
        raise ProviderError(f"answered {a.type}" + (f": {a.reason}" if a.type == "refusal" and a.reason else ""))
    return a


def _p(a: ChoiceAnswer, want: str) -> float:
    return (a.probabilities or {}).get(want, 1.0 if a.choice == want else 0.0)


def _level(x: float | None) -> str:
    return "none" if x is None else f"{x:.2f}"


def _picked(answer: Answer, want: str) -> tuple[bool, str]:
    a = _as(ChoiceAnswer, answer)
    p = _p(a, want)
    return a.choice == want and p >= PASS, f"{a.choice} {p:.2f}"


class _Probe:
    """One model's checks; remembers which model answered."""

    def __init__(self, client: AsyncClient, model: DecisionModel):
        self.client = client
        self.model = model
        self.answered_by: str | None = None

    async def ask(self, state: State, questions: Questions) -> Response:
        r = await self.client.responses.create(model=self.model, state=state, questions=questions)
        self.answered_by = self.answered_by or r.answered_by
        return r

    async def check(self, name: CheckName) -> Check:
        asks = {
            "boolean": self._boolean, "choice": self._choice, "score": self._score,
            "image": self._image, "images": self._images, "box": self._box,
        }
        try:
            ok, detail = await asks[name]()
            return Check(ok=ok, detail=detail)
        except Exception as e:  # any failure is a failed check, with what went wrong
            return Check(ok=False, detail=f"{type(e).__name__}: {str(e)[:160]}")

    async def _boolean(self) -> tuple[bool, str]:
        on = _as(BooleanAnswer, (await self.ask("The traffic light ahead turned red, so the cars stopped.", LIGHT)).answers["red"]).probability
        off = _as(BooleanAnswer, (await self.ask("The traffic light ahead turned green, so the cars drove on.", LIGHT)).answers["red"]).probability
        return on >= PASS and off <= 1 - PASS, f"P(true) {on:.2f} / {off:.2f}"

    async def _choice(self) -> tuple[bool, str]:
        blue = _picked((await self.ask("Ken painted his car blue last summer.", CAR)).answers["colour"], "blue")
        red = _picked((await self.ask("Ken painted his car red last summer.", CAR)).answers["colour"], "red")
        return blue[0] and red[0], f"{blue[1]} / {red[1]}"

    async def _score(self) -> tuple[bool, str]:
        three = _as(ScoreAnswer, (await self.ask("Mia picked three apples from the tree.", APPLES)).answers["apples"]).score
        one = _as(ScoreAnswer, (await self.ask("Mia picked one apple from the tree.", APPLES)).answers["apples"]).score
        ok = abs(three - 3) <= 0.5 and abs(one - 1) <= 0.5
        return ok, f"{_level(three)} / {_level(one)} (want 3 / 1)"

    async def _image(self) -> tuple[bool, str]:
        got = [_picked((await self.ask(["A picture:", disc(rgb)], COLOUR)).answers["colour"], c) for c, rgb in COLOURS.items()]
        return all(ok for ok, _ in got), " / ".join(d for _, d in got)

    async def _images(self) -> tuple[bool, str]:
        state: list[Part] = ["First picture:", disc(COLOURS["red"]), "Second picture:", disc(COLOURS["blue"])]
        r = await self.ask(state, PAIR)
        first, second = _picked(r.answers["first"], "red"), _picked(r.answers["second"], "blue")
        return first[0] and second[0], f"{first[1]} / {second[1]}"

    async def _box(self) -> tuple[bool, str]:
        a = _as(BoxAnswer, (await self.ask(["A picture:", box_image()], BOX_Q)).answers["disc"])
        score = iou(a.box, BOX_TRUTH)
        conf = f", confidence {a.confidence:.2f}" if a.confidence is not None else ""
        return score >= BOX_PASS, f"IoU {score:.2f}{conf}"


async def probe(client: AsyncClient, name: str) -> Verification:
    # Every model is asked about images (s1flow[images] draws them). Without a working Pillow this stops before
    # anything is asked; inside a check the error would read as a model that cannot see. Listing needs no extra.
    import PIL.Image, PIL.ImageDraw  # noqa: F401, E401

    model = client.connections.build(name)  # its own object: the declared capabilities are set aside for the probe
    model.capabilities = EVERYTHING.model_copy(update={"max_options": model.capabilities.max_options})
    p = _Probe(client, model)
    first: tuple[CheckName, ...] = ("boolean", "choice", "score", "image")
    checks: dict[CheckName, Check] = dict(zip(first, await asyncio.gather(*(p.check(c) for c in first))))
    if checks["image"].ok:
        checks["images"], checks["box"] = await asyncio.gather(p.check("images"), p.check("box"))
    else:
        checks["images"] = checks["box"] = Check(ok=False, detail="not asked: image failed")
    return Verification(at=clock.now(), answered_by=p.answered_by, checks=checks)


def unset_keys(name: str, resolve: Callable[[str], ModelSpec], env: Mapping[str, str] = os.environ) -> list[str]:
    """The keys `name` reads that are not set: without them it is not asked."""
    try:
        declared = providers.needs(resolve(name))
    except S1flowError:  # the spec's own error shows when it is built
        return []
    return [] if declared is None else [k for k in declared.keys if not env.get(k)]


async def run(client: AsyncClient, names: list[str]) -> dict[str, Verification]:
    return dict(zip(names, await asyncio.gather(*(probe(client, n) for n in names))))


# ---------- list prices ----------

STALE_DAYS = 90
PRICE_FIELDS = ("input_per_mtok", "output_per_mtok", "per_request", "per_image")


class PriceCheck(BaseModel):
    """One priced model's list price against the one its provider publishes."""

    model_config = ConfigDict(extra="forbid")
    status: Literal["same", "differs", "old", "unchecked", "unlisted", "unreadable"]
    detail: str
    published: Price | None = None


def check_price(spec: ModelSpec, cache_dir: Path | None, today: dt.date | None = None) -> PriceCheck | None:
    """None for a model with no price in s1flow.toml (it bills, or its cost is not known)."""
    if spec.price is None:
        return None
    age = ((today or dt.date.today()) - dt.date.fromisoformat(spec.price.as_of)).days
    of = providers.published(spec)
    if of is None:
        return PriceCheck(status="unchecked", detail=f"{spec.provider} publishes no price list to check it against (as of {spec.price.as_of}, {spec.price.source})")
    try:
        listed = of(spec, cache_dir)
    except Exception as e:  # the list is someone else's server: a failed read is reported, not raised
        return PriceCheck(status="unreadable", detail=f"{type(e).__name__}: {str(e)[:200]}")
    if listed is None:
        return PriceCheck(status="unlisted", detail=f"{spec.id} is not on {spec.provider}'s list")
    ours, theirs = spec.price.model_dump(), listed.model_dump()
    off = [f"{k} {ours[k]:g} here, {theirs[k]:g} listed" for k in PRICE_FIELDS if not math.isclose(ours[k], theirs[k], rel_tol=1e-9, abs_tol=1e-12)]
    if off:
        return PriceCheck(status="differs", detail="; ".join(off) + f" ({listed.source})", published=listed)
    if age > STALE_DAYS:
        return PriceCheck(status="old", detail=f"same as listed, but as_of {spec.price.as_of} is {age} days old: update it", published=listed)
    return PriceCheck(status="same", detail=f"as listed ({listed.source})", published=listed)


# ---------- models.verified.json ----------


def verified_path(project: Project) -> Path:
    return project.config.with_name("models.verified.json")


class VerifiedFile(BaseModel):
    """models.verified.json: each model's last verification, by its name in s1flow.toml."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True, serialize_by_alias=True)
    schema_: Literal["s1flow/verified@1"] = Field(default="s1flow/verified@1", alias="schema")
    models: dict[str, Verification] = {}


def read_verified(project: Project) -> dict[str, Verification]:
    path = verified_path(project)
    return VerifiedFile.model_validate_json(path.read_text()).models if path.exists() else {}


def save(project: Project, results: dict[str, Verification]) -> None:
    """Merge into models.verified.json: the models probed now replace their earlier results."""
    merged = read_verified(project) | results
    out = VerifiedFile(models={k: merged[k] for k in sorted(merged)})
    verified_path(project).write_text(json.dumps(out.model_dump(mode="json"), ensure_ascii=False, indent=1) + "\n")


# ---------- what `s1flow models` shows ----------


@dataclass(frozen=True)
class Unasked:
    """A model --verify does not ask: a key it reads is not set."""

    name: str
    keys: list[str]
    get: str  # where to get them ("" when no provider says)


@dataclass(frozen=True)
class Found:
    """One model's verification against its declaration."""

    name: str
    answered_by: str | None
    checks: list[tuple[CheckName, str, str]]  # each check, what it says of the declaration ("FAIL, declared", "ok", ...), its detail
    price: tuple[str, str] | None  # its list price's check ("warning" when it differs or is old), and its detail; None: no price to check
    failed: bool  # a capability it declares failed


def asked(project: Project, names: list[str] | None) -> tuple[list[str], list[Unasked]]:
    """The models --verify asks (`names`, default the whole line-up and its versions), and those it does not.
    A wrong name or version lists the right ones before any call."""
    models = project.client().connections
    probe = names or models.names(versions=True)
    for name in probe:
        models.resolved(name)
    unset = {n: Unasked(n, keys, "; ".join(g for k in keys if (g := where_to_get(k)))) for n in probe if (keys := unset_keys(n, models.resolved))}
    return [n for n in probe if n not in unset], list(unset.values())


def verify(project: Project, names: list[str]) -> list[Found]:
    """Ask each model (`run`), merge the results into models.verified.json, and read each one against its declaration."""
    client = project.client()
    models = client.connections
    results = asyncio.run(run(client, names))
    if results:
        save(project, results)
    out = []
    for name, result in results.items():
        failed, undeclared = disagreements(models.build(name).capabilities, result)
        checks = [(c, "FAIL, declared" if c in failed else "works, not declared" if c in undeclared else "ok" if got.ok else "no", got.detail)
                  for c, got in result.checks.items()]
        price = None if ":" in name else check_price(models.retrieve(name).spec, project.cache_dir)  # once per model
        shown = None if price is None else ("warning" if price.status in ("differs", "old") else price.status, price.detail)
        out.append(Found(name, result.answered_by, checks, shown, bool(failed)))
    return out


def _cell(said: dict[CheckName, bool], v: Verification | None, *checks: CheckName) -> str:
    """One capability in the line-up's table: declared or not, against what --verify found (`v`)."""
    declared = said[checks[0]]
    if v is None:
        return "✓?" if declared else "·"
    ok = all(v.checks[c].ok for c in checks)
    return ("✓" if ok else "✗!") if declared else ("+" if ok else "·")


def lineup(project: Project) -> list[dict[str, str]]:
    """Each model and version in s1flow.toml: what it declares, next to what --verify found (models.verified.json)."""
    models = project.client().connections
    verified = read_verified(project)
    rows = []
    for name in models.names(versions=True):
        spec = models.retrieve(name).spec
        m = models.build(name)
        caps, v = m.capabilities, verified.get(name)
        said = claims(caps)
        rows.append({
            "name": name, "provider": spec.provider, "id": models.resolved(name).id,
            "boolean": _cell(said, v, "boolean"), "choice": _cell(said, v, "choice"), "score": _cell(said, v, "score"),
            "image": _cell(said, v, "image", "images"), "box": _cell(said, v, "box"),
            "distribution": caps.distribution, "context": f"{caps.context_tokens // 1000}k",
            "limits": ", ".join(f"{k} {x}" for k, x in [("options", caps.max_options), ("instr", caps.max_instructions_chars), ("desc", caps.max_description_chars)] if x) or "-",
            "concurrency": str(m.concurrency), "checked": v.at[:10] if v else "-",
        })
    return rows
