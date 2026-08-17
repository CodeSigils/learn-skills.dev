---
name: skill-forge
description: Design, write, validate, and package complete Agent Skills (SKILL.md bundles) for AI coding agents such as Claude Code, OpenCode, Codex, Cursor, and any other agent that follows the Agent Skills specification (agentskills.io). Use this whenever the user wants to create a new skill, turn a workflow or set of instructions into a reusable skill, improve or refactor an existing SKILL.md, add scripts/references/assets to a skill, validate a skill's frontmatter and structure, or package a skill for distribution — even if they just say "make this repeatable" or "turn this into something my agent can reuse."
---

# skill-forge

A skill for building other skills. It teaches the agent a reliable, opinionated
process for turning a workflow, a body of expertise, or a set of instructions
into a well-formed **Agent Skill**: a `SKILL.md` file plus optional
`scripts/`, `references/`, and `assets/`, that any spec-compliant agent can
discover, load, and act on.

## When to use this skill

Use skill-forge when the user:
- Wants to create a new skill from scratch ("make a skill for X")
- Has a workflow, checklist, or house style they do repeatedly and wants it
  captured so any agent session can reuse it
- Wants an existing `SKILL.md` reviewed, fixed, or restructured
- Wants a skill split into multiple reference files, or wants scripts added
  for deterministic sub-steps
- Asks you to validate, lint, or package a skill for distribution
- Wants a skill's `description` field tuned so it actually triggers when it
  should

Do **not** reach for this skill just to answer a one-off question about a
topic — only when the deliverable is a reusable skill artifact.

## The core loop

1. **Capture intent** — figure out exactly what the skill should let an
   agent do, and when it should trigger.
2. **Interview & research** — fill in the gaps: inputs, outputs, edge cases,
   dependencies, example files.
3. **Design the layout** — decide whether this is a single-file skill or
   needs `scripts/`, `references/`, `assets/` (see
   `references/authoring-guide.md`).
4. **Write `SKILL.md`** — frontmatter first, then body, following
   progressive disclosure.
5. **Validate** — run `scripts/validate.py` against the draft.
6. **Package (optional)** — run `scripts/package_skill.py` to produce a
   distributable archive, and/or wire up `install.sh` if this skill is meant
   to ship as its own repo.

Be flexible about where in this loop the user actually is — they may arrive
with a rough idea, a half-written `SKILL.md`, or a finished skill that just
needs a health check.

---

## Step 1 — Capture intent

If the conversation already contains a workflow the user wants captured
(e.g. they just walked through a multi-step task and said "turn this into a
skill"), extract the answers from that history first — tools used, order of
steps, corrections they made, input/output formats you observed — and
confirm with the user before proceeding rather than re-asking from scratch.

Otherwise, ask directly:

1. What should this skill let the agent do?
2. When should it trigger — what phrasing or context should cause an agent
   to reach for it?
3. What does a good output look like?
4. Does this skill target a specific agent (e.g. only Claude Code) or should
   it be portable across agents per the Agent Skills spec? This affects
   frontmatter fields and install tooling (see
   `references/frontmatter-schema.md`).

## Step 2 — Interview & research

Ask about edge cases, exact input/output formats, example files, success
criteria, and any external dependencies (CLIs, APIs, libraries) the skill
will assume are present. If the skill wraps a known tool or convention (a
linter, a file format, a company style guide), look it up rather than
guessing — a skill with stale or invented details is worse than no skill.

## Step 3 — Design the layout

Every skill needs a `SKILL.md`. Everything else is optional and should only
be added when it earns its place:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions
└── Bundled resources (optional)
    ├── scripts/    — executable code for deterministic, repetitive, or fiddly steps
    ├── references/ — docs loaded into context only when needed
    └── assets/     — files used in the output itself (templates, icons, fonts, boilerplate)
```

Read `references/authoring-guide.md` before drafting anything — it covers
progressive disclosure, when to split into references vs. inline, domain
organization for multi-variant skills, and common failure modes. This is a
required step, not an optional one: it encodes hard-won conventions that
aren't obvious from first principles.

**By default, generate the full installable repo, not just the bare skill
folder.** Skills produced by skill-forge should be as easy to install as
the reference example at github.com/One4Shell/llm-wiki-skill: a repo root
with `LICENSE`, `README.md`, and `install.sh` around a `skills/<name>/`
directory, so the result works immediately with `npx skills add <repo-url>
--skill <name>` and with its own bundled `install.sh`, no restructuring
needed after the fact. Read `references/repo-layout.md` for the full
pattern and rationale.

To scaffold this automatically:

```bash
bash scripts/init.sh --name "<skill-name>" --dir <parent-directory> \
  --description "<one-line trigger description>" \
  --owner-repo "<github-owner>/<skill-name>-skill"
```

This creates `<parent-directory>/<skill-name>-skill/` — the full repo
layout: `LICENSE`, `README.md`, `install.sh` (all pre-filled from the
skill's name and description), plus `skills/<skill-name>/` with a starter
`SKILL.md` and empty `scripts/`, `references/`, `assets/` directories
(`.gitkeep`'d so they survive being committed empty). Fix the placeholder
`--owner-repo` before publishing if you didn't pass a real one.

Only skip the repo wrapper — with `--bare` — when the skill is meant to
live *inside* an existing project or monorepo rather than as its own
distributable unit, e.g. dropping straight into that project's
`.agents/skills/` or `.claude/skills/`:

```bash
bash scripts/init.sh --name "<skill-name>" --dir <parent-directory> --bare
```

This creates just `<parent-directory>/<skill-name>/` with `SKILL.md` and
the empty resource directories — no `LICENSE`/`README.md`/`install.sh`.

## Step 4 — Write SKILL.md

Fill in, in this order:

- **`name`** — the skill's identifier. Lowercase, hyphenated, matches the
  directory name.
- **`description`** — the *only* thing that decides whether the skill
  triggers. State both what the skill does and the specific contexts that
  should invoke it. Agents tend to under-trigger skills, so err toward being
  explicit and a little insistent about when to use it, e.g. "Use this
  whenever the user mentions X, Y, or wants to do Z, even if they don't use
  those exact words" rather than a dry one-line summary.
- **YAML-safety** — a description containing `: ` (colon+space), `#`, or
  quotes breaks unquoted YAML with errors like "mapping values are not
  allowed in this context" — most real-world descriptions contain a colon.
  Always write the description either single-quoted (escape inner `'` as
  `''`) or as a `>-` block scalar. Same rule for any other free-text
  frontmatter field.
- **Optional frontmatter fields** (`compatibility`, `license`, `version`,
  etc.) — see `references/frontmatter-schema.md` for the full field list and
  which agents honor which fields.
- **Body** — the actual instructions. Keep it under ~500 lines; if you're
  approaching that limit, split detail into `references/*.md` and leave a
  clear pointer in the body for when to read each one. Write imperative,
  step-ordered instructions rather than a prose essay about the domain.

## Step 5 — Validate

Run the validator against the draft before calling it done:

```bash
python3 scripts/validate.py <path-to-skill-dir>
```

It checks: frontmatter is present and parses as real YAML (via PyYAML when
installed), `name` matches the directory name, `description` is non-empty
and under the length agents typically truncate at, `SKILL.md` body length,
that every file referenced from the body actually exists, and that no
bundled script is dead code (referenced nowhere). Fix everything it flags
before moving on. For a manual
second pass, walk through `references/validation-checklist.md` — it covers
things a linter can't catch, like whether the description is actually
specific enough to trigger reliably.

## Step 6 — Package and distribute

If `scripts/init.sh` was run in its default (non-`--bare`) mode, the repo
is *already* installable: `LICENSE`, `README.md`, and `install.sh` are in
place around `skills/<name>/`. At this point the remaining work is just:

1. Fill in the real `--owner-repo` in `README.md` / `install.sh` if a
   placeholder was used.
2. `git init && git add -A && git commit` and push to GitHub.
3. Confirm both install paths work: `npx skills add <repo-url> --skill
   <name>` and `curl -fsSL <raw-install.sh-url> | bash`.

If instead the user only wants a one-off shareable artifact rather than a
git-hosted repo (e.g. to attach to a message or drop manually into another
agent's skills directory), package it:

```bash
python3 scripts/package_skill.py <path-to-skill-dir> [--out <output.zip>]
```

This produces a `.skill`/`.zip` archive containing exactly the skill's
directory tree, ready to hand to `present_files` (if available) or to drop
into `.claude/skills/`, `.agents/skills/`, or wherever the target agent
expects it.

See `references/repo-layout.md` for the full rationale behind this
structure and what each generated file needs to be checked before
publishing.

---

## Reference files

- `references/authoring-guide.md` — progressive disclosure, structuring
  large skills, domain/variant organization, writing style, common mistakes
- `references/frontmatter-schema.md` — full YAML frontmatter field
  reference and which fields matter for which agents
- `references/validation-checklist.md` — manual review checklist to run
  alongside `scripts/validate.py`
- `references/examples.md` — three worked example skills (minimal,
  reference-heavy, script-heavy) to pattern-match against
- `references/repo-layout.md` — the installable-repo pattern (`LICENSE` +
  `README.md` + `install.sh` + `skills/<name>/`), why it matches
  github.com/One4Shell/llm-wiki-skill, and what to check before publishing

## Scripts

- `scripts/init.sh` — scaffold a new skill. Default: a full installable
  repo (`LICENSE`, `README.md`, `install.sh`, `skills/<name>/`). Pass
  `--bare` for just the skill folder.
- `scripts/validate.py` — lint a skill's frontmatter and structure
- `scripts/package_skill.py` — zip a skill directory into a distributable
  `.skill`/`.zip` archive

## Assets

- `assets/repo-template/` — `README.md.tmpl`, `install.sh.tmpl`,
  `LICENSE.tmpl` used by `scripts/init.sh` to generate the installable repo
  wrapper. Edit these if you want every skill you scaffold to carry
  different boilerplate (a different license, an internal registry instead
  of GitHub, etc.).

---

Repeating the loop for emphasis:

1. Capture intent
2. Interview & research
3. Design the layout (single-file vs. scripts/references/assets)
4. Write `SKILL.md`
5. Validate (`scripts/validate.py` + manual checklist)
6. Package, if the user wants a distributable artifact

Iterate with the user rather than delivering a single unreviewed draft —
show the frontmatter first so they can sanity-check the trigger phrasing
before you write the full body.
