---
name: user-story-writer
description: "Generates complete user stories in the 3Cs format (Card, Conversation, Confirmation) from any feature description, requirement, or idea. Use this skill whenever the user asks to write or create a user story, draft acceptance criteria, break down requirements into stories, define a backlog item, or uses phrases like 'user story for', '3Cs', 'as a user I want', 'Given/When/Then', 'acceptance criteria', or 'story for [feature]'. Trigger even when the user only mentions one part of the 3Cs — e.g., just asks for acceptance criteria or just wants a card."
trigger: /story
---

# Story Forge

Turn any feature idea, requirement, or vague ask into a complete user story using the **3Cs format** — Card, Conversation, Confirmation — introduced by Ron Jeffries in 2001.

## The 3Cs at a Glance

| C | What it is | Why it matters |
|---|-----------|----------------|
| **Card** | One sentence: *As a [persona], I want [goal] so that [benefit].* | Fits on an index card. Starts the conversation — not ends it. |
| **Conversation** | Discussion points and open questions the team needs to resolve | Turns a vague requirement into shared understanding before code is written |
| **Confirmation** | Measurable acceptance criteria defined before development begins | Defines "done." Drives testing. Prevents scope creep. |

---

## Step 1 — Understand the Input

Read whatever the user provides. If it's too vague to write a meaningful Card (e.g., "improve the checkout"), ask **one** focused question to surface the missing piece — usually who the user is, or what outcome they need. Don't ask multiple questions at once.

## Step 2 — Identify the Persona

Use a specific role ("returning customer", "warehouse manager", "account admin") rather than the generic "user." Specific personas make stories actionable and help the team build for the right mental model. If the persona isn't stated, infer the most reasonable one from context and note your assumption.

## Step 3 — Write the Card

One sentence, this exact structure:

> As a **[specific persona]**, I want **[concrete action or capability]** so that **[clear benefit or outcome]**.

The *so that* clause is the most important part — it captures the *why*, not just the *what*. If you can't write a meaningful *so that*, ask the user what value they're trying to deliver.

If the input naturally covers more than one story (different personas, unrelated goals), split it. Label each "Story 1", "Story 2", etc. and output each with its own full 3Cs block.

## Step 4 — Write the Conversation

Write 3–5 discussion points the team would need to align on before building this story. Think from the perspective of a developer, QA engineer, and product owner sitting together. Good topics include:

- Ambiguities in the Card (what exactly counts as success?)
- Edge cases that need a decision (what happens if X fails?)
- Dependencies or constraints worth surfacing early
- Business rules or context that shapes implementation

These aren't questions for the user — they're the things the team needs to resolve to write good code. Write them as concise bullet points.

## Step 5 — Write the Confirmation

Write 3–6 acceptance criteria. Every criterion must be:

- **Testable** — someone can verify it with a concrete, repeatable action
- **Unambiguous** — no subjective terms like "fast", "easy", or "user-friendly"
- **Scoped** — specific to this story, not a system-wide requirement

Use **Given/When/Then** for interaction-driven behavior:
> **Given** [precondition], **When** [action], **Then** [expected outcome].

Use a plain statement for non-interaction criteria:
> The system logs all failed login attempts with timestamp and IP address.

If you need more than 6 criteria, the story is probably too large — suggest splitting it.

## Step 6 — Output

Use this exact structure for each story:

---

## [Story Title] *(optional — use if there are multiple stories)*

### Card

> As a **[persona]**, I want **[goal]** so that **[benefit]**.

### Conversation

*Topics for team alignment before development:*

- [Discussion point or open question]
- [Discussion point or open question]
- [Discussion point or open question]

### Confirmation

*Acceptance criteria:*

- **Given** [context], **When** [action], **Then** [outcome].
- [Plain criterion]
- [Plain criterion]

---

After outputting the story, briefly note any assumptions you made (persona, scope, edge case decisions) so the user can correct them.

## Quality Reminders

A story that takes more than one sprint to ship is too big — offer to split it.

The Conversation section is where ambiguity lives. Surface it early so it doesn't become a bug report later.

Acceptance criteria are a contract. If it's not in the Confirmation, it's out of scope for this story.
