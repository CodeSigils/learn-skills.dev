---
name: commit
description: >-
  Creates and executes one coherent git commit from staged or selected working-tree
  changes. Use when the user asks to commit changes, stage and commit a logical
  change, or create a git commit with an appropriate message. Do not use for a
  draft-only message request or an operation that only pushes existing commits.
allowed-tools: Bash(git add:*) Bash(git status:*) Bash(git diff:*) Bash(git commit:*) Bash(git log:*) Bash(git ls-files:*) Bash(git branch:*) AskUserQuestion
---

Create exactly one coherent commit while preserving changes outside its intended
scope. Write the commit message in English and communicate with the user in their
language. Follow explicit user instructions and applicable repository guidance
before the defaults below.

## Repository Context

- Status: !`git status --short`
- Staged changes: !`git diff --cached`
- Unstaged changes: !`git diff`
- Untracked files: !`git ls-files --others --exclude-standard`
- Unmerged files: !`git diff --name-only --diff-filter=U`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## 1. Define the Commit Scope

1. If the worktree and index contain no changes, tell the user there is nothing
   to commit and stop.
2. Select the target changes in this order:
   - If the user named files or a logical change, use that scope. If unrelated
     changes are already staged, explain the conflict and ask how to proceed
     before changing the index.
   - Otherwise, if staged changes exist, treat the staged diff as the complete
     target. Leave unstaged and untracked changes untouched.
   - Otherwise, group unstaged and untracked changes by purpose. If they form one
     clear logical change, use that group. If there are multiple plausible groups
     or a file's inclusion is ambiguous, present the groups and ask which one to
     commit.
3. Judge cohesion by behavior and purpose, not by file count alone. Keep tests,
   documentation, and configuration with the implementation they directly
   support.

## 2. Prepare the Index

When the exact target is not already staged, stage only its files with explicit
pathspecs:

```bash
git add -- "path/with[brackets]/file.ts" "another path/file.md"
```

Use `--` before paths and quote paths containing spaces, brackets, parentheses,
wildcards, or other shell-special characters. Include untracked files only when
they are part of the target change. Exclude local configuration, credentials,
temporary files, logs, and build artifacts unless repository guidance explicitly
tracks them and they are required by the change. If a target file mixes relevant
and unrelated hunks, stage only the relevant hunks; ask the user before staging
the whole file when safe partial staging is not practical.

After staging, re-run `git status --short` and `git diff --cached`. The staged diff
is now the sole source of truth for the commit.

## 3. Review the Staged Diff

Stop before committing when any blocking condition is present:

| Condition | Required action |
|-----------|-----------------|
| Empty staged diff | Tell the user there is nothing staged for this commit. |
| Unmerged entries or real conflict markers | List the affected files and ask the user to resolve them. |
| Suspected secret, credential, private key, or unintended `.env` file | Identify the location without repeating the value; ask the user to remove it or confirm it is non-secret test data. |
| Unclear or unrelated staged content | Explain the mismatch and ask how to scope the commit. |

Also inspect added lines for accidental debug statements, generated output, logs,
and unexplained `TODO` or `FIXME` markers. Ask only when an item appears unintended;
do not treat every occurrence as an error.

## 4. Compose the Message

Treat the message as a compact, standalone explanation for a human or coding
agent that may not inspect the diff. Prioritize the changed behavior or system
rule over author activity, file lists, and implementation inventory. Ground every
claim in the staged changes and relevant repository context.

First follow an explicit repository commit convention. Use recent commit history
as supporting evidence, not as a replacement for written guidance. Then distill:

1. The primary before-and-after change in behavior, capability, data flow, or
   system rule.
2. The single core intuition that explains most of the staged diff.
3. Only the context needed to prevent a reader from forming the wrong mental
   model.

When no convention is defined, use these defaults:

- **Title (subject):** Start with an imperative English verb. Name the affected
  concept and its changed behavior or governing rule, not merely the editing
  action or a broad benefit. Prefer `Deduplicate retries by request ID` to
  `Update retry handling`. Omit a trailing period and keep the title concise; do
  not exceed 72 characters. Exclude conventional-commit types/scopes (`feat:`,
  `fix(x):`), ticket or issue IDs, and branch names. Recent commits containing
  such a prefix are not sufficient reason to add one; only an explicit written
  convention (e.g. `CONTRIBUTING.md`, a commit template, a commitlint config)
  does.
- **Description (body):** Default to one short paragraph whose first sentence
  states the change as a delta a reader can verify: what held before versus
  what holds now. `Previously, <old rule>. Now, <new rule>.` is one natural
  shape, not a required one. When no meaningful prior behavior exists (a new
  capability, file, or first version), state the new rule directly; never
  write a contrast whose "previously" clause merely negates the "now" clause.
  Include the deciding unit, direction, or unchanged boundary only when it is
  part of that delta. Omit the body only when the title itself makes the
  change recoverable. Do not summarize files or tests.
- Use one minimal toy example when concrete input, state, or output makes a
  non-obvious rule faster to understand. For example: `Attempts r1, r1, r2 now
  create two jobs instead of three because request ID defines identity.` Keep
  the example faithful to the diff; do not invent unsupported behavior.
- After the intuition, include motivation, an important constraint or tradeoff,
  breaking behavior, or migration guidance only when it materially helps the
  reader understand or act on the change.
- Separate the description from the title with a blank line and wrap body lines
  at 72 characters.

Do not turn the description into a file-by-file or hunk-by-hunk summary. Omit
secondary edits, routine tests, and mechanical details unless they change the
core mental model. Do not force a body or toy example based only on change size.

## 5. Verify and Commit

Before executing the commit, review `git diff --cached` one final time and verify:

1. Every staged change belongs to the selected scope.
2. The message gives an accurate core mental model of the staged change without
   requiring file-by-file inspection or claiming unstaged work.
3. The staged diff still passes the safety review above.

For a subject-only message, run:

```bash
git commit -m "Subject line"
```

For a message with a body, use separate `-m` arguments so Git inserts a real blank
line. Put real line breaks in a long body; never encode them as literal `\n` text.

```bash
git commit \
  -m "Deduplicate retries by request ID" \
  -m "Retries now treat request ID as the unit of identity. Attempts r1, r1,
r2 create two jobs instead of three."
```

If the commit fails, inspect the error and current status before taking further
action. If a hook modified files or the index, review the new staged diff and
revalidate the message before retrying. Do not retry a failure blindly.

After success, inspect the complete stored message with
`git log -1 --format='%B'`. Verify that the title/body separator and body line
breaks are real line breaks, not literal `\n` text. If the just-created message
is malformed, amend it using actual line breaks and inspect it again. Then run
`git log -1 --format='%h %s'` and `git status --short`. Report the commit hash and
subject, then mention any remaining unstaged or untracked changes. Do not push
unless the user separately requested it.
