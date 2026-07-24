---
name: prep
description: |
  Turn a user request into an encoded execution package: refine the goal just enough, research the unknowns first, hand durable requirements to the encode-docs skill, draft a phased PLAN.md, and trigger handoff so a cold session can resume review or cook or cater. The generated plan always include with research, implementation phases, and ends with final verification. It must hold a production-quality verification-driven, evidence-based implementation contract. Triggers: "/prep".
---

# prep — user input -> detailed plan → PLAN.md -> handoff -> HANDOFF.md

`prep` is the planning front door for work that is too fuzzy, too large, or too session-spanning. It analysis and summarize between new idea, research setup, and a final drift-check pass by packaging them into short lived memory files.

## Quality contract

Use these operational cues in the generated plan. “Principal engineer” is a quality signal, not a substitute for an observable contract. Each cue also lives in the description of the skill that owns its step; this contract mirrors them, it is not their sole carrier.

1. **Distill the request:** make the goal, constraints, interfaces, and unknowns explicit. preserve the smallest coherent scope. Ask questions to resolve ambiguity.
2. **Plan:** 
   - research first, then implementation, then final verification;
   - each phase must be executable and verifiable;
   - each phase must have a clear exit criteria and next phase pointer;
   - each phase must have a task table with at least one task, each citing the relevant §V invariants if any.
3. **Encode:** keep `PLAN.md` compact, lossless, and encoded so a cold agent can resume without hidden context.
4. **Review the plan:** embed one cycle of review-plan after encoding to ensure the plan is complete, executable, and verifiable.
5. **Handoff:** trigger `handoff` so `HANDOFF.md` points at the next phase. A fresh plan with no baton is a broken plan.
6. **Report:** summarize the plan and highlight implementation plan in the final message to the user. Then suggest if secondary review-plan cycle is needed before the first implementation phase starts.

The quality contract is complete only when each applicable cue has evidence. Do not use “best effort”, “looks good”, or “principal engineer” as completion criteria.

## When to use

- The user gives a desire, idea, expected behaviour, or fully defined feature and wants the agent to turn it into executable work.
- The work will likely span multiple files, phases, or sessions.
- A cold implementation session should be able to begin work without extra chat context.

## Hard outputs

Every `prep` run must produce all of these:

1. `PLAN.md` at repo root, carrying the phase task details.
2. `HANDOFF.md` at repo root, written via the `handoff` skill after the plan exists.
3. `SPEC.md` at repo root, **only when** the cycle changes durable truth — goal, constraint, interface, sourced research, or a standing invariant. Many cycles need no new `SPEC.md` rows at all. Tasks and one-time fixes are not durable truth and never land in `SPEC.md`.
4. `BACKLOG.md` at repo root, handled in one of two modes chosen by the `PLAN.md` baked-header `planning status`. **Defer mode** — the status reads `work-in-progress`, so a cycle is already running: distill the user request and append it to `BACKLOG.md` for the next cycle, without pruning what is already there and without clobbering the in-flight plan. Do not interrupt an ongoing implementation phase. **Ingest mode** — the status is anything else: read `BACKLOG.md` as part of the request, write or expand `PLAN.md`, and blank `BACKLOG.md` only after that plan is on disk. Blanking any earlier loses the request outright if the session dies before the plan is written. `BACKLOG.md` does not need to be encoded, in fact, it must be detailed enough for a cold agent to pick up the next cycle. No fixed format for `BACKLOG.md` is required.

`PLAN.md`, `HANDOFF.md`, and `BACKLOG.md` are short-lived execution state. `SPEC.md` is the durable memory, and it stays lean with high bar for new inclusion.

## Load

1. Read the user request carefully.
2. Read existing `SPEC.md`, `PLAN.md`, and `HANDOFF.md` for full context.
3. Read `BACKLOG.md` if it exists, and treat it as part of the user request — but in ingest mode only, meaning the `PLAN.md` `planning status` does not read `work-in-progress`. While a plan is running, `BACKLOG.md` is a write target rather than an input.
4. Read just enough repo context to plan real work: existing tests, entrypoints, configs, public interfaces, and nearby conventions.

## Workflow

### 1. Distill the request

Extract:

- the goal the code must accomplish;
- non-negotiable constraints;
- public interfaces or files the outside world touches;
- unknowns that need proof rather than guesses.
- ask the user to resolve any ambiguity, one question at a time, until the request is unambiguous.
- be creative and suggest other possible constrains and approaches that the user may not have considered.

### 2. Always research first

The first plan phase is always research to confirm local code patterns, APIs, external latest documentations, and tests that the later phases must honor. Research is allowed to refine the rest of the plan; when it changes reality, update the later phases instead of pretending the first draft was right. External findings require a source. Only write external sourced findings into `§R` through `encode-docs`.

### 3. Guard the spec, then hand durable facts to `encode-docs`

- **Default to no spec change.** Most cycles touch behaviour that the skill files, `PLAN.md`, and `CHANGELOG.md` already record. A new spec row is the exception, not the norm.
- A new `§V`/`§C`/`§I` row must be a **standing guarantee** a future reviewer keeps checking — never a one-time fix, a task, a bug record, or a note that only matters this cycle.
- Prefer **editing or deleting** an existing row over adding one. If the cycle makes a row false, hand `encode-docs` the removal, not a second row beside it.
- When unsure whether a fact is durable, leave it out. An over-full spec drifts, and every session pays to read it.

Invoke `encode-docs` to update `SPEC.md` with only the sections that genuinely need a durable update:

- `§G` goal — only if the mission changed
- `§C` constraints — only a new non-negotiable boundary
- `§I` interfaces — only a changed external surface
- `§R` sourced research rows — findings that carry a citation
- `§V` proposed invariants — durable standing guarantees only

### 4. Draft `PLAN.md`

Draft `PLAN.md` and hand it to `encode-docs`. It must contain, in this order:

1. a one-line goal;
2. ground rules / process contract for the run, including the applicable quality-contract cues and evidence required for each phase;
3. existing assets or evidence already present;
4. a phase-order table;
5. the full section for each phase.

Set the baked-header `planning status` to `new`, both on a fresh write and on an expansion. That value tracks execution rather than authorship: `cook` and `cater` own the flip to `work-in-progress` and make it when they actually start executing, so a plan nobody has begun never claims to be running. For the same reason, `prep` may expand or rewrite a plan only while its status is not `work-in-progress` — an in-flight cycle is never clobbered.

Use phase ids `F1`, `F2`, `F3`, ... and keep them monotonic.

### 5. Make the phase skeleton predictable

The recommended minimum shape is:

- `F1` — research: confirm unknowns, collect sources, refine `SPEC.md`, tighten the later phases.
- `F2..Fn-1` — implementation phases: code, tests, migrations, docs, or rollout work, split only when a real boundary exists.
- `Fn` — final verification: a check-style pass that compares code against `SPEC.md`, `PLAN.md`, and touched tests before the work is declared done.

The first phase must be research. The last phase must be final verification. Do not put coding ahead of research or after the final verification phase.

### 6. Make every phase executable

Each phase section must name:

- goal;
- inputs of original instructions and research findings;
- files / modules / surfaces likely touched;

Then with multiple implementation tasks block containing the following:

- task id, status, and short description;
- touch paths;
- details of the work to be done including the `§V` invariants to be checked;
- verification contract;
- exit criteria;
- next phase and task pointer.

A cold agent should be able to work on any single phase without extra context.

### 7. Trigger `handoff`

After `PLAN.md` is written, invoke the `handoff` skill so `HANDOFF.md` points at the starting phase `F1`.

## Final verification phase rules

- re-read the relevant `SPEC.md` sections and touched `PLAN.md` phases;
- run verification and unit test command / script to confirm the work is correct;
- classify every relevant `§V`, `§I`, and `§T` item as `HOLD`, `VIOLATE`, or `UNVERIFIABLE`, with file/test evidence;
- sweep touched implementation for logic correctness, unnecessary complexity, missed reuse, and codebase incoherence; cite each finding;
- name any drift explicitly and decide whether code or spec changes;
- record the result table in `HANDOFF.md` before closing the phase.

If the final phase cannot prove the work, the plan is not finished.

## Boundaries

- Do not write code from `prep`.
- Do not skip `PLAN.md`.
- Do not skip `HANDOFF.md`.
- Do not skip the research-first phase.
- Do not skip the final verification phase.
- Do not make `PLAN.md` or `HANDOFF.md` the long-term source of truth; that is `SPEC.md`.
- Do not put tasks, one-time fixes, or bug records in `SPEC.md`; those belong in `PLAN.md`, `CHANGELOG.md`, and git.
- Do not add a `§V`/`§C`/`§I` row that is not a durable standing guarantee. When unsure, leave it out.
- Do not blank `BACKLOG.md` before `PLAN.md` has been written; a session that dies in between would take the request with it.
