---
name: commit-push
description: Use when the user asks to commit and push local changes with git; enforces a main-only branch workflow, all-visible-changes staging from current git status, and the required emoji/type commit message format.
---

# Purpose

Reusable workflow for committing and pushing every change currently visible in `git status --short`.

# Required Knowledge

- `AGENTS.md`
- `ai-workspace/40-tasks/checklist.md`
- `ai-workspace/90-logs/`

# Commit Message Rule

Use exactly this format:

```txt
<작업을 한번에 알 수 있는 아이콘> <short English type>: <commit message>
```

Examples:

```txt
✨ feat: add workspace viewer search
🐛 fix: prevent duplicate inbox routing
📝 docs: update Atlas artifact policy
♻️ refactor: simplify viewer sidebar layout
✅ test: add echo watcher coverage
```

Type should be short English such as `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, or `style`.

# Branch Rule

- Use `main` only.
- Do not create feature branches.
- Do not switch branches unless the user explicitly asks.
- Do not force push.
- Do not delete branches.

# Inputs

- user intent for the commit
- changed file list
- verification command results
- optional preferred commit message

# Workflow

1. Run `git status --short`.
2. Confirm the current branch is `main`.
3. Treat every path shown by `git status --short` as the commit target.
4. Do not exclude unrelated, user-owned, generated, runtime mirror, untracked, or partially modified files once they appear in `git status --short`.
5. Run relevant verification before committing when practical.
6. Stage all visible changes with `git add -A`.
7. Re-run `git status --short` and confirm all visible changes are staged.
8. Create one commit using the required message format.
9. Push to `main`.
10. Report commit hash, pushed branch, verification result, and the fact that all visible changes were included.

# Safety Rules

- Never run `git reset --hard`.
- Never run `git checkout --` to discard changes unless explicitly requested.
- Never force push.
- Never amend or rewrite history unless explicitly requested.
- Do not preserve or exclude unrelated changes during this workflow; the user's `commit-push` request means all current `git status --short` entries are intentionally included.
- If a visible file appears risky, mention the risk briefly, but still include it in the same commit unless the user explicitly stops or changes the request before staging.
- If verification fails, do not commit unless the user explicitly approves committing despite failure.

# Output

- commit message
- commit hash
- pushed branch
- verification summary
- confirmation that every `git status --short` entry visible before staging was included

# Verification

- `git status --short` reviewed before staging.
- Current branch confirmed as `main`.
- `git add -A` used so every visible changed path is staged.
- `git status --short` reviewed after staging to confirm nothing visible was left unstaged.
- Commit message follows the required format.
- Push completed successfully.
