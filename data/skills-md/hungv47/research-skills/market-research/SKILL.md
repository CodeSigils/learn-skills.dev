---
name: market-research
description: "Analyzes market landscapes, competitive dynamics, TAM/SAM/SOM sizing, and whitespace opportunities for a product or category. Produces `research/market-research.md`. Not for building customer personas (use icp-research) or planning marketing campaigns (use campaign-plan). For diagnosing a specific business problem, see diagnose. For prioritizing what to build from market data, see prioritize."
argument-hint: "[market or product category]"
allowed-tools: Read Grep Glob Bash WebSearch WebFetch
license: MIT
metadata:
  author: hungv47
  version: "2.0.0"
  budget: deep
  estimated-cost: "$1-3"
promptSignals:
  phrases:
    - "market research"
    - "competitive analysis"
    - "market size"
    - "tam sam som"
    - "competitor analysis"
    - "market landscape"
  allOf:
    - [market, landscape]
    - [competitive, dynamics]
  anyOf:
    - "competitor"
    - "market"
    - "whitespace"
    - "sizing"
    - "tam"
  noneOf:
    - "customer persona"
    - "buyer persona"
  minScore: 6
routing:
  intent-tags:
    - market-research
    - competitive-analysis
    - market-sizing
    - tam-sam-som
    - whitespace-analysis
  position: pipeline
  lifecycle: canonical
  produces:
    - research/market-research.md
  consumes:
    - research/product-context.md
  requires: []
  defers-to:
    - skill: icp-research
      when: "need audience personas, not market landscape"
    - skill: diagnose
      when: "diagnosing a specific metric decline, not surveying the market"
  parallel-with:
    - diagnose
  interactive: false
  estimated-complexity: heavy
---

# Market Research — Orchestrator

*Strategy — Entry point. Maps market landscape, competitors, and identifies gaps and opportunities.*

**Core Question:** "What does the market look like, and where are the gaps worth filling?"

## Critical Gates — Read First

1. **Sources >18 months old → flag as historical, not current.** Don't present stale data as current intelligence.
2. **TAM/SAM/SOM without methodology is a guess.** Every estimate needs method (top-down/bottom-up), source, and confidence.
3. **Adjacent competitors are the highest threat — never skip the adjacent check.** Biggest threats come from adjacent categories expanding in.
4. **Never rely on training data for positions or pricing — use WebSearch.** Competitor data changes constantly; verify live.

## Philosophy

Rigor scales with stakes. Weekend project = quick scan; Series A pivot = deep intel. Evidence, not opinions — every claim cites a source, every opportunity has data.

**Correctness > Verifiability > Completeness > Style.**

## Inputs Required
- Product context (from `research/product-context.md` or willingness to answer questions)

## Output
- `research/market-research.md`

## Chain Position
Previous: none | Next: `prioritize`, `icp-research`

### Skill Deference
- **MARKET landscape and gaps?** → This skill.
- **WHO the customer is, what they feel?** → `icp-research` (personas/VoC, not market maps).
- **A METRIC underperforming?** → `diagnose` (root causes, not landscapes).
- **Know the problem, need SOLUTIONS?** → `prioritize`.

**Re-run triggers:** New market entry, major competitor launch/pivot, fundraising, or quarterly for fast-moving categories.

---

## Pre-Dispatch

Run the Pre-Dispatch protocol (`references/_shared/pre-dispatch-protocol.md`).

**Needed dimensions:** category/niche, geo + time horizon, why-now (decision this informs), known competitors (or "find them"), B2B/B2C.

**Read order:**
1. Pipeline: `research/product-context.md` for product signal, `.agents/skill-artifacts/meta/records/diagnose-*.md` for known root-cause focus.
2. Experience: `.agents/experience/{product,business,audience}.md`.

**Warm Start** (product + B2B/B2C inferable, decision focus clear):

```
Found:
- product → "[1-line from product-context.md]"
- B2B/B2C → "[from audience.md]"

Need before dispatching: category/niche, geo+horizon, why-now, known competitors?
```

**Cold Start** (no upstream context):

```
market-research analyzes the landscape, competitors, sizing (TAM/SAM/SOM),
and whitespace. To target the scan:

1. **Category/niche** — one phrase (e.g., "async project management for engineering teams").
2. **Geo + time horizon** — US / EU / global; current state / forward-looking 12-24 months.
3. **Why now** — what decision does this need to inform? (Market entry, fundraising, pivot, positioning, etc.)
4. **Known competitors** — name 3-5, OR say "find them" if you want me to discover.
5. **B2B/B2C** — affects sizing methodology and consumer-landscape weighting.

Answer 1-5 in one response. I'll dispatch.
```

**Write-back:**

| Q | File | Key |
|---|---|---|
| 1. Category | `product.md` | `Product — category` |
| 2. Geo + horizon | `business.md` | `Business — geo + planning horizon` |
| 3. Why-now | `goals.md` | `Goals — market-research trigger` |
| 4. Competitors | `business.md` | `Business — known competitors` |
| 5. B2B/B2C | `audience.md` | `Audience — B2B or B2C` |

---

## Agent Manifest

7 agents across 2 layers:

| Agent | Layer | Role | Input | Output |
|-------|-------|------|-------|--------|
| [trends-agent](agents/trends-agent.md) | L1 (parallel) | Market trends with direction, evidence, quantification, implication | brief + scope | Market Trends table + narrative |
| [sizing-agent](agents/sizing-agent.md) | L1 (parallel) | TAM/SAM/SOM with methods and confidence levels | brief + scope | Market Sizing table + math |
| [competitor-agent](agents/competitor-agent.md) | L1 (parallel) | Feature matrix, pricing, positioning map, community, adjacent check | brief + scope + known competitors | Competitive Landscape (6 sub-sections) |
| [consumer-landscape-agent](agents/consumer-landscape-agent.md) | L1 (parallel) | Hot topics, cultural moments, sentiment, unmet needs | brief + scope | User & Consumer Landscape |
| [cross-analysis-agent](agents/cross-analysis-agent.md) | L2 (sequential) | Synthesizes L1 outputs into gap identification across 4 dimensions | merged L1 outputs | Gaps & Opportunities (4 gap types) |
| [opportunity-agent](agents/opportunity-agent.md) | L2 (sequential) | Ranks top 3 opportunities with evidence, window, risk, "why now" | cross-analysis output + L1 context | Top 3 Opportunities (ranked) |
| [critic-agent](agents/critic-agent.md) | L2 (sequential) | Validates citations, confidence, methodology, adjacent coverage | full merged artifact | PASS or FAIL with rewrite instructions |

---

## Routing Logic

### Route A: Quick Validation
**Trigger:** "Quick check on this market," "Who are the competitors?", "Is this space crowded?"

```
trends-agent ──┐
               ├──→ cross-analysis-agent → critic-agent
competitor-agent┘
```

Skip sizing-agent. Consumer-landscape-agent optional. Opportunity-agent skipped — cross-analysis identifies gaps directly at Quick scope.

### Route B: Product Positioning
**Trigger:** "Position our product," "Where do we fit?", "Competitive analysis for [product]"

```
trends-agent ────────────┐
sizing-agent (optional) ─┤
competitor-agent ────────┼──→ cross-analysis-agent → opportunity-agent → critic-agent
consumer-landscape-agent ┘
```

All 4 L1 agents parallel. Full L2 sequence.

### Route C: Fundraising / Market Entry
**Trigger:** "Market analysis for investors," "Series A research," "Entering [market]," "Full market research"

```
trends-agent ────────────┐
sizing-agent ────────────┤
competitor-agent ────────┼──→ cross-analysis-agent → opportunity-agent → critic-agent
consumer-landscape-agent ┘
```

All 4 L1 agents parallel at enhanced depth. Sizing-agent required. Opportunity-agent uses quantitative 1-5 scoring. Full L2 sequence.

---

## Scope Calibration

| Decision Context | Research Depth | Competitor Depth | Time Investment |
|-----------------|---------------|-----------------|----------------|
| Quick validation | 3-5 competitors, top-level features | Surface (pricing, positioning) | Light |
| Product positioning | 5-8 competitors, detailed features | Deep (features, community, growth) | Medium |
| Fundraising / market entry | 8-12+ competitors, full landscape | Comprehensive (all dimensions) | Heavy |

**How scope affects agent depth:**

| Section | Quick | Positioning | Fundraising |
|---------|-------|-------------|-------------|
| Market Trends | 2-3 trends, skip narrative | 3-5 trends + narrative | 5+ trends + narrative |
| Market Sizing | Skip | Optional (SAM estimate) | Required (TAM/SAM/SOM) |
| Feature Comparison | Top 5 features + type labels | 5-8 features + type labels | 8+ features + type labels |
| Pricing | Entry price + model only | Full pricing table | Full table + hidden costs |
| Positioning Map | Skip | Include | Include + adjacent entrants |
| Community & Mindshare | Skip | Top 3 competitors | All competitors |
| Gaps & Opportunities | Top 3 opportunities | Full 4-dimension analysis | Full analysis + scoring from reference |

---

## Dispatch Protocol

### Step 0: Product Context

Check for `research/product-context.md`. If missing: **strongly recommend** running `icp-research` first to create it. Skill works without it, but quality improves significantly. If user declines, interview for category, target market, and differentiator at minimum.

**If product-context.md exists**, extract before dispatch:
- **Product category** → which competitors and features
- **Differentiator** → positioning map axes and gap identification
- **Pricing model** → pricing comparison dimensions
- **Target segment** → filters direct vs. adjacent competitors

### Step 1: Scope Interview

For vague requests ("research this market", "who are the competitors"):

1. **What market/industry?** — Name product category and adjacent. (Not "tech" — which segment?)
2. **Geographic scope?** — Global, regional, or specific countries?
3. **Timeframe?** — Current snapshot, or 2-3 year trajectory?
4. **Known competitors?** — Any starting points (not the full list).
5. **What decisions will this inform?** — Building / positioning / fundraising / pivoting? Determines scope and route.

All 5 answers required — without scope, research sprawls into a Wikipedia article.

### Single-Agent Fallback

For narrow tasks ("just list competitors", "what's the market size?"), dispatch only the relevant agent. Skip cross-analysis, opportunity, and critic. Return output directly.

---

## Layer 1 Dispatch — Parallel Research Agents

Build the pre-writing context object from Step 0 and Step 1, then dispatch:

```
pre-writing = {
  category: [product category],
  differentiator: [from product-context or interview],
  pricing_model: [from product-context or interview],
  target_segment: [from product-context or interview],
  scope: "Quick" | "Positioning" | "Fundraising",
  geography: [from interview],
  timeframe: [from interview],
  known_competitors: [from interview]
}
```

**Dispatch all applicable L1 agents in parallel:**

| Agent | Always | References to Include |
|-------|--------|----------------------|
| trends-agent | Yes (all routes) | — |
| sizing-agent | Route C required, Route B optional, Route A skip | `references/market-sizing-guide.md` |
| competitor-agent | Yes (all routes) | `references/competitor-analysis-framework.md` |
| consumer-landscape-agent | Route B + C required, Route A optional | — |

### Research Tool Priority (all L1 agents)

1. **Exa MCP** or **Perplexity MCP** (if installed) — best for market reports, competitor analysis, trends
2. **Firecrawl** or **Defuddle** (if installed) — scraping specific pages (pricing, features, G2, Crunchbase)
3. **WebSearch** — always available as fallback

### Research Checkpoint

After L1 returns, present findings and gather feedback before L2:

**"Here's the competitive landscape. Before I identify gaps and opportunities:"**
1. **Right competitors?** Missing any? Deprioritize any?
2. **Internal competitive intel?** Battle cards, win/loss data, customer feedback?
3. **Surprising findings to dig deeper on?**

Incorporate any internal data (battle cards, sales notes, support tickets) into merged L1 output before dispatching L2.

---

## Layer 2 Dispatch — Sequential Analysis

After L1 returns and checkpoint feedback is incorporated, dispatch L2 in strict sequence:

### Step 1: Cross-Analysis Agent

```
dispatch cross-analysis-agent:
  upstream: [merged output from all L1 agents]
  references: [references/gap-analysis-template.md]
```

Identifies gaps across 4 dimensions: underserved segments, feature gaps, emerging trend gaps, positioning whitespace.

### Step 2: Opportunity Agent

```
dispatch opportunity-agent:
  upstream: [cross-analysis output + merged L1 context]
  references: [references/gap-analysis-template.md]
```

Receives cross-analysis plus L1 context for evidence. Force-ranks top 3 opportunities.

### Step 3: Critic Agent

```
dispatch critic-agent:
  upstream: [full merged artifact — all L1 + L2 outputs in artifact template]
  references: [all reference files]
```

Evaluates against quality gate checklist. Returns PASS or FAIL.

---

## Critic Gate — Max 2 Cycles

```
cycle = 0
while cycle < 2:
  verdict = critic-agent.evaluate(artifact)
  if verdict == PASS:
    break
  else:
    for each failure:
      re-dispatch named agent with feedback
    merge fixes into artifact
    cycle += 1

if cycle == 2 and verdict == FAIL:
  deliver artifact with critic's remaining notes as "[REVIEWER NOTE]" annotations
  warn user: "Artifact delivered with quality notes — some items could not be resolved in 2 cycles."
```

**On rewrite:** Re-dispatch only the agents the critic names. Don't re-run the full pipeline. Pass critic's per-agent feedback in the `feedback` field.

---

## Quality Gate

Before delivering, verify merged artifact passes:

- [ ] Every claim cites source (URL or publication name)
- [ ] Competitor table: >=3 competitors with quantified size/growth signals
- [ ] Feature comparison: >=5 capabilities relevant to category
- [ ] Gaps & Opportunities: >=3 distinct opportunities with evidence
- [ ] Each Top 3 opportunity: evidence source, window, risk, and "why now"
- [ ] Market trends: >=2 quantified data points (%, $, growth rates)
- [ ] No source >18 months presented as current without historical flag
- [ ] Confidence level stated with justification
- [ ] Adjacent competitors section populated — never skipped
- [ ] TAM/SAM/SOM (if present) shows methodology, not just numbers

---

## Artifact Template

On re-run: rename existing artifact to `market-research.v[N].md` and create new with incremented version.

```markdown
---
skill: market-research
version: 1
date: {{today}}
status: done | done_with_concerns | blocked | needs_context
---

# Market Research

## Scope

**Market:** [product category / industry]
**Geography:** [scope]
**Decision context:** [what this research informs]
**Date:** [today]

## Market Trends

| Trend | Direction | Evidence | Quantification | Implication |
|-------|-----------|----------|---------------|-------------|

**Narrative:** [2-3 paragraph market story connecting trends]

## Market Sizing (if applicable)

| Metric | Method | Estimate | Source | Confidence |
|--------|--------|----------|--------|-----------|

## User & Consumer Landscape

| Dimension | Findings | Source |
|-----------|----------|--------|

## Competitive Landscape

### Overview
| Competitor | Founded | Funding/Revenue | Team Size | Target Segment | Positioning | Threat |
|-----------|---------|----------------|-----------|---------------|-------------|--------|

### Adjacent Competitors
| Adjacent Category | Player | Why They Could Enter | Likelihood | Signal to Watch |
|------------------|--------|---------------------|-----------|----------------|

### Feature Comparison
| Capability | [Your Product] | Competitor A | Competitor B | Competitor C |
|-----------|---------------|-------------|-------------|-------------|

### Pricing
| Competitor | Free Tier | Entry Price | Mid Tier | Enterprise | Model |
|-----------|-----------|------------|----------|-----------|-------|

### Positioning Map
[2-axis positioning map: axes selected from buyer decision criteria]

### Community & Mindshare
| Competitor | Community Size | Activity Level | Sentiment | Share of Voice |
|-----------|---------------|---------------|-----------|---------------|

## Gaps & Opportunities

### Gap Analysis (4 dimensions)

| Dimension | Gap | Evidence | Demand Signal | Difficulty |
|-----------|-----|----------|---------------|-----------|
| Underserved Segment | [Segment] | [Evidence] | [Signal] | — |
| Feature Gap | [Gap] | [User need] | [Evidence] | S/M/L |
| Emerging Trend | [Trend] | [Incumbent response] | [Opportunity window] | — |
| Positioning White Space | [Position] | [Why empty] | [Risk] | — |

### Top 3 Opportunities

| # | Opportunity | Evidence Source | Window | Risk | Why Now |
|---|------------|---------------|--------|------|---------|

## Limitations & Confidence

| Aspect | Confidence | Justification |
|--------|-----------|---------------|

**Data gaps:** [What couldn't be found]

## Next Step

Run `prioritize` to turn top opportunities into prioritized initiatives, or `icp-research` to build personas for identified underserved segments.
```

---

## Worked Example

**User:** "Research the AI code review market."

### Step 0 — Product Context
Checked `research/product-context.md` — not found. Interview initiated.

### Step 1 — Scope Interview
- "What market?" → "AI-powered code review tools — automated PR review, code quality analysis"
- "Geography?" → "Global, English-speaking focus"
- "Timeframe?" → "Current snapshot with 2-year trajectory"
- "Known competitors?" → "CodeRabbit, Sourcery, maybe Codacy"
- "What decisions?" → "We're building a new product and need to know where the gaps are"
- **Scope calibration:** "Building a new product" → **Route B: Product positioning** (5-8 competitors, detailed features)

### Layer 1 Dispatch (parallel)

**trends-agent output (summarized):**
```
| Trend | Direction | Evidence | Quantification | Implication |
|-------|-----------|----------|---------------|-------------|
| AI dev tools adoption | Growing rapidly | GitHub Octoverse 2025 | 78% of developers use AI coding tools (+32% YoY) | Market tailwind for AI code review |
| Shift-left quality | Accelerating | GitLab DevSecOps Survey 2025 | 65% of orgs testing in CI, up from 48% | Code review moving earlier in pipeline |
| LLM cost decline | Declining costs | OpenAI, Anthropic pricing pages | GPT-4 class: ~$3/M tokens (was $30 in 2023) | AI review becoming economically viable at scale |
```

**competitor-agent output (summarized):**
```
5 direct competitors mapped (CodeRabbit, Sourcery, Codacy, Qodo, Ellipsis)
3 adjacent competitors identified (GitHub Copilot, SonarQube, Sourcegraph)
Feature matrix: 7 capabilities, Stakes/Diff labeled
Pricing: all 5 competitors with full table
```

**consumer-landscape-agent output (summarized):**
```
Hot topics: AI hallucination in code suggestions, false positive fatigue
Sentiment: Cautiously optimistic — devs want AI review but distrust accuracy
Unmet needs: Cross-repo understanding, org-specific style enforcement, test generation
```

### Research Checkpoint
- User confirmed competitor list: "Yeah, those are the main ones. I'd add Qodo and Ellipsis too."
- User shared internal sales notes: "We lose deals to CodeRabbit on speed, to Codacy on compliance"
- Incorporated internal intel into merged L1 output.

### Layer 2 Dispatch (sequential)

**cross-analysis-agent** → Identified 3 underserved segments, 5 feature gaps, 3 emerging trends, 2 positioning whitespaces.

**opportunity-agent** → Ranked top 3:
1. Multi-repo context awareness (Medium risk, 12-18 month window)
2. Self-hosted AI review for regulated industries (Low risk, 6-12 month window)
3. Review-to-test pipeline (High risk, 12-24 month window)

**critic-agent** → PASS on first cycle. Notes: "Adjacent competitor section is strong. Sizing was correctly skipped for Positioning scope."

### Final Artifact
Merged all outputs into `research/market-research.md` per artifact template.

---

## Anti-Patterns

**Describing without concluding** — Listing competitors and features without identifying gaps produces a Wikipedia article, not strategic intelligence. Gaps & Opportunities is the point — everything before is setup.
**INSTEAD:** Ensure cross-analysis-agent and opportunity-agent run. Skipping them = incomplete output.

**Unsourced market sizing** — "The market is worth $5B" without source or methodology is fiction.
**INSTEAD:** Every sizing claim needs source, methodology (top-down or bottom-up), and confidence. See [references/market-sizing-guide.md](references/market-sizing-guide.md).

**Recency blindness** — Using a 2022 report for a 2026 market. In fast categories, 18-month-old data is historical, not current.
**INSTEAD:** Flag source dates prominently. Prioritize last-12-month sources.

**Feature-only competitor analysis** — Comparing features while ignoring positioning, community, growth, and pricing produces an incomplete picture.
**INSTEAD:** competitor-agent covers all 6 dimensions (overview, adjacent, features, pricing, positioning, community). Don't accept feature-only output.

**Confirmation bias in gap identification** — Reverse-engineering "gaps" from your product's features is rationalization, not research.
**INSTEAD:** cross-analysis-agent identifies gaps from user complaints, switching reasons, and unmet needs FIRST, then checks product fit.

**Treating all competitors as equal threats** — A $40M-funded company with 200 employees in your exact segment is not a Product Hunt side project.
**INSTEAD:** competitor-agent assigns threat levels (Critical/High/Medium/Low/Watch) with justification.

**Ignoring adjacent competitors** — Biggest threats often come from adjacent categories expanding in.
**INSTEAD:** competitor-agent always researches adjacent players. critic-agent specifically checks this.

**Positioning map with self-serving axes** — Axes should reflect what MATTERS to buyers, not what makes your product look good.
**INSTEAD:** competitor-agent validates axes against what users compare when switching.

---

## Required Artifacts
None — this is an entry point for the Strategy track.

### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `product-context.md` | icp-research | Better competitor selection and gap identification |
| `diagnose.md` | diagnose | Known root causes focus analysis on relevant dimensions |

---

## Completion Status

Every run ends with explicit status:
- **DONE** — all 4 Layer 1 streams complete (trends, sizing, competitor, consumer-landscape), opportunities ranked, critic PASS
- **DONE_WITH_CONCERNS** — partial coverage (e.g., sizing data thin or estimated); opportunities listed with confidence flags in artifact
- **BLOCKED** — category undefined or too broad to size; needs user-supplied scope narrowing before any agent can dispatch
- **NEEDS_CONTEXT** — `research/product-context.md` absent and product not described; recommend `icp-research` first or interview the user

---

## References

- [references/competitor-analysis-framework.md](references/competitor-analysis-framework.md) — Structured competitor evaluation methodology
- [references/market-sizing-guide.md](references/market-sizing-guide.md) — TAM/SAM/SOM methods and search patterns
- [references/gap-analysis-template.md](references/gap-analysis-template.md) — Framework for opportunity identification and scoring
