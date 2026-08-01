---
name: typescript-expert
description: >-
  TypeScript type-level programming, performance tuning, monorepo management, and tooling.
  Use for complex type gymnastics, build performance, TypeScript migration, or TS debugging.
  NOT for React-specific patterns (use react-pro) or Node.js architecture (use nodejs-pro).
metadata:
  author: pikakit
  version: "3.9.213"
  category: typesystem-engineering
  triggers: ["TypeScript", "JavaScript", "type error", "tsconfig", "monorepo"]
  coordinates_with: ["nextjs-pro", "code-review"]
  success_metrics: ["Type Coverage", "Build Performance", "Determinism"]
---

# TypeScript Expert — Advanced TS Problem-Solving

> Strict mode. ESM-first. Type-level patterns. Deterministic error routing.

---

## 5 Must-Ask Questions (Socratic Gate)

| # | Question | Options |
|---|----------|---------|
| 1 | TS Version? | 5.0+ / Legacy |
| 2 | Build System? | Vite / Next.js / tsc / tsup |
| 3 | Project Structure? | Monorepo / Polyrepo |
| 4 | Module Target? | ESM / CJS / Dual |
| 5 | Strictness Level? | Full Strict / Gradual Migration |

---

## When to Use

| Situation | Approach |
|-----------|----------|
| Type errors | Check error routing table |
| Build performance | See performance settings |
| Monorepo setup | Check project references |
| Migration strategy | See rules/migration.md |
| Module issues | ESM-first config |

---

## System Boundaries

| Owned by This Skill | NOT Owned |
|---------------------|-----------|
| Type-level patterns (3) | Next.js integration (→ nextjs-pro) |
| Error → fix routing (4 errors) | React patterns (→ react-architect) |
| Performance config (3 settings) | Code review (→ code-review) |
| Strict config + ESM-first | Build tooling (Vite/webpack) |

**Expert decision skill:** Produces TS guidance. Does not execute compilers.

---

## Diagnostics (3 Commands)

| Task | Command |
|------|---------|
| Type check | `npx tsc --noEmit` |
| Performance | `npx tsc --extendedDiagnostics` |
| Trace resolution | `npx tsc --traceResolution` |

---

## Common Errors (4 — Deterministic Routing)

| Error | Fix |
|-------|-----|
| "Cannot be named" | Export type explicitly |
| "Excessive depth" | Limit recursion, use `interface` instead of `type` |
| "Cannot find module" | Check `moduleResolution: "bundler"` |
| Missing types | Add ambient declaration (`.d.ts`) |

---

## Type-Level Patterns (3)

### Branded Types
```typescript
type Brand<K, T> = K & { __brand: T };
type UserId = Brand<string, 'UserId'>;
```

### Deep Readonly
```typescript
type DeepReadonly<T> = T extends object
  ? { readonly [K in keyof T]: DeepReadonly<T[K]> }
  : T;
```

### Satisfies (TS 5.0+)
```typescript
const config = {
  api: "https://api.example.com",
  timeout: 5000
} satisfies Record<string, string | number>;
```

---

## Strict Config (Recommended — Fixed)

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true
  }
}
```

## ESM-First Config (Fixed)

```json
{
  "type": "module",
  "moduleResolution": "bundler"
}
```

---

## Performance Settings (3 — Fixed)

| Setting | Effect |
|---------|--------|
| `skipLibCheck: true` | Skip library type checking |
| `incremental: true` | Cache builds |
| Project references | Monorepo parallel builds |

---

## Error Taxonomy

| Code | Recoverable | Trigger |
|------|-------------|---------|
| `ERR_INVALID_REQUEST_TYPE` | No | Request type not supported |
| `ERR_UNKNOWN_ERROR` | Yes | tsc error not in routing table |
| `ERR_UNSUPPORTED_VERSION` | Yes | TS version below 5.0 |
| `ERR_UNKNOWN_PROJECT_TYPE` | Yes | Not app, library, or monorepo |

**Zero internal retries.** Same error = same fix.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `any` type spreading | Enable `noImplicitAny` in tsconfig |
| Module resolution fails | Set `moduleResolution: "bundler"` (TS 5+) |
| Slow type checking | Use project references, `skipLibCheck: true` |
| ESM/CJS mismatch | Set `"type": "module"` in package.json |

---

## Audit Logging (OpenTelemetry)

| Event | Metadata Payload | Severity |
|-------|------------------|----------|
| `type_pattern_recommended` | `{"pattern": "branded_types", "use_case": "ids"}` | `INFO` |
| `error_resolved` | `{"error_code": "TS2322", "fix_applied": "type_assertion"}` | `INFO` |
| `config_recommended` | `{"project_type": "monorepo", "settings": ["projectReferences"]}` | `INFO` |

All typescript-expert outputs MUST emit `type_pattern_recommended`, `error_resolved`, or `config_recommended` events when applicable.

---

## 📑 Content Map

| File | Description | When to Read |
|------|-------------|--------------|
| [tsconfig-strict.json](rules/tsconfig-strict.json) | Strict TS 5.x config template | New project setup |
| [typescript-cheatsheet.md](rules/typescript-cheatsheet.md) | Full TS quick reference (13 sections) | Writing TypeScript |
| [utility-types.js](rules/utility-types.js) | Runtime utilities (Result, Option, Brand) | JavaScript helpers |
| [type-patterns.md](rules/type-patterns.md) | Advanced type patterns | Type gymnastics |
| [performance.md](rules/performance.md) | Build performance | Slow builds |
| [monorepo.md](rules/monorepo.md) | Monorepo setup | Project references |
| [migration.md](rules/migration.md) | Migration strategies | Version upgrades |
| [engineering-spec.md](rules/engineering-spec.md) | Full spec | Architecture review |

---

## 🔗 Related

| Item | Type | Purpose |
|------|------|---------|
| `nextjs-pro` | Skill | Next.js + TS |
| `react-architect` | Skill | React + TS |
| `code-review` | Skill | Code quality |

---

⚡ PikaKit v3.9.213
