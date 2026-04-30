---
name: react
description: React development conventions and best practices. Use when writing React components, hooks, state management, or styling in a React project.
user-invocable: false
---

# React Conventions

## Naming Conventions

- **Components**: PascalCase — `UserProfile`, `OrderList`
- **Component files**: PascalCase matching the component name — `UserProfile.tsx`, `OrderList.tsx`
- **Hook files**: `useXxx.ts` — `useAuth.ts`, `useCart.ts`
- **Constants**: `UPPER_SNAKE_CASE` — `MAX_RETRY_COUNT`, `API_BASE_URL` (avoid PascalCase to prevent confusion with components)
- **Event handler props**: `onXxx` — `onClick`, `onSubmit`, `onStatusChange`
- **Event handler implementations**: `handleXxx` — `handleClick`, `handleSubmit`

## Component Design

- **One component per file** (default): Prefer one exported component per file. If the project's existing convention allows co-located internal sub-components in the same file, follow that convention — but never put multiple reusable public components in the same file
- **Function Components only**: Use Function Components, avoid Class Components
- **Hook priority**: Prioritize using hooks to manage state and side effects
- **Single Responsibility**: Each component focuses on a single responsibility

## Props Design

- **Interface naming**: `{ComponentName}Props` — `UserProfileProps`, `OrderListProps`
- **Destructure in body, not in parameters**: Destructure props inside the component body, not in the function signature

```tsx
// ✅ Destructure in body
function UserProfile(props: UserProfileProps) {
  const { name, avatar, onEdit } = props
  // ...
}

// ❌ Destructure in parameters
function UserProfile({ name, avatar, onEdit }: UserProfileProps) {
  // ...
}
```

- **Children**: Declare `children: ReactNode` explicitly in the Props interface, not `PropsWithChildren`
- **Avoid prop drilling**: Use composition (children pattern) to pass components through instead of threading data through intermediate layers. Use Context or state management for truly shared state

## Conditional Rendering

- **Guard clause early return**: Handle edge cases (loading, error, empty, null) with early return at the top, keep the main render path flat

```tsx
function UserProfile(props: UserProfileProps) {
  const { user } = props

  if (!user) return null

  return <div>{user.name}</div>
}
```

- **Binary choice (A or B)**: Use ternary — `condition ? <A /> : <B />`
- **Show or hide**: Use `&&` with boolean confirmation — avoid the falsy trap (`0 && <Component />` renders `"0"`)

```tsx
// ✅ Explicit boolean
{count > 0 && <Badge count={count} />}
{!!items.length && <List items={items} />}

// ❌ Falsy trap
{count && <Badge count={count} />}
```

- **Multiple states / complex conditions**: Never nest ternaries. Extract to a sub render function or a separate component

## Data Fetching / Server State

- **Client state vs Server state**: Keep them separate. Client state (UI state like modal open/close, form input) uses `useState` or Zustand. Server state (API data with cache/sync needs) uses a dedicated library
- **Library preference**: Follow the project's existing choice. For new projects, start with SWR for simplicity. Use TanStack Query when the project has complex needs (optimistic updates, infinite queries, advanced cache control)
- **Three-state handling**: Every data fetching component should handle loading, error, and empty states

## State Management

- **Store separation**: Separate stores by functional domains
- **Immutable updates**: Use Immer or the project's existing approach
- **Prefer Zustand + Immer**: For new projects without an existing solution; otherwise follow what the project uses

## Styling

Follow the project's existing styling system — design tokens, theme, breakpoints, responsive strategy, and class naming conventions. Only choose a new approach when no existing system is in place.

- **CSS Modules `.d.ts`**: When the project has `typed:scss` or `typed:css` scripts in `package.json`, run those commands to auto-generate style type declarations — never manually create or edit `.d.ts` files for styles

## Hook Patterns

- **Custom Hooks**: Extract complex logic into custom hooks
- **Dependency Arrays**: Properly manage useEffect dependency arrays
- **Cleanup Logic**: Properly implement cleanup functions in useEffect
- **Memoization — don't wrap by default**:
  - `useMemo`: Only for computationally expensive derived values, not for simple string concatenation or object creation
  - `useCallback`: Only when passing callbacks to memoized child components or when used as a dependency in other hooks
  - If there's no measurable performance problem, don't add it

## Performance

- **`React.memo` — don't add by default**: It has comparison cost. Only use when a component receives stable props but its parent re-renders frequently, confirmed by DevTools Profiler
- **List keys**: Use stable, unique IDs from data (`id`, `uuid`). Only use array index for static, never-reordered lists (e.g., fixed nav items)
- **Code splitting**: Use `React.lazy` + `Suspense` at the route level. Only split component-level for large, non-critical blocks (heavy chart libraries, modal content)

## Date & Time

- **Use `dayjs`** for all frontend date/time handling — never manipulate native `Date` directly for formatting, calculation, or comparison
- Use dayjs plugins (e.g., `relativeTime`, `utc`) for extended functionality via `dayjs.extend()`

## Error Handling

- **Error Boundary scope**: Wrap at route/page level so one page crashing doesn't take down the entire app. Add separate boundaries around critical isolated blocks (third-party widgets, charts, rich editors)
- **Don't over-wrap**: Not every component needs an Error Boundary — only pages and independently failing blocks
- **Implementation**: Write your own class component (Error Boundary only supports class components). No need for a library when usage is limited to a few places
