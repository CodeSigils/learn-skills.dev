---
name: conventionalcommits
description: Conventional Commits specification for semantic versioning and changelog generation. Use when writing commit messages, configuring commit linting, or automating releases.
metadata:
  author: froQ
  version: "2026.3.25"
  source: Generated from https://github.com/conventional-commits/conventionalcommits.org, scripts at https://github.com/0froq/skills
---

# Conventional Commits

> Based on Conventional Commits v1.0.0. A lightweight convention for writing commit messages that communicates intent and enables automated tooling.

The Conventional Commits specification provides a structured format for commit messages. It supports semantic versioning, changelog generation, and clearer project history.

## Core Concepts

| Topic | Description | Reference |
|-------|-------------|-----------|
| Structure | Type, scope, description, body, footer format | [core-structure](references/core-structure.md) |
| Types | feat, fix, and optional type conventions | [core-types](references/core-types.md) |
| SemVer Mapping | How commits translate to version bumps | [core-semver](references/core-semver.md) |
| Format Details | Scopes, bodies, footers, breaking changes | [core-format](references/core-format.md) |

## Quick Reference

### Commit Structure

```
<type>(<scope>): <description>

<body>

<footer>
```

### Types and SemVer

| Type | SemVer | Use For |
|------|--------|---------|
| `feat` | MINOR | New features (normative per spec) |
| `fix` | PATCH | Bug fixes (normative per spec) |
| `docs` | — | Documentation changes (convention) |
| `refactor` | — | Code restructuring (convention) |
| `perf` | — | Performance improvements (convention) |
| `test` | — | Test additions/changes (convention) |
| `build` | — | Build system changes (convention) |
| `ci` | — | CI configuration (convention) |
| `style` | — | Code style changes (convention) |

**Note:** Only `feat`, `fix`, and breaking-change markers have normative SemVer meaning in the specification. Other types are optional conventions—tools may categorize them differently. `chore` is intentionally excluded from recommendations; use specific types above for clarity.

### Breaking Changes

```
feat(api)!: redesign user authentication

BREAKING CHANGE: auth token format changed from JWT to opaque tokens
```

### Examples

```bash
# New feature
feat: add dark mode toggle

# Bug fix with scope
fix(auth): resolve token expiration bug

# Breaking change
feat(api)!: remove deprecated endpoints

# With body and footer
feat(search): implement fuzzy matching

Adds Levenshtein distance algorithm for typo-tolerant search.

Closes #123
```

<!--
Source references:
- https://conventionalcommits.org
- https://www.conventionalcommits.org/en/v1.0.0/
-->
