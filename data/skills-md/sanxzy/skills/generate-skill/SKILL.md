---
name: generate-skill
version: 6.0.0
description: >-
  Scaffold Claude Code skills with rigour: explicit rules, structured workflow, validation. Trigger on "create a skill for X", "scaffold a skill", "I need a skill for <domain>", or "/generate-skill <name>". Enforces frontmatter discipline and description length budget (validated by a bundled script). Self-contained. Never overwrites silently. Self-check checklist; optionally runs a user-named review agent, never auto-runs.
---

# Generate Skill

A disciplined skill scaffold: frontmatter-first, body under 100 lines, companion files by domain, self-check before handoff. Intended for skills that matter enough to get right on the first pass. **Self-contained** — every rule, threshold, and checklist lives inside this directory. No dependency on any other skill — and generated skills are self-contained by default (see rule 9 below).

## Core rules

1. **Description is the only thing the dispatcher sees.** It must encode (a) capability, (b) trigger surface, (c) sibling-disambiguation when relevant. See [RULES.md](RULES.md) for the full description anatomy.
2. **Frontmatter is mandatory.** `name`, `version`, `description`. `name` matches the directory name exactly. `version: 1.0.0` for new skills (semver). `description` always uses the `>-` YAML block scalar to prevent colon-in-value parse errors — see [RULES.md §YAML parse safety](RULES.md#yaml-parse-safety).
3. **SKILL.md stays under 100 lines.** Anything that would push it over goes into a companion file. See [STRUCTURE.md](STRUCTURE.md) for split thresholds.
4. **No fabricated references.** Don't cite packages, URLs, RFCs, or APIs that cannot be verified. If unsure, say "verify before use" or omit.
5. **Idempotent and resumable when stateful.** If the skill produces persistent artefacts, document the state-file location and resume protocol — do not silently overwrite.
6. **No time-sensitive content.** Avoid "as of <year>" or "the latest version of X". The skill outlives the date.
7. **Concrete examples beat abstract prose.** At least one worked example per non-trivial workflow step.
8. **Never overwrite an existing skill silently.** If `<base>/<name>/SKILL.md` exists, ask before proceeding.
9. **Generated skills are self-contained by default; ask before adding a cross-skill reference.** Don't put a reference to another skill into the new skill — its `description`, body, companions, scripts, or examples — unprompted; describe the capability inline or phrase it as a user action ("interview the requirements first with whatever discovery tool is available") instead. If the **user** explicitly asks the new skill to reference another skill, don't silently comply and don't silently refuse: ask whether to keep the reference (it makes the new skill depend on that skill being installed), inline the capability, or rephrase it as a user action. Runtime tools and user-named agents are fine if they actually exist. See [RULES.md](RULES.md#self-contained-output).

Full vocabulary and rule reasoning in [RULES.md](RULES.md).

## Workflow

### 1. Gather

Collect from the user (or the invoking command's arguments):

- **Skill name** — kebab-case, matches directory.
- **One-sentence purpose** — what capability the skill provides.
- **Trigger surface** — which user phrases / contexts trigger the skill.
- **Scope** — single workflow vs multi-mode; needs scripts? needs state files? language-specific?
- **Siblings** — is there an existing similar skill to disambiguate against?
- **Base directory** — defaults to `~/.agents/skills/` (the skill is then symlinked into `~/.claude/skills/` so the dispatcher finds it); let the user override.

If any of these are missing and the user hasn't given enough to infer them, ask the user directly — bundle 2–4 questions per round so they can answer in one pass. This skill assumes the user already knows roughly what they want; for open-ended discovery, use a separate interview tool before invoking this skill.

### 2. Draft

Build the skill directory under `~/.agents/skills/<name>/`:

- `SKILL.md` (always) — frontmatter + workflow body, under 100 lines.
- Companion files when warranted — see [STRUCTURE.md](STRUCTURE.md) for the split thresholds (>100 lines, distinct domains, advanced/rare features, per-language variations).
- `scripts/` only when the operation is deterministic and would otherwise be regenerated each run.

Then symlink it into the dispatcher path so Claude Code discovers it: `ln -s ~/.agents/skills/<name> ~/.claude/skills/<name>`. If `~/.claude/skills/<name>` already exists (symlink or real directory), don't clobber it — stop and tell the user, same as the overwrite check.

Apply [RULES.md](RULES.md) discipline while drafting. Detailed step-by-step authoring guidance in [WORKFLOW.md](WORKFLOW.md).

### 3. Self-check

Before handing back, run the checklist in [CHECKLIST.md](CHECKLIST.md) mechanically. Key checks:

- Description encodes capability + triggers + (if applicable) sibling disambiguation.
- Description fits the length budget — `scripts/check-description.sh` exits `0` (target) or `1` (acceptable, with a one-line justification).
- Frontmatter complete; `name` matches directory.
- SKILL.md under 100 lines.
- All links resolve — `scripts/check-links.sh` exits `0`.
- No fabricated references.
- No cross-skill references added on own initiative.

### 4. Present + offer review

Show the user the file tree and the `SKILL.md` body. Then ask: _"Want me to run an external review agent on it (if one is available), or call this done?"_ Do not auto-invoke — the user opted into rigour, not into surprise tool runs.

If the user opts into external review, invoke whichever review agent they name (none is bundled with this skill). Apply the findings they accept.

## Scripts

- `scripts/check-description.sh <path/to/SKILL.md>` — measures the `description:` length in frontmatter and prints `file=…`, `length=…`, `tier=…`, plus a one-line verdict. Exit code encodes the tier: `0` target (≤500 chars, ship it), `1` acceptable (501–800, ship with a written justification), `2` revise (801–1024, apply the Trim playbook in [RULES.md](RULES.md)), `3` over-cap (>1024, blocking). `64` for usage errors (missing arg, file not found, no `description:` field). Supports both inline and `>-` block scalar formats.
- `scripts/check-links.sh <path/to/skill-directory>` — scans all `.md` files in the directory for `[text](path)` markdown links and verifies each target file exists. Skips URL links and anchor-only fragments. Exit codes: `0` all links resolve, `1` broken links found, `64` usage errors. Prints `checked=N broken=N` summary.

## Companion files

These three companions exist because each covers a **distinct domain**, not because SKILL.md exceeded a line count. Splitting by domain is one of the warranted thresholds in [STRUCTURE.md](STRUCTURE.md).

- [RULES.md](RULES.md) — description anatomy, frontmatter schema, naming conventions, the "don't" list.
- [STRUCTURE.md](STRUCTURE.md) — directory layout, when to split, when to add scripts, companion-file conventions.
- [WORKFLOW.md](WORKFLOW.md) — step-by-step authoring guide, common pitfalls.
- [CHECKLIST.md](CHECKLIST.md) — self-check checklist, run before presenting a generated skill.

For a complete worked example, see `examples/minimal-skill/SKILL.md` — a 30-line skill demonstrating frontmatter, core rules, and workflow.
