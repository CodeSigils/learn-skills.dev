---
name: architecture-decisions
description: Use when a task introduces, changes, reviews, or discovers a durable design choice that can materially constrain system structure, dependencies, interfaces, data, deployment, trust boundaries, or quality attributes, or when deciding whether an ADR, RFC, design proposal, architecture description, or executable architecture constraint is justified. Enforce significance-based decision governance, real alternative evaluation, durable rationale when justified, and clean handoff to specifications and implementation without prescribing artifact locations.
---

# Architecture Decisions

Make architecturally significant choices deliberately and preserve their rationale when future work can depend on it.
When this workflow creates or materially edits an architecture or decision artifact, `technical-writing` MUST govern that artifact.
If existing requirements, decisions, dependencies, or constraints are not already sufficiently established, `context-acquisition` MUST govern their discovery.
If a decision changes or conflicts with normative behavior, `spec-driven-development` MUST govern that behavior and authority.
When the resolved decision leads to production-code changes, `implementation` MUST govern those changes.

## Terms

An **architecturally significant decision** is a design choice that materially constrains future system structure, interfaces, dependencies, data, deployment, trust boundaries, construction techniques, or required quality characteristics.
A **decision record** is a durable artifact that preserves a significant decision, its context, rationale, and consequences. An architecture decision record (ADR) is one common form.
A **proposal artifact** is an artifact such as an RFC or design proposal used to evaluate an unresolved significant choice before commitment.
An **architecture description** represents architectural structure, relationships, concerns, or views for communication or evaluation.
An **executable architecture constraint** is a machine-checkable rule that verifies a durable architectural restriction.

## Core Invariant

An architecturally significant decision MUST be deliberate, consistent with governing constraints, and supported by enough evidence to explain why the selected option is appropriate.
A significant decision MUST be durably recorded when future work can reasonably depend on its rationale, tradeoffs, or consequences.
A local, reversible implementation choice MUST NOT be turned into architecture ceremony only because an artifact could be written about it.

The existence of an ADR, RFC, specification, diagram, or other artifact MUST be justified by the role it serves.
This skill MUST NOT prescribe a repository path, directory, filename scheme, numbering scheme, document system, or storage medium for architecture artifacts.
Existing project conventions for architecture artifacts MUST be followed when they exist.
A new repository-wide artifact-location convention MUST NOT be invented solely to satisfy this skill.

## Resolve Existing Authority First

Before you create a new architectural decision:

1. Identify the governing requirement, contract, or constraint.
2. Locate existing accepted architecture decisions or descriptions that materially govern the choice.
3. Determine whether the choice is already resolved.
4. Determine whether the current task authorizes reconsideration when an accepted decision exists.

An existing accepted decision MUST be followed when it remains authoritative and the current task does not authorize reconsideration.
Existing implementation MAY provide evidence about current architecture, but implementation MUST NOT silently override a governing specification or accepted decision.
A new decision record MUST NOT duplicate an existing decision merely to restate it.

If governing artifacts conflict, the conflict MUST be resolved through the applicable authority process before implementation.

## Significance Gate

Before architecture ceremony is introduced, determine whether a meaningful unresolved choice exists.
A choice SHOULD be treated as architecturally significant when it can materially affect one or more of these areas:

- public or cross-component interfaces;
- persistent data, storage, migration, or serialization strategy;
- trust, authorization, or security boundaries;
- deployment, runtime, communication, or operational topology;
- major framework, platform, runtime, or dependency commitments;
- component ownership or dependency direction;
- compatibility or interoperability strategy;
- required quality characteristics beyond one local unit;
- a precedent future changes are likely to reuse;
- a choice that is costly, risky, or migration-heavy to reverse.

Code size MUST NOT determine architectural significance by itself.
A choice that is local, easily reversible, already dictated by higher authority, and unlikely to constrain future work SHOULD remain an implementation decision.
Apply `references/decision-threshold.md` when significance is unclear.

## Artifact Roles

Artifact role MUST be selected from the decision need, not from a requirement to produce a particular document type.

- A **specification** defines normative behavior or contracts. A decision record MUST NOT substitute for it.
- A **proposal artifact** supports evaluation, review, or agreement before commitment. It SHOULD be used when pre-commitment stakeholder coordination is material.
- A **decision record** preserves a significant selected decision and rationale that future work may need.
- An **architecture description** communicates structure or relationships when existing artifacts are insufficient.
- An **executable architecture constraint** verifies a durable restriction when a reliable, proportionate machine-checkable form exists.

A project artifact MAY satisfy more than one role when those roles remain clear.
Duplicate artifacts MUST NOT be created only to satisfy labels such as `RFC`, `ADR`, or `spec`.
An accepted RFC or equivalent MAY serve as the durable decision record when project convention gives it that role and its rationale remains discoverable.
Apply `references/artifact-roles.md` when the appropriate artifact is unclear.

## Evaluate a Significant Choice

For each unresolved significant decision:

1. State the decision question.
2. Identify the governing requirements and hard constraints.
3. Identify material stakeholders or concerns when they affect the decision.
4. Identify viable, materially distinct alternatives.
5. Eliminate alternatives that violate hard constraints.
6. Compare the remaining alternatives against material decision drivers.
7. Select the option whose tradeoffs best satisfy the governing constraints and current needs.
8. Record the decision when the decision-record gate is satisfied.
9. Update normative specifications through `spec-driven-development` when required behavior changes.
10. Add executable verification when a durable architecture constraint has a reliable, proportionate check.

Alternatives MUST be plausible enough to choose if their tradeoffs prove preferable.
Strawman alternatives MUST NOT be created only to make a preferred option look justified.
The status quo SHOULD be considered when it remains viable.
Hard constraints MUST be distinguished from preferences.
Decision rationale MUST identify the material tradeoffs that caused the selected option to win.
A decision MUST NOT be justified only with vague labels such as `cleaner`, `best practice`, `more scalable`, or `more flexible` without a current decision driver or evidence.
Apply `references/decision-evaluation.md` for detailed evaluation guidance.

## Uncertainty and Reversibility

Material uncertainty MUST be stated rather than converted into false confidence.
A high-impact or difficult-to-reverse decision MUST NOT be silently selected when material uncertainty prevents credible evaluation.

A provisional decision MAY be used when progress is necessary and the decision remains within governing constraints, material uncertainty is explicit, consequences are bounded or reversible, controlling assumptions are recorded, and a practical reassessment trigger is identified when one exists.
A reversible decision SHOULD receive less process than an equally uncertain irreversible decision.

## Decision Record Gate

A significant selected decision MUST have a durable decision record when future implementation is expected to depend on its rationale, it establishes a precedent, viable alternatives had materially different long-term consequences, reversal would impose material cost, it responds to a non-obvious important constraint, or code alone would make the choice easy to misinterpret.

The record SHOULD preserve the decision context, selected decision, material constraints, rationale, important alternatives, consequences, and lifecycle information when the project uses it.
The record MUST be concise enough to remain useful.
It MUST NOT duplicate obvious implementation detail unless that detail is part of the architectural constraint or rationale.

## Architecture Descriptions and Executable Constraints

An architecture description SHOULD be created or updated only when structure, relationships, or concerns cannot be evaluated or communicated efficiently from existing artifacts.
A diagram or model MUST NOT be created only because the decision is architectural.

A durable architectural constraint SHOULD have executable verification when silent drift would be material, a reliable machine-checkable representation exists, the check does not freeze incidental implementation detail, and maintenance cost is proportionate to risk.
The executable check MUST trace to the requirement, accepted decision, or other authority that gives the constraint force.
A machine-checkable rule MUST NOT become authoritative merely because it is executable.
Apply `references/executable-constraints.md` when an architectural rule can be checked automatically.

## Decision Lifecycle

A decision record is historical context, not an immutable command.
When an implemented significant decision is materially reversed or replaced, the new decision SHOULD supersede the old decision rather than erase the original rationale.
A clarification or newly discovered consequence MAY update an existing record when the selected decision does not materially change and project convention permits the update.
The agent MUST NOT retroactively document every historical architecture choice merely because this skill is active.
If implementation reveals that an accepted decision is invalid or incomplete, the decision MUST be revisited before implementation silently diverges from it.

## Scope Boundaries

An initial implementation does not require a new decision record when governing artifacts already resolve the significant architecture choices.
If implementation introduces a significant unresolved choice, this skill MUST be applied even during initial implementation.
A routine refactor, helper extraction, private naming choice, formatting choice, or other local reversible decision SHOULD NOT create an ADR or RFC.
A dependency choice SHOULD be treated as architecturally significant only when it creates a material long-term commitment, boundary, compatibility obligation, or operational consequence.
A decision record MUST NOT make an implementation detail normative by itself.
Normative behavior changes MUST be handled through `spec-driven-development`.

## Deviations

A higher-authority requirement, project convention, regulatory rule, or explicit user instruction MUST take precedence over this skill.
If the decision-record gate requires a durable artifact but the task or environment does not permit its creation, the agent MUST report the missing record.
The rationale MUST NOT be left only as an implicit consequence of the code.
If no artifact-location convention is established, this skill MUST NOT invent one as architecture policy.
Artifact placement MUST be determined by the owning project or task context.

## Completion

Before substantial architecture-decision work is reported complete, `references/review-checklist.md` MUST be applied.
An unmet MUST-level decision, authority, artifact, or handoff rule MUST block completion or be reported as an explicit unresolved constraint.

## References

- `references/decision-threshold.md` — significance and decision-record gates.
- `references/artifact-roles.md` — specifications, proposals/RFCs, decision records/ADRs, and architecture descriptions.
- `references/decision-evaluation.md` — constraints, alternatives, tradeoffs, uncertainty, and reversibility.
- `references/executable-constraints.md` — machine-checkable architectural restrictions.
- `references/review-checklist.md` — completion review.
- `references/sources.md` — standards, practitioner guidance, research evidence, and house-policy boundaries.
