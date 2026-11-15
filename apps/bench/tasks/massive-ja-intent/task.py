"""MASSIVE ja-JP: route a spoken request to one of 60 intents (the Japanese CLINC).

Built by the former `fetch` command (removed; the data is in git). The `with_none` variant adds an
explicit "none of these" option; MASSIVE has no out-of-scope utterances, so it
only shows what that option costs on in-scope requests.
"""

import json
from pathlib import Path

from s1flow.eval import Task
from s1flow.objectives import Accuracy, Coverage
from s1flow.questions import Choice

INTENTS = json.loads((Path(__file__).parent / "intents.json").read_text())
INSTRUCTIONS = "音声アシスタントへの依頼(utt)の意図を、選択肢から1つ選ぶ。選択肢は「シナリオ_動作」の形の名前。"


def describe(intent: str) -> str:
    scenario, _, action = intent.partition("_")
    return f"{scenario}: {action.replace('_', ' ')}"


CRITERIA = {i: describe(i) for i in INTENTS}

task = Task(
    id="massive-ja-intent",
    cases="data.jsonl",
    state=lambda r: {"utt": r["utt"]},
    question_id="intent",
    question=Choice(instructions=INSTRUCTIONS, criteria=CRITERIA),
    label=lambda r: r["intent"],
    # The assistant acts on a sure answer and asks back on the rest. 95%: a wrong intent runs another action
    # (an alarm set, a message sent) before the person can stop it.
    objective=Coverage(target_accuracy=0.95),
    tiebreak=[Accuracy()],
    variants={
        "with_none": Choice(instructions=INSTRUCTIONS, criteria=CRITERIA | {"none": "どれにも当てはまらない"}),
    },
    source="MASSIVE 1.1 ja-JP test（Amazon, CC BY 4.0）から各意図 5 件まで",
    show=lambda r: r["utt"],
)
