---
name: brainstorming
description: Explore and refine ideas before implementation. Use when the user wants to create, build, add, redesign, or change a product, feature, project, workflow, or behavior and the intent, requirements, or design should be clarified first, or when the user explicitly asks to brainstorm. Inspect the current context, ask one question at a time, compare approaches, present a design, and require explicit user approval before implementation.
---

# Brainstorming

Start by understanding the current project context. Ask questions one at a time to refine the idea. Once the intended outcome is clear, present the design and obtain explicit user approval.

<HARD-GATE>
Do not invoke an implementation skill, write code, scaffold a project, or take any implementation action until a design has been presented and the user has approved it. Apply this gate to every project, including apparently simple changes. A simple design may be only a few sentences, but it must still be presented and approved.
</HARD-GATE>

## Workflow

Track these stages with the available planning mechanism and complete them in order:

1. Explore the current context.
2. Offer a visual companion if upcoming questions are inherently visual.
3. Ask clarifying questions one at a time.
4. Propose two or three approaches with trade-offs and a recommendation.
5. Present the design in appropriately sized sections and obtain approval.
6. Write the approved design document.
7. Self-review the specification and fix issues inline.
8. Ask the user to review the written specification.
9. Transition to implementation planning only after approval.

The terminal state of this skill is an approved design and an implementation plan. Do not begin implementation while using this skill.

## 1. Explore the current context

- Inspect relevant files, documentation, repository instructions, and recent commits before asking detailed questions.
- Use read-only inspection until the design is approved.
- Follow established project patterns and constraints.
- Identify existing problems only when they directly affect the proposed work. Do not introduce unrelated refactoring.
- If the request contains multiple independent subsystems, flag the scope immediately. Help decompose it into smaller projects, explain their relationships and order, then brainstorm the first project through this workflow.

## 2. Offer visual help when useful

If upcoming decisions concern layouts, mockups, diagrams, spatial relationships, or other inherently visual material, offer visual help once. Send the offer as its own message, without a clarifying question or other content. In the user's language, say the equivalent of:

> Some of what we are working on may be easier to explain visually. I can show mockups, diagrams, comparisons, and other visuals as we go. Would you like to use that?

If the user accepts, use an available visualization capability for questions that benefit from seeing rather than reading. Continue to use text for requirements, conceptual choices, scope decisions, and textual trade-offs. Acceptance does not mean every question needs a visual.

## 3. Clarify the idea

- Ask exactly one question per message.
- Prefer concise multiple-choice questions when the options are meaningful; use an open-ended question when discovery matters more.
- Focus on purpose, users, constraints, boundaries, and success criteria.
- Preserve the user's original intent instead of prematurely translating it into implementation details.
- Continue until the intended outcome and important constraints are clear enough to compare approaches.

## 4. Compare approaches

- Propose two or three genuinely distinct approaches.
- Lead with the recommended approach and explain why it best fits the stated goal and constraints.
- Make trade-offs explicit, including complexity, speed, maintainability, reversibility, and risk where relevant.
- Apply YAGNI rigorously. Remove features and abstractions that are not necessary for the agreed goal.

## 5. Present the design

- Present the design in sections scaled to complexity: a few sentences for simple work, up to roughly 200–300 words for nuanced sections.
- Ask whether each section looks right before moving to the next one.
- Cover architecture, components, interfaces, data flow, error handling, and testing when relevant.
- Go back to clarification if the user identifies a misunderstanding.

Design for isolation and clarity:

- Give each unit one clear purpose.
- Define how each unit is used, what it depends on, and how it communicates with other units.
- Prefer boundaries that let a reader understand a unit without reading its internals and let internals change without breaking consumers.
- Treat files or components that are difficult to hold in context as a signal that responsibilities may need to be split.

## 6. Write the approved design

After the user approves the full design and repository writes are in scope:

- Save the specification to `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`, unless the user or repository instructions specify another location.
- Write clearly and concisely.
- Do not commit the document unless the user explicitly requests a commit or repository instructions clearly authorize it.

If the user requested brainstorming only and did not authorize repository changes, present the approved design in the conversation instead of writing a file.

## 7. Self-review the specification

Review the written design with fresh eyes and fix issues inline:

- Remove placeholders such as `TBD`, `TODO`, or incomplete sections.
- Resolve contradictions between requirements, architecture, and feature descriptions.
- Confirm the scope is small enough for one implementation plan; decompose it if not.
- Resolve ambiguous requirements by making the agreed interpretation explicit.

Do not ask the user to perform this mechanical review.

## 8. User review gate

After self-review, ask the user to review the written specification before planning implementation. If they request changes, update the design, repeat the self-review, and ask again. Proceed only after explicit approval.

## 9. Transition to implementation planning

After the user approves the reviewed specification:

- Invoke a `writing-plans` skill if one is available.
- Otherwise, create a detailed implementation plan using the available planning mechanism.
- Do not invoke any implementation skill or begin implementation during this transition.

## Anti-patterns

- "This is too simple to need a design."
- Asking several questions in one message.
- Starting implementation because the likely solution appears obvious.
- Presenting only one approach when meaningful alternatives exist.
- Using visuals for questions that are clearer as text.
- Expanding the scope with unrelated cleanup or speculative features.
- Treating a vague approval as permission to implement.

