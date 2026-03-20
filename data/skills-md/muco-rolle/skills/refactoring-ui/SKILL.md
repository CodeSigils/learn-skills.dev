---
name: refactoring-ui
description: >
  Comprehensive UI design system for developers — build, review, and polish user interfaces
  using systematic principles from Refactoring UI. Covers visual hierarchy, spacing, typography,
  color palettes, depth/shadows, images, and finishing touches with concrete CSS/Tailwind values.
  Use this skill whenever the user wants to build a UI component, create a page layout, design
  a dashboard, style a form, make a landing page, improve visual hierarchy, fix spacing issues,
  choose colors, add shadows, polish a design, make something "look better" or "more professional",
  review UI code, refactor a design, or any task involving frontend visual design. This skill
  should be used even when the user doesn't explicitly mention "design" — if they're building
  any user-facing interface, these principles apply.
---

# Refactoring UI

Good UI design isn't about talent or artistic ability — it's about making deliberate, systematic choices. Every visual decision (spacing, color, typography, depth) has a small set of correct answers that you can learn and apply consistently. This skill gives you those answers.

## Core Philosophy

- **Start with content, not chrome.** Begin with the actual feature and data. Don't start with a navbar and sidebar — start with the content that matters and build outward.
- **Work in cycles.** Get the structure right first with plain text and basic layout. Then layer in hierarchy, typography, color, depth, and polish — in that order.
- **Constrain your choices.** Pre-define scales for spacing, font sizes, colors, and shadows. Choosing from a system is faster and more consistent than picking arbitrary values.
- **Design every detail deliberately.** If you haven't consciously decided on a value, it's probably wrong. Every pixel of spacing, every shade of grey, every font weight should be intentional.

## Building New UI

When creating an interface from scratch, follow this sequence:

1. **Start with the feature, not the layout.** Build a single component with real content. Don't think about navigation, sidebars, or page structure yet.
2. **Establish hierarchy.** Decide what information is primary (large, dark, bold), secondary (smaller, medium grey), and tertiary (small, light). Not everything can be important.
3. **Apply your design system.** Use the scales below for spacing, typography, and color. Pick values from the system — never invent new ones mid-design.
4. **Add depth and polish.** Apply shadows for elevation, accent borders for flair, and finishing touches that elevate the design from functional to professional.
5. **Consult references.** When you need specific techniques (e.g., how to build a color palette, how to style text on images), read the relevant reference file.

## Improving Existing UI

When reviewing or refactoring an existing interface:

1. **Read the code.** Understand the current HTML structure and CSS/Tailwind classes.
2. **Audit across six domains.** Check hierarchy, typography, color, depth, images, and finishing touches. See the quick reference below.
3. **Prioritize by impact.** Fix the biggest visual problems first — usually hierarchy and spacing issues have the most impact.
4. **Apply fixes with explanation.** Reference which principle you're applying so the developer learns the reasoning.

## Design System Foundations

Define these scales upfront and use them consistently:

### Spacing Scale
`4, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256` (in px)

In Tailwind: `1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64`

**Important:** Never use off-scale values like 6px, 10px, 14px, 15px, 20px, or 40px. Always pick the nearest scale value instead (e.g., use 8px not 6px or 10px, use 16px not 14px or 15px or 20px).

### Font Size Scale
`12, 14, 16, 18, 20, 24, 30, 36, 48, 60, 72` (in px)

In Tailwind: `xs, sm, base, lg, xl, 2xl, 3xl, 4xl, 5xl, 6xl, 7xl`

### Font Weights
- 400 (normal) — body text, secondary content
- 500 (medium) — emphasized body text
- 600 (semibold) — headings, primary labels
- 700 (bold) — hero text, key metrics

### Shadow Elevation System (5 levels)
- **xs:** `0 1px 3px hsla(0,0%,0%,.2)` — buttons, inputs
- **sm:** `0 4px 6px hsla(0,0%,0%,.1)` — dropdowns, tooltips
- **md:** `0 5px 15px hsla(0,0%,0%,.2)` — cards, panels
- **lg:** `0 10px 24px hsla(0,0%,0%,.2)` — popovers, drawers
- **xl:** `0 15px 35px hsla(0,0%,0%,.2)` — modals, dialogs

### Color Palette Structure
- **Greys:** 8-10 shades (100-900), slightly saturated with blue (cool) or yellow (warm)
- **Primary:** 5-10 shades of your brand color
- **Accents:** 5-10 shades each for semantic colors (red/danger, yellow/warning, green/success, teal/info)

Use HSL for all colors. See `references/color.md` for palette construction process.

## Principle Quick Reference

| # | Principle | Domain | Reference |
|---|-----------|--------|-----------|
| 1 | Use size, weight, AND color for hierarchy — not size alone | Hierarchy | hierarchy-and-layout.md |
| 2 | Primary/secondary/tertiary: establish 3 levels of emphasis | Hierarchy | hierarchy-and-layout.md |
| 3 | De-emphasize secondary content instead of over-emphasizing primary | Hierarchy | hierarchy-and-layout.md |
| 4 | Labels are secondary; bold the data, lighten the label | Hierarchy | hierarchy-and-layout.md |
| 5 | Use a spacing/sizing scale — never pick arbitrary values | Hierarchy | hierarchy-and-layout.md |
| 6 | Constrain paragraph width to 20-35em | Hierarchy | hierarchy-and-layout.md |
| 7 | Don't force 12-column grids; give elements the space they need | Hierarchy | hierarchy-and-layout.md |
| 8 | Visual hierarchy ≠ document hierarchy; H2 can look smaller than a span | Hierarchy | hierarchy-and-layout.md |
| 9 | Large text → thinner weight; small text → heavier weight | Hierarchy | hierarchy-and-layout.md |
| 10 | Replace borders with spacing, background changes, or box-shadows | Hierarchy | hierarchy-and-layout.md |
| 11 | Match design fidelity to feature importance | Hierarchy | hierarchy-and-layout.md |
| 12 | Stick to 1-2 font families | Typography | typography.md |
| 13 | Use the font size scale; don't invent sizes | Typography | typography.md |
| 14 | Line-height inversely proportional to font size | Typography | typography.md |
| 15 | Line-height proportional to line length | Typography | typography.md |
| 16 | Baseline-align mixed font sizes, not center | Typography | typography.md |
| 17 | Left-align body text; center only ≤2-3 lines | Typography | typography.md |
| 18 | Right-align numbers in tables | Typography | typography.md |
| 19 | Tighten headline letter-spacing; widen all-caps letter-spacing | Typography | typography.md |
| 20 | Not every link needs a color — use weight/hover in dense link UIs | Typography | typography.md |
| 21 | Use HSL, not hex | Color | color.md |
| 22 | Build 8-10 shade palettes per color, not just 5 swatches | Color | color.md |
| 23 | Define shades with 100-900 scale; base=500, edges=100/900 | Color | color.md |
| 24 | Increase saturation as lightness moves from 50% | Color | color.md |
| 25 | Rotate hue ±20-30° for richer lighter/darker shades | Color | color.md |
| 26 | Saturate greys with blue (cool) or yellow (warm) | Color | color.md |
| 27 | WCAG: 4.5:1 contrast for small text, 3:1 for large | Color | color.md |
| 28 | Flip contrast on colored backgrounds: dark text on light bg | Color | color.md |
| 29 | Don't rely on color alone — add icons/text for colorblind users | Color | color.md |
| 30 | Light comes from above: top edges lighter, bottom edges darker | Depth | depth-and-shadows.md |
| 31 | Use the 5-level shadow elevation system consistently | Depth | depth-and-shadows.md |
| 32 | Two-part shadows: direct light (large/soft) + ambient (small/tight) | Depth | depth-and-shadows.md |
| 33 | Shadows for interaction: bigger on hover, smaller on click | Depth | depth-and-shadows.md |
| 34 | Flat depth: lighter=closer, darker=further; solid shadows | Depth | depth-and-shadows.md |
| 35 | Overlap elements across boundaries for layering | Depth | depth-and-shadows.md |
| 36 | Text on images: overlay, lower contrast, colorize, or text-shadow | Images | images-and-icons.md |
| 37 | User images: fixed containers + object-fit:cover + inset shadow | Images | images-and-icons.md |
| 38 | Don't scale icons up or down; use intended size or redraw | Images | images-and-icons.md |
| 39 | Replace bullets with contextual icons | Finishing | finishing-touches.md |
| 40 | Add accent borders: card tops, nav items, alerts, headlines | Finishing | finishing-touches.md |
| 41 | Vary backgrounds: color, gradients (≤30° hue diff), subtle patterns | Finishing | finishing-touches.md |
| 42 | Design empty states with illustration + CTA | Finishing | finishing-touches.md |
| 43 | Custom-style form controls with brand colors | Finishing | finishing-touches.md |

## When to Consult References

Read the reference files in `references/` when you need:
- **Specific CSS values** (shadow sizes, contrast formulas, spacing values)
- **Step-by-step processes** (building a color palette, constructing a shade scale)
- **Edge-case guidance** (text on images, accessible colored backgrounds, flat design depth)

Each reference file is self-contained and can be read independently for its domain.
