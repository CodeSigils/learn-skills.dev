---
name: do-task
description: "This skill implements a specific task from a project's ROADMAP.md file. It should be used when the user wants to work on a roadmap action item by its ID (e.g., '1.1', '2.3'). Triggered by requests like '/do-task 1.1', '/do-task 2.3', or 'do task 3.1'. Works alongside the project-init skill (which creates the roadmap) and the checkpoint skill (which commits afterward)."
---

# Do Task

## Overview

Implement a specific action item from `docs/ROADMAP.md` by its ID. Read the task's full context from the roadmap, research as needed, clarify ambiguities with the user, execute the implementation, and deliver a test plan.

## Workflow

### Step 1: Parse and Load Task

Extract the task ID from the user's arguments (e.g., `1.1`, `2.3`, `3.1`).

Read `docs/ROADMAP.md` from the current working directory. If the file does not exist, check for `ROADMAP.md` at the project root. If neither exists, inform the user and stop.

Locate the action item matching the given ID (the `### X.Y` heading). Extract:

- **Phase title** — the `## Phase N: ...` heading the task belongs to
- **Task title** — the `### X.Y ...` heading text
- **Description** — the `**Description**:` content
- **Requirements** — the `**Requirements**:` checklist items
- **Implementation Notes** — the `**Implementation Notes**:` content

If the task ID is not found, list all available task IDs with their titles and ask the user to pick one.

If the task belongs to the **Future** phase (which uses Description/Features/Rationale instead of Description/Requirements/Implementation Notes), inform the user that Future-phase items are high-level directions, not scoped tasks. Offer to help break it down into concrete action items instead.

### Step 2: Load Project Context

Read the following files if they exist, to understand the full project context:

- `docs/SPEC.md` — architecture, tech stack, data models, key decisions
- `docs/STYLES.md` — design tokens, component styling (for frontend tasks)

Also review the existing codebase structure to understand what has already been built. Use `Glob` and `Read` to survey the project directory — check for existing files, components, utilities, and patterns that the task should build on or integrate with.

### Step 3: Clarify Ambiguities

Before writing any code, evaluate whether the task's requirements and implementation notes are clear enough to proceed confidently. Consider:

- Are there technical implementation choices that could go multiple ways?
- Are there UI/UX decisions not specified in the requirements or STYLES.md?
- Are there concerns, trade-offs, or risks worth surfacing?
- Do the requirements reference something that doesn't exist yet or is unclear?

If anything is unclear, use the `AskUserQuestion` tool to ask focused follow-up questions. Do not guess on ambiguous requirements — ask.

If everything is clear, proceed without asking unnecessary questions.

### Step 4: Research (If Needed)

If the task involves unfamiliar APIs, libraries, patterns, or integrations mentioned in the implementation notes, conduct targeted research using `WebSearch` to understand:

- API usage and current best practices
- Library-specific patterns and gotchas
- Integration approaches

Keep research focused on what is needed for this specific task.

### Step 5: Implement

Execute the task by working through each requirement in the checklist. Follow existing project patterns and conventions discovered in Step 2.

Implementation rules:
- Address every `- [ ]` requirement item — do not skip any
- Follow the guidance in **Implementation Notes**
- Match existing code style, naming conventions, and patterns in the project
- Apply styles from `docs/STYLES.md` when the task involves UI
- Keep changes focused on this task — do not refactor unrelated code
- Write clean, working code — not placeholder stubs

### Step 6: Test Plan

After completing the implementation, provide a **concise, step-by-step test plan** the user can follow to verify the task works end-to-end.

Format the test plan as:

```
## Test Plan for X.Y: <Task Title>

1. <Action to take>
   → Expected: <What the user should see or experience>

2. <Next action>
   → Expected: <Expected result>

...
```

Each step should be a concrete action (run a command, navigate to a URL, click something, check a value) with a one-liner describing the expected outcome.

The test plan should cover:
- Happy path verification of each requirement
- Edge cases mentioned in the requirements or implementation notes
- Any error states or fallbacks the task implements
