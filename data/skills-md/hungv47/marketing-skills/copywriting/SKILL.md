---
name: copywriting
description: "Writes and evaluates persuasive copy — headlines, hooks, CTAs, taglines, and full-page section copy with rubric scoring, annotations, and ranked alternatives. Produces inline annotations or `.agents/mkt/content/[slug].copy.md`. Not for editing AI-sounding text (use humanize). For brand voice guidelines, see brand-system. For landing page conversion audits, see lp-optimization."
argument-hint: "[copy task or text to evaluate]"
allowed-tools: Read Grep Glob Bash WebSearch WebFetch
license: MIT
metadata:
  author: hungv47
  version: "2.0.0"
  budget: deep
  estimated-cost: "$1-3"
promptSignals:
  phrases:
    - "write copy"
    - "headline"
    - "tagline"
    - "call to action"
    - "write a headline"
    - "hook line"
    - "write a cta"
  allOf:
    - [write, copy]
    - [craft, headline]
  anyOf:
    - "headline"
    - "cta"
    - "tagline"
    - "hook"
    - "persuasive"
    - "ad copy"
    - "long-form copy"
  noneOf:
    - "social media post"
    - "blog post"
    - "email campaign"
    - "carousel"
  minScore: 6
routing:
  intent-tags:
    - write-copy
    - evaluate-copy
    - headline
    - cta
    - tagline
    - landing-page-copy
  position: horizontal
  produces:
    - mkt/content/[slug].copy.md
  consumes:
    - product-context.md
    - icp-research.md
    - mkt/campaign-plan.md
  requires: []
  defers-to:
    - skill: humanize
      when: "AI-sounding text needs cleanup"
    - skill: lp-optimization
      when: "diagnosing a live page's conversion problem"
    - skill: seo
      when: "optimizing for search/AI citations"
  parallel-with: []
  interactive: false
  estimated-complexity: heavy
---

# Copywriting — Orchestrator

*Communication — Horizontal. Coordinates specialized sub-agents to produce craft-quality copy with annotations, alternatives, and quantitative evaluation.*

**Core Question:** "Is every key line visual, falsifiable, and uniquely ours?"

## Philosophy

Copy frameworks (PAS, 3-Question Test, CTA formula) are proven tools — not mandatory templates. A skilled agent may combine frameworks or break a guideline when the extra words earn their place. The test is: does this stop the scroll and move the reader? This orchestrator dispatches specialist agents for each concern, then a critic agent ensures every key line meets the bar.

## Inputs Required
- Brief: what to write (headline, hook, CTA, tagline, subject line, or full-page copy)
- Context: audience, product, awareness stage (from `research/icp-research.md`, `research/product-context.md`, or user-provided)

## Output
- Inline annotations + alternatives on key lines (when called by another skill)
- `.agents/mkt/content/[slug].copy.md` (for standalone full-page copy tasks)

## Quality Gate
Before delivering, the **critic agent** verifies:
- [ ] Every key line passes the Three-Question Test: visual? falsifiable? uniquely ours?
- [ ] Rubric score averages ≥3.5 across V/F/U for all key lines
- [ ] Every key line passes the Competitor Swap Test (swap in competitor name — if it still works, rewrite)
- [ ] 3-5 variations generated per key line, best selected with top 2-3 presented as alternatives
- [ ] Every key line annotated: rule that drove the choice, cut alternative, rubric score
- [ ] CTA follows formula: [action verb] + [what they get] (not "Learn More" or "Click Here")
- [ ] Every headline/hook contains concrete nouns or specific numbers (no abstract "better," "innovative," "leading")

## Chain Position
Horizontal — called by `lp-optimization`, `campaign-plan`, `lp-brief`. Can run standalone.
**Re-run triggers:** When brand voice changes, when A/B test results suggest a different angle, or when key lines need fresh variations.

### Skill Deference
- **Content reads as AI-generated?** → Run `humanize` after
- **Diagnosing a live page's conversion problem?** → Use `lp-optimization`
- **Optimizing for search/AI citations?** → Coordinate with `seo`

---

## Agent Manifest

| Agent | Layer | File | Focus |
|-------|-------|------|-------|
| Hook Agent | 1 (parallel) | `agents/hook-agent.md` | Headlines, hooks, taglines, subject lines — 3-5 variations with 3Q scoring |
| Body Agent | 1 (parallel) | `agents/body-agent.md` | Problem, Solution, How It Works sections |
| CTA Agent | 1 (parallel) | `agents/cta-agent.md` | CTA variations per placement with risk reversal |
| Social Proof Agent | 1 (parallel) | `agents/social-proof-agent.md` | Testimonials, stats, logos, credibility signals |
| Variant Agent | 1.5 (post-merge) | `agents/variant-agent.md` | A/B alternatives for key sections |
| Voice Agent | 2 (sequential) | `agents/voice-agent.md` | Clarity + brand voice consistency, AI slop removal |
| Psychology Agent | 2 (sequential) | `agents/psychology-agent.md` | So What, Prove It, Specificity, Emotion passes |
| Zero-Risk Agent | 2 (sequential) | `agents/zero-risk-agent.md` | Barrier removal, guarantees, exit grace |
| Critic Agent | 2 (final) | `agents/critic-agent.md` | Rubric scoring, 3Q test, annotation, PASS/FAIL |

---

## Routing Logic

Classify the task, then follow the matching route.

### Route A: Single Key Line
**When:** Brief asks for a headline, hook, CTA, tagline, or subject line — not a full page.

```
1. Pre-dispatch: Gather context (Step 0 below)
2. Dispatch ONE agent:
   - Hook/headline/tagline/subject line → hook-agent
   - CTA → cta-agent
3. Dispatch: critic-agent (on the single agent's output)
4. If critic returns FAIL → re-dispatch the original agent with feedback (max 2 cycles)
5. Deliver annotated key lines
```

**Note:** Route A skips variant-agent. Hook-agent and cta-agent already generate 3-5 variations internally with rubric scoring. Variant-agent is designed for full-page copy where cross-section A/B alternatives are needed.

### Route B: Full-Page Copy
**When:** Brief asks for landing page copy, full-page copy, or multiple sections.

```
1. Pre-dispatch: Gather context (Step 0 below)
2. LAYER 1 — Dispatch IN PARALLEL:
   - hook-agent
   - body-agent
   - cta-agent
   - social-proof-agent
3. MERGE: Assemble Layer 1 outputs into page structure
4. Dispatch: variant-agent (on merged output)
5. LAYER 2 — Dispatch SEQUENTIALLY:
   - voice-agent (receives merged + varianted output)
   - psychology-agent (receives voice-agent output)
   - zero-risk-agent (receives psychology-agent output)
6. Dispatch: critic-agent (receives zero-risk-agent output)
7. If critic returns FAIL → re-dispatch named agent(s) with feedback (max 2 cycles)
8. Deliver final artifact
```

### Route C: Called by Another Skill
**When:** Invoked by `lp-optimization`, `campaign-plan`, or `lp-brief` for inline copy work.

```
1. Pre-dispatch: Read context from calling skill's artifacts
2. Dispatch the relevant Layer 1 agent(s) based on what the caller needs:
   - Headline/hook → hook-agent
   - Body sections → body-agent
   - CTAs → cta-agent
   - Social proof → social-proof-agent
3. Dispatch: critic-agent
4. Return annotated output to the calling skill
```

---

## Pre-Dispatch

Run the Pre-Dispatch protocol (`meta-skills/references/pre-dispatch-protocol.md`).

**Needed dimensions:** surface (page / email / social / headline / CTA / etc.), audience, the one shift (what should reader believe after?), unique proof (what can you say nobody else can?), traffic source (if applicable).

**Read order:**
1. Pipeline: `research/icp-research.md` for VoC + pain language. `research/product-context.md` for product details and voice adjectives. `.agents/mkt/campaign-plan.md` for angle + awareness stage.
2. Experience: `.agents/experience/{audience,product,goals}.md`.

If `research/icp-research.md` or `product-context.md` `date` fields >30 days old, warn and recommend re-running `icp-research`. Soft gate — proceed if user confirms, note "stale ICP" in artifact header.

**Language:** default English. If another language specified, note in pre-writing — agent instructions are optimized for English copy; other languages may need adapted idioms and cultural references.

**Warm Start** (icp-research + product-context + campaign-plan exist):

```
Found:
- audience → "[VoC summary from icp-research.md]"
- product/voice → "[adjectives from product-context.md]"
- campaign angle → "[from campaign-plan.md if present]"

Need before dispatching: surface (page/email/headline/CTA/etc.) + the
one shift this copy should produce.
```

**Cold Start** (no upstream artifacts):

```
copywriting writes for a specific surface, a specific audience, with a
specific shift in mind. Generic prompts produce generic copy. Before I dispatch:

1. **Surface** — landing page (full) / homepage section / email / social post
   / headline only / CTA only / tagline / subject line / other?
2. **Audience** — primary buyer (role + situation + 1-2 pains they articulate).
   Or point me at `research/icp-research.md` if it exists.
3. **The one shift** — what should the reader believe after reading this
   that they don't believe now? One sentence.
4. **Unique proof** — what can you say that nobody else can? Specific
   client + number, named feature with results, or domain credentials.
5. **Traffic source** (only if Q1 is page or email) — ad / search / email /
   social / direct? Determines what the reader already knows and expects.

Answer 1-5 (or 1-4 if no traffic source) in one response. I'll dispatch.
```

**Write-back:**

| Q | File | Key |
|---|---|---|
| 2. Audience | `audience.md` | `Audience — primary persona` (only if novel; pre-existing icp-research takes precedence) |
| 3. The one shift | `goals.md` | `Goals — copy shift: [surface]` |
| 4. Unique proof | `product.md` | `Product — proof points` |
| 1, 5. Surface + traffic source | (routing only) |

---

## Dispatch Protocol

### How to spawn a sub-agent

For each agent dispatched below, use the **Agent tool** with a prompt constructed as follows:

1. **Read** the agent instruction file (e.g., `agents/hook-agent.md`) — include its FULL content in the Agent prompt
2. **Append** the brief and pre-writing context after the instructions
3. **Resolve file paths to absolute**: replace relative paths with absolute paths rooted at this skill's directory. Example: if this skill is at `/Users/you/skills/copywriting/`, then `references/headline-formulas.md` becomes `/Users/you/skills/copywriting/references/headline-formulas.md`. Tell the agent: "Read the reference file at [absolute path] for domain knowledge."
4. **Pass upstream artifacts by content, not path**: the orchestrator reads `research/product-context.md` and `research/icp-research.md` FIRST, then includes relevant excerpts (VoC quotes, voice adjectives, pain language) in the pre-writing object. Sub-agents should NOT read artifact files directly — the orchestrator curates what they need.
5. If **feedback** exists (from a critic FAIL cycle), append it at the end of the prompt with the header "## Critic Feedback — Address Every Point"

### Single-agent fallback

If multi-agent dispatch is unavailable (no Agent tool, single-agent runtime, or context constraints), execute each agent's instructions sequentially in-context:
- Layer 1: run each agent's domain instructions one at a time, writing each section
- Layer 2: apply each refinement pass to the full document in order
- Critic: self-evaluate using the critic-agent's rubric and quality gate

The output quality should be equivalent — the multi-agent pattern optimizes for parallelism and focus, not capability.

---

## Layer 1: Parallel Section Writers

Spawn the following agents **IN PARALLEL** (multiple Agent tool calls in a single message). For each agent, follow the Dispatch Protocol above.

| Agent | Instruction File | Pass These Inputs | Reference Files to Resolve |
|-------|-----------------|-------------------|---------------------------|
| Hook Agent | `agents/hook-agent.md` | brief + pre-writing | `references/headline-formulas.md` |
| Body Agent | `agents/body-agent.md` | brief + pre-writing | `references/page-sections.md` |
| CTA Agent | `agents/cta-agent.md` | brief + pre-writing | — |
| Social Proof Agent | `agents/social-proof-agent.md` | brief + pre-writing + available proof points | `references/page-sections.md` |

**For single key line tasks (Route A):** Dispatch only the relevant agent, not all four.

---

## Merge Step

After all Layer 1 agents return, assemble their outputs into the page structure.

### Section Order (full-page copy)
1. **Hero** — Hook agent's recommended headline + subheadline + CTA agent's hero CTA
2. **Social Proof Bar** — Social proof agent's bar element
3. **Problem** — Body agent's Problem section
4. **Solution** — Body agent's Solution section
5. **How It Works** — Body agent's How It Works section
6. **Testimonials** — Social proof agent's testimonials
7. **Key Stats** — Social proof agent's stats (if applicable)
8. **Final CTA** — CTA agent's final CTA + risk reversal

### Assembly Rules
The merge is deterministic assembly, not creative synthesis. Slot each agent's output into the template by ownership:

| Section | Owner Agent | Content Source |
|---------|-----------|---------------|
| Headline + Subheadline | Hook Agent | Recommended hook + subheadline from hook-agent output |
| Hero CTA | CTA Agent | Hero CTA from cta-agent output |
| Social Proof Bar | Social Proof Agent | Bar element from social-proof-agent output |
| Problem | Body Agent | Problem section from body-agent output |
| Solution | Body Agent | Solution section from body-agent output |
| How It Works | Body Agent | How It Works section from body-agent output |
| Testimonials | Social Proof Agent | Testimonials from social-proof-agent output |
| Mid-Page CTA | CTA Agent | Mid-page CTA from cta-agent output |
| Key Stats | Social Proof Agent | Stats from social-proof-agent output |
| Final CTA + Risk Reversal | CTA Agent | Final CTA + risk reversal from cta-agent output |

### Conflict Resolution
- Each agent owns specific sections (table above). If two agents mention the same fact (e.g., both hook and social-proof reference "12,000 users"), keep the version from the section owner.
- If hook-agent's headline contradicts body-agent's problem framing, the orchestrator adjusts the body to align with the hook — the hook is the anchor because it's what the reader sees first.

### After Merge: Variant Agent
Dispatch the **variant-agent** with the assembled document as `upstream`. It returns A/B alternatives for key sections. Variant alternatives are appended to the artifact (not replacing originals) — they're testable options, not replacements.

---

## Layer 2: Sequential Craft Refiners

Dispatch these agents **ONE AT A TIME, IN ORDER** using the Dispatch Protocol above. Each receives the previous agent's full output as the `upstream` field.

```
voice-agent → psychology-agent → zero-risk-agent → critic-agent
```

| Step | Agent | Instruction File | Receives |
|------|-------|-----------------|----------|
| 1 | Voice Agent | `agents/voice-agent.md` | Merged + varianted document |
| 2 | Psychology Agent | `agents/psychology-agent.md` | Voice agent's output |
| 3 | Zero-Risk Agent | `agents/zero-risk-agent.md` | Psychology agent's output |
| 4 | Critic Agent | `agents/critic-agent.md` | Zero-risk agent's output |

Each agent returns the full document with their edits applied + a change log.

---

## Critic Gate

The critic agent returns one of two verdicts:

### PASS
The copy meets all quality standards. Deliver the critic's annotated output as the final artifact.

### FAIL
The critic returns specific failures with:
- Which lines failed and on which dimension
- Specific fix instructions
- Which agent to re-dispatch

**Rewrite loop:**
1. Read the critic's failure report
2. Re-dispatch ONLY the named agent(s) with the critic's feedback attached as the `feedback` input
3. Run the modified output back through the critic
4. **Maximum 2 rewrite cycles.** After 2 failures, deliver the copy with the critic's annotations and flag to the user: "Copy scored [X] — manual review recommended on [specific lines]."

---

## Artifact Template

```markdown
---
skill: copywriting
version: 1
date: [today's date]
status: done | done_with_concerns | blocked | needs_context
---

# Copy: [Title / Brief Description]

**Date:** [today]
**Skill:** copywriting
**Audience:** [who]
**Awareness Stage:** [stage]
**Traffic Source:** [where they're coming from]

## Pre-Writing

1. **Talking to:** [audience + current belief]
2. **Shift to:** [desired belief after reading]
3. **Only we can say:** [unique proof/angle]
4. **Traffic context:** [what they already know]

## Key Lines

### [Line Type: Headline / Hook / CTA / Tagline / Subject Line]

**Selected:** "[winning line]"
  Rule: [which principle]. Score: V:[n] F:[n] U:[n].
  Cut alternative: "[runner-up]" — [why cut].

**Alternative A:** "[second option]"
  Rule: [principle]. Score: V:[n] F:[n] U:[n].

**Alternative B:** "[third option]"
  Rule: [principle]. Score: V:[n] F:[n] U:[n].

## [Additional sections for full-page copy — Hero, Problem, Solution, etc.]

## A/B Variants
[Variant agent's alternatives with hypotheses and test priority]

> On re-run: rename existing artifact to `[slug].copy.v[N].md` and create new with incremented version.
```

## Next Step

Run `humanize` to refine voice and compress. Run `lp-optimization` if this copy is for a landing page.

---

## Worked Example — Full-Page Copy (Route B)

**Brief:** Landing page for StatusZero, a tool that replaces standups with async status updates.
**Audience:** Engineering managers at 50-200 person companies, problem aware.
**Traffic:** LinkedIn ads (cold).

### Step 0: Pre-Dispatch
1. Talking to: EMs who feel buried in status overhead but think it's part of managing.
2. Shift to: Status updates are a solvable problem, not a cost of doing business.
3. Only we can say: Internal data shows 12 hrs/week lost to status theater.
4. Traffic: LinkedIn ad click — cold, haven't searched, hook must interrupt.

### Layer 1: Parallel Dispatch
→ **Hook agent** returns 5 headline variations, recommends: "Your team loses 12 hours a week to status updates nobody reads." (V:5 F:5 U:4)
→ **Body agent** returns Problem (status theater pain), Solution (async updates), How It Works (3 steps)
→ **CTA agent** returns hero CTA ("See how teams ship without status theater →"), mid-page, and final CTAs with risk reversal
→ **Social proof agent** returns logo bar (4 tech companies), 2 testimonials with metrics, key stat

### Merge (orchestrator assembles)
Slots Layer 1 outputs into template: Hero → Social Proof Bar → Problem → Solution → How It Works → Testimonials → Final CTA

### Dispatch: Variant Agent
Receives merged document. Returns A/B alternatives:
→ Hero variant B: "I cut meetings 80%. Output doubled." (tests story hook vs. data hook)
→ Final CTA variant B: "Try StatusZero free — no credit card, cancel anytime" (tests specificity vs. risk-first)

### Layer 2: Sequential Dispatch
→ **Voice agent** receives merged + varianted doc. Fixes 3 AI patterns, adjusts tone to "direct, technical." Returns modified doc + change log.
→ **Psychology agent** receives voice output. Adds "which means..." bridges to 2 features, strengthens emotion in problem section. Returns modified doc + change log.
→ **Zero-risk agent** receives psychology output. Adds "No credit card required" near hero CTA, "Cancel anytime" near final CTA. Returns modified doc + change log.

### Dispatch: Critic Agent → PASS
Receives zero-risk output. Scores all key lines. All average ≥3.5. Annotated and delivered.

---

## Agent Files

### Sub-Agent Instructions (agents/)
- [agents/hook-agent.md](agents/hook-agent.md) — Headlines, hooks, 3Q scoring, formulas
- [agents/body-agent.md](agents/body-agent.md) — Problem, Solution, How It Works sections
- [agents/cta-agent.md](agents/cta-agent.md) — CTA formula, risk reversal, placement
- [agents/social-proof-agent.md](agents/social-proof-agent.md) — Testimonials, stats, credibility
- [agents/variant-agent.md](agents/variant-agent.md) — A/B alternatives, rubric scoring
- [agents/voice-agent.md](agents/voice-agent.md) — Clarity, voice consistency, AI slop removal
- [agents/psychology-agent.md](agents/psychology-agent.md) — So What, Prove It, Specificity, Emotion
- [agents/zero-risk-agent.md](agents/zero-risk-agent.md) — Barrier removal, guarantees, exit grace
- [agents/critic-agent.md](agents/critic-agent.md) — Final evaluation, scoring, PASS/FAIL
- [agents/_template.md](agents/_template.md) — Reusable template for creating new agent files

### Shared References (references/)
- [references/headline-formulas.md](references/headline-formulas.md) — Headline formula catalog (hook-agent)
- [references/page-sections.md](references/page-sections.md) — Page section types, templates, testimonial selection (body-agent, social-proof-agent)

### Page-Specific Guidance

| Page | Key Principle |
|------|--------------|
| **Homepage** | What you do in one sentence. Primary use case, not every feature. |
| **Landing Page** | One goal, one CTA. Match headline to traffic source. Remove nav. |
| **Pricing** | Lead with value, not price. Anchor with most popular plan. |
| **Feature** | Lead with outcome ("Track time in one click"), not feature name. |
| **About** | Founding story. What you believe. Team photos + real context. |

---

## Anti-Patterns

**Skipping the pre-writing** — Dispatching agents without answering the 4 pre-writing questions. Every agent needs this context to write relevant copy.

**Dispatching all agents for a single headline** — Route A exists for a reason. A single key line only needs one Layer 1 agent + critic.

---

## Completion Status

Every run ends with explicit status:
- **DONE** — copy written for the requested surface (Route A or B), critic PASS, voice consistent with brand
- **DONE_WITH_CONCERNS** — copy delivered but critic flagged secondary issues (specificity thin, social-proof weak, voice slightly off); concerns annotated
- **BLOCKED** — brief is fundamentally contradictory (e.g., audience and offer don't align); needs user reconciliation before any agent dispatch
- **NEEDS_CONTEXT** — brand voice or audience undefined and not derivable from the brief; recommend `brand-system` or `icp-research`

**Ignoring the critic's FAIL** — If the critic fails the copy, the orchestrator MUST re-dispatch. Delivering failed copy to the user breaks the quality contract.

**Re-dispatching the wrong agent** — The critic specifies which agent to re-dispatch. Read the failure report carefully.

**More than 2 rewrite cycles** — Diminishing returns. After 2 cycles, deliver with annotations and let the user decide.
