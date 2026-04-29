---
name: task
description: Universal task dispatcher. Start, route, and execute any task through the development workflow (Steps 0-9). Invoke on every task — /task <description>, /task #<issue>, or /task to start fresh. Also invocable as /workflow.
version: 1.0.0
---

# /task

## Surface Routing

Before starting, pick the right tool for the job:

| Activity | Tool | Why |
|---|---|---|
| Architecture planning | Claude Code /plan | Opus, 1M context |
| Feature implementation | Claude Code | Hooks, subagents, worktrees |
| Quick single-file fix | VS Code Claude ext | Faster for small scope |
| DevOps / terminal | Codex CLI | Strong at terminal tasks |
| Background refactor | Codex Cloud | Fire-and-forget PR |
| Code review | GitHub Actions | Async, no session cost |
| Test writing | subagent: test-writer (CC) / inline (Codex) | Isolated context |
| Documentation | subagent: doc-writer (CC) / inline (Codex) | Cheap, focused |
| Research | Claude.ai Projects | Persistent, web search |

## Cross-Tool Notes

This skill uses Claude Code features. Portable equivalents for Codex/Cursor:

| Claude Code | Codex / Cursor |
|---|---|
| `TaskCreate` / `TaskUpdate` | Markdown checklist in `.branch-context.md` |
| `EnterWorktree` | Use absolute paths + `git -C` for all ops |
| `/orient`, `/brainstorming`, etc. | Read `.agents/skills/<name>/SKILL.md` and follow manually |
| Subagent dispatch (`implementer`, `test-writer`) | Execute sequentially in main session |
| Agent Teams | Not supported — use sequential work |
| `/review`, `/plan-review` | Read `.agents/skills/review/SKILL.md` and follow manually |

## Skill Aliases (temporary)

These skills are planned but not yet extracted. When invoked, follow the corresponding step inline:

| Alias | Step | Status |
|---|---|---|
| `/isolate` | Step 2 | inline — extract to ai-skills later |
| `/plan` | Step 3 | extracted — invoke directly |
| `/review` | Steps 4, 6 | extracted — invoke directly |
| `/build` | Step 5 | inline — extract to ai-skills later |
| `/ship` | Step 8 | inline — extract to ai-skills later |
| `/bail` | any | existing skill — invoke directly |

## Args

| Invocation | Behavior |
|---|---|
| `/task <description>` | Start new task |
| `/task #<issue>` | Start from GitHub issue |
| `/task` | Start new task — ask what to work on |

## Copilot Mode

In copilot mode (`operating-mode.md`), the workflow is a **menu, not a pipeline**:
- Present available steps. Execute what the human asks. Don't enforce order.
- Worktree-first is relaxed — primary worktree writes are allowed.
- Invariants below still apply except where `operating-mode.md` explicitly overrides.
- If the human says "follow the workflow," run step-by-step but pause for approval at each transition.

## Invariants

These rules are agent-interpreted guidance, not machine-enforced. They cannot be skipped regardless of task type or scope unless noted:

```starlark
REQUIRE worktree BEFORE code
REQUIRE orient.complete BEFORE plan
REQUIRE review(plan).pass BEFORE build UNLESS scope == one_sentence
REQUIRE validate.pass BEFORE review(build)
REQUIRE review(build).pass BEFORE archive
REQUIRE branch.base IS CURRENT(origin/main) UNLESS stacking

WHEN ci.down:
  USE local_merge AT step_8
WHEN files_touched MATCH [AGENTS.md, config.toml, sync.sh, skills]:
  REQUIRE codex_specialist IN review_panel
```

## Steps

Persist significant decisions to `.branch-context.md` during Steps 3-5 — not just at reflect/bail time.

### Step 0 — Bootstrap

Create a task list to track progress through the steps:
- **Claude Code**: `TaskCreate` with one item: "Step 1 — Orient." Remaining steps populated after orient.
- **Codex/Cursor**: add a markdown checklist to `.branch-context.md`.

### Step 1 — Orient

Invoke `/orient` with args (Codex: read `.agents/skills/orient/SKILL.md`). It produces:
- **task_type**: feat / fix / chore / docs / test / refactor
- **scope**: can the entire diff be described in one sentence? Yes → short path (skip Steps 3-4). No → full path. Note: short description ≠ small change — "update all deps" sounds short but may touch dozens of files.

After orient completes, populate the task list with remaining steps for the detected path. Short path (one-sentence scope) skips Steps 3-4.

### Step 2 — Isolate

`git fetch origin main` first — always start from a current base.

**Not in a worktree:**

Create a worktree from origin/main:
```bash
git worktree add .worktrees/<name> -b <prefix>/<name> origin/main
```
Use the branch prefix from Step 1 (feat/, fix/, chore/, etc.). Use absolute paths and `git -C` for all subsequent operations. Claude Code: optionally use `EnterWorktree` to switch session CWD.

**Already in a worktree:**

Verify the branch is current with main:
```bash
git fetch origin main
git merge origin/main
```
Stop and ask if conflicts arise. Different base only when explicitly stacking on another feature branch.

### Step 3 — Plan

**One-sentence scope:** SKIP — proceed to Step 5. Log: "Step 3 — Plan: SKIPPED (one-sentence scope)."

**Full scope:**

**3a. Brainstorm.** Invoke `/brainstorming` with the task description. One round — refine the idea, confirm constraints, explore 2-3 approaches.

**3b. Write plan.** Write a plan to `ai-workspace/plans/<name>.md` using the template at `ai-workspace/plans/TEMPLATE.md`. Fill all template fields including:
- Branch, created date, status
- Threat model (advisory or adversarial)
- Scope ceiling
- Task description and scope
- Steps with checkboxes (include files to create/modify and testing strategy)
- Confidence scaffold (recommended for adversarial threat models)

Do NOT review the plan here — that's Step 4.

### Step 4 — Review Plan

**No plan (one-sentence scope):** SKIP — proceed to Step 5.

**Has plan:**

Run `/review` against the plan file (Codex: read `.agents/skills/review/SKILL.md` and follow manually).
- Auto-assemble the plan review panel:
  - Always: `technical-editor`
  - Code architecture: add `architect-reviewer`
  - AGENTS.md / config.toml / sync.sh / skills: add `codex-specialist`
  - Auth / credentials / permissions: add `security-auditor`
  - UI / component / CSS: add `ui-designer`
- Gate: P2 (fix P0-P2, record P3+)
- Cap: 3 rounds

On APPROVE: proceed to Step 5.
On ESCALATE after 3 rounds: stop and present unresolved findings to human.

### Step 5 — Build

**5a. Implement.**

With plan: read the plan, execute each task.
- Claude Code: use subagents for independent tasks — `implementer` (Sonnet) for code, `test-writer` (Sonnet) for tests. Parallel dispatch when tasks are independent.
- Codex/Cursor: execute sequentially in the main session.

Without plan (one-sentence / hotfix): implement directly.
- TDD: write the failing test first (RED), then fix (GREEN), then refactor
- Minimal change principle for hotfixes — fix the defect, nothing else
- Document root cause in commit message body for hotfixes

**5b. Validate (gate for Step 6).**

Run `pnpm validate` (typecheck + lint + format:check + test:all). This is a hard gate — read the output. Never claim success without evidence. If it fails, fix and re-run until green. Step 6 cannot begin until this passes.

### Step 6 — Review Build

Run `/review` against the changed files (`git diff main...HEAD`) (Codex: read `.agents/skills/review/SKILL.md` and follow manually).
- Auto-assemble the **code** review panel (differs from Step 4's plan panel):
  - Always: `code-reviewer`
  - Code architecture: add `architect-reviewer`
  - AGENTS.md / config.toml / sync.sh / skills: add `codex-specialist`
  - Auth / credentials / permissions: add `security-auditor`
  - UI / component / CSS: add `design-reviewer`
- Gate: P2
- Cap: 3 rounds

On APPROVE: proceed to Step 7.
On ESCALATE: stop and present unresolved findings to human.

### Step 7 — Archive

**Has plan:**

Invoke `/archive` (Codex: fill Outcomes & Learnings in plan file, rename to `.done.md`). It fills Outcomes & Learnings in the plan file and renames to `.done.md`.

**No plan (hotfix / one-sentence):**

Ensure root cause or change rationale is documented in the commit message body. No plan file to archive.

### Step 8 — Ship

Get the code onto main remote. Two paths:

**CI detection:** Check `gh run list --limit 3` for recent workflow status, or check if the repo has active GitHub Actions workflows. If unknown, assume CI is up.

**CI up (default):**

Create a PR and arm auto-merge:
```bash
gh pr create --title "<conventional-commit-title>" --body "<summary>"
gh pr merge --auto --merge
```
The CI review pipeline handles the rest.

**CI down:**

Local merge to main:
```bash
git fetch origin main
git checkout main
git merge <feature-branch>
git push origin main
```
Run from a temp worktree or ephemeral clone — NOT the primary worktree. Clean up the feature worktree after merge.

**Both paths:**

When files touched include AGENTS.md, config.toml, sync.sh, or skills → `codex-specialist` must be in the review panel (enforced at Step 6).

### Step 9 — Reflect

Invoke `/reflect` (Codex: read `.agents/skills/reflect/SKILL.md`). It handles:
- Reading `.branch-context.md` for session learnings
- Writing to `MEMORY.md` on main
- Filing follow-up issues if needed
- Cleaning up branch artifacts

## Agent Teams

> Claude Code only. Codex and Cursor do not support Agent Teams or MCP servers.

When teammates are available (session started with teammate mode):

- Teammates CANNOT spawn sub-agents or load MCP servers
- One task per teammate (self-contained)
- Cost: ~15x solo — start with 2 max
- Solo with subagents for sequential steps on one feature
- Agent Teams for independent features (one per worktree)

Steps can be split across teammates for large work:
- **Plan:** each teammate plans a piece using `/task`, orchestrator assembles before Step 4
- **Build:** each teammate builds a piece, orchestrator coordinates before Step 6
- The orchestrator runs Steps 4, 6, 7, 8, 9 from the main thread

## Bail

Invoke `/bail` at any step to abort cleanly. It handles: learnings capture to `.branch-context.md`, issue update, PR close if open, worktree cleanup. Bail replaces Step 9 (Reflect) — it captures learnings itself. Clean up any open task list items.
