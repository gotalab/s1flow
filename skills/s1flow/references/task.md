# Write the task and check its cases

## Write the task

`tasks/<id>/task.py` defines `task` (its `id` is the directory's name):

```python
from s1flow.objectives import Accuracy
from s1flow.questions import Choice
from s1flow.eval import Task

task = Task(
    id="ticket-kind",
    cases="data.jsonl",
    state=lambda r: {"title": r["title"], "body": r["body"][:1500]},
    question_id="kind",
    question=Choice(instructions="What kind of ticket is this?", criteria={"bug": "...", "question": "...", "feature": "..."}),
    label=lambda r: r["label"],          # None leaves the case out
    objective=Accuracy(),
    source="where the cases come from, with its license",
    show=lambda r: r["title"],           # one line per case in reports
)
```

A boolean question with a choice-like label uses `Boolean(...)`; a choice scored as one option
against the rest sets `kind_params=KindParams(positive="bug")` (`from s1flow.eval import KindParams`). When some mistakes cost more than others, `objective=Loss(default=1,
losses={"server": {"formatter": 3}})` (a loss table: right answer -> answer given -> loss; "true" / "false" for a boolean),
or `ExpectedLoss(fn=, fp=)`; the weights are the user's to set, never yours: ask, and show them report's
lines for the weights halved and doubled. A measure s1flow lacks is a function in task.py:
`@per_case(direction="min", sets="threshold") def wake_loss(label, reading, *, miss: float = 20.0) -> float`,
then `objective=wake_loss(miss=20)`. `objective=` is the one objective that decides how the policy
reads its answers; `tiebreak=[...]` lists, in order, what orders the candidates it cannot tell apart: more
objectives, each measured at the rule `objective=` chose, and `"latency"` and `"cost"`, measured on the calls
(the template writes `tiebreak=["latency", "cost"]`; a tiebreak leaving one out does not use it, and with no
tiebreak the candidates the objective cannot tell apart are listed unordered). Latency
and API cost also limit candidates through `constraints=Constraints(latency_p99_ms=..., cost_per_10k_usd=...)`. Latency counts
only between candidates run at one concurrency with retries recorded; otherwise report says so and how to run
them again (`s1flow run <id> --fresh --concurrency N`, one N for all). Re-running asks every candidate again:
say what it will spend before suggesting it. When the decision is only useful above some precision and recall
(an alert nobody ignores, a gate that catches enough), set them as floors on a binary task:
`constraints=Constraints(min_precision=0.8, min_recall=0.8)` with an objective that sets the threshold
(any binary objective but Coverage and AUROC). The threshold is chosen among those that keep both, and a model that
cannot keep them is excluded with the reason; the floors are the user's to set, like the weights. How the team already decides (a triage policy,
CONTRIBUTING, a bot's prompt) goes in `tasks/<id>/context.md`: `optimize` reads it, the model
never does.

## Check the cases

```bash
s1flow cases check <id>
```

Fix every ✗ (a state that does not build, a label outside the options, a duplicate with another
label). Read every ⚠ with the user: a smaller side under 20% means Accuracy rewards always
answering the larger side.
