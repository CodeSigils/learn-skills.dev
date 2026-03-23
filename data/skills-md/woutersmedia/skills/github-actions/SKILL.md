---
name: github-actions
description: Wouters Media GitHub Actions guidelines — keep workflows DRY and KISS, maximise caching, minimise build minutes, and avoid redundant steps.
---

# GitHub Actions

Apply these guidelines whenever writing, reviewing, or optimising GitHub Actions workflows in Wouters Media projects.

## Core Principles

- **DRY**: Extract repeated steps into reusable workflows (`workflow_call`) or composite actions. Never copy-paste the same `steps` block across multiple workflow files.
- **KISS**: Keep each workflow focused on a single purpose. Avoid multi-purpose workflows that mix build, test, and deploy concerns in one file.
- **Minimise build minutes**: Only run what is necessary. Skip redundant jobs with conditions, cache aggressively, and run jobs in parallel where possible.

## Caching

Always cache package manager stores and build artefacts to avoid reinstalling or rebuilding from scratch on every run.

```yaml
# ✅ Cache pnpm store
- name: Cache pnpm store
  uses: actions/cache@v4
  with:
    path: ~/.local/share/pnpm/store
    key: pnpm-${{ runner.os }}-${{ hashFiles('**/pnpm-lock.yaml') }}
    restore-keys: |
      pnpm-${{ runner.os }}-

# ✅ Or use the official setup-node cache integration
- uses: actions/setup-node@v4
  with:
    node-version: 22
    cache: pnpm
```

Prefer `hashFiles('**/pnpm-lock.yaml')` (or the relevant lockfile) as the cache key so the cache is invalidated only when dependencies actually change.

## Reusable Workflows

Extract shared logic into a reusable workflow called via `workflow_call`:

```yaml
# .github/workflows/_install.yml  (reusable, prefix with _ by convention)
on:
  workflow_call:
    inputs:
      node-version:
        type: string
        default: '22'

jobs:
  install:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
          cache: pnpm
      - run: pnpm install --frozen-lockfile
```

```yaml
# .github/workflows/ci.yml
jobs:
  build:
    uses: ./.github/workflows/_install.yml
```

## Job Concurrency & Parallelism

Run independent jobs in parallel and cancel stale runs on new pushes:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  lint:
    runs-on: ubuntu-latest
    # ...
  test:
    runs-on: ubuntu-latest
    # ...
  build:
    runs-on: ubuntu-latest
    needs: [lint, test]
    # ...
```

## Conditional Execution

Skip jobs or steps that are not relevant to the change using `paths` filters or `if` conditions:

```yaml
on:
  push:
    paths:
      - 'apps/web/**'
      - 'packages/**'
      - '.github/workflows/ci.yml'
```

```yaml
- name: Deploy
  if: github.ref == 'refs/heads/main'
  run: pnpm deploy
```

## Pinning Actions

Always pin third-party actions to a specific SHA or at minimum a major version tag to prevent supply-chain attacks and unexpected breakage:

```yaml
# ✅ PREFERRED — pinned to a full SHA
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2

# ✅ ACCEPTABLE — pinned to major version
- uses: actions/checkout@v4
```

## Do Not

- Do **not** store secrets in workflow files. Use GitHub Actions secrets (`${{ secrets.MY_SECRET }}`).
- Do **not** run `pnpm install` without `--frozen-lockfile` in CI — always reproduce the exact locked versions.
- Do **not** add `continue-on-error: true` to hide failures; fix the root cause instead.
- Do **not** commit generated artefacts (e.g. `dist/`, `.next/`) unless they are required for deployment via a release step.
