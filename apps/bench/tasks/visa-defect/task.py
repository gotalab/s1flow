"""VisA: is this item defective? Visual inspection from one photo, across 12 kinds of item.

240 photos from VisA's test split (Amazon's Visual Anomaly dataset), 10 defective and 10 good per item, seed 1:
four circuit boards, capsules, candles, two kinds of macaroni, cashews, chewing gum and two fried snacks. Defects
are small: scratches, cracks, spots, missing or bent parts, burns. The state names the item and shows its photo;
`defect` keeps VisA's description of what is wrong, for reading the misses. Stored as WebP (quality 75) scaled to
768 px on the long side (VisA's are about 1,300 x 1,100) to keep the repository small; the defects looked at
stay visible at that size. Half defective, far more than a production line sees: compare models with each other.
"""

from s1flow.eval import Task
from s1flow.objectives import Accuracy, Coverage
from s1flow.questions import Boolean

ITEMS = {
    "candle": "four tea candles",
    "capsules": "green soft-gel capsules",
    "cashew": "a cashew nut",
    "chewinggum": "a piece of chewing gum",
    "fryum": "a wheel-shaped fried snack",
    "macaroni1": "four pieces of macaroni",
    "macaroni2": "four pieces of macaroni",
    "pcb1": "an ultrasonic sensor circuit board",
    "pcb2": "a circuit board",
    "pcb3": "an infrared sensor circuit board",
    "pcb4": "a battery charger circuit board",
    "pipe_fryum": "a tube-shaped fried snack",
}

task = Task(
    id="visa-defect",
    cases="data.jsonl",
    state=lambda r: [f"Item: {ITEMS[r['object']]}", {"type": "image", "path": r["image"]}],
    question_id="defective",
    question=Boolean(
        instructions="Visual inspection: does the item in the photo have a defect?",
        criteria={
            "true": "Defective: a scratch, crack, hole, stain or spot, a missing, broken, bent or extra part, a burn, or anything else wrong with it.",
            "false": "Good: nothing wrong with it.",
        },
    ),
    label=lambda r: r["defective"],
    objective=Coverage(target_accuracy=0.95),
    tiebreak=[Accuracy()],
    source="VisA (Amazon, CC BY 4.0), test split: 10 defective and 10 good photos per item, 12 items",
    show=lambda r: r["id"],
)
