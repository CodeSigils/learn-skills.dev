---
name: seo
description: "This skill should be invoked when the user wants to improve search visibility or organic traffic. Triggers include 'how do I rank for...', 'keyword research', 'link building', 'site speed', 'nobody can find us online', 'how do I get more organic traffic', 'competitors outrank us', 'SEO audit', 'show up in AI answers', 'show up on ChatGPT', 'blog isn't driving leads', 'nobody reads our blog', or 'we write content but get no traffic from it' -- even if they just say 'we're invisible on Google', 'how do I build domain authority', or paste a URL and ask 'why aren't we ranking.' Not for landing page conversion (use lp-optimization), writing the actual blog or comparison page content (use content-create), or paid advertising and social media strategy (use imc-plan)."
argument-hint: "[url or mode]"
license: MIT
metadata:
  author: hungv47
  version: "1.0.1"
---

# SEO

*Communicate Track — Horizontal skill. Covers the full SEO surface: technical foundations, AI/generative engine optimization, programmatic page generation, and competitor comparison content.*

**Core Question:** "How do we get found — by both search engines and AI models?"

## Philosophy

SEO combines hard technical constraints (Google's CWV thresholds, character limits) with strategic judgment. This skill distinguishes between the two. Technical specs from platform documentation are constraints. Strategic recommendations are defaults with context for when to deviate.

## Inputs Required
- ICP research from `.agents/mkt/icp-research.md` (audience questions, pain points, search behavior)
- IMC plan from `.agents/mkt/imc-plan.md` (content pillars and angles)
- OR: User describes their SEO situation / site to audit

## Output
- `.agents/mkt/seo-[mode].md` (mode = audit | ai | programmatic | competitor)

## Quality Gate
Before delivering, verify:
- [ ] Mode is explicitly chosen based on diagnosis — not a generic "do SEO" deliverable
- [ ] Every recommendation traces to a specific principle (not generic "optimize for keywords")
- [ ] Technical issues are prioritized by impact, not listed as a flat checklist
- [ ] AI SEO recommendations are platform-specific (not just "optimize for AI")
- [ ] Programmatic SEO pages each deliver unique value (not variable substitution into a template)
- [ ] Schema markup recommendations account for CMS/framework context (static vs. dynamic vs. plugin)

## Chain Position
Previous: `icp-research` + `imc-plan` (reads audience questions and content pillars) | Next: content production / site updates / `experiment` (to test SEO changes)

Horizontal skill — can be invoked independently or after IMC planning.

**Re-run triggers:** Technical audit quarterly, AI SEO monthly (AI landscape changes fast), after Google core updates, when entering new keyword territories.

### Skill Deference
- **Need production-quality copy for comparison pages?** → Run `content-create` after SEO defines the page structure and keyword targets.
- **Content pillar prioritization?** → Defer to `imc-plan` for audience-driven prioritization; SEO provides search demand data.

### Coordination with IMC Plan

When both `seo` and `imc-plan` are in use, they should coordinate:

| Situation | Who Leads | How They Coordinate |
|-----------|----------|-------------------|
| Content pillar has search demand | SEO leads topic selection | IMC provides angles and audience language; SEO provides keyword clusters and structure |
| Content pillar is novel/contrarian | IMC leads topic selection | IMC creates shareable content; SEO optimizes for related informational queries |
| Existing content needs both reach types | Both | Tag angles as Searchable/Shareable in IMC; SEO optimizes searchable angles for AI+traditional |
| Angles include competitor comparisons | IMC leads prioritization | IMC decides which comparisons to produce and when; SEO owns technical optimization (schema, structure, internal linking) of those pages |

**Rule:** Don't let SEO keyword data override IMC audience insights or vice versa. The best content addresses a real audience pain (IMC) AND has search demand (SEO). When they conflict, audience pain wins — you can promote great content through non-search channels, but you can't make irrelevant content convert even if it ranks.

---

## Before Starting

### Step 0: Product Context
Check for `.agents/product-context.md`. If available, read for product positioning context.
If `.agents/mkt/icp-research.md` or `.agents/mkt/imc-plan.md` `date` fields are older than 30 days, recommend re-running upstream skills — stale audience data weakens SEO strategy.

### Required Artifacts
| Artifact | Source | If Missing |
|----------|--------|------------|
| `icp-research.md` | icp-research | **RECOMMENDED.** Audience search behavior drives SEO strategy. Can proceed without, but recommendations will be less targeted. |

### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `imc-plan.md` | imc-plan | Content pillars inform topic clusters |
| `product-context.md` | icp-research | Product positioning context |

---

## Step 1: SEO Diagnosis

Not every SEO problem needs the same solution. Diagnose first, then enter the right mode.

| Situation | Mode | Go To |
|-----------|------|-------|
| "Our site has technical issues / traffic dropped / we've never done an SEO audit" | **Technical Audit** | Step 2A |
| "We want to be cited by ChatGPT / Perplexity / AI search engines" | **AI SEO (GEO)** | Step 2B |
| "We have structured data and want to generate pages at scale" | **Programmatic SEO** | Step 2C |
| "We want to rank for competitor comparison queries" | **Competitor Pages** | Step 2D |
| "We need a comprehensive SEO strategy" | **Full audit first** → then prioritize modes | Step 2A, then others as needed |

Multiple modes can run sequentially. Start with Technical Audit if the site has never been audited — no point optimizing for AI citations if crawlers can't reach your content.

---

## Step 2A: Technical SEO Audit

Audit the site's SEO foundations in priority order. Fix blockers before optimizing content.

### Audit Priority Layers

Work top-down — lower layers depend on upper layers being healthy:

```
Layer 1: Crawlability & Indexation (can search engines find your pages?)
Layer 2: Technical Foundations (is the site fast, mobile-friendly, secure?)
Layer 3: On-Page Optimization (are pages targeting the right queries?)
Layer 4: Content Quality (is the content worth ranking?)
Layer 5: Authority & Links (does the site have external credibility?)
```

### Layer 1: Crawlability & Indexation
- [ ] `robots.txt` is not blocking important pages
- [ ] XML sitemap exists, is submitted, and matches actual site pages
- [ ] No orphaned pages (pages with no internal links pointing to them)
- [ ] Important pages are reachable within 3 clicks from homepage
- [ ] Canonical tags are correct (no self-referencing loops or wrong targets)
- [ ] No duplicate content issues (www vs non-www, HTTP vs HTTPS, trailing slashes)
- [ ] Crawl budget is not wasted on low-value pages (paginated archives, tag pages, search results)

### Layer 2: Technical Foundations
- [ ] Core Web Vitals pass: LCP < 2.5s, INP < 200ms, CLS < 0.1 (Google's official thresholds — not adjustable)
- [ ] Mobile-friendly (responsive, no horizontal scroll, touch targets ≥44px)
- [ ] HTTPS everywhere (no mixed content)
- [ ] URL structure is clean (lowercase, hyphenated, human-readable, no over-nesting)
- [ ] 404 errors handled (custom page, no broken internal links)
- [ ] Redirects are clean (no chains, no loops, 301 for permanent moves)
- [ ] Page speed: load time < 3s on mobile

### Layer 3: On-Page Optimization
- [ ] Title tags: 50-60 characters, include primary keyword, unique per page (display limits set by search engines — content beyond gets truncated)
- [ ] Meta descriptions: 150-160 characters, include CTA, unique per page (display limits set by search engines — content beyond gets truncated)
- [ ] H1: one per page, includes primary keyword
- [ ] H2/H3 hierarchy: logical, covers subtopics, matches search intent
- [ ] Primary keyword appears in first 100 words
- [ ] Images: descriptive alt text, compressed (WebP), lazy-loaded below fold
- [ ] Internal links: 5-10 contextual links per 1,000 words, descriptive anchor text
- [ ] No keyword cannibalization (multiple pages targeting the same query)

### Layer 4: Content Quality (E-E-A-T)

| Signal | What to Check |
|--------|--------------|
| **Experience** | Does the content show first-hand experience? (Case studies, screenshots, personal results) |
| **Expertise** | Is the author credible for this topic? (Named author, credentials, bio) |
| **Authoritativeness** | Is the site recognized in this space? (Mentions, citations, awards) |
| **Trustworthiness** | Can users trust this site? (HTTPS, clear contact info, privacy policy, accurate claims) |

### Layer 5: Authority & Links
- [ ] Backlink profile: quality over quantity (relevant domains > random directories)
- [ ] No toxic backlinks (spammy sites, link farms)
- [ ] Internal linking creates clear topic clusters
- [ ] Key pages have sufficient incoming internal links

### Site-Type-Specific Issues

| Site Type | Watch For |
|-----------|----------|
| **SaaS** | Pricing page indexation, feature page cannibalization, documentation vs. marketing SEO conflict |
| **E-commerce** | Faceted navigation creating duplicate pages, out-of-stock page handling, product schema |
| **Content/Blog** | Thin content, category/tag page bloat, author page optimization |
| **Local Business** | Google Business Profile accuracy, NAP consistency, local schema |

**Schema detection caveat:** Web fetching / curl cannot reliably detect JSON-LD schema because CMS plugins (Yoast, AIOSEO, RankMath) often inject it via client-side JavaScript. Use Google Rich Results Test or browser DevTools to verify schema presence — don't flag missing schema based on raw HTML alone.

See [references/technical-audit.md](references/technical-audit.md) for the full audit report template.

---

## Step 2B: AI SEO (Generative Engine Optimization)

Traditional SEO = ranked in results. AI SEO = cited in AI-generated answers. Different systems, different rules.

### The Three Pillars of AI Visibility

#### Pillar 1: Structure (Make Content Citable)

AI models extract and cite content that's structured for easy parsing.

| Rule | Why | How |
|------|-----|-----|
| Clear H2/H3 hierarchy | AI models parse headings to understand topic structure | Every section answers one specific question |
| 40-60 word answer passages (typical — adjust for topic complexity: simple definitions may need 20-30 words; technical explanations may need 80-100) | Citation-length sweet spot — long enough to be useful, short enough to quote in full | Write a concise answer paragraph immediately after each H2 |
| Comparison tables | Comparisons are #1 most-cited content type (33% of AI citations) | Use tables for feature comparisons, pricing tiers, tool comparisons |
| Source citations in content | Citing sources is the **strongest single factor** for AI visibility — +40% citation boost (Princeton GEO study) | Link to primary sources, studies, data |
| Statistics in content | +37% citation boost | Include specific numbers, percentages, data points |

**Most-Cited Content Types:**
1. Comparisons — 33% (X vs Y, best tools for Z)
2. How-to guides — 15% (step-by-step instructions)
3. Original research — 12% (proprietary data, surveys)
4. Definitions/explainers — 10% (what is X, how X works)
5. Lists/roundups — 8% (top N, best practices)

**Princeton GEO Study — optimization impact on AI citations:**

| Optimization | Citation Impact |
|-------------|----------------|
| Citing sources | +40% |
| Including statistics | +37% |
| Including quotations | +30% |
| Authoritative tone | +25% |
| Clarity of writing | +20% |
| Technical terminology (appropriate) | +18% |
| Unique vocabulary | +15% |
| Fluency | +15-30% |
| Keyword stuffing | **-10%** (hurts) |

#### Pillar 2: Authority (Be Worth Citing)

| Signal | Impact | Action |
|--------|--------|--------|
| Third-party mentions | Brands cited 6.5x more via third-party sources than their own content | Get mentioned in industry publications, review sites, expert roundups |
| Original data | AI models heavily cite proprietary data | Publish original research, surveys, benchmarks with specific numbers |
| Expert attribution | Named experts increase citation likelihood | Attribute content to real people with credentials |
| Review site presence | G2, Capterra, TrustRadius feed AI training data | Actively manage review profiles |
| Wikipedia presence | 7.8% of ChatGPT citations come from Wikipedia | Contribute to relevant Wikipedia articles (following their guidelines) |

#### Pillar 3: Presence (Be Findable by AI)

**AI Crawler Management:**

| Crawler | AI Engine | robots.txt Directive |
|---------|-----------|---------------------|
| GoogleOther | Google AI Overviews | `User-agent: GoogleOther` |
| GPTBot | ChatGPT | `User-agent: GPTBot` |
| ClaudeBot | Claude | `User-agent: ClaudeBot` |
| PerplexityBot | Perplexity | `User-agent: PerplexityBot` |
| Bingbot | Microsoft Copilot | `User-agent: Bingbot` |

Decision: If you want AI citations, allow the crawlers. If GPTBot is blocked, ChatGPT won't cite you.

**Platform-Specific Focus:**

| Platform | Data Source | Optimization Priority |
|----------|-----------|----------------------|
| Google AI Overviews | Traditional search index + schema | Schema markup, featured snippets, E-E-A-T |
| ChatGPT | Bing + GPTBot + training data | Third-party mentions, original data, entity consistency |
| Perplexity | Own crawler + Bing | Source citations in content, comparison tables, freshness |
| Claude | Training data + ClaudeBot | Expert content, balanced analysis, original research |
| Gemini | Google index + Knowledge Graph | Google Business Profile, YouTube, schema |

### AI SEO Audit Steps

1. **Direct testing:** Query your brand + key topics across ChatGPT, Perplexity, Google AI Overviews, Claude. Document: mentioned? cited? accurate?
2. **Structure audit:** Do top pages have H2/H3 hierarchy, 40-60 word answer passages, comparison tables, source citations?
3. **Authority audit:** Third-party mentions, review site presence, expert attribution, original data published?
4. **Crawler audit:** robots.txt directives for AI bots, sitemap accessibility, server log activity?

### AI SEO Validation Protocol

Optimization without validation is guesswork. Track whether changes actually improve AI citations:

**Baseline (before optimization):**
1. Pick 10-20 queries: 5 brand queries, 5 category queries, 5 "how to" queries from ICP research
2. Run each across ChatGPT, Perplexity, Google AI Overviews, Claude
3. Score each: 0 = not mentioned, 1 = mentioned but not cited, 2 = cited with link/attribution
4. Record total baseline score (max = queries × platforms × 2)

**Post-optimization (re-test weekly for 4 weeks):**
1. Run the same 10-20 queries on the same platforms
2. Score identically
3. Track delta from baseline

| Outcome | Interpretation | Action |
|---------|---------------|--------|
| Score improves >20% in 4 weeks | Optimization working | Continue and expand to more content |
| Score flat after 4 weeks | Wrong optimization target | Re-diagnose: is the issue Structure, Authority, or Presence? |
| Score improves on some platforms but not others | Platform-specific gap | Focus on the lagging platform's specific data source |
| Score decreases | Something broke | Check crawler access (robots.txt), content freshness, and entity consistency |

See [references/ai-seo.md](references/ai-seo.md) for platform-specific optimization details and content templates.

---

## Step 2C: Programmatic SEO

Generate hundreds or thousands of pages at scale from templates + structured data. Each page must deliver unique value — not just variable substitution.

### When to Use pSEO

| Use When | Don't Use When |
|----------|---------------|
| You have structured data with many entities (cities, integrations, comparisons) | You'd be creating thin pages with no unique value per page |
| Each page serves a distinct search intent | All pages would answer basically the same question |
| You can add unique value beyond the data (analysis, recommendations, context) | You're just spinning templates to get more indexed pages |
| Your data is defensible (proprietary or hard to replicate) | The same data is freely available everywhere |

### Data Defensibility Hierarchy

How defensible is your pSEO play? Higher = harder for competitors to replicate.

| Tier | Data Type | Example | Defensibility |
|------|-----------|---------|---------------|
| 1 | **Proprietary** | Your own user data, benchmarks, metrics | Highest — no one else has it |
| 2 | **Product-derived** | Integration-specific data, compatibility info | High — tied to your product |
| 3 | **User-generated** | Reviews, community content, templates | Medium — builds over time |
| 4 | **Licensed** | Purchased datasets, API data | Low-medium — others can license too |
| 5 | **Public** | Government data, Wikipedia, free APIs | Lowest — anyone can build this |

**Rule:** If your data is Tier 4-5, you need exceptional template quality or additional proprietary enrichment to compete.

### 12 pSEO Playbook Patterns

| Pattern | Example | Search Intent |
|---------|---------|--------------|
| **Templates** | "[Tool] [use case] template" | Canva's templates, Notion templates |
| **Curation** | "Best [category] in [city]" | NomadList, Yelp |
| **Conversions** | "[Unit A] to [Unit B]" | Wise currency pages |
| **Comparisons** | "[Tool A] vs [Tool B]" | G2 comparison pages |
| **Examples** | "[Type] examples" | Dribbble, Behance |
| **Locations** | "[Service] in [City]" | Thumbtack, Yelp |
| **Personas** | "[Tool] for [role/industry]" | Monday.com's use-case pages |
| **Integrations** | "[Your tool] + [Other tool]" | Zapier's integration pages |
| **Glossary** | "What is [term]" | HubSpot's glossary |
| **Translations** | "[Phrase] in [language]" | Google Translate pages |
| **Directory** | "[Category] companies/tools" | ProductHunt, G2 |
| **Profiles** | "[Entity] overview/stats" | CrunchBase, LinkedIn |

### pSEO Quality Requirements

Every generated page must pass:
- [ ] **Unique value test:** Does this page offer something you can't get from any other page on the site?
- [ ] **Search intent match:** Does the page answer what someone searching this query actually wants?
- [ ] **Heading hierarchy:** Proper H1/H2/H3 structure (not just injected variables)
- [ ] **Schema markup:** Appropriate structured data for the page type
- [ ] **Internal linking:** Connected to hub pages and related pSEO pages
- [ ] **Indexation strategy:** Only index pages that meet quality bar; noindex thin pages

### URL Architecture

- Use subfolders, not subdomains (consolidates domain authority)
- Pattern: `/[category]/[entity]` — e.g., `/integrations/slack`, `/vs/competitor-name`
- Keep URLs flat (2-3 levels max)

### Post-Launch Monitoring

| Metric | Check | Frequency |
|--------|-------|-----------|
| Indexation rate | What % of pSEO pages are indexed? | Weekly (first month), monthly after |
| Thin content flags | Search Console coverage report | Weekly |
| Traffic per page | Are pages getting traffic, or are they dead weight? | Monthly |
| Cannibalization | Are pSEO pages competing with each other? | Monthly |
| Conversion | Are pSEO pages driving signups/leads? | Monthly |

See [references/programmatic-seo.md](references/programmatic-seo.md) for template design patterns and implementation guide.

---

## Step 2D: Competitor Comparison Pages

Competitor comparison and alternative pages are high-intent SEO content. These capture buyers actively evaluating options.

### Four Page Formats

Each format targets a different search intent:

| Format | URL Pattern | Search Intent | Example |
|--------|------------|--------------|---------|
| **Singular alternative** | `/alternatives/[competitor]` | "I want to leave [competitor]" | `/alternatives/salesforce` |
| **Plural alternatives** | `/[competitor]-alternatives` | "What are my options besides [competitor]?" | `/salesforce-alternatives` |
| **Direct comparison** | `/vs/[competitor]` | "How does [your product] compare to [competitor]?" | `/vs/salesforce` |
| **Third-party comparison** | `/[comp-a]-vs-[comp-b]` | "Which is better, [A] or [B]?" (you may not be either) | `/salesforce-vs-hubspot` |

**Priority:** Start with direct comparison pages for your top 3 competitors. Then build alternative pages. Third-party comparisons only if you have the authority to rank.

### Content Architecture

**Centralized data:** Maintain a single source of truth for competitor data (pricing, features, ratings) that propagates across all comparison pages. When a competitor changes pricing, update once.

**Essential sections per page:**
1. **TL;DR summary** — 40-60 word direct answer (AI-citable)
2. **Comparison table** — specific, verifiable features (not vague "better UX")
3. **Category breakdown** — compare by use case, not just feature list
4. **Audience segmentation** — "Choose [competitor] if... Choose [us] if..."
5. **Migration guidance** — how to switch, with social proof from switchers
6. **Honest assessment** — acknowledge competitor strengths (Pratfall Effect builds trust)

### Internal Linking

Build a hub-and-spoke structure:
- **Hub:** `/alternatives` or `/compare` (links to all comparison pages)
- **Spokes:** Individual comparison pages (link back to hub + to related comparisons)
- **Cross-links:** Each comparison page links to 2-3 related comparisons

### Update Cadence
- **Quarterly:** Verify competitor pricing and feature changes
- **Annually:** Full content refresh
- **Triggered:** When a competitor launches a major feature or changes pricing

See [references/competitor-pages.md](references/competitor-pages.md) for content templates and keyword targeting.

---

## Artifact Template

```markdown
---
skill: seo
mode: [audit | ai | programmatic | competitor]
version: 1
date: [today's date]
status: draft
---

# SEO: [Mode Name]

**Date:** [today]
**Skill:** seo
**Mode:** [Technical Audit | AI SEO | Programmatic SEO | Competitor Pages]
**Product:** [from product-context.md]

## Diagnosis

[Why this mode was chosen. What's the current situation?]

## Findings

[Mode-specific findings — see mode sections above for structure]

## Priority Actions

| # | Action | Category | Impact | Effort |
|---|--------|----------|--------|--------|
| 1 | [action] | [category] | H/M/L | H/M/L |
| 2 | [action] | [category] | H/M/L | H/M/L |

## Implementation Plan

[Ordered list of what to do first, second, third]

## Metrics to Track

| Metric | Current | Target | Check Frequency |
|--------|---------|--------|----------------|
| [metric] | [value] | [value] | [frequency] |

## Next Step

[What to do after implementing — re-audit timeline, experiment to run, etc.]

> On re-run: rename existing artifact to `seo-[mode].v[N].md` and create new with incremented version.
```

---

## Anti-Patterns

**"Do SEO" without diagnosis** — Running a generic checklist without determining whether the problem is technical, content, authority, or AI visibility. Different problems need different modes.

**Keyword stuffing (traditional or AI)** — Reduces AI visibility by ~10% (Princeton GEO study) and triggers Google's spam detection. Write for humans, structure for machines.

**pSEO as a content farm** — Generating thousands of thin pages with no unique value per page. Google's Helpful Content Update specifically targets this. Better to have 100 great pages than 10,000 thin ones.

**Ignoring third-party presence for AI SEO** — Optimizing only your own site while ignoring review sites and publications. Third-party sources drive 6.5x more AI citations.

**Blocking AI crawlers then expecting citations** — If GPTBot is blocked in robots.txt, ChatGPT can't cite your content.

**Flat competitor comparison tables** — Listing features with checkmarks tells the reader nothing about context. Compare by use case and audience, not just features.

**Schema false positives** — Flagging missing schema based on raw HTML when CMS plugins inject JSON-LD via client-side JavaScript. Always verify schema with Google Rich Results Test or browser DevTools.

**One-and-done audits** — SEO is ongoing. Technical issues resurface, competitors change, algorithms update. Set re-audit cadence (quarterly for technical, monthly for AI visibility).

---

## References

- [references/technical-audit.md](references/technical-audit.md) — Full audit report template and detailed checklists
- [references/ai-seo.md](references/ai-seo.md) — Platform-specific AI optimization and content templates
- [references/programmatic-seo.md](references/programmatic-seo.md) — pSEO template patterns and implementation
- [references/competitor-pages.md](references/competitor-pages.md) — Comparison page templates and keyword targeting
- [references/schema-reference.md](references/schema-reference.md) — Schema types, implementation contexts, and validation
