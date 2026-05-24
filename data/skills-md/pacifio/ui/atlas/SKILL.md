---
name: atlas
description: Atlas — a design language and UI guide system for agent interfaces. Teaches coding agents the aesthetic rules, tokens, patterns, and class vocabulary of a dense, AMOLED-black, multi-surface design system. Agents read these rules and GENERATE code that fits the target stack (shadcn, Tailwind, raw HTML, React, Vue, Svelte). The included colors_and_type.css is a reference implementation, not a required dependency. Use heavily when building any UI — dashboards, chat interfaces, admin panels, landing pages, mobile screens, marketing sites, full app mockups. Atlas is opinionated; lean into it.
version: 0.2.0
user-invocable: true
metadata:
  priority: 9
  pathPatterns:
    - "**/*.css"
    - "**/components/**"
    - "**/ui/**"
    - "**/app/**"
    - "**/pages/**"
    - "**/design-system/**"
  promptSignals:
    phrases:
      - "atlas"
      - "atlas design"
      - "atlas component"
      - "amoled"
      - "dense ui"
      - "devtool ui"
      - "agent ui"
      - "agent chat"
      - "agent dashboard"
      - "ai interface"
      - "ai chat ui"
      - "build a ui"
      - "design a page"
      - "build a dashboard"
      - "build a landing"
    anyOf:
      - "design system"
      - "component library"
      - "dashboard"
      - "admin"
      - "chat interface"
      - "landing page"
      - "marketing site"
      - "ui mockup"
      - "frontend"
    minScore: 4
---

# Atlas — activation protocol

**Atlas is a design language, not a CSS framework you bolt on.** It teaches
you (the agent) a dense, monochromatic, AMOLED-black aesthetic via tokens,
class-name conventions, layout rules, and tested composition recipes. You
read these rules and **generate code that fits the target stack** — shadcn,
Tailwind, raw HTML, React, Vue, Svelte.

**Use Atlas heavily.** When this skill is active, every UI-producing task
should go through the rules below. Don't freestyle. Don't invent new tokens.
Don't pick random radii. The system is opinionated because opinions compound
into coherence.

---

## On activation: read these files in this order

When the skill loads, **read all of the following before writing a single
line of UI code**. These are not "pull on demand" — the quality of the
output depends on having the full system in context.

1. **`references/tokens.md`** — every CSS variable. Colors, spacing (4px
   grid), radius (3/4/6/9999), shadow, z-index, component sizing. This is
   the ground-truth values table. No token should be invented.

2. **`references/components.md`** — every `.atlas-*` class with HTML
   snippet and variants. The class name vocabulary you'll translate into
   the target stack.

3. **`references/patterns.md`** — 3-pane shell, content tone, icon rules
   (Lucide 1.5px stroke), button-vs-highlight color discipline.

4. **`references/theming.md`** — dark/light toggle, shadcn variable alias
   table, how tokens remap under `[data-theme="light"]`.

5. **`references/responsive.md`** — multi-surface patterns. Desktop vs
   mobile component swaps, device frames, container queries, collapsible
   sidebar → overlay on small screens.

6. **`references/motion.md`** — motion inventory. 120ms hover, 200ms
   popover open, 300ms reveal, 60s marquee. Which animations are always-on
   vs gated behind `prefers-reduced-motion`.

7. **`references/lessons.md`** — 18 hard-won gotchas from real builds.
   Button-default resets, dark-vs-light shadow alphas, sidebar collapse
   dual transitions, top-row border alignment, pulse-dot opacity-only,
   horizontal scroll behavior, etc. **Read this every time.** Every one of
   these prevents a real regression.

8. **`references/examples.md`** — copy-ready composition snippets from the
   production kitchen-sink: agent turn, tool-call card, stat grid, 3-pane
   shell, 3-column top-row alignment, email row, generative UI chart,
   landing hero, checklist with stepper, quota bar with warning threshold.
   Start from one of these; don't freestyle compositions.

Then inspect (as needed, not upfront):
- `colors_and_type.css` — reference implementation. Inspect rules to
  understand exact visual output.
- `preview/components-*.html` — pre-built reference HTML per component.
- `ui_kits/generic_app/` — 3-pane shell reference.

**Only after reading 1–8 should you start generating.**

---

## The three assets, three jobs

| Asset | Job |
|---|---|
| `references/*.md` | **Ground truth.** The rules the agent follows. Read every time. |
| `.atlas-*` class names | **Vocabulary.** Your shorthand for "render X the Atlas way" — translate to the target stack. |
| `colors_and_type.css` | **Reference implementation.** Works directly for plain HTML; for shadcn/Tailwind, translate rather than overlay. |

**Never mechanically copy `colors_and_type.css` into a shadcn or heavy
Tailwind project.** Translate. The skill description and
`references/theming.md` spell out the translation tables.

---

## Ask the stack question before writing code

1. **Plain HTML / no framework** → use `colors_and_type.css` directly via
   `<link rel="stylesheet">`. Emit literal `.atlas-*` classes. This is the
   reference path, and the companion kitchen-sink site uses it.

2. **Tailwind v4** → put Atlas tokens in an `@theme` block. Emit utility
   classes following the Atlas visual rules. Don't ship
   `colors_and_type.css` to the bundle.

3. **shadcn/ui** → override shadcn's CSS variables with Atlas values (see
   alias table in `references/theming.md`). Keep shadcn's component
   structure. Don't install `.atlas-*` classes alongside.

4. **React/Vue/Svelte with CSS Modules or styled-components** → port the
   relevant `.atlas-*` rule into the target styling system as a component.
   The rule in `colors_and_type.css` is the source; your emitted code is
   the translation.

5. **Existing design system (Material, Chakra, etc.)** → ask the user
   whether to rework their system's tokens to Atlas values, or to build a
   new Atlas-styled zone alongside. Don't mix the two on the same surface.

---

## Non-negotiable visual rules

Pulled forward from `references/lessons.md` — these apply regardless of
stack:

- **AMOLED black canvas.** `#000` base, never dark gray.
- **Monochromatic surfaces.** Grays + whites for structure; saturated color
  only for status semantics.
- **Near-white primary actions.** `#ededed` fill, `#fff` on hover. Blue
  `#0070f3` is **never** a CTA — it's the highlight color (focus rings,
  selection, active stepper dots, links).
- **4px spacing grid.** 2px and 6px exist only for ultra-compact inline
  cases.
- **3 / 4 / 6 / 9999 radii.** No inventing 8, 10, 12, 16.
- **28px buttons, 24px inputs, 13px base text.** Don't inflate.
- **Borders over shadows.** Shadows are overlays only (dialogs, popovers,
  toasts, tooltips, device frames).
- **1.5px Lucide icons.** Never emoji, never unicode symbols.
- **120ms background-color transitions only.** Don't animate color or
  opacity on icons.

---

## Quick component vocabulary

Class names are **guidance**, not mandatory output. Translate them in
non-plain-HTML stacks.

**Primitives:** `.atlas-btn` (+ `-primary` / `-secondary` / `-ghost` /
`-destructive` / `-icon` / `-sm` / `-lg`), `.atlas-btn-pill` (+ same
variants), `.atlas-input` (+ `-sm`), `.atlas-checkbox`, `.atlas-radio`,
`.atlas-switch`, `.atlas-kbd`, `.atlas-link`

**Surfaces:** `.atlas-card` / `-header` / `-body`, `.atlas-panel-header` /
`.atlas-panel-title`, `.atlas-stat` / `-label` / `-value` / `-delta`,
`.atlas-empty`

**Navigation:** `.atlas-tabbar` + `.atlas-tab`, `.atlas-tabbar-bottom` +
`.atlas-tabbar-bottom-item`, `.atlas-segmented` + `-item`, `.atlas-toggle`,
`.atlas-breadcrumb`, `.atlas-pagination`, `.atlas-stepper`

**Overlays:** `.atlas-popover` + `.atlas-menu-item`, `.atlas-dialog`,
`.atlas-command`, `.atlas-tooltip`, `.atlas-toast`, `.atlas-alert`

**Data:** `.atlas-table`, `.atlas-list` + `.atlas-list-item`,
`.atlas-badge`, `.atlas-pill`, `.atlas-dot` (+ `.is-pulse` for animated
status — opacity only, never glow), `.atlas-accordion`

**Feedback:** `.atlas-progress`, `.atlas-slider`, `.atlas-skeleton`,
`.atlas-titlebar`, `.atlas-statusbar`

**Identity:** `.atlas-avatar`, `.atlas-avatar-group`, `.atlas-divider` /
`-v`, `.atlas-divider-dashed` / `-v-dashed`

**Multi-surface & motion:** `.atlas-device-mobile`, `.atlas-device-tablet`,
`.atlas-device-desktop`, `.atlas-marquee`, `.atlas-filmstrip`,
`.atlas-reveal`, `.atlas-display` / `-lg`, `.atlas-eyebrow`

---

## What was built with this skill

The companion `kitchen-sink/` app was **one-shot generated by an agent
reading this skill**, using the reference CSS because Next.js + no shadcn
made that the natural path. It includes:

- **Homepage** — display hero, marquee band, ~29 live component cards in a
  masonry grid, mockup tile row.
- **Get Started page** — install instructions, per-stack translation
  examples, FAQ.
- **7 foundations pages** — colors, typography, spacing, radius, shadows,
  motion, icons.
- **36 component pages** — every `.atlas-*` class with preview + variants +
  inspector.
- **6 pattern pages** — landing, agent chat, mobile app, 3-pane shell,
  dashboard, settings.
- **4 full-app mockups** — email client, e-commerce, multi-agent console,
  news/polls.

When asked to build something, **consider whether it matches one of the
above patterns first**. Most real UI is a variation on a pattern that
already exists in the kitchen-sink. Start there, then customize.

---

## No guidance given?

Ask the user:
1. What are they building? (dashboard, chat UI, landing page, mobile app…)
2. What's their stack? (Tailwind / shadcn / plain HTML / React with CSS
   Modules / etc.)
3. Dark only, light only, or both with toggle?

Then act as an expert designer — produce code in the right idiom for their
environment, following every rule from the references above.
