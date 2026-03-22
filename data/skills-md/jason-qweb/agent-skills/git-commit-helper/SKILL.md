---
name: git-commit-helper
description: Generate clear, conventional commit messages from staged changes. Use when the user asks to commit or needs a commit message.
---

# Git Commit Helper

You help write high-quality commit messages following the Conventional Commits specification.

## Steps

1. Run `git diff --cached` to see staged changes.
2. Analyze what changed and why.
3. Write a commit message in this format:

```
<type>(<scope>): <short summary>

<body - explain what and why, not how>
```

## Types

- `feat`: new feature
- `fix`: bug fix
- `docs`: documentation only
- `refactor`: code change that neither fixes a bug nor adds a feature
- `test`: adding or updating tests
- `chore`: build process, dependencies, CI changes

## Rules

- Summary line must be under 72 characters.
- Use imperative mood: "add feature" not "added feature".
- Body should explain motivation and contrast with previous behavior.
- If the change is trivial (typo fix, formatting), keep it to one line.
- Reference issue numbers when applicable: `Fixes #123`.
