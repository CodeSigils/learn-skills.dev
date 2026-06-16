---
name: sync
description: Use when the user asks to sync with remote, pull latest changes, or run /sync; runs git pull on main with pre-pull status checks and safe conflict handling.
---

# Purpose

Reusable workflow for pulling the latest changes from the remote repository.

# Required Knowledge

- `AGENTS.md`
- `ai-workspace/40-tasks/checklist.md`

# Branch Rule

- Use `main` only.
- Do not create or switch branches unless the user explicitly asks.
- Do not force pull or rewrite history.

# Inputs

- optional remote name (default: `origin`)
- optional branch name (default: current branch, expected `main`)

# Workflow

1. Run `git status --short`.
2. Confirm the current branch is `main`.
3. If there are uncommitted changes, report them and stop unless the user explicitly approves pulling with a dirty worktree.
4. Run `git fetch origin`.
5. Run `git pull origin main` (or `git pull` when already on `main` tracking `origin/main`).
6. If merge conflicts occur, stop and report conflicted files; do not auto-resolve unless the user explicitly requests it.
7. Run `git status --short` and `git log -3 --oneline` after a successful pull.
8. Summarize what changed (files/commits pulled).

# Safety Rules

- Never run `git reset --hard`.
- Never run `git checkout --` to discard local changes unless explicitly requested.
- Never force pull (`git pull --rebase` with force, `git fetch --force`, etc.) unless explicitly requested.
- Never stash or drop user changes without explicit approval.
- If pull fails due to local commits diverging, report the situation and ask before rebasing or merging manually.

# Output

- current branch
- pull result (success, up to date, or failure)
- commits pulled (if any)
- post-pull `git status --short`
- unresolved conflicts or blocked local changes, if any

# Verification

- Current branch confirmed as `main` before pull.
- `git pull` completed successfully or failure reason is reported.
- Post-pull status and recent commits are shown.
