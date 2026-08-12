---
name: git-commit
description: Git rules for safe staging, the commit message format, never-allowed commands, and rebase-conflict handling. Read before any commit, merge, or rebase.
---

# Git

Multiple sessions may be running in this cwd at the same time, each modifying different files. Git operations that touch unstaged, staged, or untracked files outside your own changes will stomp on other sessions' work.

## Committing

1. Run `git status` and verify you are only staging files you changed in THIS session. Continue once every changed path is accounted for as yours or unrelated to your session.
2. Stage explicit paths (`git add <path1> <path2>`); never `git add -A` / `git add .`. Continue once the index holds all and only your session's files.
3. Commit with the Conventional Commits format `<type>[(scope)]: <commit message>` (optionally multiple lines) — informative and concise. Continue once the commit exists, its message matches the format, and no check was bypassed.
4. Squash merges: pass an explicit subject in the same format (`gh pr merge --squash --subject "..."`). Continue once the merge used the passed subject.

## Never run

`git reset --hard`, `git checkout .`, `git clean -fd`, `git stash`, `git add -A`, `git add .`, `git commit --no-verify` — these destroy other agents' work or bypass checks. Where a positive exists, use it: stage explicit paths, commit with hooks enabled.

## Rebase conflicts

If rebase conflicts occur:

- Resolve conflicts only in files you modified.
- If a conflict is in a file you did not modify, abort and ask the user.
- Never force push.
