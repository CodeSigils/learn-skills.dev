---
name: conventional-commits
description: Create git commits using Conventional Commits with scoped, reviewable changes. Use when the user asks to commit changes, make a conventional commit, write a commit message, or prepare staged changes for commit.
---

# Conventional Commits

## Flow

1. Inspect: `git status --short`, `git diff --stat`, `git diff`, `git diff --staged`.
2. Decide what belongs in this commit.
3. Stage only those files or hunks.
4. Message: `type(scope): summary`.
5. Description: add a short body after the summary when possible, explaining what changed and why.
6. Commit non-interactively: `git commit -m "type(scope): summary" -m "Description."`.

Use the second `-m` paragraph whenever there is enough useful context. Skip it only for trivial commits where the summary fully explains the change.

## Message

Format: `type(scope): summary`

Types, lowercase:

- `feat`: new user/product capability
- `fix`: bug fix
- `docs`: docs only
- `style`: formatting only
- `refactor`: restructure, no behavior change
- `perf`: speed/resource improvement
- `test`: tests only
- `build`: build/deps/package changes
- `ci`: CI config
- `chore`: maintenance
- `revert`: undo a commit

Scope when useful: `api`, `ui`, `auth`, `deps`, `docs`, package name. Skip vague scopes.

Summary: imperative, specific, about 72 chars or less, no ending punctuation.

Good:

- `feat(auth): add passkey registration`
- `fix(api): reject expired invite tokens`
- `docs: document local setup`

## Safety

- Leave unrelated user changes alone.
- If related and unrelated edits share a file, inspect and stage hunks only.
- No destructive git commands unless user explicitly asked.
- If hooks change files, inspect the new diff before retrying.

## Staging

- Clean related files: `git add path/to/file`.
- Mixed files: `git add -p path/to/file`.
- Verify staged work: `git diff --staged --stat`, then `git diff --staged`.

## Body / Description

Prefer a short body after the summary when it adds useful context. Describe what changed and why; avoid restating the summary.

```sh
git commit \
  -m "fix(cache): prevent stale workspace reads" \
  -m "Invalidate cached workspace metadata when the selected account changes."
```

## Breaking Changes

Use `!` plus footer only when callers, users, stored data, or deploy expectations must change:

```text
feat(api)!: rename token exchange endpoint

BREAKING CHANGE: /token/exchange is replaced by /oauth/token.
```
