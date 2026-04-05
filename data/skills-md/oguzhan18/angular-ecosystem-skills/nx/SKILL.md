---
name: nx
description: "ALWAYS use when working with Nx monorepo, workspace configuration, or Angular/Nx project setup."
metadata:
  version: 22.0.0
  generated_by: oguzhancart
  generated_at: 2026-02-19
---

# Nx (Smart, Fast, Extensible Build System)

**Version:** 22.x (2025)
**Tags:** Monorepo, Build System, Angular, React, Node

**References:** [Docs](https://nx.dev) — guides, tutorials • [GitHub](https://github.com/nrwl/nx) • [Enterprise Patterns Book](https://nx.dev/blog/enterprise-angular-book)

## API Changes

This section documents recent version-specific API changes.

- NEW: TypeScript Project References — Faster builds and type checks using modern TypeScript setup [source](https://nx.dev/blog/wrapping-up-2025)

- NEW: pnpm catalog support — Manage single version policy with pnpm catalogs [source](https://nx.dev/blog/wrapping-up-2025)

- NEW: Angular Rspack support — Fast bundler for Angular projects [source](https://nx.dev/blog/wrapping-up-2025)

- NEW: AI Agent integration — Code mode for better LLM context management [source](https://nx.dev/blog/wrapping-up-2025)

- NEW: Polyglot workspaces — Native support for Gradle, Maven, .NET alongside JS/TS projects

## Best Practices

- Use domain-based folder structure — Group projects by business domain

```
libs/
├── auth/
│   ├── feature-login/
│   └── data-access/
├── products/
│   ├── feature-list/
│   └── ui/
└── shared/
    ├── ui/
    └── utils/
```

- Use Nx generators — Scaffold consistent code across workspace

```bash
# Create new library
nx g @nx/angular:library --name=shared-data-access --directory=libs/shared/data-access

# Create new feature
nx g @nx/angular:component --name=user-profile --project=my-app
```

- Use affected commands — Only run tasks on changed projects

```bash
nx affected:build     # Build only changed projects
nx affected:test      # Test only changed projects
nx affected:lint     # Lint only changed projects
```

- Use shared libraries — Avoid code duplication with common utilities

- Configure task dependencies — Define how tasks depend on each other in `project.json`

```json
{
  "build": {
    "dependsOn": ["^build"]
  }
}
```

- Use Nx Cloud — Enable distributed caching for faster CI

- Use `nx.json` and `tsconfig.base.json` — Enforce consistent settings across projects

- Use `@nx/angular:component` generator — Follow workspace conventions for components
