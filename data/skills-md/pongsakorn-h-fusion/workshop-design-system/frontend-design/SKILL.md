---
name: frontend-design
description: "Create production-ready HTML/CSS layouts, banners, and visual compositions at exact pixel dimensions. Handles responsive markup, safe-zone compliance, brand injection, and cross-platform sizing. Actions: create, build, layout, compose HTML/CSS. Outputs: self-contained HTML files ready for screenshot export."
argument-hint: "[component] [width]x[height]"
license: MIT
metadata:
  author: claudekit
  version: "1.0.0"
---

# Frontend Design

Create pixel-perfect HTML/CSS compositions for banners, social images, and visual assets.

## When to Activate

- Banner or social image HTML/CSS creation
- Precise pixel-dimension layouts (e.g., 820x312, 1200x630)
- Composing text, CTA, and logo overlays on visual backgrounds
- Building self-contained HTML files for screenshot export

## Workflow

### Step 1: Receive Specifications

From the calling skill (usually `banner-design` or `design`):
- **Dimensions** — exact width × height in pixels
- **Content** — headline, subtext, CTA text, logo
- **Brand tokens** — colors, fonts, spacing (from `brand` or `design-system` skill)
- **Style direction** — minimalist, photo-based, gradient, etc.

### Step 2: Build HTML/CSS

Create a single self-contained HTML file:

```html
<!doctype html>
<html lang="th">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width={WIDTH}, initial-scale=1.0" />
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    html, body {
      width: {WIDTH}px;
      height: {HEIGHT}px;
      overflow: hidden;
    }
    .canvas {
      width: {WIDTH}px;
      height: {HEIGHT}px;
      position: relative;
    }
  </style>
</head>
<body>
  <main class="canvas">
    <!-- Content layers -->
  </main>
</body>
</html>
```

### Step 3: Apply Design Rules

- **Safe zones** — critical content within central 70-80%
- **Typography** — max 2 fonts, min 16px body, ≥32px headline
- **CTA** — single CTA, min 44px touch target, action verb
- **Contrast** — 4.5:1 minimum text-to-background ratio
- **Self-contained** — inline all CSS, embed fonts via Google Fonts CDN
- **No scrolling** — everything fits in one viewport

### Step 4: Brand Injection

If brand guidelines exist (`docs/brand-guidelines.md`):

```sh
node .github/skills/brand/scripts/inject-brand-context.cjs
```

Run from the repository root. The Node command works in Windows PowerShell, macOS, and Linux.

Apply extracted colors, fonts, and voice to the composition.

## Output Convention

```
{output-dir}/
├── {style}-{width}x{height}.html
└── ...
```

- kebab-case filenames
- Dimensions in filename for traceability
- One HTML file per variant

## Integration

**Called by:** banner-design, design (social photos)
**Works with:** brand (tokens), design-system (CSS vars), chrome-devtools (export)
