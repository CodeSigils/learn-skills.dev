---
name: coding-guidelines
description: Wouters Media coding standards index. Use when writing or reviewing code in any project. Covers React/TypeScript style, DRY, tests, styling, database, component architecture, and i18n. Triggers on tasks involving components, API routes, database, tests, or general project standards.
---

# Coding Guidelines

Comprehensive Wouters Media coding rules. Apply these when writing or reviewing any code in Wouters Media projects.

## Core Standards

See also: `coding-standards` skill for TypeScript strict typing, exports, React imports, file naming.

---

## General React / TypeScript Style

- **No `any`, `unknown`, or `never` types.** Use explicit interfaces and type unions.
- **No `React.` prefix.** Import types and hooks directly from `"react"`.
- **No `FC` or `FunctionComponent`.** Type props via an interface; let TypeScript infer the return type.
- Files should stay **under 100 lines**. Split large files into focused modules.

```typescript
// ❌ FORBIDDEN
import React from "react";
const MyComponent: React.FC<{ name: string }> = ({ name }) => <p>{name}</p>;

// ✅ CORRECT
import { type ReactNode } from "react";

interface MyComponentProps {
  name: string;
  children?: ReactNode;
}

export const MyComponent = ({ name, children }: MyComponentProps) => (
  <p>
    {name}
    {children}
  </p>
);
```

Always `export const`, never `export function` for components and utilities.

```typescript
// ❌ FORBIDDEN
export function Button({ children }: ButtonProps) { ... }

// ✅ CORRECT
export const Button = ({ children }: ButtonProps) => { ... };
```

**Naming Conventions**

| Artifact   | Convention  | Example                    |
| ---------- | ----------- | -------------------------- |
| Component  | PascalCase  | `UserProfile.tsx`          |
| Container  | PascalCase  | `UserProfileContainer.tsx` |
| Utility    | camelCase   | `formatDate.ts`            |
| Type file  | PascalCase  | `User.ts`                  |
| Test file  | `*.test.ts` | `UserProfile.test.tsx`     |

**Error Handling**

```typescript
// ❌ FORBIDDEN
} catch (error: any) { console.error(error.message); }

// ✅ CORRECT
} catch (error) {
  if (error instanceof Error) {
    console.error(error.message);
  }
}
```

---

## DRY — Don't Repeat Yourself

**Keep It Simple and Don't Repeat Yourself.** Every piece of logic should have a single, authoritative representation in the codebase.

- Remove unused code, props, variables, and imports immediately.
- Extract repeated logic into a shared utility or hook — but only when it is used in **two or more** places.
- Prefer composing small, focused functions over large, multi-purpose ones.
- Minimize abstraction layers; a direct solution is almost always clearer than a generic one.

```typescript
// ❌ AVOID — same fetch pattern copy-pasted across containers
const res = await fetch(new URL("/api/users", window.location.origin).toString());

// ✅ CORRECT — shared utility
export const apiFetch = <T>(path: string): Promise<T> =>
  fetch(new URL(path, window.location.origin).toString()).then((r) => {
    if (!r.ok) throw new Error(`API error ${r.status}`);
    return r.json() as Promise<T>;
  });
```

Do not create an abstraction for code that appears similar but serves different domains or may diverge in the future.

---

## Avoid `useEffect` — Prefer Alternatives

**`useEffect` is discouraged as a default choice.**

**Derived values → use `useMemo`**

```typescript
// ❌ AVOID — derived value computed in useEffect
useEffect(() => {
  setFiltered(items.filter((i) => i.name.includes(searchTerm)));
}, [items, searchTerm]);

// ✅ CORRECT — useMemo for derived values
const filtered = useMemo(
  () => items.filter((i) => i.name.includes(searchTerm)),
  [items, searchTerm],
);
```

**Data fetching → use server components**

```typescript
// ❌ AVOID — client-side data fetching in useEffect
useEffect(() => {
  fetch("/api/items").then((r) => r.json()).then(setItems);
}, []);

// ✅ CORRECT — server component fetches data directly
export const ItemListPage = async () => {
  const items = await getItems();
  return <ul>{items.map((i) => <li key={i.id}>{i.name}</li>)}</ul>;
};
```

Only use `useEffect` for genuine external-system synchronisation (WebSockets, imperative DOM APIs, third-party SDK initialisation). Always include a cleanup function.

---

## Component Architecture

**Presentation in `/components`. Logic and data in `/containers`. Nothing else in `app/` except framework files.**

**Components (`/components`)** are dumb and presentational:
- Accept all data via props
- Return JSX with no side effects, no data fetching
- Do not access global state or stores

**Containers (`/containers`)** are smart orchestrators:
- Fetch data (server-side preferred) or call mutations
- Contain business logic and access global state
- Delegate all complex rendering to components

**App Directory (`/app`)** — only these file types:
- `page.tsx`, `layout.tsx`, `error.tsx`, `loading.tsx`, `not-found.tsx`, `route.ts`
- **No custom components in `app/`.** Move them to `/components` or `/containers`.

**File naming:**
- `components/ComponentName/ComponentName.tsx` — PascalCase folder + matching filename
- `containers/ContainerName.tsx` — PascalCase, no subfolder needed unless complex
- Always `export const`, never `export default` for components (pages are the exception)

---

## Testing

Every non-trivial feature must have tests. Aim for meaningful coverage, not 100% line coverage.

- `ComponentName.test.tsx` — component tests
- `utilityName.test.ts` — utility/hook tests
- Co-locate test files with the source they test, or place them in a `__tests__/` sibling directory.

Use **React Testing Library** — test behaviour, not implementation details.

```typescript
import { render, screen, fireEvent } from "@testing-library/react";

describe("SaveButton", () => {
  it("calls onSave when clicked", () => {
    const onSave = jest.fn();
    render(<SaveButton onSave={onSave} />);
    fireEvent.click(screen.getByRole("button", { name: /save/i }));
    expect(onSave).toHaveBeenCalledTimes(1);
  });
});
```

Mock external dependencies (Prisma, fetch, third-party SDKs) — never call live services in tests.

Do **not** test implementation internals, snapshot-test large component trees, or remove/skip existing tests without a documented reason.

---

## Styling

**Tailwind CSS only. No inline `style` props, no CSS modules, no styled-components.**

```typescript
// ❌ FORBIDDEN — inline styles
<div style={{ marginTop: "16px", color: "#6b7280" }}>Content</div>

// ✅ CORRECT — Tailwind utilities
<div className="mt-4 text-muted-foreground">Content</div>
```

Prefer design-token classes (`text-primary`, `bg-background`, `border-border`) over raw color values when the project has a design system. Use mobile-first responsive prefixes.

Inline `style` is only allowed for truly dynamic runtime values (e.g. `style={{ width: `${percentage}%` }}`).

---

## Database Schema

**Use a typed ORM or query builder for all database access.** Preferred: [Prisma](https://www.prisma.io/).

After editing `schema.prisma`, always regenerate the client:

```bash
npx prisma generate
```

**Schema conventions:**
- Model names: PascalCase in ORM, snake_case in DB (`@@map("users")`)
- Field names: camelCase in code, snake_case in DB
- Always include `createdAt` and `updatedAt` timestamp fields
- Use a generated unique ID (`cuid`, `uuid`) as the primary key

```prisma
// ✅ CORRECT
model User {
  id        String   @id @default(cuid())
  name      String
  email     String   @unique
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@map("users")
}
```

Prefer typed ORM queries over raw SQL. Catch and translate database-level errors into meaningful application errors.

---

## i18n — Multilingual Labels

**Never hardcode Dutch (or any language) text.** All user-visible strings must use the i18n translation system. All **code** (variable names, comments, function names) must be written in **English**.

```typescript
// ❌ FORBIDDEN
<h1>Welkom</h1>
<h1>Welcome</h1>  // still forbidden for UI text

// ✅ CORRECT — server component
const t = await getTranslation(locale, "common");
return <h1>{t("welcome")}</h1>;

// ✅ CORRECT — client component
const { t } = useTranslation("common");
return <button>{t("save")}</button>;
```

Always add new keys to **both** `en.json` and `nl.json` simultaneously.

Navigation items use dot-notation translation keys:

```typescript
// ❌ FORBIDDEN
{ label: "Instellingen", href: "/settings" }

// ✅ CORRECT
{ labelKey: "nav.settings", href: "/settings" }
```

---

## Middleware Prohibition

**Never create, suggest, or mention `middleware.ts`.**

Routing and authentication are handled exclusively by `apps/proxy.ts`. Next.js `middleware.ts` conflicts with the existing proxy-based routing architecture. If Next.js warns about missing middleware, do **not** create `middleware.ts` — inform the user that routing is managed via the proxy.
