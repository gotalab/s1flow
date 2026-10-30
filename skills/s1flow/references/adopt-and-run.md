# Adopt and run

Evaluation is development work. It produces a candidate and, after the final check, a versioned
runtime specification. The base install can validate and run that specification without installing
the evaluation extra:

```bash
s1flow policy create spec.json --connections s1flow.toml --check
s1flow policy create spec.json --root policies
s1flow promote ticket-kind@v3 --root policies --connections s1flow.toml --json
```

`policy create` only accepts a v2 `PolicySpec` and never overwrites a saved version. With `--check` it
only validates the file; adding `--connections` also binds its `connection` and `model_id` to the trusted
connections in that file. `promote` always checks that binding. A valid unevaluated version can be
activated manually. If an evaluation record exists, `promote` also checks that its execution digest
still matches the supplied connections and reports the held-out test result. `--force` can override a
below test verdict; it cannot make stale execution conditions current.

The evaluation loop is:

```bash
s1flow compare <task> --json                   # preferred overview of model × question variants
s1flow rank <task>                              # development comparison; writes nothing
s1flow adopt <task> <candidate> --reason "..."  # write the next policy and adoption record
s1flow check <task> --candidate next             # final held-out check
s1flow promote <task>@v<N> --connections s1flow.toml
```

The user or an agent with authority chooses the candidate and records why. `adopt` then explicitly scores that
selected candidate on the held-out test and records the result. The choice may differ from the
explicit objective-based ranking when the candidate is eligible. `compare`, `rank`, `report` and the optional HTML
page describe development data; they do not activate a runtime policy. `check` is the final test comparison
before promotion. Recommendation, adoption, and the current channel remain separate; ordinary compare/rank/report
do not read the held-out share.
Historical benchmark files are reference material only and are not proof that a current model works;
run the current task when a claim matters.

An application owns the trusted model connections. Bind the runtime explicitly and keep the policy
separate from the connection file. In `app.py` beside `connections.toml`, anchor paths to the file,
so starting the application from another directory does not change its configuration:

```python
from pathlib import Path
from s1flow import Client, policies

APP = Path(__file__).resolve().parent
client = Client(connections=APP / "connections.toml")  # grants every connection listed in this file
runtime = policies.load(path=APP / "policies/ticket-kind/v1.json", client=client,
                        log=APP / "decisions.jsonl")
decision = runtime.decide({"title": "...", "body": "..."}, case_id="issue-123")
print(decision.value, decision.probability, decision.below_min_probability, decision.decision_id)

# When the right label is known, use the exact id returned above.
runtime.feedback(decision.decision_id, True)
```

`case_id` is kept on an answered or failed log line for application context and may repeat. It does
not identify a unique judgement. Feedback uses the returned `decision_id` so a repeated case cannot be
attached to the wrong answer. The lower-bound field is `None` when the policy has no
`min_probability`, `True` below the bound, and `False` at or above it.

For another repository, another language, or a GitHub workflow, read `references/workflow.md` (`s1flow
guide workflow`). `s1flow policy export` writes a runtime-only policy set that the application can
vendor and review. The decide Action installs s1flow in the workflow when needed; the Python SDK never
installs dependencies at runtime.
