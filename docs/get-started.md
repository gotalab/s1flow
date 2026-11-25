---
description: Ask your coding agent to compare Decision Models on your own cases, then run your pick in your app. Install the CLI and the s1flow Skill first.
---

# Get started

You use s1flow by asking your coding agent. Say what to decide, in your own words:

```text
Use s1flow to decide whether a new GitHub issue is a bug. Call the task is-bug,
collect 200 labeled issues, compare the models and show me the result.
```

The agent collects the cases, compares the models and shows you the result. You make the choice, and your app runs
it. Before the first ask, your agent needs the CLI and the s1flow Skill.

## Install the CLI

You need Python 3.13 or later.

```bash
uv tool install "s1flow[eval]"
```

## Add the Skill to your coding agent

| Agent | How |
|---|---|
| Claude Code | `/plugin marketplace add gotalab/s1flow`, then `/plugin install s1flow@s1flow` |
| Codex | `codex plugin marketplace add gotalab/s1flow`, then install s1flow from the Plugins directory |
| Antigravity, Cursor and other agents | `s1flow init --skill` copies the Skill into `.agents/skills/` and `.claude/skills/` at the Git root |

Plugins update through your agent's plugin manager. `s1flow init --skill` copies the files into your repository
instead, so they change only when you run it again.

Antigravity's default terminal sandbox has no network, so it asks before each s1flow command that calls a model.
To stop the prompts, allow `command(s1flow)` in its [permission settings](https://antigravity.google/docs/permissions).

## Ask your agent

With the Skill in place, make the ask above. The agent runs `s1flow init`, which creates an `s1flow/` folder and
touches nothing else in your repository. The default line-up needs one key, `OPENROUTER_API_KEY`, and fetching
issues needs the `gh` CLI, signed in.

From there the agent:

1. writes the task (`s1flow/tasks/is-bug/task.py`): the question, how to read the label, and the objective,
2. collects labeled cases and checks them with `s1flow cases check`,
3. asks every model in the line-up with `s1flow run`,
4. shows you the comparison from `s1flow report`, and leaves the choice to you.

The comparison shows, for each model and prompt, how much of the decision it can take on its own at your target
accuracy, with confidence intervals, latency and cost. [Concepts](concepts.md) explains why that, and not accuracy
alone, is what to look at.

## Choose, and save the choice as a policy

When you pick a model, the agent runs `s1flow adopt`. It tests your pick on the cases held out during the
comparison, and saves it only if it passes. The result is a *policy*: one JSON file holding the model, the
question and the confidence threshold. Open a pull request with it; merging it is the release.

## Run it in your app

Your app needs only the base package, which depends on just httpx and pydantic, plus a `connections.toml` that
lists the models it is allowed to call ([format](app.md#your-first-decision)).

```bash
pip install s1flow
```

```python
from s1flow import Client, policies

client = Client(connections="connections.toml")
policy = policies.load(path="s1flow/policies/is-bug/v1.json", client=client)
decision = policy.decide({"text": "Crash on startup"})
decision.value, decision.probability   # True, 0.93
```

What your app does with the answer is up to your code: act on it, or send it to a person when the probability is
below the policy's minimum. Record the correct answer once you know it, and it becomes a case in the next
comparison ([Feedback and improvement](feedback.md)).

No labels yet? You can [ship a policy today](app.md) and evaluate it later.

## Next

- [Concepts](concepts.md): the words s1flow uses, and why it checks before it hands off.
- [Evaluate and compare](evaluate.md): the commands behind the agent's work.
- [Benchmarks](benchmarks/index.md): what a comparison looks like, on public tasks.
