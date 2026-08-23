---
name: ask

description: Ask which installed skill fits your situation. A dynamic router that discovers the skills currently available to the agent. Use when you are unsure which skill to invoke, have a vague task, or want a recommended path through the available skills.

metadata:

  disable-model-invocation: true

---

# Ask

You don't remember every skill, so ask.

This is a **router** over the skills currently available to the agent. Describe the situation you are in; the agent identifies the skill (or short sequence) that best fits and stops. It does not execute the recommended skill — you take the next step yourself.

It only knows skills that are actually available to the agent right now. It will not invent skills that are not present.

## Step 1 — Discover what is available

Before answering, build a fresh inventory of the skills currently available to the agent.

Prefer the agent's native skill-listing or discovery mechanism when one exists. If no reliable discovery mechanism is available, fall back to filesystem discovery using the skill locations exposed by the current environment.

For each discovered skill, collect:

- `name`
- `description`

If the same skill appears in multiple locations, prefer the highest-priority copy according to the current environment's resolution rules.

Do not cache the inventory across turns. Always discover the current state so newly installed, removed, or changed skills are reflected.

### Filesystem fallback

When filesystem discovery is necessary, check the standard skill locations used by the current agent environment.

Common examples include:

| Environment | Typical skill roots |
|---|---|
| **Grok** | `/root/.grok/skills/`, `/home/workdir/.grok/skills/` |
| **Claude Code** | `~/.claude/skills/`, `.claude/skills/`, project `skills/` |
| **Codex** | `~/.codex/skills/`, project `.skills/` or `skills/` |
| **Other agents** | Agent-specific skill directories, project `.skills/`, or `skills/` |

Search for `SKILL.md` files under the skill roots that exist in the current environment.

Read only the YAML frontmatter needed to identify each skill:

- `name`
- `description`

Build a simple `name → description` inventory.

## Step 2 — Route

Using only the discovered skills:

1. Restate the user's situation in one short sentence.
2. Match the situation against the discovered skills.
3. Name the single best skill, or a short ordered sequence when a natural hand-off exists.
4. Give the exact next thing the user should type or do.
5. **Stop.**

Do not begin executing the recommended skill in the same turn.

### Decision heuristics

Use these heuristics only when the relevant skill is actually present.

**File type / deliverable**

If the user mentions a concrete deliverable or file type, prefer the matching skill when it exists:

| User intent | Prefer |
|---|---|
| Word / `.docx` / memo / letter / report as a document | `docx` or equivalent |
| PDF create / extract / merge / form / OCR | `pdf` |
| Slides / deck / `.pptx` | `presentation` or `pptx` |
| Spreadsheet / Excel / `.xlsx` | `spreadsheet` or `xlsx` |
| Video / audio processing | `ffmpeg` or media skill |
| Existing image processing | `imagemagick` or image skill |
| Generate or edit an image | image-generation or image-edit skill |

When multiple file skills could apply, use the primary deliverable to decide. If the primary deliverable is unclear, ask the user to clarify it.

**Situation → skill**

| Situation | Prefer |
|---|---|
| Unsure which skill to use | `ask` |
| Professional document | document / docx skill |
| PDF work | pdf skill |
| Slides | presentation / pptx skill |
| Spreadsheet or structured tabular data | spreadsheet / xlsx skill |
| Video or audio processing | ffmpeg / media skill |
| Existing image processing | imagemagick / image skill |
| Image generation or AI image editing | image-generation / image-edit skill |
| Color palette, contrast, accessibility | color skill |
| Live market / stock / crypto data | finance skill |
| Scheduling or recurring jobs | tasks / automation skill |
| Remembering or forgetting information | memory skill |
| Interacting with external services | relevant connected-tool skill |
| Installing a skill | skill-installer or the agent's native install mechanism |
| Creating or improving a skill | skill-creator / writing-skills skill |
| Engineering workflow | the best matching installed engineering skill |

**Common sequences**

Recommend a sequence only when the discovered skills naturally hand off to one another and all participating skills are available.

Examples:

- Research / data → document
- Image generation / processing → document or slides
- Video → still extraction → slides
- New capability → install skill → use it → skill-creator for local changes

Do not create a sequence merely because multiple skills could theoretically help.

## When nothing fits

If no specialized skill is appropriate:

> No specialized skill is required. Proceed with the base agent.

Do not force a skill simply because one exists.

## How to answer

Format every reply as:

1. **Situation** — one short restatement.
2. **Recommendation** — skill name(s) or `no specialized skill`.
3. **Next step** — the exact command or action the user should take.
4. Stop.

If two skills are close, state the concrete test that decides between them.

## Maintenance

This skill intentionally contains no hard-coded skill inventory.

When skills are added, removed, or renamed, the next invocation of `ask` discovers the current state automatically.

Only update this file when the discovery procedure or answer format itself needs to change.