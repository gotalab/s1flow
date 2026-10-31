"""HelpSteer2: how helpful is an assistant's response? A judge's score over five levels.

300 responses from HelpSteer2's validation split (prompt and response under 4,000 characters), 60 per
helpfulness level, seed 1. `label` is the dataset's helpfulness, the mean of 2-5 annotators after its outlier
filtering; `ratings` keeps each annotator's own (its disagreements file). On these cases one annotator against
the mean of the others has QWK 0.71 and MAE 0.76 levels: a model near that agrees with people about as well as
they agree with each other. The level descriptions are ours; HelpSteer2 asks only "overall helpfulness".
"""

from s1flow.eval import Task
from s1flow.objectives import QWK, Accuracy
from s1flow.questions import Score

task = Task(
    id="helpsteer2-helpfulness",
    cases="data.jsonl",
    state=lambda r: {"conversation": r["conversation"], "response": r["response"]},
    question_id="helpfulness",
    question=Score(
        instructions="How helpful is the response to the conversation's last user turn?",
        criteria=[
            "Not helpful: it ignores or fails the request, or is wrong in a way that makes it useless.",
            "Slightly helpful: it touches the request but misses most of it or has major errors.",
            "Partly helpful: it addresses the request with notable gaps, errors or needless content.",
            "Mostly helpful: it addresses the request well, with minor gaps or issues.",
            "Fully helpful: it does what was asked, completely and correctly; little to improve.",
        ],
    ),
    tiebreak=[QWK(), Accuracy()],
    label=lambda r: r["label"],
    source="NVIDIA HelpSteer2 (CC BY 4.0), validation split: 60 responses per helpfulness level, under 4,000 characters",
    show=lambda r: r["conversation"][:120],
)
