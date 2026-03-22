---
name: pnpm
description: Always use pnpm as the package manager unless the project already uses npm or yarn.
metadata:
  tags: [pnpm, package-manager, dependencies]
---

## When to use

Use this skill proactively for:
- Installing dependencies
- Adding or removing packages
- Running scripts
- Any command that involves a package manager

## Instructions

Always use **pnpm** as the package manager. Before running any package manager command, check which package manager the project is already using:

1. If `pnpm-lock.yaml` exists → use **pnpm**
2. If `yarn.lock` exists → use **yarn**
3. If `package-lock.json` exists → use **npm**
4. If none exist (new project) → use **pnpm**

Never switch the package manager mid-project. If a project already uses npm, continue with npm throughout. Do not mix package managers in the same project.

### pnpm Command mappings

| Instead of                  | Use                              |
|-----------------------------|----------------------------------|
| `npm install`               | `pnpm install`                   |
| `npm install <pkg>`         | `pnpm add <pkg>`                 |
| `npm install -D <pkg>`      | `pnpm add -D <pkg>`              |
| `npm install -g <pkg>`      | `pnpm add -g <pkg>`              |
| `npm uninstall <pkg>`       | `pnpm remove <pkg>`              |
| `npm run <script>`          | `pnpm run <script>`              |
| `npm ci`                    | `pnpm install --frozen-lockfile` |
| `npx <cmd>`                 | `pnpm dlx <cmd>`                 |

### Lockfile and Dockerfile

- Always reference `pnpm-lock.yaml` (not `package-lock.json`) in pnpm projects
- In Dockerfiles, use `pnpm install --frozen-lockfile --prod` for production installs
- Copy both `package.json` and `pnpm-lock.yaml` into Docker images
