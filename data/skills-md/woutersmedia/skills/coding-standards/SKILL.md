---
name: coding-standards
description: Wouters Media coding standards - TypeScript strict typing, export const components, no FC, no React namespace, server-side first, file naming, and implementation standards.
---

# Wouters Media Coding Standards

Apply these rules whenever writing or reviewing code in Wouters Media projects.

## TypeScript Strict Typing

**CRITICAL: No `any`, `unknown`, or `never` types.**

```typescript
// ❌ FORBIDDEN
function processData(data: any) { return data.value; }

// ✅ CORRECT
interface Data { value: string; }
function processData(data: Data): string { return data.value; }
```

Error handling:

```typescript
// ❌ FORBIDDEN
} catch (error: any) { console.log(error.message); }

// ✅ CORRECT
} catch (error) {
  if (error instanceof Error) {
    console.log(error.message);
  }
}
```

## Component Export Style

**Always use `export const`, never `export function` for components and utilities.**

```typescript
// ❌ FORBIDDEN
export function Button({ children }: ButtonProps) { ... }

// ✅ CORRECT
export const Button = ({ children }: ButtonProps) => { ... };
```

## React Imports — No `React.` Namespace

**Never use `React.FC`, `React.ReactNode`, `React.useState`, etc. Import directly.**

```typescript
// ❌ FORBIDDEN
import React from 'react';
const Component: React.FC<Props> = ({ children }) => { ... };

// ❌ FORBIDDEN
const Component: FC<Props> = ({ children }) => { ... };

// ✅ CORRECT
import { type ReactNode } from 'react';
export const Component = ({ children }: { children: ReactNode }) => { ... };
```

Common React type imports (never import `FC` or `FunctionComponent`):

```typescript
import {
  type ReactNode,
  type ComponentProps,
  type ChangeEvent,
  type FormEvent,
  useState,
  useMemo,
  useRef,
} from "react";
```

## Component Structure

Props interface defined above the component, typed inline:

```typescript
interface ButtonProps {
  children: ReactNode;
  onClick?: () => void;
  disabled?: boolean;
  variant?: 'primary' | 'secondary';
}

export const Button = ({
  children,
  onClick,
  disabled = false,
  variant = 'primary',
}: ButtonProps) => {
  return (
    <button onClick={onClick} disabled={disabled}>
      {children}
    </button>
  );
};
```

## Server-Side First

Prefer server components and server-side logic wherever possible:

```typescript
// ✅ CORRECT — server component (default, no directive)
export const Page = async () => {
  const data = await fetchFromDatabase();
  return <Component data={data} />;
};

// Only use client components when interactivity is required
"use client";
```

## File Naming

- Components: `PascalCase.tsx` → `Button.tsx`, `UserProfile.tsx`
- Utilities: `camelCase.ts` → `formatDate.ts`, `apiClient.ts`
- Types: `PascalCase.ts` → `User.ts`, `Booking.ts`
- Tests: `*.test.ts` or `*.test.tsx`

## Import Paths

- Components: `@/components/Example/Example` (PascalCase folder + file)
- ShadCN UI: `@/components/ui/button` (lowercase, kebab-case)
- All paths use `@/` alias for absolute imports

## 🛠️ Implementation Standards

- **Project Artifacts**: Do **NOT** create `output.txt`, `tsconfig.tsbuildinfo`, or other temporary files.
- **KISS & DRY**: Keep it simple. Remove unused code, props, and imports. Minimize abstractions.
- **Strict Typing**: No `any`, `unknown`, or `never`. We want robust types.

## See Also

- `rules/use-effect.md` — when and how to avoid `useEffect`
- `rules/component-architecture.md` — components vs containers vs app directory
- `rules/multilingual-labels.md` — localization requirements
- `rules/general.md` — naming conventions and error handling

