---
name: generate-prd
version: 4
description: >-
  Write a product requirements document — triggers like "write a PRD", "turn my discussion into a PRD", "document the decisions from my discussion", or planning a new feature. Generates `<cwd>/.plans/<feature>/prd.md` from a finalized discussion summary at `.plans/discussion/<topic>/FINAL.md` (preferred) or an inline interview when none exists. Local file only (no GitHub issue). Lightly resumable via `prd-draft.md` checkpoints. Suggests a design-discussion pass first if no FINAL.md exists.
---

# Generate PRD

Turn either a finalized discussion or a user brief into a PRD. **Prefer a finalized `FINAL.md` (at `.plans/discussion/<topic>/FINAL.md`) when available** — the discussion already resolved the design tree, so the PRD is mostly a translation step rather than a fresh interview.

## Inputs and outputs

**One PRD comes from exactly one FINAL.md.** This skill never aggregates multiple discussions into a single PRD — each invocation processes one discussion topic. If the user wants a PRD that spans multiple discussions, they should first merge them into a single discussion topic and finalize that one `FINAL.md`.

- **Input (preferred):** `<cwd>/.plans/discussion/<topic>/FINAL.md` — a finalized design-discussion summary. Exactly one topic per PRD.
- **Input (fallback):** user brief + inline interview (when no FINAL.md exists).
- **Output:** `<cwd>/.plans/<feature>/prd.md`. The `<feature>` slug **must equal** the source `<topic>` slug when sourcing from FINAL.md, so the discussion and PRD stay linked 1:1.
- **Draft checkpoint:** `<cwd>/.plans/<feature>/prd-draft.md` — incrementally rewritten after each major step so a mid-skill interruption is recoverable.

No GitHub issue is created. The user can post manually if they choose.

See [MAPPING.md](MAPPING.md) for the FINAL.md → PRD section-by-section mapping rules.

## Workflow

### 1. Init — find the source

- **Always look for `.plans/discussion/` first.** List every `<topic>/FINAL.md` whose `STATE.md` contains the line `_Status: finalized_`.
- If one or more exist, ask which **single** discussion to source from (use AskUserQuestion if more than one). One PRD = one FINAL.md; never select multiple.
- If none exist, tell the user: _"No finalized discussion found at `.plans/discussion/<topic>/FINAL.md`. A resolved design discussion produces a much better PRD because the decision tree is already worked out. Want to run a design discussion first, or do an inline interview now?"_ Use AskUserQuestion with two options: `Run a design discussion first (Recommended)` and `Inline interview now`.
- If the user picks inline interview, run these three steps inline before going to step 2:
  1. Ask the user for a long, detailed description of the problem and any candidate solutions.
  2. Explore the repo (Read/Grep/Glob) to verify their assertions and understand the current state.
  3. Interview the user relentlessly about every aspect of the plan, walking the decision tree branch-by-branch with one AskUserQuestion call per turn until you reach shared understanding. Always include a recommended answer.
  Then proceed to step 2, treating the interview output as if it were FINAL.md.
- Confirm the **feature slug** with the user — must equal the discussion `<topic>` slug when sourcing FINAL.md, otherwise propose one from the brief.
- Resume check (after slug is known): if `<cwd>/.plans/<feature>/prd-draft.md` exists, read it and ask whether to resume from the last completed section or restart. If no slug is known yet, scan `<cwd>/.plans/*/prd-draft.md` and surface any matches.

### 2. Map FINAL.md → PRD draft

When sourcing from FINAL.md (see [MAPPING.md](MAPPING.md) for the full table):

| FINAL.md section | PRD section |
|---|---|
| Summary | Solution (verbatim, refined) |
| Decisions table | Implementation Decisions (one bullet per row) |
| Deferred (revisit later) | Out of Scope |
| Open follow-ups | Further Notes |

**Problem Statement** is not in FINAL.md — ask the user to write it from the user's perspective (1–3 sentences). Provide a recommended draft inferred from the discussion if possible.

Write the partial PRD to `prd-draft.md` after this step.

### 3. Sketch deep modules

Propose the major modules to build or modify. Actively look for **deep modules** — modules that encapsulate a lot of functionality behind a simple, testable interface that rarely changes. Present the module list to the user and ask:

- Do these match your expectations?
- Which modules should have tests written?

Update `prd-draft.md`. Avoid file paths or code snippets — those rot fast.

### 4. Derive user stories

Generate a long, numbered list of user stories in `As an <actor>, I want <feature>, so that <benefit>` form, derived from the Decisions + Summary. Aim for extensive coverage — every concrete capability should be a story.

Show the list to the user. Ask: _"Anything missing or wrong?"_ Iterate until confirmed.

Update `prd-draft.md`.

### 5. Testing decisions

Propose:
- A short statement of what makes a good test for this codebase (test external behaviour, not implementation).
- Which modules will be tested (from step 3).
- Prior art — point to similar tests already in the codebase (use Read/Grep to find them).

Confirm with the user. Update `prd-draft.md`.

### 6. Assemble final PRD

Render the full PRD using the template in [MAPPING.md](MAPPING.md#prd-template). Write to `<cwd>/.plans/<feature>/prd.md`. Delete `prd-draft.md` once `prd.md` is final, or keep it if the user prefers an audit trail.

Show the user the final path. **Default: delete `prd-draft.md`** once `prd.md` is written. Only keep the draft if the user explicitly asks for an audit trail before you delete it. Mention they can post the PRD as a GitHub issue manually if they want (`gh issue create --title ... --body-file .plans/<feature>/prd.md`).

## Checkpoint discipline

Rewrite `prd-draft.md` after **every** major step (2–5). If a session dies, the next invocation reads `prd-draft.md`, identifies the last completed section, and resumes from the next.

## What NOT to do

- Don't aggregate multiple FINAL.md files into one PRD — one PRD per discussion. If the user asks to combine, redirect them to merge the discussions into a single `FINAL.md` first.
- Don't re-interview when FINAL.md already answers the question — it wastes the user's time and risks contradicting prior decisions.
- Don't include file paths or code snippets in the PRD — they rot.
- Don't post to GitHub. This skill writes a local file only.
- Don't modify production code.
