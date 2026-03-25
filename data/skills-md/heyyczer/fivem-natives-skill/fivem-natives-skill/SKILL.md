---
name: fivem-natives-skill
description: A complete reference for FiveM native functions, auto-updated from [cfxnatives.dev](https://cfxnatives.dev) and organized by namespace. Use this skill to get accurate native signatures, parameters, return types, and examples when developing FiveM resources.
---

# FiveM Natives Skill

A complete reference for FiveM native functions, auto-updated from [cfxnatives.dev](https://cfxnatives.dev) and organized by namespace. Use this skill to get accurate native signatures, parameters, return types, and examples when developing FiveM resources.

## What this skill provides

- **Native reference by namespace** — PED, VEHICLE, NETWORK, CFX, HUD, GRAPHICS, and 40+ more namespaces, each in its own file
- **Types reference** — explanation of all native types: `Ped`, `Vehicle`, `Entity`, `Vector3`, `Hash`, `Player`, etc.
- **Best practices** — FiveM-specific patterns for performance, threading, events, security, and entity management

## Files

| File | Description |
|------|-------------|
| `docs/index.md` | Index of all namespaces with native counts |
| `docs/{namespace}.md` | All natives for that namespace (e.g. `docs/ped.md`) |
| `docs/types-reference.md` | Native type definitions and usage |
| `docs/best-practices.md` | FiveM development best practices |

## Versioning

Version format: `{generator-semver}+natives.{YYYYMMDD}`

| Tag pattern | Meaning |
|-------------|---------|
| `v1.0.0` | Generator code changed (manual release) |
| `natives-20260324` | Natives data updated (automatic, every 3 days) |

## Using in Claude Code

Add to your project's `CLAUDE.md`:

```markdown
## FiveM Natives Reference
See the files in @docs/ for the complete FiveM native function reference.
- @docs/index.md — namespace index
- @docs/ped.md — PED natives
- @docs/vehicle.md — VEHICLE natives
- @docs/best-practices.md — development guidelines
```

Or import all docs at once using the `@docs/` directory reference.

## Updating

```bash
bun run build         # rebuild only if natives changed
bun run build:force   # always rebuild
```

The GitHub Actions workflow runs automatically every 3 days and commits + tags any changes.
