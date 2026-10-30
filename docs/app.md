# Run decisions in your app

This page takes you from nothing to a saved policy that your app calls, using only the base install. You don't
need labels or an evaluation to get started. Once you have labeled cases, move on to
[Evaluate and compare](evaluate.md).

## Install the runtime

You need Python 3.13 or later. Add the base package to your app. It depends directly on just httpx and pydantic,
and it neither installs nor imports the evaluation tools.

```bash
uv add s1flow   # or: pip install s1flow
```

## Your first decision

Your app decides which model connections it allows. For example, `connections.toml`:

```toml
default = ["triage"]

[models.triage]
provider = "typesafe"
id = "jev-1.14.0" # use a model ID your account has access to
```

Put the provider's API key in the environment (`TYPESAFE_API_KEY` in this example). In a sandbox whose proxy adds
the key on the way out (a network secret), leave the variable unset: s1flow then sends no key of its own, and a
401 or 403 back is reported as the key not being set. Which file is trusted, and
how the SDK and the CLI find it, is covered in [Connections and discovery](connections.md).

The file must define the connection that a policy names. A policy adopted from an evaluation names a model from
your project's line-up, such as `jev@openrouter`, so copy that model's entry from `s1flow/s1flow.toml`.

Now write `bug.json`. You don't need any evaluation data, model responses or placeholder scores:

```json
{
  "schema": "s1flow/policy@2",
  "task": "ticket-bug",
  "version": 1,
  "connection": "triage",
  "model_id": "jev-1.14.0",
  "questions": {
    "bug": {
      "question": {"type": "boolean", "instructions": "Does this report describe a software defect?"},
      "rule": {"threshold": 0.5}
    }
  }
}
```

```bash
s1flow policy create bug.json --connections connections.toml --check --json
s1flow adopt --spec bug.json --root policies --connections connections.toml --reason "first rule" --json
s1flow decide --policy ticket-bug@v1 --path policies/ticket-bug/v1.json \
  --connections connections.toml --state '{"text":"Crash on startup"}' --json
```

`policy create --check` checks the policy without calling a model or saving it. With `--connections`, it also checks that the
file defines the connection and that the connection allows the policy's model ID. `adopt --spec` saves the policy as a new version that can't be changed,
stamped with when it was created and which SDK version created it, and makes it current; it doesn't claim the
policy has been evaluated.

In `app.py`, next to `connections.toml`, build paths from the location of the file itself so it doesn't matter
which directory the app is started from:

```python
from pathlib import Path
from s1flow import Client, policies

APP = Path(__file__).resolve().parent
client = Client(connections=APP / "connections.toml")
policy = policies.load(path=APP / "policies/ticket-bug/v1.json", client=client,
                       log=APP / "decisions.jsonl", keep_state=True)
decision = policy.decide({"text": "Crash on startup"}, case_id="ticket-42")
print(decision.value, decision.probability, decision.decision_id)
policy.feedback(decision.decision_id, True)  # the correct answer, once you know it
```

## The policy API

You can also build a `PolicySpec` in Python and pass it to `DecisionPolicy(spec, client=client)`. Use `adecide`
for async code. Neither `decide` nor `adecide` reads a Task or an Evaluation.

The optional `state_schema` checks the shape of the input against a subset of JSON Schema: object, array and
scalar types, properties, required fields and additional properties. It is not a full JSON Schema validator. If
the input doesn't match, you get a `DataError` before any request is sent. Without a schema, s1flow can't
promise that production inputs have the same shape as the ones you evaluated.

A `DecisionRule` can set a `threshold` (for a yes/no question, or a choice question with a positive option) and a
`min_probability`.
`Decision.below_min_probability` is `None` when no minimum is set, `True` when the answer's probability is below it, and
`False` otherwise. It doesn't mean the answer is right, or that the action is allowed. Your app decides what to
do, who is allowed to do it, and when to escalate or fall back.

## Errors

If a provider returns an invalid response, s1flow raises `ProviderError` instead of returning a decision. A
refused question comes back as `Refusal` from the Client and as `Rejected` when a policy runs. Configuration
errors, bad input and unsupported features each raise their own subclass of `S1flowError`.

## Images and logged input

Images must be passed as `Image` values that your code prepares before the policy runs. Input JSON can't make the
runtime fetch files or URLs. On the CLI, `--image PATH` loads a local file you name, and needs `s1flow[images]`.
Input is logged only if you ask for it (`keep_state=True` or `--keep-state`).

## Call a model directly

Use `Client` or `AsyncClient` when you don't need a saved policy or a threshold. You still don't need an
evaluation.

```python
from s1flow import Client
from s1flow.client import ModelSpec
from s1flow.questions import Boolean

response = Client().responses.create(
    model=ModelSpec(provider="typesafe", id="jev-1.14.0"),
    state={"text": "Crash on startup"},
    questions={"bug": Boolean(instructions="Does this report describe a software defect?")},
)
print(response.answers["bug"].probability)
```

The `ModelSpec` here is written in your own code, so this example needs no connection file. If you refer to
the model by an alias instead, pass the app's list of allowed models:

```python
response = Client(connections="connections.toml").responses.create(
    model="triage",
    state={"text": "Crash on startup"},
    questions={"bug": Boolean(instructions="Does this report describe a software defect?")},
)
```

The Client supports yes/no (`boolean`), choice, score and box questions, and several questions in one request, as far as
the provider supports them. Comparisons support yes/no, choice and box questions, but not score. A policy holds
one yes/no or choice question.
