---
name: implementation
description: Use when writing, changing, or refactoring production code. Enforce the smallest general implementation that satisfies governing requirements and tests, prefers existing capabilities, keeps changes surgical, preserves required quality constraints, and stops when the task is satisfied.
---

# Implementation

Implement only the code required to satisfy the current behavior correctly.
When observable behavior or a governing requirement changes, `spec-driven-development` MUST be applied.
`test-driven-development` MUST be applied to executable behavior changes and behavior-preserving refactors.
If the relevant code boundary, dependencies, or repository behavior are not already established, `context-acquisition` MUST be applied before production edits.
If implementation creates or materially edits code comments, JSDoc, docstrings, public API comments, or test names, `technical-writing` MUST govern those artifacts.
If implementation exposes an unresolved architecturally significant choice, `architecture-decisions` MUST govern that choice before it becomes an implicit production-code decision.
`secure-coding` MUST govern every production-code change. Its universal baseline always applies; its security-impact assessment selects any additional controls and verification.

## Terms

A **smallest general implementation** is the least repository-owned logic that satisfies the current requirement for the relevant input class. It is not a test-specific shortcut.
A **surgical change** changes only the code and supporting artifacts required by the current task.
**Delegation** means using an existing language, platform, framework, dependency, generated capability, or project abstraction instead of implementing equivalent repository-owned behavior.
**Structural erosion** is cumulative growth in redundant logic or concentrated complexity that makes the affected code harder to extend correctly.

## Core Invariant

The implementation MUST be the smallest general solution that satisfies the governing requirements and required tests.
The implementation MUST NOT add code only because it might be useful later.
The implementation MUST NOT add speculative flexibility, configuration, abstractions, compatibility paths, or optimizations without a current requirement or demonstrated need.
The implementation MUST NOT hard-code a current test case instead of satisfying the required input class.

When the governing requirements are satisfied, required verification passes, and the current change contains no unnecessary code, the agent MUST stop editing.

## Preconditions

Before you change production code:

1. Identify the current required behavior.
2. Identify the verification that demonstrates success.
3. Resolve any specification or authority gap through `spec-driven-development`.
4. Satisfy the required RED gate through `test-driven-development` when behavior changes.
5. Identify the smallest code boundary that can satisfy the behavior.
6. Apply the universal `secure-coding` baseline and complete its security-impact assessment.

Production code MUST NOT be used to resolve an undefined requirement.
A behavior-changing implementation MUST NOT begin before the applicable TDD RED gate is satisfied.

## Prefer Existing Capability

Before new repository-owned logic is added, applicable existing capabilities MUST be considered.
Check capabilities in this order unless project constraints make another order more appropriate:

1. language or standard-library capability;
2. platform or runtime capability;
3. framework capability;
4. existing project abstraction or utility;
5. already-adopted dependency;
6. new repository-owned implementation.

Delegation SHOULD be preferred when an existing capability satisfies the requirement with acceptable compatibility, failure behavior, performance, security, and maintenance tradeoffs.
A parallel implementation MUST NOT be created only because the existing capability is unfamiliar.
A dependency MUST NOT be wrapped only to rename its API or hide it behind a one-use abstraction.

Material behavior or compatibility claims SHOULD be verified against authoritative documentation, source, or tests when needed.
When choosing between delegation and custom code, `references/delegation.md` SHOULD be applied.

## Simplicity

The implementation SHOULD minimize concepts, states, branches, abstractions, indirection, and repository-owned behavior before it minimizes line count.
Direct control flow SHOULD be preferred over unnecessary indirection.
One clear implementation SHOULD be preferred over multiple configurable strategies when only one strategy is required.
Data and functions SHOULD be preferred over a new object hierarchy when the hierarchy adds no required behavior.

An abstraction MUST NOT be created for one use unless it removes current complexity or establishes a required boundary.
A helper SHOULD NOT be created when it only hides a simple expression or makes behavior harder to follow.
A concrete requirement MUST NOT be generalized to hypothetical future cases.

Fewer lines MUST NOT be treated as simpler when they obscure behavior, weaken types, duplicate an existing capability, or increase conceptual complexity.
When the simplest solution is disputed or unclear, `references/minimal-implementation.md` SHOULD be applied.


## Iterative Change Discipline

A passing test suite MUST NOT justify redundant logic or avoidable complexity introduced by the current change.
Successive changes MUST NOT accumulate one-off branches, duplicated behavior, or parallel paths when the currently affected code can represent the required behavior more simply.

When a new requirement would materially increase duplication or concentrate more logic in an already-complex unit, the affected code SHOULD be restructured when all of these conditions hold:

- the restructuring is limited to the behavior affected by the current task;
- the restructuring reduces current conceptual complexity or duplication;
- observable behavior that is not changing remains preserved;
- the applicable TDD workflow verifies the restructuring.

This rule MUST NOT authorize unrelated cleanup, speculative generalization, or an implicit architectural change.
The goal is to prevent structural erosion in the code being changed, not to redesign neighboring code.

## Surgical Changes

The change MUST be limited to code and supporting artifacts required by the current requirement, verification, or necessary documentation.
Established local patterns SHOULD be followed when they satisfy the requirement.
Public behavior and compatibility MUST be preserved unless the governing requirement changes them.

Unrelated code MUST NOT be refactored during the task.
Unrelated symbols MUST NOT be renamed.
Unrelated code MUST NOT be reformatted.
A working dependency or architectural pattern MUST NOT be replaced without a current requirement or accepted design reason.

Imports, variables, branches, helpers, or other code made unused by the current change SHOULD be removed.
Unrelated pre-existing dead code MUST NOT be removed unless the task includes that cleanup.

When useful cleanup falls outside the current behavior, `references/change-scope.md` SHOULD be applied.

## Quality Constraints

The local ISO/IEC 25010- and ISO/IEC 5055-informed profile in `references/quality.md` MUST be applied when implementation choices affect quality characteristics.
Functional suitability MUST be preserved: the implementation MUST satisfy the required behavior correctly and completely for the current scope.

Other applicable quality characteristics MUST be preserved when a governing requirement, architecture, risk, or existing contract makes them relevant.
Code MUST NOT be added only to improve an unrequired quality characteristic.

Extra implementation complexity for a claimed quality improvement SHOULD require at least one current basis:

- an explicit requirement;
- an accepted architectural constraint;
- a demonstrated defect or risk;
- measured evidence;
- a compatibility or interoperability obligation.

ISO/IEC 25010 or ISO/IEC 5055 conformance MUST NOT be claimed based only on this skill.

## Performance

Non-trivial optimization machinery MUST NOT be added from intuition alone.
Explicit performance requirements and established hot-path constraints MUST be preserved.
A material bottleneck SHOULD be measured or otherwise established before complexity is added for performance.
A simpler implementation SHOULD be preferred when performance differences are immaterial to the requirement.

When an existing dependency provides a faster implementation without unacceptable project complexity or compatibility cost, delegation SHOULD be preferred.

## Error and Edge Behavior

Required failure behavior and required boundary cases MUST be implemented.
A defined failure MUST NOT be converted into silent success by an invented fallback.
Handling for states made impossible by authoritative invariants SHOULD NOT be added unless safety, security, reliability, or another governing requirement justifies defense in depth.
Validation, authorization, type guarantees, and trust boundaries MUST NOT be weakened to simplify implementation or make a test pass.

## Comments and Documentation

A comment MAY be added when code cannot clearly express an important invariant, constraint, boundary, or rationale.
Comments MUST NOT narrate obvious code or justify unnecessary complexity.
Documentation MUST be updated when this implementation changes behavior or information that the documentation owns.

## Deviations

If the smallest correct implementation conflicts with a higher-authority architecture, compatibility, security, or quality constraint, the higher-authority constraint MUST be followed.
A material complexity tradeoff SHOULD be reported when that constraint requires a larger implementation.

If a simpler solution requires a durable architectural change, that change MUST NOT be made implicitly.
The `architecture-decisions` skill MUST govern the unresolved significant choice before implementation continues.

If a requirement cannot be satisfied without unresolved speculative scope, behavior MUST NOT be invented.
The unresolved requirement or constraint MUST be reported.

## Completion

Before substantial implementation work is reported complete, `references/review-checklist.md` MUST be applied.
When the governing requirements are satisfied, required verification passes, and the current change contains no unnecessary code, the agent MUST stop changing the repository.

## References

- `references/minimal-implementation.md` — minimum sufficient code and anti-overengineering rules.
- `references/delegation.md` — existing-capability and dependency decisions.
- `references/change-scope.md` — surgical changes and cleanup boundaries.
- `references/quality.md` — ISO/IEC 25010 and ISO/IEC 5055-informed quality profile.
- `references/review-checklist.md` — implementation completion review.
- `references/sources.md` — provenance, versions, and house-policy boundaries.
