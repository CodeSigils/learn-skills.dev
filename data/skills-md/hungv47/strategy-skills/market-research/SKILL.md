---
name: market-research
description: "This skill should be invoked when the user needs to understand a market landscape, competitive dynamics, or identify gaps and opportunities. Triggers include 'research this market', 'who are the competitors', 'what does the competitive landscape look like', 'market analysis', 'competitive analysis', 'market sizing', 'TAM SAM SOM', 'where are the gaps', 'market opportunity', 'is there room for us', 'what's the white space', 'landscape analysis', 'industry overview', or 'who else is doing this' -- even if they just describe a product idea and want to know if it's viable, ask about competitors without naming the skill, or want to understand market trends before building. Not for diagnosing why a metric is underperforming (use problem-analysis), identifying WHO the customer is and building personas (use icp-research), brainstorming solutions to a known problem (use solution-design), or planning marketing campaigns (use imc-plan)."
license: MIT
metadata:
  author: hungv47
  version: "1.0.0"
---

# Market Research

*Strategy — Entry point. Maps market landscape, competitors, and identifies gaps and opportunities.*

**Core Question:** "What does the market look like, and where are the gaps worth filling?"

## Philosophy

Research rigor scales with stakes. A weekend project needs a quick landscape scan; a Series A pivot needs deep competitive intelligence. This skill produces evidence, not opinions. Every claim cites a source. Every opportunity has supporting data.

**Correctness > Verifiability > Completeness > Style.**

## Inputs Required
- Product context (from `.agents/product-context.md` or willingness to answer questions)

## Output
- `.agents/market-research.md`

## Quality Gate
Before delivering, verify:
- [ ] Every claim cites a source with URL or publication name
- [ ] Competitor table includes ≥3 competitors with quantified size/growth signals
- [ ] Feature comparison covers ≥5 capabilities relevant to the product category
- [ ] Gaps & Opportunities section identifies ≥3 distinct opportunities with evidence
- [ ] Each Top 3 opportunity includes: evidence source, estimated window, and risk level
- [ ] Market trends include ≥2 quantified data points (%, $, growth rates)
- [ ] No source older than 18 months unless flagged as historical context
- [ ] Confidence level stated with justification

## Chain Position
Previous: none | Next: `solution-design`, `icp-research`

### Skill Deference
- **Need to understand the MARKET and WHERE the gaps are?** → Use this skill.
- **Need to understand WHO the customer is and what they feel?** → Use `icp-research` (from comms-skills) instead — it builds personas and VoC, not market maps.
- **Have a METRIC that's underperforming?** → Use `problem-analysis` instead — it diagnoses root causes, not landscapes.
- **Already know the problem and need SOLUTIONS?** → Use `solution-design` instead.

**Re-run triggers:** When entering a new market, when a major competitor launches or pivots, when fundraising (investors expect current data), or quarterly for fast-moving markets.

---

## Before Starting

### Step 0: Product Context
Check for `.agents/product-context.md`. If missing: **Strongly recommended:** run `product-description` or `icp-research` (from `hungv47/comms-skills`) first — both create `.agents/product-context.md`, and `product-description` also produces `.agents/mkt/product-description.md` (deep product intelligence with features, positioning, pricing that directly feeds competitor comparison). This skill works without them but produces significantly better analysis with product context. If the user prefers not to, interview for the product's category, target market, and key differentiator at minimum.

**If product-context.md exists**, extract before proceeding:
- **Product category** → determines which competitors to include and which features to compare
- **Differentiator** → anchors positioning map axes and gap identification
- **Pricing model** → frames pricing comparison dimensions
- **Target segment** → filters competitors by segment overlap (direct vs. adjacent)

**If product-description.md exists**, also extract: feature list (for feature comparison "Your Product" column), competitive positioning claims (to verify against research), and pricing details (for pricing table).

### Required Artifacts
None — this is an entry point for the Strategy track.

### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `product-context.md` | product-description or icp-research (from hungv47/comms-skills) | Product context for better competitor selection and gap identification |
| `product-description.md` | product-description (from hungv47/comms-skills) | Deep product intelligence (features, positioning, pricing) sharpens competitor comparison |
| `problem-analysis.md` | problem-analysis | Known root causes focus competitive analysis on relevant dimensions |

---

## Step 1: Scope

### Market Interview

If the user provides a vague request ("research this market", "who are the competitors"):

1. **What market/industry?** — Name the product category and adjacent categories. (Not "tech" — which segment?)
2. **Geographic scope?** — Global, specific regions, or specific countries?
3. **Timeframe?** — Current snapshot, or include trajectory (last 2-3 years)?
4. **Known competitors?** — List any the user already tracks. These are starting points, not the full list.
5. **What decisions will this inform?** — Building a new product? Positioning an existing one? Fundraising? Pivoting? The answer determines depth.

All 5 answers are necessary before proceeding — without scope, research sprawls and produces a Wikipedia article instead of actionable intelligence.

### Scope Calibration

| Decision Context | Research Depth | Competitor Depth | Time Investment |
|-----------------|---------------|-----------------|----------------|
| Quick validation | 3-5 competitors, top-level features | Surface (pricing, positioning) | Light |
| Product positioning | 5-8 competitors, detailed features | Deep (features, community, growth) | Medium |
| Fundraising / market entry | 8-12+ competitors, full landscape | Comprehensive (all dimensions) | Heavy |

**How scope affects later steps:**

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

## Step 2: Research

### Research Tool Priority
1. **Exa MCP** or **Perplexity MCP** (if installed) — best for market reports, competitor analysis, and trend data. Use first when available.
2. **Firecrawl** or **Defuddle** (if installed) — for scraping specific pages (pricing pages, feature lists, G2 comparisons, Crunchbase profiles).
3. **WebSearch** — supporting role for broad discovery and gap-filling. Always available as fallback.

### Search Query Patterns

| Goal | Query Pattern |
|------|--------------|
| Market size/trends | `"[market] market size [year]" OR "[market] industry report [year]"` |
| Growth rates | `"[market] growth rate" OR "[market] CAGR"` |
| Competitor discovery | `"[product category] alternatives" OR "[known competitor] vs" OR "[product category] landscape"` |
| Competitor funding/size | `"[competitor] funding" OR "[competitor] revenue" OR site:crunchbase.com "[competitor]"` |
| Feature comparison | `"[product category] comparison" OR "[competitor 1] vs [competitor 2]" features` |
| Pricing intelligence | `site:[competitor].com pricing OR "[competitor] pricing [year]"` |
| Community/mindshare | `site:reddit.com "[competitor]" OR "[product category]" recommendations` |
| Consumer sentiment | `"[product category]" frustrated OR "switched from" OR "moved to"` |
| Emerging trends | `"[market] trends [year]" OR "[market] emerging" OR "[market] future of"` |
| Regulatory landscape | `"[market] regulation [year]" OR "[market] compliance requirements"` |

### Multi-Source Coverage

Search across multiple source types for breadth:

| Source Type | Where | What to Extract |
|-------------|-------|----------------|
| Market reports | Analyst firms, industry publications | Market size, growth rates, trends |
| Competitor sites | Pricing pages, feature pages, about pages | Positioning, pricing, capabilities |
| Review platforms | G2, Capterra, TrustRadius, Product Hunt | User sentiment, feature gaps, switching reasons |
| Communities | Reddit, HN, Twitter/X, industry forums | Real opinions, complaints, unmet needs |
| Funding data | Crunchbase, TechCrunch, PitchBook | Growth signals, investor confidence, runway |
| Job postings | Competitor careers pages | Growth direction, tech stack, team expansion areas |

### Source Quality Criteria

| Quality | Characteristics | Use For |
|---------|----------------|---------|
| **High** | Primary data, named methodology, recent (<12 months) | Core claims, market sizing |
| **Medium** | Secondary analysis, reputable publication, recent-ish (<18 months) | Supporting evidence, trend confirmation |
| **Low** | Blog posts, undated, no methodology stated | Directional signals only — flag confidence |

---

## Step 3: Analysis

### Market Trends

For each major trend identified:

| Trend | Direction | Evidence | Quantification | Implication |
|-------|-----------|----------|---------------|-------------|
| [Trend name] | Growing/Declining/Emerging | [Source + URL] | [%, $, or growth rate] | [What it means for this market] |

Narrative: Connect trends into a coherent market story. Where is the market heading in 12-24 months?

### Market Sizing (Fundraising / market entry scope only)

Skip for Quick validation. Optional for Product positioning. Required for Fundraising / market entry.

Use methods from [references/market-sizing-guide.md](references/market-sizing-guide.md):

| Metric | Method | Estimate | Source | Confidence |
|--------|--------|----------|--------|-----------|
| **TAM** | Top-down / Bottom-up | $[X-Y]B | [Source, date] | High/Medium/Low |
| **SAM** | Filters: [geo, segment, model] | $[X-Y]M | [Calculation] | High/Medium/Low |
| **SOM** | [Basis: benchmarks, capacity] | $[X-Y]M | [Assumptions] | High/Medium/Low |

Express as ranges, not point estimates. Show your math. If no reliable data exists for this specific category, state that explicitly and provide the best available proxy with its limitations.

### User & Consumer Landscape

| Dimension | Findings | Source |
|-----------|----------|--------|
| **Hot topics** | What the audience is talking about now | [Communities, social] |
| **Cultural moments** | Events/shifts driving behavior change | [News, trends] |
| **Sentiment** | Overall feeling toward the category | [Reviews, forums] |
| **Unmet needs** | What users ask for that doesn't exist | [Forums, reviews, support threads] |

### Competitor Deep-Dive

For each competitor, analyze across all dimensions — feature-only analysis misses positioning, community, and growth dynamics that determine competitive threat level.

#### Overview Table

| Competitor | Founded | Funding/Revenue | Team Size | Target Segment | Positioning | Threat |
|-----------|---------|----------------|-----------|---------------|-------------|--------|
| [Name] | [Year] | [Amount or estimate] | [Size or estimate] | [Who they serve] | [One-line positioning] | Critical/High/Medium/Low/Watch |

**Threat level** (see [references/competitor-analysis-framework.md](references/competitor-analysis-framework.md) for criteria): Critical = same segment, well-funded, growing, heading toward your differentiation. Watch = early-stage or adjacent player that could pivot into your space. The most dangerous competitors are often "Medium" — adjacent players with resources who haven't entered your space yet.

#### Adjacent Competitor Check

Before finalizing the competitor list, check for adjacent-category players who could expand into this market:

| Adjacent Category | Player | Why They Could Enter | Likelihood | Signal to Watch |
|------------------|--------|---------------------|-----------|----------------|
| [Category] | [Name] | [Capability + motivation] | High/Medium/Low | [Job posting, feature announcement, acquisition] |

**Search patterns:** `"[adjacent category leader] [your category]"`, `"[adjacent player] roadmap OR 'coming soon'"`, `"[adjacent player]" hiring "[your category keyword]"`

Ignoring adjacent competitors is the most common blind spot — the biggest competitive threat often comes from an adjacent category expanding into yours, not from a direct competitor.

#### Feature Comparison Matrix

Include "Your Product" column only if product exists (from product-context.md or product-description.md). Omit for greenfield / new market research.

| Capability | Type | [Your Product] | Competitor A | Competitor B | Competitor C |
|-----------|------|---------------|-------------|-------------|-------------|
| [Feature 1] | Stakes/Diff | ✅/❌/🟡 | ✅/❌/🟡 | ✅/❌/🟡 | ✅/❌/🟡 |
| [Feature 2] | Stakes/Diff | ... | ... | ... | ... |

Legend: ✅ = Full support, 🟡 = Partial/limited, ❌ = Not available

Select ≥5 capabilities that matter most for the product category. Label each as **table stakes** (expected by all buyers) or **differentiator** (distinguishes winners) — this distinction feeds gap analysis.

#### Pricing Comparison

| Competitor | Free Tier | Entry Price | Mid Tier | Enterprise | Model |
|-----------|-----------|------------|----------|-----------|-------|
| [Name] | [Yes/No + limits] | [$/mo] | [$/mo] | [Custom?] | [Per seat/usage/flat] |

#### Positioning Map

Plot competitors on two axes most relevant to the market:

```
[Axis Y label]
    ▲
    │  [Competitor A]
    │         [Competitor C]
    │
    │     [Your Product?]
    │  [Competitor B]
    │              [Competitor D]
    └──────────────────────────► [Axis X label]
```

Common axis pairs: Price vs. Complexity, SMB vs. Enterprise, Breadth vs. Depth, Self-serve vs. Sales-led.

#### Community & Mindshare Assessment

| Competitor | Community Size | Activity Level | Sentiment | Share of Voice |
|-----------|---------------|---------------|-----------|---------------|
| [Name] | [Members/followers] | [Posts/week or engagement rate] | [Positive/Mixed/Negative] | [Estimated % of category mentions] |

See [references/competitor-analysis-framework.md](references/competitor-analysis-framework.md) for detailed evaluation methodology.

---

### Research Checkpoint

Before proceeding to gap analysis, present findings and gather feedback:

**"Here's the competitive landscape I've found. Before I identify gaps and opportunities:"**
1. **Are these the right competitors?** Any missing? Any to deprioritize?
2. **Do you have internal competitive intel?** Sales battle cards, win/loss data, customer feedback about competitors?
3. **Any surprising findings you want me to dig deeper on?**

If user provides internal data (battle cards, sales notes, support tickets), read and incorporate directly — internal competitive intelligence is often more accurate than public sources for feature comparison and positioning.

---

## Step 4: Gaps & Opportunities

This is the most important step. Without it, the output is a Wikipedia article, not strategic intelligence.

### Cross-Analysis Synthesis

Review all research and identify gaps across four dimensions:

#### 1. Underserved Segments
Who is poorly served by existing solutions?

| Segment | Current Options | Why Underserved | Demand Signal |
|---------|----------------|----------------|--------------|
| [Segment] | [What they use now] | [Why it's inadequate] | [Source + how you know they want better] |

#### 2. Feature Gaps
What capabilities do users need that no one (or few) provide well?

| Gap | User Need | Current Workarounds | Demand Evidence | Difficulty |
|-----|-----------|-------------------|-----------------|-----------|
| [Gap] | [What users want] | [How they cope today] | [Source: reviews, forums, requests] | S/M/L |

#### 3. Emerging Trends Not Yet Addressed
What market shifts are creating new needs that incumbents haven't adapted to?

| Trend | Incumbent Response | Opportunity Window | Evidence |
|-------|-------------------|-------------------|----------|
| [Trend] | [How current players are (not) responding] | [Estimated timeframe] | [Source] |

#### 4. Positioning White Space
Where on the positioning map is there room?

| White Space | Description | Why Empty | Risk |
|-------------|------------|-----------|------|
| [Position] | [What this positioning looks like] | [Why no one occupies it] | [Why it might be empty for a reason] |

### Top 3 Opportunities (Ranked)

Synthesize the above into the top 3 most promising opportunities. Force-rank — if everything is equally promising, the analysis isn't sharp enough.

For each:

| # | Opportunity | Evidence Source | Estimated Window | Risk Level | Why Now |
|---|------------|---------------|-----------------|-----------|---------|
| 1 | [Specific opportunity statement] | [Primary evidence] | [How long this window stays open] | Low/Medium/High | [What makes this timely] |
| 2 | ... | ... | ... | ... | ... |
| 3 | ... | ... | ... | ... | ... |

**Ranking criteria:**
- **Evidence strength** — How much data supports this opportunity? (Multiple sources > single blog post)
- **Window urgency** — Is a competitor about to close this gap? Is a trend accelerating?
- **Fit** — How well does this align with the product's strengths and positioning? (Requires product-context.md for strong assessment)

For Quick/Positioning scope, the qualitative ranking above is sufficient. For Fundraising / market entry scope, use the quantitative 1-5 scoring from [references/gap-analysis-template.md](references/gap-analysis-template.md) (Demand Evidence × Competition × Window × Fit) — investors expect structured prioritization, not just a ranked list.

### Limitations & Confidence

| Aspect | Confidence | Justification |
|--------|-----------|---------------|
| Market sizing | High/Medium/Low | [Why — e.g., "Multiple analyst reports agree" or "Extrapolated from limited data"] |
| Competitor data | High/Medium/Low | [Why — e.g., "Public company with reported revenue" or "Estimated from team size"] |
| Gap identification | High/Medium/Low | [Why — e.g., "Strong demand signals from multiple forums" or "Based on absence, not presence"] |

Explicitly state what you couldn't find and where data gaps exist. Honest limitations are more useful than false confidence.

---

## Artifact Template

On re-run: rename existing artifact to `market-research.v[N].md` and create new with incremented version.

```markdown
---
skill: market-research
version: 1
date: {{today}}
status: draft
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
| [Trend] | [Direction] | [Source + URL] | [Data point] | [What it means] |

**Narrative:** [2-3 paragraph market story connecting trends]

## Market Sizing (if applicable)

| Metric | Method | Estimate | Source | Confidence |
|--------|--------|----------|--------|-----------|
| TAM | [Method] | $[X-Y]B | [Source, date] | [Level] |
| SAM | [Filters] | $[X-Y]M | [Calculation] | [Level] |
| SOM | [Basis] | $[X-Y]M | [Assumptions] | [Level] |

## User & Consumer Landscape

| Dimension | Findings | Source |
|-----------|----------|--------|
| Hot topics | [What audience discusses] | [Source] |
| Cultural moments | [Driving behavior change] | [Source] |
| Sentiment | [Category feeling] | [Source] |
| Unmet needs | [What's missing] | [Source] |

## Competitive Landscape

### Overview

| Competitor | Founded | Funding/Revenue | Team Size | Target Segment | Positioning | Threat |
|-----------|---------|----------------|-----------|---------------|-------------|--------|
| [Name] | [Year] | [Amount] | [Size] | [Segment] | [One-line] | [Level] |

### Adjacent Competitors

| Adjacent Category | Player | Why They Could Enter | Likelihood | Signal to Watch |
|------------------|--------|---------------------|-----------|----------------|
| [Category] | [Name] | [Reason] | [Level] | [What to monitor] |

### Feature Comparison

| Capability | Type | [Your Product] | Competitor A | Competitor B | Competitor C |
|-----------|------|---------------|-------------|-------------|-------------|
| [Feature] | Stakes/Diff | ✅/❌/🟡 | ✅/❌/🟡 | ✅/❌/🟡 | ✅/❌/🟡 |

### Pricing

| Competitor | Free Tier | Entry Price | Mid Tier | Enterprise | Model |
|-----------|-----------|------------|----------|-----------|-------|
| [Name] | [Details] | [$/mo] | [$/mo] | [Details] | [Type] |

### Positioning Map

​```
[Axis Y]
    ▲
    │  [Competitors plotted]
    └──────────────────► [Axis X]
​```

### Community & Mindshare

| Competitor | Community Size | Activity Level | Sentiment | Share of Voice |
|-----------|---------------|---------------|-----------|---------------|
| [Name] | [Size] | [Posts/week] | [Sentiment] | [Estimate] |

## Gaps & Opportunities

### Underserved Segments

| Segment | Current Options | Why Underserved | Demand Signal |
|---------|----------------|----------------|--------------|
| [Segment] | [Options] | [Why] | [Evidence] |

### Feature Gaps

| Gap | User Need | Workarounds | Demand Evidence | Difficulty |
|-----|-----------|-------------|-----------------|-----------|
| [Gap] | [Need] | [Cope] | [Evidence] | S/M/L |

### Emerging Trends Not Addressed

| Trend | Incumbent Response | Opportunity Window | Evidence |
|-------|-------------------|-------------------|----------|
| [Trend] | [Response] | [Window] | [Source] |

### Positioning White Space

| White Space | Description | Why Empty | Risk |
|-------------|------------|-----------|------|
| [Position] | [Details] | [Reason] | [Risk] |

### Top 3 Opportunities

| # | Opportunity | Evidence Source | Window | Risk | Why Now |
|---|------------|---------------|--------|------|---------|
| 1 | [Opportunity] | [Source] | [Time] | [Level] | [Reason] |
| 2 | [Opportunity] | [Source] | [Time] | [Level] | [Reason] |
| 3 | [Opportunity] | [Source] | [Time] | [Level] | [Reason] |

## Limitations & Confidence

| Aspect | Confidence | Justification |
|--------|-----------|---------------|
| Market sizing | [Level] | [Why] |
| Competitor data | [Level] | [Why] |
| Gap identification | [Level] | [Why] |

**Data gaps:** [What couldn't be found]

## Next Step

Run `solution-design` to turn top opportunities into prioritized initiatives, or `icp-research` to build personas for identified underserved segments.
```

---

## Worked Example

**User:** "Research the AI code review market."

**Step 1 — Scope Interview:**
- "What market?" → "AI-powered code review tools — automated PR review, code quality analysis"
- "Geography?" → "Global, English-speaking focus"
- "Timeframe?" → "Current snapshot with 2-year trajectory"
- "Known competitors?" → "CodeRabbit, Sourcery, maybe Codacy"
- "What decisions?" → "We're building a new product and need to know where the gaps are"
- Scope calibration: "Building a new product" → Product positioning depth (5-8 competitors, detailed features)

**Research Checkpoint:**
- User confirmed competitor list: "Yeah, those are the main ones. I'd add Qodo and Ellipsis too."
- User shared internal sales notes: "We lose deals to CodeRabbit on speed, to Codacy on compliance"
- No battle cards available

**Step 2-4 — Research, Analysis, and Gaps (summarized):**

```markdown
---
skill: market-research
version: 1
date: 2026-03-19
status: draft
---

# Market Research

## Scope

**Market:** AI-powered code review tools (automated PR review, code quality analysis)
**Geography:** Global, English-speaking focus
**Decision context:** New product — identifying gaps worth building into
**Date:** 2026-03-19

## Market Trends

| Trend | Direction | Evidence | Quantification | Implication |
|-------|-----------|----------|---------------|-------------|
| AI dev tools adoption | Growing rapidly | GitHub Octoverse 2025 | 78% of developers use AI coding tools (+32% YoY) | Market tailwind for AI code review |
| Shift-left quality | Accelerating | GitLab DevSecOps Survey 2025 | 65% of orgs testing in CI, up from 48% | Code review moving earlier in pipeline |
| LLM cost decline | Declining costs | OpenAI, Anthropic pricing pages | GPT-4 class: ~$3/M tokens (was $30 in 2023) | AI review becoming economically viable at scale |

**Narrative:** AI code review is riding two tailwinds: developer AI adoption is mainstream (78%), and the shift-left movement pushes quality checks earlier in the pipeline. Declining LLM costs remove the unit economics barrier that limited earlier entrants. The market is transitioning from "nice-to-have" to "table stakes" within engineering teams, with consolidation likely in 12-24 months as leaders emerge.

## User & Consumer Landscape

| Dimension | Findings | Source |
|-----------|----------|--------|
| Hot topics | AI hallucination in code suggestions, false positive fatigue, context window limits | r/programming, r/ExperiencedDevs |
| Cultural moments | GitHub Copilot ubiquity normalizing AI in dev workflow | HN threads, developer surveys |
| Sentiment | Cautiously optimistic — devs want AI review but distrust accuracy | G2 reviews, Reddit sentiment |
| Unmet needs | Cross-repo understanding, org-specific style enforcement, test generation from findings | G2 feature requests, Reddit complaints |

## Competitive Landscape

### Overview

| Competitor | Founded | Funding/Revenue | Team Size | Target Segment | Positioning | Threat |
|-----------|---------|----------------|-----------|---------------|-------------|--------|
| CodeRabbit | 2023 | $3M seed | ~20 | Mid-market dev teams | "AI-first code reviewer" — speed + context | Critical |
| Sourcery | 2018 | $5M Series A | ~15 | Individual devs + teams | "Instant code improvement" — refactoring focus | Medium |
| Codacy | 2012 | $8M total | ~50 | Enterprise | "Automated code quality" — traditional + AI layer | High |
| Qodo (ex-CodiumAI) | 2022 | $40M Series A | ~80 | Enterprise | "Code integrity" — testing + review | Critical |
| Ellipsis | 2023 | $2M seed | ~5 | Startups | "AI teammate" — PR review + fixes | Watch |

### Adjacent Competitors

| Adjacent Category | Player | Why They Could Enter | Likelihood | Signal to Watch |
|------------------|--------|---------------------|-----------|----------------|
| AI coding assistants | GitHub (Copilot) | Already in dev workflow, code understanding capabilities, massive distribution | High | Copilot PR review feature announcements |
| Static analysis | SonarQube | Existing enterprise install base, adding AI features | Medium | AI-powered analysis in release notes |
| Code search/intelligence | Sourcegraph (Cody) | Deep code understanding, could add review layer | Medium | "Code review" in job postings or roadmap |

### Feature Comparison

| Capability | Type | CodeRabbit | Sourcery | Codacy | Qodo | Ellipsis |
|-----------|------|-----------|---------|-------|------|---------|
| PR-level review | Stakes | ✅ | 🟡 | 🟡 | ✅ | ✅ |
| Auto-fix suggestions | Stakes | ✅ | ✅ | ❌ | ✅ | ✅ |
| Security scanning | Stakes | 🟡 | ❌ | ✅ | 🟡 | ❌ |
| Custom rules | Diff | ✅ | 🟡 | ✅ | ❌ | ❌ |
| Multi-repo context | Diff | ❌ | ❌ | ✅ | ❌ | ❌ |
| Self-hosted option | Diff | ❌ | ❌ | ✅ | ✅ | ❌ |
| Test generation | Diff | ❌ | ❌ | ❌ | ✅ | ❌ |

### Pricing

| Competitor | Free Tier | Entry Price | Mid Tier | Enterprise | Model |
|-----------|-----------|------------|----------|-----------|-------|
| CodeRabbit | Yes (public repos) | $12/seat/mo | $24/seat/mo | Custom | Per seat |
| Sourcery | Yes (limited) | $10/seat/mo | — | Custom | Per seat |
| Codacy | Yes (3 users) | $15/seat/mo | $30/seat/mo | Custom | Per seat |
| Qodo | Yes (individual) | $19/seat/mo | $39/seat/mo | Custom | Per seat |
| Ellipsis | Yes (public repos) | $20/repo/mo | — | N/A | Per repo |

### Positioning Map

​```
Enterprise ▲
           │  Codacy          Qodo
           │
           │     CodeRabbit
           │
           │  Sourcery    Ellipsis
           └──────────────────────────► AI-native
     Traditional                         (LLM-first)
​```

### Community & Mindshare

| Competitor | Community Size | Activity Level | Sentiment | Share of Voice |
|-----------|---------------|---------------|-----------|---------------|
| CodeRabbit | 5K+ GitHub stars, active Discord | ~15 posts/week | Positive | ~35% of category mentions |
| Qodo | 8K+ GitHub stars (CodiumAI legacy) | ~8 posts/week | Mixed — pivot confusion | ~25% |
| Codacy | Established but aging community | ~5 posts/week | Neutral | ~20% |
| Sourcery | Small but loyal Python community | ~3 posts/week | Positive | ~12% |
| Ellipsis | Nascent | ~1 post/week | Positive but thin | ~8% |

## Gaps & Opportunities

### Underserved Segments

| Segment | Current Options | Why Underserved | Demand Signal |
|---------|----------------|----------------|--------------|
| Regulated industries (healthcare, finance) | Codacy (legacy), manual review | AI tools require cloud; compliance blocks adoption | G2 reviews: "can't send code to cloud" |
| Monorepo / microservice teams | None adequate | Tools review PRs in isolation, miss cross-repo impact | r/programming: "doesn't understand our monorepo" |
| Solo devs / OSS maintainers | Free tiers (limited) | Priced for teams; solo pricing is afterthought | HN: "I'd pay $5/mo but not $12/seat for just me" |

### Feature Gaps

| Gap | User Need | Workarounds | Demand Evidence | Difficulty |
|-----|-----------|-------------|-----------------|-----------|
| Multi-repo context | Understand cross-service dependencies | Manual review + tribal knowledge | G2 requests, Reddit complaints | L |
| Review → test pipeline | Auto-generate regression tests from review findings | Write tests manually after review | r/ExperiencedDevs threads | L |
| Org-specific style rules | Enforce team conventions, not just lint rules | Custom linter configs + code review checklists | G2 feature requests for CodeRabbit, Codacy | M |
| False positive tuning | Reduce noise after initial setup | Manually dismiss + hope it learns | Common G2 complaint across all tools | M |
| IDE integration | Review feedback in editor, not just PR UI | Tab back and forth between PR and IDE | Sourcery has this; others lack it | S |

### Emerging Trends Not Addressed

| Trend | Incumbent Response | Opportunity Window | Evidence |
|-------|-------------------|-------------------|----------|
| On-prem LLMs (Llama, Mistral) viable for code | No AI-native tool offers self-hosted | 6-12 months | Open-weight model benchmarks matching GPT-4 on code tasks |
| Agentic coding workflows | Tools are passive reviewers, not active agents | 12-18 months | Devin, Cursor, Copilot Workspace setting expectations |
| Security-first DevOps | Most treat security as add-on, not core | 12-24 months | CISA secure-by-design push, SOC2 prevalence |

### Positioning White Space

| White Space | Description | Why Empty | Risk |
|-------------|------------|-----------|------|
| "AI code reviewer for regulated teams" | Self-hosted, compliance-first, SOC2/HIPAA-friendly | AI-native players prioritized cloud GTM; legacy players lack AI depth | Market may be too small for VC-scale returns |
| "Cross-repo intelligence platform" | Review + understand the full dependency graph | Technically hard — requires codebase-wide indexing | Engineering complexity; incumbents may catch up |

### Top 3 Opportunities

| # | Opportunity | Evidence Source | Window | Risk | Why Now |
|---|------------|---------------|--------|------|---------|
| 1 | **Multi-repo context awareness** — no tool understands cross-repo dependencies; reviews miss breaking changes | r/programming complaints, G2 reviews mentioning "doesn't understand our monorepo" | 12-18 months before leaders add this | Medium | Monorepo adoption growing; microservice sprawl creates cross-repo review need |
| 2 | **Self-hosted AI review for regulated industries** — healthcare, finance, gov need on-prem; only legacy tools offer it | Multiple G2 reviews: "love AI review but can't send code to cloud" | 6-12 months — compliance pressure increasing | Low | Open-weight LLMs now capable enough to run on-prem |
| 3 | **Review-to-test pipeline** — reviewers find issues but devs still write tests manually; close the loop | r/ExperiencedDevs: "AI review finds the bug but I still spend 30min writing the regression test" | 12-24 months | High | Only Qodo attempts this; execution is hard |

## Limitations & Confidence

| Aspect | Confidence | Justification |
|--------|-----------|---------------|
| Market sizing | Low | No reliable analyst report for this specific niche; extrapolated from broader DevOps tools market |
| Competitor data | Medium | Mix of public (Crunchbase) and estimated (team size from LinkedIn, pricing from websites) data |
| Gap identification | High | Strong demand signals from multiple independent communities (Reddit, G2, HN) |

**Data gaps:** No reliable TAM figure for AI code review specifically (only broader "code quality tools" market). Competitor revenue data is unavailable for all private companies. Community sentiment is English-language biased.

## Next Step

Run `solution-design` to turn the multi-repo context opportunity into a prioritized product initiative, or `icp-research` to build personas for the regulated-industry segment.
```

---

## Anti-Patterns

**Describing without concluding** — Listing competitors and features without identifying gaps and opportunities produces a Wikipedia article, not strategic intelligence. Step 4 (Gaps & Opportunities) is the point of this skill — everything before it is setup.

**Unsourced market sizing** — "The market is worth $5B" without citing a source or methodology is fiction. Every market size claim needs a source, methodology (top-down or bottom-up), and confidence level. See [references/market-sizing-guide.md](references/market-sizing-guide.md).

**Recency blindness** — Using a 2022 report to describe a 2026 market. In fast-moving categories, 18-month-old data is historical context, not current intelligence. Flag source dates prominently.

**Feature-only competitor analysis** — Comparing features while ignoring positioning, community, growth trajectory, and pricing produces an incomplete picture. A competitor with worse features but stronger community and better positioning is a bigger threat than a feature-rich product nobody uses.

**Confirmation bias in gap identification** — Reverse-engineering "gaps" from your product's features isn't research — it's rationalization. Identify gaps from user complaints, switching reasons, and unmet needs FIRST, then check if your product addresses them.

**Treating all competitors as equal threats** — A $40M-funded company with 200 employees targeting your exact segment is a different threat level than a side project on Product Hunt. Differentiate by funding, team size, growth signals, and segment overlap.

**Positioning map with wrong axes** — Axes should reflect dimensions that MATTER to buyers, not dimensions that make your product look good. Validate axis choices against what users actually compare when switching.

**Ignoring adjacent competitors** — The biggest competitive threat often comes from an adjacent category expanding into yours, not from a direct competitor. Check: who could add this capability easily?

---

## References

- [references/competitor-analysis-framework.md](references/competitor-analysis-framework.md) — Structured competitor evaluation methodology
- [references/market-sizing-guide.md](references/market-sizing-guide.md) — TAM/SAM/SOM methods and search patterns
- [references/gap-analysis-template.md](references/gap-analysis-template.md) — Framework for opportunity identification and scoring
