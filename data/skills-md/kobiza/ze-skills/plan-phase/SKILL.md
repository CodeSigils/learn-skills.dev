---
name: plan-phase
description: Reads the active plan, finds the next unchecked phase, generates a granular implementation guide, and loops for review before handing off to execute-phase.
disable-model-invocation: true
---

You are executing the "/plan-phase" protocol. Your job is to act as the Systems Analyst. Do NOT write application code.

1. **Resolve Active Plan:** Read `.plan/.active` to get the current plan name (e.g. `user-auth`).
   - If the file is missing or empty, list all subdirectories in `.plan/` and tell me: *"No active plan is set. Run `/list-plans` to select one."* Then stop.
2. **Locate the Plan:** Read `.plan/[active-name]/plan.md` and `.plan/[active-name]/findings.md` to refresh your context.
3. **Identify Target:** Find the very first unchecked phase `[ ]` in the checklist.
4. **Draft the Granular Plan (JIT):** Append a detailed implementation guide for THIS PHASE ONLY directly below the checklist in the plan file. It MUST include:
   - **Acceptance Criteria:** 2-3 bullet points of what defines success.
   - **Atomic Tasks:** Break the work down into bite-sized (2-5 minute) steps.
   - **Exact Files:** For every task, explicitly list the file paths to create or modify (e.g., `Modify: src/api/users.ts:10-25`).
   - **Verification:** Include the exact terminal commands needed to test/verify the phase (e.g., `npm run test:auth`).
5. **Review Loop:** Print an inline summary of what was drafted: the phase name, acceptance criteria, number of atomic tasks, and the verification command(s). Then ask:
   *"Does this look right? Reply with: **approve** to proceed to `/execute-phase`, or **change: [your feedback]** to request revisions."*
   - **If `change`:** Apply the requested edits to the appended section in `plan.md`, re-print the summary, and ask again. Repeat until resolved.
   - **If `approve`:** Confirm *"Tasks approved. Run `/execute-phase` to implement this phase."* and stop.
