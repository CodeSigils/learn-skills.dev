---
name: icp-research
description: "This skill should be invoked when the user needs to understand who they are selling to. Triggers include 'researching customers', 'building personas', 'ideal customer', 'analyzing pain points', 'understanding a target market', 'who are we building for', 'who should we target', 'buyer persona', 'jobs to be done', 'competitive audience analysis', 'market sizing', 'how should we segment', or 'what do people actually want' -- even if they just say 'I don't know who my customer is', 'we're guessing at our audience', or 'we're attracting the wrong people.' Not for competitive positioning or strategy (use solution-design), campaign planning (use imc-plan), or fixing existing copy (use humanize)."
license: MIT
metadata:
  author: hungv47
  version: "2.2.1"
---

# ICP Research & Audience Intelligence

*Communicate Track — Step 1 of 4. Foundational skill for all stacks. Builds deep audience intelligence from real research, not assumptions.*

**Core Question:** "Who exactly are we talking to and what keeps them up at night?"

## Philosophy

This skill provides research structure, not a rigid formula. The minimums for channels, quotes, and platforms ensure thoroughness — they're not arbitrary thresholds. If overwhelming evidence surfaces in 2 channels, you don't need a third. If one devastating quote captures a pain perfectly, you don't need three. Let evidence dictate depth.

## Inputs Required
- Product context from `.agents/product-context.md` (or willingness to answer product questions)

## Output
- `.agents/mkt/icp-research.md`

## Quality Gate
Before delivering, verify:
- [ ] Every VoC quote includes platform name and is from a real source (not agent-generated)
- [ ] Each persona has a habitat map with specific channels with supporting evidence. Aim for ≥3; if research surfaces fewer, document why (niche audience, concentrated community). (Not just "Reddit" — which subreddit?)
- [ ] Each emotional driver is traced to ≥2 specific quotes
- [ ] Decision psychology section names specific cognitive biases and objections (not generic "they need trust")

## Chain Position
Previous: none (or any skill needing audience context) | Next: `imc-plan`, `brand-system` (from design-skills — uses audience data for brand strategy)

**Foundational role:** This skill creates `.agents/product-context.md`, used by 12+ downstream skills across all 4 stacks (comms, strategy, prod, design). Running it first provides significantly better output for all downstream skills.
**Re-run triggers:** When pivoting audience, entering a new market, after major product changes, or quarterly for active products.

---

## Before Starting

### Step 0: Product Context (Canonical Source)
Check for `.agents/product-context.md`. If missing, **scan first, then interview for gaps:**

1. **Auto-scan available sources:** Look for README.md, marketing site copy, pricing page, product descriptions, and any existing documentation in the codebase. Extract what you can about the 8 dimensions below.
2. **Interview only for gaps:** Present what you found and ask the user to confirm, correct, or fill in missing dimensions.

This scan-then-interview approach avoids asking the user questions they've already answered elsewhere. This skill is the canonical source for product context across all skill stacks (comms, strategy, prod, design). Save to `.agents/product-context.md`:

```markdown
# Product Context

**Date:** [today]

## Product
[One sentence: what you sell]

## Buyer
[Primary buyer: role, company type, situation]

## Problem
[The pain it solves — in their words, not yours]

## Differentiator
[What's different — something a competitor CANNOT claim]

## Social Proof
[Best testimonial or most repeated praise]

## Model
[Price, pricing model, free trial availability]

## Voice
[3 adjectives: e.g., "direct, technical, warm"]

## Primary CTA
[What should people do next: e.g., "Start free trial"]
```

All marketing skills read this file for product context.

### Required Artifacts
| Artifact | Source | If Missing |
|----------|--------|------------|
| `product-context.md` | icp-research | **INTERVIEW.** Interview for 8 product dimensions and save to `.agents/product-context.md`. |

### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `problem-analysis.md` | problem-analysis (from hungv47/strategy-skills) | Problem context sharpens audience research |

---

## Step 1: Scope

Interview for:
1. **Who are we researching?** (Job role, mindset, community, or use case)
2. **What decisions will this inform?** (Messaging? Channels? Positioning? All three?)
3. **B2C or B2B?** Geography? Specific segments to focus or exclude?

---

## Step 2: Research

Use research tools to find real quotes — they prevent hallucinated personas and ground pain points. Avoid generating hypothetical quotes, invented personas, or assumed pain points — they collapse under scrutiny and mislead downstream skills.

**Research tool priority:**
1. **Exa MCP** or **Perplexity MCP** (if installed) — best for semantic search across forums, communities, and reviews. Use first when available.
2. **Firecrawl** or **Defuddle** (if installed) — for scraping specific pages (G2 reviews, competitor blogs, community threads).
3. **WebSearch** — supporting role for broad discovery and gap-filling. Always available as fallback.
4. **User interview fallback** — when all tools yield insufficient data, ask the user for customer quotes, support tickets, sales call notes, or internal Slack threads.

When data is thin (niche audience, few public discussions), flag confidence level as **LOW** in the artifact and note specific data gaps.

### Search Query Patterns

Use these specific queries. Adapt [topic] to the product/audience:

| Goal | Query Pattern |
|------|--------------|
| Find communities | `site:reddit.com "[topic]" subreddit` |
| Find pain points | `site:reddit.com "[topic]" frustrated OR struggling OR hate` |
| Find reviews | `site:g2.com "[product category]" OR site:capterra.com "[product category]"` |
| Find discussions | `"[topic]" forum OR community best OR worst` |
| Find Twitter takes | `site:twitter.com "[topic]" thread` |
| Find decision criteria | `"[product category]" vs OR alternative OR switch from` |
| Find objections | `"[product/competitor]" not worth OR overpriced OR disappointing` |

### Multi-Platform Coverage

Search across multiple categories for breadth. Aim for ≥4 when audience is spread; for niche B2B, 2-3 may suffice if they cover primary habitats:

| Category | Where | What to Extract |
|----------|-------|----------------|
| Communities | Reddit, Facebook Groups, LinkedIn Groups | Pain expressions, solution attempts |
| Social | Twitter/X, TikTok | Real-time frustrations, opinions |
| Reviews | G2, Capterra, App Store, Amazon | Feature complaints, switching reasons |
| Content | YouTube comments, Quora | Questions asked, knowledge gaps |
| Professional | Discord, Slack communities, industry forums | Unfiltered opinions, workflow details |

### VoC Quality Criteria

A **good quote** has:
- Emotional intensity (frustration, excitement, relief — not neutral)
- Specificity (mentions a specific tool, workflow, number, or scenario)
- Recency (within last 12 months)
- Relevance to the product category

A **bad quote** is:
- Generic ("I wish there was a better way")
- Old (2+ years, industry may have shifted)
- From a seller/marketer, not a real user
- A one-word reaction with no context

Collect 3 quotes per pain category. Stop when patterns repeat.

**Quote weighting** — not all quotes are equally useful. Prioritize:

| Priority | Quote Type | Why |
|----------|-----------|-----|
| **Critical** | Decision-maker quote (buyer, budget holder) | Their words are what stops or starts a purchase |
| **High** | Quote revealing mechanism (explains WHY pain exists, not just that it does) | Mechanisms inform solutions; complaints only inform messaging |
| **High** | Quote contradicting your assumptions | The most valuable data is what surprises you |
| **Standard** | User/practitioner quote expressing pain | Useful for copy but doesn't reveal buying dynamics |
| **Low** | Emotion-only quote ("this is so frustrating") without mechanism | Validates intensity but gives no strategic direction |

Hunt for mechanism-revealing and decision-maker quotes first — they're the most strategically useful.

When you have 3 quotes for a pain category, check: do you have at least one mechanism-revealing quote? If all 3 are emotion-only, keep searching — you have the WHAT but not the WHY.

### Pain Analysis (3 Levels)

| Level | What | Where to Find |
|-------|------|--------------|
| **Surface** | What they openly complain about | Public forums, review sites |
| **Hidden** | What they say anonymously | Reddit throwaways, anonymous reviews |
| **Emotional** | Identity threats, status anxiety, fear | Language intensity, desperation indicators |

### Habitat Mapping

For every platform where audience activity appears, document specifically — vague platform names produce vague channel strategies downstream:

| Platform | Specific Community | Density | Engagement Type | Role |
|----------|-------------------|---------|----------------|------|
| Reddit | r/[specific subreddit] | H/M/L | Lurker/Engager/Creator | Discovery/Trust/Conversion |

Specify the exact community, not just the platform — "Reddit" is too vague; name the subreddit. "LinkedIn" is too vague; name the group or content type.

**Engagement type classification** — sample 20-30 profiles from the community to classify:

| Type | Behavior Threshold | How to Identify |
|------|-------------------|----------------|
| **Lurker** | Visits regularly, posts <1x/month, consumes >10 pieces/week | No visible post history in community; high member count vs. low post volume |
| **Engager** | Comments/likes 1-4x/month, occasionally shares | Visible in comment sections, responds to others, doesn't start threads |
| **Creator** | Posts original content 1x/week+, starts discussions, responds to replies | Active post history, recognized by community, generates threads |
| **Subscriber** | Prefers push content (email, notifications), passive consumption | Follows newsletters, subscribed to feeds, rarely visible in community |
| **Searcher** | Uses platform search when problems arise, no ongoing presence | Appears in search-triggered threads, asks questions then disappears |

Assign **density** as % of your target persona active in the community: H = >30%, M = 10-30%, L = <10%. Estimate by checking: how many posts in the last month are from someone matching your persona's role/situation?

See [references/habitat-mapping.md](references/habitat-mapping.md) for density definitions.

### Decision Psychology

Document:
- **Trigger:** What event makes them seek solutions?
- **Research behavior:** Where they go first, second, third
- **Cognitive biases:** Which are strongest? (Loss aversion? Social proof? Authority?)
- **Top 3 objections:** What stops them from buying? What's the psychological root of each?
- **Trust signals:** Who/what do they trust? What creates instant distrust?

---

## Step 3: Synthesize

### 2 Personas (max) — Genuine constraint: more than 2 dilutes focus for downstream skills. Force-rank if research reveals 4+ segments.

For each persona, provide ALL of:
- **Demographics:** Age range, role, industry, company size
- **Pain Profile:** Top 3 pains with triggers, impact, and quotes
- **Decision Psychology:** Research behavior, biases, objections + roots
- **Habitat Map:** ≥3 specific channels with density and engagement type
- **VoC Quotes:** 3-5 most revealing, with platform attribution

### Top 3 Emotional Drivers
Core psychological motivations. Each traced to ≥2 specific quotes.

### Red Flags
Language or positioning that triggers instant skepticism for this audience.

---

## Artifact Template

```markdown
---
skill: icp-research
version: 1
date: [today's date]
status: draft
---

# ICP Research

**Date:** [today]
**Skill:** icp-research
**Product:** [from product-context.md]

## Persona 1: [Name/Archetype]

**Demographics:** [Age, role, industry, company size]

### Pain Profile
1. **[Pain name]** — [description]
   - Trigger: [what causes acute pain]
   - Impact: [daily/financial/professional]
   - Quote: "[exact quote]" — [Platform, context]
   - Quote: "[exact quote]" — [Platform, context]

2. **[Pain name]** — [description]
   [Same format]

3. **[Pain name]** — [description]
   [Same format]

### Decision Psychology
- **Trigger:** [what event starts their search]
- **Research path:** [where they go 1st → 2nd → 3rd]
- **Key biases:** [which cognitive biases are strongest]
- **Objections:** (1) [objection] — root: [psychological reason]. (2) [objection] — root: [reason]. (3) [objection] — root: [reason].
- **Trust signals:** [what they trust]
- **Distrust triggers:** [what kills credibility]

### Habitat Map
| Platform | Community | Density | Engagement | Role |
|----------|-----------|---------|-----------|------|
| [Specific] | [Specific] | H/M/L | [Type] | [Role] |

## Persona 2: [Name/Archetype]
[Same format]

## Top 3 Emotional Drivers
1. **[Driver]** — [explanation]. Quotes: "[quote 1]" ([source]), "[quote 2]" ([source])
2. **[Driver]** — [explanation]. Quotes: ...
3. **[Driver]** — [explanation]. Quotes: ...

## Red Flags
- [Language/positioning that triggers skepticism and why]

## Next Step
Run `imc-plan` to turn these insights into a communication plan.

> On re-run: rename existing artifact to `icp-research.v[N].md` and create new with incremented version.
```

---

## Worked Example

**User:** "Research my ICP for a project management tool aimed at engineering teams."

**Interview:**
- "Who are we researching?" → "Engineering managers at mid-size SaaS companies (50-200 engineers)"
- "What decisions will this inform?" → "Messaging and channel strategy for launch"
- "B2B or B2C?" → "B2B, US and EU"

**Artifact saved to `.agents/mkt/icp-research.md`:**

```markdown
# ICP Research

**Date:** 2026-03-17
**Skill:** icp-research
**Product:** ProjectSync — async project visibility for engineering teams

## Persona 1: The Overwhelmed EM

**Demographics:** 30-40, Engineering Manager, B2B SaaS, 50-200 engineers

### Pain Profile
1. **Status update theater** — hours lost writing updates nobody reads
   - Trigger: Monday morning status email that takes 45 min to compile
   - Impact: 6-8 hrs/week across the team on reporting instead of building
   - Quote: "I spend more time telling people what I did than actually doing it" — r/ExperiencedDevs
   - Quote: "Our Monday standup is 45 minutes of people reading Jira tickets aloud" — r/engineeringmanagers

### Habitat Map
| Platform | Community | Density | Engagement | Role |
|----------|-----------|---------|-----------|------|
| Reddit | r/ExperiencedDevs | H | Engager | Discovery |
| Reddit | r/engineeringmanagers | M | Lurker | Trust |
| LinkedIn | #engineeringmanagement feed | M | Creator | Conversion |
```

---

## Anti-Patterns

**Demographic-only personas** — "35-year-old male, $80K income" tells marketing nothing about motivations or language. Personas must include pain profile, decision psychology, and habitat map — demographics alone produce generic messaging.

**Hallucinated quotes** — Generating plausible-sounding VoC quotes instead of finding real ones. Fabricated quotes collapse under scrutiny and mislead downstream skills. Every quote must include a real platform attribution.

**Researching existing customers only** — Existing customers survived the funnel; their feedback has survivorship bias. Research must include prospects who *didn't* convert and users of competitor products.

**Too many personas** — More than 2 personas dilutes focus and makes downstream IMC planning impossible. If research reveals 4+ distinct segments, force-rank and pick the top 2 by revenue potential.

**Platform-level habitat mapping** — "They're on LinkedIn" is too vague to act on. Specify the exact subreddit, group, hashtag, or content type — vague platforms produce vague channel strategies.

**Recycling stale research** — Reusing personas and VoC quotes from a previous product iteration or market without re-validation. Markets shift, competitors launch, and pain points evolve. Always validate existing research against current sources before reusing.

---

## References

- [references/habitat-mapping.md](references/habitat-mapping.md) — Density definitions, cross-persona analysis
- [references/icp-to-imc-handoff.md](references/icp-to-imc-handoff.md) — How to package outputs for IMC
- [references/voice-of-customer.md](references/voice-of-customer.md) — VoC collection patterns
- [references/customer-interviews.md](references/customer-interviews.md) — Win/loss interview methodology, support ticket analysis
