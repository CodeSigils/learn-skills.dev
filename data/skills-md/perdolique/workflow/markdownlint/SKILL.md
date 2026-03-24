---
name: markdownlint
description: Configure, manage, and troubleshoot markdownlint in projects. Use when user wants to setup/install/configure markdownlint, add/remove/modify linting rules, fix markdown validation issues, customize .markdownlint.yaml, update ignore patterns, integrate with tools (Husky, CI), or troubleshoot markdown linting errors. Use even when user mentions markdown formatting problems, quality issues, or style consistency without explicitly saying "markdownlint".
license: Unlicense
---

## Package manager detection

**Before any operation**, detect which package manager the project uses:

1. Check for lock files:
   - `pnpm-lock.yaml` → use `pnpm`
   - `yarn.lock` → use `yarn`
   - `package-lock.json` → use `npm`
   - `bun.lockb` → use `bun`

2. Check `packageManager` field in package.json:

   ```json
   "packageManager": "pnpm@8.0.0"
   ```

3. If no indicators, ask the user which package manager they prefer

**Throughout this skill**, commands use `pnpm` as examples. Replace with the detected package manager:

- `pnpm add -D` → `npm install --save-dev` / `yarn add -D` / `bun add -d`
- `pnpm run` → `npm run` / `yarn run` / `bun run`
- `pnpm install` → `npm install` / `yarn install` / `bun install`

## Operation selection guide

Identify what the user needs and read the appropriate reference file:

- **Initial Setup** → Read [references/setup.md](references/setup.md)
  - First time installation
  - Creating config files (.markdownlint.yaml, .markdownlintignore)
  - Adding npm scripts
  - Adding verification to AGENTS.md
  - Husky integration

- **Modifying Rules** → Read [references/rules.md](references/rules.md)
  - Enabling/disabling specific rules
  - Configuring rule options (heading-style, ul-style, etc.)
  - Understanding rule names and codes (MD###)

- **Updating Ignore Patterns** → Read [references/ignoring.md](references/ignoring.md)
  - Adding files/folders to .markdownlintignore
  - Gitignore-style pattern syntax
  - Verifying ignored files

- **Fixing Violations** → Read [references/fixing.md](references/fixing.md)
  - Understanding error messages
  - Auto-fix with --fix flag
  - Common violations (MD009, MD012, MD022, MD040, etc.)
  - Manual fixes for specific errors

- **Integration Management** → Read [references/integration.md](references/integration.md)
  - Updating npm scripts
  - Modifying Husky hooks
  - CI/CD integration (GitHub Actions, GitLab CI)
  - VS Code extension setup

- **Troubleshooting** → Read [references/troubleshooting.md](references/troubleshooting.md)
  - Too many errors
  - Files not being checked
  - Hook failures
  - Module not found errors
  - Performance issues

## Quick reference: Common commands

```bash
# Install
pnpm add -D markdownlint markdownlint-cli

# Run linting
pnpm run lint:markdown

# Auto-fix issues
markdownlint '**/*.md' --fix

# Lint specific file
markdownlint README.md

# Lint specific directory
markdownlint 'docs/**/*.md'
```

## Quick reference: Config file basics

`.markdownlint.yaml` in project root:

```yaml
$schema: ./node_modules/markdownlint/schema/markdownlint-config-schema.json

# Disable a rule
line-length: false

# Enable a rule
no-duplicate-heading: true

# Configure a rule
heading-style:
  style: "atx"
```

`.markdownlintignore` in project root (gitignore syntax):

```gitignore
node_modules
dist/
build/
CHANGELOG.md
```

## Key examples

### Example 1: Basic setup

**User:** "Add markdownlint to my project"

**Action:** Read [references/setup.md](references/setup.md) and follow Steps 1-9 for complete initial setup.

### Example 2: Disable annoying rule

**User:** "Stop complaining about duplicate headings"

**Action:** Read [references/rules.md](references/rules.md) → Removing rules section. Add `no-duplicate-heading: false` to `.markdownlint.yaml`.

### Example 3: Fix many errors

**User:** "I have 50 markdown errors, fix them"

**Action:** Read [references/fixing.md](references/fixing.md) → Auto-fixing section. Run `markdownlint '**/*.md' --fix`, show diff, handle remaining errors.

### Example 4: Ignore folder

**User:** "Don't lint the dist folder"

**Action:** Read [references/ignoring.md](references/ignoring.md). Add `dist/` to `.markdownlintignore`.

### Example 5: Add to CI

**User:** "Add markdown linting to GitHub Actions"

**Action:** Read [references/integration.md](references/integration.md)tions"

**Action:** Read `references/integration.md` → CI integration section. Create workflow file with pnpm setup and linting step.

## Progressive workflow

For complex requests that span multiple operations:

1. **Start with the main operation** - Read the primary reference file first
2. **Chain related operations** - Read additional reference files as needed
3. **Verify each step** - Run commands to confirm changes work
4. **Document what was done** - Summarize changes for the user

Example: "Set up markdownlint with strict rules and CI"

- Read [references/setup.md](references/setup.md) → complete initial setup
- Read [references/rules.md](references/rules.md) → enable strict rules
- Read [references/integration.md](references/integration.md) → add CI configuration
- Test all steps work together

## When to use which reference

**User mentions installation, setup, "add markdownlint":**
→ [references/setup.md](references/setup.md)

**User mentions specific rules, MD codes, enabling/disabling:**
→ [references/rules.md](references/rules.md)

**User mentions ignoring files, excluding folders:**
→ [references/ignoring.md](references/ignoring.md)

**User has errors and wants to fix them:**
→ [references/fixing.md](references/fixing.md)

**User mentions npm scripts, husky, pre-commit, CI, GitHub Actions:**
→ [references/integration.md](references/integration.md)

**User reports issues, things not working, errors:**
→ [references/troubleshooting.md](references/troubleshooting.md)

## Default configuration philosophy

When setting up markdownlint, use this opinionated default configuration:

```yaml
$schema: ./node_modules/markdownlint/schema/markdownlint-config-schema.json

line-length: false # Modern editors handle wrapping
```

**Rationale:** Start permissive, enable rules gradually. The `line-length` rule is disabled by default because:

- Modern editors and viewers handle text wrapping automatically
- Fixed line length creates unnecessary friction in most projects
- Semantic issues are more valuable to catch than presentation issues

Only add more rules if user explicitly requests them or if the project needs stricter validation.
