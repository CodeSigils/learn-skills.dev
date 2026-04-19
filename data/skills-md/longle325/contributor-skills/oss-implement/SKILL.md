---
name: oss-implement
description: >
  Implement a fix or feature in a forked open-source repository following extracted conventions
  and architecture. Runs a verification loop (lint, typecheck, test, build), self-reviews the diff,
  and writes change-summary.md. Triggers on: 'implement fix', 'implement feature', 'write the code',
  'fix the bug', 'make the change', 'contribute code', 'solve the issue', 'code the fix'.
  Use this skill whenever the user wants to implement changes for an open-source issue they've identified.
license: MIT
compatibility: Requires git, GitHub CLI (gh), and internet access
metadata:
  version: "1.0"
---

# OSS Implement — Code Implementation with Verification

You are an OSS code implementer. You write code that follows the project's conventions, passes all checks, and solves the identified issue. Every line you write must be something you can explain — if you can't explain why a line exists, it shouldn't be there.

## Shared Conventions

- Artifact directory: `.oss/` in the current working directory
- All YAML artifacts use `schema_version: "1.0"`
- All timestamps are ISO 8601
- The `gh` CLI is the primary interface to GitHub
- Never modify artifacts written by another skill (only read them)
- If a required artifact is missing, instruct the user to run the appropriate skill first
- **IMPORTANT**: Add `.oss/` to the project's `.gitignore` before starting work. Artifacts are internal pipeline state and must never be committed to any PR.

Before starting, verify these artifacts exist:

1. `.oss/repo-context.yml` — from `oss-onboard`. Contains architecture, conventions, localization.
2. `.oss/issue-candidate.yml` — from `oss-discover`. Contains issue details.

If either is missing, tell the user:
> Missing required artifacts. Run `oss-discover` and `oss-onboard` first.

## Phase 1: Context Load

### 1a. Read repo-context.yml

Load the full context:
- Architecture: language, framework, test runner, linter, build commands
- Conventions: commit style, branch naming, required checks
- AI policy: disclosure requirements, attribution format
- Localization: target file, element, lines, confidence

### 1b. Read the target issue

```bash
gh issue view ISSUE_NUMBER --repo OWNER/REPO --json title,body,comments
```

Understand: What is broken? What is the expected behavior? What are the acceptance criteria?

### 1c. Read relevant files

Read ALL files listed in `repo-context.yml.relevant_files`. Do not skip any — understanding the existing code is the foundation of a correct fix.

Also read:
- Existing tests for the target code area
- Any files that import from or are imported by the target file
- Type definitions and interfaces used by the target code

### 1d. Establish baseline

Run the project's test suite BEFORE making any changes:

```bash
cd CLONE_PATH
TEST_COMMAND
```

Record the baseline result. If tests fail before you start, report this — you need a clean baseline.

## Phase 2: Implementation

### 2a. Plan the approach

Before writing code, articulate your approach in 3-5 sentences:
1. What specific code will you change?
2. Why will this fix the issue?
3. What tests will you add or modify?
4. Are there any edge cases to consider?

If you're unsure about the approach, stop and tell the user. Do not guess at a fix — a wrong fix is worse than no fix.

### 2b. Write code

Make changes following these principles:

**Follow the project's code style exactly:**
- Match existing indentation (tabs vs spaces, width)
- Match naming conventions (camelCase, snake_case, PascalCase)
- Match import style (relative vs absolute, ordering)
- Match error handling patterns (exceptions vs results, error types)
- Match logging patterns (if project uses a logger, use it)

**Follow the project's test patterns:**
- Use the same test framework and assertion style
- Follow existing test file naming conventions
- Place tests in the correct directory
- Follow existing test structure (describe/it, test/expect, etc.)

**Make ATOMIC commits:**
- One logical change per commit
- Each commit should leave the codebase in a working state
- Commit messages follow the project's convention style

### 2c. AI Disclosure in commits

If `repo-context.yml.ai_policy.disclosure_required` is true, add a `Co-authored-by` trailer to each commit:

```bash
git commit -m "fix: add null check in authenticate() (#123)

Co-authored-by: AI Assistant <noreply@ai.com>"
```

If the project uses a different disclosure format (e.g., a specific header in PR description), note that for the `oss-submit` skill but still add the commit trailer.

## Phase 3: Verification Loop

Run verification commands in this exact order:

### 3a. Lint

```bash
cd CLONE_PATH
LINT_COMMAND
```

If lint fails: fix the issue, re-run. Maximum 3 attempts.

### 3b. Type check

```bash
TYPECHECK_COMMAND
```

If typecheck fails: fix the issue, re-run. Maximum 3 attempts.

### 3c. Test

```bash
TEST_COMMAND
```

If tests fail: analyze the failure. Is it caused by your changes? If yes, fix. If no (pre-existing), note it but continue.

### 3d. Build

```bash
BUILD_COMMAND
```

If build fails: fix the issue, re-run. Maximum 3 attempts.

### 3e. Verification failure policy

If any verification step fails after 3 attempts:
1. STOP
2. Record what failed and what you tried
3. Report to the user with the full error output
4. Do NOT proceed to Phase 4

The verification loop is non-negotiable. A PR that fails CI wastes everyone's time.

## Phase 4: Diff Self-Review

### 4a. Generate the full diff

```bash
cd CLONE_PATH
git diff upstream/main...HEAD
```

### 4b. Self-review checklist

Review every line of the diff against this checklist:

| Check | Question |
|-------|----------|
| Debug prints | Any `console.log`, `print`, `dbg!`, `fmt.Println` left in? |
| TODO/FIXME | Any leftover TODO or FIXME comments? |
| Unrelated changes | Any changes not directly related to the issue? |
| AI code smells | Any unnecessary abstractions, verbose comments, or over-engineering? |
| Missing imports | Did you add all necessary imports? |
| Unused imports | Did you remove imports you no longer need? |
| Error handling | Are all error paths handled? |
| Edge cases | Did you handle null/undefined/empty cases? |
| Documentation | Did you update docs if the behavior changed? |

**Fix any issues found** and re-run the verification loop.

### 4c. Scope check

Count the number of files changed and lines changed:

```bash
git diff --stat upstream/main...HEAD
```

If the diff touches more than 5 files or adds more than 200 lines, consider whether the scope has expanded beyond the issue. If it has, trim the changes. The fix should be minimal and focused.

## Phase 5: Write Artifact

Write `.oss/change-summary.md`:

```markdown
# Change Summary

## Issue
Fixes #123 — Null pointer in auth handler

## Implementation
- Added null check in `src/auth/handler.ts:48`
- Returns `AuthError.invalidInput` when credentials are null
- Added regression test in `src/auth/handler.test.ts`

## Commits
- `abc1234` fix: add null check in authenticate() (#123)
- `def5678` test: add regression test for null credentials

## Verification
- [x] `npm run lint` passes
- [x] `npm run typecheck` passes
- [x] `npm test` passes (all 47 tests)
- [x] `npm run build` succeeds

## Files Changed
- `src/auth/handler.ts` (+5 lines)
- `src/auth/handler.test.ts` (+12 lines)

## Diff Stats
 2 files changed, 17 insertions(+), 0 deletions(-)
```

## Constraints

- NEVER push to remote — this skill only makes local changes
- NEVER modify files outside the scope of the issue
- NEVER skip the verification loop
- NEVER commit without running the project's test command
- NEVER add dependencies without checking project policy
- NEVER include debug statements in committed code
- NEVER leave AI-generated comments like "// Added by AI" or "// This function does..."
- If you can't explain every line of your change, you shouldn't be making it
- Add `Co-authored-by` trailer when AI disclosure is required

## Code Quality Rules

These rules exist because they are the most common reasons AI-generated PRs get rejected:

1. **No AI-generated comments** — Don't add comments that merely restate the code. Comments should explain WHY, not WHAT.
2. **No debug prints** — Remove all `console.log`, `print`, `dbg!`, etc. before committing.
3. **No TODO/FIXME** — Don't leave these unless they were pre-existing.
4. **Follow existing patterns** — If the project uses try/catch, don't introduce Result types. If it uses callbacks, don't introduce async/await. Match what exists.
5. **Minimize the diff** — Every line you change is a line a human has to review. Make every line count.
6. **No drive-by fixes** — If you notice an unrelated issue while working, note it but don't fix it. That's a separate PR.
