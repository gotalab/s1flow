# Bench reports

Each task is measured by the objective its use calls for, declared in its `task.py` with the reason. There is no
score across tasks: a model is chosen for one decision, by what that decision needs.

| Task | The answer is used to | Objective | Why |
|---|---|---|---|
| [gh-ruff-area](gh-ruff-area/questions/base.md) | label an issue with its area, only when sure | coverage at 95% accuracy | the area decides who looks at the issue, so a wrong label sends it to the wrong person |
| [gh-ruff-kind](gh-ruff-kind/questions/base.md) | label an issue with its kind, only when sure | coverage at 90% accuracy | the kind describes the issue and routes it nowhere; whoever reads it first corrects a wrong one |
| [enrico-screen](enrico-screen/questions/base.md) | tag a screen for search in a design library, only when sure | coverage at 90% accuracy | a wrong tag puts one screen in the wrong search result |
| [massive-ja-intent](massive-ja-intent/questions/base.md) | act on a spoken request when sure, ask back otherwise | coverage at 95% accuracy | a wrong intent runs another action before the person can stop it |
| [jnli-support](jnli-support/questions/base.md) | pass a claim its source backs, send back one it contradicts, when sure | coverage at 95% accuracy | a wrong "backed" lets a claim the source does not support reach the reader |
| [visa-defect](visa-defect/questions/base.md) | send an item read defective to a person | recall at 10% false alarms or fewer | half of these photos are defective, so an accuracy target says little about a line where few are |
| [gh-gemini-needinfo](gh-gemini-needinfo/questions/base.md) | ask the reporter for more information | recall at 5% false alarms or fewer | asking someone who gave everything is the mistake that costs most |
| [nod-wake](nod-wake/questions/base.md) | wake an agent for a message, or let it sleep | loss per case (miss 10, false alarm 1) | a missed message drops work; a needless wake costs one LLM call |
| [gh-gemini-pr-rework](gh-gemini-pr-rework/questions/base.md) | review the pull requests most likely to need rework first | AUROC | a forecast: nothing is acted on alone, so the order is what counts |
| [helpsteer2-helpfulness](helpsteer2-helpfulness/questions/base.md) | score a response as a judge | MAE (levels) | the score is used as a number; annotators are 0.76 levels apart from each other |

gh-ruff-kind keeps the maintainers' labels as applied, though about 3 in 10 record a decision they made later that
the issue text does not hold (its `task.py` says which). Its low coverage shows a decision that should mostly go to
a person, not a weak model.

Coverage is the share of cases a model answers on its own while those answers keep the target accuracy; the rest
go to a person. It fits a question with one right answer (yes/no, a choice). A gate is measured by the errors it
makes on each side, and a score by its distance from people's.

Each folder holds `questions/base.md` (the report), `questions/base.json` and `comparison.json` (the same
numbers, with the curves). `python plugin/skills/s1flow/scripts/charts.py comparison.json` draws a page from one.
