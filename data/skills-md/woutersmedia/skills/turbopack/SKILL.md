---
name: turbopack
description: Wouters Media Turbopack / Turborepo guidelines — enable caching, define task pipelines, and optimise build performance across monorepo workspaces.
---

# Turbopack / Turborepo

Apply these guidelines whenever working with Turbopack (the bundler) or Turborepo (the monorepo build system) in Wouters Media projects.

## Turborepo Task Pipelines

Define every task in `turbo.json` so Turborepo can cache outputs and schedule tasks in the correct dependency order.

```json
// turbo.json
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": [".next/**", "dist/**", "!.next/cache/**"]
    },
    "lint": {
      "outputs": []
    },
    "test": {
      "outputs": []
    },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

- `"dependsOn": ["^build"]` ensures a workspace's dependencies are built before the workspace itself.
- List all output artefacts in `outputs` so Turborepo can restore them from cache.
- Set `"cache": false` for long-running dev tasks — they should never be cached.

## Remote Caching

Enable Vercel Remote Cache so build artefacts are shared across local machines and CI:

```bash
# Authenticate once (or use a CI token)
npx turbo login
npx turbo link
```

In CI, provide the token via environment variables. Wouters Media organisation secrets expose `VERCEL_TOKEN` and `VERCEL_ORG_ID` which Turborepo also accepts:

```yaml
# .github/workflows/ci.yml
env:
  # Preferred — use the organisation-wide Vercel token and org ID
  TURBO_TOKEN: ${{ secrets.VERCEL_TOKEN }}
  TURBO_TEAM: ${{ vars.VERCEL_ORG_ID }}
  # Alternative — project-specific token if a dedicated one exists
  # TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
  # TURBO_TEAM: ${{ vars.TURBO_TEAM }}
```

Turborepo will then read from and write to the remote cache automatically.

## Running Tasks

Always run tasks through `turbo` so caching and parallelism are applied:

```bash
# ✅ PREFERRED — run via turbo (uses cache, runs in parallel)
pnpm turbo build
pnpm turbo lint test

# ❌ AVOID — bypasses turbo cache and scheduling
pnpm -r build
```

## Turbopack Bundler (Next.js)

Turbopack is the default bundler for local development in Next.js 15+. No configuration is needed — simply run `next dev` and Turbopack is used automatically.

```bash
# ✅ Next.js 15+ — Turbopack is the default
pnpm dev        # runs `next dev` with Turbopack automatically
```

For older Next.js projects (< 15), opt in explicitly:

```json
// package.json
{
  "scripts": {
    "dev": "next dev --turbopack"
  }
}
```

Turbopack performs incremental compilation — only the changed module and its dependants are re-bundled, keeping HMR near-instant even in large apps.

## Filtering & Affected Packages (Monorepos only)

When the project is a Turborepo monorepo, use `--filter` to run tasks only for packages affected by the current change:

```bash
# Run build only for the web app and its local dependencies
pnpm turbo build --filter=web

# Run tasks for all packages that have changed since the last commit
pnpm turbo build --filter=[HEAD^1]
```

In CI, combine this with GitHub Actions path filters to further reduce unnecessary work.

> This section only applies to monorepo projects that use Turborepo. Skip for single-app repositories.

## Do Not

- Do **not** run `next build` directly inside a Turborepo monorepo — always go through `turbo build` so the cache is used.
- Do **not** add `.turbo/` to version control — it contains local cache metadata. Add it to `.gitignore`.
- Do **not** list `node_modules` or other non-deterministic directories in `outputs`.
- Do **not** set `"cache": false` for `build`, `lint`, or `test` — these tasks must be cacheable.
