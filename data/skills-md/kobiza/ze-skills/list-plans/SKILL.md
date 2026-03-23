---
name: list-plans
description: Lists all existing plans with their progress, and lets you focus on one to make it active.
disable-model-invocation: true
---

You are executing the "/list-plans" protocol.

1. **Scan Plans:** List all subdirectories inside `.plan/` — each one is a plan. If there are none, tell me: *"No plans found. Start one with `/plan-task` (small task) or `/plan-feature` (multi-phase feature)."* Then stop.
2. **Read Active:** Check `.plan/.active` to see which plan is currently focused (if any).
3. **Show Progress:** For each plan folder, read its `plan.md` and count the rows in the `## Progress` table by status: `done`, `ready-for-dev`, `backlog`.
4. **Display Summary:** Print a table like this:

   ```
   Plans:
   ──────────────────────────────────────────────────
     Name              Progress                Status
   ──────────────────────────────────────────────────
   * user-auth         2 done · 1 ready · 1 backlog  Active
     shopping-cart     0 done · 0 ready · 3 backlog
     payment-flow      3 done · 0 ready · 0 backlog  Complete
   ──────────────────────────────────────────────────
   * = currently active
   ```

5. **Ask to Focus:** Use `AskUserQuestion` with the question *"Which plan would you like to focus on?"* and one option per plan name, plus a `Keep current` option if a plan is already active.
6. **Set Active:** Write the chosen plan name as a single line into `.plan/.active`.
7. **Confirm:** Tell me: *"Now focused on **[chosen-name]**. Run `/plan-phase` to detail the next phase, or `/execute` to run it immediately."*
