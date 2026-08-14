---
name: spec-driven-development
description: Use for new or changed observable behavior, requirements-to-code work, conformance implementation, specification changes, or conflicts between specifications, tests, and code. Enforce authoritative requirements, requirements-engineering gates before code, traceability, conformance verification, and handoff to test-driven-development.
---

# Spec-Driven Development

Develop observable behavior from authoritative, validated, verifiable specifications.
When specification prose is created or changed, the `technical-writing` skill MUST be applied.
Before executable behavior is implemented, the `test-driven-development` skill MUST be applied.
When specification work exposes an unresolved architecturally significant choice, `architecture-decisions` MUST govern that choice without replacing the specification's authority over normative behavior.

## Terms

A **governing specification** is the highest-authority normative artifact that defines the behavior for the current work.
A **traceability chain** connects a requirement or normative contract to its test, implementation, and verification result.
**Requirement verification** checks whether a requirement is well-formed enough to implement and verify.
**Requirement validation** checks whether the requirement represents the intended need or behavior.

## Core Invariant

Before observable behavior changes, the governing requirement or normative machine-readable contract MUST be identified.
Its authority and intended behavior MUST be resolved before production code changes.

If required behavior is absent, ambiguous, contradictory, or invalidated by higher authority, the governing specification MUST be resolved before implementation.
An existing requirement MUST NOT be rewritten only to describe an implementation when it already defines the intended behavior.
A specification MUST NOT be changed merely to make existing code or tests appear conformant.

## Authority

The project's defined artifact precedence MUST be used when it exists.
If the project does not define precedence, this order SHOULD be used for behavior:

1. governing external standards and protocols;
2. project normative specifications and declared normative machine-readable contracts;
3. public schemas and API contracts;
4. accepted design decisions that project governance authorizes to define behavior;
5. tests and conformance cases that are not themselves declared normative;
6. existing implementation;
7. examples and tutorials.

A current task MAY authorize a specification change when higher-authority project, contractual, or regulatory constraints permit it.
That authorization MUST NOT make stale implementation behavior authoritative.
If authoritative artifacts conflict, the conflict MUST be reported and resolved before implementation.
The artifact that is easiest to change MUST NOT be selected silently as the authority.

When artifact authority is unclear, `references/authority.md` MUST be applied.

## Requirements-Engineering Profile

Before normative behavior is added or materially changed, `references/requirements-engineering.md` MUST be applied.
This local profile is primarily informed by ISO/IEC/IEEE 29148:2018, with supporting lifecycle context from ISO/IEC/IEEE 12207:2026.
ISO/IEC/IEEE 15289:2019 SHOULD apply only when the project requires formal lifecycle information-item structure.

A standard name MUST NOT substitute for requirements-engineering work.
Full lifecycle or documentation ceremony MUST NOT be imposed when the project does not require it.
Formal conformance with these standards MUST NOT be claimed based only on this skill.

Before implementation, each new or materially changed requirement MUST pass these applicable gates:

1. **Authority:** identify the source that is allowed to define or change the behavior.
2. **Validation:** confirm that the requirement represents the intended need from the available authority.
3. **Quality:** confirm that the requirement is singular, unambiguous, complete enough, feasible or explicitly unresolved, verifiable, consistent, traceable, and implementation-independent by default.
4. **Assumptions:** resolve or record assumptions that materially affect behavior.
5. **Impact:** identify affected contracts, compatibility commitments, tests, implementation, documentation, migration, security, and quality requirements when applicable.

If a material gate fails, a resolution MUST NOT be invented.
The requirement MUST be resolved through the proper authority before that behavior is implemented.

## Workflow

For each observable behavior change:

1. Identify the governing requirement or normative contract.
2. Apply the requirements-engineering gates.
3. Update or clarify the governing specification first when required.
4. Select one small required behavior for implementation.
5. Apply `test-driven-development` to that behavior.
6. Verify the implemented behavior against the governing requirement and applicable conformance cases.
7. Complete the traceability chain.
8. Repeat for the next required behavior.

Production implementation MUST NOT begin while the behavior remains undefined or conflicted.
Speculative implementation MUST NOT be batched ahead of unresolved requirements.

## Specification Changes

A specification edit MUST be classified before it is made:

- **Requirement change:** changes required observable behavior or conformance.
- **Clarification:** removes ambiguity without intentionally changing required behavior.
- **Editorial change:** changes presentation without changing normative meaning.

A requirement change MUST receive change-impact analysis before implementation.
Affected tests and implementation MUST be updated through the normal workflow.
A clarification MUST be checked against existing tests and implementation for agreement with the clarified meaning.
An editorial change MUST NOT manufacture implementation work.

If implementation reveals a specification gap, implementation of that behavior MUST stop until the gap is resolved.
For specification-change edge cases, `references/specification-changes.md` SHOULD be applied.

## Traceability

Each durable behavior change MUST be traceable through:

1. a stable requirement reference or normative machine-readable contract;
2. an acceptance, conformance, regression, compile-time, or other behavior test;
3. the implementation that satisfies the behavior;
4. the verification result.

The narrowest durable requirement reference that the project provides SHOULD be used.
Normative requirement text MUST NOT be copied into source comments merely to create traceability.
Comments and implementation details MUST NOT substitute for a governing requirement.

When the project has multiple specifications, generated contracts, or portable conformance fixtures, `references/traceability.md` SHOULD be applied.

## Tests and Conformance

Tests MUST operationalize requirements.
Tests MUST NOT replace a governing specification unless the project explicitly declares a machine-readable test or contract normative.

When a machine-readable conformance schema exists, typed conformance fixtures SHOULD be preferred for valid conformance behavior.
Raw malformed fixtures MAY be used when malformed encoding is itself the behavior under test.
Conformance cases MUST focus on observable requirements rather than incidental implementation structure.

Test design and RED-GREEN-REFACTOR execution MUST be delegated to `test-driven-development`.
This skill MUST NOT duplicate the TDD workflow.
For substantial conformance-suite work, `references/conformance.md` SHOULD be applied.


## Executable Constraints

A durable behavioral or architectural constraint SHOULD have executable verification when a reliable machine-checkable representation exists and the maintenance cost is proportionate to the risk.
The executable check MUST trace to the governing requirement, contract, or accepted architecture decision that gives the constraint authority.
An executable check MUST NOT silently become normative authority only because it is machine-readable.

A machine-checkable form SHOULD NOT be created when it would encode an approximation that is less reliable than the governing requirement or would add disproportionate maintenance cost.
Executable constraints complement normative specifications; they do not replace the authority model in this skill.

See `references/conformance.md` for machine-readable conformance guidance and `references/sources.md` for the emerging agent evidence that motivates continuous executable checks in long-horizon work.

## Scope Boundaries

A pure behavior-preserving refactor MUST NOT require a specification change.
An internal implementation choice MUST NOT become normative merely because the implementation uses it.
An implementation detail SHOULD become normative only when interoperability, compatibility, security, a required quality attribute, or another governing constraint depends on it.
An accepted architecture decision MUST NOT substitute for a specification when the decision changes normative behavior; the governing specification or contract MUST be updated through this workflow.

Exploration MAY inform a future requirement.
Exploratory behavior MUST NOT ship as the final implementation until the governing behavior is defined and verified through the normal workflow.

Generated artifacts MUST NOT become the edit authority when a maintained source artifact generates them.
The authoritative source MUST be changed and regenerated according to the project workflow.
Before specification work is added to a mechanical or internal-only change, `references/scope-boundaries.md` SHOULD be applied.

## Deviations

Spec-driven development MUST NOT be claimed when observable behavior was implemented before its governing behavior was resolved.
If a higher-authority constraint requires a different order, that constraint MUST be followed and the deviation MUST be reported.
If accidental implementation precedes the specification, the specification MUST NOT be retroactively rewritten only to justify the code.
The intended behavior MUST be resolved from the proper authority before specifications, tests, and implementation are brought into agreement.

## Completion

Before substantial spec-driven work is reported complete, `references/review-checklist.md` MUST be applied.
The governing behavior MUST be authoritative and sufficiently defined; required specification changes MUST precede implementation; durable behavior changes MUST have a complete traceability chain; unresolved conflicts or conformance gaps MUST be reported.

## References

- `references/requirements-engineering.md` — ISO/IEC/IEEE 29148-informed operational requirements profile and change-impact analysis.
- `references/authority.md` — artifact authority and conflict handling.
- `references/specification-changes.md` — requirement changes, clarifications, and editorial changes.
- `references/traceability.md` — requirement-to-verification traceability.
- `references/conformance.md` — conformance suites and machine-readable contracts.
- `references/scope-boundaries.md` — refactors, implementation details, exploration, and generated artifacts.
- `references/review-checklist.md` — completion review.
- `references/sources.md` — standards provenance and scope.
