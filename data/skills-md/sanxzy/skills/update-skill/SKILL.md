---
name: update-skill
version: 6.0.0
description: >-
  Modify an existing Claude Code skill safely — edit frontmatter, body, or companions; rename; bump version; apply review findings. Trigger on "update the X skill", "fix skill Y's description", "rename skill Z", or "/update-skill <name>". Pick generate-skill for new skills; pick this to modify what exists. Audits the target, proposes a change set, diffs every file, writes only after confirmation. Auto-bumps semver (MAJOR/MINOR/PATCH) per change impact; never silently overwrites. Self-contained.
---

# Update Skill

Modify an existing Claude Code skill the safe way: read first, audit, propose, diff, confirm, then write. Every change is shown to the user before it lands. Renames and structural changes are treated as breaking by default and bump the version. **Self-contained** — every rule, audit item, and workflow step lives inside this directory. No invocation of or dependency on any other skill — and neither do the skills edited by this tool (see rule 9 below).

For creating a brand-new skill from scratch, use `generate-skill`. This skill only modifies what already exists.

## Core rules

1. **Read before write.** Every invocation starts by reading the target skill end-to-end (SKILL.md plus every companion file). Never edit an unread file.
2. **Audit before propose.** Produce a findings list against the audit checklist before suggesting any edit. Surfaces issues the user did not ask about.
3. **Diff before confirm.** For every file to change, show a unified diff (or per-file before/after) **before** writing.
4. **Confirm before write.** Never apply a change without explicit user opt-in. Per-file or per-change-set acceptance — either approach works, but the opt-in must be explicit.
5. **Auto-bump version using semver.** Every accepted change set bumps at least PATCH. MAJOR for breaking changes (trigger surface, file renames/removals, workflow reordering), MINOR for new capabilities, PATCH for fixes and refinements. Surface the bump level in the diff so the user can override.
6. **Preserve the user's hand-edits.** Don't rewrite styling, wording, or formatting the user picked unless they explicitly asked. Targeted edits, not opportunistic rewrites.
7. **Never silently rename or move.** A rename changes how the dispatcher finds the skill — always treated as breaking. Update `name:` in frontmatter, the directory itself, and any cross-references in companions, all in one change set.
8. **No fabricated references.** Don't add tool names, package names, URLs, or RFCs that cannot be verified. Audit the skill **for** fabricated references; never introduce new ones.
9. **Self-contained by default; ask before any cross-skill reference.** Don't add a reference to another skill — in the target's `description`, body, companions, scripts, or examples — unprompted. If the **user** asks for one, or the target **already** has one, don't silently include or strip it: ask whether to keep the reference (it makes the target depend on that skill being installed), inline the capability instead, or phrase it as a user action. Runtime tools and user-named agents may stay if they actually exist. See [RULES.md](RULES.md#self-contained-output).

Full audit checklist in [AUDIT.md](AUDIT.md). Workflow detail in [WORKFLOW.md](WORKFLOW.md). Invariants and edge-case rules in [RULES.md](RULES.md).

## Workflow

### 1. Locate

Resolve the target skill from the user's request:

- Explicit path → use it directly.
- Skill name only → look under `~/.agents/skills/<name>/` (the canonical store; `~/.claude/skills/<name>` is typically a symlink to it), or the user's configured base, and confirm the directory exists.
- Ambiguous → ask the user which one they mean. Never guess across multiple candidates.

Confirm the target by listing the directory and reading every `*.md` file in it.

### 2. Audit

Run the [AUDIT.md](AUDIT.md) checklist against the target skill. Group findings into:

- **Critical** — breaks the skill (broken links, missing frontmatter fields, dispatcher will misroute).
- **Concern** — meaningful quality issue (description anatomy violation, vocabulary drift, line-count over threshold).
- **Nit** — cosmetic.

Combine the audit findings with the user's explicit change requests into a single proposed change set.

### 3. Propose

Show the user the change set as a numbered list, grouped by file. Each item: one-sentence description + which files it touches + whether it triggers a version bump. Ask which items to apply (let the user accept all, accept some, or reject the lot).

### 4. Diff

For every accepted item, generate the edit as a unified diff (or per-file before/after block) **without writing anything**. Show the user. If the diff includes a `version:` bump, surface it as a separate line so the user can veto the bump independently of the content change.

### 5. Confirm

Wait for explicit user confirmation. "Apply", "yes", "go" → write. Anything else → loop back to step 3 with the user's revisions.

### 6. Apply

Write the accepted edits using `Edit` (preferred) or `Write` for full rewrites. Apply renames/moves last so intermediate diffs stay coherent. After writing, re-read each modified file once to confirm the edit landed (the runtime errors on failure, but a quick `ls` of the directory confirms structural changes).

### 7. Report

One short summary: files changed, version delta (if any), items skipped (if any), and any followups the audit surfaced but the user deferred. End.

## Companion files

These three companions exist because each covers a **distinct domain**, not because SKILL.md exceeded a line count.

- [RULES.md](RULES.md) — invariants: read-before-write, diff-before-confirm, what counts as breaking, hand-edit preservation, the "don't" list.
- [AUDIT.md](AUDIT.md) — the audit checklist: description anatomy, link integrity, vocabulary drift, line counts, frontmatter integrity, fabricated references, naming, structural sanity.
- [WORKFLOW.md](WORKFLOW.md) — step-by-step detail for each workflow stage, the diff-and-confirm protocol, the rename sub-flow, version-bump decision table, common pitfalls.
