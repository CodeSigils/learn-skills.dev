---
name: skill-gap

description: Identify useful capabilities that are missing from the skills currently available to the agent. Use when a task needs something the current skill set does not cover well, or when you want to discover what skill would be useful to add.

metadata:

  disable-model-invocation: true

---

# Skill Gap

What skill are we missing?

This skill identifies capabilities that would be useful for the current situation but are **not adequately covered by the skills currently available to the agent**.

It does not invent a missing skill merely because one could exist. The gap must come from a real need in the current situation.

It is a **capability-gap detector**, not a skill generator.

## Step 1 — Understand the situation

Before identifying a gap, inspect:

- What the user is trying to accomplish
- The desired outcome
- Important constraints
- What has already been done
- What capability is needed to move forward
- Which available skills could potentially address that need

Use the current context as the source of truth.

## Step 2 — Compare against available skills

Build a current inventory of available skills using the agent's native discovery mechanism when possible.

If necessary, use the same discovery fallback used by `ask`.

For the current task, determine:

1. What capability is needed.
2. Whether an available skill already provides that capability.
3. Whether the available skill only partially covers it.
4. Whether a genuinely useful capability is missing.

Do not recommend a new skill when an existing skill is already sufficient.

Do not confuse a missing workflow, missing tool, or missing information with a missing skill.

## Identify the gap

A real skill gap exists when:

- The task requires a repeatable capability.
- No currently available skill covers that capability adequately.
- Having that capability as a dedicated skill would provide meaningful value.

A skill gap does **not** necessarily exist when:

- The base agent can handle the task directly.
- An existing skill already covers the need.
- The problem is missing data or context.
- The problem requires a one-off action rather than a reusable capability.
- A tool or external integration is missing instead of a skill.

## Describe the missing skill

When a gap exists, describe it in terms of the capability rather than implementation details.

Include:

- What the missing skill should accomplish
- Why it is useful for the current situation
- What kind of situations should trigger it
- What existing skills it would complement or hand off to

Do not design the complete skill unless explicitly asked.

Do not assume a specific name is required.

## Prioritize the gap

When multiple gaps are possible, identify the **single most valuable missing capability** first.

Prefer the gap that:

1. Directly blocks or improves the current task.
2. Is likely to be reusable in similar situations.
3. Has a clear responsibility.
4. Is not already adequately covered.

Mention additional gaps only when they are materially important.

## When no gap exists

If the current skill set is sufficient:

> No meaningful skill gap. The current capabilities are sufficient for this situation.

Do not manufacture a gap just to recommend a new skill.

## How to answer

Format every reply as:

### Gap

<missing capability, or "none">

### Why

<why this capability is missing and useful>

### Suggested role

<what the skill would be responsible for>

### Trigger

<when it should be used>

When no gap exists, use:

### Gap

None.

### Why

<why the current skills are sufficient>

Stop after that.

## Boundaries

This skill does not:

- Create the missing skill
- Write a `SKILL.md`
- Rename or modify existing skills
- Install a new skill
- Execute a recommended skill
- Replace `ask`

Its purpose is to identify **what capability is missing**, not to implement it.

## Maintenance

This skill should remain focused on detecting meaningful gaps in the currently available skill set.

Only update this file when its gap-detection criteria, prioritization rules, or output format need to change.