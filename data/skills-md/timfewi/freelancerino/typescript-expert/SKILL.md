---
name: typescript-expert
description: Use this skill when writing, reviewing, or refactoring TypeScript code for type safety, idiomatic patterns, and modern best practices.
metadata:
  applyTo: "**/*.ts, **/*.tsx"
---

# TypeScript Expert Skill

Universal TypeScript best practices for type safety, maintainability, and performance.

## Core Philosophy

> **Types are documentation the compiler enforces.**

Write types that make illegal states unrepresentable. Prefer compile-time errors over runtime errors.

## 1. Type Safety Fundamentals

### Enable Strict Mode

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "exactOptionalPropertyTypes": true
  }
}
```

### Prefer `unknown` Over `any`

```ts
// ❌ any bypasses all type checking
function process(data: any) {
  return data.foo.bar; // No error, crashes at runtime
}

// ✅ unknown forces narrowing
function process(data: unknown) {
  if (typeof data === "object" && data !== null && "foo" in data) {
    // Safe to access
  }
}
```

### Use `as const` for Literal Types

```ts
// Type: { method: string }
const req = { method: "GET" };

// Type: { readonly method: "GET" }
const req = { method: "GET" } as const;

// Arrays become readonly tuples
const colors = ["red", "green", "blue"] as const;
// Type: readonly ["red", "green", "blue"]
```

### Type Narrowing

```ts
// typeof guard
function format(value: string | number) {
  if (typeof value === "string") {
    return value.toUpperCase();
  }
  return value.toFixed(2);
}

// in operator
function move(animal: Fish | Bird) {
  if ("swim" in animal) return animal.swim();
  return animal.fly();
}

// Custom type predicate
function isString(value: unknown): value is string {
  return typeof value === "string";
}
```

## 2. Discriminated Unions

Model state and variants with a shared discriminant property:

```ts
type Result<T, E = Error> =
  | { status: "ok"; data: T }
  | { status: "error"; error: E };

function handle(result: Result<User>) {
  if (result.status === "ok") {
    console.log(result.data);  // TS knows data exists
  } else {
    console.log(result.error); // TS knows error exists
  }
}
```

### Exhaustiveness with `never`

```ts
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; side: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "square":
      return shape.side ** 2;
    default:
      const _exhaustive: never = shape;
      throw new Error(`Unhandled: ${_exhaustive}`);
  }
}
```

## 3. Generics

### Constrain Properly

```ts
// ❌ Too loose
function getProp<T>(obj: T, key: string) {
  return obj[key]; // Error
}

// ✅ Constrained
function getProp<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}
```

### Provide Defaults

```ts
type Response<T = unknown, E = Error> = {
  data: T | null;
  error: E | null;
};
```

### Generics vs Overloads

```ts
// ❌ Overloads are verbose
function parse(input: string): string;
function parse(input: number): number;
function parse(input: string | number) { return input; }

// ✅ Generic is cleaner
function parse<T extends string | number>(input: T): T {
  return input;
}
```

### Keep Generics Minimal

```ts
// ❌ Unused generic
function greet<T>(name: string): string { return `Hello, ${name}`; }

// ✅ No generic needed
function greet(name: string): string { return `Hello, ${name}`; }
```

## 4. Utility Types

```ts
Partial<T>       // All properties optional
Required<T>      // All properties required
Pick<T, K>       // Select properties
Omit<T, K>       // Exclude properties
Record<K, V>     // Key-value map
NonNullable<T>   // Remove null/undefined
ReturnType<F>    // Function return type
Parameters<F>    // Function parameters as tuple
Awaited<T>       // Unwrap Promise
Exclude<T, U>    // Remove union members
Extract<T, U>    // Keep union members
```

### Common Patterns

```ts
// Make all optional
type Draft<T> = Partial<T>;

// Select fields
type UserPreview = Pick<User, "id" | "name">;

// Exclude fields
type PublicUser = Omit<User, "password" | "email">;

// Typed dictionary
type UserMap = Record<string, User>;

// Remove nullability
type Defined<T> = NonNullable<T>;
```

## 5. Advanced Type Patterns

### Template Literal Types

```ts
type EventName = `on${Capitalize<"click" | "focus">}`;
// "onClick" | "onFocus"

type Route = `/${string}`;
type CSSValue = `${number}${"px" | "rem" | "%"}`;
```

### Conditional Types with `infer`

```ts
// Extract return type
type Return<T> = T extends (...args: never[]) => infer R ? R : never;

// Unwrap Promise
type Unwrap<T> = T extends Promise<infer U> ? U : T;

// Array element type
type Element<T> = T extends (infer E)[] ? E : never;
```

### Mapped Types

```ts
// Add readonly
type Immutable<T> = { readonly [K in keyof T]: T[K] };

// Remove readonly
type Mutable<T> = { -readonly [K in keyof T]: T[K] };

// Rename keys
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};
```

## 6. Module Patterns

### Type-Only Imports

```ts
// ✅ Explicit type imports
import type { User, Config } from "./types";
import { createUser } from "./users";

// ✅ Inline type import
import { createUser, type User } from "./users";
```

### Enable `verbatimModuleSyntax`

```json
{
  "compilerOptions": {
    "verbatimModuleSyntax": true
  }
}
```

## 7. Interface vs Type

| Use `interface` for | Use `type` for |
|---------------------|----------------|
| Object shapes | Unions |
| Extensible contracts | Intersections |
| Class implementations | Mapped types |
| Declaration merging | Function types |

```ts
// Interface for extensible shapes
interface User {
  id: string;
  name: string;
}

// Type for unions and compositions
type Status = "active" | "inactive";
type UserWithStatus = User & { status: Status };
```

## 8. Function Signatures

### Callbacks: Use `void`, Not `any`

```ts
// ❌ any allows accidental use of return value
function run(cb: () => any) { cb(); }

// ✅ void prevents using return value
function run(cb: () => void) { cb(); }
```

### Overloads: Specific First

```ts
// ❌ General overload first hides specific ones
declare function fn(x: unknown): unknown;
declare function fn(x: HTMLElement): number;

// ✅ Specific overloads first
declare function fn(x: HTMLDivElement): string;
declare function fn(x: HTMLElement): number;
declare function fn(x: unknown): unknown;
```

### Prefer Union Over Multiple Overloads

```ts
// ❌ Verbose
interface Moment {
  utcOffset(b: number): Moment;
  utcOffset(b: string): Moment;
}

// ✅ Union type
interface Moment {
  utcOffset(b: number | string): Moment;
}
```

## 9. Error Handling

### Result Type Pattern

```ts
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

function divide(a: number, b: number): Result<number, string> {
  if (b === 0) return { ok: false, error: "Division by zero" };
  return { ok: true, value: a / b };
}

const result = divide(10, 2);
if (result.ok) {
  console.log(result.value);
} else {
  console.error(result.error);
}
```

### Typed Custom Errors

```ts
class ValidationError extends Error {
  constructor(
    message: string,
    public readonly field: string,
    public readonly code: string
  ) {
    super(message);
    this.name = "ValidationError";
  }
}
```

## 10. Performance

### Prefer Interfaces Over Intersections

```ts
// ❌ Slower for type checker
type Extended = Base & { extra: string };

// ✅ Faster
interface Extended extends Base {
  extra: string;
}
```

### Enable Incremental Builds

```json
{
  "compilerOptions": {
    "incremental": true,
    "tsBuildInfoFile": "./.tsbuildinfo"
  }
}
```

### Use Project References

```json
{
  "references": [
    { "path": "./packages/core" },
    { "path": "./packages/ui" }
  ]
}
```

## Quick Reference

| You're doing... | Don't use | Use instead |
|-----------------|-----------|-------------|
| Unknown input | `any` | `unknown` + narrowing |
| Operation result | `T \| null` | Discriminated union |
| Immutable value | `let` | `as const` |
| Object shape | `type` | `interface` (if extendable) |
| Union/mapped | `interface` | `type` |
| Callback return | `any` | `void` |
| Type assertion | `as Type` | Type guard or narrowing |
| Deep nesting | Manual recursion | Utility types |

## Red Flags

| Pattern | Problem | Fix |
|---------|---------|-----|
| `any` | Disables type checking | Use `unknown` |
| `as Type` | Hides type errors | Narrow properly |
| `!` non-null | Runtime error risk | Handle null case |
| `// @ts-ignore` | Suppresses real errors | Fix the type |
| Unused generic | Adds complexity | Remove it |
| `Object` type | Wrong type | Use `object` |

## References

- TypeScript Handbook: https://www.typescriptlang.org/docs/handbook/
- Do's and Don'ts: https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html
- Creating Types from Types: https://www.typescriptlang.org/docs/handbook/2/types-from-types.html
- Narrowing: https://www.typescriptlang.org/docs/handbook/2/narrowing.html
- Utility Types: https://www.typescriptlang.org/docs/handbook/utility-types.html
- TSConfig Reference: https://www.typescriptlang.org/tsconfig/
- Effective TypeScript (book by Dan Vanderkam)
