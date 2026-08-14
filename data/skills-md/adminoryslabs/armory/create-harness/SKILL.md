---
name: create-harness
description: Guía al usuario, paso a paso y con preguntas, para diseñar su propio harness — un flujo de trabajo chico y de un solo propósito, armado con la combinación de skills, reglas o hooks que la tarea realmente necesite — para una tarea recurrente de su proyecto, como revisión de deuda técnica, seguridad, despliegue, bug fixing, lo que necesite. Use when the user wants to build their own lightweight harness/workflow for a recurring project task, or asks how to package a repeatable agent process from skills, rules, and hooks.
---

# Harness Builder (Interactive)

## Goal

Guide the user through designing a **small, single-purpose harness** for a recurring task on
their own project — a debt review, a security check, a deploy checklist, a bug-fixing routine, or
anything else that follows a repeatable process.

**A harness is not a single skill.** It's a small workflow, built from whichever combination of
pieces the task actually needs: a skill (something the agent runs on request), a rule (context the
agent should always have, added to `CLAUDE.md`), a hook (something that must execute automatically
at a specific event, not just be read), or occasionally a dedicated sub-agent. Most small harnesses
need only one or two of these — do not reach for all of them by default.

**This skill is conversational, not one-shot.** Never assemble the final harness from a single
guess at what the user wants. Walk through each decision below one at a time, and write nothing
until the user has actually answered it.

**Scope discipline is the point of this skill.** A harness that tries to cover "everything" isn't
a harness, it's a wish list — it will drift, contradict itself, and be too vague to actually guide
an agent. If the user proposes something broad (security AND debt AND deploy, all in one), stop and
ask them to pick ONE concern for this pass. They can run this skill again later for the next one.
Scope discipline is about a single clear purpose per pass, not about capping how complete or
substantial the resulting harness ends up being — a harness can end up with several pieces and real
depth if the task genuinely needs it.

## Step 0 — Repo context

Before anything else, check whether this project is part of a multirepo ecosystem (see session 10):
look for a `CLAUDE.md` one folder above the current one.

- **No parent `CLAUDE.md` found:** this is a single-repo project. Proceed directly to Input below,
  using only this repo's own `CLAUDE.md` as context.
- **Parent `CLAUDE.md` found:** ask the user whether this harness needs to operate on just this repo,
  or needs to coordinate across repos (e.g., a deploy checklist that touches both an API and a web
  client).
  - **Single-repo scope:** read this repo's own `CLAUDE.md` as context and proceed normally — the
    parent structure doesn't change anything else below.
  - **Cross-repo scope:** also read the parent `CLAUDE.md`, and treat Context (step 2) and Workflow
    (step 3) as potentially spanning more than one repo. In that case, the bundle from step 7 belongs
    in the parent folder (e.g. `harnesses/{slug}/`), not inside a single child repo, so any repo that
    needs it can find it.

## Input

- A description, in the user's own words, of the recurring task this harness should handle —
  **required**. If it's vague ("something for code quality"), ask what specifically keeps
  happening that they want handled the same way every time.
- The project's existing `CLAUDE.md` / rules, if any — **optional but read them if present**. They
  tell you what context already exists vs. what this new harness will need to state explicitly.

## Workflow

1. **Purpose.** Ask what single, narrow task this harness should handle. If the answer bundles
   multiple unrelated concerns, push back per the Scope discipline note above and ask the user to
   choose one for this pass.
2. **Context required.** Ask what the agent needs to read every time this harness runs to do the
   task well (specific files, folders, existing docs, external references). If the project's
   `CLAUDE.md` is missing something this harness will depend on, say so explicitly — do not assume
   the agent will "figure it out."
3. **Workflow steps.** Ask the user to walk you through the actual process, step by step, in the
   order it should happen. This is domain knowledge only the user has — do not invent a generic
   process and present it as theirs. Number the steps as they describe them.
4. **Output format.** Ask what the harness should produce each time it runs — a written report, a
   pass/fail checklist, inline findings, a file written to a specific path. Get a concrete shape,
   not "a summary."
5. **Guardrails, and how to enforce each one.** Ask explicitly: "Is there anything this harness
   should never do without asking you first?" For each one the user names, decide together which
   kind of enforcement it actually needs:
   - **Hard rule → hook.** If it must never be skipped or forgotten, it needs a hook that executes
     at the right event (e.g., before a commit, before a deploy command runs) — an instruction in a
     rules file can be read and ignored, a hook cannot.
   - **Soft expectation → rule or a step inside the workflow.** If it's a "should remember" rather
     than a "must never", a line in `CLAUDE.md` or a step in the workflow below is enough.
   If the user says there's nothing like that, skip this without inventing a guardrail they didn't
   ask for.
6. **Choose the pieces.** For each part of the workflow defined in steps 3-5, decide the smallest
   mechanism that does the job — do not default to "make it a skill" for everything:
   - A **skill** (`SKILL.md`) for a task the agent performs on request, following the steps from
     step 3.
   - A **rule** (an addition to the project's `CLAUDE.md` or rules file) for context the agent
     should always have without being asked.
   - A **hook** for anything identified in step 5 as a hard rule — it has to execute, not just be
     read.
   - A dedicated **sub-agent** only if the task genuinely needs isolated context — rare for a small,
     single-purpose harness. If the user reaches for this without a concrete reason, ask why a skill
     isn't enough first.
7. **Assemble everything into one small bundle**, e.g. `harnesses/{harness-slug}/` in the user's own
   project, with:
   - Whichever combination of `SKILL.md`, a rules snippet, hook config, and/or sub-agent definition
     the previous step decided on.
   - A short `README.md` at the root of that folder explaining, in plain language: what this
     harness does, which pieces it's made of and what each one is for, and the steps a teammate
     needs to take to turn it on in their own setup (install the skill, add the rule to their
     `CLAUDE.md`, register the hook, copy the sub-agent definition — whatever applies).

   Any `SKILL.md` inside the bundle follows this catalog's frontmatter convention (`name`,
   `description` ending in an English "Use when..." clause) so it stays consistent if it's ever
   published or shared on its own. Any sub-agent definition follows the project's own sub-agent
   convention (frontmatter with `name`, `description`, and the tools it's scoped to) — this is
   the heaviest piece a small harness can have, so keep its scope as narrow as the one purpose
   from step 1, same as everything else in the bundle.
8. **Activate it for the person who just built it.** The README from step 7 is written for a
   teammate setting this up later on their own machine — it does not, by itself, make the harness
   work right now for the user in this session. Do everything that's safely automatable immediately:
   - If a hook was decided in step 6, merge its entry into the current project's
     `.claude/settings.json` (create the `hooks` key or matcher if missing — never overwrite or
     drop any hook entries already there).
   - If a rule was decided in step 6, add it to the current project's `CLAUDE.md` now, not just
     describe it in the README.
   - If a sub-agent was decided in step 6, place its definition file where this project's setup
     actually discovers sub-agents (e.g. `.claude/agents/`), not only inside the harness bundle
     folder — otherwise it exists on disk but isn't invocable.
   - If the skill needs to live somewhere specific to be discoverable in this project (not just
     inside the harness bundle folder), put it there too.
   Tell the user exactly what got activated automatically versus what still requires a manual step
   (e.g., a teammate installing this on a different machine still follows the README).

## Quality Gate

Before writing the final files, silently check:

- The harness has exactly one clear purpose — not several concerns bundled together.
- Every workflow step and every guardrail came from the user's actual answer, not invented to fill
  a gap.
- The output format is concrete enough that two different runs would produce comparably shaped
  results.
- Nothing the user marked as a hard rule ended up as a soft instruction (a "please remember to..."
  line) instead of a hook — and nothing the user marked as a soft expectation was over-engineered
  into a hook it didn't need.
- The harness is not forced into a single skill file when the task genuinely needed more than one
  kind of piece — and it's not split into unnecessary pieces when one skill would have covered it.
- If a sub-agent was chosen, it earned its place (genuine need for isolated context, not reached
  for by default) and it's actually placed where this project discovers sub-agents, not just
  described in the README.
- The bundle's `README.md` actually explains how a teammate turns the harness on, not just what it
  does.
- Whatever was safely automatable got activated now, for the current user — the harness isn't left
  working only "on paper" in the README while nothing actually runs yet.
- If a parent `CLAUDE.md` exists (Step 0), the bundle was placed according to the scope the user
  actually chose — not defaulted to the child repo just because that's where the session started.

## After this skill

The user now has both a working harness and the process to build another one. Remind them at the
end: the same set of questions applies to any other recurring task they identify later — a
different harness for bug-fixing, a lighter SDD variant, a deploy checklist. Running this skill
again, once per concern, is the expected way to grow their own set of harnesses over time.
