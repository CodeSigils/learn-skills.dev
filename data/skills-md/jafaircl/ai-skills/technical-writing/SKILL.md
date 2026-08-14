---
name: technical-writing
description: Apply technical writing standards when creating or reviewing specifications, requirements, documentation, comments, test names, agent instructions, or technical identifiers. Enforce clear controlled prose, deliberate BCP 14 requirement levels, precise naming, evidence discipline, and execution-focused skill instructions.
---

# Technical Writing

Write technical text that is clear, consistent, testable, and traceable to evidence.
This style MUST NOT be forced onto creative, marketing, legal, or casual prose unless the user requests it.

## Workflow

Before you write or review technical text:

1. Classify the text as procedural, descriptive, or mixed.
2. Identify normative statements.
3. Identify names that the task creates or changes.
4. Identify material claims that require evidence.
5. Apply the relevant operational profiles and precedence.
6. Review the result before delivery.

## Precedence

When rules conflict:

1. Follow explicit user, project, regulatory, and governing specification requirements.
2. Preserve language syntax, protocol tokens, and established ecosystem conventions.
3. Use BCP 14 for intentional normative requirement levels.
4. Use AIP-190 and AIP-140 for naming semantics when no stronger naming rule applies.
5. Use ASD-STE100 for technical prose and terminology discipline.
6. Apply the evidence policy to externally verifiable claims.

BCP 14 MUST take precedence over conflicting STE vocabulary rules for normative keywords.
Intentional `SHOULD`, `SHOULD NOT`, and `MAY` requirement levels MUST NOT be rewritten as stronger or weaker language only to satisfy a prose rule.
Formal standards compliance MUST NOT be claimed unless the complete applicable standard can be verified.

## Operational Profiles

A standard name MUST NOT substitute for executable guidance.
When a standard materially controls a skill or artifact, the applicable local profile MUST translate the relevant subset into operational rules.
The source standard SHOULD be consulted when formal conformance, an uncovered case, or an exact definition requires it.

- Technical prose: `references/ste.md`.
- Normative requirements: `references/requirements.md`.
- Technical names: `references/naming.md`.
- External claims and citations: `references/evidence.md`.
- Agent skills and reusable instructions: `references/skill-writing.md`.

An exact standard rule MUST NOT be invented when it cannot be verified.
A local adaptation MUST be identified as house guidance rather than as a requirement of the source standard.

## Prose

Technical prose MUST apply `references/ste.md`.

- Technical prose MUST use American English unless a governing rule requires another form.
- One term MUST identify one concept.
- Different concepts MUST use different terms when confusion is possible.
- Synonyms MUST NOT rotate only for style.
- Sentences SHOULD be short, direct, and complete.
- Active voice SHOULD be used when the actor is known and relevant.
- A condition MUST appear before the dependent action when order affects interpretation.
- An instruction SHOULD contain one action when practical.
- A descriptive paragraph SHOULD keep one main topic.
- Slang, idioms, decorative language, and unnecessary qualifiers SHOULD be avoided.
- Established technical nouns and verbs MUST be preserved when they identify defined concepts.

In strict STE mode, the sentence limits and vocabulary checks in `references/ste.md` MUST apply.

## Normative Language

BCP 14 MUST be used when a normative statement needs to distinguish obligation, prohibition, recommendation, or permission.
`MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT`, and `MAY` SHOULD be preferred over synonymous BCP 14 alternatives when they state the requirement more simply.
Only uppercase BCP 14 keywords have normative meaning in this profile.

- `MUST` identifies a mandatory requirement.
- `MUST NOT` identifies a mandatory prohibition.
- `SHOULD` identifies a recommendation with legitimate exceptions.
- `SHOULD NOT` identifies a discouraged behavior with legitimate exceptions.
- `MAY` identifies permitted or optional behavior.

`SHOULD` MUST NOT express uncertainty.
`MAY` MUST NOT describe possibility.
Descriptive test names MUST NOT copy BCP 14 keywords merely because the governing requirement uses them.

For substantial requirements work, apply `references/requirements.md`.

## BCP 14 in Agent Skills

Normative skill policy MUST use BCP 14 when requirement strength matters.
Core invariants, high-risk gates, prohibitions, permissions, exception policies, and precedence rules MUST use an explicit BCP 14 requirement level when a weaker or stronger interpretation could change execution.

Procedural workflow steps MAY use direct imperative language when every step is required and an explicit requirement level adds no information.
Imperative wording MUST NOT erase a meaningful distinction between mandatory, recommended, discouraged, and optional behavior.
A dependent skill MUST NOT replace an intentional `SHOULD` or `MAY` with an undifferentiated imperative.

Example:

- Policy: `A production behavior change MUST NOT precede valid RED.`
- Procedure: `Run the focused test.`
- Recommendation: `The test SHOULD use the narrowest stable seam that proves the behavior.`

## Naming

When the task creates, reviews, or changes technical names, `references/naming.md` MUST be applied.

- Established project and domain terminology MUST be preferred.
- The same concept MUST use the same name.
- Different concepts MUST use different names when confusion is possible.
- Specific names SHOULD be preferred over ambiguous general names.
- Words that add no meaning SHOULD be removed.
- Target-language casing and syntax conventions MUST be preserved.
- AIP-190 and AIP-140 semantic guidance SHOULD apply when no stronger rule exists.
- The AIP-140 field profile SHOULD apply to protobuf fields when no stronger rule exists.

An existing public identifier MUST NOT be silently renamed during a prose-only task.

## Evidence

When material claims depend on external facts, `references/evidence.md` MUST be applied.
Governing and primary sources SHOULD be preferred over secondary sources.
The highest-authority source that directly supports the claim SHOULD be used.
A source MUST be inspected before it is cited.
Citations, rule numbers, quotations, benchmarks, versions, and source locations MUST NOT be invented.
An inference MUST be labeled when the source supports only its premises.
Version-sensitive claims SHOULD be anchored when the version can affect the decision.
Meaningful disagreement between authoritative sources MUST be reported.
A material claim that cannot be verified MUST be qualified or omitted.

## Technical Literals

During prose-only work, code, identifiers, commands, paths, protocol tokens, quoted errors, URLs, and externally defined names MUST be preserved exactly.
An identifier SHOULD be reviewed only when the task includes naming or renaming.

## Comments and Tests

When a task creates, edits, or materially reviews code comments, JSDoc, docstrings, public API comments, or test names, this skill MUST govern those artifacts.
Comments SHOULD explain intent, constraints, invariants, non-obvious behavior, or public API semantics.
Comments MUST NOT narrate obvious code.
Test names SHOULD be concise behavioral descriptions.
Test names MUST use the same domain terminology as the governing requirement and implementation.
Test names MUST NOT encode implementation details unless the detail is the behavior under test.

## Agent Instructions and Skills

This skill MUST be applied before another technical skill or reusable instruction set is created or materially edited.
Skill authoring MUST apply `references/skill-writing.md`.
Dependent skills MUST reference this skill instead of restating its general rules.
Dependent skills MUST add only domain-specific rules that affect their workflow.
Cross-skill references MUST distinguish ownership from activation. A handoff MUST be conditional when the owning concern may be absent or already resolved; unconditional activation is appropriate only for an intentionally universal dependency.

Skills MUST optimize for reliable execution rather than exhaustive explanation.
Mandatory workflow rules and high-risk gates MUST remain in the root skill.
Rationale, extended examples, edge cases, and detailed techniques SHOULD move to references when they are not execution-critical.

## Review

For substantial work, apply `references/review-checklist.md` before delivery.
At minimum, verify terminology, normative requirement levels, requirement quality, naming, evidence, and preserved technical literals.

## References

- `references/ste.md` — ASD-STE100 software writing profile.
- `references/requirements.md` — BCP 14 and ISO/IEC/IEEE 29148-informed requirement-writing profile.
- `references/naming.md` — AIP-190 and AIP-140 naming profile.
- `references/evidence.md` — claim verification and source selection.
- `references/skill-writing.md` — execution-focused profile for agent skills and reusable instructions.
- `references/review-checklist.md` — final review checklist.
- `references/sources.md` — standards provenance and maintenance links.
