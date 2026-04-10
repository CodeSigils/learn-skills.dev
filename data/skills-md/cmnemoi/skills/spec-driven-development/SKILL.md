---
name: spec-driven-development
description: Proactively apply when defining feature behavior before implementation, keeping specs aligned with tests and code, or introducing lightweight spec workflows. Triggers on spec-driven development, SDD, spec-first, acceptance criteria, spec -> tests -> code, @spec, behavioral traceability, feature spec, bugfix spec, design-first spec. Use when building or changing production features, clarifying expected behavior, or reducing drift between intent and implementation. Pragmatic Spec-Driven Development centered on a lightweight spec-test-code triangle.
---

# Spec-Driven Development

> Core idea: write a **short, testable, repo-anchored spec**, then use it as the pivot between **tests** and **code**.
>
> Recommended model: not `spec -> code`, but a **triangle**: `spec <-> tests <-> code`.

---

## When to Use / Skip

| Use When | Skip When |
|----------|-----------|
| Behavior is important and should remain understandable after delivery | Throwaway demo, spike, or one-shot script |
| A feature needs clear acceptance criteria before coding | Small exploratory change where the shape is still unknown |
| You want durable intent, not a chat prompt that disappears | Hotfix requiring immediate manual intervention |
| Multiple people or agents will touch the feature over time | Very small local refactor with no behavior change |
| The cost of drift or regression is significant | The process cost would exceed the protection gained |

Rule of thumb: use SDD for **durable production behavior**, not for disposable exploration.

---

## Quick Decision Trees

### "Should I use SDD here?"

```
What kind of work is this?
├─ New or changed production behavior              → Yes, use SDD
├─ Bugfix with regression risk                     → Yes, use bugfix spec
├─ Architecture already decided, behavior to pin   → Yes, use design-first spec
├─ Pure refactor, no behavior change               → Usually no
└─ Prototype / spike / throwaway demo              → No, skip formal SDD
```

### "Which spec type should I write?"

```
What are you trying to control?
├─ New feature or extension                        → Feature spec
├─ Existing design is already chosen               → Design-first spec
├─ Fix one bug without widening scope              → Bugfix spec
└─ Large unknown area                              → Investigate first, then spec
```

### "How much documentation do I need?"

```
How complex is the change?
├─ Small/medium feature                            → One spec file
├─ Complex multi-step delivery                     → Spec + small local plan
├─ External contract matters                       → Spec + separate API contract
└─ Tiny isolated fix                               → Short bugfix spec only
```

### "When is a behavior really implemented?"

```
Is the behavior triangulated?
├─ Exists in spec only                             → Not implemented yet
├─ Spec + tests, no code reference                 → Fragile / incomplete
├─ Spec + code, no test                            → Unverified
└─ Spec + test + code all linked                   → Properly implemented
```

---

## Recommended Workflow

Use the lightest workflow that still preserves intent.

1. Write or update the spec.
2. Write tests linked to the spec.
3. Implement code linked to the spec.
4. Revise the spec if tests or implementation reveal a missing rule.
5. Review alignment before merge.

Two human checkpoints matter more than extra documents:

1. Before implementation: confirm the spec and acceptance criteria are sufficient.
2. Before merge: confirm spec, tests, and code still say the same thing.

---

## The Spec-Test-Code Triangle

```text
        spec
       /    \
      /      \
   tests ---- code
```

- **Spec** states intent and observable behavior.
- **Tests** prove the intended behavior.
- **Code** implements the behavior.

This is safer than test/code alone:

- tests can validate the wrong thing
- code can pass tests while missing business intent
- specs can become vague if never connected to execution

Treat drift anywhere in the triangle as a problem to reconcile.

---

## What a Good Spec Contains

Keep specs short, behavioral, and testable.

### Minimum structure

1. **Why**: what problem this change solves
2. **Scope**: what the spec covers
3. **Rules**: the important behaviors or invariants
4. **Acceptance criteria**: concrete, testable examples
5. **Out of scope**: what is intentionally excluded

### Quality checks

For each important rule, ask:

- Can a test be written against it?
- Can a human understand it without reverse engineering the code?
- Can an agent use it to produce or modify code?
- Is it describing observable behavior rather than internal mechanics?

### Avoid

- file-by-file structure
- speculative implementation details
- pseudo-code too early
- long lists of nice-to-have ideas
- multi-document process by default

---

## Traceability with Stable IDs

The most useful SDD habit is explicit linking inside the repo.

Assign each behavior a stable ID following the format: `(bounded-context).subdomain.feature::business-rule`

Examples:

- `checkout.pricing.applies-member-discount::member-discount-applied`
- `search.product.find-by-query::partial-matches-allowed`
- `auth.session.security::expires-after-inactivity`

Then link that ID in:

1. the spec
2. at least one test
3. at least one implementation location

### Spec example

```md
### Member discount is applied

`{#checkout.pricing.applies-member-discount::member-discount-applied}`

When a signed-in member confirms checkout, the final total includes the member discount.
```

### Test example

```ts
/** @spec checkout.pricing.applies-member-discount::member-discount-applied */
it("applies the member discount at checkout", () => {
  // ...
});
```

### Code example

```ts
/** @spec checkout.pricing.applies-member-discount::member-discount-applied */
function computeCheckoutTotal(input: CheckoutInput): Money {
  // ...
}
```

Coverage rule: a behavior is only solid when the repo contains the full triangle.

---

## Acceptance Criteria

Acceptance criteria are the operational heart of the spec.

- Prefer business language over UI or transport details.
- Prefer bullets by default; promote only risky or ambiguous cases to heavier scenarios.
- Write them in a form that can be converted almost directly into tests.

```md
## Acceptance criteria

- Given a signed-in member with eligible items, when checkout is confirmed, then the final total reflects the member discount.
- Given a guest with the same items, when checkout is confirmed, then the final total remains unchanged.
```

Good criteria talk about domain truth, not mechanics like clicking buttons or posting to endpoints.

---

## Spec Variants

### Feature Spec

Use for new behavior or an extension of existing behavior.

Include:

- intent
- scope
- behavioral rules
- acceptance criteria
- out of scope

### Design-First Spec

Use when architecture or technical constraints are already known and the main job is to define the behavior that design must support.

Include:

- required constraints that are externally relevant
- the behavior the chosen design must preserve
- acceptance criteria validating that behavior

Do not turn the spec into an implementation narrative.

### Bugfix Spec

Use when fixing a bug without allowing scope drift.

Minimum structure:

```md
## Current behavior

What happens today and why it is wrong.

## Expected behavior

What must happen after the fix.

## Unchanged behavior

What must remain untouched.
```

This format prevents the agent from "fixing" more than intended.

---

## File and Granularity Rules

Default to one spec file per coherent feature or sub-feature:

- `docs/specs/<feature>.md`

Only add more artifacts when there is a real reason:

- a small local plan for genuinely multi-step work
- a research note worth preserving
- a separate API contract when the interface itself matters

Do not create a PRD, design doc, task list, data model, and quickstart by default for a feature that fits in one short spec.

The right amount of process reduces cognitive load. It does not move the work from code to markdown.

---

## Implementation Pattern

Use this execution order unless there is a strong reason not to:

1. Spec first
2. Tests second
3. Code third

When updating an existing system:

1. extract or repair the relevant spec
2. write or update tests against that spec
3. change the implementation
4. reconcile any newly discovered rule back into the spec

This is still pragmatic SDD. It does not require code generation or spec-as-source dogma.

---

## Examples

### Minimal spec template

```md
# Checkout Discount

## Why

Members should automatically receive their negotiated discount at checkout.

## Scope

This spec covers discount application in the final checkout total.

## Rules

### Member discount is applied

`{#checkout.pricing.applies-member-discount::member-discount-applied}`

When a signed-in member confirms checkout, the final total includes the member discount.

### Guest users do not receive the discount

`{#checkout.pricing.applies-member-discount::guest-no-discount}`

When a guest confirms checkout, no member discount is applied.

## Acceptance criteria

- Given a signed-in member with eligible items, when checkout is confirmed, then the final total reflects the member discount.
- Given a guest with the same items, when checkout is confirmed, then the final total remains unchanged.

## Out of scope

- Coupon stacking
- Loyalty points
```

### Good vs bad spec language

```md
<!-- ❌ Too technical -->
- Click the green checkout button and call POST /v1/cart/apply.

<!-- ✅ Behavioral -->
- Apply the member discount to the final checkout total.
```

```ts
// ❌ Test not linked to intent
it("applies discount", () => {
  // ...
});

// ✅ Test linked to the spec
/** @spec checkout.pricing.applies-member-discount::member-discount-applied */
it("applies the member discount at checkout", () => {
  // ...
});
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Better Approach |
|--------------|---------|-----------------|
| Specfall | Over-detailed specs create process paralysis | Keep micro-specs focused on behavior |
| Specification theater | Specs exist but are not reconciled with code | Review alignment before merge |
| Phantom completions | Tasks marked done without real implementation | Require spec/test/code evidence |
| Spec as prompt dump | Unstructured and non-maintainable | Use IDs, rules, and acceptance criteria |
| Too many files | Review overhead exceeds value | Start with one spec file |
| Spec too technical too early | Mixes intent with implementation | Keep the spec behavioral |
| Swarm of sub-agents | Coordination costs more than it helps | Keep one main agent and a short workflow |
| Tests/code without `@spec` links | Weak traceability | Add explicit stable references |

Practical heuristic: if a spec generates more than about 10 tasks for less than 3 days of work, it is probably too granular.

---

## How This Works with ATDD

This skill pairs naturally with `dsl-driven-testing`.

- The spec defines the behavior and acceptance criteria.
- Acceptance tests should speak domain language.
- Technical details belong in adapters, drivers, or helper layers, not in the spec itself.

Pipeline:

```text
spec -> acceptance criteria -> executable tests -> code
```

If you need help designing acceptance tests that stay stable across in-memory, API, and UI execution levels, load `dsl-driven-testing` alongside this skill.

---

## Review Checklist

Before considering the work complete, verify:

- the spec is short, readable, and stored in the repo
- important behaviors have stable IDs
- acceptance criteria are testable and written in business language
- tests reference the relevant `@spec` IDs
- implementation references the relevant `@spec` IDs
- spec, tests, and code do not contradict each other
- the workflow stayed proportionate to the problem size

---

## Sources

### Primary sources
- [Martin Fowler - Understanding Spec-Driven Development: Kiro, spec-kit, and Tessl](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)
- [Thoughtworks Technology Radar - Spec-driven development](https://www.thoughtworks.com/radar/techniques/spec-driven-development)
- [GitHub spec-kit - spec-driven.md](https://github.com/github/spec-kit/blob/main/spec-driven.md)
- [GitHub Blog - Spec-driven development with AI: Get started with a new open source toolkit](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
- [Kiro - New spec types: fix bugs and build on top of existing apps](https://kiro.dev/blog/specs-bugfix-and-design-first/)
- [couzic/ts-graph-mcp - specs/CLAUDE.md](https://github.com/couzic/ts-graph-mcp/blob/master/specs/CLAUDE.md)

### Academic and research references
- [Constitutional Spec-Driven Development: Enforcing Security by Construction in AI-Assisted Code Generation](https://arxiv.org/abs/2602.02584)
- [Spec-Driven Development: From Code to Contract in the Age of AI Coding Assistants](https://arxiv.org/abs/2602.00180)
- [VibeContract: The Missing Quality Assurance Piece in Vibe Coding](https://arxiv.org/abs/2603.15691)
- [Spec Kit Agents: Context-Grounded Agentic Workflows](https://arxiv.org/abs/2604.05278)

### Related practices
- [Dan North - Introducing BDD](https://dannorth.net/blog/introducing-bdd/)
- [Martin Fowler - Specification by Example](https://martinfowler.com/bliki/SpecificationByExample.html)
