---
name: typography
description: "Use when setting type: scale, weight, line-height, measure, tracking, numerals, font loading, and hierarchy carried by weight and grey instead of size."
---


# Setting Type

Default posture: one family, a short closed scale, unitless leading banded by role, a capped measure — and hierarchy carried by **weight and grey value before size**. Most product UI never needs a display size at all. Benji Taylor's site sets its article `h1` at `15px/600`, `h2` at `14px/560` and body at `14px/460` on a `20px` line-height with `-0.09px` tracking, and `19px` is the largest type anywhere on it; the page still reads as ordered because weight and value do the work size normally does. Reach for a larger step only once weight and grey have run out. **This skill sets type for legibility and rhythm; whether the family *expresses* the brand belongs to `brand-identity`, which picks the face and never renegotiates the scale, leading, measure or numerals fixed here.** The words inside the type are `ui-copy`. Contrast ratios have exactly one owner and it is `color`.

**Detect the styling idiom before proposing a single declaration.** Read how the project already expresses type — Tailwind utilities, a `@theme` block, CSS custom properties, CSS Modules, styled-components, generated tokens — and write every fix in that same mechanism. A type fix is never a reason to bolt a second styling system onto a codebase; if the scale lives in `@theme`, the new step goes there, not in a one-off `style` prop.

## Quick Reference

| Open this | When |
| --- | --- |
| [scale-and-rhythm.md](references/scale-and-rhythm.md) | You are building or repairing the size scale itself, or setting leading and tracking per step. |
| [line-behavior.md](references/line-behavior.md) | Lines break, wrap, truncate or overflow badly, or the content is multilingual or right-to-left. |
| [typefaces-and-loading.md](references/typefaces-and-loading.md) | A face is being chosen, paired, or swapped, or text flashes, shifts or renders late on load. |
| [font-capabilities.md](references/font-capabilities.md) | You need a variable axis, an OpenType feature, small caps, or a numeral style. |
| [tailwind-map.md](references/tailwind-map.md) | The project is Tailwind and you need the utility for a declaration named in this skill. |

## Core Principles

1. **Carry hierarchy with weight and grey value before you carry it with size.** Size inflation is what makes an app look like a poster; weight and value separate roles without spending vertical space. Ship a near-flat scale where the whole body sits at `14–16px` and roles separate at `460 / 560 / 600`, with secondary text stepping down in value rather than in size. *Exception:* marketing surfaces, where `marketing-pages` explicitly buys a display step for the hero.
2. **Every `font-size` traces back to a closed scale.** Ad-hoc values decay fast: each new component invents a size that is nearly, but not exactly, an existing one. Define six to eight steps — a ratio-derived set (`1.2` on a `16px` root) or Tailwind's `text-*` both qualify. *Exception:* a wordmark or one optical fix on a single headline, which gets a comment saying why it is off-scale.
3. **Write `line-height` unitless and band it by role.** A hard-coded `24px` leading detonates on the first size change or user zoom. Body copy reads at `1.5`–`1.6`; display and headings sit near `1.1`. *Exception:* single-line boxed labels — buttons, badges, table cells — where the box sets the height and `line-height: 1` (plus `text-box` trimming) is correct.
4. **Cap the reading measure near `65ch`.** Past roughly 75 characters the eye loses its return path and reading turns into work; `max-width: 65ch` states the intent directly, and Tailwind's `max-w-prose` is defined as exactly `65ch`. This is a house default, not a standards number. *Exception:* table cells, code blocks and dense grids, where the column, not the measure, sets the width — `dense-ui` owns those.
5. **Apply tracking only at the two ends of the scale.** Large glyphs are fit too loosely and small capitals too tightly; body sizes are already fit for reading. Use roughly `-0.015em` on display steps and `0.06em` on small uppercase labels, and write it in `em` so it scales with the text. *Exception:* none for body copy — a single `letter-spacing` value applied uniformly across a whole scale is a finding, not a style.
6. **Put `tabular-nums` on any number that changes in place.** Most fonts draw a narrow `1` and a wide `4`, so a live timer, price, counter or ticking total shoves its neighbours on every update. Reach for `font-variant-numeric: tabular-nums`. *Exception:* numbers inside running prose, where proportional figures read better and nothing re-renders.
7. **Ask for a CSS property, never the raw axis or feature tag.** High-level properties still do something sensible when a fallback font renders; a raw tag aimed at a font that never loaded does nothing at all. Write `font-weight: 620`, `font-optical-sizing: auto`, `font-variant-numeric: tabular-nums`. *Exception:* things with no property of their own — a custom axis such as Fraunces' `"WONK" 1`, or a numbered stylistic set such as `"ss03" 1`.
8. **Forbid synthesized styles.** Ask for a bold or italic that was never loaded and the browser fabricates one by thickening or shearing the real glyphs, which reads as a quietly ugly render rather than an obvious bug. Declare `font-synthesis: none` once at the root. *Exception:* a deliberate system-stack product that ships no font files — then synthesis is all there is, and the decision belongs in a comment.
9. **Switch typeface for emphasis before you add a weight.** When body weight already carries hierarchy, another bold flattens the page; a second face marks the emphasis without competing. Benji's articles emphasise by switching to Newsreader italic at `opsz 10` rather than bolding. *Exception:* single-family products, where bold is the only tool — and italic never becomes UI hierarchy, since italic means citation and linguistic stress, not importance.
10. **Serve `woff2`, subset it, and reserve the space it will occupy.** `woff2` carries Brotli compression and every browser that matters accepts it; `ttf`/`otf` are uncompressed desktop containers. Preload the one face above the fold and metric-match the fallback so the swap does not shift layout. *Exception:* `woff` when a written requirement names a genuinely ancient browser.

Non-integer variable weights are legitimate — `460`, `560` and `430` are real values in a variable font, and they are how a near-flat scale gets its separation. One floor restated from Tier 0: mobile input text never drops below `16px`, and `maximum-scale=1` is a WCAG 1.4.4 failure, never the fix; `touch-input` holds the rest of the iOS Safari quirks.

## Smell / Fix

| Smell | Fix |
| --- | --- |
| Layout twitches as a number ticks | `font-variant-numeric: tabular-nums` |
| Bold looks smudged or unusually black | The weight file never loaded; load it and set `font-synthesis: none` |
| Weight change does nothing on some machines | Weight set via the raw `"wght"` tag — use `font-weight` |
| Headline breaks seven words / one word | `text-wrap: balance` |
| Paragraph ends on a stranded single word | `text-wrap: pretty` |
| Reading a paragraph feels like work | Measure far past 75 characters — cap near `65ch` |
| Text is cramped in one component, airy in another | One-off sizes and leading — route both through the scale |
| Page looks like a poster inside an app | Hierarchy carried by size — move it to weight and grey value |
| Small uppercase labels look clumped | Missing positive tracking (`0.06em`) |
| Long URL blows out a card | `overflow-wrap: break-word` |
| Text pops in late or reflows on load | No preload and no metric-matched fallback |
| ALL-CAPS strings scattered through JSX | Sentence case in the source, `text-transform` in CSS |
| Ellipsis with no way to see the rest | Add a tooltip or expand control |

## Reporting a Type Pass

Group findings by file. Each is one line: where it is, what is wrong, the corrected declaration in the project's own idiom, and the principle number it serves. Stay silent on what the code already gets right, and fix with the smallest possible diff — type work does not restructure markup unless an expandable truncation genuinely needs an extra element.

## Checklist

- [ ] Hierarchy separates by weight and value first; size is the last resort
- [ ] Every `font-size` traces to a closed scale, exceptions commented
- [ ] `line-height` unitless — `1.5`–`1.6` body, ~`1.1` display, `1` on boxed single-line labels
- [ ] Reading columns capped near `65ch`
- [ ] Tracking only at the extremes, written in `em`; body is `0`
- [ ] `tabular-nums` on every value that updates in place
- [ ] Weights and features go through `font-weight` / `font-variant-*`; raw tags only for custom axes and numbered sets
- [ ] `font-synthesis: none` declared; no fabricated bold or italic anywhere
- [ ] Emphasis uses a second face or a real weight, never italic-as-hierarchy
- [ ] Fonts are `woff2`, subset, preloaded above the fold, with a metric-matched fallback
- [ ] Mobile input text is `16px` or larger; no `maximum-scale=1`
- [ ] Source strings keep human casing; any shouting is done by CSS
- [ ] Every truncation offers a route to the full string
- [ ] Logical properties plus `lang` / `dir` wherever direction can vary
