"""policies/kinds.py: one class per type of question, the one place that reads its answers and checks its labels."""

from __future__ import annotations

import pytest

from s1flow.client import Boolean, BooleanAnswer, Box, BoxAnswer, BoxEdges, Choice, ChoiceAnswer, Score
from s1flow.client.answers import ScoreAnswer
from s1flow.core.errors import ProviderError
from s1flow.eval.kinds import kind_of
from s1flow.policies import DecisionRule
from s1flow.policies.kinds import KindParams

YES_NO = Choice(instructions="?", criteria={"yes": None, "no": None, "maybe": None})
LEVELS = Score(instructions="?", criteria=["none", "some", "many"])
BOX = BoxEdges(top=0.1, bottom=0.5, left=0.2, right=0.6)


def test_each_question_has_its_kind():
    b, c, p, s, x = kind_of(Boolean(instructions="?")), kind_of(YES_NO), kind_of(YES_NO, KindParams(positive="yes")), kind_of(LEVELS), kind_of(Box(instructions="?"), KindParams(iou=0.7))
    assert [k.type for k in (b, c, p, s, x)] == ["boolean", "choice", "choice", "score", "box"]
    assert [k.adoptable for k in (b, c, p, s, x)] == [True, True, True, False, False]
    assert b.binary and p.binary and not c.binary and not s.binary and not x.binary
    assert b.sets == p.sets == {"threshold", "min_probability"} and c.sets == s.sets == x.sets == {"min_probability"}
    assert [k.objectives[0] if k.objectives else None for k in (b, c, p, s, x)] == ["accuracy", "accuracy", "accuracy", "mae", "accuracy"]
    assert [k.report for k in (b, c, p, s, x)] == [("f1", "precision", "recall"), ("macro_f1",), ("f1", "precision", "recall"), ("mae", "qwk"), ("mean_iou",)]
    assert c.options == p.options == ["yes", "no", "maybe"] and x.iou == 0.7


def test_labels_are_checked_in_one_place():
    assert kind_of(Boolean(instructions="?")).label_error("yes") == "a binary task's label is true or false, got 'yes'"
    assert kind_of(YES_NO).label_error("nope") == "label 'nope' is not an option (yes, no, maybe)"
    assert kind_of(YES_NO, KindParams(positive="yes")).label_error(True) is None
    assert kind_of(YES_NO, KindParams(positive="yes")).as_label("yes") is True and kind_of(YES_NO).as_label("yes") == "yes"
    assert kind_of(LEVELS).label_error(2) is None and kind_of(LEVELS).label_error(3) and kind_of(LEVELS).label_error(True)
    assert kind_of(Box(instructions="?")).label_error(BOX.model_dump()) is None
    assert "top, bottom, left, right" in (kind_of(Box(instructions="?")).label_error({"top": 2}) or "")


def test_the_answers_are_averaged_then_read():
    c = kind_of(YES_NO)
    a, b = ChoiceAnswer(choice="yes", probabilities={"yes": 0.6, "no": 0.4}), ChoiceAnswer(choice="no")
    avg = c.average([a, b])
    assert avg.distribution == [0.3, 0.7, 0.0] and not avg.distributed  # the second gave no distribution: one-hot
    r = c.reading(avg, DecisionRule(min_probability=0.8))
    assert (r.value, r.probability, r.below_min_probability) == ("no", 0.7, True) and r == c.read([a, b], DecisionRule(min_probability=0.8))
    r = c.read([a], DecisionRule())
    assert (r.value, r.probability, r.below_min_probability, r.distribution) == ("yes", 0.6, None, [0.6, 0.4, 0.0])  # no min: not judged
    p = kind_of(YES_NO, KindParams(positive="yes")).read([a, b], DecisionRule(threshold=0.25))
    assert (p.value, p.p_positive, p.probability, p.distribution) == (True, 0.3, 0.3, None)  # read as binary: no distribution
    b, yes = kind_of(Boolean(instructions="?")), BooleanAnswer(probability=0.7)
    assert b.read([BooleanAnswer(probability=0.2)] * 2, DecisionRule()).value is False and b.read([yes], DecisionRule()).value is True
    r = b.read([yes], DecisionRule(threshold=0.8))
    assert (r.value, r.probability, r.p_positive) == (False, pytest.approx(0.3), 0.7)  # the probability of the value read
    assert b.read([yes], DecisionRule(min_probability=0.75)).below_min_probability
    with pytest.raises(ProviderError, match="outside the contract"):
        kind_of(YES_NO).read([ChoiceAnswer(choice="bogus")], DecisionRule())
    with pytest.raises(ProviderError, match="outside the contract"):
        kind_of(YES_NO).read([yes], DecisionRule())  # another type's answer
    with pytest.raises(ProviderError, match="outside the contract"):
        kind_of(Boolean(instructions="?")).read([BooleanAnswer(probability=2)], DecisionRule())


def test_a_distribution_needs_positive_mass_for_choice_and_score_readers():
    choice = Choice(instructions="?", criteria={"billing": None, "support": None})
    for params in (KindParams(), KindParams(positive="billing")):
        for probabilities in ({"billing": 0.0, "support": 0.0}, {"bogus": 1.0}):
            with pytest.raises(ProviderError, match="positive mass"):
                kind_of(choice, params).read([ChoiceAnswer(choice="billing", probabilities=probabilities)], DecisionRule())

    score = kind_of(Score(instructions="?", criteria=["low", "high"]))
    with pytest.raises(ProviderError, match="positive mass"):
        score.read([ScoreAnswer(score=0, probabilities={"0": 0.0, "1": 0.0})], DecisionRule())


def test_a_score_reads_the_rounded_expected_level():
    s = kind_of(LEVELS)
    r = s.read([ScoreAnswer(score=1.0, probabilities={"0": 0.25, "1": 0.25, "2": 0.5})], DecisionRule())
    assert (r.expected, r.value, r.probability) == (1.25, 1, 0.25)
    r = s.read([ScoreAnswer(score=1.5)], DecisionRule())  # no probabilities: the score as is, .5 up
    assert (r.expected, r.value) == (1.5, 2)
    assert s.correct(2, r) and not s.correct(1, r)


def test_a_box_reads_the_first_box_and_its_confidence():
    x = kind_of(Box(instructions="?"))
    off = BoxEdges(top=0.6, bottom=0.9, left=0.6, right=0.9)
    r = x.read([BoxAnswer(box=BOX, confidence=0.9), BoxAnswer(box=off, agreement=0.5)], DecisionRule(min_probability=0.8))
    assert (r.value, r.probability, r.confidence, r.below_min_probability) == (BOX, None, pytest.approx(0.7), True)
    assert x.correct(BOX.model_dump(), r) and not x.correct(off.model_dump(), r) and not x.correct(BOX.model_dump(), None)
