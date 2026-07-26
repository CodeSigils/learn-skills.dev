---
name: workflow
description: Frame a task with explicit scope, proof, and next step before execution starts.
metadata:
  version: "0.1.0"
  owner: adaptive-skills
  category: engineering
---

# Overview

Use this skill to start non-trivial work without relying on hidden thread memory. It creates a lightweight operational frame before action.

# When to Use

- starting a non-trivial task
- returning from a handoff or compaction
- work that can sprawl across multiple files or decisions

# When NOT to Use

- tiny mechanical edits with obvious scope
- tasks already covered by a fresh detailed plan

# Core Moves

1. State the goal in one sentence.
2. Define what is in scope right now and what is not.
3. Read only the minimum context needed to act safely.
4. Declare the minimum proof before making meaningful changes.

# Optional Modules

- **Scope guard** — Add an explicit in/out list when the work has a high risk of expansion.
- **Plan snapshot** — Write a short plan when there are multiple steps or decision points.
- **Handoff reset** — Summarize the current state when picking work back up after a pause.

# Activation Triggers

- Use the scope guard if the task crosses more than one subsystem.
- Use the plan snapshot if success depends on ordered steps.
- Use the handoff reset if the context is fragmented or stale.

# Expected Output

- clear goal
- explicit immediate scope
- minimum proof statement
- next operational step

# Verification

- The task can be explained in one sentence.
- There is a visible boundary around the immediate work.
- The proof is proportionate to the change.

# Handoff Signals

- The work crosses ownership or domain boundaries.
- A different specialist is needed to continue safely.
- The next step requires a different operating context.

# Pairs Well With

- `feature-planning`
- `testing`
- `triad-check`

# Anti-patterns

- Starting implementation before naming scope.
- Loading large amounts of context instead of framing the task.
- Treating momentum as proof of clarity.
