---
name: project-memory
description: Create and maintain a concise per-project documentation memory system for agent handoff and low-loss project continuity. Use when setting up or refreshing repository docs, when docs/current-status/next-steps are stale, or after substantial work should be captured for future sessions.
---

# Project Memory

Use this skill to create or refresh a repository's lightweight memory layer without polluting context.

This skill owns project documentation memory. It does not own global `AGENTS.md` setup or Architect methodology setup. Use `$setup-ashieslashy-skills` for those setup tasks.

## Baseline Shape

Expected repository memory set:

- `AGENTS.md`: concise repo-local agent guardrails only; no runtime flow, status history, release process, environment catalog, or architecture overview.
- `docs/00-START-HERE.md`: entrypoint and source-of-truth map.
- `docs/01-repo-overview.md`: stable project map, architecture, key directories, commands.
- `docs/02-current-status.md`: living snapshot of what works, what changed, risks, last validation.
- `docs/03-roadmap.md`: milestones, priorities, deferred work, sequencing.
- `docs/04-next-steps.md`: practical pickup list for the next work session.
- `docs/adr/`: baseline hint directory; add ADR files only when a choice has meaningful tradeoffs.
- `docs/ai/`: baseline hint directory; add temporary handoff, investigation, or implementation-plan files only when useful.

Copy and adapt templates from `assets/templates/` when creating missing files. Treat them as starting points, not boilerplate to leave untouched.

The project-memory methodology snippet lives at `assets/snippets/project-memory-methodology.md`.

## Setup Workflow

1. Read any existing root `AGENTS.md`, `docs/00-START-HERE.md`, and nearby docs before writing.
2. Inspect the repo shape with `rg --files`, package manifests, deployment/config files, and existing tests or scripts.
3. Create only the missing baseline files and hint directories. Preserve the project's existing doc style and naming if it already has one.
4. Keep each doc short and link to deeper docs instead of duplicating detail.
5. Put durable project truth in `docs/`; put temporary investigation notes and draft plans in `docs/ai/`.
6. Audit any existing `AGENTS.md` for durable project truth that should move into `docs/`, then propose a lean guardrail-only rewrite when it would prevent drift.
7. Never overwrite existing docs without reading them. If replacing structure would be substantial, explain the proposed move first.

If this skill is noticed during unrelated work, do not derail the task. Briefly mention that the repo is missing/stale and offer to run the setup later.

## Refresh Workflow

Use this workflow when docs exist but are stale, incomplete, or still contain placeholders. Do not treat existing files as a no-op by default.

1. Read the existing root `AGENTS.md`, baseline docs, and any nearby domain/architecture docs before writing.
2. Inspect repo shape, recent work, validation signals, and current user context enough to distinguish stale content from still-accurate content.
3. Audit `AGENTS.md` for drift against `docs/`. If it contains stable project facts now owned by `docs/`, propose moving those facts and leaving only concise guardrails plus links.
4. Preserve the project's existing doc structure and voice where it is useful. Avoid broad rewrites when targeted updates will do.
5. Replace stale facts and placeholders with repo-specific facts discovered from files. Delete sections that do not apply.
6. If information cannot be discovered, write a dated unknown such as "Not identified from repo scan on YYYY-MM-DD" only when keeping the section is still useful.
7. Update `docs/02-current-status.md` and `docs/04-next-steps.md` first when refreshing after work; update overview, roadmap, ADRs, or `docs/ai/` only when their facts actually changed.
8. Summarize semantic changes, validation run or skipped, and remaining unknowns before writing.

## AGENTS.md Boundary

`AGENTS.md` is part of the baseline, but it is instruction prose rather than ordinary documentation.

- If root `AGENTS.md` is missing during project-memory setup, propose a concise repo-local file from `assets/templates/AGENTS.md` and render `{{PROJECT_MEMORY_METHODOLOGY}}` from `assets/snippets/project-memory-methodology.md`.
- If root `AGENTS.md` exists and mixes agent guardrails with durable project facts, treat that as documentation drift. Propose moving durable facts into the smallest appropriate `docs/` file and rewriting `AGENTS.md` as lean guardrails.
- Keep guardrails short and actionable: usually 5-10 bullets, one or two lines each. If a guardrail needs background, examples, runtime flow, or operational procedure, put the explanation in `docs/` and link or point to it from `AGENTS.md`.
- Keep only constraints that should shape agent behavior before or while reading project docs: safety rules, approval boundaries, validation expectations, repository-specific hazards, and pointers into the docs memory set.
- Do not preserve runtime flow, environment variable catalogs, release procedure, architecture overview, current status, roadmap, or long maintenance notes in `AGENTS.md` merely because they already exist there.
- Architect methodology adoption still belongs to `$setup-ashieslashy-skills`; use that skill when the user wants to install or refresh Ashie-owned methodology blocks.
- When adding project-memory guidance, use `assets/snippets/project-memory-methodology.md` between its BEGIN/END markers.
- Show a semantic summary and diff/full file before writing any `AGENTS.md` change, and write only after explicit approval.

## Update Workflow

After substantial work, update the smallest relevant docs:

- Update `docs/02-current-status.md` when behavior, deployment state, known risks, or validation state changes.
- Update `docs/04-next-steps.md` when the next operator/agent action changes.
- Update `docs/01-repo-overview.md` when architecture, directory ownership, or core workflows change.
- Update `docs/03-roadmap.md` when priority or sequencing changes.
- Add an ADR only for durable decisions with meaningful tradeoffs.
- Promote lasting findings from `docs/ai/` into canonical docs; prune or mark temporary notes as superseded.

Do not paste chat transcripts. Summarize outcomes, decisions, commands, and verification signals in current-state language. Use concrete dates when recording status.

## Writing Rules

- Optimize for fast pickup by a future human or agent.
- Prefer bullets, links, and short sections over narrative.
- Record "what is true now" and "what to do next"; avoid historical archaeology unless it explains current constraints.
- Keep secrets, token paths, and sensitive environment dumps out of docs.
- Make validation explicit: command run, result, date, and any gaps.
- When uncertain, mark assumptions and open questions plainly.

## Template Use

Templates live at:

- `assets/templates/AGENTS.md`
- `assets/templates/docs/00-START-HERE.md`
- `assets/templates/docs/01-repo-overview.md`
- `assets/templates/docs/02-current-status.md`
- `assets/templates/docs/03-roadmap.md`
- `assets/templates/docs/04-next-steps.md`
- `assets/templates/docs/ai/HANDOFF.md` when a handoff note is useful
- `assets/templates/docs/adr/0001-record-architecture-decisions.md` when an ADR is useful
- `assets/snippets/project-memory-methodology.md`

When using templates, replace placeholders with repo-specific facts discovered from files and render snippet placeholders from their canonical snippet files. Delete sections that do not apply. Before proposing generated docs, check the proposed `AGENTS.md` and `docs/` content for unresolved `TODO` placeholders and either resolve them, remove the section, or mark a dated unknown.
