---
name: simplify
description: "Simplify code, architecture, and prose while preserving behavior and intent. Use when asked to reduce complexity, clean up confusing implementation, make code easier to maintain, or tighten writing without losing important detail."
---

# Simplify

Simplification means fewer moving parts, clearer names, smaller surfaces, and less surprise. Do not flatten useful domain detail just to make something shorter.

## Workflow

1. Find the real source of complexity: branching, state, naming, dependency direction, data shape, side effects, or wording.
2. Preserve public behavior unless the user explicitly wants a behavior change.
3. Prefer local improvements before broad rewrites.
4. Remove abstractions that are used once or hide simple logic.
5. Keep abstractions that encode a real invariant or prevent repeated mistakes.
6. Validate with existing tests or the smallest relevant check.

## Code heuristics

- Inline tiny wrappers when their names do not add meaning.
- Extract functions only when the extracted name explains intent or removes duplication.
- Prefer direct data flow over hidden mutation.
- Replace boolean flag combinations with explicit states when flags interact.
- Collapse branches that return the same shape.
- Push error handling close to the operation that can fail.
- Avoid clever generic helpers for one-off code.
- Keep names boring and precise.

## Writing heuristics

- Start with the point, then add context.
- Replace abstract nouns with the action they hide.
- Delete setup phrases like "it is important to note" and "in order to".
- Keep examples when they prevent ambiguity.
- Split long sentences when each part carries a separate decision.

## Output

When editing files, make the change and explain the simplification briefly. When reviewing, list the highest-impact simplifications first and mention behavior or test risks.
