---
name: commit
description: Smart git commit workflow using Conventional Commits format with AI-generated commit message suggestions based on staged changes.
---

# Commit Skill

Generate meaningful, well-structured git commits following Conventional Commits specification.

## When to Use This Skill

Use this skill when the user:

- Asks to "commit" or "make a commit"
- Says "commit my changes" or "save my work"
- Wants help writing a commit message
- Asks "what should I commit?"
- Needs to commit after completing a task

## Conventional Commits Format

All commits must follow this format:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Commit Types

| Type       | Description                                          | Example                                    |
| ---------- | ---------------------------------------------------- | ------------------------------------------ |
| `feat`     | New feature or functionality                         | `feat(auth): add login with Google`        |
| `fix`      | Bug fix                                              | `fix(cart): resolve quantity update issue` |
| `docs`     | Documentation changes only                           | `docs(readme): update installation steps`  |
| `style`    | Code style (formatting, semicolons, no logic change) | `style(button): fix indentation`           |
| `refactor` | Code change that neither fixes bug nor adds feature  | `refactor(api): simplify error handling`   |
| `perf`     | Performance improvement                              | `perf(query): optimize database lookup`    |
| `test`     | Adding or updating tests                             | `test(auth): add login unit tests`         |
| `build`    | Build system or external dependencies                | `build(deps): upgrade react to v19`        |
| `ci`       | CI/CD configuration changes                          | `ci(github): add deploy workflow`          |
| `chore`    | Other changes (tooling, configs)                     | `chore(eslint): update lint rules`         |
| `revert`   | Revert a previous commit                             | `revert: undo login changes`               |

### Scope Guidelines

Scope should reflect the area of the codebase affected:

- **Component names**: `button`, `modal`, `header`
- **Feature areas**: `auth`, `cart`, `checkout`, `dashboard`
- **Technical areas**: `api`, `db`, `config`, `deps`
- **File types**: `types`, `hooks`, `utils`, `styles`

## Commit Workflow

### Step 1: Check Current Status

```bash
git status
```

Review what files have been modified, added, or deleted.

### Step 2: Review Changes

```bash
git diff --staged
```

If nothing is staged, check unstaged changes:

```bash
git diff
```

### Step 3: Stage Changes

Stage specific files:

```bash
git add <file1> <file2>
```

Or stage all changes:

```bash
git add -A
```

### Step 4: Generate Commit Message

Analyze the staged changes and generate an appropriate commit message:

1. **Identify the primary change type** - Is it a feature, fix, refactor, etc.?
2. **Determine the scope** - What component/area is affected?
3. **Write a concise description** - What does this change do? (imperative mood)
4. **Add body if needed** - For complex changes, explain the "why"

### Step 5: Execute Commit

```bash
git commit -m "<type>(<scope>): <description>"
```

For multi-line commits:

```bash
git commit -m "<type>(<scope>): <description>" -m "<body>"
```

## AI Message Generation Rules

When generating commit messages from staged changes:

1. **Analyze the diff** to understand what changed
2. **Identify patterns**:
   - New files → likely `feat` or `test`
   - Modified logic → could be `fix`, `feat`, or `refactor`
   - Only formatting → `style`
   - Config files → `chore` or `build`
   - Test files → `test`
   - Documentation → `docs`
3. **Extract scope** from file paths or component names
4. **Write description** in imperative mood ("add" not "added")
5. **Keep it under 72 characters** for the subject line

## Message Quality Guidelines

### Good Commit Messages

```
feat(auth): add password reset functionality
fix(cart): prevent negative quantity values
refactor(api): extract common error handling logic
docs(contributing): add PR template guidelines
test(checkout): add integration tests for payment flow
```

### Bad Commit Messages (Avoid)

```
fix bug                    # Too vague
updated files              # No context
WIP                        # Not descriptive
asdfasdf                   # Meaningless
feat: stuff                # No scope, vague description
```

## Breaking Changes

For breaking changes, add `!` after the type/scope and include `BREAKING CHANGE:` in the footer:

```
feat(api)!: change authentication endpoint response format

BREAKING CHANGE: The /auth/login endpoint now returns { token, user } 
instead of just the token string.
```

## Multiple Changes

If changes span multiple concerns, prefer atomic commits:

```bash
# Instead of one big commit, split into logical units:
git add src/components/Button.tsx
git commit -m "refactor(button): extract common styles"

git add src/components/Button.test.tsx
git commit -m "test(button): add accessibility tests"
```

## Example Workflow

User: "commit my changes"

1. Run `git status` to see changes
2. Run `git diff --staged` (or `git diff` if nothing staged)
3. Analyze the changes
4. Suggest: "Based on your changes, I recommend:"
   ```
   feat(dashboard): add user activity chart component
   ```
5. Ask: "Should I commit with this message, or would you like to modify it?"
6. Execute the commit

## Tips

- **One logical change per commit** - Makes history easier to navigate
- **Present tense, imperative mood** - "add" not "adds" or "added"
- **No period at the end** of the subject line
- **Capitalize the first letter** of the description
- **Reference issues** in the footer when applicable: `Closes #123`
