---
name: responsive
description: "Use when a layout must adapt across widths: breakpoints, fluid type and space, container queries, reflow order, and safe-area insets."
---


# Adapting Across Widths

The default number of breakpoints is zero. Build one layout that is already fluid — percentage and `fr` columns, `clamp()`ed type, wrapping flex rows — confirm it survives from `320px` up, and then add a breakpoint only at the exact width where you can point at something breaking. Most layouts that ship with five breakpoints needed one, and each unnecessary one is a state nobody will test again. The sibling `layout` composes the page at a single width — regions, columns, container cap, layer order — and this skill is only concerned with what changes as the width changes; if the regions and their order are not settled yet, that work is `layout`'s and belongs before any of this. Safe-area insets live here rather than in `native-feel`, which owns whether an app *reads* as installed, not how a viewport is measured.

**Adopt the project's breakpoint names before writing a query.** Read the Tailwind `theme.screens` (or `--breakpoint-*` in v4), a `@custom-media` block, or the SCSS mixins already in use, and express every rule through them. A hand-written `@media (min-width: 811px)` inside a Tailwind codebase is invisible to anyone reading the config, and a sixth breakpoint added for one component taxes every future one. If a component needs a boundary the project does not have, that is usually the signal it should be a container query instead.

## Quick Reference

| Topic | File |
| --- | --- |
| You need the actual widths, the unit table (`dvh` vs `svh` vs `lvh`, `cqi`, `ch`), the `clamp()` arithmetic, or the per-archetype reflow ladder | Open [breakpoint-map.md](references/breakpoint-map.md) whenever a concrete width, unit or formula is needed rather than a rule. |

## Core Principles

1. **Add a breakpoint where the content breaks, never at a device width.** Named device sizes are a moving target and routinely miss the real failure point by a hundred pixels either way. The procedure is mechanical: drag the viewport from `320px` upward and record the first width at which something fails — a headline reaching four lines, a card's text dropping under about `30ch`, two buttons colliding, a label wrapping mid-word — then put the breakpoint there. **Exception:** if the project already has a named set, snap to the nearest existing name rather than adding a one-off; consistency beats precision at this scale.

2. **Use `min-width` only, and write it in `rem`.** Min-width queries are additive, so the base styles are the fallback and nothing has to be undone; mixing directions for the same property produces a rule whose winner depends on source order. Write `@media (min-width: 48rem)`. The unit matters for a non-obvious reason: media queries resolve `rem` against the browser's *default* font size, not against `html { font-size }`, so a user who raised their default text size gets an earlier layout change — a `px` query ignores them entirely. **Exception:** queries with no additive form, which are legitimately one-directional — `@media (max-height: 667px)` for short landscape viewports, `print`, and the `prefers-*` family.

3. **Treat `320px` as a floor with a specification behind it.** WCAG 2.1 SC 1.4.10 (Reflow) requires content to be usable without two-dimensional scrolling at a viewport equivalent to `320` CSS pixels wide and `256` CSS pixels tall. This is not a courtesy width — it is what a 1280px screen at 400% zoom becomes, which is how low-vision users read. **Exception:** the SC exempts content that genuinely requires two-dimensional layout — data tables, maps, diagrams, source code — which may scroll horizontally *inside their own container*, never by moving the page.

4. **Reach for `clamp()` before a breakpoint, and always keep a `rem` term in the middle.** A fluid value removes the need for the query entirely, but `font-size: clamp(2rem, 5vw, 4rem)` is a trap: a preferred value made only of `vw` does not respond to text scaling, so the text stops resizing and fails WCAG 1.4.4 (Resize Text, 200%). The correct shape carries both: `clamp(1.75rem, 1.333rem + 2.083vw, 3rem)`. **Exception:** values that must stay physically constant never go fluid at all — hairlines, icon sizes, hit areas, and border radii on small controls.

5. **Container queries for components, media queries for the shell.** A component that asks the viewport how wide it is will be wrong the first time someone drops it into a sidebar. If the rule is about the element's own box — a card that turns horizontal once it has room — it is `@container (min-width: 30rem)` with `container-type: inline-size` on a wrapper. Two traps: a container cannot query *itself*, so the wrapper is mandatory; and `container-type: size` needs a determinate height and collapses a content-sized element — use `inline-size`. **Exception:** genuinely viewport-scoped facts stay media queries — `100dvh` panes, releasing a sticky header on short screens, and safe-area behaviour.

6. **Write the reflow priority order before the first query.** Rank the regions by user priority; at each narrower step the lowest-ranked one collapses — below the content, into a disclosure, or into an overflow menu. Without a written order, columns stack in DOM order and the sidebar lands above what the user came for. Fix that in the DOM, not with `order:` or explicit `grid-row`, because CSS reordering desynchronises announced and focus order from visual order — `a11y` owns that contract and will flag it. **Exception:** purely decorative, non-interactive elements with no reading sequence, where visual reordering carries no meaning to lose.

7. **A breakpoint that only changes font sizes is a missing structural change.** Wide screens are not a phone layout scaled up; if the *structure* does not change — column count, what is visible, what became persistent instead of hidden — the layout is stretching, not adapting, and the result is a reading column a thousand pixels wide. **Exception:** reading-first pages such as docs, where the only correct wide-screen change is genuinely a table of contents appearing beside the capped measure.

8. **Safe-area insets are additive padding, and require `viewport-fit=cover`.** Without `<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">`, every `env(safe-area-inset-*)` resolves to `0` and the bug is invisible in review. Write `padding-bottom: calc(16px + env(safe-area-inset-bottom))` so the inset adds to the design value instead of replacing it, and let the element's *background* extend under the inset while only its contents are padded. **Exception:** elements not pinned to a viewport edge need no inset at all — sprinkling it through a page is noise, since it resolves to zero everywhere it is not needed.

9. **Pick the viewport height unit deliberately: `dvh`, `svh`, `lvh` are not interchangeable.** `100vh` on mobile equals the *largest* height, so a full-screen pane overflows under the browser chrome. Use `100dvh` for panes that may resize as the chrome shows and hides, and `100svh` for a shell that must never resize — `dvh` reflows during scroll on iOS and drags sticky children with it, which reads as jitter. **Exception:** desktop-only surfaces, where all four units are equal and `vh` is fine.

## Output Format

State adaptations as a width ladder before writing any query. One row per breakpoint, and any row whose only change is type size is a row to reconsider:

```
width      columns   nav             what collapses
──────────────────────────────────────────────────────
base       1         bottom bar      filters → sheet
48rem      2         top tabs        filters → inline
80rem      2 + rail  top tabs        nothing
```

## Smells and Fixes

| Smell | Fix |
| --- | --- |
| Breakpoints at `768` / `1024` because those are devices | Resize until something breaks; put it there |
| `max-width` and `min-width` queries for the same property | Mobile-first `min-width` only |
| `clamp(2rem, 5vw, 4rem)` | Add a `rem` term to the middle: `clamp(2rem, 1.5rem + 2.5vw, 4rem)` |
| A component querying the viewport | `@container` on a wrapper with `container-type: inline-size` |
| `@container` matching nothing | The container is querying itself — add the wrapper |
| Full-height pane collapsing to zero | `container-type: size` without a determinate height; use `inline-size` |
| `order: -1` fixing the mobile stack | Change the DOM order instead |
| Fixed bottom bar under the home indicator | `calc()` the design value plus `env(safe-area-inset-bottom)` |
| `env()` returning `0` on device | Missing `viewport-fit=cover` |
| `100vh` on a mobile full-screen view | `100dvh`, or `100svh` for a fixed shell |
| Horizontal page scroll below `320px` | WCAG 1.4.10 failure — reflow, or scroll inside the table's own container |

## Checklist

- [ ] Every breakpoint traceable to an observed break, or to an existing project name
- [ ] `min-width` only, expressed in `rem`
- [ ] Usable at `320` CSS px with no two-dimensional page scroll
- [ ] Fluid values use `clamp()` with a `rem` term in the preferred value
- [ ] Component-level rules are container queries on a wrapper
- [ ] Reflow priority written down; no `order:` overrides on interactive content
- [ ] Every breakpoint changes structure, not only type size
- [ ] `viewport-fit=cover` set; insets added with `calc()`, backgrounds extend beneath
- [ ] Height units chosen per surface: `dvh` for resizing panes, `svh` for fixed shells
