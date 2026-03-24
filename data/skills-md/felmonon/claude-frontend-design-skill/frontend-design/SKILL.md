---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use when building web components, pages, dashboards, or applications. Avoids generic AI aesthetics through aesthetic archetype commitment, token-based constraints, and iterative refinement.
---

# Frontend Design

This skill produces distinctive, professional frontend interfaces that avoid generic "AI slop" aesthetics through structured design methodology.

## Before Coding (Required)

Commit to a BOLD aesthetic direction. Answer these questions before any implementation:

1. **Purpose**: What problem does this interface solve?
2. **Audience**: Who uses this? What are their expectations?
3. **Archetype**: Select ONE from [references/archetypes/](references/archetypes/)
4. **Differentiation**: What makes this UNFORGETTABLE?
5. **Anti-goals**: What must this NOT look like?

## Aesthetic Archetypes

Select one archetype and apply its complete design system. See [references/archetypes/](references/archetypes/) for full specifications.

| Archetype | Signature Elements | Best For |
|-----------|-------------------|----------|
| **Editorial** | Dramatic type hierarchy, asymmetric layouts, reading-focused | Publishing, portfolios, long-form content |
| **Swiss** | Grid-based, systematic spacing, clean sans-serif typography | Corporate, data-heavy applications |
| **Brutalist** | Raw elements, system fonts, visible structure, anti-decoration | Statement sites, creative agencies |
| **Minimalist** | Generous whitespace, limited palette, essential elements only | Luxury brands, photography |
| **Maximalist** | Dense information, layered visuals, intentional complexity | E-commerce, entertainment, gaming |
| **Retro-Futuristic** | Neon accents, gradient meshes, tech-noir atmosphere | Tech products, innovation showcases |
| **Organic** | Fluid shapes, natural colors, soft corners, flowing motion | Wellness, sustainability, lifestyle |
| **Industrial** | Monospace type, exposed grid, mechanical precision | Dev tools, technical documentation |
| **Art Deco** | Geometric patterns, gold accents, symmetrical elegance | Hospitality, fashion, events |
| **Lo-Fi** | Hand-drawn elements, paper textures, imperfect warmth | Creative tools, personal projects |

## Typography Rules

### NEVER Use These Overused Fonts
- Inter
- Roboto
- Arial
- Open Sans
- system-ui (as default stack)
- Helvetica Neue
- Lato

### ALWAYS Use Distinctive Typography
- Source quality fonts from Google Fonts, Adobe Fonts, or commercial foundries
- Create contrast: Pair serif headings with sans-serif body, or vice versa
- Use extreme weight contrasts: 300 body + 800 headings, not 400 + 600

### Recommended Distinctive Pairings
```
Headlines          Body Text           Use Case
─────────────────────────────────────────────────
Space Grotesk      Source Serif Pro    Tech + editorial blend
DM Sans            Fraunces            Modern + classic
Outfit             Crimson Pro         Clean + literary
Playfair Display   Karla               Elegant + approachable
Sora               Literata            Geometric + readable
JetBrains Mono     Inter               Dev tools ONLY
Clash Display      Satoshi             Bold + contemporary
```

See [references/typography.md](references/typography.md) for complete guidelines.

## Color Philosophy

### Reject These Clichés
- Purple/indigo gradients on white
- Blue as the only accent color
- Gray text on gray backgrounds
- Rainbow gradients
- Neon on dark (unless Retro-Futuristic archetype)

### Apply the 60-30-10 Rule
- **60%**: Dominant surface color (often neutral)
- **30%**: Secondary color for structure and hierarchy
- **10%**: Accent color for CTAs and emphasis ONLY

### Color Principles
- One primary accent color maximum
- Ensure 4.5:1 minimum contrast for text (WCAG AA)
- Consider color meaning (red = danger, green = success)
- Dark mode is not "invert colors" — it's a separate palette

## Token System (Required)

All values MUST reference design tokens. See [references/tokens.md](references/tokens.md).

### Never Hardcode Values
```css
/* WRONG */
color: #3b82f6;
padding: 16px;
font-size: 14px;
border-radius: 8px;
```

### Always Use Tokens
```css
/* CORRECT */
color: var(--color-interactive-primary);
padding: var(--space-4);
font-size: var(--font-size-sm);
border-radius: var(--radius-md);
```

### Token Layers
1. **Option tokens**: Raw values (--color-blue-500, --space-4)
2. **Decision tokens**: Semantic application (--color-interactive-primary)
3. **Component tokens**: Scoped to elements (--button-padding-x)

## Implementation Pipeline

Follow this exact sequence:

### Step 1: Design Brief
Copy and complete:
```markdown
## Design Brief
- **Purpose**: [What problem does this solve?]
- **Audience**: [Who uses this?]
- **Archetype**: [Selected archetype]
- **Differentiation**: [What makes it memorable?]
- **Anti-goals**: [What must it NOT be?]
```

### Step 2: Visual Specification
Define WITHOUT writing code:
```markdown
## Visual Specification
### Layout
- Container: [max-width, padding]
- Grid: [columns, gutters]
- Sections: [spacing rhythm]

### Color Application
- Surface: [token] at [coverage]%
- Accent: [token] at 10% max
- Text: [tokens for hierarchy]

### Typography
- Display: [font, size token, weight]
- Body: [font, size token, line-height]
- UI: [font for buttons/labels]
```

### Step 3: Component Implementation
Generate code following:
- The selected archetype's specific patterns
- Token references for ALL values
- Mobile-first responsive approach
- Complete interaction states

### Step 4: Self-Review
Evaluate against this checklist before presenting:

```markdown
## Quality Checklist
- [ ] Follows selected archetype consistently
- [ ] Uses tokens exclusively (no hardcoded values)
- [ ] Typography is distinctive (not generic fonts)
- [ ] Color follows 60-30-10 rule
- [ ] Contrast ratios meet WCAG AA (4.5:1 text, 3:1 UI)
- [ ] Responsive across mobile (375px) / tablet (768px) / desktop (1200px+)
- [ ] Includes hover / focus / active states
- [ ] Focus indicators visible for keyboard navigation
- [ ] Touch targets minimum 44x44px
- [ ] Loading / error / empty states defined
- [ ] Has meaningful motion (not just opacity fades)
```

If ANY check fails, revise before presenting final code.

## Interaction States (Required)

Every interactive element needs:

```css
.interactive-element {
  /* Default state */
  background: var(--color-interactive-primary);
  transition: all 0.2s ease-out;
}

.interactive-element:hover {
  /* Hover: visual feedback */
  background: var(--color-interactive-hover);
  transform: translateY(-1px);
}

.interactive-element:focus-visible {
  /* Focus: keyboard navigation indicator */
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
}

.interactive-element:active {
  /* Active: pressed state */
  background: var(--color-interactive-active);
  transform: translateY(0);
}

.interactive-element:disabled {
  /* Disabled: reduced prominence */
  opacity: 0.5;
  cursor: not-allowed;
}
```

## Animation Guidelines

### Meaningful Motion Only
- Entrance: Elements should feel like they're arriving naturally
- Feedback: Interactions confirm user actions
- Hierarchy: Motion guides attention to important changes

### Timing Tokens
```css
:root {
  --duration-instant: 100ms;   /* Micro-interactions */
  --duration-fast: 200ms;      /* Hover, focus */
  --duration-normal: 300ms;    /* Transitions */
  --duration-slow: 500ms;      /* Page transitions */

  --ease-out: cubic-bezier(0.0, 0.0, 0.2, 1);
  --ease-in-out: cubic-bezier(0.4, 0.0, 0.2, 1);
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

### Anti-Patterns
- Generic fade-in only animations
- Bounce effects on everything
- Animation delays longer than 100ms
- Motion that blocks interaction

## Responsive Strategy

### Breakpoint Tokens
```css
:root {
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
}
```

### Mobile-First Approach
```css
/* Base: Mobile (< 640px) */
.component { /* mobile styles */ }

/* Tablet (>= 768px) */
@media (min-width: 768px) {
  .component { /* tablet overrides */ }
}

/* Desktop (>= 1024px) */
@media (min-width: 1024px) {
  .component { /* desktop overrides */ }
}
```

## Anti-Patterns

See [references/anti-patterns.md](references/anti-patterns.md) for the complete list.

### Critical Violations (Automatic Revision Required)
- Generic font stacks (Inter, Roboto, system fonts)
- Indigo/purple as primary accent
- Minimal or no animations
- Symmetrical "template" layouts
- Missing loading/error/empty states
- Small touch targets (< 44px)
- No focus indicators
- Hardcoded color/spacing values

## Examples

- Good implementations: [examples/good-examples.md](examples/good-examples.md)
- What to avoid: [examples/bad-examples.md](examples/bad-examples.md)

## Critic Review Protocol

For complex interfaces, perform explicit review:

```markdown
## Design Review

### Archetype Consistency
Does every element match [selected archetype]?
- Typography: [pass/fail + notes]
- Color: [pass/fail + notes]
- Spacing: [pass/fail + notes]
- Motion: [pass/fail + notes]

### Technical Quality
- Token usage: [% of values using tokens]
- Responsive: [tested breakpoints]
- Accessibility: [WCAG checks passed]

### Distinctiveness Test
- Would a designer recognize this as professional? [yes/no]
- Is this memorable? [yes/no]
- Does it look like a template? [yes/no]

### Required Revisions
1. [Specific issue and fix]
2. [Specific issue and fix]
```

## Figma Integration

When converting Figma designs using the Figma MCP:

1. Extract design context using `get_design_context` tool
2. Map Figma variables to skill token system
3. Identify closest archetype match
4. Generate code maintaining design intent

### Token Mapping
```
Figma Variable Type    →    CSS Token
─────────────────────────────────────
Color primitive        →    --color-[name]-[shade]
Color semantic         →    --color-[context]-[variant]
Spacing                →    --space-[scale]
Typography             →    --font-[property]-[size]
Border radius          →    --radius-[size]
Shadow                 →    --shadow-[level]
```

### Font Substitution Rule
If Figma uses generic fonts (Inter, Roboto, etc.), REPLACE with distinctive alternatives that maintain the same visual weight and character.
