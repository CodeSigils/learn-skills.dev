---
name: typescript-best-practices
description: TypeScript code quality and performance optimization guidelines for writing type-safe, maintainable code. Use when writing new TypeScript files, reviewing existing code, refactoring to improve type safety, optimizing build performance, or setting up TypeScript configuration. Triggers on tasks involving TypeScript, tsconfig, type definitions, generics, or type system design.
license: MIT
metadata:
  author: bilal-skills
  version: "1.0.0"
---

# TypeScript Best Practices

Act as a TypeScript expert advisor. Provide guidance on writing type-safe, performant, and maintainable TypeScript code following community best practices and the official TypeScript team recommendations.

## Purpose

This skill helps AI agents produce high-quality TypeScript code that leverages the type system effectively while avoiding common pitfalls. It covers type system design, configuration optimization, performance patterns, and project structure.

## When to Use

- Writing new TypeScript files or modules
- Reviewing existing TypeScript code for type safety issues
- Refactoring JavaScript to TypeScript
- Configuring `tsconfig.json` for a project
- Designing type definitions or generic APIs
- Optimizing TypeScript build and compilation performance
- Debugging complex type errors
- Setting up strict mode and linting integration
- Working with union/discriminated union types
- Implementing advanced patterns (branded types, type guards, assertion functions)

## When NOT to Use

- Writing pure JavaScript code that will not be migrated to TypeScript
- Projects using a different type system (Flow, ReasonML)
- Simple type annotations that are obvious (the agent should already handle these)
- When the user explicitly asks for non-TypeScript solutions

## Instructions

### 1. Configuration First

Before writing code, ensure:

- `strict: true` is enabled in `tsconfig.json`. Without it, the type system is significantly weaker.
- `noUncheckedIndexedAccess: true` for safer object access.
- `exactOptionalPropertyTypes: true` for stricter optional property handling.
- `verbatimModuleSyntax: true` for consistent module syntax.

### 2. Type System Design

#### Prefer interfaces over type aliases for object shapes

Interfaces are more extensible and produce clearer error messages. Use `type` for unions, intersections, mapped types, and utility patterns.

```typescript
// Prefer
interface User {
  id: string;
  name: string;
}

// Use type for
type Status = 'active' | 'inactive' | 'pending';
type DeepPartial<T> = { [K in keyof T]?: DeepPartial<T[K]> };
```

#### Use branded types for domain primitives

Prevent mixing up values that share the same underlying type but represent different concepts.

```typescript
type Brand<T, B> = T & { __brand: B };
type UserId = Brand<string, 'UserId'>;
type OrderId = Brand<string, 'OrderId'>;

function getUser(id: UserId): User { /* ... */ }
function getOrder(id: OrderId): Order { /* ... */ }

// TypeScript prevents: getUser(orderId)
```

#### Leverage discriminated unions for state management

Model states explicitly so invalid states are unrepresentable.

```typescript
type RequestState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error };

function renderState(state: RequestState<User>) {
  switch (state.status) {
    case 'idle': return null;
    case 'loading': return <Spinner />;
    case 'success': return <UserProfile user={state.data} />;
    case 'error': return <ErrorMessage error={state.error} />;
  }
}
```

#### Prefer type inference over explicit annotations

Let TypeScript infer types when the type is obvious from context. Add explicit annotations at module boundaries (function signatures, exported API surface).

```typescript
// Good: inferred
const items = [1, 2, 3];

// Good: explicit at boundary
export function processItems(items: number[]): Result[] { /* ... */ }

// Unnecessary
const name: string = 'hello';
```

### 3. Generics and Utility Types

#### Constrain generics with the minimal required shape

```typescript
// Instead of
function clone<T>(obj: T): T { return JSON.parse(JSON.stringify(obj)); }

// Prefer
function clone<T extends Record<string, unknown>>(obj: T): T { return JSON.parse(JSON.stringify(obj)); }
```

#### Use `satisfies` for type validation without widening

```typescript
const palette = {
  red: [255, 0, 0],
  green: '#00ff00',
  blue: [0, 0, 255],
} satisfies Record<string, string | number[]>;

// palette.red is number[] (not string | number[])
// palette.green is string (not string | number[])
```

### 4. Strictness Patterns

#### Use `as const` for literal types and readonly tuples

```typescript
const COLORS = ['red', 'green', 'blue'] as const;
type Color = (typeof COLORS)[number]; // 'red' | 'green' | 'blue'
```

#### Prefer `unknown` over `any`

`unknown` forces type checking before use. Reserve `any` for migration scenarios only.

```typescript
// Prefer
function parseJSON(input: string): unknown {
  return JSON.parse(input);
}

// Avoid
function parseJSON(input: string): any {
  return JSON.parse(input);
}
```

#### Use type guards and assertion functions

```typescript
function isError(value: unknown): value is Error {
  return value instanceof Error;
}

function assertString(value: unknown): asserts value is string {
  if (typeof value !== 'string') {
    throw new TypeError('Expected string');
  }
}
```

### 5. Performance Optimization

#### Prefer interfaces for object types

Interfaces are faster for the compiler to check than type aliases due to caching.

#### Avoid large union types

Break large unions (100+ members) into smaller, composable types. Consider using branded types or enums for finite sets.

#### Use `ts-reset` or explicit narrowing

Import `@total-typescript/ts-reset` for better array and Promise type inference. Otherwise, manually narrow with explicit checks.

#### Avoid excessive conditional types

Deeply nested conditional types slow down compilation. Prefer mapped types or lookup types when possible.

### 6. Error Handling

#### Use Result types for expected failures

```typescript
type Result<T, E = Error> = { success: true; value: T } | { success: false; error: E };

function divide(a: number, b: number): Result<number> {
  if (b === 0) return { success: false, error: new Error('Division by zero') };
  return { success: true, value: a / b };
}
```

#### Use typed `try/catch` with error handling

```typescript
try {
  await riskyOperation();
} catch (error) {
  if (error instanceof ApiError) {
    handleApiError(error);
  } else if (error instanceof NetworkError) {
    retry();
  } else {
    throw error;
  }
}
```

## Examples

### Before (untyped)
```typescript
function process(data) {
  return data.map(item => item.value);
}
```

### After (type-safe)
```typescript
interface DataItem {
  id: string;
  value: number;
}

function process(data: DataItem[]): number[] {
  return data.map(item => item.value);
}
```

### API Response Handling
```typescript
interface ApiResponse<T> {
  data: T;
  timestamp: string;
  version: number;
}

async function fetchApi<T>(url: string): Promise<ApiResponse<T>> {
  const response = await fetch(url);
  if (!response.ok) throw new ApiError(response.status, await response.text());
  return response.json();
}
```

## Best Practices

- Enable `strict: true` in every project. This catches the majority of type errors.
- Use `@ts-expect-error` instead of `@ts-ignore` when you must suppress an error. `@ts-expect-error` will warn you if the error is no longer relevant, while `@ts-ignore` silently suppresses forever.
- Keep functions small and focused. TypeScript's type inference works best with small, pure functions.
- Prefer `interface` over `type` for public API shapes. Interfaces are more extensible and produce better editor tooling.
- Use `const` assertions for constant tuples and configurations.
- Export types that consumers of your library or module need.
- Write unit tests for your type definitions using `expectTypeOf` from `vitest` or `ts-expect`.

## Common Mistakes

- **Using `any` instead of `unknown`**: `any` disables type checking entirely. Always prefer `unknown` and narrow the type before use.
- **Over-using type assertions (`as`)**: Type assertions hide type errors. Prefer type guards and constructor functions.
- **Missing `strict: true`**: Without strict mode, TypeScript misses null checks, implicit any, and other common errors.
- **Complex generic signatures**: If a generic type signature is hard to read, it is probably too complex. Break it down or use simpler patterns.
- **Ignoring `noUncheckedIndexedAccess`**: Accessing object properties without checking for `undefined` leads to runtime errors.
- **Defining types in the same file as implementation**: Keep type definitions in separate `.types.ts` files for better organization.

## Expected Output

When this skill is triggered, the agent should produce:

1. Type-safe code with proper annotations at module boundaries
2. Fully configured `tsconfig.json` with strict mode enabled
3. Discriminated unions for state management where applicable
4. Branded types for domain primitives to prevent type confusion
5. Proper error handling with typed error variants
6. Clean, readable generics constrained to the minimum required shape
7. Inline documentation only where the type signature is non-obvious

## Limitations

- This skill does not cover runtime validation libraries like Zod or Yup (consider installing a separate skill for those).
- This skill does not cover framework-specific TypeScript patterns for React, Next.js, or Angular.
- TypeScript compilation performance depends on project size; this skill provides general guidance but cannot fix inherent scalability limits of the TypeScript compiler.
- Some pattern recommendations may conflict with existing codebase conventions; always respect the project's established style.
