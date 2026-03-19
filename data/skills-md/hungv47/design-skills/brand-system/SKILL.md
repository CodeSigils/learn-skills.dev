---
name: brand-system
description: "This skill should be invoked when the user wants to build or define a brand identity, visual system, or design system. Triggers include 'create a brand', 'I need brand guidelines', 'logo', 'color palette', 'typography', 'fonts', 'style guide', 'visual identity', 'rebrand', 'design tokens', 'we look like every other startup', 'our design feels inconsistent', or 'what should my brand look like' -- even if they just say 'we look unprofessional', 'we don't have consistent design', or 'our product doesn't feel premium.' Not for writing marketing copy (use content-create) or mapping user flows (use user-flow)."
license: MIT
metadata:
  author: hungv47
  version: "4.0.1"
---

# Brand Identity & Design System Generator

*Design — Step 1 of 2. Transform product artifacts into a complete brand identity and design system.*

**Core Question:** "Does every visual decision trace back to who we are?"

## Inputs Required
- Product description or PRD (what the product does, who it serves)
- Target audience profile (demographics, psychographics, context of use)
- Competitive context (who else serves this audience, how they're positioned)

## Output
- `.agents/design/brand-system.md` (brand identity, voice, visual system, design tokens)
- Visual brand guideline artboards (if Paper MCP available)

## Quality Gate
Before delivering, verify:
- [ ] Every visual, verbal, and token decision traces back to strategy and archetype
- [ ] Values have real tradeoffs (not generic "innovation, quality, integrity")
- [ ] Voice chart has Do/Don't examples for every attribute
- [ ] All semantic tokens have both light and dark mode values
- [ ] Every token pair meets WCAG AA contrast (4.5:1 normal text, 3:1 large/UI)
- [ ] Background/foreground convention used consistently (`bg-primary text-primary-foreground`)
- [ ] One global `--radius` value — all components derive from it
- [ ] Cross-element coherence: radius maps to archetype (see `references/token-templates.md`), type personality matches archetype (see `references/typography-psychology.md`), color emotion aligns with brand personality (see `references/color-emotion.md`), and imagery direction reflects the archetype's visual world. Flag any element that contradicts the others.
- [ ] AI slop check: run `references/ai-slop-detection.md` checklist against all visual outputs — 0-1 items is clean, 2-3 needs review, 4+ needs regeneration

## Chain Position
Previous: none | Next: `user-flow`

**Re-run triggers:** After major product pivots, when entering new markets, after significant audience shifts, or annually for brand refresh.

**Related skills (non-chain):** `icp-research` (audience data for brand strategy), `content-create` (consumes voice guidelines), `humanize` (uses voice adjectives)

---

## Before Starting

### Step 0: Gather Context

**Required inputs** — interview if missing:
- Product description or PRD
- Target audience profile
- Competitive context

**Strongly recommended:**
- Existing brand assets (logos, colors, fonts, past guidelines)
- Founder/team values and origin story
- Key differentiators

**Helpful:**
- Admired brands (aspirational and anti-aspirational)
- Market positioning intent (premium, accessible, disruptive, trusted)

### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `.agents/product-context.md` | icp-research (from `hungv47/comms-skills`) | Product positioning, audience, and voice adjectives — grounds brand strategy in audience research |
| `.agents/mkt/icp-research.md` | icp-research (from `hungv47/comms-skills`) | Audience personas, pain profiles, and VoC quotes — brand strategy without audience research produces generic archetypes |

**Strongly recommended:** Run `icp-research` (from comms-skills) first if audience research hasn't been done. Brand strategy built on assumed audiences produces generic, untested archetypes.

If upstream artifacts' `date` fields are older than 30 days, recommend re-running `icp-research` before proceeding — audience insights evolve and stale data produces misaligned brand strategy.

### Mode Selection

| Mode | When | Scope |
|------|------|-------|
| **Full Brand System** | Established product, full rebrand, comprehensive guidelines needed | All 13 steps (Parts I + II) |
| **Quick Brand** | MVP, early-stage, need to ship fast with basic brand foundations | Steps 1-7 only (through Step 7: Messaging Architecture) — defers visual identity, tokens, and components |

Ask: *"Full brand system or quick brand for MVP?"*

**Quick Brand** covers: Purpose/mission/vision, core values, positioning, archetype, personality, voice/tone, messaging architecture. Defers: visual identity, token architecture, component tokens, accessibility/dark mode, and Paper artboards. Quick Brand output includes a note: "Run full brand-system when ready to build the design system."

Missing product details are not guessable — interview for them.

---

# Part I: Brand Identity

## Step 1: Brand Strategy Foundation

Define the bedrock everything else builds on.

### Purpose, Mission, Vision

```
PURPOSE (why we exist — beyond money): [One sentence]
MISSION (what we do, for whom, how): [1-2 sentences, present-tense, action-oriented]
VISION (future state we're building toward): [One sentence, aspirational but believable]
```

### Core Values

3-5 values. Each specific enough to guide real decisions. **Test**: if the opposite is obviously stupid, the value is too generic. Good values have a real tradeoff ("transparency over comfort").

```
1. [Value]: [What it means in practice — a specific behavioral standard]
2. [Value]: [What it means in practice]
3. [Value]: [What it means in practice]
```

### Brand Positioning

```
POSITIONING: For [target audience], [brand] is the only [category] that [difference] because [proof].
PROMISE: [One sentence — single most important commitment to customers]
VALUE PROP: We help [who] do [what] by [how], so they can [outcome].
```

### Competitive Landscape

```
PERCEPTUAL MAP:
  Axis 1: [e.g., Affordable ←→ Premium]
  Axis 2: [e.g., Traditional ←→ Innovative]
  Our position: [where and why]
  White space: [opportunity this position exploits]

KEY COMPETITORS:
  - [Competitor A]: [position]. Weakness: [gap we exploit].
  - [Competitor B]: [position]. Weakness: [gap we exploit].
```

---

## Step 2: Brand Personality & Archetype

Select one primary (70%) and one secondary (30%) archetype from the 12 Jungian archetypes. Reference `references/brand-archetypes.md` for the complete guide.

```
Primary (70%): [Archetype] — [why it fits core desire and strategy]
Secondary (30%): [Archetype] — [nuance it adds]

In action: How we inspire / communicate / make people feel / what we'd never do
```

### Personality Traits

3-5 traits using "trait, but not" format to prevent misinterpretation:

```
1. [Trait] — but not [extreme to avoid]. In practice: [example]
2. [Trait] — but not [extreme]. In practice: [example]
3. [Trait] — but not [extreme]. In practice: [example]
```

### Emotional Journey Map

```
Before product: [emotional state]  →  During: [transformation]  →  After: [desired outcome]
CORE TENSION: [problem/desire resolved]
DESIGN PROMISE: [what the entire brand experience communicates]
```

---

## Step 3: Brand Voice & Tone

Voice is constant (personality in words). Tone is variable (shifts by context). Reference `references/brand-voice.md` for frameworks.

### Voice Chart

3-5 attributes with Do/Don't examples:

```
| Attribute | Description | Do | Don't |
|-----------|-------------|-----|-------|
| [Attr]    | [Meaning]   | [Right example] | [Wrong example] |
```

### Tone Spectrum

Map across NN/g dimensions, then specify tone by context (marketing, product UI, help docs, errors, social).

### On-Brand vs Off-Brand Examples

Provide side-by-side examples for: welcome email, error message, CTA button.

---

## Step 4: Messaging Architecture

```
TAGLINE (2-7 words): [memorable, ownable, evocative]
ELEVATOR PITCH (25 words): [what, for whom, why it matters]
VALUE PROPOSITION (1-2 sentences): [functional + emotional benefits]

MESSAGING PILLARS (3-5):
  Pillar N: [Headline] → Narrative (2-3 sentences) → Proof points

BOILERPLATE: One-liner (10w) | Short (50w) | Standard (100w) | Full (200w)
```

---

## Step 5: Visual Identity System

Every visual decision traces to archetype, personality, and positioning. Reference `references/visual-identity.md` for detailed logo, imagery, and iconography rules.

### Logo System
Primary lockup, secondary, logomark, wordmark. Define clear space, minimum size, color variations, usage rules.

### Color System
Colors serve the emotional journey and archetype. Reference `references/color-emotion.md` for color psychology. Provide values in all formats: Hex, OKLCH, Pantone, CMYK, RGB.

```
PRIMARY (60%): [Name] [hex] [oklch] — emotional purpose traced to archetype
SECONDARY (30%): [Name] [values] — supporting role
ACCENT (10%): [Name] [values] — CTAs, highlights, celebration
SEMANTIC: Success / Warning / Error / Info
NEUTRALS: Full 50-950 scale
```

### Typography System
Select fonts embodying archetype and personality. Reference `references/typography-psychology.md`. Maximum 2 families (3 if mono needed). Define full type hierarchy (H1 through caption).

### Imagery & Iconography
Photography mood, lighting, color treatment, subjects, composition. Icon style (line/filled/duotone), stroke weight, grid, color rules. Brand devices (patterns, shapes, textures).

---

# Part II: Design System

## Step 6: Token Architecture

Three-layer system (W3C Design Tokens spec, shadcn/ui-inspired):

```
PRIMITIVE (what exists)   →  color.blue.500, spacing.4, font.size.md
SEMANTIC (what it means)  →  --primary, --muted-foreground, --border
COMPONENT (where it goes) →  button.primary.background, input.border.default
```

**Background/foreground convention**: Every semantic role comes as a pair. Base name = background/fill. `-foreground` suffix = text/icon on that surface. Pair them: `bg-primary text-primary-foreground`.

**Color format**: OKLCH primary, hex fallbacks.

Reference `references/token-architecture.md` for the complete spec and `references/token-templates.md` for primitive scales, semantic token map, radius-to-archetype mapping, and a full mapping example.

---

## Step 7: Component Tokens & Patterns

Map semantic tokens to specific components. Reference `references/component-tokens.md` for full component token map (buttons, inputs, cards, badges), button hierarchy with sizes, form element specs, card specs, and motion/interaction tokens.

Reference `references/component-patterns.md` for extended UI component patterns with token consumption maps.

Key principles:
- One primary button per view maximum
- Buttons: 6 variants (primary, secondary, destructive, outline, ghost, link)
- Inputs: validate on blur, not keystroke
- Motion: instant/fast/normal/slow timing scale, ease-out for entering, ease-in for exiting

---

## Step 8: Accessibility & Dark Mode

Reference `references/implementation-rules.md` for full accessibility baseline (WCAG 2.1 AA), dark mode rules, and brand application templates.

Key requirements:
- **Contrast**: 4.5:1 normal text, 3:1 large text and UI components
- **Targets**: 44x44px minimum touch targets, 8px spacing between
- **Focus**: Visible ring on all interactive elements — never remove without replacement
- **Color independence**: Pair color with icons, labels, patterns, or position
- **Motion safety**: Respect `prefers-reduced-motion`
- **Dark mode**: Parallel track from Step 1. Reduce saturation and shift lightness — avoid inverting. Surface hierarchy, not just "black."

---

## Step 9: Visual Artboard Generation (Paper MCP)

Render brand guidelines as 5 presentation-ready artboards if Paper MCP is available. Reference `references/artboard-generation.md` for complete specs, workflow, and prerequisites.

After generating artboards, run the AI slop detection checklist (`references/ai-slop-detection.md`). Artboards are the highest-risk output for AI default patterns because they're visual-first and the agent may lean on familiar layouts instead of archetype-driven decisions.

Artboards: Color Palette | Typography System | Spacing & Tokens | UI Style Principles | Logo System

Skip this step if Paper MCP tools are unavailable.

---

## Process Summary

1. **Gather** — product docs, audience, competitors, existing assets
2. **Strategy** — purpose, mission, vision, values, positioning
3. **Archetype** — primary + secondary, rationale traced to strategy
4. **Personality** — 3-5 traits in "trait, but not" format
5. **Voice** — voice chart, tone spectrum, writing guidelines
6. **Messaging** — tagline through boilerplate, pillars with proof
7. **Visual identity** — logo, colors, type, imagery, icons
8. **Primitives** — neutral base, color scales (OKLCH), type, spacing, radius
9. **Semantic tokens** — map primitives to UI roles using bg/fg pairs
10. **Components** — token consumption maps, button/input/card specs
11. **Accessibility + dark mode** — WCAG AA, parallel dark track
12. **Applications** — brand across touchpoints
13. **Artboards** — render in Paper MCP (if available), screenshot and refine

---

## Artifact Template

Save to `.agents/design/brand-system.md`.

On re-run: rename existing artifact to `brand-system.v[N].md` and create new with incremented version.

```markdown
---
skill: brand-system
version: 1
date: {{today}}
status: draft
---

# Brand System: [Brand Name]

## Part I: Strategy
- Purpose, positioning, competitive landscape

## Part II: Personality
- Primary archetype, voice framework, messaging examples

## Part III: Visual Identity
- Logo, color palette (OKLCH + hex), typography, imagery direction

## Part IV: Design Tokens
- Primitive scales, semantic map, component tokens (see references/)

## Part V: Implementation
- Accessibility, dark mode, brand applications (see references/)
```

---

## Worked Example (Condensed)

**Input**: FinLit — a personal finance app for young professionals (22-30), positioned against intimidating banking apps.

**Strategy**: Purpose: make finance empowering, not shameful. Positioning: the only finance app that feels like a supportive friend, not a stern banker.

**Archetype**: Caregiver (70%) + Explorer (30%). Warm, supportive core with curiosity and growth.

**Voice**: Encouraging but not patronizing. "You've got this" energy. Casual-leaning, never jargon-heavy.

**Visual**: Primary: warm teal (`oklch(0.65 0.15 180)` / `#2cbaa0`). Neutral base: Stone (warm gray). Display: Plus Jakarta Sans. Body: Inter. Radius: 0.5rem (friendly, Caregiver). Imagery: real people, natural light, warm tones.

**Tokens**: `--primary: stone.50/stone.950` (light/dark bg). `--primary: teal.600/teal.400`. `--radius: 0.5rem`. All pairs verified 4.5:1+.

---

## References

- `references/brand-archetypes.md` — 12 Jungian archetypes with visual and verbal mappings
- `references/brand-voice.md` — Voice frameworks, tone dimensions, messaging architecture
- `references/visual-identity.md` — Logo systems, imagery direction, iconography, graphic elements
- `references/token-architecture.md` — Three-layer token system, semantic token map, neutral presets
- `references/token-templates.md` — Primitive scales, semantic token map, radius-archetype mapping, mapping example
- `references/component-tokens.md` — Component token map, button/input/card specs, motion tokens
- `references/implementation-rules.md` — Accessibility baseline, dark mode rules, brand applications
- `references/artboard-generation.md` — Paper MCP artboard specs and workflow
- `references/typography-psychology.md` — Font personality mappings and pairing rules
- `references/color-emotion.md` — Color psychology, OKLCH values, audience palettes
- `references/component-patterns.md` — Extended UI component patterns with token consumption maps
- `references/paper-artboard-templates.md` — Paper MCP HTML/CSS templates
- `references/ai-slop-detection.md` — AI-generated design anti-patterns checklist

## Anti-Patterns

### Brand
- **Aesthetics without strategy** — picking colors or fonts because they "look nice" without tracing back to archetype and positioning. Every visual choice needs a strategy justification.
- **Visual-first thinking** — choosing colors/fonts before strategy makes the brand feel hollow
- **Generic values** — "innovation, quality, integrity" have no tradeoff; they guide nothing
- **Archetype confusion** — commit to one primary; the secondary adds nuance, not contradiction
- **Voice without examples** — "we're friendly" is meaningless without a concrete error message example

### Design System
- **Token soup** — ~20 semantic tokens cover an entire component library; more creates decision paralysis
- **Skipping semantic layer** — components reference semantic tokens, not primitives directly
- **Mismatched pairs** — `bg-primary text-primary` is wrong; use `bg-primary text-primary-foreground`
- **Hex-only thinking** — use OKLCH for perceptually uniform manipulation; hex for readability
- **Dark mode as inversion** — requires deliberate surface hierarchy, not black/white flip

### Visual Artboards
- **Batching entire artboards** — one visual group per `write_html` call
- **Using grid/margins/tables** — Paper is flex-only; use `display: flex`, `gap`, `padding`
- **Unchecked fonts** — call `get_font_family_info` before using any font family
- **Skipping screenshots** — `get_screenshot` every 2-3 `write_html` calls
- **Artboards before markdown** — Parts I-III are source of truth; artboards visualize them
