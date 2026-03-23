---
name: changelog
description: Maintain changelogs following the Keep a Changelog 1.1.0 specification (keepachangelog.com). Use when users ask to create a new CHANGELOG.md, update an existing changelog with recent changes, add entries to the Unreleased section, or review git history to suggest changelog entries. Supports any project type and language.
---

# Changelog

Maintain project changelogs following [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/).

## Workflow

1. Check if `CHANGELOG.md` exists in the project root.
   - **No** -> Go to [Create a New Changelog](#create-a-new-changelog)
   - **Yes** -> Go to [Update an Existing Changelog](#update-an-existing-changelog)
2. If the user wants entries based on recent work, go to [Git-Aware Entry Suggestions](#git-aware-entry-suggestions).
3. After adding entries, update [Comparison Links](#comparison-links) at the bottom of the file.

## Create a New Changelog

Use this template:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

[Unreleased]: https://github.com/USER/REPO/compare/HEAD...HEAD
```

- File must be named `CHANGELOG.md` (not HISTORY, NEWS, or RELEASES).
- Replace the comparison link with the actual remote URL (see [Comparison Links](#comparison-links)).
- If the project already has releases, add existing version sections below Unreleased.
- Only include category headings (e.g. `### Added`) that have entries — omit empty categories.

## Update an Existing Changelog

1. Read the existing `CHANGELOG.md` fully before modifying.
2. Add new entries under `## [Unreleased]`, grouped by category.
3. If the Unreleased section doesn't exist, create it above the latest version.
4. Preserve all existing content, formatting, and comparison links.
5. Only add category headings that have entries.

### Entry Writing Guidelines

- Write entries for humans, not machines — use clear, concise language.
- Each entry is a bullet point describing one notable change.
- Focus on *what changed and why it matters*, not implementation details.
- Use present tense imperative: "Add support for..." not "Added support for...".

Good:
```markdown
- Add bulk export to CSV for transaction reports
- Fix crash when opening files with unicode characters in the path
```

Bad:
```markdown
- Updated the export module to support CSV format by refactoring the serializer
- Fixed bug #1234
```

## Git-Aware Entry Suggestions

When the user wants entries based on recent work, inspect git history to draft them.

### 1. Find the Reference Point

```bash
# Latest tag
git describe --tags --abbrev=0

# If no tags exist, use initial commit
git rev-list --max-parents=0 HEAD
```

### 2. Inspect Changes

```bash
# Commit messages since last tag (or reference point)
git log --oneline <ref>..HEAD --no-merges

# File-level summary for additional context
git diff --stat <ref>..HEAD
```

### 3. Categorize Changes

Map commits to changelog categories using these heuristics as starting guidance — always use judgment based on the actual changes:

| Commit signal | Category |
|---------------|----------|
| `feat`, `add`, new files/modules | Added |
| `change`, `update`, `refactor`, behavior changes | Changed |
| `deprecate` | Deprecated |
| `remove`, `delete`, deleted files/modules | Removed |
| `fix`, `bug`, `patch` | Fixed |
| `security`, `vuln`, `cve` | Security |

### 4. Filter Noise

Skip these — they are not changelog-worthy:

- Merge commits
- CI/CD-only changes (pipeline configs, GitHub Actions)
- Code formatting or linting-only changes
- Internal refactors with no user-visible effect
- Dependency bumps (unless they fix a security issue or change behavior)

### 5. Draft Entries

Translate developer commit messages into user-facing changelog prose. Group related commits into a single entry when they represent one logical change.

Commit messages:
```
feat: add csv export to reports controller
feat: add csv download button to reports page
fix: handle empty report gracefully
```

Changelog entries:
```markdown
### Added

- Add bulk export to CSV for transaction reports

### Fixed

- Fix crash when generating reports with no data
```

## Formatting Rules

### Categories

Use exactly these six categories, in this order. Only include categories that have entries:

1. `### Added` — new features
2. `### Changed` — changes in existing functionality
3. `### Deprecated` — soon-to-be removed features
4. `### Removed` — removed features
5. `### Fixed` — bug fixes
6. `### Security` — vulnerability fixes

### Version Headers

```markdown
## [Unreleased]

## [1.1.0] - 2026-03-22

## [1.0.0] - 2026-01-15 [YANKED]
```

- Each version is an `## [x.y.z] - YYYY-MM-DD` header.
- Dates use ISO 8601 format (`YYYY-MM-DD`).
- Latest version comes first, oldest last.
- `## [Unreleased]` is always the first section (below the file header).
- Yanked releases append `[YANKED]` after the date.

## Comparison Links

Add reference-style links at the bottom of `CHANGELOG.md` so version headers are clickable.

### 1. Detect the Remote URL

```bash
git remote get-url origin
```

### 2. Normalize the URL

Convert SSH to HTTPS and strip `.git` suffix:

- `git@github.com:user/repo.git` -> `https://github.com/user/repo`
- `https://github.com/user/repo.git` -> `https://github.com/user/repo`

### 3. Generate Compare URLs

**GitHub and GitLab:**
```markdown
[Unreleased]: https://github.com/user/repo/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/user/repo/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/user/repo/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/user/repo/releases/tag/v0.1.0
```

**Bitbucket:**
```markdown
[Unreleased]: https://bitbucket.org/user/repo/branches/compare/HEAD..v1.1.0
[1.1.0]: https://bitbucket.org/user/repo/branches/compare/v1.1.0..v1.0.0
```

Rules:
- `[Unreleased]` compares the latest tag to `HEAD`.
- Each version compares its tag to the previous version's tag.
- The oldest version links to its release tag (GitHub/GitLab) or compares to the initial commit.
- Detect tag prefix convention from existing tags (`v1.0.0` vs `1.0.0`).
