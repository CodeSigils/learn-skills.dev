---
name: improve-agents-md
description: 'Use when creating, reviewing, or rewriting CLAUDE.md or AGENTS.md files. Applies rules: concise onboarding context, progressive disclosure, pointers over copies, deterministic tools over style prose, and conditional task rules.'
---

# Improve `AGENTS.md`

Create, critique, or rewrite root `CLAUDE.md` / `AGENTS.md` into a **high-leverage onboarding file**, not a prompt dump.

HumanLayer model:

- `AGENTS.md` is **entry context**, not the knowledge base.
- Explain **WHY / WHAT / HOW**.
- Keep it **short, universal, stable**.
- Move detailed or task-specific guidance to **separate docs**.
- Prefer **pointers to sources** over copied snippets.
- Use **linters, formatters, hooks, commands** for deterministic enforcement.

---

## Use When

Use when the user asks to:

- create a new `AGENTS.md`
- improve or rewrite an existing `AGENTS.md`
- convert a large `AGENTS.md` into a layered setup
- make agent instructions shorter, clearer, or more reliable
- extract task-specific guidance from a root instruction file
- discuss instruction-file structure before editing

Do **not** use this skill for ordinary application code changes.

---

## Operating Modes

Modes:

- **`analyze`** - diagnose and redesign without editing files
- **`rewrite`** - implement a refactor of the instruction files

If intent is ambiguous, default to **`analyze`**.

---

## Execution

Load as needed:

1. **Core methodology:** [references/methodology.md](./references/methodology.md)
2. **Analyze mode output contract:** [references/analyze-mode.md](./references/analyze-mode.md)
3. **Rewrite mode workflow:** [references/rewrite-mode.md](./references/rewrite-mode.md)
4. **Quality rubric and anti-patterns:** [references/quality-rubric.md](./references/quality-rubric.md)

Always classify sections before proposing or rewriting.

---

## Core Rule

Treat the root instruction file as an **onboarding contract** for every session.

If content does not help most tasks, it likely does **not** belong in root.

---

## Deliverables

### In `analyze` mode

Return:

- current problems
- keep / move / conditionalize / delete classification
- recommended root structure
- suggested companion docs
- key tradeoffs and risks

Do **not** edit files.

### In `rewrite` mode

Deliver:

- an updated or newly created root `CLAUDE.md` / `AGENTS.md`
- companion markdown files needed for progressive disclosure
- concise keep / move / conditionalize / delete explanation

---

## Final Standard

Result: **reusable operator handbook**, not prompt dump.
