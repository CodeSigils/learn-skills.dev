---
name: commit
description: Write commit messages in Conventional Commits format with gitmoji and execute the commit — type, scope, summary, and body.
disable-model-invocation: true
---

# Purpose

Guide the agent to produce a commit message in `<gitmoji> <type>(<scope>): <summary>\n\n<body>` format and execute the commit.

# Scope

This skill writes commit messages and commits staged changes. It does NOT stage files, manage branches, resolve merge conflicts, amend history, push, or interact with remotes. The user decides what to commit; the skill decides how to format it.

---

# Leading words

- **header** — the first line: `<gitmoji> <type>(<scope>): <summary>`
- **body** — the optional paragraph(s) after the blank line, explaining why and what
- **summary** — the imperative, one-line description in the header (50–72 chars)
- **scope** — the module, component, or area affected (lowercase, hyphenated when multi-word)

---

# Workflow

## 1. Pre-flight

Check the staging area:

```bash
git diff --cached --stat
```

If staged changes exist, proceed to step 2.

If no staged changes exist, run `git status` and report which files are modified/untracked. Ask: "Which files should I stage for this commit?" Do not proceed until the user answers.

Completion: Staged changes are confirmed and ready for analysis.

---

## 2. Analyze changes

Read the staged diff:

```bash
git diff --cached
```

Determine from the diff content, not the file names alone:

- **type** — one of the conventional commit types (see [references/format.md](./references/format.md))
- **scope** — the affected module, component, or area (lowercase, hyphenated)
- **gitmoji** — one emoji matching the primary intent (see [references/format.md](./references/format.md))

Decision rules:

- When changes span multiple types, pick the dominant one (the change with the most lines or highest impact).
- When scope is ambiguous, use the directory or package name of the affected files.
- When the diff is too large to categorize (>500 lines), ask the user: "This is a large change. What is the primary intent — feat, fix, refactor, or something else?"

Completion: type, scope, and gitmoji are selected. Every selection has a reason traceable to the diff.

---

## 3. Draft message

Construct the commit message in two parts:

**Header**: `<gitmoji> <type>(<scope>): <summary>`

- Summary is imperative, present tense ("add" not "adds" or "added").
- Summary does not exceed 72 characters.
- Summary is lowercase unless proper nouns.
- No trailing period.

**Body** (when the change needs explanation):

- Start after one blank line.
- Explain **why** the change was made and **what** it does (not how — the diff shows how).
- Wrap lines at 72 characters.
- Reference related tickets or issues when available.

When the change is trivial (e.g., typo fix, formatting only, single-line change), omit the body. Do not add filler.

Draft the full message and present it to the user as a code block:

```
✨ feat(auth): add OAuth2 token refresh

Invalid tokens were silently rejected after expiry, causing unexpected
login prompts. This adds automatic refresh via the /token endpoint.
```

Completion: A draft message is displayed. The user has not yet approved.

---

## 4. Confirm

Ask the user: "Commit with this message?"

Wait for explicit approval. Do not commit on "looks good," "sure," or similar vague affirmations — treat those as approval only if the message was displayed in the same turn.

If the user asks for changes, return to step 3 and revise.

Completion: User has explicitly approved the message. Execution proceeds to step 5.

---

## 5. Commit

Execute:

```bash
git commit -m "<header>" -m "<body>"
```

If the body is empty, use only `-m "<header>"`.

After commit, confirm with the commit hash from `git rev-parse --short HEAD`.

Do NOT push.

Completion: Commit is created. Short hash is reported. Execution ends.

---

# Rules

- Never stage files. The user controls what goes into the commit.
- Never push. Commits stay local.
- Never amend or force-push without an explicit user request.
- Never generate a message without reading the diff. Guessing from file names is not sufficient.
- The summary must fit in 72 characters. Shorten or split scope before truncating meaning.
- Format details live in [references/format.md](./references/format.md). SKILL.md controls workflow only.

---

# References

- [format.md](./references/format.md) — full type list, gitmoji mapping, scope naming rules, and edge cases
