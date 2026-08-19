---
name: ui-states
description: "Use when specifying non-happy-path states: empty, loading, skeleton versus spinner, error, offline, partial data, and optimistic updates."
---


# Empty, Loading, Error, and Partial States

The default posture: **a surface is not finished until loading, empty, error, and partial have each been specified — the happy path is one of five states, not the state with four edge cases.** Most of what makes software feel unreliable happens here: the spinner that flashes for 200ms, the "No data" that never says why, the dashboard that blanks because one tile's request failed. This skill is the **single owner of the loading threshold ladder**; no other skill may restate those numbers. Three neighbours: `notifications` owns anything thrown *at* the user, while anything rendered *in place of* the data belongs here; `ui-copy` owns the words inside these states, this skill owns their container, timing, and anatomy; and `onboarding` owns the first-run sequence, while the spec of any individual empty state — the first-run one included — is here.

**Render these states from the data layer the project already has.** TanStack Query and SWR expose `isPending`, `isFetching`, `isError`, and `isPlaceholderData`; RSC exposes Suspense boundaries and `error.tsx`; a Redux or Zustand store already carries status fields. Read those flags and branch on them. A parallel `const [loading, setLoading] = useState(false)` beside a query hook guarantees the two disagree on a refetch, and the symptom — a spinner that outlives the data — is always blamed on the network.

## Quick Reference

| Topic | Reference | Open it when |
|---|---|---|
| Per-surface state specs for tables, lists, dashboards, forms, and charts | `references/state-catalog.md` | Open it when you know which surface you are building and need its concrete state-by-state spec rather than the general rule. |

## The loading ladder — house rule, one owner

| Expected wait | Show | Why |
|---|---|---|
| Under `800ms` | Nothing at all | An indicator that flashes and vanishes makes a fast response look unstable |
| `800ms` – `3s` | A spinner, or a pending state on the control that started it | Long enough to need acknowledgement, too short to justify fake content |
| Above `3s` | A skeleton of the known layout, or determinate progress | The user needs the shape of what is arriving, or how much remains |

These are house numbers, not a designer's — a testable default. Run a real surface with and against them before enshrining them project-wide.

## Error taxonomy — classify before you style

| Cause | Render | Recovery control |
|---|---|---|
| Network / timeout | In place; keep stale data if any exists | Retry (re-runs the request) |
| Server 5xx | In place, with a reference the user can quote | Retry, then a support path |
| Permission 403 | In place, naming who can grant access | Request access — never retry |
| Not found 404 | In place, naming what was looked for | Back to the list, plus search |
| Validation 4xx | On the field that caused it — `forms` | Fix and resubmit |
| Client exception | Error boundary scoped to the broken region | Reload that region |

A retry button on a 403 is the tell that classification was skipped.

## Core Principles

1. **Match the indicator to the shape you can promise.** Use a skeleton only when you know the layout arriving and it will not move once it does; use a spinner whenever the result's shape is unknown. A skeleton that resolves into a differently sized element is worse than none: it promised something and broke the promise. Skeletons occupy the same box as the loaded content. Exception: an unbounded list on first load renders skeleton rows sized to fill the visible area and no more — a full screen of fake rows for three real results reads as a lie.

2. **No state transition may change the layout size.** Reserve the box before the data lands: `aspect-ratio` on media, a min-height on the region, `tabular-nums` on numbers that tick. Empty, loading, error, and loaded all fit one reserved area. Exception: height that is genuinely user-driven (an expanding textarea, an accordion) may grow — but only from an action the user just took.

3. **Empty is three states wearing one name.** *First-run* empty (nothing ever existed) coaches and offers the primary action. *Filtered* empty (things exist, this query found none) restates the query and offers a way to clear it — never a "Create" button, the wrong action for a search that missed. *Error* empty is not empty; it is an error, and must never render as "No results". Exception: a deliberately quiet surface — a notifications inbox, an audit log — may use one flat empty line, because reaching zero there is success.

4. **Every empty state answers three questions in order: what belongs here, why it is not here, what to do next.** "You haven't created a project yet" plus a **Create project** button, never "No projects found". One action, not three. Exception: a read-only surface the user cannot populate ("No incidents in the last 30 days") answers the first two and stops — inventing an action there is worse than none.

5. **Offline is a state, not an error.** Keep the last known data on screen and mark it stale rather than blanking the surface; queue writes rather than rejecting them; retry on reconnect and confirm quietly when the queue drains. Exception: an action whose result depends on server state you cannot verify — a purchase, a booking, a claim on a limited resource — is refused while offline rather than queued, and says so.

6. **Partial data renders; failure is scoped to the region that failed.** A dashboard where one of six tiles 500s shows five tiles and one tile-shaped error, not six empty tiles or a full-page error. Wrap each independently-fetched region in its own boundary. Exception: a region whose absence makes the rest misleading — an unlabelled axis, a total whose components failed — fails the whole surface rather than showing a number nobody can trust.

7. **Optimistic updates keep the pre-image and revert visibly.** Apply instantly only when the write is user-initiated, cheap to undo, and near-certain to succeed (toggles, reorders, likes, marking read). Hold the previous value, and on failure restore it *and* say what happened — a silent revert makes the user believe they mis-clicked. Exception: never optimistic for payments, deletions, anything with a server-assigned identity you display, or anything the user acts on next.

8. **A retry retries the request, not the page.** A "Reload" that discards scroll position, filters, and unsent input punishes the user for the network's mistake. Retry the failed call, keep everything else, and back off if the second attempt fails. Exception: corrupted client state that a re-fetch cannot fix — say so plainly before reloading.

## Smell / Fix

| Smell | Fix |
|---|---|
| Spinner on every fetch, instant ones included | Nothing under `800ms` |
| Full-screen skeleton for a three-row result | Skeleton rows sized to the visible area only |
| Skeleton blocks that don't match the real layout | Match the box, or use a spinner |
| "No data" / "No results found" | Say what belongs here and the one action |
| "Create project" when a filter matched nothing | Filtered empty offers *clear the filter* |
| One failed widget blanks the dashboard | Per-region boundary; one tile-shaped error |
| Retry button on a permission error | Classify first — 403 gets *Request access* |
| Optimistic delete that reverts silently | Not optimistic at all; or revert loudly |
| Content jumps when data arrives | Reserve the box before fetching |
| Stale data blanked when the connection drops | Keep it, mark it stale, retry on reconnect |

## Output Format

Spec a surface as a fixed six-row block. Write `n/a` explicitly where a state does not apply — a blank row means it was forgotten, and telling those apart is the point of the format:

```
Surface:   <name>
Loading:   <ladder tier + indicator>
Empty:     first-run / filtered / quiet — text + one action
Error:     per taxonomy row + recovery control
Offline:   stale-data behavior + write queue
Partial:   which regions fail independently
```

## Checklist

- [ ] Nothing under `800ms`; spinner `800ms`–`3s`; skeleton or progress above `3s`
- [ ] Skeleton used only where the shape is known and matches the loaded box
- [ ] Box reserved so no state transition shifts the layout
- [ ] First-run, filtered, and error empties distinguished; each has one action
- [ ] Every error classified before styling; recovery control matches the cause
- [ ] Offline keeps stale data, queues writes, retries on reconnect
- [ ] Independently-fetched regions fail independently
- [ ] Optimistic writes limited to cheap, near-certain actions; reverts visible
- [ ] Retry re-runs the request and preserves scroll, filters, and input
- [ ] States wired to the existing data layer's flags, not a parallel boolean
