---
name: create-spec
description: Create a SPEC.md file for a new feature, product, or system using the Spec-Driven Development (SDD) approach. The spec works in the problem space — it clarifies the "what", not the "how". Use this skill whenever the user wants to write a spec, define requirements, capture what needs to be built, create a specification document, or start the SDD workflow. Trigger even if the user says things like "let's spec this out", "I want to define what we're building", "help me think through requirements", or "let's write a spec for X".
---

# Spec Creator

This skill helps you create a `SPEC.md` — a structured requirements document that clarifies *what* needs to be built, for whom, and why. It lives in the problem space, not the solution space. No architecture diagrams, no code, no "how". Just a crisp, shared understanding of the goal.

The output is a filled-in spec file saved under `specs/<folder-name>/SPEC.md` in the current project.

---

## Step 0: Read the constitution

Check if `specs/CONSTITUTION.md` exists. If it does, read it before doing anything else. It contains project-wide context (tech stack, conventions, rules) that will help you ask better questions and avoid asking things already captured there.

If it doesn't exist, proceed — you don't need it to create a spec.

---

## Step 1: Get familiar with the codebase

Do a quick, read-only scan of the project to build context — like a senior engineer glancing at the codebase before writing a story. This is not a deep exploration (that's what `create-plan` does), just enough to understand what's already there.

- Read the README if one exists.
- Look at the top-level file and folder structure to understand the project layout.
- If the user's request touches a specific area, check whether something similar already exists (e.g., an existing endpoint, component, or module that does something close).
- Note any relevant terminology, patterns, or naming conventions you spot.

If the Agent tool is available, use a subagent for this so it doesn't clutter the main conversation. Keep it fast — spend a minute orienting, not ten minutes exploring.

The goal is to ask better questions in Step 3 and avoid specifying something that already exists or conflicts with what's already built.

---

## Step 2: Get the user's query

Check if the user provided a high-level description of what they want to build in their message.

- If yes, move to Step 3.
- If no, ask them: "What are you looking to build or specify? Give me a rough idea — even a sentence or two is enough to get started."

Wait for their response before proceeding.

---

## Step 3: Ask clarifying questions

Before writing anything, you need a clear enough picture to produce a useful spec. A vague spec is worse than no spec — it gives false confidence while hiding the real unknowns.

Ask multiple targeted questions to uncover:

- **Who** is this for? (roles, stakeholders)
- **Why** does it need to exist? (the pain, the opportunity, the business reason)
- **What does "done" look like?** (acceptance criteria — concrete, observable outcomes)
- **What's out of scope?** (explicit non-goals prevent scope creep)
- **What constraints exist?** (technical, legal, timeline, performance, security, platform)
- **What's unknown?** (open questions that need answers)
- **Is there a ticket ID or project reference?** (for folder naming)

You don't need to ask all of these at once. Group them naturally and ask what feels most relevant given what the user already told you. If the answer to a question is obvious from context, skip it.

Keep asking follow-up questions until you have a clear enough picture. Stop asking when:
- You understand the core problem and who it affects
- You know what success looks like
- You can identify at least the major functional requirements
- Key non-goals are clear

If something is ambiguous, say so and ask. It's better to surface uncertainty now than to spec something nobody needs.

---

## Step 4: Determine the folder name

Create a kebab-case folder name that reflects the topic. Rules:

- Use the subject matter as the base: `user-authentication`, `invoice-export`, `admin-dashboard`
- If the user mentioned a ticket ID or reference number, prepend it: `PROJ-123-user-authentication`
- If the user specified an exact folder name they want, use that as-is
- Keep it short but recognizable — someone should understand what this spec is about from the folder name alone
- Each spec should have a unique folder name. If the user wants to spec something that already has a spec, ask if they want to update the existing one instead of creating a new one. If yes, read the existing `SPEC.md` and continue the conversation to refine it — no new file needed.

Do not ask the user to confirm the folder name unless you are genuinely unsure. Make a reasonable choice and proceed.

---

## Step 5: Create the spec

1. Read `assets/SPEC-TEMPLATE.md` from this skill's directory. This tells you the structure you need to fill in.

2. Create the folder `specs/<folder-name>/` in the project root (create `specs/` too if it doesn't exist).

3. Write the template contents to `specs/<folder-name>/SPEC.md`, preserving the structure exactly. Then fill it in with everything you learned from the conversation — do not create a second file.

The template (`assets/SPEC-TEMPLATE.md`) contains inline guidance for each section — read it before filling in the spec. Follow the instructions in the template's comment block at the top, then remove that block before saving.

4. Before saving the final file, do a self-review pass:
   - Remove all placeholder instructions — italic hints like `_What is this, why does it need to exist..._`, the HTML comment block at the top, and any other template scaffolding that isn't real content
   - Remove sections that ended up empty or irrelevant
   - Check that every acceptance criterion is binary and testable, not vague
   - Check that the spec reads as a clean document an engineer can pick up and act on — no ghost instructions, no leftover template noise

---

## Step 6: Tell the user

Once the spec is written, do a quick assessment of the change's complexity:

- **Trivial/straightforward**: a small, well-scoped change with clear acceptance criteria, no significant unknowns, no risky side effects, touches a limited surface area. A formal plan adds little value here.
- **Non-trivial**: multiple moving parts, unclear dependencies, architectural decisions to make, risk of breaking existing behavior, or the spec leaves open questions about approach. A plan is worth it.

Then tell the user:

> The spec has been created at `specs/<folder-name>/SPEC.md` and is ready for review.
>
> Please review it before we move forward. Let me know if anything is missing, unclear, or needs to change — we can keep refining it here together.
>
> **Suggested next step:** [one sentence based on your assessment — trivial: suggest implement, non-trivial: suggest plan]
>
> When you're ready, reply with:
> - `[P]` to create an implementation plan
> - `[I]` to implement directly

> ⚠️ **Context tip:** If your agent is showing that you've used more than ~50% of the available context window, it's worth opening a fresh chat before proceeding. Long conversations accumulate noise that degrades output quality. In the new chat, just mention the spec you want to plan or implement by name and continue from there.

Then stop and wait. Do not proceed until the user explicitly approves the spec and picks a next step.
