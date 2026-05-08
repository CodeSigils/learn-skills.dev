---
name: seo
description: "Audits and plans search visibility — keyword research, on-page optimization, technical SEO, link building strategy, and AI search optimization. Produces `.agents/mkt/seo-[mode].md`. Not for landing page conversion (use lp-optimization) or writing copy (use copywriting)."
argument-hint: "[url or mode]"
allowed-tools: Read Grep Glob Bash WebSearch WebFetch
license: MIT
metadata:
  author: hungv47
  version: "2.0.0"
  budget: deep
  estimated-cost: "$2-5"
promptSignals:
  phrases:
    - "seo audit"
    - "keyword research"
    - "search ranking"
    - "search optimization"
    - "app store optimization"
    - "aso"
  allOf:
    - [seo, audit]
    - [keyword, research]
  anyOf:
    - "seo"
    - "keyword"
    - "ranking"
    - "backlink"
    - "search"
    - "aso"
    - "aeo"
  noneOf:
    - "landing page audit"
    - "cro"
  minScore: 6
routing:
  intent-tags:
    - seo-audit
    - ai-seo
    - programmatic-seo
    - keyword-research
    - search-optimization
    - competitor-seo
    - aso
    - app-store-optimization
    - marketplace-seo
    - aeo
    - agent-engine-optimization
  position: horizontal
  produces:
    - mkt/seo-[mode].md
    # mode = audit | ai | programmatic | competitor | aso
  consumes:
    - product-context.md
    - icp-research.md
    - mkt/campaign-plan.md
  requires: []
  defers-to:
    - skill: copywriting
      when: "need to write headlines/copy for SEO-targeted pages"
    - skill: lp-optimization
      when: "optimizing for conversion, not search"
  parallel-with:
    - lp-optimization
  interactive: false
  estimated-complexity: heavy
---

# SEO — Orchestrator

*Communication — Horizontal. Covers the full SEO surface: technical foundations, AI/agent engine optimization, programmatic page generation, and competitor comparison content.*

**Core Question:** "How do we get found — by both search engines and AI models?"

## Philosophy

SEO mixes hard technical constraints (CWV thresholds, character limits) with strategic judgment. Platform specs are constraints; strategic recommendations are defaults with deviation context.

---

## Critical Gates

Before delivering, all must hold:

1. **Every recommendation names exact page, exact change, expected impact.** No "consider" / "you might."
2. **AI SEO is additive, not alternative.** No point optimizing for AI citations if crawlers can't reach content.
3. **Source recency.** AI platform behavior shifts fast — verify no deprecated practices, outdated crawlers, stale metrics.
4. **Mode is diagnosis-driven**, not a generic "do SEO" deliverable.

---

## Agent Manifest

| Agent | File | Layer | Mode(s) | Focus |
|-------|------|-------|---------|-------|
| crawl-agent | `agents/crawl-agent.md` | 1 (parallel) | Technical Audit, Full | Crawlability, indexation, robots.txt, sitemaps, canonicals |
| foundations-agent | `agents/foundations-agent.md` | 1 (parallel) | Technical Audit, Full | CWV, mobile, HTTPS, URL structure, on-page optimization |
| content-quality-agent | `agents/content-quality-agent.md` | 1 (parallel) | Technical Audit, Full | E-E-A-T, thin content, duplicate detection, content gaps |
| authority-agent | `agents/authority-agent.md` | 1 (parallel) | Technical Audit, Full | Backlink profile, internal linking, link equity |
| ai-structure-agent | `agents/ai-structure-agent.md` | 1 (parallel) | AI SEO, Full | Schema, heading hierarchy, answer passages, structured data |
| ai-presence-agent | `agents/ai-presence-agent.md` | 1 (parallel) | AI SEO, Full | AI crawler access, llms.txt, citation monitoring, AEO |
| programmatic-template-agent | `agents/programmatic-template-agent.md` | 1 (parallel) | Programmatic | Template design, URL architecture, defensibility |
| programmatic-quality-agent | `agents/programmatic-quality-agent.md` | 1 (parallel) | Programmatic | Thin page detection, quality gates, monitoring plan |
| comparison-page-agent | `agents/comparison-page-agent.md` | 1 (parallel) | Competitor Pages | Page format, content architecture, comparison matrices |
| aso-keyword-agent | `agents/aso-keyword-agent.md` | 1 (parallel) | ASO | Keyword research for App Store, Play Store, G2, Capterra |
| aso-listing-agent | `agents/aso-listing-agent.md` | 1 (parallel) | ASO | Title, subtitle, description, screenshots, preview video optimization |
| aso-reviews-agent | `agents/aso-reviews-agent.md` | 1 (parallel) | ASO | Review sentiment analysis, response templates, rating improvement |
| aso-competitive-agent | `agents/aso-competitive-agent.md` | 1 (parallel) | ASO | Competitor listing comparison, feature matrix positioning |
| prioritization-agent | `agents/prioritization-agent.md` | 2 (sequential) | All | Impact x effort ranking of all findings |
| critic-agent | `agents/critic-agent.md` | 2 (sequential) | All | Quality gate — specific fixes, no vague language, actionability |

---

## Inputs Required

- ICP research from `research/icp-research.md` (audience questions, pain points, search behavior)
- IMC plan from `.agents/mkt/campaign-plan.md` (content pillars and angles)
- OR: User describes their SEO situation / site to audit

## Output

- `.agents/mkt/seo-[mode].md` (mode = audit | ai | programmatic | competitor | aso)

---

## Pre-Dispatch

Run the Pre-Dispatch protocol (`meta-skills/references/pre-dispatch-protocol.md`).

**Needed dimensions:** mode (audit / ai / programmatic / competitor / aso), site or property (domain or app store listing), audience, geographic + language scope.

**Read order:**
1. Pipeline: `research/icp-research.md` for audience + search behavior. `.agents/mkt/campaign-plan.md` for pillars/angles. `research/product-context.md` for category context.
2. Experience: `.agents/experience/{audience,product,business}.md`.

**Warm Start** (mode + site supplied, audience known):

```
Found:
- mode → "[audit | ai | programmatic | competitor | aso]"
- site → "[domain]"
- audience → "[from icp-research.md]"

Need before dispatching: geographic + language scope (US-en / global / specific)?
```

**Cold Start** (mode unclear or no audience context):

```
seo runs in 4 modes — each dispatches different agents. Pick the mode first:

1. **Mode** — pick one:
   - **audit** — technical foundations + Core Web Vitals + on-page review
   - **ai** — AI/agent engine optimization (LLMs as discovery channel)
   - **programmatic** — page templates for high-volume keyword targeting
   - **competitor** — comparison content + share-of-voice analysis
   - **aso** — App Store Optimization (Apple App Store + Google Play)
2. **Site or property** — domain (for audit/ai/programmatic/competitor)
   OR app store listing URL (for aso).
3. **Audience** — primary buyer + their search behavior. Or point me at
   `research/icp-research.md` if it exists.
4. **Geographic + language scope** — US-en / global-en / multi-language /
   specific market (e.g., "VN, north dialect, Tiếng Việt").

Answer 1-4 in one response. I'll dispatch the agents for that mode.
```

**Write-back:**

| Q | File | Key |
|---|---|---|
| 3. Audience (if novel) | `audience.md` | `Audience — search behavior` |
| 4. Geo + language | `audience.md` | `Audience — geo + language scope` |
| 1, 2. Mode + site | (run-specific, not persisted) |

## Chain Position

Previous: `icp-research` + `campaign-plan` | Next: content production / site updates / re-audit after 30 days. Horizontal — invokable independently or post-IMC.

**Re-run triggers:** Technical audit quarterly, AI SEO monthly, after Google core updates, when entering new keyword territories.

### Skill Deference
- **Production copy for comparison pages?** → `copywriting` after SEO defines structure/keywords.
- **Content pillar prioritization?** → `campaign-plan` for audience-driven; SEO supplies search demand.

### Coordination with IMC Plan

| Situation | Who Leads | How They Coordinate |
|-----------|----------|-------------------|
| Pillar has search demand | SEO leads topic | IMC provides angles/audience language; SEO provides keyword clusters/structure |
| Pillar is novel/contrarian | IMC leads topic | IMC creates shareable content; SEO optimizes related informational queries |
| Content needs both reach types | Both | Tag angles Searchable/Shareable in IMC; SEO optimizes searchable for AI+traditional |
| Competitor comparisons | IMC leads prioritization | IMC picks which/when; SEO owns technical optimization (schema, structure, internal linking) |

**Rule:** Don't let SEO keyword data override IMC audience insights (or vice versa). Best content addresses real audience pain (IMC) AND has search demand (SEO). On conflict, audience pain wins — non-search channels can promote great content, but ranking can't make irrelevant content convert.

---

## Before Starting

### Step 0: Product Context
Read `research/product-context.md` if present. If `icp-research.md` or `campaign-plan.md` `date` fields exceed 30 days, recommend re-running upstream — stale audience data weakens strategy.

### Required Artifacts
| Artifact | Source | If Missing |
|----------|--------|------------|
| `icp-research.md` | icp-research | **RECOMMENDED.** Audience search behavior drives strategy. Proceed without is allowed but less targeted. |

### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `campaign-plan.md` | campaign-plan | Content pillars inform topic clusters |
| `product-context.md` | icp-research | Product positioning context |

---

## Routing Logic — Mode-Based Dispatch

### Step 1: Determine Mode

Diagnose first, then enter the right mode.

| Situation | Mode | Route |
|-----------|------|-------|
| Technical issues / traffic dropped / never audited | **Technical Audit** | Route A |
| Want citations from ChatGPT / Perplexity / AI search | **AI SEO (AEO)** | Route B |
| Structured data, want to generate pages at scale | **Programmatic SEO** | Route C |
| Rank for competitor comparison queries | **Competitor Pages** | Route D |
| Comprehensive SEO strategy | **Full SEO** (Technical + AI) | Route E |
| Distribute via app stores / listings (App Store, Play Store, G2, Capterra, Product Hunt) | **ASO** | Route F |

Modes can run sequentially. Start with Technical Audit if never audited — no point optimizing for AI citations if crawlers can't reach content.

### Step 2: Dispatch per Route

**Route A — Technical Audit:**
```
Layer 1 (parallel): crawl-agent + foundations-agent + content-quality-agent + authority-agent
       ↓ merge
Layer 2 (sequential): prioritization-agent → critic-agent
```

**Route B — AI SEO:**
```
Layer 1 (parallel): ai-structure-agent + ai-presence-agent
       ↓ merge
Layer 2 (sequential): prioritization-agent → critic-agent
```

**Route C — Programmatic SEO:**
```
Layer 1 (parallel): programmatic-template-agent + programmatic-quality-agent
       ↓ merge
Layer 2 (sequential): prioritization-agent → critic-agent
```

**Route D — Competitor Pages:**
```
Layer 1: comparison-page-agent
       ↓
Layer 2 (sequential): prioritization-agent → critic-agent
```

**Route E — Full SEO (Technical + AI combined):**
```
Layer 1 (parallel): crawl-agent + foundations-agent + content-quality-agent + authority-agent + ai-structure-agent + ai-presence-agent
       ↓ merge
Layer 2 (sequential): prioritization-agent → critic-agent
```

**Route F — ASO (App Store Optimization):**
```
Layer 1 (parallel): aso-keyword-agent + aso-listing-agent + aso-reviews-agent + aso-competitive-agent
       ↓ merge
Layer 2 (sequential): prioritization-agent → critic-agent
```

---

## Dispatch Protocol

### Multi-Agent Dispatch (default)

1. **Gather context:** Read product-context, icp-research, campaign-plan. Identify site type, CMS/framework, known issues.
2. **Determine mode:** Apply the Step 1 routing table. Ask if unclear; "comprehensive SEO" → Route E.
3. **Prepare pre-writing object:**
   ```
   {
     site_url: "[URL]",
     site_type: "[SaaS / E-commerce / Content-Blog / Local / Hybrid]",
     cms_framework: "[WordPress / Next.js / Webflow / etc.]",
     mode: "[audit / ai / programmatic / competitor / aso / full]",
     known_issues: "[user-mentioned issues]",
     icp_data: "[audience questions, pains from icp-research]",
     competitors: "[competitor domains]",
     brand_name: "[brand]",
     category: "[product category for AI search testing]"
   }
   ```
4. **Dispatch Layer 1 agents** in parallel with the pre-writing object and absolute reference paths.
5. **Merge Layer 1 outputs** into the artifact template — each agent maps to designated sections.
6. **Dispatch prioritization-agent** with the merged doc.
7. **Dispatch critic-agent** with the prioritized doc.
8. **Apply verdict:** PASS → deliver. FAIL → re-dispatch named agents with feedback (max 2 cycles).

### Single-Agent Fallback

If multi-agent dispatch is unavailable:

1. Read this SKILL.md fully (including referenced sections)
2. Read reference files for the active mode
3. Follow the mode's audit steps (in Reference Knowledge sections)
4. Quality gate: every finding has Issue, Impact, Evidence, Fix, Priority
5. Produce the artifact using the template below

---

## Layer 1: Mode-Specific Agents

Domain knowledge lives in agent files. Orchestrator dispatches; agents hold techniques, checklists, anti-patterns.

| Mode | Agents | Domain Focus |
|------|--------|-------------|
| Technical Audit | crawl-agent, foundations-agent, content-quality-agent, authority-agent | Crawlability, CWV, E-E-A-T, backlinks — top-down audit layering |
| AI SEO (AEO) | ai-structure-agent, ai-presence-agent | Structure for AI citation + AI crawler access. **ai-structure-agent** targets: 40-60 word answer passages per key question, FAQ/HowTo/speakable schema, heading hierarchy matching user questions, comparison content (33% of AI citations), citation-optimized content types. **ai-presence-agent** targets: AI crawler access (GPTBot, ClaudeBot, PerplexityBot, GoogleOther in robots.txt), llms.txt implementation, citation monitoring across ChatGPT/Perplexity/Gemini, third-party presence optimization (6.5x more AI citations from G2/Capterra/publications than owned content) |
| Programmatic SEO | programmatic-template-agent, programmatic-quality-agent | Scalable page templates, data defensibility, quality gates |
| Competitor Pages | comparison-page-agent | Page format selection, content architecture, comparison matrices |
| ASO | aso-keyword-agent, aso-listing-agent, aso-reviews-agent, aso-competitive-agent | App Store / Play Store keyword research, listing optimization (title, subtitle, description, screenshots), review management and sentiment analysis, competitor listing comparison. Also covers marketplace SEO for G2, Capterra, Product Hunt, Trustpilot — profile completeness scoring, review velocity, category ranking factors |

**Reference files** (passed to agents at dispatch, not read by orchestrator):
- `references/technical-audit.md` — Full audit template and checklists
- `references/ai-seo.md` — Platform-specific AI optimization, citation data, AEO techniques (answer passages, AI crawler access, structured data, freshness signals)
- `references/programmatic-seo.md` — pSEO template patterns and implementation
- `references/competitor-pages.md` — Comparison page templates and keyword targeting
- `references/schema-reference.md` — Schema types, implementation contexts, validation
- `references/aso.md` — App Store / Play Store + marketplace SEO (G2, Capterra, Product Hunt) — keyword research, listing optimization, review management, competitive analysis

**Single-agent fallback principle:** Read the active mode's reference files, follow documented steps, apply the quality gate (Issue, Impact, Evidence, Fix, Priority).

---

## Layer 2: Prioritization and Critic

### Prioritization (all modes)

**prioritization-agent** ranks all Layer 1 findings into one action plan:

1. **Quick Wins** (High Impact, Low Effort) — execute first
2. **Strategic Investments** (High, High) — plan next
3. **Low-Hanging Fruit** (Medium, Low) — fill gaps
4. **Backlog** (Low or High Effort) — defer

Phases: P1 (Week 1-2), P2 (Month 1), P3 (Month 2-3), P4 (Ongoing). Dependencies mapped — no action recommended before its prerequisite.

### Critic Gate (all modes)

**critic-agent** evaluates against:

- Every finding has Issue, Impact, Evidence, Fix
- Every Fix is implementable without further research
- No vague language ("consider," "might want to," "could potentially")
- Actions force-ranked (not flat "High priority" lists)
- Mode-appropriate coverage complete
- Technical specs cite correct thresholds

**Verdict:** PASS or FAIL (binary). **Max:** 2 rewrites; after that, deliver with unresolved-items note. On FAIL, critic names the agent to re-dispatch with fix instructions.

---

## Artifact Template

```markdown
---
skill: seo
mode: [audit | ai | programmatic | competitor | aso]
version: 1
date: [today's date]
status: done | done_with_concerns | blocked | needs_context
---

# SEO: [Mode Name]

**Date:** [today]
**Skill:** seo
**Mode:** [Technical Audit | AI SEO | Programmatic SEO | Competitor Pages | ASO]
**Product:** [from product-context.md]

## Diagnosis

[Why this mode was chosen. What's the current situation?]

## Findings

[Mode-specific findings from Layer 1 agents — merged by section]

### [Section from Agent 1]
[Agent 1's findings]

### [Section from Agent 2]
[Agent 2's findings]

[Continue for all Layer 1 agents in the active mode]

## Priority Actions

| # | Action | Category | Impact | Effort | Timeline |
|---|--------|----------|--------|--------|----------|
| 1 | [action] | Quick Win | H | L | [timeline] |
| 2 | [action] | Strategic | H | H | [timeline] |

## Implementation Plan

### Phase 1: Immediate (Week 1-2)
[Quick wins]

### Phase 2: Short-term (Month 1)
[Strategic investments]

### Phase 3: Medium-term (Month 2-3)
[Remaining items]

### Phase 4: Ongoing
[Maintenance and monitoring]

## Dependencies

| Action | Depends On | Why |
|--------|-----------|-----|
| [action] | [prerequisite] | [reason] |

## Metrics to Track

| Metric | Current | Target | Check Frequency |
|--------|---------|--------|----------------|
| [metric] | [value] | [value] | [frequency] |

## Next Step

[What to do after implementing — re-audit timeline, experiment to run, etc.]

> On re-run: rename existing artifact to `seo-[mode].v[N].md` and create new with incremented version.
```

---

## Worked Example: Technical Audit (Route A)

**Scenario:** SaaS company, Next.js site, first SEO audit. User says "Our organic traffic dropped 30% last quarter."

**Step 1: Mode determination** → Technical Audit (traffic drop + never audited = Route A)

**Step 2: Context gathering**
```
pre-writing: {
  site_url: "https://example.com",
  site_type: "SaaS",
  cms_framework: "Next.js",
  mode: "audit",
  known_issues: "30% organic traffic drop last quarter",
  icp_data: "from research/icp-research.md",
  competitors: ["competitor-a.com", "competitor-b.com"]
}
```

**Step 3: Layer 1 dispatch (parallel)**

*crawl-agent finds:*
```
- Issue: robots.txt line 8 blocks /resources/ (47 indexed guides)
- Impact: 47 guide pages deindexed, ~2,300 sessions/month lost
- Fix: Replace Disallow: /resources/ with Disallow: /resources/internal/
- Priority: Critical
```

*foundations-agent finds:*
```
- Issue: LCP is 4.2s on /pricing (hero image 2.4MB PNG)
- Impact: Fails CWV (threshold: <2.5s), poor mobile experience on highest-intent page
- Fix: Convert hero.png to WebP via next/image, add priority loading. Expected: ~180KB, LCP <2s.
- Priority: Critical
```

*content-quality-agent finds:*
```
- Issue: 23 integration pages average 142 words unique content each
- Impact: Helpful Content Update risk — thin pSEO pages can drag down domain quality
- Fix: Add 2-3 unique workflows + setup steps per integration page. Target 600+ unique words.
- Priority: High
```

*authority-agent finds:*
```
- Issue: /pricing has 0 internal links from blog posts (12 posts mention pricing)
- Impact: Highest-intent page has no internal link equity from content
- Fix: Add contextual links to /pricing from 12 blog posts that mention pricing
- Priority: Medium
```

**Step 4: Merge + prioritization-agent**

Quick Wins:
1. Fix robots.txt /resources/ block (Critical, 5 minutes)
2. Add internal links to /pricing from 12 blog posts (Medium impact, 2 hours)

Strategic Investments:
3. Convert hero images to WebP across site (Critical, 1-2 days)
4. Enrich 23 integration pages with unique content (High, 2-3 weeks)

**Step 5: critic-agent evaluates** → PASS (every finding has specific fix, no vague language, priorities are ranked)

**Step 6: Deliver** `.agents/mkt/seo-audit.md`

---

## Anti-Patterns

**"Do SEO" without diagnosis** — Generic checklist without identifying technical vs content vs authority vs AI visibility. Different problems, different modes.
INSTEAD: Diagnose via the routing table. Ask what triggered the request.

**Keyword stuffing (traditional or AI)** — Cuts AI visibility ~10% (Princeton GEO/AEO study) and triggers Google spam detection.
INSTEAD: Write for humans, structure for machines. Natural-language headings matching audience questions.

**pSEO as a content farm** — Thousands of thin pages, no unique per-page value. Helpful Content Update targets this.
INSTEAD: 100 great pages beat 10,000 thin ones. Enforce 60% uniqueness threshold.

**Ignoring third-party presence for AI SEO** — Optimizing only own site. Third-party drives 6.5x more AI citations.
INSTEAD: Build G2/Capterra profiles, pursue industry mentions, manage review responses.

**Blocking AI crawlers then expecting citations** — GPTBot blocked → ChatGPT can't cite.
INSTEAD: Audit robots.txt for all 5 AI crawler directives. Allow crawlers for target platforms.

**Flat competitor comparison tables** — Checkmark feature lists give no context.
INSTEAD: Compare by use case and audience. Cells carry specific data, not checkmarks.

**Schema false positives** — Flagging missing schema from raw HTML when CMS plugins inject JSON-LD client-side.
INSTEAD: Verify with Google Rich Results Test or browser DevTools.

**One-and-done audits** — SEO is ongoing; issues resurface, competitors shift, algorithms update.
INSTEAD: Quarterly technical re-audit; monthly AI visibility.

**"Consider improving" recommendations** — Hedge language gives nothing to act on.
INSTEAD: Every recommendation names exact page, exact change, expected impact.

---

## Completion Status

Every run ends with explicit status:
- **DONE** — selected mode (audit / ai / programmatic / competitor / aso) executed end-to-end, recommendations specific and prioritized, critic PASS
- **DONE_WITH_CONCERNS** — analysis delivered but with data gaps (rank tracker unavailable, GSC not connected, competitor data scraped at low confidence); recommendations annotated
- **BLOCKED** — site/property inaccessible (auth wall, robots block, no URL provided); cannot scan
- **NEEDS_CONTEXT** — audience or product context missing for relevance scoring; recommend `icp-research` or proceed with explicit scope reduction

---

## References

Agent instruction files and reference catalogs live in `agents/` and `references/`. See the Agent Manifest for the complete inventory.
