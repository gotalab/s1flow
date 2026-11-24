---
description: Check a repeated judgment on your own data, then hand it to a Decision Model.
hide:
  - navigation
  - toc
---

# Check a repeated judgment on your own data, then hand it to a Decision Model { .hero-title }

Automation is full of small branch points: should the agent act or ask, which team gets this ticket, does this
message need a reply. A Decision Model answers one typed question like these fast, with a probability. s1flow
measures on your own cases how much of the judgment a model can take over at the accuracy you need. Your app acts on
the answers the model is sure of and sends the rest to a person, and the person's answers become new cases.
{ .hero-lead }

[Get started](get-started.md){ .md-button .md-button--primary } [How it works](concepts.md){ .md-button }

<figure class="flow" markdown>
![Your coding agent, with the s1flow Skill, collects your labeled cases and measures Decision Models on those cases. You choose the one you trust, and your app decides with it exactly as measured: answers above the confidence threshold are acted on, the rest go to a person, and the person's answers become new cases.](images/how-it-works.svg#only-light)
![](images/how-it-works-dark.svg#only-dark)
</figure>

<div class="entries" markdown>

- [**Get started**](get-started.md)
  Install the CLI, add the Skill to your coding agent, and ask it for your first comparison.
- [**Concepts**](concepts.md)
  Decision Models, cases, objectives, thresholds and policies: why s1flow checks before it hands off.
- [**Evaluate and compare**](evaluate.md)
  Collect labeled cases and compare models and prompts on the objective your decision needs.
- [**Run decisions in your app**](app.md)
  Load the policy you chose and decide with it, exactly as it was measured.
- [**Feedback and improvement**](feedback.md)
  Record the correct answers, measure in production, and turn them into new cases.
- [**Benchmarks**](benchmarks/index.md)
  A dated snapshot of Decision Models on public tasks, each measured by what its answer is used for.

</div>
