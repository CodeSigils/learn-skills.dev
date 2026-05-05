---
name: react-best-practices
description: |
  # React & Next.js Performance & Best Practices Skill

  This skill provides a comprehensive guide to optimizing React and Next.js applications. It prioritizes the "React Way" of doing things: declarative, performant, and type-safe.
license: MIT
metadata:
  author: vercel
  version: "1.0.0"
---

## Core Rules

### 1. Rendering Optimization
*   **React Server Components (RSC):** Favor RSC for data fetching by default. Use `"use client"` only for interactivity or browser-only APIs.
*   **Hydration:** Minimize the waterfall by using `Suspense` and `streaming`. Never perform state updates in `useEffect` that could be handled during rendering.
*   **Memoization:** Avoid `useMemo` and `useCallback` for trivial operations. Use them only when referential equality is required to prevent expensive re-renders in deep trees.

### 2. State Management (The Antigravity Way)
*   **Server State:** **MANDATORY** use of TanStack Query. Disable `refetchOnWindowFocus` for data that rarely changes.
*   **URL as State:** Use search parameters (URL) for UI state like filters, tabs, and pagination to ensure shareability.
*   **Local UI State:** Use `useOptimistic` for instant feedback on mutations.

### 3. Styling & Layout
*   **Tailwind CSS:** Use the `clsx` and `tailwind-merge` pattern for dynamic class strings.
*   **Images:** Use `next/image` for automatic optimization. Always provide `width`, `height`, and `alt`.
*   **Layouts:** Use the Next.js `layout.tsx` pattern for persistent navigation and persistent state.

### 4. Advanced Performance
*   **Code Splitting:** Use `next/dynamic` or `React.lazy` for components that are not visible on the initial fold.
*   **Bundle Analysis:** Audit the bundle periodically. Avoid heavy libraries (e.g., Moment.js, Lodash) where lightweight alternatives or native JS exist.
*   **Strict Mode:** Always develop with `React.StrictMode` enabled to catch side-effect bugs early.

## Interaction Protocol
*   **Input:** React codebase fragments or performance profiling reports.
*   **Output:** Refactored code with specific performance and best-practice improvements.

**Tag**: Start your response with `[REACT-BEST-PRACTICES]`.

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Eliminating Waterfalls | CRITICAL | `async-` |
| 2 | Bundle Size Optimization | CRITICAL | `bundle-` |
| 3 | Server-Side Performance | HIGH | `server-` |
| 4 | Client-Side Data Fetching | MEDIUM-HIGH | `client-` |
| 5 | Re-render Optimization | MEDIUM | `rerender-` |
| 6 | Rendering Performance | MEDIUM | `rendering-` |
| 7 | JavaScript Performance | LOW-MEDIUM | `js-` |
| 8 | Advanced Patterns | LOW | `advanced-` |

## Quick Reference

### 1. Eliminating Waterfalls (CRITICAL)

- `async-defer-await` - Move await into branches where actually used
- `async-parallel` - Use Promise.all() for independent operations
- `async-dependencies` - Use better-all for partial dependencies
- `async-api-routes` - Start promises early, await late in API routes
- `async-suspense-boundaries` - Use Suspense to stream content

### 2. Bundle Size Optimization (CRITICAL)

- `bundle-barrel-imports` - Import directly, avoid barrel files
- `bundle-dynamic-imports` - Use next/dynamic for heavy components
- `bundle-defer-third-party` - Load analytics/logging after hydration
- `bundle-conditional` - Load modules only when feature is activated
- `bundle-preload` - Preload on hover/focus for perceived speed

### 3. Server-Side Performance (HIGH)

- `server-cache-react` - Use React.cache() for per-request deduplication
- `server-cache-lru` - Use LRU cache for cross-request caching
- `server-serialization` - Minimize data passed to client components
- `server-parallel-fetching` - Restructure components to parallelize fetches
- `server-after-nonblocking` - Use after() for non-blocking operations

### 4. Client-Side Data Fetching (MEDIUM-HIGH)

- `client-swr-dedup` - Use SWR for automatic request deduplication
- `client-event-listeners` - Deduplicate global event listeners

### 5. Re-render Optimization (MEDIUM)

- `rerender-defer-reads` - Don't subscribe to state only used in callbacks
- `rerender-memo` - Extract expensive work into memoized components
- `rerender-dependencies` - Use primitive dependencies in effects
- `rerender-derived-state` - Subscribe to derived booleans, not raw values
- `rerender-functional-setstate` - Use functional setState for stable callbacks
- `rerender-lazy-state-init` - Pass function to useState for expensive values
- `rerender-transitions` - Use startTransition for non-urgent updates

### 6. Rendering Performance (MEDIUM)

- `rendering-animate-svg-wrapper` - Animate div wrapper, not SVG element
- `rendering-content-visibility` - Use content-visibility for long lists
- `rendering-hoist-jsx` - Extract static JSX outside components
- `rendering-svg-precision` - Reduce SVG coordinate precision
- `rendering-hydration-no-flicker` - Use inline script for client-only data
- `rendering-activity` - Use Activity component for show/hide
- `rendering-conditional-render` - Use ternary, not && for conditionals

### 7. JavaScript Performance (LOW-MEDIUM)

- `js-batch-dom-css` - Group CSS changes via classes or cssText
- `js-index-maps` - Build Map for repeated lookups
- `js-cache-property-access` - Cache object properties in loops
- `js-cache-function-results` - Cache function results in module-level Map
- `js-cache-storage` - Cache localStorage/sessionStorage reads
- `js-combine-iterations` - Combine multiple filter/map into one loop
- `js-length-check-first` - Check array length before expensive comparison
- `js-early-exit` - Return early from functions
- `js-hoist-regexp` - Hoist RegExp creation outside loops
- `js-min-max-loop` - Use loop for min/max instead of sort
- `js-set-map-lookups` - Use Set/Map for O(1) lookups
- `js-tosorted-immutable` - Use toSorted() for immutability

### 8. Advanced Patterns (LOW)

- `advanced-event-handler-refs` - Store event handlers in refs
- `advanced-use-latest` - useLatest for stable callback refs

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/async-parallel.md
rules/bundle-barrel-imports.md
rules/_sections.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and references

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
