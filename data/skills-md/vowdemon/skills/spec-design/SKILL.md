---
name: spec-design
description: Use when a PRD, product idea, feature, bug, or existing behavior needs clarification and a stable specification before code design or implementation. Also use when reviewing a specification for ambiguity, gaps, contradictions, or unverifiable behavior. Use this skill for OpenSpec specifications as well.
license: MIT
metadata:
  author: vowdemon
  version: "1.0"
---

# Spec Design

## Overview

Turn a PRD, rough requirement, or product idea into a stable specification that can guide multiple implementations toward the same business behavior. Describe the capability in enough detail to reproduce its intended design without binding it to current code structure or technology choices.

Use this skill for a complete capability specification. Keep change proposals, code plans, implementation tasks, and low-level technical designs separate.

## Specification Model

The specification sections have distinct responsibilities:

- `Purpose` explains why the capability exists, its basic usage, responsibilities, and scope.
- `Design` defines the stable, implementation-independent design of the capability.
- `Requirements` state the observable behavior that must hold.
- `Scenario` blocks verify and constrain the design through BDD examples.
- `Open Questions`, when needed, expose defects, ambiguity, or missing definitions in the specification.

Keep these sections consistent. If a design detail affects observable behavior and must remain stable, cover it with a requirement and at least one scenario. If a requirement introduces behavior absent from the design, update the design. Treat unresolved conflicts as open questions rather than choosing an interpretation silently.

## Scope Check

Before drafting, decide whether the request describes one coherent capability. Split it into separate specs when parts have different goals, rules, lifecycles, or can be released and verified independently. Keep multiple states or branches in one spec when they belong to the same capability.

Clarify missing information only when it materially changes the purpose, design, requirements, or scenarios. Record unresolved matters in `Open Questions`; do not invent behavior to make the document appear complete.

## Output Contract

Use this structure:

```markdown
# <Capability> Specification

## Purpose

<Explain the purpose, basic usage, responsibilities, and scope.>

## Design

<Describe the stable, implementation-independent design in sufficient detail
for different implementations to reproduce the same business behavior.>

### <Optional design topic>

<Organize substantial design details under descriptive level-three headings.>

## <Optional supporting section>

<Add only when the spec needs an independent kind of explanation that does not
fit naturally in Purpose, Design, Requirements, or Open Questions.>

## Requirements

### Requirement: <Behavior name>

The system SHALL <one observable and verifiable behavior>.

#### Scenario: <Concrete case>

- **GIVEN** <initial state>
- **WHEN** <action or trigger>
- **THEN** <observable outcome>
- **AND** <additional outcome, when needed>
```

When unresolved issues exist, append this section:

```markdown
## Open Questions

- <Question>. This spec does not define <missing behavior>.
- <Question>. This spec does not define <missing detail> in sufficient detail.
```

Keep `Purpose`, `Design`, and `Requirements` as level-two headings. Keep `Open Questions` at level two when present. Keep requirement headings in the exact form `### Requirement: ...` and scenario headings in the exact form `#### Scenario: ...` so OpenSpec-style tooling can recognize them.

## Purpose Rules

Write a concise introduction to the capability. Explain its intent, expected use, responsibilities, and practical scope in natural prose. Include basic usage when it helps establish the capability, such as the invocation model of a CLI.

Do not turn Purpose into a detailed design, acceptance checklist, implementation plan, or fixed list of boundary and dependency fields.

## Design Rules

Define the stable business design that should survive changes in code, framework, storage, and internal architecture. Include only topics relevant to the capability, such as:

- public interface or usage model
- core concepts and relationships
- workflows, states, and transitions
- input, output, and error semantics
- business rules and precedence
- command, option, configuration, or response behavior
- interactions with other capabilities
- compatibility or lifecycle rules

For a CLI, Design may define command grammar, command responsibilities, option semantics, configuration precedence, output conventions, exit behavior, and interaction flow. It should not prescribe parser libraries, classes, functions, source files, or internal algorithms.

Describe dependencies naturally where they affect the design. When a dependency changes observable behavior, capture that behavior in a requirement and scenario. Leave purely technical dependencies to implementation design.

## Requirement Rules

- Use one requirement for one behavior contract.
- Use `SHALL` or `MUST` for mandatory behavior.
- Use `SHOULD` only when justified exceptions are allowed, and `MAY` only for genuinely optional behavior.
- Make every requirement observable or explicitly verifiable.
- Give every requirement at least one scenario.
- Keep requirement names concise and stable.
- Put implementation mechanics in later design or planning artifacts.

Do not add a separate acceptance-criteria section. Scenarios are the executable-style acceptance criteria for their requirements.

## Scenario Rules

Every scenario must use `GIVEN`, `WHEN`, and `THEN`; use `AND` only for additional conditions or outcomes. Each scenario should describe one concrete case that exercises its parent requirement instead of paraphrasing it.

Cover the cases that materially constrain the design, including relevant success paths, invalid input, empty states, permissions, repeated actions, boundary values, dependency failures, partial failures, and recovery behavior. Do not create scenarios mechanically for cases that do not apply.

## Open Questions Rules

Include `## Open Questions` only when the specification has unresolved issues. When present, keep it as the final section and use it to identify:

- behavior the spec has not defined
- behavior mentioned but not defined in sufficient detail
- conflicting rules that still need a decision
- missing decisions that could change the design or requirements

State the missing definition directly and explain why the question remains open when useful. Do not hide open questions inside requirements or resolve them through unstated assumptions. Omit the entire section when no open questions remain.

## Additional Sections

Add another level-two section only when the spec needs a distinct type of explanation that cannot fit naturally in Purpose, Design, Requirements, or Open Questions. Name it for its actual content and keep it at the stable specification layer. Do not add standard sections by habit or repeat information already expressed elsewhere.

Place supporting sections where they best preserve the reading flow. Keep `Open Questions` last when present.

## OpenSpec Compatibility

When working in an OpenSpec project, inspect its existing specs, configuration, and workflow instructions before deciding the output form. Preserve the project's distinction between current specifications and proposed changes, and keep requirement and scenario structures compatible with its tooling.

Treat Design and other optional sections as extensions that must not interfere with structured requirement blocks. Prefer project conventions over generic assumptions, and use available OpenSpec validation when appropriate.

## Bug Specifications

For a bug, specify the intended correct behavior rather than the implementation of the fix. Design should explain the correct execution path at the level needed to make the behavior reproducible.

Requirements and scenarios should constrain that path and cover the conditions that exposed the defect as regression behavior. Use the observed faulty behavior only as context, update existing behavior instead of duplicating it, and record uncertainty in Open Questions.

## Review Checklist

Before finalizing, verify that:

- Purpose explains why the capability exists and what role it serves.
- Design is detailed enough to reproduce the same business behavior without relying on current code.
- Design avoids volatile implementation choices.
- Every requirement is observable, normative, and covered by a scenario.
- Every scenario uses the exact heading level and GIVEN/WHEN/THEN structure.
- Critical success, failure, and boundary behavior is covered where relevant.
- Design, requirements, and scenarios do not contradict one another.
- Missing or ambiguous behavior is listed in Open Questions, and the section is omitted when none exists.
- The document describes one coherent capability.

## Red Flags

Stop and revise when:

- Purpose contains detailed workflows, rules, or implementation decisions that belong in Design.
- Design is too vague for another implementation to reproduce the same business behavior.
- Design prescribes current classes, functions, files, frameworks, storage choices, or internal algorithms without an explicit external constraint.
- A stable observable design rule has no corresponding requirement or scenario.
- A requirement introduces behavior that Design does not explain.
- A scenario paraphrases its requirement without a concrete initial state, trigger, and observable result.
- A scenario omits `GIVEN`, `WHEN`, or `THEN`, or uses the wrong heading level.
- Requirements and scenarios describe incompatible outcomes for the same condition.
- The document adds a separate acceptance-criteria section that duplicates scenarios.
- Missing decisions are silently converted into assumptions instead of Open Questions.
- Open Questions contain resolved decisions or implementation tasks.
- Optional sections repeat existing content or exist only to fill a template.
- One spec combines capabilities with independent goals, rules, or lifecycles.

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Treating Purpose as a complete feature description | Keep Purpose concise; move stable behavioral detail into Design |
| Writing Design as a code plan | Describe durable interfaces, concepts, workflows, rules, and semantics |
| Keeping Design at summary level | Add enough detail for independent implementations to reproduce the same business behavior |
| Copying Design paragraphs into Requirements | Extract the specific observable obligations that must remain true |
| Using scenarios to introduce the design | Define the behavior in Design first, then verify it with requirements and scenarios |
| Restating a requirement as its scenario | Give the scenario a concrete context, trigger, and outcome |
| Creating a separate acceptance-criteria list | Use scenarios as the acceptance criteria for each requirement |
| Adding fixed boundary or dependency sections by habit | Explain relevant context naturally and add a section only when the content needs one |
| Describing a dependency only by name | Define its observable effect in Design and cover failure behavior when it matters |
| Guessing through ambiguity | Record the exact missing or insufficient definition in Open Questions |
| Adding an empty Open Questions section | Omit the section when no unresolved issue exists |
| Adding every possible edge case | Cover cases that materially constrain the design and omit irrelevant ceremony |
