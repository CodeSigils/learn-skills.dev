---
name: navigation
description: "Use when structuring how users move through an app: tabs, sidebars, breadcrumbs, hierarchy depth, active state, back behavior, and URL as state."
---


# Moving Through an App

Navigation is a rendering of the information architecture, not a layer designed on top of it. Default posture: the flattest tree the content permits, exactly one primary index, and the URL as the single source of truth for where the user is and what they are looking at. Every level, every nav region, and every menu you add is paid for by every user on every visit — so add one only when the content forces it, and delete one the moment a flatter shape still answers "where am I, and what else is there?". This skill owns the movement graph and never names a container: which container a single flow gets once it has a place in that graph — modal, drawer, sheet, popover, inline expand, or full page — belongs to `modal-or-page`. Arrangement inside one page is `layout`; the timing of the movement between destinations is `transitions`.

**Read the router before writing a line of nav.** Next App Router, React Router, TanStack Router, SvelteKit, Nuxt and Expo Router each have their own model of nested layouts, route params, search params, scroll restoration and history. Navigation state lives in the router the project already has (`<Link>`, `useSearchParams`, loaders) — never in a parallel `useState` store shadowing the URL, which is how back buttons start lying. If the project already ships a nav primitive from its design system, extend that one; a second sidebar component is a second source of truth about the app's shape.

## Quick Reference

| Topic | File |
| --- | --- |
| Per-archetype nav skeletons — structure, URL shape, active carrier, back behavior, and mobile collapse for dashboards, settings, list-detail, record sub-tabs, docs, and content sites | [patterns.md](references/patterns.md) |

Open it once you know which archetype you are building; it saves re-deriving the same skeleton and keeps two apps in one product from disagreeing about their own shape.

## Decision: which nav shape

| The destination set | Shape |
| --- | --- |
| Peer views of one object, fits without horizontal scroll | Tabs — or a segmented control when there are two |
| A fixed set of distinct areas or object types | Persistent sidebar, or a top bar if the labels fit on one line |
| Fixed set, narrow viewport | Bottom bar carrying **top-level destinations only** — never a hamburger holding the whole tree |
| Data-driven and unbounded (projects, workspaces, files) | Search / command palette is the index; the sidebar shows pinned plus recent |
| One level below what the sidebar shows | A breadcrumb, never a second sidebar |

## Core Principles

1. **Cap reachable depth at three levels.** Past three nested levels people stop building a model of the app and start hunting, and the third level is where a breadcrumb stops being decoration: `home → section → detail`, with a breadcrumb mandatory from level three down. Exception: user-generated hierarchies — files, folders, org charts — where depth is data rather than architecture; those get an unbounded tree plus a full breadcrumb trail, and search as the primary way in.

2. **Tabs are views of one object; a sidebar is different objects.** A tab strip promises that whatever sits above it stays constant, so `/invoice/42/history` is a tab and "Invoices / Customers" is not. The test is mechanical: if the set does not fit without horizontal scroll at the narrowest supported width, it is not a tab set. Exception: tabs that are *content* rather than architecture — open files, channels, boards — may scroll, because the user created them and expects them to accumulate.

3. **When the destination set is unbounded, search is the navigation.** No static nav enumerates every project or file; a sidebar that tries becomes a scrolling list of everything, which is a database, not a nav. Show pinned items plus a capped recents list, and make the palette (`Cmd+K` / `Ctrl+K`) the real index. Exception: a bounded, stable set that fits on screen without its own scrollbar — just list it and skip the palette.

4. **Every route lights exactly one nav item, detail routes included.** A page that highlights nothing tells the user they have fallen out of the app; `/projects/42/settings` keeps **Projects** active all the way down. Exception: deliberately global routes — a full-screen search, a checkout, an onboarding wizard — show no nav at all, and must then remove it rather than render it dimmed and unusable.

5. **Active state never rests on color alone, and never borrows hover's treatment.** If hover and active look alike, wherever the cursor happens to sit looks like where the user is. Carry active on a persistent second signal — a background surface, a weight change, or a rail — and mark it `aria-current="page"`, the only ARIA attribute this skill owns; roles, tab order and announcements are `a11y`. Exception: a segmented control, where the moving thumb is already the persistent indicator.

6. **Push history when the user went somewhere; replace it when they adjusted the view.** If a filter keystroke pushes, Back becomes an undo stack nobody asked for and the user presses it eleven times to escape the page. Use `router.push` for opening a record or section, `router.replace` for search text, sort, facets and expansion state — debounced before it is written. Exception: paginated content people deliberately page through (an archive, docs, search results) is a destination, so push it.

7. **The in-app back affordance is a link up, not a history step.** `history.back()` sends a deep-linked visitor to whatever site they came from, and it makes the control lie about where it goes. Point it at the parent route and label it with the destination — `← Projects`, not `← Back`. Exception: a genuine step flow, where Back means the previous step — and even there it should be a state transition you control, not a call into browser history.

8. **Whatever survives a reload belongs in the URL.** Reload is the cheapest test in this skill: everything the user loses was state that belonged in the address bar. Route, active tab, selected record, filters, sort, page and expanded panel go in the URL; drafts, hover, focus and scroll do not. Never put personal or sensitive values in a query string — key by id. Exception: state so large it makes the URL unshareable (a forty-facet filter set) — persist it server-side and put its id in the URL instead.

9. **Restore scroll on back, and only on back.** Returning to a feed at the top erases the user's progress; arriving at a brand-new page halfway down is disorienting. Restore the saved offset on POP navigations and reset to top on PUSH. Exception: a fragment deep link (`#pricing`) wins over both.

10. **Name items in the user's words, and read search queries as bug reports about those names.** If people keep searching "invoices" while the nav says "Billing", the nav is wrong, not the users. Nav labels are nouns; a verb in the sidebar (`Create`, `Upload`) is a button that wandered in. Exception: one primary action deliberately docked at the top of the nav — visually distinct from the destination list, and only one.

## Smells and Fixes

| Smell | Fix |
| --- | --- |
| Clicking a tab does not change the URL | Peer views go in a path segment (`/record/42/history`); filters go in a query param |
| `← Back` calls `history.back()` | Link to the parent route; label the button with the destination |
| Filter typing fills the history stack | Debounce, then `replace` |
| A detail route highlights no nav item | Keep the ancestor section active for all of its descendants |
| Hover and active are the same treatment | Give active a persistent carrier plus `aria-current="page"` |
| Sidebar scrolls through sixty workspaces | That set is data — pinned plus recent, palette as the index |
| Hamburger menu on a desktop viewport | The space exists; show the destinations |
| Four levels of nested flyout menus | Flatten to three and add a breadcrumb |
| Returning from a detail resets the list to the top | Restore scroll on POP navigations |
| A sidebar and a top bar both list sections | One primary index; the other becomes context or account chrome |
| Nav label is internal jargon ("Async relay") | Rename it to whatever users type into search |
| Every page opens with thirty nav tab stops | It needs a skip target — `a11y` owns the implementation |

## Checklist

- [ ] Nothing sits more than three levels deep, or the depth is user data and has a breadcrumb
- [ ] Tabs hold peer views of one object and fit without horizontal scroll
- [ ] Unbounded destination sets are reached by search, not enumerated in the sidebar
- [ ] Every route — detail routes included — leaves exactly one nav item active
- [ ] Active state carries a non-color signal and `aria-current="page"`, distinct from hover
- [ ] Destinations push history; view adjustments replace it, debounced
- [ ] The in-app back control links to the parent and names it
- [ ] Reload preserves route, tab, selection, filters, sort and page; no personal data in the query string
- [ ] Back restores scroll position; forward navigation starts at the top
- [ ] Every label is a noun in the user's vocabulary, and the nav carries at most one docked action
