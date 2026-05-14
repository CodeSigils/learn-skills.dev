---
name: decision-making
description: Apply decision-making frameworks to compare options, prioritize work, and manage tradeoffs under uncertainty.
compatibility: opencode
metadata:
  audience: general
  workflow: decisions
---

# Decision Making

## What this skill does

Use this skill when the main task is choosing what to do, what to do first, or how to act under uncertainty.

This domain covers option comparison, prioritization, consequence analysis, assumption checking, and response style.

## When this domain is appropriate

Use it when the user is mainly asking:

- which option is best
- what should be prioritized now
- what kind of decision this is
- what consequences a decision may create
- how to move under uncertainty or speed pressure

Do not use it when the real problem is root-cause diagnosis, system mapping, or message drafting.

## Routing logic

- classify decision type first -> `frameworks/hard-choice-model.md`
- compare explicit options on shared criteria -> `frameworks/decision-matrix.md`
- prioritize by impact vs effort -> `frameworks/impact-effort-matrix.md`
- prioritize by urgency vs importance -> `frameworks/eisenhower-matrix.md`
- test long-term consequences -> `frameworks/second-order-thinking.md`
- check whether conclusions are over-interpreted -> `frameworks/ladder-of-inference.md`
- force perspective balance -> `frameworks/six-thinking-hats.md`
- decide iteratively in a fast-changing context -> `frameworks/ooda-loop.md`
- match response style to context type -> `frameworks/cynefin-framework.md`
- set the right speed/quality posture -> `frameworks/confidence-determines-speed-vs-quality.md`

## Framework chaining

- `hard-choice-model.md` -> `decision-matrix.md` when options are comparable and high impact
- `decision-matrix.md` -> `second-order-thinking.md` to stress-test the leading option
- `ladder-of-inference.md` -> any recommendation when assumptions seem fragile
- `cynefin-framework.md` -> `ooda-loop.md` when the context is complex or chaotic
- `confidence-determines-speed-vs-quality.md` after a choice to set execution pace

## Execution policy

Before applying a framework:

1. State the decision clearly.
2. Name the options if present.
3. Separate facts from assumptions.
4. Choose the minimum framework or sequence needed.
5. Follow the selected framework file's process exactly.
6. End with a recommendation, tradeoff summary, and next action.

## Output contract

- `Goal:`
- `Chosen framework:`
- `Why this framework:`
- `Known facts:`
- `Assumptions:`
- `Reasoning:`
- `Recommendation:`
- `Tradeoffs:`
- `Recommended next action:`

## Framework references

- `frameworks/six-thinking-hats.md`
- `frameworks/eisenhower-matrix.md`
- `frameworks/second-order-thinking.md`
- `frameworks/decision-matrix.md`
- `frameworks/impact-effort-matrix.md`
- `frameworks/ladder-of-inference.md`
- `frameworks/hard-choice-model.md`
- `frameworks/ooda-loop.md`
- `frameworks/cynefin-framework.md`
- `frameworks/confidence-determines-speed-vs-quality.md`
