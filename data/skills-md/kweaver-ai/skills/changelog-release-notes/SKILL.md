---
name: changelog-release-notes
description: Draft or update release notes and changelog entries from repository evidence. Use when the user asks to add a new version to CHANGELOG files, summarize what changed in a branch or release, explain how changelog content was derived, or keep multilingual changelogs consistent.
---

# Changelog Release Notes

## Overview

Turn repository evidence into concise release notes. Derive changelog content from version files, git history, diffs, migrations, API/docs changes, and existing changelog structure instead of guessing from memory.

## Workflow

1. Confirm the target release.
   Read `VERSION` or the user-provided version number.
   If the repo already has a release bump commit or release metadata, use that to confirm the version.

2. Read the current changelog format first.
   Open existing `CHANGELOG*` files before drafting anything.
   Match the established section order, heading style, date format, language coverage, and level of detail.

3. Collect high-signal evidence from the repo.
   Start with `git diff --stat <base>...HEAD` and recent `git log --oneline`.
   Then inspect the specific commits or files that explain behavior changes.
   Prefer source files, migrations, API schemas, tests, and docs over commit messages alone.

4. Group changes by externally visible impact.
   Use categories such as `New Features`, `Bug Fixes`, `Improvements`, `Documentation`, or the repo's existing headings.
   Focus on behavior users or operators would care about, not raw file churn.

5. Filter out low-signal edits.
   Do not list purely mechanical renames, formatting-only edits, generated lockfile noise, or internal refactors unless they materially change behavior, deployment, compatibility, or observability.

6. Cross-check release claims.
   If a feature appears in commit messages but not in code, migrations, docs, tests, or API/schema changes, treat it as unconfirmed.
   If a change touches control plane, runtime, frontend, and docs, summarize it once as one capability rather than duplicating it by file.

7. Update every required changelog file consistently.
   Keep version headings aligned across `CHANGELOG.md`, `CHANGELOG_ZH.md`, or other localized files.
   Preserve equivalent meaning across languages rather than translating word-for-word mechanically.

8. State the release date explicitly.
   Use the actual release date if provided.
   Otherwise use the current working date only when the user is clearly asking for a release entry for "now".

## Evidence Order

Use this order unless the repo has a stronger release source:

1. `VERSION`
2. Existing `CHANGELOG*`
3. `git diff --stat <base>...HEAD`
4. `git log --oneline` or release bump commits
5. Targeted reads of changed source files
6. Migrations and deployment artifacts
7. API schemas and docs
8. Integration or unit tests that confirm end-to-end behavior

Read [references/source-checklist.md](./references/source-checklist.md) when you need a quick checklist of evidence sources and mapping rules.

## Drafting Rules

- Prefer capability-oriented bullets over file-oriented bullets.
- Merge related backend, runtime, frontend, and docs work into one release item when they ship one user-facing feature.
- Mention upgrade steps when a release introduces schema changes, new environment variables, or migration behavior.
- Keep wording factual. Avoid marketing language.
- If the changelog already uses emojis or a specific heading taxonomy, preserve it.
- If the repo contains multilingual changelogs, update all of them in the same turn.

## Validation

Before finishing:

- Verify the version heading was inserted in the correct chronological position.
- Verify all localized changelogs mention the same major capabilities.
- Verify dates are in the repo's established format.
- Verify no bullet depends only on an unverified commit subject.
- Verify the final text reflects what shipped, not what was merely discussed in specs.

## Response Pattern

When the user asks how the changelog was derived, explain the evidence chain succinctly:

- existing changelog structure
- version source
- branch diff and recent commits
- targeted reads of changed modules
- migrations, API docs, and tests used to confirm behavior

Do not claim exhaustive accuracy if you only inspected a subset of the changed files.
