"""MASSIVE en-US: the same 288 utterances and 60 intents as massive-ja-intent, in English.

Built by the former `fetch` command (removed; the data is in git). MASSIVE is parallel by id, so comparing the
two tasks changes only the language (of the utterance and the instructions).
"""

import json
from pathlib import Path

from s1flow.eval import Task
from s1flow.questions import Choice

INTENTS = json.loads((Path(__file__).parent / "intents.json").read_text())
INSTRUCTIONS = "Pick the intent of the request to a voice assistant (utt) from the options. Option names have the form scenario_action."


def describe(intent: str) -> str:
    scenario, _, action = intent.partition("_")
    return f"{scenario}: {action.replace('_', ' ')}"


task = Task(
    id="massive-en-intent",
    cases="data.jsonl",
    state=lambda r: {"utt": r["utt"]},
    question_id="intent",
    question=Choice(instructions=INSTRUCTIONS, criteria={i: describe(i) for i in INTENTS}),
    label=lambda r: r["intent"],
    source="MASSIVE 1.1 en-US test（Amazon, CC BY 4.0）、massive-ja-intent と同じ 288 件",
    show=lambda r: r["utt"],
)
