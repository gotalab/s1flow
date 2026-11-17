---
description: Decision Models, tasks and cases, objectives, confidence thresholds, policies and feedback, and why s1flow checks a judgment before handing it off.
---

# Concepts

s1flow is built on one idea: **check a repeated judgment on your own data before you hand it to a Decision
Model, and hand off only the part the model is sure of.** This page explains the words that idea needs, in the
order of the loop s1flow runs: collect cases, compare, run, feed back.

## Decision Models

Automation is full of branch points: should the agent act or ask, which team gets this ticket, is this message
worth waking someone for. Each is a judgment made again and again, on inputs that look alike.

A Decision Model answers one typed question about an input, such as yes or no, or one of several options, and
returns a probability with the answer instead of free text. Jev, Clef, d1 and OpenAI's Decisions API are Decision
Models (some providers call them System One models). They are fast and cheap enough to sit on every branch point,
but no model is right on every input, and how often it is right depends on your inputs, not on a public score.

## Tasks and cases

A **task** is one decision: the question, the labeled cases, and how to measure the answers. It lives in
`tasks/<task>/task.py` inside the `s1flow/` folder of your repository.

A **case** is one input (the *state*, such as an issue's title and body) with its correct answer (the *label*).
Cases come from wherever the decision already happens: GitHub issues, app logs, labels you already have, or a
person's answers to the decisions the model was unsure of.

A share of the cases is **held out** when you first run a task. Comparisons use only the rest, so the held-out
cases can give an honest final test of the one you choose.

## Candidates and objectives

A **candidate** is a model with one way of asking the question (a *question variant*, or prompt). s1flow asks
every candidate the same cases and measures each by the task's **objective**: the measure that matches what the
answer is used for.

Accuracy alone is rarely that measure. Two models can be equally accurate while one of them is sure of far more of
its answers, so it can take over more of the work. The objective says what "good enough to hand off" means for this
decision:

| The answer is used to | Objective |
|---|---|
| act when sure, send the rest to a person | **coverage** at a target accuracy: the share of cases the model answers on its own while those answers stay at the target |
| catch the cases that need action, without too many false alarms | **recall** at a cap on false alarms |
| choose between errors that cost different amounts | **expected loss** per case, with a cost for each kind of error |
| put the most likely cases first | **AUROC**: how well the probabilities order the cases |
| give a score that is used as a number | **MAE**: how far the score is from people's |

The objective goes in `task.py`, with the reason for it. Who sets it is whoever owns the decision; s1flow measures
against it and never picks one for you.

## Confidence thresholds

A Decision Model's probability is what lets you hand off only part of a judgment. For each candidate, s1flow finds
the **threshold** that meets the objective on your cases: answers above it are sure enough to act on, and the rest
go to a person. When you adopt a candidate, the held-out cases check its threshold on inputs it was never fit on.

Every result comes with a confidence interval. When the intervals of two candidates overlap, s1flow shows them as
not told apart rather than pretending one is better. A comparison is something to choose from, not a ranking.

## Policies

When you choose a candidate, `s1flow adopt` tests it on the held-out cases and saves it as a **policy**: one JSON
file with the model, the question and the threshold. Your app loads that file and decides with it.

**What runs is what you measured.** A policy pins everything that changes the answers: the model and its version,
the question, how the input is sent, and the threshold. Change any of them and the old measurement no longer
applies; you measure again and save a new version. Saved versions are never rewritten, so the version your app ran
can always be read as it shipped.

Saving a policy changes your working tree only. The pull request that carries it is the review, and merging it is
the release. See [Policies, evidence and releases](policies.md).

## Feedback

Each decision your app makes has a **decision ID**. When you learn the correct answer, from the person who handled
an unsure case or from what happened next, record it against that ID. s1flow then measures the policy on real
traffic, and turns the decisions with known answers into new cases for the next comparison. That closes the loop:
the cases grow where the model was unsure, and the next comparison is measured on them.

See [Feedback and improvement](feedback.md).

## What stays in your app

s1flow keeps only what would change the measurement, or what is needed to bring the correct answer back. Acting on
the answer, where unsure answers go, falling back when a call fails, and how several decisions are combined stay in
your code or your agent framework. s1flow runs inside your Python app or as the CLI, with no server of its own.
[Why, and what it means for your app](app.md#what-s1flow-leaves-to-your-app).
