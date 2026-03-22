---
name: create-plan
description: Generate a PLAN.md implementation plan from a SPEC.md file. Use when the user wants to plan implementation for a spec, says "[P]" after creating a spec, or asks to create an implementation plan. The plan translates the spec's "what" into a technical "how" — approach, trade-offs, sequencing, and a task checklist — without writing any code. Trigger whenever someone says "let's plan this", "create a plan for", "plan the implementation", or provides a spec path and wants to move to the planning phase.
---

# Plan Creator

This skill generates a `PLAN.md` — a technical implementation plan grounded in the codebase. It reads a spec, explores the relevant parts of the codebase, and produces a plan that answers the "how": what approach to take, what trade-offs were considered, which files change, and in what order.

The output is saved at `specs/<folder-name>/PLAN.md`, alongside the spec it plans.

**Important constraint:** No code is written during this process. The entire skill is read-only until the final write of PLAN.md.

---

## Step 0: Read the constitution

Check if `specs/CONSTITUTION.md` exists. If it does, read it before doing anything else. It contains the canonical sanity checks, coding conventions, key files, and hard rules for this project — use it to guide your codebase exploration and to pre-populate the Technical Notes in the plan.

If it doesn't exist, proceed — you'll discover what you need during exploration.

---

## Step 1: Ensure there's a spec to plan

A plan must be grounded in a spec. If the user invoked this skill without referencing an existing spec — for example, by describing a feature idea directly or asking you to "plan X" where X is a new concept — do not proceed. Instead, respond:

> "I can only plan changes that are described in a pre-defined spec. Do you want me to load an existing spec or create a new one?"

Wait for the user's answer:

- If they provide a spec folder name (e.g., `user-auth`), proceed to Step 2 using that name.
- If they want to create a new spec, stop this skill and invoke the `create-spec` skill to run the spec creation workflow. Once the spec is created, resume from Step 2 with the newly created spec folder.

---

## Step 2: Find the spec

Check if the user provided a spec path or the name of the spec folder (e.g., `specs/user-auth/SPEC.md` or `user-auth`).

- If yes, proceed to Step 3.
- If no, prompt the user and ask which one to plan:
  > "Which spec would you like to plan? Please provide the path (e.g., `specs/user-auth/SPEC.md`) or the name of the spec folder (e.g., `user-auth`)."

---

## Step 3: Check for an existing plan

Check if `specs/<folder-name>/PLAN.md` already exists.

- If it doesn't exist, proceed to Step 4.
- If it already exists, ask the user:
  > "A plan already exists at `specs/<folder-name>/PLAN.md`. Do you want to replace it from scratch, or update specific sections?"

  - If replacing: proceed to Step 4.
  - If updating: read the existing plan, then focus exploration (Step 5) only on the sections the user wants updated.

---

## Step 4: Read the spec

Read the SPEC.md fully. Extract and note:

- The core feature/goal
- Acceptance criteria (these drive what the plan must achieve)
- Constraints (technical, organizational, timeline)
- Any Technical Notes already in the spec (don't ignore these — they contain early observations)

If the spec is too vague to plan against (missing acceptance criteria, unclear scope), tell the user:
> "This spec is missing [X]. I can generate a plan, but it may not be reliable. Would you like to refine the spec first, or should I proceed with what's here?"

---

## Step 5: Explore the codebase (read-only)

Before writing anything, explore the codebase to ground the plan in reality. The goal is to answer: *what actually needs to change, and where?*

**Do NOT write any code or modify any files during this step.**

Explore to understand:

- **Analogous patterns**: How does the codebase already handle similar concerns? Find the nearest existing equivalent (e.g., if the spec is about adding an endpoint, find how existing endpoints are structured).
- **Files to change**: Which specific files will need to be created or modified?
- **Dependencies**: What does each change depend on? What must be done first?
- **Conventions**: What naming conventions, module structure, test patterns, or framework idioms are already in use? The plan must follow these.

When multiple independent areas need investigation (e.g., backend + frontend + database), use subagents via the Agent tool to explore them in parallel. This saves time and keeps the main context clean.

After exploration, you should be able to name specific real files — not hypothetical ones. If you can't find where something lives, record it as an open question — don't invent a path.

If you discover gotchas, surprises, or non-obvious constraints during exploration that go beyond pure implementation reference, add them to the Technical Notes section under a clearly labeled `### Planning Observations` subsection.

---

## Step 6: Generate the plan

1. Read `assets/PLAN-TEMPLATE.md` from this skill's directory. This tells you the structure and contains inline guidance for each section.

2. Write the template contents to `specs/<folder-name>/PLAN.md` (same folder as the SPEC.md), preserving the structure exactly. Then fill it in with everything you learned from exploration — do not create a second file.

The template contains inline guidance in a comment block at the top — read it before filling in the plan. Follow those instructions, then remove the comment block before saving.

3. Cross-check tasks against acceptance criteria: number the acceptance criteria in SPEC.md (AC 1, AC 2, ...) and tag each task with the ACs it covers — e.g. `**(AC 1, 3)**`. Then verify every AC is referenced by at least one task. If an AC is not covered, either add a task for it or record it as an open question explaining why it was left out.

4. Before saving the final file, do a self-review pass:
   - Remove all placeholder instructions — italic hints, the HTML comment block, and any other template scaffolding that isn't real content
   - Remove sections that ended up empty
   - Verify every file path in Technical Notes is either a real file you found or is labeled "new file"
   - Confirm every task has a binary `Done when:` check
   - Check that the plan reads as a clean document an engineer can pick up and act on — no ghost instructions, no leftover template noise
   - Confirm the human-readable part (Approach + Trade-offs + Tasks + Open Questions) fits under 5 minutes of reading

---

## Step 7: Tell the user

Once the plan is written, surface any open questions directly in your message — don't just say "see the plan":

> The plan has been created at `specs/<folder-name>/PLAN.md`.
>
> Please review it before we move forward — especially the Tasks and Technical Notes.
>
> [If there are open questions, list them here as numbered questions, e.g.:]
> **I have a few questions that would sharpen the plan:**
> - **Q1:** [question] — this affects [what it blocks]
> - **Q2:** [question] — without this, [what's uncertain]
>
> [If no open questions:]
> **Suggested next step:** [one sentence — small/low-risk: suggest implementing; touches critical paths: suggest review sync first]
>
> You can reply with `[I]` to begin implementation now — the plan is valid as-is — but the parts that depend on the open questions above may need revision once answered.

Then stop and wait. Update the plan when the user answers (see Step 8).

> ⚠️ **Context tip:** If you've been in this conversation a while, consider opening a fresh chat before implementing. Long conversations accumulate noise. Just mention the plan path and continue from there.

---

## Step 8: Handle user answers to open questions

When the user answers one or more open questions:

1. **Verify if possible** — if the answer points to a file or location, read it to confirm. Trust what the user says, but verify when you can. If verification reveals something unexpected, mention it.

2. **Update the plan** — revise the Approach, Tasks, or Technical Notes as needed based on what you learned. Remove resolved questions from the Open Questions section.

3. **Tell the user what changed** — briefly summarize what was updated in the plan (e.g., "Updated the middleware mount point in Task 2 and Technical Notes based on your answer about `src/server.ts`").

4. **If all questions are resolved**, suggest implementation:
   > The plan is now fully resolved. Reply with `[I]` to begin implementation.

5. **If questions remain**, list them again so the user can continue answering at their own pace. A plan with open questions is still a valid plan, and if the user want it can proceed to the implementation.
