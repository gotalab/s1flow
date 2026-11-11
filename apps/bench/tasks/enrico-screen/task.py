"""Enrico: which kind of mobile app screen is this? One of 20 design topics, from the screenshot alone.

221 Android screenshots from Enrico (1,460 Rico screens, each labelled with one design topic), up to 12 per
topic, seed 1, leaving out the 10 its issues.csv flags for a faulty screenshot. Enrico's labels are noisy: every
drawn screen was looked at against its topic's description, and a second reviewer, not told which screens the first
had flagged, judged the flagged ones mixed with kept ones. The 69 both judged plainly something else (a login form
labelled gallery, a news article labelled terms) are listed in mislabelled.csv and replaced by further draws; maps,
camera and calculator have too few screens left for 12. Screens that fit two topics (a login form is also a form)
keep Enrico's. Stored as WebP (quality 80) at Enrico's 540x960 to keep the repository small. The topic descriptions
are Enrico's own.
"""

from s1flow.eval import Task
from s1flow.objectives import Accuracy, Coverage
from s1flow.questions import Choice

TOPICS = {
    "bare": "Largely unused area",
    "calculator": "Number entry",
    "camera": "Camera functionality",
    "chat": "Chat functionality",
    "editor": "Text/Image editing",
    "form": "Form filling functionality",
    "gallery": "Grid-like layout with images",
    "list": "Elements organized in a column",
    "login": "Input fields for logging",
    "maps": "Geographic display",
    "mediaplayer": "Music or video player",
    "menu": "Items list in an overlay or aside",
    "modal": "A popup-like window",
    "news": "Snippets list: image, title, text",
    "other": "Everything else",
    "profile": "Info on a user profile or product",
    "search": "Search engine functionality",
    "settings": "Controls to change app settings",
    "terms": "Terms and conditions of service",
    "tutorial": "Onboarding screen",
}

task = Task(
    id="enrico-screen",
    cases="data.jsonl",
    state=lambda r: [{"type": "image", "path": r["screen"]}],
    question_id="topic",
    question=Choice(
        instructions="Which kind of screen does this mobile app screenshot show?",
        criteria=TOPICS,
    ),
    label=lambda r: r["label"],
    objective=Coverage(target_accuracy=0.95),
    tiebreak=[Accuracy()],
    source="Enrico (labels MIT) on Rico screenshots (CC BY 4.0): up to 12 screens per design topic, mislabelled ones replaced",
    show=lambda r: r["id"],
)
