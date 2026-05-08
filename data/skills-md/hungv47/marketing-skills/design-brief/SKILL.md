---
name: design-brief
description: "Produces graphic-design briefs for individual visual assets — social posts (IG carousel/post/story, LinkedIn doc/single, FB ad), thumbnails (YouTube, X card), banners/display ads, OOH/billboard, OG/share cards, hero illustrations. Pulls brand-system tokens, generates concept directions, and writes a per-asset brief with platform-aware specs (aspect ratio, safe zones, type scale, contrast, file format, anti-patterns) plus an image-gen prompt or designer-handoff spec. Produces `.agents/mkt/design-briefs/[slug].md`. Does NOT render the asset — rendering happens downstream via image-gen tool, vector tool, or human designer. Not for brand identity definition (use brand-system) or whole-page redesigns (use lp-brief). Not for writing the copy that goes IN the asset (use copywriting)."
argument-hint: "[asset description, e.g. 'instagram carousel about pricing tiers']"
allowed-tools: Read Edit Grep Glob Bash WebSearch WebFetch
license: MIT
metadata:
  author: hungv47
  version: "2.0.0"
  budget: standard
  estimated-cost: "$1-2"
  status: done_with_concerns
  notes: "Re-scoped from design-create (brief-only, no rendering). Platform-aware module content for IG/LinkedIn/FB/YT/X/OOH/banner is skeleton-only — needs a follow-up build pass with practitioner-grade specs (aspect ratios, safe zones, mobile type scales, thumb-stop contrast, file conventions, anti-patterns) per platform."
promptSignals:
  phrases:
    - "design brief"
    - "graphic brief"
    - "asset brief"
    - "create graphic"
    - "design asset"
    - "social graphic"
    - "ad creative"
    - "og image"
    - "hero image"
    - "banner design"
    - "carousel design"
    - "thumbnail"
    - "illustration brief"
  allOf:
    - [design, brief]
    - [graphic, brief]
    - [asset, brief]
    - [create, graphic]
    - [generate, image]
  anyOf:
    - "graphic"
    - "illustration"
    - "carousel"
    - "banner"
    - "thumbnail"
    - "midjourney"
    - "imagen"
    - "dall-e"
    - "claude design"
    - "figma"
    - "ad creative"
  noneOf:
    - "brand identity"
    - "design system"
    - "design tokens"
    - "user flow"
    - "wireframe"
    - "landing page redesign"
  minScore: 6
routing:
  intent-tags:
    - graphic-design-brief
    - visual-asset-brief
    - ad-creative-brief
    - social-graphic-brief
    - og-image-brief
    - thumbnail-brief
    - generative-prompt
  position: pipeline
  produces:
    - mkt/design-briefs/[slug].md
  consumes:
    - brand/BRAND.md
    - brand/DESIGN.md
    - brand/ASSETS.md
    - mkt/lp-brief/[slug]/asset-slots/*.md
  requires:
    - brand/BRAND.md
    - brand/DESIGN.md
  defers-to:
    - skill: brand-system
      when: "need to define brand identity, logo, palette, or full design system"
    - skill: copywriting
      when: "need craft-quality headline / CTA copy that goes IN the asset"
    - skill: lp-brief
      when: "redesigning a whole page, not a single asset"
  parallel-with: []
  interactive: true
  estimated-complexity: medium
---

# Design Brief — Orchestrator

*Communication — visual layer. Produces a graphic-design brief for a single visual asset; rendering is downstream.*

**Core Question:** "Could a designer or image-gen tool execute this asset on-brand and on-platform without follow-up questions?"

## Critical Gates — Read First

- **Do NOT render.** This skill produces the brief, not the asset. The brief carries spec + reference direction + image-gen prompt (where applicable). Rendering happens downstream — image-gen (Midjourney / Imagen / DALL·E / Claude Design), vector tooling (Pencil / Figma), or a human designer.
- **Do NOT proceed without brand anchors.** Missing `brand/BRAND.md` or `brand/DESIGN.md` → return `NEEDS_CONTEXT`, recommend running `brand-system` first.
- **Do NOT invent tokens, fonts, or motion specs.** Every visual decision traces to DESIGN.md. If DESIGN.md doesn't cover what's needed (e.g. illustration style), flag it in the brief — don't guess.
- **Do NOT use stock-AI defaults.** No default purple-blue gradients, centered-isolated-on-white, faux-3D bevels, or glassmorphism unless DESIGN.md specifies. Critic scores generic-AI smell explicitly.
- **Do NOT skip the brief approval gate.** The brief is a candidate, not a delivery — user reviews before downstream rendering.
- **Platform spec is mandatory.** Every brief includes aspect ratio, safe zones, mobile readability (type scale, thumb-stop contrast), file format, and file-size limits. See `references/platform-modules.md`.

## Philosophy

A great brief eliminates downstream ambiguity. Render quality is bounded by brief quality — a vague brief produces drift no matter how good the renderer. The brief is the deliverable; every visual decision binds to a brand anchor and a platform constraint.

Brand fidelity > aesthetic novelty. Platform fitness > generic polish. A boring on-brand brief beats a striking off-brand one.

## Inputs Required

- **Asset request** — type (IG carousel, OG image, banner ad), platform/format, purpose (announce/educate/convert/recruit), copy if available
- **`brand/BRAND.md`** — voice, archetype, sacred elements
- **`brand/DESIGN.md`** — palette, typography, surface language, motion (if applicable)

## Inputs Optional

- **`brand/ASSETS.md`** — pre-fills format/dimensions if asset matches a row; ticks box on completion
- **`.agents/mkt/lp-brief/[slug]/asset-slots/[slot-id].md`** — slot spec when brief is for a landing-page asset
- **`.agents/mkt/content/[slug].copy.md`** — copy used IN the asset (headline, body, CTA)
- **`.agents/mkt/campaign-plan.md`** — campaign context, channel placement, awareness stage

## Output

`.agents/mkt/design-briefs/[slug].md` containing:
- Approved concept (visual direction, references)
- Brand anchors (palette/typography/sacred elements from DESIGN.md)
- Platform spec (aspect ratio, safe zones, type scale, contrast, format, size cap)
- Asset slots (compound assets — e.g. carousel slides)
- Copy placement (when copy lives in the asset)
- Failure modes (platform-specific + generic-AI)
- Downstream handoff: image-gen prompt OR designer spec OR vector-tool spec
- Critic report (rubric + generic-AI-aesthetic check)

## Quality Gate

Before delivering, the **critic agent** verifies:
- [ ] Brand fidelity — palette, typography, motion all trace to DESIGN.md
- [ ] Sacred elements respected (no proposed change to logo, primary palette anchor, tagline, etc. unless brief explicitly authorizes)
- [ ] Hierarchy — clear focal point, scannable in 1 second
- [ ] Composition — balance, intentional white space
- [ ] Typography — pairing/sizing/leading consistent with DESIGN.md
- [ ] Contrast — text passes WCAG AA (≥4.5:1 normal, ≥3:1 large) on its actual background
- [ ] **Platform fit** — dimensions, safe zones, platform crop behavior, mobile thumb-stop readability, file format, file-size cap all verified against the asset's platform module
- [ ] CTA clarity (if applicable) — readable at preview size, action verb visible
- [ ] **Generic-AI-aesthetic check — full 13-pattern detector from `references/visual-rubric.md` §"Generic-AI-Aesthetic Detector". Score 0-3 per pattern (max 39). Thresholds: 0-7 clean / 8-15 DONE_WITH_CONCERNS / 16+ auto-FAIL.**
- [ ] Downstream-handoff completeness — image-gen prompt is specific (lens / lighting / mood / era / composition / color cast), or designer spec covers placement/typography/color tokens, or vector-tool spec specifies layout grid

## Chain Position

Previous: `brand-system` (required), `lp-brief` (optional — slot spec), `copywriting` (optional — copy) | Next: external rendering (image-gen / Pencil / Figma / human designer)

**Re-run triggers:** BRAND.md or DESIGN.md updates, new asset row in ASSETS.md, lp-brief slot needs an explicit per-asset brief, campaign launch.

### Skill Deference

- **No brand system?** → run `brand-system` first; design-brief hard-blocks without it.
- **Need in-asset copy?** → run `copywriting` first or in parallel.
- **Whole-page redesign?** → use `lp-brief`.

---

## Agent Manifest

| Agent | Layer | File | Focus |
|-------|-------|------|-------|
| Brand-Anchor Agent | 1 (parallel) | `agents/brand-anchor-agent.md` | Pulls relevant tokens, sacred elements, lexicon, motion spec from BRAND.md + DESIGN.md |
| Concept Agent | 1 (parallel) | `agents/concept-agent.md` | Generates 3 distinct concept directions (mood, composition, references) |
| Copy-Anchor Agent | 1 (parallel) | `agents/copy-anchor-agent.md` | Resolves copy that appears IN the asset (from copywriting artifact, or interview the user) |
| Brief Synthesizer | 1.5 (after L1) | `agents/brief-synth-agent.md` | Merges anchor + 3 concepts + copy into 3 candidate briefs with platform spec, hierarchy, asset slots |
| Prompt-Craft Agent | 2 (downstream-route: `image-gen` / `template-pack`) | `agents/prompt-craft-agent.md` | Produces image-gen prompts (Claude Design / Midjourney / Imagen / DALL·E / Veo / Suno) for the chosen brief |
| Figma-Spec Agent | 2 (downstream-route: `designer-handoff`) | `agents/figma-spec-agent.md` | Produces design spec markdown for human designer in Figma |
| Critic Agent | 3 (final) | `agents/critic-agent.md` | Visual rubric scoring + generic-AI-aesthetic detection + platform-fit check |

---

## Routing Logic

Every brief carries a **downstream-route** tag identifying its renderer. The tag drives which optional sub-agent runs after the brief is approved.

### Downstream routes

| Route | When | Optional Layer 2 agent | Output addition |
|-------|------|------------------------|------------------|
| `image-gen` | Photographic, illustrative, abstract, or compositionally complex. Hero/OG/blog illustrations, ad backgrounds, video thumbnails. | `prompt-craft-agent` | Image-gen prompt + 2 variants |
| `vector-tool` | Vector layouts, UI mockups, branded social templates, multi-format variants, infographics. Pencil/Figma execution. | (none — brief carries vector-tool spec block) | Layout grid spec + token references |
| `designer-handoff` | Executed by human designer in Figma or print shop. Print-grade, OOH, complex composition. | `figma-spec-agent` | Designer-file spec |
| `template-pack` | Multi-format social packs (IG + LinkedIn + X variants of one asset). | `prompt-craft-agent` per format | Per-format prompts in one brief |

Override auto-detection with `--route=image-gen|vector-tool|designer-handoff|template-pack`.

### Auto-detection (asset type → default downstream route)

| Asset Type | Default Route | Why |
|-----------|--------------|-----|
| OG image / blog hero / ad photo | image-gen | Generative gives photo/illustration diversity |
| Instagram carousel (typographic) | vector-tool | Vector + multi-slide layout |
| Instagram carousel (image-led) | image-gen (per slide) | Generate slides, assemble |
| Instagram post / story | image-gen or vector-tool | Depends on photo vs typographic |
| LinkedIn document post | vector-tool | Multi-slide typographic |
| LinkedIn single-image | image-gen or vector-tool | Depends on photo vs typographic |
| FB / display banner (text-heavy) | vector-tool | Vector text + crop variants |
| FB / display banner (visual-led) | image-gen | Generate visual, overlay text |
| YouTube thumbnail | image-gen | Photo-based + bold text overlay |
| X/Twitter card | image-gen or vector-tool | Depends on photo vs typographic |
| OOH / billboard / print | designer-handoff | Print-grade, needs human designer |
| Email hero | image-gen or vector-tool | Depends on photo vs typographic |
| Hero illustration (custom) | image-gen or designer-handoff | Generative or human-designer |
| Spot icon / decoration | vector-tool | Vector |

---

## Pre-Dispatch

This skill is **hard-gated** on brand artifacts. Cold-start questioning happens after the gate. Full Pre-Dispatch protocol pattern: `meta-skills/references/pre-dispatch-protocol.md`.

### Hard gate (before any questioning)

`brand/BRAND.md` AND `brand/DESIGN.md` must be present. If either missing → return **NEEDS_CONTEXT**, recommend `brand-system` (Route A for BRAND only, Route B for full design tokens). If either >60 days stale and user hasn't confirmed, warn before proceeding.

If `brand/ASSETS.md` exists, scan for a row matching the requested asset. If found, pre-fill format/dimensions/path and prepare to tick the checkbox on completion.

### Needed dimensions
- Asset type (OG image / IG carousel / banner / hero / OOH / etc.)
- Downstream route (image-gen / vector-tool / designer-handoff / template-pack — drives Layer 2)
- Brand reference (resolved by hard gate to `brand/DESIGN.md`)
- Copy/headline if any (to render IN the asset)
- Constraints (dimensions, deadline, must-include elements)

### Read order (post-gate)
1. Pipeline: `brand/BRAND.md`, `brand/DESIGN.md` (confirmed by hard gate). `brand/ASSETS.md` for dimension pre-fill. `.agents/mkt/lp-brief/[slug]/asset-slots/[slot-id].md` if invoked from lp-brief. `.agents/mkt/content/[slug].copy.md` if copy supplied separately. `.agents/mkt/campaign-plan.md` for campaign context. `research/icp-research.md` for audience visual preferences.
2. Experience: `.agents/experience/{brand,goals}.md`.

### Optional Artifacts (read if present)

| Artifact | Source | Benefit |
|----------|--------|---------|
| `brand/ASSETS.md` | brand-system Route B | Auto-fill dimensions, tick checkbox on completion |
| `.agents/mkt/lp-brief/[slug]/asset-slots/[slot-id].md` | lp-brief | Slot spec when brief is for an LP asset |
| `.agents/mkt/content/[slug].copy.md` | copywriting | Copy to use in the asset |
| `.agents/mkt/campaign-plan.md` | campaign-plan | Campaign context, awareness stage |
| `research/icp-research.md` | icp-research | Audience visual preferences |

**Warm Start** (invoked from lp-brief or campaign-plan with asset spec):

```
Hard gate passed: brand/BRAND.md + brand/DESIGN.md present.
Found:
- asset spec → "[from upstream slot or campaign-plan]"
- copy → "[from copywriting if present]"
- ASSETS.md row → "[matched / no match]"

Auto-detecting downstream route from asset type. Override or proceed?
```

**Cold Start** (standalone invocation, asset request from user):

```
design-brief produces a per-asset brief that downstream renderers (Claude
Design / Pencil MCP / Figma / human designer) execute. Before I dispatch:

1. **Asset type** — what's being designed? (OG image / IG carousel / IG post /
   IG story / LinkedIn document / LinkedIn single-image / FB ad / YouTube
   thumbnail / X card / OOH / banner / hero / other.)
2. **Downstream route** — image-gen (generative for photos/illustrations) /
   vector-tool (Pencil/Figma for layouts and variants) / designer-handoff
   (human designer for print or complex composition) / template-pack
   (multi-format social packs from one brief). Auto-detected from asset
   type by default — override here.
3. **Copy/headline** — what text appears IN the asset? Headline, body,
   CTA, brand mark text. Reference `.agents/mkt/content/[slug].copy.md`
   if supplied separately.
4. **Constraints** — dimensions (if non-standard), deadline, must-include
   elements (logo placement, brand mark, legal disclaimer, etc.).

Answer 1-4 in one response. (Brand reference is auto-resolved from
brand/BRAND.md + brand/DESIGN.md.) I'll dispatch.
```

**Write-back:**

| Q | File | Key |
|---|---|---|
| 4. Constraints (durable: legal disclaimer policies, logo placement rules) | `brand.md` | `Brand — design constraints` (only if user expresses durable rule) |
| 1, 2, 3. Asset-specific dimensions | (per-asset, lives in design-brief artifact) |

---

## Step 0.5: Route Detection (Orchestrator)

Before Layer 1, pick a downstream route AND (for `image-gen`) a target generative tool. Both are required by downstream sub-agents.

1. **`--route=` override** → honor it. Warn if asset-type default differs.
2. **Else** walk the asset-type → default route table above.
3. **State route + rationale in 1 line** before dispatching:
   > "Downstream route: image-gen (photographic OG image). Target tool: midjourney-v6 (editorial mood). Override with `--route=` if needed."
4. **For `image-gen`**, pick `target_tool` from `references/prompt-patterns.md` "tool → asset type" table (e.g., `claude-design`, `midjourney-v6`, `imagen-3`, `dall-e-3`, `ideogram`, `veo`, `suno`).
5. **Pull the platform module** from `references/platform-modules.md` and pass its spec checklist (aspect, safe zones, type scale, contrast, format, size cap, anti-patterns) to brief-synth-agent and critic-agent.

`route`, `target_tool`, and `platform_module` are part of every agent's context.

---

## Layer 1: Parallel Foundation

Spawn **IN PARALLEL**; outputs feed Layer 1.5:

| Agent | Instruction File | Pass These Inputs | Reference Files |
|-------|-----------------|-------------------|-----------------|
| Brand-Anchor Agent | `agents/brand-anchor-agent.md` | full BRAND.md + DESIGN.md + asset request | — |
| Concept Agent | `agents/concept-agent.md` | asset request + brand digest | `references/asset-types.md`, `references/platform-modules.md`, `references/failure-modes.md` |
| Copy-Anchor Agent | `agents/copy-anchor-agent.md` | asset request + copywriting artifact (if any) + brand voice rules | — |

---

## Layer 1.5: Brief Synthesis

| Agent | Instruction File | Pass These Inputs | Reference Files |
|-------|-----------------|-------------------|-----------------|
| Brief Synthesizer | `agents/brief-synth-agent.md` | brand anchor + 3 concepts + copy + route + platform module + asset request | `references/asset-types.md`, `references/platform-modules.md` |

Output: 3 candidate briefs, each with concept name, visual direction, hierarchy, platform spec (resolved against the module), copy placement, failure modes to avoid.

---

## Approval Gate 1 — Brief Selection

**STOP and present** the 3 candidate briefs. Do not proceed to image-gen prompt or designer spec.

Format:

```
## Brief Candidates

### A. [Concept Name]
[Visual direction, mood, references — 3-5 lines]
**Why this:** [argument]
**Risk:** [main concern]

### B. [Concept Name]
...

### C. [Concept Name]
...

**Pick one (A/B/C), request revisions, or specify your own direction.**
```

User responses:
- **"A" / "B" / "C"** → proceed with that brief to Layer 2.
- **"Revise X"** → re-dispatch concept-agent with feedback, regenerate, re-present.
- **"None of these"** → ask one clarifying question, regenerate.
- **"Switch route to X"** → re-dispatch brief-synth with the new route. If concept-agent's tool-feasibility for that concept was RETHINK on the new route, re-run concept-agent first.
- **"Stop"** → save as `.agents/mkt/design-briefs/[slug]-candidates.md`, exit BLOCKED.

---

## Layer 2: Downstream Handoff Augmentation

Dispatch ONE based on downstream route:

| Route | Agent | Output addition |
|-------|-------|--------|
| `image-gen` | `agents/prompt-craft-agent.md` | Image-gen prompt block (primary + 2 variants) appended to brief |
| `vector-tool` | (none — brief synth already wrote the vector spec block) | — |
| `designer-handoff` | `agents/figma-spec-agent.md` | Designer-handoff spec block appended to brief |
| `template-pack` | `agents/prompt-craft-agent.md` per format | Per-format prompt blocks |

---

## Layer 3: Critic Gate

| Agent | Instruction File | Receives |
|-------|-----------------|----------|
| Critic Agent | `agents/critic-agent.md` | Approved brief + Layer 2 output + platform module |

Critic produces an inline rubric report with PASS / FAIL.

- **PASS** → Approval Gate 2.
- **FAIL** → re-dispatch the relevant Layer 2 agent or brief-synth with feedback. Max 2 rewrite cycles; after 2 failures, deliver with critic annotations as DONE_WITH_CONCERNS.

---

## Approval Gate 2 — Brief Acceptance

**STOP and present** the assembled brief + critic report.

Format:

```
## [Asset Name] — Design Brief — [Downstream route]

**Concept:** [name selected at Gate 1]
**Critic:** [PASS / DONE_WITH_CONCERNS]
**Score:** [/40 with sub-scores]

[Brief preview — concept, anchors, platform spec, copy placement, failure modes, handoff block]

[Critic notes — concerns to monitor]

**Approve to write artifact, revise, or reject.**
```

User responses:
- **"Approve"** →
  1. Write `.agents/mkt/design-briefs/[slug].md`.
  2. **ASSETS.md auto-tick:** if the brief's asset path is a literal string match for a `brand/ASSETS.md` row's path field (never auto-tick on slug or asset-type heuristic), flip `[ ]` → `[x]` and append a date stamp. No match → skip; design-brief doesn't own ASSETS.md row creation (that's brand-system).
  3. Status DONE.
- **"Revise X"** → re-dispatch brief-synth or Layer 2 agent with feedback (1 cycle), re-present.
- **"Reject"** → save as `.agents/mkt/design-briefs/[slug]-rejected.md` with a `Rejection Notes` block, exit BLOCKED.

---

## Artifact Template — `.agents/mkt/design-briefs/[slug].md`

```markdown
---
skill: design-brief
version: 1
date: [today]
status: [done | done_with_concerns | blocked | needs_context]
downstream_route: [image-gen | vector-tool | designer-handoff | template-pack]
target_tool: [claude-design | midjourney-v6 | imagen-3 | dall-e-3 | ideogram | pencil | figma | print | ...]
asset_type: [og-image | ig-carousel | ig-post | ig-story | li-doc | li-single | fb-ad | yt-thumbnail | x-card | ooh | banner | ...]
platform: [instagram | linkedin | facebook | youtube | x | print | web | email | ...]
dimensions: [WxH or per-format list]
brand_anchors:
  primary_color: [hex]
  primary_type: [font, weight]
  motion: [duration token if applicable]
sacred_respected: [list of sacred elements honored]
---

# Design Brief: [Asset Name]

**Asset:** [type + platform]
**Purpose:** [announce | educate | convert | recruit | brand-build]
**Source copy:** [path or "none"]
**Downstream route:** [image-gen / vector-tool / designer-handoff / template-pack]

## Concept (Approved)

**Name:** [concept name]
**Visual direction:** [3-5 lines — mood, composition, palette emphasis, type role, motion if applicable]
**References:** [3 reference URLs or named brands/artworks IF applicable — never copy, only direction]

## Brand Anchors

- **Palette pull:** [3-5 hex values from DESIGN.md, with token name]
- **Typography:** [primary + secondary from DESIGN.md, sizes for this asset]
- **Sacred elements respected:** [list — what was preserved]
- **Lexicon:** [forbidden phrases avoided, preferred phrases used if copy is in asset]

## Platform Spec

| Field | Value | Source (platform module) |
|-------|-------|--------------------------|
| Aspect ratio | [X:Y] | [platform module name] |
| Dimensions | [WxH px] | [platform module] |
| Safe zone | [px from edges, platform-specific] | [platform module] |
| Type scale (mobile readability floor) | [min px at 1x] | [platform module] |
| Contrast (thumb-stop) | [WCAG ratio min for the asset's smallest text on its actual background] | platform module |
| File format | [PNG / SVG / WebP / MP4 / ...] | [platform module] |
| File-size cap | [KB/MB] | [platform module] |
| Color mode | [sRGB / DCI-P3 / CMYK] | [platform module] |
| Anti-patterns flagged | [list specific to this platform] | [platform module] |

## Hierarchy

1. **Focal point:** [what the eye lands on first]
2. **Supporting:** [secondary element]
3. **Tertiary:** [text body, fine detail]

## Asset Slots (compound assets only — e.g., carousel)

| Slot | Dimensions | Format | Fallback |
|------|-----------|--------|----------|
| [Slide 1] | [WxH] | [PNG] | [...] |
| [Slide 2] | [WxH] | [PNG] | [...] |

## Copy Placement (if any)

- **Headline:** "[exact copy]" — [position, type token]
- **Body:** "[exact copy]" — [position, type token]
- **CTA:** "[exact copy]" — [position, type token, contrast pair]

## Failure Modes to Avoid

- [Platform-specific traps — from platform module]
- [Generic-AI smell — from failure-modes.md]
- [Brand drift — from brand_anchors]

## What NOT to Do

- [Sacred elements: do not propose changing X, Y, Z]
- [Off-brand defaults to reject]

## Downstream Handoff Block

### When `downstream_route: image-gen`
- **Primary prompt** ([target_tool]): [full prompt with lens / lighting / mood / era / composition / color cast / aspect-ratio flag]
- **Variant 1:** [specific deviation]
- **Variant 2:** [specific deviation]
- **Post-processing note:** [overlay copy, logo placement, export profile]

### When `downstream_route: vector-tool`
- **Layout grid:** [columns × rows, gutters, baseline]
- **Component references:** [DESIGN.md tokens used]
- **Multi-format crops** (if applicable): [per-format dimensions and reflow rules]

### When `downstream_route: designer-handoff`
- **Spec sheet** for the designer (Figma file or print shop): [section list, type scale, palette, asset bundle paths]
- **Open questions for designer:** [decisions deferred to designer judgment]

### When `downstream_route: template-pack`
- **Per-format prompt blocks:** [one per platform variant]

## Critic Report

[rubric scores, PASS / FAIL, concerns to monitor]
```

> On re-run with same slug: rename existing artifact to `[slug].v[N].md` and create new with incremented version. Preserves history for A/B comparison.

---

## Anti-Patterns

**Skipping the brief approval gate** — Going straight to image-gen burns credits or designer time on a misaligned concept. INSTEAD: 3 briefs, user picks one, then handoff.

**Inventing tokens** — Using a color or font not in DESIGN.md because it "fits the mood." INSTEAD: If DESIGN.md is incomplete for this asset's needs, flag it in the brief and ask the user — either expand DESIGN.md (re-run brand-system) or accept the limitation.

**Stock-AI defaults** — Default purple-blue gradient, centered isolated subject on white, glassmorphism, faux-3D bevels. INSTEAD: Critic-agent's generic-AI rubric explicitly catches these. If a concept relies on them, score it down before delivering.

**Generic-photo prompts** — "Modern office, professional, 4k, hyperrealistic." Looks like every other AI-stock-photo. INSTEAD: Specific lens, lighting, mood, era, composition, color cast.

**Ignoring safe zones** — Designing edge-to-edge for Instagram and losing CTA to the crop. INSTEAD: Platform module defines safe zones — concept must fit them.

**Treating the brief as a render** — Writing a fluffy concept paragraph and calling it done. The brief must be specific enough that a downstream tool/designer can execute without follow-up.

**Treating Claude Design output as brand-system input** — claude.ai/design generates exploration. It's a starting point downstream of this brief, not a brand commitment.

---

## Completion Status Protocol

Per project standard, every run ends with explicit status:

- **DONE** — brief approved, critic PASS, artifact written
- **DONE_WITH_CONCERNS** — approved but critic flagged issues; concerns documented in artifact frontmatter. **Currently the skill itself ships in this state until platform-modules.md is fully populated.**
- **BLOCKED** — user rejected at a gate, or external dependency missing
- **NEEDS_CONTEXT** — BRAND.md or DESIGN.md missing; cannot proceed without brand-system

---

## Agent Files

### Sub-Agent Instructions (agents/)

- [agents/brand-anchor-agent.md](agents/brand-anchor-agent.md) — Token + sacred element pull
- [agents/concept-agent.md](agents/concept-agent.md) — 3 concept directions
- [agents/copy-anchor-agent.md](agents/copy-anchor-agent.md) — In-asset copy resolution
- [agents/brief-synth-agent.md](agents/brief-synth-agent.md) — 3 candidate briefs
- [agents/prompt-craft-agent.md](agents/prompt-craft-agent.md) — Image-gen prompts
- [agents/figma-spec-agent.md](agents/figma-spec-agent.md) — Designer handoff spec
- [agents/critic-agent.md](agents/critic-agent.md) — Visual rubric + AI-aesthetic + platform-fit check

### Shared References (references/)

- [references/asset-types.md](references/asset-types.md) — Per-asset format specs
- [references/platform-modules.md](references/platform-modules.md) — Per-platform brief checklists (skeleton — needs follow-up build pass)
- [references/prompt-patterns.md](references/prompt-patterns.md) — Image-gen prompt structures
- [references/visual-rubric.md](references/visual-rubric.md) — Critic scoring dimensions
- [references/failure-modes.md](references/failure-modes.md) — Generic-AI catalog, brand drift
- [references/examples.md](references/examples.md) — End-to-end worked examples
