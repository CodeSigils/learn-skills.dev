---
name: plan-ceo-review
version: 1.1.0
description: |
  Founder-mode product review. Rethinks the problem, challenges scope, searches
  for stronger product opportunities, and chooses one of four review modes:
  SCOPE EXPANSION, SELECTIVE EXPANSION, HOLD SCOPE, or SCOPE REDUCTION.
benefits-from: [interrogate-me, plan-review-intake, plan-review-scope]
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
  - AskUserQuestion
---

# Plan CEO Review

Review the plan from a founder/product strategy perspective before execution.
Do not implement. Keep the user in control of every scope change.

## Guardrails

- Challenge assumptions directly and write down unresolved ambiguity.
- Prefer focus over expansion unless the user explicitly chooses an expansion mode.
- Treat each opportunity as optional until accepted. Do not smuggle rejected ideas into scope.
- Define success in observable product or business terms, not vague quality claims.

## Skill Chain

For a full founder/product review, run these local skills in order:

1. `/plan-review-intake` - find the plan and local `.planning/*` context.
2. `/interrogate-me` - stress-test the problem, user, scope, assumptions, risks, and tradeoffs.
3. `/plan-review-scope` - establish what already exists, what is in scope, and what is out of scope.
4. `/plan-ceo-strategy` - select the review mode and challenge the product direction.
5. `/plan-ceo-opportunities` - surface expansion, simplification, positioning, and trust opportunities one at a time.
6. `/plan-ceo-wrapup` - write the `.planning/reviews/plan-ceo-review.md` artifact.

If a named skill is unavailable, inline that section using the same instructions
from the corresponding skill file name above.

## Review Modes

- `SCOPE EXPANSION`: dream bigger and propose high-leverage improvements. Every expansion requires explicit opt-in.
- `SELECTIVE EXPANSION`: preserve baseline scope while offering optional improvements one by one.
- `HOLD SCOPE`: make the accepted scope sharper, more coherent, and safer without expanding or reducing it.
- `SCOPE REDUCTION`: find the smallest version that still achieves the core outcome.

Once the user chooses a mode, do not drift modes.

## Product Review Principles

- Start with the user problem, not the proposed implementation.
- Separate reversible decisions from one-way decisions.
- Prefer focus: fewer things, better.
- Challenge proxy metrics that do not prove user value.
- Look for trust, safety, onboarding, and retention consequences.
- Ask what would make the plan fail, then remove or expose those failure paths.
- Prefer complete, bounded work over shortcuts that leave avoidable quality gaps.
- Write all durable outputs under `.planning/*`.

## Required Output

Write or update `.planning/reviews/plan-ceo-review.md` with:

- `Status`: `CLEAR`, `CLEAR_WITH_CONCERNS`, `NEEDS_DECISION`, or `BLOCKED`
- `Review mode`
- `Plan reviewed`
- `Problem framing`
- `Target users and use cases`
- `Scope decisions`
- `Accepted opportunities`
- `Rejected opportunities`
- `NOT in scope`
- `Risks and reversibility`
- `Success metrics`
- `TODO proposals`
- `Unresolved decisions`
- `Completion summary`

When a larger strategy document is useful, write it under:

`.planning/strategy/{feature-slug}.md`

Do not write durable workflow artifacts outside `.planning/*`.
---

> **Install:** ``npx skills add ChristopherAlphonse/calphonse-skills --skill plan-ceo-review``
