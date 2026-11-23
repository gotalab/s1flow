"""JNLI (JGLUE): does the source sentence back the claim, contradict it, or leave it open?

The judgment of a grounding check: before a summary or an answer goes out, each claim is checked against the text
it came from. JNLI's pairs are short Japanese image captions, so this is that check on easy text; models still
differ, mostly on what a sentence leaves open. On 8 of the 300 pairs nearly every model (16 or more of 21) gives
another answer than the label, and on most of those the label is arguable; they are kept as labelled. Sampled from JNLI v1.3's validation file (its test set is not
public): 100 pairs per label, `random.Random(1)`, ids `p<sentence_pair_id>`.
"""

from s1flow.eval import Task
from s1flow.objectives import Accuracy, Coverage
from s1flow.questions import Choice

task = Task(
    id="jnli-support",
    cases="data.jsonl",
    state=lambda r: {"source": r["source"], "claim": r["claim"]},
    question_id="support",
    question=Choice(
        instructions="元の文(source)だけを根拠にしたとき、主張(claim)は正しいと言えるか。",
        criteria={
            "entailment": "元の文から主張が正しいと言える。",
            "contradiction": "元の文と主張は矛盾する。",
            "neutral": "元の文だけでは主張が正しいとも誤りとも言えない。",
        },
    ),
    label=lambda r: r["label"],
    # A sure answer passes the claim or sends it back to be fixed; a person checks the rest. 95%: a wrong
    # "backed" lets a claim the source does not support reach the reader.
    objective=Coverage(target_accuracy=0.95),
    tiebreak=[Accuracy()],
    source="JGLUE JNLI v1.3（Yahoo Japan, CC BY-SA 4.0）の validation から各ラベル 100 件",
    show=lambda r: r["claim"],
)
