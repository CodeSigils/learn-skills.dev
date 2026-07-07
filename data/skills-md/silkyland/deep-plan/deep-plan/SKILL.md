---
name: deep-plan
description: >-
  Research-first, evidence-first implementation planning in seven gated phases:
  frame the task, inventory the real codebase, verify ground truth from vendor
  source or official docs, adversarially audit existing code, analyze gaps,
  commit to design decisions, and write a phased plan document with timeline,
  risks, and verification. Enforces "no claim without evidence, no design
  before research". Use when the user asks to plan, design, architect, audit,
  or review before implementing a feature, refactor, migration, or system, or
  mentions deep-plan, /deep-plan, or Plan mode.
license: MIT
argument-hint: "[task] [project-root] [ground-truth-source] [plan-output-path]"
---

# Deep Plan

Audit-grade planning: **evidence first, design later, never guess.**

You are producing a plan that a junior implementer agent can execute **without
asking a single question**. That is the bar. Everything below exists to reach it.

## The Prime Directive

> **No claim without evidence. No design before research.**

Every statement in your plan is one of:

| Tag | Meaning | Required proof |
|-----|---------|----------------|
| `VERIFIED` | You read it yourself, this session | `file:line`, vendor path, or URL + version |
| `UNVERIFIED` | You could not confirm it | Explicit label + what would confirm it |
| `CORRECTED` | You previously believed it and were wrong | The old belief AND the new evidence |

If you cannot cite it, you cannot claim it. Training-data memory of framework
APIs is **never** evidence — versions drift, and confident-but-wrong is the
most expensive failure mode in planning.

## Before you start

1. Read [references/protocol.md](references/protocol.md) in full — the phase
   protocol is mandatory and executed in order.
2. Switch to **Plan mode** if the tool supports it. Do not edit project files;
   the only file you write is the plan document.
3. Expect high token/time cost. That is the price of a plan an implementer can
   execute without guessing.

## Progress checklist

Copy this into your response and check items off as you complete each phase.
**A phase is complete only when its exit criteria in the protocol pass.**

```
Deep Plan Progress:
- [ ] Phase 0: Frame — task, scope, definition of done, inputs confirmed
- [ ] Phase 1: Inventory — codebase mapped with file paths, classified works/half-wired/dead
- [ ] Phase 2: Ground truth — every framework claim backed by vendor path or versioned doc URL
- [ ] Phase 3: Adversarial audit — defects with file:line, corrections recorded
- [ ] Phase 4: Gap analysis — numbered gaps: broken / missing / fights-the-framework
- [ ] Phase 5: Decisions — one committed recommendation per gap, evidence-cited
- [ ] Phase 6: Plan document — written with phased roadmap, risks, verification
- [ ] Phase 7: Self-review gate — checklist passed, zero-questions bar met
```

**GATE:** Phases 0–3 are research. Phases 5–6 are design. Do not write one line
of design until Phases 1–3 are checked. If mid-design you catch yourself
assuming an API, a schema, or a behavior you have not read — stop, go verify,
tag it, then resume.

## Inputs to collect (Phase 0)

Use the arguments provided with the invocation (some platforms substitute
them as `$ARGUMENTS`); otherwise infer from the repo. If a required
input is genuinely ambiguous, ask **one question at a time** and always attach
your recommended answer with a one-line reason.

| Field | Example |
|-------|---------|
| Task (2–5 lines: what, why, done-when) | Refactor cart pricing to use the framework's rule engine |
| Project root | `/Users/me/Sites/my-shop` |
| Ground-truth source | `vendor/shopware/core`, `node_modules/next`, or official docs URL |
| Plan output path | `docs/PLAN.md` |

## Execution rules

- Follow Phases 0–7 in [references/protocol.md](references/protocol.md) **in order**.
- If exploration subagents are available, fan them out **in parallel with
  distinct, non-overlapping scopes** (structure / data flow / config / history).
- Every bug or finding needs `file:line`. Every framework claim needs a vendor
  path or a versioned doc URL.
- Record every wrong assumption you catch in a **Corrections** ledger as you
  go. A plan that never found itself wrong did not look hard enough.
- The final plan contains **decisions, not menus**. Weigh alternatives during
  Phase 5, then commit.

## Output

- Write the plan document following
  [references/plan-template.md](references/plan-template.md) — including the
  dependency-ordered phased roadmap with entry/exit criteria, effort estimates,
  and a risk register.
- Before presenting, self-grade against
  [references/review-checklist.md](references/review-checklist.md). If any
  item fails, return to the relevant phase — do not present a failing plan
  as done.

## After acceptance

Once the plan is accepted (and again after implementation makes progress),
suggest running the companion skill **deep-plan-ingest** to distill the
plan's verified knowledge into durable project files: `AGENTS.md`,
`docs/ARCHITECTURE.md`, and `ROADMAP.md`. The plan document is a snapshot;
those three files are what future agent sessions actually load.

## If the plan is rejected

Reply briefly: `Checklist item <N> failed acceptance — returning to Phase <X>
to do the research for real.` Then actually do it.
