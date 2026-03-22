---
name: typescript-sdk
description: Guide for integrating and using the published `@minswap/sdk` npm package in TypeScript projects. Use when users need help installing the package, fixing ESM/runtime setup, choosing between Blockfrost and Maestro adapters, querying pools or prices, using calculation helpers, or building Minswap transactions with Lucid. Focus primarily on `Dex`, `DexV2`, and `Stableswap` consumer workflows. Treat `LbeV2`, `Dao`, and `ExpiredOrderMonitor` as secondary exports to cover only when the user explicitly asks. Ignore repo-only infrastructure such as indexer/syncer, Prisma/Postgres, Docker, and other internal tooling unless the user explicitly asks for self-hosted syncer details.
---

# TypeScript SDK

## Core Workflow

1. Treat `@minswap/sdk` as an npm package integration task, not a repo contribution task.
2. Prefer root imports from `@minswap/sdk`. Do not suggest `src/*`, `build/*`, or other internal paths.
3. Classify the request before answering:
   - setup, install, or runtime issue
   - read-only pool or price query
   - pure math or quoting helper
   - stableswap workflow
   - transaction building with Lucid
4. Default to `BlockfrostAdapter` or `MaestroAdapter` for consumer apps.
5. Treat `Dex`, `DexV2`, and `Stableswap` as the primary package workflows.
6. Treat `LbeV2`, `Dao`, and `ExpiredOrderMonitor` as secondary exports. Mention them only when the user explicitly asks or their task clearly depends on them.
7. Treat `MinswapAdapter` and syncer-backed workflows as out of scope unless the user explicitly asks for self-hosted infrastructure.

## Setup Rules

- Read [references/setup-and-scope.md](references/setup-and-scope.md) first for install commands, ESM caveats, and scope boundaries.
- Call out ESM requirements when imports, Node execution, or test runners fail.
- Recommend direct dependencies for whichever provider SDK the user imports in app code. Do not rely on transitive dependencies being available.
- If a user asks about version-specific behavior, inspect their installed package or lockfile when available instead of assuming the repo snapshot matches their app.

## Implementation Rules

- Use exact exported names from the package root.
- Preserve the package's split between:
  - adapters for on-chain data access
  - calculation helpers for offline quoting
  - `Dex` and `DexV2` for transaction construction
  - `Stableswap` and `StableswapCalculation` for stable-pool workflows
  - Lucid helper factories for backend setup
- Prioritize examples for `Dex`, `DexV2`, and `Stableswap`.
- Keep `LbeV2`, `Dao`, and `ExpiredOrderMonitor` short and secondary when they are needed.
- Use `bigint` amounts in examples.
- Keep examples minimal and task-shaped. Only show the APIs needed for the user's request.
- When users need asset identifiers, use `ADA` for lovelace or `Asset.fromString(...)` for a policy ID plus token name.

## Task Guide

### Setup Or Import Errors

- Start with [references/setup-and-scope.md](references/setup-and-scope.md).
- Check `package.json` ESM settings, `.npmrc`, Node version, and whether the user installed the provider packages they import directly.

### Read-Only Queries

- Use [references/common-patterns.md](references/common-patterns.md) for adapter setup and pool lookup examples.
- Reach for:
  - `BlockfrostAdapter`
  - `MaestroAdapter`
  - `Asset`
  - `ADA`
  - `NetworkId`

### Pure Calculations

- Use [references/common-patterns.md](references/common-patterns.md) for quote and slippage examples.
- Reach for:
  - `calculateSwapExactIn`
  - `calculateSwapExactOut`
  - `calculateDeposit`
  - `calculateWithdraw`
  - `calculateAmountWithSlippageTolerance`
  - `DexV2Calculation`

### Stableswap

- Use [references/common-patterns.md](references/common-patterns.md) for stable-pool math and order construction examples.
- Reach for:
  - `Stableswap`
  - `StableswapCalculation`
  - `StableOrder`

### Transaction Building

- Use [references/common-patterns.md](references/common-patterns.md) for Lucid-backed examples.
- For V1 orders, use `new Dex(lucid)`.
- For V2 orders, use `new DexV2(lucid, adapter)` and build orders via `createBulkOrdersTx(...)`.
- For stableswap orders, use `new Stableswap(lucid)`.
- Use `getBackendBlockfrostLucidInstance(...)` or `getBackendMaestroLucidInstance(...)` when the user wants a backend/read-only wallet setup.

### Secondary Exports

- Cover `LbeV2`, `Dao`, and `ExpiredOrderMonitor` only when the user explicitly asks or when the task cannot be solved with the primary workflows.
- Keep secondary guidance shorter than the primary `Dex`, `DexV2`, and `Stableswap` guidance unless the user asks for depth.

## Scope Guardrails

- Ignore repo-only material like `docs/database-indexer.md`, `src/syncer/**`, Prisma schema files, Docker Compose, and other operational infrastructure by default.
- Mention those pieces only if the user explicitly asks for self-hosted syncer or `MinswapAdapter` internals.
- If the repo exposes a symbol that clearly targets internal infrastructure, do not surface it unless the user's request requires it.
