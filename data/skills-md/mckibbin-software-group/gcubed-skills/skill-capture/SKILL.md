---
name: skill-capture
description: Capture reusable delivery lessons as review-first skill proposals or upstream packets. Use after completed tasks, debugging, deliveries, repeated workflows, or hard-won lessons to decide docs update, new skill, skill patch, or maintainer-ready upstream proposal.
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
4. For `patch-existing-skill`, draft a minimal proposed change to that skill. Do not mutate installed or shared skills unless the user explicitly asked for implementation and the target is in the current writable project.
5. For `new-skill-proposal`, read `references/new-skill-proposals.md`, choose the authoring route before drafting, and keep the main agent responsible for review and writes.
6. For `upstream-skill-proposal`, read `references/upstream-proposals.md` and create a self-contained packet that can be sent by issue, chat, email, or pull request without exposing the original project.
7. Keep proposals review-first. Show the intended files, summary, and diff before writing unless the user explicitly asked to implement.
8. For `new-skill-proposal` and `upstream-skill-proposal`, once the full proposal or packet is drafted, run `$review-synthesis` over it before final presentation. Use the skill-review lenses, apply useful cleanup changes when edits are already in scope, and present any remaining findings or tradeoffs with the final proposal.

## Proposal Destinations

- Local review packet: a project-local proposal for future review; it is not an installed skill.
- Upstream packet: a portable handoff for another maintainer; it is not accepted or incorporated until that maintainer says so.
- Distributed skill change: direct changes under `skills/<skill-name>/` only when working in the target collection and the user explicitly asked to implement.

## Agent-Led Quality Gate

Before presenting a proposal, run an explicit review pass in prose. If subagents are available and the user allowed their use, use an independent reviewer when the candidate skill is broad, safety-sensitive, or likely to be reused across projects.

The main agent remains responsible for deciding which findings to apply, preserving privacy and portability, and producing the final user-facing proposal.

- Trigger clarity: the description says exactly when to use the skill.
- Scope: the skill captures procedure, not project diary entries.
- Duplication: no existing skill already owns the workflow.
- Shape: `SKILL.md` has `name` and `description`, the name matches the directory, and `agents/openai.yaml` follows the collection's existing interface shape when present.
- Consent: subagents, tool installs, writes, and upstream PRs or publication are explicitly approved before use.
- Safety: no instruction conflicts with higher-priority rules or approval boundaries.
- Privacy: no secrets, customer identifiers, private URLs, token paths, local-only absolute paths, raw logs, or transcript excerpts.
- Portability: examples and commands are framed so another repo can adapt them.
- Progressive disclosure: `SKILL.md` stays concise, with details moved to directly linked references only when needed.
- Verification: the skill tells future agents how to check their work.
- Repository fit: README and maintainer docs are updated when adding a distributed skill, and the proposal does not duplicate setup, install, or scope behavior owned by the Skills CLI or setup skills.
- Upstream fit: the packet is understandable without the source project, states why the skill is broadly useful, and redacts project-private facts.

If a deterministic script would clearly catch repeated mechanical mistakes, recommend it as a follow-up rather than adding it by default.

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
