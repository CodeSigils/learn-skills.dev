---
name: typescript
description: TypeScript conventions and best practices. Use when writing any TypeScript code, whether frontend or backend.
user-invocable: false
---

# TypeScript Conventions

## Naming Conventions

| Item | Style | Example |
|------|-------|---------|
| Types, interfaces, enums | `PascalCase` | `UserProfile`, `HttpStatus` |
| Functions, variables, methods | `camelCase` | `getUserById`, `isActive` |
| Constants | `UPPER_CASE` | `MAX_RETRIES`, `API_BASE_URL` |
| File names (modules) | `camelCase` or `kebab-case` | `userService.ts`, `user-service.ts` — follow project convention |
| Generic type parameters | Single uppercase or short `PascalCase` | `T`, `K`, `V`, `TResult` |

- **No `I` prefix on interfaces** — `User` not `IUser`. TypeScript makes no runtime distinction
- **No `T` prefix on types** — `Props` not `TProps`
- **Boolean names**: Use `is`, `has`, `can`, `should` prefixes — `isActive`, `hasPermission`

## `unknown` vs `any`

- **`any` is banned** — no exceptions
- Use `unknown` when the type is uncertain, then narrow with type guards before use
- External packages missing types: create `types.d.ts` to define types, not `any`
- When type constraints are truly unsolvable, use `as unknown as Xxx` with a comment explaining why — never `as any`

## Type Assertions

- Avoid `as` — prefer type guards or discriminated unions to let the compiler narrow automatically
- Prefer `satisfies` over `as` — `satisfies` checks the type without overriding inference
- When `as` is unavoidable, use `as unknown as Xxx` and add a comment explaining why

## Type Narrowing

- Use discriminated unions (shared literal field) to represent multiple states, with `switch` for exhaustive checking
- Use type guard functions (`function isFoo(x): x is Foo`) to encapsulate complex type checks
- For simple cases, use `typeof`, `instanceof`, `in` directly
- `satisfies` operator: checks type conformance without widening the inferred type

## Discriminated Unions

- Use a shared literal field (typically `type`, `kind`, `status`) to distinguish each variant
- `switch` with `default: never` for exhaustive checking — the compiler errors when a new variant is added
- Prefer discriminated unions over stacking optional fields — make invalid states unrepresentable

## Interface vs Type

- Prefer `interface` for object shapes and contracts — supports declaration merging, `extends` inheritance, and works well as abstraction boundaries
- Prefer `type` for unions, intersections, mapped types, and conditional types
- Both can describe object structures — no strict enforcement, follow project conventions

## Generic Constraints

- Use `extends` to constrain generics — `<T extends HasId>` not unconstrained `<T>`
- Use `keyof` for safe object key access — `<K extends keyof T>`
- Keep generics simple — if more than 2-3 type parameters, consider splitting or simplifying the design
- Conditional types (`T extends U ? X : Y`) only in library/utility types — avoid complex type gymnastics in business logic

## Type Inference

- Let TypeScript infer what it can — local variables and function return values usually don't need explicit annotations
- **Must annotate**: function parameters, public API return types, exported constants
- If inference produces unexpected results, restructure the code rather than adding type assertions

## Utility Types

- Use built-in utility types: `Partial`, `Required`, `Pick`, `Omit`, `Record`, `Readonly`, `ReturnType`, `Parameters`, etc.
- Use `Pick` / `Omit` to derive from existing types — avoid duplicating similar interfaces
- `Record<K, V>` over `{ [key: string]: V }` — more explicit semantics

## `as const`

- Use `as const` for literal types and readonly tuples — prevents widening to `string`, `number`
- Combine with `typeof` to extract types from `as const` objects, instead of manually maintaining a separate type definition

## Enum Alternatives

- Avoid `enum` — causes tree-shaking issues and generates extra runtime code
- Prefer `as const` objects or string union types
- Example: `const Status = { Active: 'active', Inactive: 'inactive' } as const` with `type Status = typeof Status[keyof typeof Status]`

## Nullability

- Enable `strict: true` (includes `strictNullChecks`) — disallow implicit `null`/`undefined`
- Use optional chaining `?.` for safe access on potentially null properties
- Use nullish coalescing `??` for defaults — prefer over `||` (`||` treats `0`, `""` as falsy)
- Avoid non-null assertion `!` — prefer type guards or early returns

## Branded Types

- Use branded types to prevent misuse of same-typed values — similar to Rust's newtype pattern
- Example: `type UserId = string & { readonly __brand: unique symbol }` — compile-time distinction between `UserId` and plain `string`
- Create values through a constructor function: `function UserId(id: string): UserId`

## Import Style

- **Prefer named imports** — `import { foo } from 'pkg'` over `import pkg from 'pkg'` or `import * as pkg from 'pkg'` to ensure bundlers can tree-shake unused exports
- **Default import is acceptable** when the package only has a default export (e.g., React) or named imports are unavailable
- **Avoid `import *`** unless the module is designed as a namespace (e.g., `import * as path from 'node:path'`)

## Import Type

- Use `import type { Foo }` or `import { type Foo }` for type-only imports — ensures no runtime import is emitted
- Enable `verbatimModuleSyntax` to let the compiler enforce the distinction between type and value imports

## JSON Serialization

- `JSON.stringify` omits `undefined` fields automatically. Use `null` when an API contract requires an explicit empty value

## Money (Decimal)

- Use `decimal.js` for all monetary calculations — never use native `number` for money (IEEE 754 precision issues)
- All monetary storage, transmission, and computation should go through `Decimal`; only convert to string for final display

## Date & Time

- Date/time package choices are owned by runtime/framework skills (e.g., Node.js backend vs React frontend). Do not pick a TypeScript-wide default here
