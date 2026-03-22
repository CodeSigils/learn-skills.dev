---
name: commit-message
description: Generate a conventional commit message from staged or recent changes. Use when the user asks for a commit message, wants to commit, or says "give me a commit message".
---

# Generate Conventional Commit Message

## What This Does

Analyzes the current git changes and produces a conventional commit message with type, scope, and bullet-point body. Prints the message only — does not run `git commit`.

## Steps

### 1. Read the changes

Run `git diff --staged` first. If nothing is staged, fall back to `git diff HEAD`. Also run `git status` to understand the full picture of what changed.

### 2. Determine the type

Choose exactly one:

| Type       | When to use                                                    |
|------------|----------------------------------------------------------------|
| `feat`     | New feature or capability visible to the user                  |
| `fix`      | Bug fix                                                        |
| `refactor` | Code restructure with no behavior change                       |
| `style`    | Formatting, whitespace, visual-only changes                    |
| `perf`     | Performance improvement                                        |
| `docs`     | Documentation only                                             |
| `test`     | Adding or updating tests                                       |
| `chore`    | Build scripts, config, tooling, deps — nothing in src         |
| `ci`       | CI/CD pipeline changes                                         |
| `revert`   | Reverting a previous commit                                    |

If the change clearly spans two types (e.g. `fix` + `refactor`), pick the one that best represents the intent. Do not combine types.

### 3. Determine the scope

The scope is a **feature area**, not a file or component name. Derive it from what area of the product is affected:

Examples: `a11y`, `gtd`, `reading-list`, `activity-feed`, `milestones`, `auth`, `db`, `api`, `ui`, `nav`, `editor`

- Use `kebab-case`
- Keep it short (1–2 words max)
- Omit the scope entirely if the change is truly cross-cutting (e.g. a global config change)

### 4. Write the subject line

Format: `type(scope): short description`

Rules:
- Imperative mood: "add", "fix", "remove" — not "added", "fixes", "removing"
- No capital letter after the colon
- No period at the end
- Max 72 characters total
- Describe **what** the change does, not **how**

### 5. Write the body

- Blank line between subject and body
- Bullet points (`-`) only — no prose paragraphs
- Each bullet explains **why** the change was made or **what problem** it solves — not just what the code does
- Be specific: reference function names, component names, or behaviors where helpful
- 3–6 bullets is usually right; use fewer for small changes, more for complex ones

### 6. Add footer (only when needed)

Add a footer only for:
- **Breaking changes**: `BREAKING CHANGE: description of what breaks and how to migrate`
- **Reverts**: `Reverts: <original commit subject>`

Do not add footers for normal changes.

### 7. Output

Print the final message in a single fenced code block so it can be copied directly:

```
type(scope): short description

- why this change was needed
- what problem it solves or what it improves
- any non-obvious decisions made
```

Do not explain the message or add commentary outside the code block unless there is genuine ambiguity to flag.
