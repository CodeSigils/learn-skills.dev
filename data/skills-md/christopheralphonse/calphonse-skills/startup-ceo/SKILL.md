---
name: startup-ceo
version: 1.1.0
description: |
  Unified founder-mode product review. Orchestrates intake, interrogation, scope
  mapping, strategy selection, opportunity surfacing, and artifact writing.
  Delegates parallel research to sub-agents. Keeps user in control of every scope change.
benefits-from: [plan-ceo-review, plan-ceo-strategy, plan-ceo-opportunities, plan-ceo-wrap-up, interrogate-me]
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
  - AskUserQuestion
  - Agent
---

# Startup CEO Review

Full founder/product review before execution. Do not implement. Every scope
change requires explicit user opt-in.

## Guardrails

- Do not launch broad exploration when the plan, product surface, and decision needed are already clear.
- Keep each scope change explicit, reversible when possible, and tied to a concrete user or business outcome.
- Mark assumptions, rejected opportunities, and unresolved decisions plainly.
- Prefer the smallest product shape that proves the strategic bet before proposing expansion.

## Phase 1 — Research

For a full review, gather both lenses below. If the plan, product surface, and decision needed are already clear from local files, do the intake inline instead of launching broad exploration.

### Sub-Agent A: Plan Intake

**Type:** `Explore`

**Goal:** Locate the plan and all local planning context.

Instructions:

- Find `PLAN.md` or any `*.md` file that describes the feature/phase plan.
- Read `.planning/` directory tree: tasks, reviews, strategy, research files.
- Read `ROADMAP.md`, `MILESTONE.md`, `AI-SPEC.md` if present.
- Return: plan file path, plan summary (problem, users, scope, key decisions), list of `.planning/*` files found, any prior CEO review artifacts.

### Sub-Agent B: Codebase Scope Map

**Type:** `Explore`

**Goal:** Map what already exists vs what the plan proposes to build.

Instructions:

- Identify modules, files, and components that are in scope.
- Note what already exists (implemented), what is partially done, and what is entirely new.
- Flag external dependencies, integration points, and surfaces that affect trust or safety.
- Return: existing vs proposed breakdown, integration risks, surfaces that touch users directly.

Wait for both sub-agents to complete before proceeding.

## Phase 2 — Interrogation (Interactive)

Invoke the `interrogate-me` skill.

Pass the sub-agent findings from Phase 1 as context so the session is grounded in
the actual plan and codebase state rather than abstract questions.

`interrogate-me` will:

- Interview relentlessly about every aspect of the plan, one question at a time.
- Challenge against any existing domain glossary (`CONTEXT.md`, `ADR`s).
- Sharpen fuzzy or overloaded terminology.
- Cross-reference claims against the codebase and surface contradictions.
- Update `CONTEXT.md` inline as terms are resolved.
- Offer an ADR only when a decision is hard to reverse, surprising without context, and the result of a real trade-off.

Stop when enough signal exists to select a review mode confidently.

## Phase 3 — Strategy Selection (Interactive)

Using interrogation output:

1. Restate the product problem and target user in one sentence.
2. Identify the plan's implicit strategic bet.
3. Classify reversibility (reversible / one-way) and magnitude (small / large).
4. Recommend one mode:

   - `SCOPE EXPANSION` — dream bigger, propose high-leverage improvements.
   - `SELECTIVE EXPANSION` — preserve baseline, offer optional improvements one by one.
   - `HOLD SCOPE` — sharpen and de-risk accepted scope, no additions or cuts.
   - `SCOPE REDUCTION` — find smallest version that achieves the core outcome.

5. Present recommendation with rationale. Ask user to confirm.

Lock mode. Do not drift after confirmation.

## Phase 4 — Opportunities (Interactive)

Surface each meaningful opportunity as its own question. One at a time.

For each opportunity present:

- Plain-English description
- Recommendation
- 2–3 options with effort, risk, and completeness for each
- Whether acceptance changes scope

Evaluate across:

- Stronger user outcome
- Simpler product shape
- Trust and safety improvements
- Onboarding and activation
- Retention and repeated-use value
- Positioning and narrative clarity
- Work to remove (dilutes core outcome)
- Work to add (materially raises quality or value)

Accepted → scope. Rejected → `NOT in scope` or ask if user wants it in `.planning/tasks/TODOS.md`.

## Phase 5 — Wrap-up

Write or update `.planning/reviews/plan-ceo-review.md` with:

```markdown
# Plan CEO Review

**Status:** CLEAR | CLEAR_WITH_CONCERNS | NEEDS_DECISION | BLOCKED
**Review mode:** <mode>
**Plan reviewed:** <path>

## Problem Framing
## Target Users and Use Cases
## Scope Decisions
## Accepted Opportunities
## Rejected Opportunities
## NOT in Scope
## Risks and Reversibility
## Success Metrics
## TODO Proposals
## Unresolved Decisions
## Completion Summary
```

If a long-form strategy note is needed, write `.planning/strategy/{feature-slug}.md`.

For each rejected opportunity the user wants to preserve, ask:

- A) Add to `.planning/tasks/TODOS.md`
- B) Skip
- C) Put back into current plan

Do not write durable artifacts outside `.planning/*`.

## Principles

- Start with the user problem, not the proposed implementation.
- Separate reversible from one-way decisions.
- Fewer things, better.
- Challenge proxy metrics that do not prove user value.
- Ask what would make the plan fail — then remove or expose those paths.
- Prefer complete, bounded work over shortcuts that leave quality gaps.
---

> **Install:** ``npx skills add ChristopherAlphonse/calphonse-skills --skill startup-ceo``
