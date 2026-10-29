"""The System One wire format, as TypeSafe, OpenRouter (`/systemone`), the AI Gateway (`/v1/evaluate`) and
Workers AI speak it: the questions sent, and the answers read back. Adding a type of question to these
providers is changing this module.

    questions(qs)               # {"q": {"type": "noul", "instructions": ...}}: yes / no is TypeSafe's `noul`
    questions(qs, noul=False)   # the Gateway's: yes / no stays `boolean`
    answers(raw, confidence)    # {"q": BooleanAnswer(...)}; a `noul` or `boolean` answer, a choice, a score, a box

OpenAI's Decisions API (openai_decisions.py) and the LLMs (llm.py) speak their own.
"""

from __future__ import annotations

from typing import Any

from ..answers import Answer, BooleanAnswer, BoxAnswer, BoxEdges, ChoiceAnswer, ScoreAnswer
from ..questions import Questions
from .contract import outside_contract, refusal


def questions(qs: Questions, *, noul: bool = True) -> dict[str, Any]:
    wire = {k: q.model_dump(exclude_none=True) for k, q in qs.items()}
    return {k: {**q, "type": "noul"} if noul and q["type"] == "boolean" else q for k, q in wire.items()}


def answers(raw: dict[str, Any], confidence: dict[str, float] | None = None) -> dict[str, Answer]:
    """`confidence`: a per-question confidence the model returns beside the answers (the Gateway's TypeSafe metadata)."""
    out: dict[str, Answer] = {}
    for qid, a in raw.items():
        if (r := refusal(a)) is not None:
            out[qid] = r
            continue
        with outside_contract(qid):
            out[qid] = _answer(qid, a, confidence)
    return out


def _answer(qid: str, a: dict[str, Any], confidence: dict[str, float] | None) -> Answer:
    kind = a.get("type")
    if kind in ("noul", "boolean"):
        return BooleanAnswer(probability=a["noul" if kind == "noul" else "probability"])
    if kind == "box":
        b = a["box"]
        return BoxAnswer(box=BoxEdges.clipped(b["top"], b["bottom"], b["left"], b["right"]), confidence=a.get("confidence"))
    conf = (confidence or {}).get(qid, a.get("confidence"))
    if kind == "choice":
        return ChoiceAnswer(choice=a["choice"], probabilities=a.get("probabilities") or None, confidence=conf)
    if kind == "score":
        return ScoreAnswer(score=a["score"], probabilities=a.get("probabilities") or None, confidence=conf)
    raise TypeError(f"no answer type {kind!r}")
