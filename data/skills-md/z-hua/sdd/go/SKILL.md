---
name: go
description: Use for complex, multi-subsystem changes — isolate, specify, brainstorm, plan, execute with subagents, verify, archive
---

# SDD — Spec-Driven Development

## Invocation Arguments

Check for `--skip-setup` in the arguments passed to this skill.

**If `--skip-setup` is present:**
- Skip Language Selection — default language is **简体中文**
- Skip Prerequisites Check — HARD GATE
- Proceed directly to **Resume or Start**

## Language Selection

**This is the first step.** Ask the user which language to use for all subsequent communication and generated documents (proposals, specs, design docs, task lists, commit messages, etc.). Present the options:

- **English**
- **简体中文**
- **Other** (let user specify)

Use the chosen language consistently throughout the entire workflow.

**Announce** (in the chosen language): "I'm using sdd:go for this change."

## Prerequisites Check — HARD GATE

**After language selection is complete, you MUST pass these checks before doing ANYTHING else. If any check fails, STOP IMMEDIATELY. All messages to the user — including error messages and installation instructions from these checks — must be in the chosen language.**

**Check 1 — OpenSpec:** Run two checks independently:

- **Directory:** `ls openspec/ 2>/dev/null` — does the `openspec/` directory exist?
- **CLI:** `which openspec 2>/dev/null` — is the `openspec` CLI on PATH?

Both are required. If only one is present:

- Directory exists but CLI missing → "Found `openspec/` directory but `openspec` CLI is not in PATH. Run `npm install -g openspec` or check your PATH."
- CLI exists but directory missing → "Found `openspec` CLI but no `openspec/` directory. Run `npx openspec init` to initialize."
- Neither exists → Show full installation instructions (see Results below).

**Check 2 — Superpowers:** Look at your available skills list. All of the following must be present:

- `superpowers:using-git-worktrees`
- `superpowers:brainstorming`
- `superpowers:writing-plans`
- `superpowers:subagent-driven-development`
- `superpowers:test-driven-development`
- `superpowers:systematic-debugging`
- `superpowers:verification-before-completion`
- `superpowers:finishing-a-development-branch`

If any are missing, Superpowers is not fully installed. Do NOT verify by reading internal files — the only reliable check is whether the skills are loaded in your current session.

**Check 3 — OpenSpec skills:** Look for `opsx:propose`, `opsx:verify`, `opsx:archive` in your available skills list. All three must be present. If any are missing, tell the user which ones and instruct: "Run `openspec update` to generate the missing OpenSpec skills." — then **END.**

**Results:**

- **All checks pass** → Announce "Full SDD mode — specs + quality enforcement." and continue.
- **OpenSpec missing** → STOP. Show the targeted message from Check 1. If neither exists: "Install with: `npx openspec init` then run `openspec update`. See https://github.com/allaboutai/OpenSpec" — then **END.**
- **OpenSpec skills missing** → STOP. List the missing skills. Tell user: "Run `openspec update` to generate the missing OpenSpec skills." — then **END.**
- **Superpowers missing** → STOP. List which required skills are missing. Tell user: "SDD requires Superpowers. Install with: `/plugin install superpowers@claude-plugins-official`. See https://github.com/obra/superpowers" — then **END.**
- **Multiple checks fail** → STOP. Show all relevant installation instructions — then **END.**

## Branch Naming Convention

Use `sdd/<change-name>` where `<change-name>` matches the OpenSpec change directory name exactly. Collect or confirm the kebab-case `change-name` before isolation so the workspace can be created first and `/opsx:propose` generates the matching change directory inside it.

## Unified Output Directory

**All artifacts live in the OpenSpec change directory.** Do not write to `docs/superpowers/specs/` or `docs/superpowers/plans/`.

```
openspec/changes/<change-name>/
├── proposal.md       ← Specify: /opsx:propose generates
├── specs/*.md        ← Specify: /opsx:propose generates (delta specs)
├── design.md         ← Brainstorm: superpowers:brainstorming writes HERE
├── tasks.md          ← Plan: superpowers:writing-plans writes HERE
└── .openspec.yaml    ← OpenSpec metadata
```

Override rules for Superpowers skills:

- `superpowers:brainstorming` → write to `openspec/changes/<change-name>/design.md`
- `superpowers:writing-plans` → write to `openspec/changes/<change-name>/tasks.md`
- `superpowers:verification-before-completion` → any reports go to the change directory
- `superpowers:systematic-debugging` → any investigation notes go to the change directory

## Iron Laws

1. **Specs before code** — No implementation without a specification first.
2. **Tests before implementation** — RED-GREEN-REFACTOR for every change. **Exempt:** pure configuration, static assets, CSS/styling, documentation, dependency version bumps — state the reason explicitly.
3. **Root cause before fix** — No fixes without systematic investigation.
4. **Evidence before claims** — Run it, read it, prove it. No "should work."
5. **Archive preserves knowledge** — Every completed change archives full context.

Creating or entering an isolated workspace before writing the spec is allowed. The prohibition is against writing implementation code before the spec/proposal exists.

If you catch yourself thinking "just this once" or "it's too simple to need specs" — **STOP. The iron laws apply especially when you think they don't.**

## Start

After prerequisites pass, proceed to **Isolate** to start a new change. You may start a new change at any time, even if other changes are already in progress in other branches or worktrees.

---

## Phase Sequence

All phases are mandatory and must execute in order: **Isolate → Specify → Brainstorm → Plan → Execute → Verify → Archive → Finish**. No phase may be skipped, abbreviated, or reordered.

---

## Isolate

**REQUIRED SUB-SKILL:** Use `superpowers:using-git-worktrees`

- Create an isolated worktree at `.worktrees/<change-name>` with branch `sdd/<change-name>`
- Auto-detect and run project setup
- Verify clean baseline (all tests pass, 0 failures) before starting implementation

**Gate:** Isolated workspace ready before running `/opsx:propose`.

---

## Specify

**REQUIRED:** Run `/opsx:propose` with the change description.

- OpenSpec creates: `proposal.md`, `specs/*.md`, `design.md`, `tasks.md`
- `design.md` and `tasks.md` are initial scaffolds — Brainstorm and Plan phases will refine them

`/opsx:propose` may output a generic next-step message — **ignore it**. Next phase is always **Brainstorm**. Announce: "Specify phase complete. Next: Brainstorm."

---

## Brainstorm

**REQUIRED SUB-SKILL:** Use `superpowers:brainstorming`

Feed the OpenSpec artifacts as starting context — read `proposal.md`, `specs/*.md`, `design.md`. The skill will ask clarifying questions, propose 2-3 approaches with trade-offs, present design in sections for approval, and write a validated design document.

**Output path override:** Read the existing `openspec/changes/<change-name>/design.md` first, then fully rewrite it incorporating its original content and the brainstorm discussion results.

**HARD GATE:** Design must be approved by user before proceeding. No code until design is signed off.

---

## Plan

**REQUIRED SUB-SKILL:** Use `superpowers:writing-plans`

**Input:** `tasks.md` (high-level), `design.md` (technical approach), `specs/*.md` (requirements)

**Output:** Bite-sized implementation plan where each task has exact file paths, complete code blocks (no placeholders, no "TBD"), verification commands with expected output, and TDD steps.

**Output path override:** Read the existing `openspec/changes/<change-name>/tasks.md` first, then fully rewrite it incorporating its original content and the plan discussion results.

Self-review checklist before presenting to user:
- Every spec requirement maps to at least one task
- No placeholders or incomplete code blocks
- Type consistency across tasks
- TDD steps included (failing test before implementation), or TDD exemption reason explicitly stated

**HARD GATE:** Plan must pass self-review AND user approval before execution begins.

---

## Execute

**REQUIRED SUB-SKILL:** Use `superpowers:subagent-driven-development`

Tasks execute sequentially — each subagent completes and its changes are committed before the next is dispatched. This avoids merge conflicts and ensures each subagent sees the up-to-date working tree.

Per task:

1. **Dispatch implementer subagent** — fresh context. Subagents must read the current working tree; do not rely solely on the plan's code blocks.
2. **Implementer implements with TDD** — follows `superpowers:test-driven-development`
3. **Spec compliance review** — verify code matches OpenSpec's delta specs exactly (nothing more, nothing less)
4. **Code quality review** — check patterns, tests, maintainability
5. **Fix issues** → re-review until both stages pass
6. **Mark task complete** in tasks.md

**If a bug is encountered:** Use `superpowers:systematic-debugging` — reproduce → hypothesize → validate → fix. Write a failing test BEFORE fixing.

**If implementation diverges from spec:** STOP, update the spec, then continue. Specs are the source of truth.

---

## Verify

**Step 1 — Full test suite:** All tests must pass. No exceptions. No "known failures."

**Step 2 — Evidence-based verification:**
- **REQUIRED SUB-SKILL:** Use `superpowers:verification-before-completion`
- Run every verification command fresh. Read actual output. Every claim backed by output from after the last code change.

**Step 3 — Spec compliance:**
- Run `/opsx:verify`
- Fix all ERROR issues before proceeding. WARNINGs are advisory.

**Gate:** Tests pass AND verification evidence shown AND no ERROR issues.

---

## Archive + Finish

**Step 1 — Archive knowledge:**
- Run `/opsx:archive`
- Delta specs merge into `openspec/specs/`; full context preserved in `openspec/changes/archive/YYYY-MM-DD-<name>/`
- **No spec changes?** For infrastructure/tooling changes with no spec impact, use `--skip-specs`.

**Step 2 — Integrate code:**
- **REQUIRED SUB-SKILL:** Use `superpowers:finishing-a-development-branch`
- Options: merge locally, create PR, keep branch, or discard. Tests must pass before any integration option.

**Done.** The change is implemented, verified, archived, and integrated.

---

## Failure Handling

**Verification repeatedly fails (`/opsx:verify` reports ERROR issues):**
- Re-read the failing spec requirements carefully
- Fix implementation to match spec, or update spec if the requirement was wrong
- Re-run — max 3 attempts before escalating to user
- After 3 failures: present full error context, then suggest: (1) update the spec if the requirement was wrong, (2) confirm with user before running `git reset --hard` to last passing commit and re-approach, (3) manual investigation

**Tests keep failing during execution:**
- **REQUIRED SUB-SKILL:** Use `superpowers:systematic-debugging`
- If root cause is outside change scope, STOP and report to user
- Do NOT work around failures with skips or mocks

**User wants to abandon a change:**
- Use `superpowers:finishing-a-development-branch` → choose "Discard work" (handles both branches and worktrees)
- OpenSpec change directory remains — user can delete manually or resume later
- Do NOT run `/opsx:archive` on incomplete work

**A required sub-skill fails or is unavailable mid-workflow:**
- Report to the user immediately — do not skip the phase or continue
- Show the exact error or the name of the missing skill
- Ask the user to verify the skill is still loaded, then restart from the failed phase

**OpenSpec command failures:**
- `/opsx:propose` fails → Check: invalid change name (must be kebab-case), schema not found, directory already exists
- `/opsx:verify` issues → Fix ERROR-level before proceeding; WARNINGs are advisory
- `/opsx:archive` fails validation → Fix spec validation errors; for infrastructure/tooling changes with no spec impact, use `--skip-specs`
- Any unexpected error → Show full output to user. Do not retry blindly.

## Red Flags

**STOP immediately if:**

- Writing code before the spec/proposal exists
- Skipping TDD (unless the change qualifies for TDD exemption — see Iron Laws)
- Claiming tests pass without running them since the last code change
- Proceeding after a verification failure
- Skipping archive because "the change is done"
