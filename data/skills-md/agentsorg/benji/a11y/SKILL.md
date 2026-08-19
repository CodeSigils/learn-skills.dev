---
name: a11y
description: "Use when a UI must work without a mouse or without sight: keyboard order, focus management, focus-visible, ARIA roles, live regions, and announcements."
---


# Keyboard and Assistive Access

Build the keyboard path first and let the pointer be the enhancement. Every interactive thing must be reachable by Tab, operable by Enter, Space or arrows, and announced with a name, a role and a state — and the cheapest way to get all of that is to stop reimplementing it. A `<button>` already carries the role, the focus behaviour, the Enter/Space handling, the disabled semantics and the forced-colors treatment that a `div` with a click handler will get wrong for the next three years. Assume nothing about the user's input device and change nothing that the platform already does correctly. **Pointer physics belong to `touch-input` — hit-target size, hover gating and tap latency are its nouns and never appear here; `a11y` owns the keyboard and the accessibility tree.** Contrast ratios have exactly one owner and it is `color`; do not restate them.

**Read the project before adding anything.** If it already renders Radix, Base UI, React Aria or Headless UI primitives, the focus trap, the roving tabindex and the ARIA wiring exist — configure them and delete your parallel implementation. If there is a `FocusScope` or `useFocusTrap` in the codebase, that is the one. If the project is plain semantic HTML, the fix is almost always swapping an element, not adding attributes. Never introduce a second a11y layer next to a working one; two focus traps fight and the outer one wins.

| Topic | Reference |
|---|---|
| Wiring one specific widget | Open `references/aria-recipes.md` when you need the exact key bindings and ARIA contract for a dialog, menu, combobox, tabs, disclosure, listbox or grid. |
| Sweeping a screen or a PR | Open `references/audit.md` when you are checking existing work and need the pass order, what each pass catches, and how to rank what you find. |

## Core Principles

1. **Reach for the native element before the ARIA attribute.** ARIA adds semantics and nothing else — no focus, no key handling, no state. `role="button"` on a `div` still needs `tabindex`, an Enter handler, a Space handler and a `aria-disabled` story; `<button type="button">` needs none. *Exception:* composite widgets with no native equivalent — combobox, tree, grid, toolbar — which is exactly what `references/aria-recipes.md` exists for.

2. **Tab order is DOM order. Never write a positive `tabindex`.** A positive value creates a second, invisible ordering that silently drifts the first time anyone reorders the markup. Only `tabindex="0"` (add to the order) and `tabindex="-1"` (focusable by script only) are legitimate. *Exception:* a roving-tabindex composite, where every child but the active one is deliberately `-1`.

3. **Anything invisible must be unfocusable.** `opacity: 0`, `transform: translateX(-100%)` and `height: 0` all leave the subtree in the tab order — closed drawers and off-screen carousels are where keyboard users fall into a void. Use `inert` on the container, or `visibility: hidden`. *Exception:* skip links and live regions must stay in the accessibility tree while staying off-screen — clip them with `position: absolute; clip-path: inset(50%)`, never `visibility: hidden`.

4. **`:focus-visible` gets the ring, and `:focus { outline: none }` never ships alone.** Killing the outline to hide it from mouse users kills it for keyboard users on the same element. Ship `:focus-visible { outline: 2px solid var(--focus); outline-offset: 2px }` and pair every `outline: none` with a replacement in the same rule. *Exception:* text inputs should keep a ring on plain `:focus` — in a dense form the caret alone is too weak an affordance.

5. **Focus enters on open and returns on close.** On open, move focus to the first interactive element, or to the dialog container itself when the first control is destructive. On close, return it to the trigger — capture that node at open time, and if it has unmounted, fall back to the nearest surviving ancestor. Focus must never land on `document.body`, which sends a keyboard user back to the top of the page. *Exception:* non-modal surfaces — toasts, ambient popovers, autosave notices — must not take focus at all.

6. **One trap at a time, and `Escape` closes exactly one layer.** A trap inside a trap is unescapable in some screen-reader modes, and `Escape` that closes two layers loses work. Which container a flow gets is decided by `modal-or-page`; this skill only requires that whatever it is, it traps once and unwinds one step per press. *Exception:* an alert dialog confirming a destructive action opened from inside a dialog — a deliberate second layer, which must return focus to the first on close.

7. **Announce the change, not the screen.** A client-side route change is silent: the DOM swaps and a screen-reader user hears nothing at all. On navigation, move focus to the new `<h1>` (`tabindex="-1"`, focus it, do not scroll-jack) and mirror async results into a live region. *Exception:* a result rendered immediately next to the control that caused it needs no announcement — moving focus into it says more than reading it aloud.

8. **A live region must exist before its text does, and defaults to `polite`.** Injecting the container and its content in the same tick announces nothing in most screen readers; the region has to be observed empty first. Render an empty `aria-live="polite"` node on mount and write into it later. Reserve `assertive` / `role="alert"` for the two things that earn an interruption: a failed submit and lost data. *Exception:* if your toast library already renders a polite region, use it — nesting two live regions produces a double announcement.

9. **Reduced motion means fewer and gentler animations, not zero** (Emil Kowalski). Deleting every transition removes the state change along with the movement, and the user loses the cue entirely. Under `prefers-reduced-motion: reduce`, keep `opacity` and colour transitions; drop translation, scale, parallax and auto-playing loops. *Exception:* motion that *is* the content — a video, an explanatory animation — gets a play control rather than deletion.

10. **Never take zoom away.** `user-scalable=no` and `maximum-scale=1` fail WCAG 1.4.4 (Resize Text), and the layout must survive 200% zoom and forced text spacing without clipping or overlap. The mobile-input-zoom annoyance that tempts people here has a real fix that costs nothing, and it lives in `touch-input`. *Exception:* an element implementing its own pinch-zoom (a map, a canvas) may take `touch-action: none` for itself — the page around it must still zoom.

## Smells and Fixes

| Smell | Fix |
|---|---|
| `<div onClick>` with `role="button"` | `<button type="button">`; delete the role, the `tabindex` and the key handlers |
| `:focus { outline: none }` anywhere | `:focus-visible { outline: 2px solid var(--focus); outline-offset: 2px }` |
| Panel hidden with `opacity: 0` or `translate` | `inert` on the container, or `visibility: hidden` |
| `aria-label` on an element that already has visible text | Delete it; label the icon `aria-hidden="true"` instead |
| Live region rendered together with its message | Render the empty region on mount, write the message after |
| `aria-live="assertive"` on a success toast | `polite`; assertive is for failed submits and data loss |
| Dialog closes and focus is on `<body>` | Store the trigger node at open; restore it, or its nearest surviving ancestor |
| `@media (prefers-reduced-motion: reduce) { * { animation: none !important } }` | Keep opacity and colour; drop transforms only |
| `tabindex="1"` on a "priority" field | `tabindex="0"` and reorder the DOM |

## Finding Format

One line per finding, in this order: **element → input path that breaks → what the user hits → fix.** For example: `Filter drawer → keyboard → Tab enters the closed drawer and focus disappears → inert on the container while closed`. Naming the input path is what makes the finding reproducible; "not accessible" is not a finding.

## Checklist

- [ ] Every interactive element is a native control, or has a recipe from `references/aria-recipes.md` behind it
- [ ] Tab through the whole screen with the mouse unplugged and never lose the focus ring
- [ ] No positive `tabindex`; hidden subtrees are `inert` or `visibility: hidden`
- [ ] `:focus-visible` ring defined; no unpaired `outline: none`
- [ ] Every overlay moves focus in, traps once, returns it to the trigger, and closes on `Escape`
- [ ] Route changes move focus to the new heading; async results reach a pre-existing live region
- [ ] `assertive` used only for failed submits and data loss
- [ ] Icon-only controls have an accessible name; decorative icons are `aria-hidden`
- [ ] Reduced motion keeps opacity and colour, drops movement
- [ ] Page survives 200% zoom and forced text spacing; nothing blocks pinch-zoom
