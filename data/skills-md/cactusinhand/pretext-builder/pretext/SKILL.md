---
name: pretext
version: "2.1.0"
description: "Pretext: zero-reflow text measurement & layout via canvas measureText + pure arithmetic. Build height prediction, chat bubble shrinkwrap, masonry grids, multi-column editorial flow, obstacle-aware text routing, rich inline content, canvas/SVG rendering. Use when: 'text height', 'virtual scroll', 'masonry layout', 'pretext', 'React pretext hook', 'React layout', 'chat bubble'. Also trigger on '文字排版', '文本高度', '前端排版', 'React 虚拟列表', 'React 高度预测'."
---

# Pretext Builder

Two-phase model: **prepare** (one-time, canvas measurement) → **layout** (per-resize, ~0.0002ms, pure arithmetic, zero DOM reflow).

## Step 0: Ensure dependency

```bash
ls node_modules/@chenglou/pretext 2>/dev/null || bash ~/.claude/skills/pretext/scripts/ensure-pretext.sh
```

Skip if inside the Pretext source repo. The script auto-detects bun/pnpm/yarn/npm and creates `package.json` if missing.

If no `tsconfig.json` exists, create one with `target: "ES2022"`, `module: "ESNext"`, `moduleResolution: "bundler"`, `strict: true`.

## Step 1: Pick your path

```
What do you need from the text?
│
├─ Just height / line count (no line content needed)
│  → Fast path: prepare() + layout()
│  │
│  ├─ Virtualized list / scroll anchoring  → template: height-prediction
│  ├─ Animated expand/collapse             → template: accordion
│  ├─ Card grid with height prediction     → template: masonry
│  ├─ Virtual scroll with culling          → template: virtual-scroll
│  └─ Auto-resize textarea (pre-wrap)      → template: pre-wrap
│
└─ Need line text, widths, or cursors
   → Rich path: prepareWithSegments() + ...
   │
   ├─ Fixed width, all lines at once
   │  → layoutWithLines()
   │  ├─ Render to canvas/SVG              → template: canvas-rendering
   │  └─ Display lines in DOM              → template: multi-column-flow
   │
   ├─ Fixed width, geometry only (no text strings)
   │  → walkLineRanges()
   │  ├─ Shrinkwrap / tightest width       → template: bubble-shrinkwrap
   │  ├─ Binary search font size           → template: headline-fitting
   │  └─ Balanced text / width search      → template: shrinkwrap-width-search
   │
   └─ Variable width per line
      → layoutNextLine() with cursor handoff
      ├─ Columns with cursor handoff        → template: multi-column-flow
      ├─ Text around images/shapes          → template: obstacle-routing
      └─ Mixed text + chips/badges          → template: rich-inline
```

Read `references/templates.md` for standard template code. Pick the closest one and adapt.
For **React** applications, ALWAYS prioritize `references/react-templates.md` which includes robust patterns handling `ResizeObserver` lifecycle, async fonts, component unmounting, and zero-width caching.

Read `references/api-quick-ref.md` for full API signatures and types.

## Step 2: Write the code

Three things happen in every integration:

**Prepare once, after fonts load:**
```typescript
await document.fonts.ready
const prepared = prepare(text, '16px Inter') // or prepareWithSegments()
```

**Layout on resize (hot path — no DOM, no canvas):**
```typescript
const { height } = layout(prepared, containerWidth, lineHeight)
```

**Throttle with RAF:**
```typescript
let raf: number | null = null
function scheduleRender() {
  if (raf !== null) return
  raf = requestAnimationFrame(() => { raf = null; render() })
}
```

For multi-region flows, hand off cursors between `layoutNextLine()` calls:
```typescript
const line1 = layoutNextLine(prepared, cursor, width1)
cursor = line1.end // hand off to next region
const line2 = layoutNextLine(prepared, cursor, width2)
```

## Red lines

Testable quality gates. Fix before shipping.

1. **Fonts loaded before prepare** — `prepare()` must run after `document.fonts.ready`. Without this, segment metrics are wrong. The resulting layout will silently produce incorrect heights.
2. **Handle React edge cases** — In React, initial container width might be `0` or `undefined`, and text might be empty. `layout()` must check `containerWidth > 0` and `prepared != null` before executing. Never render layout-dependent UI before dimensions resolve.
3. **Memoize and Cache** — Re-preparing the same `(text, font)` pair wastes 0.05-5ms every time. Use `useMemo` in React, or cache by key in vanilla JS. Call `clearCache()` only when cycling through many fonts.
4. **React lifecycle** — Ensure ResizeObservers are disconnected on unmount (`return () => observer.disconnect()`) to prevent memory leaks.
5. **layout() is stateless** — No DOM reads, no canvas calls, no string work, no allocations beyond the return value. If your resize handler touches DOM before calling `layout()`, restructure to read DOM once, then compute.
6. **lineHeight is a number** — Pass `24`, not `'24px'` or `'1.5em'`. Pretext does arithmetic, not CSS parsing.
7. **Named fonts only** — `system-ui` is unsafe on macOS (canvas and DOM resolve to different optical variants). Use `'16px Inter'`, `'16px "Helvetica Neue"'`, etc.
8. **Font string matches CSS** — The `font` parameter uses canvas format: `'700 italic 24px "Helvetica Neue"'`. Mismatch = silent height errors.
9. **Cursor handoff is explicit** — When flowing text across regions with `layoutNextLine()`, always pass `line.end` as the next call's `start`.
10. **prepare() is opaque** — Don't read internals of `PreparedText`. If you need segment data, use `prepareWithSegments()` which returns `PreparedTextWithSegments`.

## Rendering targets

Pretext computes geometry. It does not render. Your target decides the API:

| Target | API | Render |
|---|---|---|
| DOM (set height) | `layout()` | `el.style.height = height + 'px'` |
| DOM (position lines) | `layoutWithLines()` | Absolute-position `<div>` per line |
| Canvas 2D | `layoutWithLines()` / `layoutNextLine()` | `ctx.fillText(line.text, x, y)` |
| SVG | `layoutWithLines()` | `<text x y>` per line |
| Geometry only | `walkLineRanges()` | No render — aggregate widths/counts |

## Working in the Pretext repo

If editing the library itself (not consuming it):

```
bun start              # dev server, port 3000
bun run check          # typecheck + lint
bun test               # invariant tests
bun run accuracy-check # browser sweep (Chrome)
bun run benchmark-check
```

Read the project `CLAUDE.md` for architecture, corpus commands, and engine constraints.
