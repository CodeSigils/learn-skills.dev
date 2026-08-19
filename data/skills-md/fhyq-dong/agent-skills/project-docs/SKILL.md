---
name: project-docs
description: >-
  Set up and maintain a project's durable documentation layer — the plan/, AGENTS.md
  (agent-facing truth), README.md (human-facing), and docs/. Use this whenever the user
  wants to lay down doc scaffolding for a NEW project; ADOPT this convention on an existing
  or messy codebase (audit what's there, regenerate accurate docs from the real code); or,
  after a stretch of development, SYNC/reconcile drift (fold durable lessons into AGENTS.md,
  refresh README from reality, archive the now-stale plan). Trigger it on phrases like
  "set up the docs / plan structure", "write/refresh AGENTS.md or CLAUDE.md", "my docs are a
  mess, clean them up", "reconcile the plan with what we actually built", "wrap up and
  document this", "update the project docs after this work" — even when the user doesn't name
  a specific file. Prefer this skill over ad-hoc doc edits whenever the goal is keeping the
  plan/AGENTS.md/README/docs coherent as a set.
---

# project-docs

Keep a project's documentation honest with **minimum ceremony**. The whole point is that the
user defines architecture up front, lets it drift while building, and does **not** want to
babysit docs — so this skill draws a sharp line between docs that are *disposable scaffolding*
and docs that are *maintained truth*, and it regenerates the maintained ones from **reality**
(the code) rather than from a plan that has since drifted.

## The mental model (read this first — everything below follows from it)

Four destinations, three different lifespans. Conflating them is the mistake this skill exists
to prevent:

| Path | What it is | Who reads it | Lifespan |
|---|---|---|---|
| `plan/` | Up-front architecture + execution path | the agent, at kickoff | **Disposable scaffolding.** Value is at creation; archive it once it drifts. Nobody maintains it for re-reading. |
| `AGENTS.md` | Durable agent-facing truth: commands, architecture shape, conventions, gotchas | every agent, every session | **Maintained + lean.** It's loaded into context each session, so bloat has a running cost. |
| `README.md` / `docs/` | Human-facing usage/reference | people (and agents) | **Regenerated from the real code**, never copied from a drifted plan. |
| `CLAUDE.md` | Claude Code's native entry point | Claude Code | **One line importing AGENTS.md** — single source, no duplication. |

Two principles that fall out of this:

- **A drifted plan left lying around is a liability, not an asset** — a future agent reads it as
  current truth and gets misled. So the skill *archives* stale plans with a "historical" stamp
  instead of leaving them to rot or silently deleting them.
- **AGENTS.md and README must match the code, not the intention.** Verify every command, flag,
  path, and config key against the actual repo. Never write a fact you didn't confirm.

## Choosing the mode

The user has one of three situations. If they name it ("new project", "adopt this on my old
repo", "update the docs"), use that. Otherwise infer from the repo state and **say which mode
you picked and why** before acting:

- **`init`** — new/empty project, little or no code yet, no AGENTS.md. → Lay down the scaffolding.
- **`adopt`** — real code exists but the doc layer is absent, partial, or messy. → Audit, then
  regenerate accurate docs from the code and set up the structure.
- **`sync`** — the convention is already in place and development has moved on. → Reconcile drift.

When unsure between `adopt` and `sync`, look for an existing `AGENTS.md` that already follows
this convention: present → `sync`; absent/ad-hoc → `adopt`.

---

## Mode: init (new project)

The goal is to give the project a clean skeleton and force the architecture thinking up front —
without producing docs that will immediately go stale.

1. **Confirm the essentials** you can't safely guess: language/stack, how it's meant to be run,
   and the rough goal. Ask only what you genuinely can't infer; don't interrogate.
2. **Write `plan/PLAN.md`** — the up-front architecture and execution path (template below). Stamp
   it as initial scaffolding so nobody mistakes it for living truth later.
3. **Write `AGENTS.md`** — seed it from the *durable* parts of the plan (stack, intended commands,
   architecture shape, conventions). Keep it lean. Leave commands you haven't verified marked as
   `(planned)` until real code makes them runnable.
4. **Point `CLAUDE.md` at it** — create `CLAUDE.md` containing a single import line `@AGENTS.md`
   (Claude Code resolves this). This keeps one source of truth and works cross-platform without
   symlinks. If a `CLAUDE.md` already exists with content, fold that content into `AGENTS.md`
   first, then replace it with the import line.
5. **Write a minimal `README.md`** — what it is + intended quick start. Note that it will be
   regenerated from real code as the project fills in.
6. **Create `docs/`** only if there's something to put there; don't make empty folders.
7. **Tell the user the layout** in two lines and remind them `plan/` is disposable scaffolding.

## Mode: adopt (existing, possibly messy project)

The goal is to make the doc layer reflect what the code *actually* is — this is a from-reality
audit, not a polish of whatever docs happen to exist.

**Adopt is not "regenerate." Gauge the existing docs first.** Some projects already have meticulous,
accurate, well-structured docs — a from-scratch rewrite there destroys hand-crafted value for nothing.
After reading reality and the existing docs (steps 1–2), make an honest call: if they already match the
code and follow this convention's spirit, **say so plainly and stop at surgical fixes** (a dedupe, a
stale line, the one missing piece) plus whatever structural change the user actually wants. Reserve a
full regeneration for docs that are genuinely absent, wrong, or incoherent. Churning good docs to look
busy is the opposite of the point.

1. **Read reality first.** Scan the codebase for the real architecture, entry points, and module
   layout. Extract the *actual* build/test/run commands from `package.json` scripts, Makefile,
   pyproject/tox, Dockerfile/compose, CI config, etc. When practical, verify a command works
   rather than trusting a stale README.
2. **Read what's already there** — existing `README`, `CLAUDE.md`, `AGENTS.md`, `docs/`, stray
   design/plan files. Note where they contradict the code; the code wins.
3. **Regenerate `AGENTS.md` from the code** — real commands, real structure, real conventions,
   and the non-obvious gotchas you noticed while reading (the things that would bite the next
   agent). Lean and true beats comprehensive and stale.
4. **Consolidate to a single source** — fold any useful `CLAUDE.md` content into `AGENTS.md`, then
   make `CLAUDE.md` the one-line `@AGENTS.md` import.
5. **Rewrite `README.md` from reality** — accurate quick start; every example must actually run.
6. **Handle the mess without destroying it.** For outdated plan/design docs, **move** them to
   `plan/archive/` with a `> Historical — see AGENTS.md/README for current truth` stamp rather than
   deleting. If you must delete or overwrite something with real content, surface it to the user
   and ask first.
7. **Optionally reconstruct `plan/PLAN.md`** as a snapshot of the *current* architecture (marked
   "reconstructed from code") so future work has a baseline — only if the user wants a plan doc.
8. **Report a short diff**: what was stale/contradictory, what you regenerated, what you archived.

## Mode: sync (reconcile after development)

The goal is the wrap-up step the user actually cares about: turn "what really got built" into
maintained docs, and retire the plan that drifted.

1. **Find what changed.** Use git when available (`git log`/`git diff` since the last doc update,
   or the current branch's diff) plus the current `plan/` to see where things moved. If there's no
   git signal, diff the plan against the current code by reading.
2. **Do a plan↔reality diff.** Note where the implementation diverged from `plan/` and *why* — this
   is the useful part of drift, not noise. Keep it brief.
3. **Fold durable lessons into `AGENTS.md`** — new/changed commands, new conventions, new gotchas.
   Add only things that are *durable and non-obvious*; resist turning AGENTS.md into a changelog.
   Prune anything the code no longer does.
4. **Refresh `README.md` / `docs/` from the real code** — update usage, examples, and reference to
   match current behavior. Re-verify commands and examples; fix stale references you find.
5. **Retire the drifted plan.** If the plan is now history, move it to `plan/archive/` with the
   historical stamp. If it's still an active roadmap, update it — but don't polish it for reading;
   it stays scaffolding.
6. **Report** the doc changes and any stale references you fixed, so the user can eyeball it
   without reading the whole thing.

---

## Rules that apply in every mode

- **Verify, don't invent.** Never write a command, flag, path, env var, config key, or API field
  you haven't confirmed in the source. A fabricated-but-plausible instruction is worse than a
  missing one because it looks trustworthy.
- **Every code example must be runnable.** If you can't verify it, mark it clearly or leave it out.
- **AGENTS.md earns its length.** It's loaded every session — include the durable, non-obvious
  stuff (architecture shape, gotchas, the commands that matter) and cut the rest. If it reads like
  it could be regenerated from the code in five seconds, it's probably filler.
- **Don't destroy to tidy.** Archive stale docs; ask before deleting or overwriting real content.
- **Match the house style.** If the repo already has a doc voice/structure, follow it rather than
  imposing this skill's templates verbatim.
- **Single source for agent context.** AGENTS.md is canonical; CLAUDE.md imports it; don't maintain
  two copies that can drift apart.

## Templates

Adapt these — they're starting points, not a rigid format. Keep sections that carry weight, drop
ones that don't apply.

**`plan/PLAN.md`**
```markdown
# Plan: <project / feature>
> Initial scaffolding — expected to drift. Current truth lives in AGENTS.md and README.
> Archived to plan/archive/ once superseded.

## Goal
What we're building and why (a few sentences).

## Architecture
The intended shape: major components, how they fit, key decisions + the reasoning.

## Execution path
Ordered steps to get there. Mark parallelizable ones.

## Open questions / risks
Unknowns and things likely to change.
```

**`AGENTS.md`**
```markdown
# AGENTS.md
One-line description of what this project is.

## Stack
Languages, frameworks, notable dependencies.

## Commands
Run / build / test / lint — the real, verified invocations.

## Architecture
The durable shape: where the major pieces live and how they relate. Not a file listing —
the map that stays true as files move.

## Conventions
Patterns the code follows that an agent should match (naming, error handling, structure).

## Gotchas
The non-obvious things that will bite: sharp edges, required setup, footguns, "don't do X".
```

**`CLAUDE.md`**
```markdown
@AGENTS.md
```

**`README.md`** — standard human-facing: what it is, quick start (verified), usage, and a pointer
to `docs/` if it exists. Written for a person who's never seen the repo.
