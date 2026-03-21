---
name: api-design
description: Design high-leverage developer-facing APIs with strong ergonomics, composability, and long-term maintainability. Use this skill whenever the user asks to design, redesign, or review a library/module/service API, SDK surface, hooks/utilities interface, or public package contract, especially when they want "high quality", "best practice", "production grade", "like TanStack/Convex/shadcn/better-auth", or need comparison of multiple API shapes before implementation.
---

# API Design Skill

Design APIs that are hard to misuse, easy to evolve, and pleasant to adopt.

## Core Intent

Produce high-value API designs by:

1. Asking meaningful, high-signal questions.
2. Generating multiple plausible API designs.
3. Comparing tradeoffs with explicit criteria.
4. Recommending one design and migration path.
5. Grounding choices in proven patterns from top ecosystems.

## When Not to Use

Skip this skill when the user only needs:

- A tiny one-off helper function with no public API surface.
- Mechanical refactors without interface changes.
- Pure implementation debugging where API design is not in scope.

In those cases, answer directly and keep API-design overhead low.

## Design North Star

Optimize for:

- **Clarity:** Names and behavior are obvious from call sites.
- **Safety:** Invalid states are difficult or impossible.
- **Composability:** Small primitives combine into advanced use cases.
- **Progressive Power:** Great default path plus escape hatches.
- **Evolvability:** Versioning and extensions avoid future dead-ends.
- **DX Velocity:** Fast to learn, test, and debug.

## Workflow

Follow this sequence.

### 1) Frame the problem with meaningful questions

Ask 6-12 focused questions, tailored to the domain. Prioritize uncertainty that changes the API shape.

Question themes:

- Primary users and skill level (app devs, infra team, plugin authors).
- Runtime/environment constraints (browser, server, edge, mobile, SSR).
- Performance envelope (latency targets, throughput, memory, bundle size).
- Data and consistency model (sync/async, optimistic updates, transactions).
- Failure semantics (retries, partial failures, cancelation, timeouts).
- Extension model (plugins, adapters, middleware, custom transports).
- Type guarantees (schema-first, inference-first, runtime validation).
- Security boundaries (authz, tenancy, secrets, least privilege).
- Compatibility constraints (existing users, semver, migration window).
- Success criteria (adoption speed, fewer support tickets, error rate).

If context is missing, call out assumptions explicitly and continue.

### 2) Define API quality criteria

State weighted criteria before proposing designs. Use percentages that sum to 100.

Suggested criteria:

- Learnability
- Correctness by construction
- Flexibility/extensibility
- Runtime performance
- Type-level ergonomics
- Operational observability
- Migration safety

### 3) Produce 3 distinct API designs

Generate at least three genuinely different approaches (not cosmetic variants).

Candidate families to consider:

- **Fluent Builder API** (guided setup, staged configuration)
- **Functional Core API** (small pure primitives, composition-heavy)
- **Declarative Object/Schema API** (configuration-first, policy-rich)
- **Command/Client API** (imperative calls, transport-agnostic)
- **Evented/Reactive API** (streams, subscriptions, live updates)

For each design provide:

- Core surface area (key types/functions).
- 2-3 call-site examples (simple, intermediate, advanced).
- Technical pattern stack and why it fits the constraints.
- Error and cancelation model.
- Extension/plugin story.
- Backward compatibility story.

### 4) Compare with a tradeoff matrix

Use a matrix scored 1-5 against the weighted criteria, then explain the score deltas in plain language.

Also include:

- Biggest risk for each design.
- What must be true for that design to win.
- Likely failure mode in year 2.

### 5) Recommend one design

Give a clear recommendation and rationale:

- Why it wins for this context.
- Which compromises are accepted intentionally.
- How to keep escape hatches without polluting the default path.

### 6) Deliver an implementation blueprint

Include:

- Public API spec (names/signatures/contracts).
- Internal layering boundaries.
- Validation and error taxonomy.
- Test strategy (unit, contract, integration, misuse tests).
- Migration strategy and deprecation plan.
- Documentation map (quickstart, recipes, edge cases, anti-patterns).

### 7) Run final quality gates

Before final recommendation, verify the design against `references/checklists.md` and report any failed gates plus fixes.

## Reference Pack

Use references intentionally (do not dump all of them every time):

- `references/patterns.md` for reusable API patterns and anti-patterns.
- `references/technical-patterns.md` for concrete construction patterns (composition, builder, chainable/fluent APIs, plugin, strategy, middleware, command, factory).
- `references/archetypes.md` for choosing an API shape by problem type.
- `references/case-studies.md` for lessons from successful library ecosystems.
- `references/checklists.md` for final quality gates before proposing.

In each proposal, cite which reference sections informed the recommendation.

## Pattern Guidance (Inspired by top libraries)

Use these principles:

- Prefer inference and sane defaults for the common path.
- Expose primitives that compose rather than giant option bags.
- Keep side effects explicit and observable.
- Make cache/consistency semantics first-class when data is involved.
- Separate transport/auth/storage concerns from business primitives.
- Offer strong type feedback and actionable runtime errors.

## Output Format

Use this structure exactly unless the user asks otherwise.

```markdown
# API Design Proposal: <name>

## Context Snapshot
- Domain:
- Users:
- Constraints:
- Success metrics:
- Assumptions:

## Clarifying Questions
1. ...

## Quality Criteria (Weighted)
- Criterion: XX%

## Candidate Designs
### Design A - <title>
#### Surface
#### Examples
#### Technical Pattern Stack
#### Error Model
#### Extensibility
#### Compatibility
#### Pros
#### Cons

### Design B - <title>
...

### Design C - <title>
...

## Tradeoff Matrix
| Criterion | Weight | A | B | C |
|---|---:|---:|---:|---:|

## Recommendation
- Chosen design:
- Why:
- Accepted tradeoffs:
- Guardrails:

## Pattern Selection Rationale
- Primary pattern(s):
- Why these patterns fit:
- Patterns rejected and why:

## Implementation Blueprint
### Public Contracts
### Internal Architecture
### Error Taxonomy
### Test Plan
### Migration Plan
### Docs Plan

## Risks and Mitigations
- Risk:
- Mitigation:

## References Used
- <file + section and why it applies>
```

## Example Prompts and Expected Behavior

**Example 1:**
Input: "Design a TypeScript caching SDK for browser + Node with plugin support and retries."
Expected behavior: Ask focused context questions, compare at least 3 patterns (for example builder vs functional vs middleware pipeline), provide weighted matrix, choose one design, include migration and docs plan.

**Example 2:**
Input: "I need an auth API like better-auth: secure defaults, multiple providers, adapters."
Expected behavior: Emphasize security boundaries, adapter contracts, error taxonomy, and safe-by-default flows; include rejected design rationale.

**Example 3:**
Input: "Redesign my query client API to feel like TanStack and support realtime invalidation."
Expected behavior: Make cache identity and invalidation semantics explicit, compare reactive/evented vs command/client designs, and include observability/test strategy.

## Design Anti-Patterns

Avoid:

- Overloaded "god" functions with dozens of options.
- Hidden global state or magic behavior.
- Inconsistent naming for related concepts.
- Unbounded generic abstractions before concrete needs.
- Leaky internals in the public contract.
- Breaking changes without migration affordances.

## Interaction Style

- Be opinionated but transparent about tradeoffs.
- Ask fewer, better questions instead of long questionnaires.
- Prefer concrete examples over abstract doctrine.
- Name decisions and their consequences explicitly.
- If user asks for speed, produce a quick recommendation first, then expanded comparison.
