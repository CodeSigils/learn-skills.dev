---
name: shaping
description: Use when scoping work or choosing between approaches before writing code. Separates problems from solutions, evaluates options with binary fit checks, and produces a lightweight shaping doc. Trigger on phrases like "not sure which approach", "should we build X or Y", "what's the scope", "tradeoffs between", "before we start", or whenever multiple viable solutions exist and none is obviously right. Pairs with the `slicing` skill, which plans how to build the selected shape.
---

# Shaping

## Overview

Shaping is thinking before building. It answers two questions:

1. **What problems are we solving?** (Requirements)
2. **What solutions are possible?** (Shapes)

**Core principle:** Problems and solutions are different things. Name them separately. Evaluate them against each other.

## When to Use

- Starting a new feature or project
- Unclear what to build or which approach to take
- Multiple possible solutions and no clear winner
- Need to scope work before committing to an approach

**Not for:** Work where the problem and solution are both obvious. Just build it.

## The Conversation

Shaping is a thinking partnership, not a document-generation exercise:

- Propose concrete solution mechanisms, not intentions
- Challenge shapes that sound good but don't actually address requirements
- Surface tradeoffs the human hasn't considered

**Don't rush to document.** Think first, write when the picture is clear enough to be useful.

## Clarify First

Before proposing shapes, clear ambiguity in the original request with a brief back-and-forth. Shapes built on unexamined assumptions waste work, and the user usually has context you lack.

**What to probe:**
- **Purpose** — what's the underlying problem? What hurts right now?
- **Success criteria** — how do we know it worked? What's "good enough"?
- **Constraints** — deadlines, stack, existing systems, team capacity
- **Hidden assumptions** — things treated as obvious that might not be (scale, audience, who operates it, failure modes)
- **Scope** — what's explicitly out? v1 vs. later?

**How to ask:**
- One question at a time, or a tight batch of 2–3 closely related ones. No walls of questions.
- Prefer multiple choice — faster for the user than open-ended, and surfaces options they may not have considered
- Scale to the request: a small ask may need one check; a feature-sized ask may need several rounds
- If the request spans multiple independent subsystems, flag that first — decompose before clarifying details

**When to skip:** Truly unambiguous requests where the shapes are already obvious. Bias toward asking — under-asking costs more than one extra exchange. But don't fire questions to look thorough; each one should close a specific ambiguity that would change a requirement or a shape.

## Requirements (R)

Requirements describe **what's needed**, not what satisfies it.

- Numbered: `R0, R1, R2…` — max 9 top-level (few enough to hold in your head at once; if you need more, you're solving multiple problems)
- Each has a status: `core | must | nice | out`
- A requirement states a problem or constraint, never a solution
- If a requirement sounds like a solution, there's a hidden problem underneath — find it

| ✅ Requirement | ❌ Not a requirement |
|---|---|
| "Users need to find items quickly" | "Add a search bar" |
| "State must survive page refresh" | "Use localStorage" |
| "Admins need to see who changed what" | "Add an audit log table" |

**Negotiate status.** Not everything is `must`. Ask: "What happens if we don't do this?" If the answer is "it's fine for now," that's `nice` or `out`.

## Shapes (A, B, C)

Shapes are mutually exclusive solution approaches. Pick one.

- Lettered: `A, B, C…`
- Each shape is a short list of **mechanisms** — concrete things you build or change
- Mechanisms describe *what*, not *why* (requirements already cover *why*)
- If two shapes share most mechanisms, they're not different shapes — they're variants of one shape

**Parts must be mechanisms:**

| ✅ Mechanism | ❌ Not a mechanism |
|---|---|
| "URL query params store filter state" | "Make it fast" |
| "Server-side search with debounced input" | "Good search experience" |
| "Webhook fires on record change" | "Keep systems in sync" |

If a shape part restates a requirement in different words, it adds no information. Delete it.

## Fit Check

The decision tool. A matrix of Requirements × Shapes.

```markdown
| Req | Requirement | Status | A | B | C |
|-----|-------------|--------|---|---|---|
| R0  | Find items quickly | core | ✅ | ✅ | ✅ |
| R1  | State survives refresh | must | ✅ | ❌ | ✅ |
| R2  | Works offline | nice | ❌ | ❌ | ✅ |
```

**Rules:**

- **Binary only** — ✅ or ❌. Never "partially" or "with some work." It either addresses the requirement or it doesn't.
- If you don't know whether a shape addresses a requirement, that's ❌. Uncertainty is not a pass.
- If a shape passes all checks but feels wrong, there's a missing requirement. Articulate it, add it, re-run the check.
- `nice` and `out` requirements don't disqualify a shape, but they inform the decision.

## Output

Ask where to capture output — repo file (e.g., `shape.md`), task tracker, or wiki — and format the summary to fit. `shape.md` is a lightweight working doc, not a specification.

If writing `shape.md`, use the template below as a starting point, not a mandate. The fit check table is the one non-negotiable — it's where thinking becomes visible.

```markdown
# [Project Name] — Shape

## Problem
2-3 sentences. What hurts, what does good look like.

## Requirements
| # | Requirement | Status |
|---|-------------|--------|

## Shapes
### Shape A: [Name]
- mechanism 1
- mechanism 2

### Shape B: [Name]
- mechanism 1
- mechanism 2

## Fit Check
| Req | Requirement | Status | A | B |
|-----|-------------|--------|---|---|

## Decision
[Which shape and why. 1-2 sentences.]
```

Once a shape is selected, if its mechanisms need ordering into increments, hand off to the `slicing` skill.

## Red Flags

- **Requirements that are solutions in disguise** — find the problem underneath
- **Shapes that are identical except for one detail** — that's one shape with a decision point, not two shapes
- **"We need all of these"** — if everything is `must`, nothing is prioritized. Push back.
- **Fit check with all ✅** — either the shapes aren't different enough or requirements aren't specific enough
- **Giant requirements list** — if you have more than 9, you're solving multiple problems. Split them.
- **Premature detail** — shaping decides *what* and *which approach*, not *how exactly*. Implementation details belong in slicing.
- **Jumping to shapes on an ambiguous request** — if you can see two plausible interpretations of what the user wants, ask before shaping. You'll shape the wrong thing otherwise.
