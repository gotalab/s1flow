"""JNLI: is the hypothesis supported by the premise? Stands in for fact-level verification.

Built by the former `fetch` command (removed; the data is in git).
"""

from s1flow.eval import Task
from s1flow.questions import Choice

task = Task(
    id="jnli",
    cases="data.jsonl",
    state=lambda r: {"premise": r["premise"], "hypothesis": r["hypothesis"]},
    question_id="relation",
    question=Choice(
        instructions="前提(premise)が正しいとき、仮説(hypothesis)はどうなるか。",
        criteria={
            "entailment": "含意。前提が正しければ、仮説も必ず正しい。",
            "contradiction": "矛盾。前提が正しければ、仮説は正しくない。",
            "neutral": "中立。前提だけでは、仮説が正しいかどうか決まらない。",
        },
    ),
    # JNLI pairs are two captions of one photo (SNLI convention), so a different place or
    # subject is a contradiction, not "can't tell". The base question leaves this unsaid.
    variants={
        "same-scene": Choice(
            instructions="前提(premise)と仮説(hypothesis)は、同じ1枚の写真を説明した文である。前提が正しいとき、仮説はどうなるか。",
            criteria={
                "entailment": "含意。前提が正しければ、仮説も必ず正しい。",
                "contradiction": "矛盾。前提が正しければ、仮説は正しくない。",
                "neutral": "中立。前提だけでは、仮説が正しいかどうか決まらない。",
            },
        ),
        "same-scene-mismatch": Choice(
            instructions="前提(premise)と仮説(hypothesis)は、同じ1枚の写真を説明した文である。前提が正しいとき、仮説はどうなるか。",
            criteria={
                "entailment": "含意。前提が正しければ、仮説も必ず正しい。",
                "contradiction": "矛盾。同じ写真の説明として両立しない。場所、物、人、動物、数、動作のどれかが前提と食い違う。",
                "neutral": "中立。前提と食い違わないが、前提に書かれていないことを足している。",
            },
        ),
    },
    label=lambda r: r["label"],
    source="JGLUE JNLI v1.3 valid（Yahoo Japan, CC BY-SA 4.0）から各ラベル 100 件",
    show=lambda r: f"{r['premise']} ⇒ {r['hypothesis']}",
)
