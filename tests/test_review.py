"""Reviewing labels: what is listed, how a correction is recorded, and that scoring follows it."""

import asyncio
import json

import pytest
from conftest import attach, make_project

from s1flow.core.errors import DataError, NotFound
from s1flow.client import Capabilities, Choice, ChoiceAnswer, Response
from s1flow.eval import Task, data, metrics, review, evalset
from s1flow.eval import run as running

CLASSES = ["a", "b", "c"]
WRONG = {"3", "7"}  # cases collected with the wrong label: the fake answers their true class


class Fake:
    def __init__(self, b):
        self.id, self.model_id, self.concurrency, self.capabilities = f"fake:{b.name}", b.name, 4, Capabilities()

    async def decide(self, state, questions, *, options=None):
        q = next(iter(questions))
        return Response(answers={q: ChoiceAnswer(choice=state["truth"], probabilities={c: 0.96 if c == state["truth"] else 0.02 for c in CLASSES})},
                        answered_by=self.model_id)


@pytest.fixture
def task(tmp_path):
    p = make_project(tmp_path, {"m1": Fake, "m2": Fake})
    rows = []
    for i in range(30):
        truth = CLASSES[i % 3]
        label = CLASSES[(i + 1) % 3] if str(i) in WRONG else truth
        rows.append({"id": str(i), "text": f"case {i}", "truth": truth, "label": label})
    rows.append({"id": "30", "text": "case 0", "truth": "a", "label": "b"})  # the same state as case 0, another label
    (tmp_path / "data.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    t = attach(Task(id="toy", cases="data.jsonl", dir=tmp_path, state=lambda r: {"text": r["text"], "truth": r["truth"]},
                    question=Choice(instructions="Which?", criteria={c: None for c in CLASSES}), label=lambda r: r["label"]), p)
    # The review scenarios are dev; unrelated cases remain genuinely held out.
    sf = evalset.SplitFile(seed=1, test_share=9/31, at="", source="review-fixture",
                           assign={str(i): "test" if 15 <= i < 24 else "train" for i in range(31)})
    (t.dir / "split.json").write_text(sf.model_dump_json(by_alias=True))
    for m in ("m1", "m2"):
        asyncio.run(running.run_model(t, m, limit=None, variant="base"))
    return t


def test_the_cases_models_disagree_with_are_listed_strongest_first(task):
    r = review.review(task, sample=5)
    ids = [x.id for x in r.listed]
    assert set(ids) == {"3", "7", "0", "30"} and set(ids[:3]) == {"3", "7", "30"}  # both models disagree with these; 0 only shares a state
    three = next(x for x in r.listed if x.id == "3")
    assert [o.model for o in three.opinions] == ["m1", "m2"] and three.opinions[0].answer == "a"
    assert any("the same state as" in w for w in next(x for x in r.listed if x.id == "0").why)
    assert len(r.sample) == 5 and all(x.sampled and x.id not in ids for x in r.sample)


def test_a_correction_changes_what_is_scored_and_leaves_the_data(task):
    before = (task.dir / "data.jsonl").read_text()
    review.correct(task, "3", "relabel", label="a", reason="criterion a fits", by="gota")
    review.correct(task, "7", "missing", reason="decided by the linked PR", by="gota")
    pr = metrics.load(task, "base", "m1")
    assert "7" not in pr.ids and pr.unlabeled == 1
    assert pr.y[pr.ids.index("3")] == "a"
    assert (task.dir / "data.jsonl").read_text() == before
    listed = [x.id for x in review.review(task).listed]
    assert "3" not in listed and "7" not in listed  # read once: not listed again
    assert data.check(task).corrected == {"relabel": 1, "missing": 1}


def test_a_later_correction_wins_and_the_history_stays(task):
    review.correct(task, "3", "keep", reason="first reading", by="gota")
    review.correct(task, "3", "relabel", label="a", reason="second reading", by="gota")
    assert task.load_cases().corrections()["3"].verdict == "relabel"
    assert len((task.dir / "corrections.jsonl").read_text().splitlines()) == 2


def test_a_correction_is_checked(task):
    with pytest.raises(NotFound):
        review.correct(task, "99", "keep", reason="x", by="gota")
    with pytest.raises(DataError, match="not an option"):
        review.correct(task, "3", "relabel", label="z", reason="x", by="gota")
    with pytest.raises(DataError, match="already"):
        review.correct(task, "3", "relabel", label="b", reason="x", by="gota")
    with pytest.raises(DataError, match="reason"):
        review.correct(task, "3", "keep", reason=" ", by="gota")


def test_many_unclear_or_missing_point_at_the_task_itself(task):
    for cid in ("1", "2"):
        review.correct(task, cid, "missing", reason="only the code tells", by="gota")
    drawn = review.review(task, sample=1).sample[0].id  # recorded: its correction counts as sampled
    review.correct(task, drawn, "keep", reason="fits a", by="gota")
    t = review.review(task).tally
    assert t.read == 3 and len(t.premise) == 2 and t.sample_read == 1 and t.sample_relabelled == 0  # every reason shown, no fixed share
    assert t.error_rate is not None and t.error_rate[0] == 0.0 and 0.9 < t.error_rate[1] <= 1.0
    assert "Evidence against the premise (unclear or missing 2 of 3 read)" in review.markdown(task, review.review(task))
    assert review.review(task).sample == []  # no sample unless asked for


def test_a_collected_label_that_changed_after_its_correction_is_flagged(task):
    review.correct(task, "3", "keep", reason="fits b", by="gota")
    path = task.dir / "data.jsonl"
    path.write_text(path.read_text().replace('"id": "3", "text": "case 3", "truth": "a", "label": "b"', '"id": "3", "text": "case 3", "truth": "a", "label": "c"'))
    task.load_cases().forget()
    assert any("read it again" in w for w in data.check(task).warnings)
