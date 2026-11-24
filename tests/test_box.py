"""Box questions: wire format, LLM units, and scoring by IoU (no network)."""

import asyncio
import io
import json

import httpx
import pytest
import respx
from PIL import Image as PILImage

from conftest import PROJECT, attach, make_project

from s1flow.client.boxes import iou
from s1flow.core.errors import DataError, Unsupported
from s1flow.client import Box, BoxAnswer, BoxEdges, Capabilities, Response, Image
from s1flow.eval import Task, data, metrics, report
from s1flow.policies.kinds import same_label
from s1flow.eval import run as running
from s1flow.project import Project
from s1flow.client.providers.llm import box_answer, to_answers, user_content
from s1flow.client.providers.typesafe import BASE_URL as TS_URL

LINEUP = Project(PROJECT).client().connections

Q = {"disc": Box(instructions="the red disc")}
TRUTH = BoxEdges(top=0.1, bottom=0.5, left=0.2, right=0.6)
MISS = BoxEdges(top=0.6, bottom=0.9, left=0.7, right=0.9)


def test_iou():
    assert iou(TRUTH, TRUTH) == 1.0
    assert iou(TRUTH, MISS) == 0.0
    half = BoxEdges(top=0.1, bottom=0.5, left=0.4, right=0.8)  # overlaps half of TRUTH's width
    assert iou(TRUTH, half) == pytest.approx(1 / 3)


@respx.mock
def test_typesafe_box_answer_and_header(monkeypatch):
    monkeypatch.setenv("TYPESAFE_API_KEY", "t")
    body = {"model": "jev-1.14.0", "answers": {"disc": {"type": "box", "box": TRUTH.model_dump(), "confidence": 0.95}}}
    route = respx.post(f"{TS_URL}/systemone").mock(return_value=httpx.Response(200, json=body))
    m = LINEUP.build("jev:1.14")
    r = asyncio.run(m.decide("text", Q))
    assert route.calls[0].request.headers["typesafe-danger-zone-images"] == "true"
    assert json.loads(route.calls[0].request.read())["questions"]["disc"] == {"type": "box", "instructions": "the red disc"}
    assert r.answers["disc"].box == TRUTH and r.answers["disc"].confidence == 0.95


def test_box_only_where_declared():
    for name in ("jev", "d1@vercel", "luna@decisions", "clef"):
        with pytest.raises(Unsupported):
            asyncio.run(LINEUP.build(name).decide("text", Q))


def test_llm_asks_in_its_own_units_and_answers_fractions():
    img = Image(media_type="image/png", data="AAAA", sha256="0", width=400, height=300)
    state = ["A picture:", img]
    assert "400x300 pixels" in user_content(state, Q, "pixels")[0]["text"]
    assert "0-1000" in user_content(state, Q, "k1000")[0]["text"]
    px = to_answers([{"disc": {"top": 30, "bottom": 150, "left": 80, "right": 240}}], Q, False, "pixels", (400, 300))
    assert px["disc"].box == TRUTH
    k = to_answers([{"disc": {"top": 100, "bottom": 500, "left": 200, "right": 600}}], Q, False, "k1000")
    assert k["disc"].box == TRUTH
    flipped = to_answers([{"disc": {"top": 500, "bottom": 100, "left": 1200, "right": 200}}], Q, False, "k1000")
    assert flipped["disc"].box == BoxEdges(top=0.1, bottom=0.5, left=0.2, right=1.0)  # put in order and clipped


def test_box_samples_take_the_median_and_their_agreement():
    a = box_answer([TRUTH, TRUTH, MISS])
    assert a.box == TRUTH and a.agreement == pytest.approx(2 / 3)
    with pytest.raises(ValueError):
        BoxEdges(top=0.5, bottom=0.1, left=0, right=1)  # out of order
    with pytest.raises(ValueError):
        BoxEdges(top=0, bottom=1.2, left=0, right=1)  # outside the image
    assert box_answer([TRUTH]).agreement is None


class FakeBox:
    """Hits on even ids with high confidence, misses on odd ids with low confidence."""

    id, model_id, concurrency = "fake:box", "fake-box", 4
    capabilities = Capabilities(image=True, question_types={"box"})

    def __init__(self, b=None):
        pass

    async def decide(self, state, questions, *, options=None):
        n = int(state[0])
        hit = n % 2 == 0
        box = TRUTH if hit else MISS
        return Response(answers={"q": BoxAnswer(box=box, confidence=0.9 if hit else 0.4)}, answered_by=self.model_id)


def test_box_task_is_scored_by_iou(tmp_path):
    p = make_project(tmp_path, {"fakebox": FakeBox})
    buf = io.BytesIO()
    PILImage.new("RGB", (400, 300), "white").save(buf, "PNG")
    (tmp_path / "shot.png").write_bytes(buf.getvalue())
    rows = [{"id": str(i), "n": i, "box": TRUTH.model_dump()} for i in range(40)]
    (tmp_path / "data.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    task = attach(Task(
        id="box-test", cases="data.jsonl", dir=tmp_path,
        state=lambda r: [str(r["n"]), {"type": "image", "path": "shot.png"}],
        question=Box(instructions="the red disc"), label=lambda r: r["box"],
    ), p)
    assert task.kind.type == "box" and not task.kind.binary and task.kind.iou == 0.5
    asyncio.run(running.run_model(task, "fakebox", limit=None, variant="base"))
    pr = metrics.load(task, "base", "fakebox")
    e = metrics.evaluate(task, pr)
    assert e.n == 28  # only dev, with the fixed 30% test share held out
    expected = sum(int(cid) % 2 == 0 for cid in pr.ids) / len(pr.ids)
    assert e.accuracy and e.accuracy.value == expected and e.measures["mean_iou"].value == pytest.approx(expected)
    assert e.auroc and e.auroc.value == 1.0  # the confidence separates hits from misses perfectly
    sel = e.selective[0]
    assert sel.coverage.value == pytest.approx(0.5, abs=0.1) and sel.errors == 0
    md = report.render(task, "base", [e], {"fakebox": pr})
    assert "mean IoU" in md and "right at IoU 0.5 or more" in md
    from s1flow.eval import adopt as adopting

    r = adopting.adopt(task, "fakebox", "me", "a box policy ships like any other")
    assert r.spec.question.type == "box" and task.policies.read(task.id).digest == r.spec.digest


def test_provider_boxes_are_clipped_and_ordered():
    from s1flow.client.providers.systemone import answers as parse_answers

    a = parse_answers({"d": {"type": "box", "box": {"top": 0.5, "bottom": 0.1, "left": -0.001, "right": 1.0000001}}})
    assert a["d"].box == BoxEdges(top=0.1, bottom=0.5, left=0.0, right=1.0)


def test_unprepared_images_are_a_data_error(tmp_path):
    (tmp_path / "s1flow.toml").write_text('default = ["m"]\n[models.m]\nprovider = "llm"\nid = "vercel_ai_gateway/x/m"\ncapabilities.image = true\n')
    llm = Project(tmp_path).client().connections.build("m")
    with pytest.raises(DataError):
        asyncio.run(llm.decide(["x", {"type": "image", "path": "a.png"}], Q))
    with pytest.raises(DataError):
        asyncio.run(LINEUP.build("d1@vercel").decide({"shot": {"type": "image", "path": "a.png"}}, Q))


def test_a_box_label_can_say_the_target_is_not_in_the_picture():
    from s1flow.eval.kinds import kind_of
    from s1flow.eval.objectives import measure
    from s1flow.policies import ABSENT, DecisionRule

    kind = kind_of(Q["disc"])
    assert kind.label_error(ABSENT) is None and "or False when the target is not in the picture" in kind.label_error(True)
    gone = kind.read([BoxAnswer(box=None, found=0.1)], DecisionRule(min_probability=0.95))
    assert gone.value is None and gone.confidence == pytest.approx(0.9) and gone.below_min_probability is True
    assert kind.average([BoxAnswer(box=None)]).distributed is False  # a model that says nothing of how sure: 1, and said so
    there = kind.read([BoxAnswer(box=TRUTH, confidence=0.8, found=0.99)], DecisionRule())
    assert there.value == TRUTH and there.confidence == 0.8  # a box found keeps its own confidence
    answers = [BoxAnswer(box=TRUTH, confidence=0.9), BoxAnswer(box=None, found=0.2), BoxAnswer(box=None, found=0.05), BoxAnswer(box=MISS, confidence=0.6), None]
    labels = [TRUTH.model_dump(), TRUTH.model_dump(), ABSENT, ABSENT, ABSENT]  # hit, missed it, right (none), a box where none is, no answer
    p = measure.pairs(kind, labels, [None if a is None else kind.read([a], DecisionRule()) for a in answers])
    assert list(p.correct) == [True, False, True, False, False]
    assert measure.measure("mean_iou", p) == pytest.approx((1 + 0 + 1 + 0 + 0) / 5)
    assert list(p.confidence) == pytest.approx([0.9, 0.8, 0.95, 0.6, 0.0])
    assert [measure.shown(p, i) for i in range(4)] == [("box", "IoU 1.00"), ("box", "absent"), ("absent", "absent"), ("absent", "box")]
    all_absent = measure.pairs(kind, [ABSENT, ABSENT], [kind.read([BoxAnswer(box=None, found=0.1)], DecisionRule()), kind.read([BoxAnswer(box=TRUTH)], DecisionRule())])
    assert list(all_absent.correct) == [True, False] and all_absent.y[0] is ABSENT


class FakeBoxOrNone:
    """Says the disc is not there on every third case (right: those have none), unsure and wrong about it on every twelfth."""

    def __init__(self, spec):
        self.id, self.model_id, self.concurrency = "fake:boxornone", "fake-boxornone", 4
        self.capabilities = Capabilities(image=True, question_types=frozenset({"box"}))

    async def decide(self, state, questions, *, options=None):
        n = int(state[0])
        if n % 12 == 1:
            a = BoxAnswer(box=None, found=0.4)  # there is one
        elif n % 3 == 0:
            a = BoxAnswer(box=None, found=0.02)
        else:
            a = BoxAnswer(box=TRUTH, confidence=0.97, found=0.99)
        return Response(answers={"q": a}, answered_by=self.model_id)


def test_a_box_task_with_pictures_that_have_no_target(tmp_path):
    p = make_project(tmp_path, {"boxornone": FakeBoxOrNone})
    buf = io.BytesIO()
    PILImage.new("RGB", (400, 300), "white").save(buf, "PNG")
    (tmp_path / "shot.png").write_bytes(buf.getvalue())
    rows = [{"id": str(i), "n": i, "box": None if i % 3 == 0 else TRUTH.model_dump()} for i in range(60)]
    (tmp_path / "data.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    task = attach(Task(
        id="box-none-test", cases="data.jsonl", dir=tmp_path, state=lambda r: [str(r["n"]), {"type": "image", "path": "shot.png"}],
        question=Box(instructions="the red disc"), label=lambda r: r["box"] if r["box"] is not None else False,
    ), p)
    asyncio.run(running.run_model(task, "boxornone", limit=None, variant="base"))
    pr = metrics.load(task, "base", "boxornone")  # an answer of no box comes back from the saved run
    e = metrics.evaluate(task, pr)
    wrong = sum(int(cid) % 12 == 1 for cid in pr.ids)
    assert e.accuracy and e.accuracy.value == pytest.approx(1 - wrong / len(pr.ids)) and e.measures["mean_iou"].value == pytest.approx(1 - wrong / len(pr.ids))
    assert e.selective[0].accuracy == 1.0 and e.selective[0].errors == 0  # the unsure "not there" answers are left out
    md = report.render(task, "base", [e], {"boxornone": pr})
    assert "with no target)" in md and "right is an answer of no box" in md


# ---------- boxes: every instance ----------

OTHER = BoxEdges(top=0.6, bottom=0.9, left=0.1, right=0.4)
NEAR = BoxEdges(top=0.1, bottom=0.5, left=0.25, right=0.65)  # IoU 0.78 with TRUTH


def test_boxes_are_matched_one_to_one_best_first():
    from s1flow.client.boxes import matched

    assert matched([TRUTH, OTHER], [OTHER, TRUTH], 0.5) == 2 and matched([NEAR], [TRUTH], 0.5) == 1 and matched([NEAR], [TRUTH], 0.8) == 0
    assert matched([TRUTH, NEAR], [TRUTH], 0.5) == 1  # two answer boxes on one instance: one of them is its box
    assert matched([], [TRUTH], 0.5) == 0 == matched([TRUTH], [], 0.5)
    # best first would give g1 to t1 (IoU 0.78) and leave g2 without a box; g2 to t1 (0.75) and g1 to t2 (0.45) are two
    strip = lambda left, right: BoxEdges(top=0, bottom=1, left=left, right=right)  # noqa: E731
    t1, t2, g1, g2 = strip(0, 0.4), strip(0.2, 0.6), strip(0.05, 0.45), strip(0, 0.3)
    assert matched([g1, g2], [t1, t2], 0.4) == 2 == matched([g2, g1], [t2, t1], 0.4)


def test_a_boxes_label_is_every_instance_and_the_answer_is_as_sure_as_the_whole_set():
    from s1flow.client import Boxes, BoxesAnswer, FoundBox
    from s1flow.core.errors import ProviderError
    from s1flow.eval.kinds import kind_of
    from s1flow.eval.objectives import measure
    from s1flow.objectives import Accuracy, BoxF1
    from s1flow.policies import DecisionRule, KindParams

    kind = kind_of(Boxes(instructions="every red disc"))
    assert kind.type == "boxes" and kind.iou == 0.5 and kind_of(Boxes(instructions="x"), KindParams(iou=0.7)).iou == 0.7
    assert kind.label_error([]) is None and kind.label_error([TRUTH.model_dump()]) is None
    for bad in (TRUTH.model_dump(), [{"top": 2}], None, False):
        assert "list of every instance's box" in kind.label_error(bad)
        with pytest.raises(ValueError, match="list of every instance's box"):
            kind.as_label(bad)
    assert same_label(kind, [TRUTH.model_dump(), OTHER.model_dump()], [OTHER, TRUTH]) and not same_label(kind, [TRUTH.model_dump()], [])
    one = lambda b, found=0.9, conf=0.8: FoundBox(box=b, found=found, confidence=conf)
    r = kind.read([BoxesAnswer(boxes=[one(TRUTH), one(OTHER)], presence=[0.9, 0.9, 0.2])], DecisionRule(min_probability=0.5))
    assert r.value == (TRUTH, OTHER) and r.confidence == pytest.approx(0.9 * 0.9 * 0.8 * 0.8 * 0.8) and r.below_min_probability is True
    assert kind.read([BoxesAnswer(boxes=[], presence=[0.1, 0.0])], DecisionRule()).confidence == pytest.approx(0.9)
    assert kind.read([BoxesAnswer(boxes=[one(TRUTH)], at_least=True, presence=[0.99])], DecisionRule()).confidence == 0.0  # it says there are more
    bare = kind.average([BoxesAnswer(boxes=[FoundBox(box=TRUTH)])])
    assert bare.confidence == 1.0 and bare.distributed is False
    with pytest.raises(ProviderError, match="found"):
        kind.read([BoxesAnswer(boxes=[one(TRUTH, found=1.5)])], DecisionRule())
    answers = [[TRUTH, OTHER], [NEAR], [], [TRUTH, MISS], [TRUTH], None]
    labels = [[OTHER.model_dump(), TRUTH.model_dump()], [TRUTH.model_dump()], [], [TRUTH.model_dump()], [TRUTH.model_dump(), OTHER.model_dump()], [TRUTH.model_dump()]]
    # both found, found (near enough), none and none, one too many, one missed, no answer
    p = measure.pairs(kind, labels, [None if a is None else kind.read([BoxesAnswer(boxes=[one(b) for b in a])], DecisionRule()) for a in answers])
    assert list(p.correct) == [True, True, True, False, False, False]
    assert measure.bound(Accuracy(), kind).value(p) == 0.5
    # answer boxes 2 + 1 + 0 + 2 + 1 = 6, of which 5 match; label boxes 2 + 1 + 0 + 1 + 2 + 1 = 7
    assert measure.measure("box_precision", p) == pytest.approx(5 / 6) and measure.measure("box_recall", p) == pytest.approx(5 / 7)
    assert measure.measure("box_f1", p) == pytest.approx(2 * 5 / (6 + 7)) == measure.bound(BoxF1(), kind).value(p)
    assert measure.measure("count_error", p) == pytest.approx((0 + 0 + 0 + 1 + 1 + 1) / 6)
    assert measure.shown(p, 3) == ("1 box", "2 boxes, 1 matched") and measure.shown(p, 2) == ("0 boxes", "0 boxes, 0 matched") and measure.shown(p, 5)[1] == "no answer"


class FakeBoxes:
    """Finds every disc, but one too few on every fifth case, where it is unsure of the last slot."""

    def __init__(self, spec):
        from s1flow.client import Capabilities as C
        self.id, self.model_id, self.concurrency = "fake:boxes", "fake-boxes", 4
        self.capabilities = C(image=True, question_types=frozenset({"boxes"}))

    async def decide(self, state, questions, *, options=None):
        from s1flow.client import BoxesAnswer, FoundBox

        n = int(state[0])
        truth = [TRUTH, OTHER, MISS][: n % 4]
        short = n % 5 == 0 and bool(truth)
        given = truth[:-1] if short else truth
        presence = [0.98] * len(given) + ([0.45] if short else []) + [0.01]
        return Response(answers={"q": BoxesAnswer(boxes=[FoundBox(box=b, found=0.98, confidence=0.97) for b in given], presence=presence)}, answered_by=self.model_id)


def test_a_boxes_task_runs_reports_and_compares(tmp_path):
    from s1flow.client import Boxes
    from s1flow.core.errors import Unsupported as U
    from s1flow.eval import comparison, review
    from s1flow.objectives import BoxF1, Coverage

    p = make_project(tmp_path, {"boxes": FakeBoxes})
    buf = io.BytesIO()
    PILImage.new("RGB", (400, 300), "white").save(buf, "PNG")
    (tmp_path / "shot.png").write_bytes(buf.getvalue())
    rows = [{"id": str(i), "n": i, "boxes": [b.model_dump() for b in [TRUTH, OTHER, MISS][: i % 4]]} for i in range(80)]
    (tmp_path / "data.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    task = attach(Task(
        id="boxes-test", cases="data.jsonl", dir=tmp_path, state=lambda r: [str(r["n"]), {"type": "image", "path": "shot.png"}],
        question=Boxes(instructions="every disc"), label=lambda r: r["boxes"], objective=Coverage(target_accuracy=0.99), tiebreak=[BoxF1()],
    ), p)
    asyncio.run(running.run_model(task, "boxes", limit=None, variant="base"))
    pr = metrics.load(task, "base", "boxes")
    e = metrics.evaluate(task, pr)
    short = sum(int(cid) % 5 == 0 and int(cid) % 4 != 0 for cid in pr.ids)
    assert e.probabilities and e.accuracy and e.accuracy.value == pytest.approx(1 - short / len(pr.ids))
    assert e.measures["box_precision"].value == 1.0 and e.measures["box_recall"].value < 1.0 and e.measures["count_error"].value == pytest.approx(short / len(pr.ids))
    assert e.selective[0].accuracy == 1.0 and e.selective[0].errors == 0  # the cases it was unsure of are left out
    md = report.render(task, "base", [e], {"boxes": pr})
    assert "| box F1 |" in md and "Boxes: right when every box of the label has an answer box of its own" in md and "cases with none)" in md
    c = comparison.collect(task)
    row = next(r for r in c.candidates if r.model == "boxes")
    assert c.question_type == "boxes" and {"box_f1", "box_precision", "box_recall", "count_error", "brier"} <= set(row.metrics)
    assert row.adoption_blocked == []
    with pytest.raises(U, match="boxes tasks are not supported yet"):
        review.review(task)
    assert not [w for w in data.check(task).warnings if "same state" in w]
    with pytest.raises(DataError, match="already"):  # the same boxes in another order
        review.correct(task, "2", "relabel", reason="same boxes", by="tester", label=[OTHER.model_dump(), TRUTH.model_dump()])
    fix = review.correct(task, "2", "relabel", reason="a third disc", by="tester", label=[b.model_dump() for b in (TRUTH, OTHER, MISS)])
    assert len(fix.was) == 2 and len(fix.label) == 3


def test_a_boxes_answer_has_no_more_boxes_than_the_question_allows():
    from s1flow.client import Boxes, BoxesAnswer, FoundBox
    from s1flow.client.providers.contract import validate_response
    from s1flow.core.errors import ProviderError

    two = Response(answers={"q": BoxesAnswer(boxes=[FoundBox(box=TRUTH), FoundBox(box=OTHER)])}, answered_by="m")
    assert validate_response(two, {"q": Boxes(instructions="every disc", max=2)}, "p") is two
    with pytest.raises(ProviderError, match="2 boxes, more than the question's max of 1"):
        validate_response(two, {"q": Boxes(instructions="every disc", max=1)}, "p")
