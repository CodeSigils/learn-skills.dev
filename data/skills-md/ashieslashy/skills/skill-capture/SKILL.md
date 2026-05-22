---
name: skill-capture
description: Capture reusable delivery experience as review-first skill proposals, including upstream packets for shared skill collections. Use when a user wants to review a completed task, debugging session, project delivery, repeated workflow, or hard-won lesson and propose whether it belongs in docs, a new skill, an existing skill patch, or a maintainer-ready upstream proposal.
---

# Skill Capture

Use this skill to decide whether recent work should become reusable agent capability. The output is a proposal, not a live skill mutation.

## Core Judgement

Capture a skill only when the experience contains reusable procedure:

- A workflow likely to recur across projects or sessions.
- A debugging pattern with clear symptoms, checks, and fixes.
- A verification checklist that prevents real regressions.
- A domain convention that agents repeatedly need but would not infer reliably.
- A correction to an existing skill's trigger, procedure, boundary, or validation.

Do not create a skill for:

- One-off project status, roadmap, or handoff notes. Use project docs instead.
- Facts that belong in `AGENTS.md` as local guardrails.
- Secrets, credentials, private customer data, or environment-specific paths.
- Broad preferences without a narrow trigger.
- Anything that mostly says "remember this happened".

## Workflow

1. Inspect the task context, relevant diffs, docs, command output, and any existing skills that may already cover the lesson.
2. Classify the result:
   - `no-action`: no durable reusable knowledge.
   - `recommend-docs-update`: useful project fact, but not a skill.
   - `patch-existing-skill`: an installed or repo skill needs a focused change.
   - `new-skill-proposal`: a new reusable workflow is justified.
   - `upstream-skill-proposal`: a reusable workflow should be offered to a shared skill collection that the current project may not be able to access directly.
3. Explain the classification in 2-5 bullets.
4. If proposing a skill, draft only the files needed for review:
   - `SKILL.md`
   - `agents/openai.yaml` when this repo or skill collection uses it
   - optional `references/` only when the main skill would otherwise become long
   - optional `scripts/` only for deterministic, repeated, low-judgement operations
5. For upstream proposals, create a self-contained packet that can be sent by issue, chat, email, or pull request without exposing the original project.
6. Keep proposals review-first. Show the intended files, summary, and diff before writing unless the user explicitly asked to implement.

For `upstream-skill-proposal`, read `references/upstream-proposals.md` for the packet shape and maintainer handoff workflow.

## Agent-Led Quality Gate

Before presenting a proposal, run an explicit review pass in prose. If subagents are available and the user allowed their use, use an independent reviewer when the candidate skill is broad, safety-sensitive, or likely to be reused across projects.

- Trigger clarity: the description says exactly when to use the skill.
- Scope: the skill captures procedure, not project diary entries.
- Duplication: no existing skill already owns the workflow.
- Shape: `SKILL.md` has `name` and `description`, the name matches the directory, and `agents/openai.yaml` follows the collection's existing interface shape when present.
- Safety: no instruction conflicts with higher-priority rules or approval boundaries.
- Privacy: no secrets, customer identifiers, private URLs, token paths, or local-only absolute paths.
- Portability: examples and commands are framed so another repo can adapt them.
- Progressive disclosure: `SKILL.md` stays concise, with details moved to directly linked references only when needed.
- Verification: the skill tells future agents how to check their work.
- Repository fit: README and maintainer docs are updated when adding a distributed skill, and the proposal does not duplicate setup, install, or scope behavior owned by the Skills CLI or setup skills.
- Upstream fit: the packet is understandable without the source project, states why the skill is broadly useful, and redacts project-private facts.

If a deterministic script would clearly catch repeated mechanical mistakes, recommend it as a follow-up rather than adding it by default.

## Proposal Shape

For new skills, prefer `skills/<skill-name>/SKILL.md` plus `agents/openai.yaml` when the collection uses it.

For work captured outside a shared skill collection, prefer a local review packet. Local packets keep the candidate `SKILL.md` at the packet root for quick project review; upstream packets use a nested `skill/` directory so the portable files can be copied cleanly into a shared collection.
```text
docs/ai/skill-proposals/<YYYY-MM-DD>-<skill-name>/
  SKILL.md
  rationale.md
```

`rationale.md` should summarize:

- source task or delivery context, without pasting transcripts
- why this should be a skill rather than docs
- what existing skill was checked, if any
- known limits and review questions

## Example

- Classification: `patch-existing-skill`
- Rationale: repeatable failure mode in an existing workflow; verification belongs in that skill, not project docs.
- Proposal: patch `skills/<existing-skill>/SKILL.md`; no script needed.

## Drafting Rules

- Keep `SKILL.md` under 100 lines when practical.
- Use one clear workflow before adding variants.
- Prefer "ask the user when..." boundaries over brittle guessing.
- Add scripts only when the operation is deterministic and worth maintaining.
- Do not include auxiliary README, changelog, or installation files inside a skill folder.
- For this repository, update the top-level README skill list and maintainer map when adding a new distributed skill.
- Keep external projects proposal-only: they may produce upstream packets, but incorporation into a shared collection is a maintainer action.
