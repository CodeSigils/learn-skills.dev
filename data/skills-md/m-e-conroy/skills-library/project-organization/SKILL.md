---
name: project-organization
description: Organize web projects with clear folder structures, file naming conventions, and module patterns. Use this skill whenever the user asks about project structure, folder layout, where to put files, file naming conventions, directory organization, scaffolding a new project, import paths, config file placement, or general project architecture questions. Also triggers when users ask "where should I put this file", "how should I organize my project", or want to restructure an existing codebase.
---

# Project Organization

Structure projects so that files are predictable, discoverable, and scalable.

Good organization means a new contributor can open the repo and immediately understand where things live, where to add new code, and how modules relate to each other. The goal is **convention over configuration** — reduce decisions by following consistent patterns.

---

## Core Principles

| Principle | Why it matters |
|-----------|---------------|
| **Colocation** | Keep related files together — a component's markup, styles, tests, and types in the same folder |
| **Flat until painful** | Start with a flat structure, nest only when a folder grows beyond ~10–15 files |
| **Predictable naming** | Anyone should guess the file path from the feature name |
| **Separation of concerns** | Distinguish source code, configuration, build output, documentation, and tests |
| **Single responsibility** | Each folder has one clear purpose described by its name |

---

## Universal Project Root

Every web project shares a common root anatomy regardless of framework:

```
project-root/
├── .github/              # CI/CD workflows, PR templates, actions
│   ├── workflows/        # GitHub Actions YAML files
│   └── PULL_REQUEST_TEMPLATE.md
├── .vscode/              # Editor settings shared with team
│   ├── settings.json
│   ├── extensions.json   # Recommended extensions
│   └── launch.json       # Debug configurations
├── docs/                 # Project documentation, ADRs, guides
├── public/               # Static assets served as-is (favicon, robots.txt)
├── src/                  # All application source code
├── tests/                # Integration & e2e tests (unit tests colocate with source)
├── scripts/              # Build scripts, data migrations, CI helpers
├── .gitignore
├── .editorconfig         # Cross-editor formatting baseline
├── package.json          # Dependencies, scripts, metadata
├── tsconfig.json         # TypeScript config (if applicable)
├── README.md             # Project overview, setup, and usage
├── LICENSE
└── CHANGELOG.md
```

### What Goes Where

| Content | Location | Rationale |
|---------|----------|-----------|
| Application logic | `src/` | Clean separation from config and tooling |
| Static files (images, fonts, favicon) | `public/` or `src/assets/` | `public/` for files served as-is; `src/assets/` for files processed by the build |
| Environment variables | `.env`, `.env.local`, `.env.production` | Root level, never committed (add to `.gitignore`) |
| CI/CD pipelines | `.github/workflows/` | GitHub Actions convention |
| Editor/IDE config | `.vscode/`, `.editorconfig` | Shareable team settings at the root |
| Documentation | `docs/` | Separate from source, easily discoverable |
| Build output | `dist/`, `build/`, `out/` | Root level, always gitignored |
| Dependencies | `node_modules/` | Auto-managed, always gitignored |

---

## Source Code Organization (`src/`)

Two dominant patterns — choose one and be consistent.

### Pattern 1: Feature-Based (Recommended for Most Projects)

Group by feature or domain, not by file type. Each feature is self-contained:

```
src/
├── features/
│   ├── auth/
│   │   ├── components/
│   │   │   ├── LoginForm.tsx
│   │   │   ├── LoginForm.test.ts
│   │   │   └── LoginForm.module.css
│   │   ├── hooks/
│   │   │   └── useAuth.ts
│   │   ├── services/
│   │   │   └── auth.service.ts
│   │   ├── types/
│   │   │   └── auth.types.ts
│   │   └── index.ts          # Public API barrel file
│   ├── dashboard/
│   │   ├── components/
│   │   ├── hooks/
│   │   └── index.ts
│   └── settings/
│       └── ...
├── shared/                    # Cross-feature code
│   ├── components/            # Reusable UI (Button, Modal, Input)
│   ├── hooks/                 # Generic hooks (useMediaQuery, useDebounce)
│   ├── utils/                 # Pure utility functions
│   ├── types/                 # Shared TypeScript types
│   └── constants/             # App-wide constants
├── layouts/                   # Page layout shells
├── pages/  or  routes/        # Route-level entry points
├── styles/                    # Global styles, tokens, themes
├── lib/                       # Third-party wrappers, SDK clients
├── config/                    # App-level config (API URLs, feature flags)
├── App.tsx
└── main.ts
```

**When to use:** Applications with distinct features/domains — dashboards, SaaS products, e-commerce.

### Pattern 2: Type-Based (Layer-Based)

Group by technical role — all components together, all services together:

```
src/
├── components/
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.test.ts
│   │   └── Button.module.css
│   ├── Modal/
│   └── ...
├── hooks/
├── services/
├── utils/
├── types/
├── pages/
├── styles/
├── App.tsx
└── main.ts
```

**When to use:** Smaller projects, component libraries, simple sites.

### Hybrid Approach

Many real projects blend both — shared utilities are type-based, while business logic is feature-based:

```
src/
├── features/          # Feature-based (business logic)
├── components/        # Type-based (shared UI primitives)
├── hooks/             # Type-based (shared hooks)
├── utils/             # Type-based (shared utilities)
└── ...
```

---

## File Naming Conventions

Consistent naming reduces ambiguity. Pick one convention per file category and enforce it.

### Common Patterns

| Category | Convention | Example |
|----------|-----------|---------|
| Components (React/Vue/Svelte) | PascalCase | `UserProfile.tsx`, `NavBar.vue` |
| Component folders | PascalCase | `UserProfile/index.tsx` |
| Utilities / helpers | camelCase or kebab-case | `formatDate.ts`, `string-utils.ts` |
| Constants | camelCase file, UPPER_SNAKE values | `apiEndpoints.ts` → `export const API_BASE_URL` |
| Types / interfaces | camelCase or PascalCase file | `auth.types.ts`, `UserTypes.ts` |
| Tests | Mirror source + suffix | `UserProfile.test.tsx`, `formatDate.spec.ts` |
| Styles | Mirror source + module suffix | `UserProfile.module.css`, `UserProfile.styles.ts` |
| Config files | Lowercase dotfiles or kebab-case | `.eslintrc.js`, `vite.config.ts` |
| Routes / pages | kebab-case matching URL slug | `user-settings.tsx` → `/user-settings` |

### File Suffixes by Role

Suffixes communicate purpose at a glance:

| Suffix | Meaning | Example |
|--------|---------|---------|
| `.test.ts` / `.spec.ts` | Unit or integration test | `auth.service.test.ts` |
| `.e2e.ts` | End-to-end test | `checkout.e2e.ts` |
| `.stories.tsx` | Storybook story | `Button.stories.tsx` |
| `.module.css` | CSS Module (scoped) | `Card.module.css` |
| `.d.ts` | TypeScript declaration | `global.d.ts` |
| `.types.ts` | Type definitions | `user.types.ts` |
| `.service.ts` | Data/API service layer | `auth.service.ts` |
| `.hook.ts` | Custom hook | `useAuth.hook.ts` |
| `.util.ts` | Utility functions | `date.util.ts` |
| `.config.ts` | Configuration | `database.config.ts` |
| `.mock.ts` | Test mock/fixture | `user.mock.ts` |
| `.schema.ts` | Validation schema | `login.schema.ts` |

---

## Module Organization

### Barrel Files (`index.ts`)

Use barrel files to create clean public APIs per folder:

```ts
// src/features/auth/index.ts
export { LoginForm } from "./components/LoginForm";
export { useAuth } from "./hooks/useAuth";
export type { User, AuthState } from "./types/auth.types";
```

```ts
// Consumer imports from the feature, not deep paths
import { LoginForm, useAuth } from "@/features/auth";
```

**Caveats:**
- Barrel files can hurt tree-shaking in some bundlers — avoid re-exporting everything in large libraries.
- Don't nest barrel files too deeply (barrels importing barrels).

### Import Path Aliases

Configure path aliases to avoid long relative imports:

```json
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@features/*": ["src/features/*"],
      "@shared/*": ["src/shared/*"]
    }
  }
}
```

| Instead of | Use |
|------------|-----|
| `../../../shared/components/Button` | `@shared/components/Button` |
| `../../features/auth` | `@features/auth` |

### Circular Dependency Prevention

- Features should never import from each other directly.
- Shared code goes in `shared/` or is lifted to a parent scope.
- If two features need the same logic, extract it to `shared/`.

```
✅  features/auth → shared/utils
✅  features/dashboard → shared/components
❌  features/auth → features/dashboard  (circular risk)
```

---

## Config Files

Modern web projects accumulate many config files. Keep them organized:

### Root Config Files

| File | Purpose |
|------|---------|
| `package.json` | Dependencies, scripts, project metadata |
| `tsconfig.json` | TypeScript compiler options |
| `vite.config.ts` / `next.config.js` / `webpack.config.js` | Build tool configuration |
| `.eslintrc.js` / `eslint.config.js` | Linting rules |
| `.prettierrc` | Code formatting |
| `.editorconfig` | Cross-editor whitespace/encoding |
| `.env` / `.env.local` | Environment variables (gitignored) |
| `.env.example` | Template showing required env vars (committed) |
| `tailwind.config.js` | Tailwind CSS configuration |
| `postcss.config.js` | PostCSS plugins |
| `.gitignore` | Files excluded from version control |
| `Dockerfile` / `docker-compose.yml` | Container definitions |

### When There Are Too Many Configs

If the root is cluttered, some teams consolidate into a `config/` folder — but only for custom configs. Tooling dotfiles (`.eslintrc`, `.prettierrc`) typically must stay at the root for auto-discovery.

---

## Test Organization

### Colocated Unit Tests (Recommended)

Place unit tests next to the code they test:

```
src/features/auth/
├── services/
│   ├── auth.service.ts
│   └── auth.service.test.ts    # Right next to the source
├── components/
│   ├── LoginForm.tsx
│   └── LoginForm.test.tsx
```

### Separate Test Directory for Integration & E2E

```
tests/
├── integration/
│   ├── auth.integration.test.ts
│   └── checkout.integration.test.ts
├── e2e/
│   ├── login.e2e.ts
│   └── signup.e2e.ts
└── fixtures/                   # Shared test data
    ├── users.json
    └── products.json
```

### Test Utilities

```
src/
└── test-utils/                 # Custom render functions, providers, mocks
    ├── render.tsx              # Wrapped render with providers
    ├── mocks/
    │   └── handlers.ts         # MSW request handlers
    └── factories/
        └── user.factory.ts     # Test data factories
```

---

## Documentation Structure

```
docs/
├── README.md                   # Docs index / overview
├── getting-started.md          # Setup and onboarding
├── architecture.md             # System design, diagrams
├── adr/                        # Architecture Decision Records
│   ├── 001-use-react.md
│   ├── 002-api-layer.md
│   └── template.md
├── guides/
│   ├── contributing.md
│   ├── coding-standards.md
│   └── deployment.md
└── api/                        # API documentation
    └── endpoints.md
```

### Architecture Decision Records (ADRs)

Capture the *why* behind structural decisions. Use a simple template:

```markdown
# ADR-001: Use feature-based folder structure

## Status: Accepted
## Date: 2026-03-13

## Context
The project is growing beyond 20 components and navigating by file type is becoming difficult.

## Decision
Organize src/ by feature domain rather than file type.

## Consequences
- Easier to find all code for a feature
- Requires discipline to keep shared code in shared/
```

---

## Monorepo Structure

For multi-package projects, use a workspace-based layout:

```
monorepo-root/
├── apps/
│   ├── web/                    # Main web application
│   │   ├── src/
│   │   └── package.json
│   ├── admin/                  # Admin dashboard
│   │   ├── src/
│   │   └── package.json
│   └── docs/                   # Documentation site
├── packages/
│   ├── ui/                     # Shared component library
│   │   ├── src/
│   │   └── package.json
│   ├── utils/                  # Shared utilities
│   └── config/                 # Shared configs (ESLint, TS, etc.)
│       ├── eslint/
│       └── typescript/
├── package.json                # Root workspace config
├── turbo.json / nx.json        # Build orchestration
└── pnpm-workspace.yaml         # Workspace definition
```

| Folder | Contains |
|--------|----------|
| `apps/` | Deployable applications |
| `packages/` | Shared libraries consumed by apps |
| `packages/config/` | Shared tooling configs extended by each app |

---

## Common Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Deeply nested folders (5+ levels) | Hard to navigate, long import paths | Flatten — restructure when a folder exceeds ~15 files |
| Dumping everything in `utils/` | Becomes a junk drawer | Split into focused modules: `date-utils`, `string-utils`, `validation` |
| One huge `components/` folder | 50+ components, no discoverability | Group by feature or by domain |
| No barrel files | Imports reach deep into internal modules | Add `index.ts` to define public API per folder |
| Mixed concerns in one folder | Tests, mocks, source, stories jumbled | Use consistent suffixes; colocate related files but name them clearly |
| Gittracking build output | Bloated repo, merge conflicts on artifacts | Add `dist/`, `build/`, `.next/` to `.gitignore` |
| Env files committed to repo | Leaked secrets | Only commit `.env.example`; gitignore actual `.env` files |
| Framework-specific names as top-level | `reducers/`, `actions/` — couples structure to implementation | Use domain names: `features/auth`, not `reducers/authReducer` |

---

## Quick Decision Guide

| Question | Answer |
|----------|--------|
| *Where does a new component go?* | Feature-specific → `src/features/<feature>/components/`. Shared → `src/shared/components/` |
| *Where does a new utility go?* | Used by one feature → that feature's folder. Used broadly → `src/shared/utils/` |
| *Where does a new API service go?* | `src/features/<feature>/services/` or `src/lib/api/` for shared clients |
| *Where do types go?* | Colocated next to the code that uses them. Shared types → `src/shared/types/` |
| *Where do global styles go?* | `src/styles/` for tokens, resets, and themes |
| *Where do tests go?* | Unit → next to source. Integration/E2E → `tests/` folder |
| *How do I name a new file?* | Components: PascalCase. Everything else: camelCase or kebab-case. Use role suffixes. |
| *When should I create a subfolder?* | When a folder has more than ~10–15 files, or when files naturally group by subdomain |
---

## Related Skills

- **[documentation-standards](https://github.com/skills/documentation-standards)** — Write clear, maintainable documentation that helps teams understand your codebase and architecture decisions.

**When to use this skill vs relevant skills:**
- Use **project-organization** when structuring the overall project, deciding where files go, setting up folder conventions, and organizing source code, tests, and documentation.
- Use **documentation-standards** when writing the actual documentation files that explain the project structure, architectural decisions, coding standards, or any guides that live in the `docs/` folder. This skill ensures your documentation is clear, consistent, and useful for onboarding and reference.
