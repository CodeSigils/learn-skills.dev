---
name: git-commit
description: Creates well-formatted, meaningful git commit messages following conventional commits and industry best practices. Use when committing changes, creating commits, writing commit messages, or managing version control history.
---

# Git Commit Best Practices

## Overview

This skill provides guidelines for creating clear, consistent, and meaningful git commit messages that improve project history, facilitate code reviews, and enable better collaboration.

## Conventional Commits Format

Use the following structure for commit messages:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Required: Type and Subject

```
<type>: <subject>
```

### Common Commit Types

- **feat**: A new feature for the user
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that don't affect code meaning (formatting, whitespace, etc.)
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **perf**: Performance improvement
- **test**: Adding or updating tests
- **chore**: Changes to build process, dependencies, or tooling
- **ci**: Changes to CI/CD configuration
- **build**: Changes to build system or dependencies
- **revert**: Reverts a previous commit

### Optional: Scope

Specify the area of the codebase affected:

- Component name: `feat(menu): add filtering functionality`
- Module name: `fix(auth): resolve token expiration issue`
- File/folder: `docs(README): update installation instructions`

## Subject Line Rules

1. **Character limit**: Keep under 50 characters (hard limit: 72)
2. **Imperative mood**: Use "Add" not "Added" or "Adds"
3. **No period**: Don't end with a period
4. **Capitalization**: Start with a capital letter
5. **Be specific**: Clearly describe what the commit does

### Good Examples

```
feat: add user authentication with JWT
fix: resolve null pointer in order processing
docs: update API endpoint documentation
refactor: simplify customer validation logic
test: add unit tests for Comanda service
```

### Bad Examples

```
✗ Updated stuff                    (vague, past tense)
✗ fixed bug                        (not capitalized, no type)
✗ feature: adding new things.      (period, not imperative)
✗ This commit adds a really long description that exceeds the character limit  (too long)
```

## Commit Body (Optional but Recommended)

Add a blank line after the subject, then provide:

- **Why**: Explain the reason for the change
- **What**: Describe what changed (if not obvious)
- **How**: Detail the approach taken (for complex changes)
- **Context**: Background information or related issues

```
feat(menu): add real-time inventory tracking

Implements WebSocket connection to update product availability
in real-time as orders are processed. This prevents customers
from ordering out-of-stock items.

- Connects to inventory service via WebSocket
- Updates producto.disponibal field automatically
- Shows "Out of Stock" badge in menu UI

Resolves #142
```

## Footer (Optional)

Use for:

- **Breaking changes**: `BREAKING CHANGE: description`
- **Issue references**: `Fixes #123`, `Closes #456`, `Refs #789`
- **Reviewed by**: `Reviewed-by: Name <email>`
- **Co-authors**: `Co-authored-by: Name <email>`

```
fix(comanda): change status validation logic

BREAKING CHANGE: ComandaStatusEnum values changed from uppercase
to titlecase. Update any hardcoded status references.

Fixes #234
```

## Atomic Commits

Each commit should represent **one logical change**:

✓ **Good**: Separate commits for separate changes

```
git commit -m "feat(produto): add category filtering"
git commit -m "fix(comanda): correct subtotal calculation"
git commit -m "docs: update setup instructions"
```

✗ **Bad**: Multiple unrelated changes in one commit

```
git commit -m "add features, fix bugs, update docs"
```

## Project-Specific Guidelines

### For StreetBite/SnackinBack

Given the bilingual context (code in Portuguese, comments/docs may vary):

**Accepted subject languages**:

- **Portuguese** (preferred for domain concepts): `feat(comanda): adicionar validação de pagamento`
- **English**: `feat(comanda): add payment validation`

**Consistency**: Choose one language per commit message

**Scope examples**:

- `comanda`, `produto`, `cliente`, `endereco`, `item`
- `controller`, `service`, `repository`, `dto`
- `frontend`, `backend`, `api`
- `menu`, `orders`, `requests`, `settings`

### Common Scenarios

**Adding a new feature**:

```
feat(menu): add category filter dropdown

Allows users to filter products by categoria (BEBIDA, LANCHE,
COMBO, ACOMPANHAMENTO). Implemented in menu.js with dynamic
button generation.
```

**Fixing a bug**:

```
fix(comanda): calculate correct subtotal with items

Fixed getTotalComanda() to properly sum all item totals.
Previously returned null when items list was empty.

Fixes #78
```

**Refactoring code**:

```
refactor(service): extract comanda validation logic

Moved status validation from controller to service layer
for better separation of concerns and reusability.
```

**Updating dependencies**:

```
chore(deps): upgrade Spring Boot to 3.4.2

Security patch for CVE-2024-XXXXX
```

**Documentation**:

```
docs(AGENTS): add frontend API conventions

Documents ApiService usage pattern and CORS requirements
for frontend-backend communication.
```

## Commands for Creating Commits

### Stage and commit

```bash
# Stage specific files
git add path/to/file

# Stage all changes
git add .

# Interactive staging
git add -p

# Commit with inline message (short commits)
git commit -m "feat(scope): description"

# Commit with detailed message (opens editor)
git commit

# Amend last commit (change message or add files)
git commit --amend
```

### Review before committing

```bash
# See what's staged
git diff --cached

# See status
git status

# Review changes
git log --oneline -n 5
```

## Multi-line Commits in Command Line

```bash
git commit -m "feat(menu): add search functionality" \
-m "" \
-m "Implements real-time search across product names and descriptions." \
-m "Uses debouncing to optimize API calls during typing." \
-m "" \
-m "Closes #156"
```

## Tips for Writing Great Commits

1. **Commit often**: Small, focused commits are easier to review and revert
2. **Test before committing**: Ensure code compiles and tests pass
3. **Review your diff**: Check what you're committing with `git diff --cached`
4. **Use feature branches**: Keep main/develop branch stable
5. **Write for your future self**: You'll read this message later
6. **Be honest**: Don't hide mistakes; explain fixes clearly
7. **Link to issues**: Connect commits to project management tools

## Bad Practices to Avoid

- ✗ `git commit -m "fix"` (too vague)
- ✗ `git commit -m "WIP"` (don't commit incomplete work to main)
- ✗ `git commit -m "asdfgh"` (meaningless)
- ✗ `git commit -m "fixed the thing that was broken"` (no type, vague)
- ✗ Committing directly to main without review
- ✗ Mixing multiple unrelated changes
- ✗ Including commented-out code or debug statements
- ✗ Committing generated files (build artifacts, node_modules, etc.)

## Recommended Workflow

1. **Make changes** to implement one logical feature/fix
2. **Test locally** to ensure it works
3. **Review changes**: `git status` and `git diff`
4. **Stage changes**: `git add <files>`
5. **Write commit message** following this skill's guidelines
6. **Commit**: `git commit`
7. **Repeat** for next logical change

## References

- [Conventional Commits](https://www.conventionalcommits.org/)
- [How to Write a Git Commit Message](https://chris.beams.io/posts/git-commit/)
- [Angular Commit Guidelines](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit)

---

**When invoked**: Use these guidelines to help users create well-structured commit messages, review commit history, or improve their git workflow.
