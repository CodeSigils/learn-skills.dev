---
name: architecture-review
description: "Find practical architecture improvements in a codebase. Use when the user asks to improve architecture, reduce coupling, find refactoring opportunities, make code easier to test, or identify shallow modules. Prefer evidence from the current repo over generic architecture advice."
---

# Architecture review

Use this to find refactors worth considering. Do not produce a grand redesign unless the user asks for one.

## Focus

Look for places where the current shape makes change harder:

- One concept is spread across many files.
- A module is mostly pass-through glue.
- Callers must know too many ordering rules, flags, or data-shape details.
- Tests need awkward mocks because behavior has no useful seam.
- Two modules change together often enough that the boundary is probably wrong.
- A dependency points inward toward business logic instead of outward through an adapter.

## Review shape

Return a short ranked list. For each candidate include:

- Files involved.
- The friction, with evidence from code.
- The smallest useful refactor.
- Why it improves locality, testability, or coupling.
- Risk: behavior, migration, or churn.

Use existing project terms from `SPEC.md`, docs, and ADRs when they exist. If an ADR rules out the obvious refactor, say so and either skip it or explain why the friction may justify revisiting it.

## Guardrails

- Prefer local changes over architecture theater.
- Do not introduce interfaces for single implementations unless they remove real caller knowledge or isolate an external dependency.
- Do not recommend a pattern just because it is common.
- Stop when you have enough evidence for the top few candidates.
