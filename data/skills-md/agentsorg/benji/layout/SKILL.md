---
name: layout
description: "Use when composing a page: grid, container width, column structure, alignment, z-index layering, and where the eye lands first. Gaps and density are `spacing`."
---


# Composing a Page

Default to one column inside a capped container, and make every additional column earn its place. A page is a vertical stack of full-width bands; each band holds one centred content well; a grid arranges items *inside* a band and never the page itself. That posture is correct more often than it feels, because a product page is read down one axis and every extra column is a decision you then owe at every width. The sibling `spacing` owns every gap, padding value and density mode — this skill decides which regions exist, how wide they are, and which one sits above which; the moment the question becomes *how far apart*, hand it over. Three neighbours take the rest: `responsive` owns what changes as the width changes, `navigation` owns movement between pages rather than composition within one, and a request that names a table or a dashboard is `dense-ui` by the named-noun rule.

**Read the project's layout primitives before adding any of your own.** Look for a `<Container>` / `<Stack>` / `<PageShell>` component, a `max-w-*` convention in existing pages, a `grid-template-areas` block in a layout stylesheet, and an existing z-index token set (`--z-*`, `theme.zIndex`, a `zIndex.ts`). Compose with what you find. Two containers with different caps, or a second z-index vocabulary alongside the first, is the failure this skill exists to prevent — a page that "looks fine" while every future page inherits the ambiguity.

## Quick Reference

| Topic | File |
| --- | --- |
| The page's shape is a known type — split view, sidebar + detail, feed, settings, wizard | Open [page-archetypes.md](references/page-archetypes.md) before writing markup, and read only the archetype that matches. |
| Something is stacked wrongly, a popover is trapped inside a card, or you are about to type a `z-index` literal | Open [z-index.md](references/z-index.md) — it holds the layer set and the stacking-context traps that make `z-index` appear not to work. |

## Core Principles

1. **Cap the container, and know it is not the same cap as the measure.** An uncapped page produces unreadable line lengths and compositions that drift apart on wide monitors. The default content well is `max-width: 1200px` centred, with full-bleed reserved for bands whose *background* spans the viewport while their contents still sit in the well. The reading measure (`65ch`) is a different, narrower cap and belongs to `typography` — a page routinely uses both, nested. **Exception:** canvases, editors, maps and data grids take the whole viewport and set their own bound; capping them wastes the screen the user opened them for.

2. **One column until a second one is justified by content, not by width available.** The ladder is `1` column for reading, forms, settings detail and wizards; `2` for sidebar + detail; `8` for marketing composition; `12` only where users arrange tiles themselves, because 12 divides evenly by 2, 3, 4 and 6. A twelve-column grid on a marketing page is configuration overhead nobody reads. **Exception:** an existing design file that already specifies 12 — match it rather than re-deriving.

3. **Make two-column splits asymmetric.** Equal columns read as static and give the eye no entry point; unequal ones create a primary and a secondary. Write `grid-template-columns: 2fr 1fr` (or a fixed sidebar, `280px 1fr`), never `1fr 1fr`. **Exception:** layouts where equality *is* the message — pricing tiers, before/after, diff views, side-by-side comparison — where symmetry is the correct signal.

4. **Treat z-index as a named layer set with six members and no others.** Arbitrary values (`z-index: 9999`) are a bidding war that the next component always wins. The set is `--z-base: 0`, `--z-sticky: 50`, `--z-dropdown: 100`, `--z-modal: 200`, `--z-tooltip: 300`, `--z-toast: 400`; popovers and menus share the dropdown layer, a modal's scrim shares the modal layer. **Exception:** inside a component that has already sealed itself with `isolation: isolate`, local `z-index: 1` / `2` are correct and must *not* be promoted to tokens.

5. **Seal a component's stacking before you raise anything inside it.** Without a local stacking context, a raised child competes with the entire document and wins or loses by accident. Put `isolation: isolate` on any component that overlaps its own children — a card with a floating badge, a media object with a play button. **Exception:** an element that must escape its ancestor's bounds (a popover anchored inside an `overflow: hidden` card) cannot be solved by layering at all; portal it to the layer root instead.

6. **Give the page exactly one focal point and verify it by squinting.** The test is falsifiable: blur the screen or view it in greyscale at 10% size, and name the first thing still identifiable. If that is the nav bar, a cookie banner or a decorative image, the hierarchy is inverted — demote everything else rather than enlarging the hero. Hierarchy is subtraction. **Exception:** split views with two working panes (mail, IDE, inbox + thread) have their focal point *inside the active pane*, not on the page.

7. **Keep the primary action inside the viewport on any page taller than one screen.** Scroll-depth data will confirm most users never reach the bottom of a long form. If the region exceeds `100dvh`, the primary action goes into a sticky footer bar or travels with a sticky sidebar. **Exception:** irreversible destructive confirmations, which should require deliberately reaching the end — never make "Delete account" sticky.

8. **Put destructive actions in a different region, not a wider gap.** Proximity implies equivalence, and space alone does not undo it: a Delete sitting in the same button row as Save reads as a peer of Save. Move it to its own block (a bordered "Danger zone") or into an overflow menu. **Exception:** a bulk-action toolbar where every action is destructive — there the confirmation step carries the separation instead.

9. **Declare the sticky header's height once and consume it everywhere.** Hard-coding `80px` in three places guarantees that anchored links land under the header the first time the header changes. Define `--header-h` and use it for `top:` on sub-navs, `scroll-margin-top: var(--header-h)` on every `[id]`, and `height: calc(100dvh - var(--header-h))` on full-height panes. **Exception:** short viewports — an `80px` header on a `667px` landscape phone eats an eighth of the screen, so release the sticky there; the query that does it belongs to `responsive`.

## Output Format

Before writing markup for a page, emit the region sketch and get it agreed. It is four columns and it prevents most of the rework:

```
band        container    columns   sticky   layer
─────────────────────────────────────────────────
header      full-bleed   1         yes      sticky
hero        1200         1         no       base
features    1200         8-col     no       base
footer      full-bleed   1         no       base
```

## Smells and Fixes

| Smell | Fix |
| --- | --- |
| `z-index: 9999`, or two components at `999` | Assign the nearest named layer; nothing outside the six-member set |
| A `z-index` that visibly does nothing | An ancestor created a stacking context — see `references/z-index.md` |
| Content stretching edge to edge at 1920px | Cap the well at `1200px`; let only the background go full-bleed |
| `1fr 1fr` on a page-level split | `2fr 1fr`, or a fixed sidebar plus `1fr` |
| Anchor links landing beneath the sticky header | `scroll-margin-top: var(--header-h)` on `[id]` |
| Delete and Save in the same button row | Separate region or overflow menu, not a bigger gap |
| Two elements competing to be the hero | Demote one; re-run the greyscale squint test |
| Submit only reachable at the end of a `3` screen form | Sticky action bar |
| A second container component with a different cap | Delete it and reuse the existing one |

## Checklist

- [ ] Content well capped; full-bleed limited to backgrounds
- [ ] Column count justified by content, off the `1 / 2 / 8 / 12` ladder
- [ ] Page-level splits asymmetric unless equality is the message
- [ ] Every `z-index` is a named token, or local inside an isolated component
- [ ] `isolation: isolate` on components that overlap their own children
- [ ] One focal point, confirmed by the greyscale squint test
- [ ] Primary action reachable without scrolling to the end
- [ ] Destructive actions in their own region
- [ ] Header height declared once as `--header-h` and consumed everywhere
