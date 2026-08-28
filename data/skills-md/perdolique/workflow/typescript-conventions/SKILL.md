---
name: typescript-conventions
description: TypeScript coding conventions for writing, reviewing, and refactoring typed code. Use when working on `.ts`, `.tsx`, or files that embed TypeScript such as Vue, Astro, or Svelte components. Also use for TypeScript snippets, typed refactors, and review comments about code organization or function structure.
license: Unlicense
---

# TypeScript coding conventions

Apply conventions from the documentation, AGENTS.md files, lint rules, and configuration of the repository containing the active file first. Then use this skill for general TypeScript guidance, including TypeScript embedded in other file formats. Combine it with more specific framework, testing, or library-focused skills when needed.

## Avoid `return undefined`

Do not use `return undefined`. When exiting a function without a value, use a bare `return`.

```typescript
if (item) {
  return
}
```

## Extract non-trivial intermediate computations

- Before embedding a non-trivial computation in an argument, property value, array element, condition, loop input, spread source, return value, or larger expression, assign it to a named `const` or `let`.
- Always extract calls, awaited values, constructors, chained transforms, template-built values, ternaries, and multi-operator expressions when they are nested inside another consumer or computation.
- Exception: keep immediately clear elementary expressions inline, including property or element access, optional chaining, `??`, unary checks, simple comparisons, and one-step arithmetic. Do not split them solely to satisfy this rule. An initializer that already gives its result a meaningful name may contain a clear calculation.
- Arrange dependent statements in execution order: resolve input, transform it, then consume the result.
- Allow nested declarative validator or schema-builder DSL calls when the schema shape is the primary focus.
- Preserve behavior and algorithmic complexity; do not add intermediate collections or passes solely for formatting.

```typescript
const properties = categoryDetail.value?.properties ?? []

for (const property of properties) {
  const enumOptions = property.enumOptions ?? []
  const selectableOptions = enumOptions.map(toOption)
  const options = [defaultOption, ...selectableOptions]

  const group = {
    name: property.name,
    options
  }

  groups.push(group)
}
```

## Avoid meaningless pass-through wrapper functions

Do not create a function whose only job is to call another function and immediately return its result or await it without adding any behavior. If the wrapper does not name a real concept and does not own logic such as validation, branching, retries, mapping, instrumentation, or error handling, inline the call at the usage site or rename the underlying function instead.

Use a wrapper only when it creates a clearer domain boundary or adds behavior that the caller should not repeat.

```typescript
// Avoid wrappers that add no behavior
function getPath() : string {
  return buildPath()
}

const path = buildPath()

replaceRoute(path)

// Allowed: wrapper adds real behavior
async function loadUser() : Promise<User> {
  const user = await fetchUser()

  trackLoad('user')

  return user
}
```

## Keep wrapper contracts source-owned when possible

When wrapping a typed API, reuse source types and inference first. Add local named types only when the wrapper owns a narrower contract or typecheck proves inference is insufficient.

If the wrapper changes return/error shape, lifecycle, validation, mapping, or side effects, name that owned contract and test it.

## Require a concrete reason for every spread

Every object or array spread must serve a concrete purpose at that construction site, such as changing selected fields immutably, merging collections, or creating a required ownership boundary. If the original value will not be mutated and sharing it is safe, reuse it directly instead of making a shallow copy. Do not spread defensively or merely to make code look immutable.

When creating a view model, API payload, or other deliberately shaped object, list its properties explicitly. Do not use a broad source spread that hides the resulting contract or copies unrelated fields. Spread is shallow; do not use it when the required isolation is deeper.

During authoring and review, be able to state the purpose of each spread. Add a short code comment only when that purpose is not evident from the surrounding operation. Apply the same standard to production code, tests, and fixtures; a focused fixture override is a valid purpose, while an unnecessary copy is not.

```typescript
// Avoid an unnecessary shallow copy
const copiedOptions = { ...options }
runTask(copiedOptions)

// Reuse the safe, unmodified value
runTask(options)

// Make a deliberately shaped payload explicit
const payload = {
  description: formState.description,
  isArchived: formState.isArchived,
  name: formState.name
}

// Spread has a concrete purpose: replace one field without mutating the source
const archivedPayload = {
  ...payload,
  isArchived: true
}
```

## Prefer flat interface structures

Keep `interface` declarations and named object `type` aliases to one level of named properties. When a property needs an object shape, extract that shape into a separate named interface and reference it from the parent type.

Apply this to direct object properties, arrays of objects, and nullable or union forms such as `brand: { ... }`, `items: { ... }[]`, and `brand: { ... } | null`.

This rule covers type declarations only. It does not apply to runtime object literals, validator schemas, framework configuration objects, or library DSL values where the object shape is executable configuration rather than a reusable type contract.

```typescript
// Avoid inline object shapes in interfaces
interface ItemDetailResponse {
  brand: {
    id: number;
    name: string;
  };
  id: string;
}

// Prefer named nested contracts
interface ItemDetailBrand {
  id: number;
  name: string;
}

interface ItemDetailResponse {
  brand: ItemDetailBrand;
  id: string;
}
```

## Comment shared utility roles

For exported helpers, composables, services, and other shared utilities, add a short role-level comment only when nearby layers make the purpose easy to confuse. Explain what contract the utility owns.

Avoid line-by-line comments in straightforward code; improve naming or split the function instead.
