---
name: ui-review
description: "Use when reviewing non-motion UI code and a Before/After/Why table plus an explicit verdict is required."
---


# Reviewing Interface Code

Review as if the happy path was tested and the details were not, and **default to flagging** — approval is earned, never assumed. This matters most because most UI arriving for review is now model-generated, and model-generated UI is good at exactly the thing a test suite cannot catch: code that renders on the first try, screenshots cleanly, then falls apart under a real keyboard, a slow network, or a second look at the spacing. You are the second look. Every finding leaves here as one row of a `| Before | After | Why |` table quoting the project's actual code beside an exact replacement. That table is Emil Kowalski's mandated review format, and the `Before:` / `After:` list form is forbidden, because a list lets a reviewer *describe* a change while a table forces them to *write* one.

Three siblings sit close enough to confuse. A hunk containing animation code belongs to `motion-review`; a rendered screen or screenshot instead of a diff belongs to `design-critique`; and the single question "does this look AI-generated?" belongs to `ai-tells`, which matches a fixed token list and owes no verdict. A mixed diff is still yours: review the non-motion hunks here and hand the motion hunks to `motion-review` with their `file:line` ranges.

**Read what the project already uses before writing the first row.** Grep for the token file, the Tailwind theme, the existing easing and shadow variables, the component library in `package.json`. A finding that proposes a value the project does not use is a proposal to fork the design system, and it is wrong even when the value is better in isolation. Quote the project's own token in the After column whenever one exists; propose a raw value only when grep proves there is no scale to quote, and say so in the Why. Never resolve a finding by introducing a second styling system.

## Quick reference

| Topic | File | Open it when |
|---|---|---|
| Exact non-motion thresholds — a11y floor, layout stability, type, surface, API, perf, residue | `references/standards.md` | Open it the moment a finding needs a number you would otherwise approximate, so the Why column can cite a threshold instead of an adjective. |

## Review order

Read in this order and rank findings in this order. The last column names who owns the value, so a finding cites one skill instead of loading five.

| # | Dimension | A finding here looks like | Value owner |
|---|---|---|---|
| 1 | Interaction correctness | an action reachable only by mouse; Escape not wired | this skill |
| 2 | Accessibility floor | icon-only button with no accessible name; `outline: none` | `a11y`, `touch-input`, `color` |
| 3 | Layout stability | a ticking figure with no tabular numerals; unsized image | `ui-polish` |
| 4 | Motion | present at all | route to `motion-review` |
| 5 | Spacing & hierarchy | an off-scale value; two competing primary actions | `spacing`, `layout` |
| 6 | Type | a 95-character measure; a synthesized bold | `typography` |
| 7 | Surface & depth | a shadow that belongs to no ladder; non-concentric radii | `surfaces`, `dark-mode` |
| 8 | Component API | eleven boolean props — only when a shared component is added | `component-api` |
| 9 | Performance | an unbounded list rendered without virtualization | `perf` |
| 10 | Residue | selection, cursors, scrollbars, missing empty and error states | `ui-polish`, `ui-states` |

## Core principles

1. **Read the whole diff before writing a row.** Rank is a property of the set — you cannot rank the first finding until you have seen the last. Write `0` rows during the first pass. *Exception:* when the diff is too large to hold at once, review it surface by surface and name in the verdict which surfaces you covered.

2. **Block on the accessibility floor; negotiate everything else.** It is a floor, so a violation is a finding regardless of how the rest reads: `44×44px` targets (Apple HIG), `4.5:1` body and `3:1` large-text contrast (WCAG), `16px` minimum on `<input>` so iOS Safari does not zoom on focus, and a visible ring on every keyboard-reachable control. *Exception:* a visually smaller target passes if padding or a pseudo-element already extends the hit area to 44×44px — measure before flagging.

3. **An absence is a finding and it gets a row.** Missing `:focus-visible`, missing `aria-label`, missing `:disabled` styling, missing empty state. Write the Before cell as the selector followed by `(absent)`. *Exception:* do not flag missing interaction states on an element that is not interactive.

4. **Never let a changing number reflow the layout.** Proportional figures have different advance widths, so a counter jitters its neighbours every tick: require `font-variant-numeric: tabular-nums` on anything that updates in place. *Exception:* a figure that only changes on a deliberate navigation does not need tabular numerals.

5. **Route motion; do not rule on it.** Duration, curve, origin, and interruptibility have one owner and it is not this skill. *Exception:* `transition: all` is a lint-level prohibition — flag it in place with `transition: transform 200ms ease-out` in the After cell, then still route the hunk.

6. **Cite the exact value in every Why.** An adjective is a reaction, not a finding: `padding: 13px` is off the project's scale and the nearest step is `12px` — "the padding is tight" is not reviewable. *Exception:* a phenomenon with no number (a heading orphan, optical mis-centering) is named instead; `naming` owns the term.

7. **One issue per row, ordered by the review table.** Combining three changes into one row hides two of them from whoever applies the patch. *Exception:* a one-character nit inside a blocking row rides along on that row rather than earning its own.

8. **Say it plainly when it ships.** The verdict is exactly one of `Blocked`, `Approve with changes`, or `Ship it`, and manufacturing nits to look thorough spends trust you will need on the next review. *Exception:* if the diff touches a surface you could not exercise — email rendering, print, a native shell — name it and scope the verdict to what you reviewed.

## Smells

| Smell | Fix |
|---|---|
| `transition: all` | Name the properties: `transition: transform 200ms ease-out` |
| Icon-only button with no accessible name | `aria-label`, or visually-hidden text |
| `outline: none` with no replacement | A `:focus-visible` ring on the same element |
| Core action available only on `:hover` | A keyboard- and touch-reachable equivalent |
| `<input>` under `16px` | `16px` minimum, or a font-size bump at the touch breakpoint |
| `z-index: 9999` | A named layer from the project's scale, or `isolation: isolate` |
| Dynamic number with no reserved box | `tabular-nums` plus a fixed min-width |
| Font weight that changes on hover or select | Change color or background — weight reflows the text by a pixel |
| Unbounded list rendered in full | Virtualize, or paginate |
| Image with no `width`/`height` or `aspect-ratio` | Lock the ratio so nothing shifts on load |

## Output format

Lead with one verdict line. Then up to three tables, under the headings **Blocking**, **Should fix**, and **Nits**, each with the columns `| Before | After | Why |`, one row per issue, ordered by the review table. Omit any heading with no rows. Never emit the `Before:` / `After:` list form. Cite `file:line` in the Before cell. If motion hunks were routed, close with a one-line handoff naming their ranges and the skill they went to.

Blocked means at least one finding breaks an interaction or the accessibility floor. Approve with changes means every finding is a craft problem. Ship it means the tables are empty — say so in one sentence and stop.

## Checklist

- [ ] Whole diff read before the first row was written
- [ ] Project tokens grepped; After cells quote them where they exist
- [ ] Every dimension in the review table considered, in order
- [ ] Accessibility floor checked against exact thresholds, not impressions
- [ ] Absences written as rows with `(absent)` in the Before cell
- [ ] Motion hunks routed to `motion-review`, not judged here
- [ ] Every Why cites a value, a token, or a named phenomenon
- [ ] One issue per row; `file:line` present
- [ ] Verdict is exactly one of `Blocked` / `Approve with changes` / `Ship it`
- [ ] No nit invented to fill a table
