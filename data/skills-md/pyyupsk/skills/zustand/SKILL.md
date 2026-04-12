---
name: zustand
description: Use when creating Zustand stores, managing React client-side state, or structuring per-domain state in a project.
license: MIT
metadata:
  author: pyyupsk
  version: "1.0"
---

# Zustand

Lightweight React state management. One store per domain — never one giant store.

## Store Structure

```ts
// src/stores/useFilterStore.ts
import { create } from "zustand";

type FilterStore = {
  // state
  search: string;
  status: "all" | "active" | "inactive";
  // actions
  setSearch: (search: string) => void;
  setStatus: (status: FilterStore["status"]) => void;
  reset: () => void;
};

const initialState = {
  search: "",
  status: "all" as const,
};

export const useFilterStore = create<FilterStore>((set) => ({
  ...initialState,
  setSearch: (search) => set({ search }),
  setStatus: (status) => set({ status }),
  reset: () => set(initialState),
}));
```

## Rules

### One store per domain

```ts
// ❌ one giant store for everything
export const useStore = create(...)

// ✅ one store per concern
export const useFilterStore = create(...)
export const useCartStore = create(...)
export const useAuthStore = create(...)
```

### Always define `initialState` separately

```ts
// ❌ reset() reconstructs state inline — easy to drift
reset: () => set({ search: "", status: "all" })

// ✅ reset() spreads shared initialState — single source of truth
const initialState = { search: "", status: "all" as const };
reset: () => set(initialState),
```

### Actions stay inside `create()`

```ts
// ❌ mutating state outside the store
useFilterStore.setState({ search: "foo" });

// ✅ expose named actions, call them from components
const { setSearch } = useFilterStore();
setSearch("foo");
```

### Type shape

Keep state and actions in one `type` — no interface, no splitting:

```ts
type FilterStore = {
  // state fields first
  search: string;
  // then action fields
  setSearch: (search: string) => void;
  reset: () => void;
};
```

## File Naming

`src/stores/use<Domain>Store.ts` — camelCase, starts with `use` (same rule as hooks)

```tree
src/stores/
├── useAuthStore.ts
├── useCartStore.ts
└── useFilterStore.ts
```

## Common Mistakes

- **One giant store** — split by domain, each file owns one concern
- **`reset()` without `initialState`** — always define `initialState` separately
- **Mutating state outside `create()`** — expose actions, never call `setState` directly in components
- **Using `interface`** — use `type` for store shape
- **Forgetting `as const`** — literal union fields in `initialState` need `as const` to preserve type
