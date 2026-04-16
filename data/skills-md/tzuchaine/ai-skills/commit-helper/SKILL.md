---
name: commit-helper
description: Intelligently analyze code changes and split them into multiple logical commits based on functionality and change types. This skill should be used when users want to commit code changes, especially when there are multiple unrelated changes in the working directory.
---

# Commit Helper

## Overview

This skill helps create well-structured atomic commits by analyzing all code changes and intelligently splitting them into multiple logical commits. Each commit should be focused, related, and follow best practices.

## When to Use

- When users request "commit my changes", "commit code", or similar requests
- When there are multiple unrelated changes in the working directory

## Workflow

Execute the following steps in order:

### Step 1: Analyze Changes

1. Run `git status` to view all changed files
2. Run `git diff` to understand the nature of changes
3. Analyze changes to identify:
   - Which files belong to the same module/directory
   - Which files implement the same functionality
   - What type of change each file represents (feat, fix, refactor, docs, etc.)
   - Dependencies between files

### Step 2: Group Changes

Split changes into multiple logical commits based on the following criteria:

**Primary Grouping Criteria:**
- **Functional cohesion**: Files implementing the same functionality or solving the same problem are grouped together
- **Change type**: Separate different types (feat, fix, refactor, docs, test, chore) into different commits when possible

**Grouping Rules:**
- Each commit should represent one logical change
- Related files (even in different directories) that implement one functionality should be in the same commit
- Bug fixes should be separate from new features
- Refactoring should be separate from feature additions
- Test files should be grouped with the code they test
- Documentation updates can be committed separately unless directly related to a specific feature

**Grouping Examples:**
```
Commit 1 (feat): User Authentication
  - src/auth/login.ts
  - src/auth/middleware.ts
  - src/routes/auth.ts
  - tests/auth.test.ts

Commit 2 (fix): Profile validation bug
  - src/user/profile.ts
  - tests/user.test.ts

Commit 3 (refactor): Error handling
  - src/utils/errors.ts
  - src/middleware/errorHandler.ts
  - Multiple files using the new error handling
```

### Step 3: Generate Commit Messages

Generate commit messages following **Conventional Commits** specification for each commit group:

**Format:**
```
type(scope): brief description

Detailed explanation of why this change was made.
What problem was solved? What was the previous behavior?
How does this change improve the codebase?
```

**Type Options:**
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Refactoring code without changing functionality
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `chore`: Maintenance tasks (dependencies, configs, etc.)
- `perf`: Performance improvements
- `style`: Code style/formatting changes
- `ci`: CI/CD changes

**Scope Examples:**
- Module names: `auth`, `user`, `api`, `database`
- Component names: `LoginForm`, `ProfilePage`
- Domains: `validation`, `error-handling`, `logging`

**Message Guidelines:**
- Subject line (first line): Max 72 characters, use imperative mood ("add" not "added")
- Body: Explain why, not what (the diff shows what)
- Body should be 2-4 sentences providing context
- Leave a blank line between subject and body

**Example:**
```
feat(auth): add JWT-based authentication system

Implemented complete authentication system using JWT tokens to replace
the previous session-based approach. This provides better scalability
for our API and supports stateless authentication across multiple servers.
```

### Step 4: Present Plan to User

Display the proposed commit plan in this format:

```
🔍 Analyzed X files with changes

💡 Proposed commit plan:

【Commit 1/N】type(scope): description
  Files:
  ├─ path/to/file1.ts
  ├─ path/to/file2.ts
  └─ path/to/file3.ts

  Commit message:
  type(scope): brief description

  Detailed body explaining why...

【Commit 2/N】type(scope): description
  Files:
  ├─ path/to/file4.ts
  └─ path/to/file5.ts

  Commit message:
  type(scope): brief description

  Detailed body explaining why...

---
⚠️  Next: Code quality checks (linter + type checking)

Do you approve this commit plan? (yes/no/adjust)
```

Use the AskUserQuestion tool to wait for user confirmation before continuing.

### Step 5: Run Code Quality Checks

Before committing, run these checks:

1. **Linter Check**:
   - Try to detect the project's linter (eslint, prettier, ruff, etc.)
   - Run the appropriate lint command
   - Common commands: `npm run lint`, `eslint .`, `prettier --check .`

2. **Type Check** (if applicable):
   - For TypeScript: `tsc --noEmit` or `npm run type-check`
   - For Python: `mypy .` or similar tools
   - For other languages: appropriate type checkers

**If checks fail:**
- Clearly display errors
- Use AskUserQuestion to ask: "Code quality checks failed. Do you want to: 1) Fix issues and retry, 2) Commit anyway, 3) Cancel"
- Respect the user's choice

**If checks pass:**
- Notify user and proceed to commit

### Step 6: Execute Commits

For each commit group in the plan:

1. Stage only the files for this commit:
   ```bash
   git add file1 file2 file3
   ```

2. Create commit with the generated message:
   ```bash
   git commit -m "$(cat <<'EOF'
   type(scope): brief description

   Detailed body explaining the change and its rationale.
   Additional context if needed.
   EOF
   )"
   ```

3. Verify the commit was created successfully

**Important Rules:**
- Execute commits sequentially, not in parallel
- After each commit, confirm it succeeded before proceeding to the next
- Do not automatically push to remote - only create local commits
- Do not use `git add -A` or `git add .` - selectively stage files for each commit

### Step 7: Summary

After creating all commits, display a summary:

```
✅ Successfully created N commits:

1. abc1234 - feat(auth): add JWT authentication
2. def5678 - fix(user): fix profile validation
3. ghi9012 - refactor(api): improve error handling

All changes committed locally.
Use 'git push' to push to remote when ready.
```

## Important Notes

- **Never auto-push**: Always commit locally only, let users manually push
- **Atomic commits**: Each commit should be independently buildable and testable
- **Clear messages**: Focus on why in the commit body, not what
- **User control**: Always show plan and get approval before executing
- **Quality first**: Run checks before committing, but respect user's decision
- **Don't mix**: Don't mix refactoring with features, or fixes with new features

## Example Session

```
User: Please commit my code

Claude: 🔍 Analyzing code changes...

[Runs git status and git diff]

🔍 Analyzed 8 files with changes

💡 Proposed commit plan (3 commits):

【Commit 1/3】feat(auth): implement user login system
  Files:
  ├─ src/auth/login.ts (new file)
  ├─ src/auth/types.ts (modified)
  ├─ src/routes/auth.ts (new file)
  └─ tests/auth/login.test.ts (new file)

  Commit message:
  feat(auth): implement user login system

  Added JWT-based login functionality with email/password authentication.
  Includes token generation, validation middleware, and complete test coverage.

【Commit 2/3】fix(validation): correct email regex
  Files:
  ├─ src/utils/validation.ts (modified)
  └─ tests/utils/validation.test.ts (modified)

  Commit message:
  fix(validation): correct email regex

  Fixed email validation regex to properly handle plus signs and subdomains.
  The previous regex would reject valid emails like user+tag@subdomain.example.com.

【Commit 3/3】docs(readme): update installation instructions
  Files:
  └─ README.md (modified)

  Commit message:
  docs(readme): update installation instructions

  Updated setup guide to include new environment variables needed for
  authentication system. Added troubleshooting section for common JWT
  configuration issues.

---
⚠️  Next: Code quality checks (linter + type checking)

Do you approve this commit plan?

User: Yes

Claude: ✅ Plan approved. Running code quality checks...

[Runs npm run lint]
✅ Linter passed

[Runs npm run type-check]
✅ Type check passed

Creating commits...

✅ Commit 1/3: feat(auth) - abc1234
✅ Commit 2/3: fix(validation) - def5678
✅ Commit 3/3: docs(readme) - ghi9012

✅ Successfully created 3 commits:

1. abc1234 - feat(auth): implement user login system
2. def5678 - fix(validation): correct email regex
3. ghi9012 - docs(readme): update installation instructions

All changes committed locally.
Use 'git push' to push to remote when ready.
```

## Advanced Scenarios

### Handling Large Change Sets

If more than 20 files changed:
- Group more aggressively by top-level modules
- Limit to maximum 5 commits for readability
- Prioritize logical grouping over perfect atomicity

### Mixed Changes in Single File

If a single file has multiple unrelated changes:
- Notify user that the file has mixed changes
- Suggest using `git add -p` for partial staging if appropriate
- Group the entire file with the most significant change

### Configuration Files

For package.json, package-lock.json, poetry.lock, etc.:
- Group with the commit that requires the dependency change
- If it's a standalone dependency update, create a separate `chore(deps)` commit

### Generated Files

For build output, compiled files:
- Warn user that these might not should be committed
- Ask if they want to exclude them
- Respect .gitignore patterns

## Error Handling

### No Changes Detected
```
ℹ️  No changes detected in working directory.
Nothing to commit, working tree clean.
```

### All Files Already Staged
```
ℹ️  All changes are already staged.
Do you want to continue with the current staging area, or reset and let
me reorganize commits? (continue/reorganize)
```

### Commit Failed
```
❌ Failed to create commit: [error message]

This might be due to:
- Pre-commit hook rejected the commit
- Invalid file permissions
- Git configuration issue

Please resolve the issue and try again.
```

## Tips for Users

- Run this skill regularly to maintain clean commit history
- The more detailed your code comments, the better the commit messages
- Review the plan carefully - adjust grouping if needed
- Keep working directory focused on related changes for best results
