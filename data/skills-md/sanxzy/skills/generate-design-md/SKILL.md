---
name: generate-design-md
version: 4
description: >-
  Generate a Material 3 design document — triggers like "generate DESIGN.md", "create a design system", "scaffold M3 design tokens", "write a Material 3 design doc". Reads `<cwd>/.plans/<feature>/prd.md` (required — hard-stops if absent), runs a 7-question interview (mood, primary color, light/dark, font, density, shape, elevation), derives a full M3 palette via a bundled Node script, writes `<cwd>/.plans/DESIGN.md`. One per project. Lightly resumable via `design-draft.md` checkpoints.
---

# Generate DESIGN.md

Generate `<cwd>/.plans/DESIGN.md` from a PRD plus a short design interview. Output is a Material 3 token set (47 colour roles + typography + density + shape) and seven prose sections. **One DESIGN.md per project** — refuse to silently overwrite.

## Inputs and outputs

- **Input (required):** `<cwd>/.plans/<feature>/prd.md` — a finalized PRD. If multiple feature folders exist, ask which to source. If none exists, hard-stop (see step 1).
- **Output:** `<cwd>/.plans/DESIGN.md` (always this path; not a feature subdirectory — design is project-wide).
- **Draft checkpoint:** `<cwd>/.plans/design-draft.md` — rewritten after each major step.

See [REFERENCE.md](REFERENCE.md) for the full frontmatter schema, density/shape presets, dual-scheme merge logic, and Components template.

## Workflow

### 1. Discover PRD

- Glob `<cwd>/.plans/*/prd.md`.
  - **Multiple matches** → ask which to source (AskUserQuestion).
  - **One match** → use it.
  - **Zero matches** → **hard-stop**. Tell the user: _"No PRD found under `.plans/<feature>/prd.md`. This skill needs a PRD as grounding — a PRD must exist at `.plans/<feature>/prd.md` first, then re-run me."_ Do not accept an inline brief; do not fabricate a PRD.

### 2. Guard the output and check for resume

Apply these checks in order — they are mutually exclusive:

1. **Final exists** — if `<cwd>/.plans/DESIGN.md` is already present, **stop** and ask whether to overwrite. Never silently overwrite. Only proceed on explicit confirmation. (A leftover draft is irrelevant once the final exists.)
2. **Draft exists, no final** — if `<cwd>/.plans/design-draft.md` is present and `DESIGN.md` is not, read the draft's `last_completed_step:` header and offer: resume from the next step, or restart from step 3.
3. **Neither exists** — proceed to step 3 fresh.

### 3. Read the PRD

Extract product context only — do not infer design preferences:
- Audience and tone (from Problem Statement, User Stories).
- User-facing modules (from Implementation Decisions / Modules) — feeds the Components section in step 6.
- Technical depth signals (consumer vs. internal tool vs. dense data app) — feeds default recommendations in step 4.

Write `design-draft.md` with the captured context.

### 4. Interview — 7 questions, one per turn

Use AskUserQuestion. Always recommend a default grounded in the PRD context (e.g. dense data tool → compact density; consumer marketing → airy + rounded). Ask in this order, never batch:

1. **Brand mood** — minimal/document-first · technical/dense · playful · luxe · brutalist
2. **Primary brand color** — single hex (`#005da9`). If the user gives a name, ask for an exact hex.
3. **Color schemes** — light only · dark only · both
4. **Font family** — Inter (default sans) · serif (e.g. Source Serif) · mono-forward (e.g. JetBrains Mono headings) · custom pair (if chosen, follow up: ask for the exact heading family + body family names)
5. **Density** — compact · default · airy
6. **Shape language** — sharp (0px) · soft (4px) · rounded (8px) · pill
7. **Elevation style** — tonal layers + outlines · soft shadows · glassmorphism

After each answer, update `design-draft.md` with the choice.

### 5. Derive the M3 palette

Resolve `SKILL_DIR` to this skill's directory at runtime — do **not** hardcode a username-specific path. Discover it from the loaded skill metadata, or derive from a known skills root (e.g. `"$HOME/.claude/skills/generate-design-md"` or the project's plugin path). Then ensure deps are installed and run the bundled script:

```bash
[ -d "$SKILL_DIR/node_modules" ] || (cd "$SKILL_DIR" && npm install --quiet)
node "$SKILL_DIR/scripts/derive-palette.mjs" <hex-seed> light   # → drop under colors:
node "$SKILL_DIR/scripts/derive-palette.mjs" <hex-seed> dark    # → drop under colors-dark: (only when "both")
```

For light-only or dark-only, run a single invocation. For "both" schemes, run twice and merge per [REFERENCE.md](REFERENCE.md#dual-scheme-output). The script outputs YAML lines ready to paste into the frontmatter. If `npm install` fails, surface the error — do not fall back to a hand-rolled palette; the schema commitment is to deterministic M3 output.

### 6. Compose the doc

Assemble:

- **Frontmatter:** `name`, `colors` (+ `colors-dark` if both), `typography`, `rounded`, `spacing` — apply density and shape presets from [REFERENCE.md](REFERENCE.md). **Note:** density `compact` also bumps `body-large` to 15px and `body-small` to 13px.
- **Prose sections (in order):** Brand & Style · Colors · Typography · Layout & Spacing · Elevation & Depth · Shapes · Components.
- **Components:** baseline (Buttons & Inputs, Forms, Navigation) plus one entry per user-facing module from the PRD. 2–4 lines each. Skip purely-backend modules.

Update `design-draft.md` after each section so a mid-step crash leaves a recoverable state.

### 7. Write the file

Write the assembled doc to `<cwd>/.plans/DESIGN.md`. By default delete `design-draft.md`; keep it only if the user explicitly asks for an audit trail. Confirm with the absolute path and a one-line token summary (mood, primary, schemes, density, shape, elevation).

## Checkpoint discipline

Rewrite `design-draft.md` after every major step (3–6). Each rewrite **must** start with a `last_completed_step: <N>` YAML frontmatter so resume detection is mechanical, not inferred from prose. See [REFERENCE.md](REFERENCE.md#design-draft-checkpoint-format) for the exact draft layout.

## What NOT to do

- Don't write multiple DESIGN.md files — one per project, always at `<cwd>/.plans/DESIGN.md`.
- Don't infer design preferences from the PRD — the PRD has none. Use it only as grounding context for recommendations.
- Don't accept an inline brief in place of a PRD — the PRD is a required input; hard-stop if it's missing.
- Don't hand-roll palettes — always run the bundled script. Deterministic M3 is the contract.
- Don't silently overwrite an existing DESIGN.md.
- Don't modify production code. This skill writes a single Markdown file.
