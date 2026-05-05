---
name: geo
description: Generative Engine Optimization — optimize content for AI search engines (ChatGPT, Perplexity, Google AI Overviews, Gemini). Use when user wants to rank in AI search, improve AI citability, audit content for LLM visibility, or explicitly invokes /geo commands. Triggers on "GEO", "generative engine", "AI search", "AI overviews", "citability", "Perplexity", "ChatGPT search", or /geo commands.
---

# Generative Engine Optimization (GEO) Skill

Optimize content so AI search engines (ChatGPT, Perplexity, Google AI Overviews, Gemini) cite, reference, and recommend your pages.

Traditional SEO gets you into search results. GEO gets you into AI-generated answers.

## Commands

| Command | What it does |
|---------|-------------|
| `/geo:score` | Score a page's content for AI citability (0-100) |
| `/geo:optimize` | Rewrite or restructure content for AI search visibility |
| `/geo:audit` | Audit an entire site's GEO readiness |
| `/geo:help` | Command reference |

---

## How AI Search Engines Select Sources

Understanding this is the foundation of GEO:

1. **Retrieval** — The LLM's search system retrieves candidate pages (similar to traditional crawling)
2. **Relevance scoring** — Pages are ranked by topical match, authority signals, and freshness
3. **Extraction** — The LLM extracts specific claims, facts, and structured data from top pages
4. **Synthesis** — Extracted information is woven into a generated answer
5. **Citation** — Some engines (Perplexity, AI Overviews) link back to sources

**Key insight:** AI engines don't just rank pages — they extract and reuse specific passages. Your content needs to be *extractable*.

---

## GEO Scoring (`/geo:score`)

**Goal:** Score how likely a page is to be cited by AI search engines.

### Scoring Rubric (100 points total)

```
GEO CITATION-READINESS SCORE
==============================

STRUCTURE (25 points)
  [ /5 ] Clear H1 that matches a searchable question
  [ /5 ] Hierarchical heading structure (H2/H3) with descriptive text
  [ /5 ] First paragraph directly answers the core question (no fluff intro)
  [ /5 ] Key claims are in standalone sentences (not buried in paragraphs)
  [ /5 ] Lists, tables, or structured formats for comparisons/steps

AUTHORITY SIGNALS (25 points)
  [ /5 ] Original data, statistics, or research cited
  [ /5 ] Author/organization credentials visible
  [ /5 ] Publication date present and recent
  [ /5 ] External citations to authoritative sources
  [ /5 ] Unique insight not available on competing pages

EXTRACTABILITY (25 points)
  [ /5 ] Definitions are crisp (1-2 sentences, self-contained)
  [ /5 ] Claims include specific numbers, dates, or named entities
  [ /5 ] Comparison/contrast content uses structured format (tables, lists)
  [ /5 ] Step-by-step content uses ordered lists with clear labels
  [ /5 ] FAQ or Q&A format present for common sub-questions

TECHNICAL (25 points)
  [ /5 ] Schema markup present (Article, FAQ, HowTo, etc.)
  [ /5 ] Clean, descriptive URL slug
  [ /5 ] Meta description summarizes the page's key answer
  [ /5 ] Page loads fast (LCP < 2.5s) — slow pages get deprioritized
  [ /5 ] Content accessible without JavaScript rendering

TOTAL: ___/100
```

### Score Interpretation

| Score | Rating | Action |
|-------|--------|--------|
| 80-100 | Excellent | Minor tweaks. Monitor AI search presence. |
| 60-79 | Good | Specific optimizations needed. Address weakest category. |
| 40-59 | Needs work | Significant restructuring required. |
| 0-39 | Poor | Content is essentially invisible to AI search. Major rewrite needed. |

### Output
Deliver: Score breakdown by category + specific issues found + prioritized fix list.

---

## GEO Optimization (`/geo:optimize`)

**Goal:** Rewrite or restructure content to maximize AI citability.

### Optimization Techniques

1. **Lead with the answer.** AI engines extract from the first paragraph heavily.

```
BAD:  "In today's rapidly evolving digital landscape, businesses
       are increasingly turning to..." (4 sentences before the answer)

GOOD: "A GTM strategy is a plan for how you'll bring a product to
       market, reach your target customers, and achieve competitive
       advantage. It covers positioning, channels, pricing, and
       launch execution." (Answer in sentence 1)
```

2. **Create extractable definitions.** Self-contained, quotable sentences:

```
BAD:  "There are many ways to think about pricing, and it really
       depends on your market and what competitors charge..."

GOOD: "Value-based pricing sets the price according to the
       customer's perceived value of the outcome, not the cost
       of production. Companies using value-based pricing report
       15-25% higher margins than cost-plus alternatives (OpenView 2024)."
```

3. **Use structured comparisons.** Tables and lists > prose for comparisons:

```
BAD:  "Tool A is good for small teams while Tool B works better
       for enterprises. Tool A costs less but Tool B has more features..."

GOOD:
| Factor    | Tool A          | Tool B           |
|-----------|-----------------|------------------|
| Best for  | Small teams     | Enterprise       |
| Price     | $19/mo          | $99/mo           |
| Key feature| Simplicity     | Advanced workflows|
```

4. **Include unique data points.** AI engines prefer pages with original information:
   - Original research, surveys, benchmarks
   - Case study results with specific numbers
   - Expert quotes with attribution
   - Proprietary frameworks with named concepts

5. **Answer sub-questions explicitly.** AI engines often synthesize from multiple sections:
   - Use H2/H3 headings phrased as questions
   - Each section should be self-contained (readable without context)
   - Include a FAQ section for long-tail variations

6. **Cite authoritative sources.** Pages that reference other trusted sources are seen as more reliable:
   - Link to primary research, not aggregator articles
   - Include publication year in citations
   - Name the organization, not just "studies show"

### Optimization Checklist

```
GEO OPTIMIZATION CHECKLIST
============================
[ ] First sentence directly answers the page's core question
[ ] Every key claim is in a standalone, extractable sentence
[ ] At least 1 original data point / unique insight per section
[ ] Comparisons use tables or structured lists
[ ] Steps use numbered lists with clear action verbs
[ ] H2/H3 headings are phrased as questions where natural
[ ] FAQ section covers 3-5 common sub-questions
[ ] Sources cited with organization name + year
[ ] Schema markup matches content type (Article, FAQ, HowTo)
[ ] Author bio with credentials visible on page
```

### Output
Deliver: Optimized content (or specific rewrite suggestions) + before/after comparison + updated GEO score.

---

## GEO Site Audit (`/geo:audit`)

**Goal:** Assess an entire site's readiness for AI search engines.

### Audit Process

1. **Identify high-value pages** — Focus on pages that target informational or comparison queries (these are what AI engines answer)

2. **Score each page** using the GEO scoring rubric above

3. **Aggregate findings:**

```
GEO SITE AUDIT SUMMARY
========================
Pages audited:        ___
Average GEO score:    ___/100
Pages scoring 80+:    ___ (___%)
Pages scoring <40:    ___ (___%)

CATEGORY AVERAGES
  Structure:          ___/25
  Authority:          ___/25
  Extractability:     ___/25
  Technical:          ___/25

TOP ISSUES (by frequency)
  1. [Issue] — affects ___ pages
  2. [Issue] — affects ___ pages
  3. [Issue] — affects ___ pages

PRIORITY FIXES
  1. [Fix] — impact: HIGH, effort: LOW
  2. [Fix] — impact: HIGH, effort: MED
  3. [Fix] — impact: MED, effort: LOW
```

4. **Page-level recommendations** for the 5 highest-opportunity pages (high traffic + low GEO score)

### Output
Deliver: Site audit summary + category breakdown + priority fix list + per-page recommendations for top 5 opportunities.

---

## GEO vs SEO: When to Use What

| Signal | Traditional SEO | GEO |
|--------|----------------|-----|
| Goal | Rank in search results | Get cited in AI answers |
| Content format | Keyword-optimized prose | Extractable, structured claims |
| Authority | Backlinks, domain rating | Original data, expert credentials |
| Technical | Core Web Vitals, crawlability | Schema, clean HTML, fast load |
| Measurement | Rankings, CTR, traffic | AI mention monitoring, citation tracking |

**They're complementary, not competing.** A page optimized for both SEO and GEO wins in traditional search AND gets cited by AI engines.

---

## AI Search Engines and Their Behaviors

| Engine | Citation style | Key signals | Notes |
|--------|---------------|-------------|-------|
| Google AI Overviews | Inline links to sources | Authority, freshness, schema | Pulls from top organic results |
| Perplexity | Numbered footnote citations | Structure, specificity, recency | Most generous with citations |
| ChatGPT (Browse) | Inline links when browsing | Relevance, extractability | Only when actively searching |
| Gemini | Inline references | Google index signals | Heavily tied to Google organic |
| Claude (web search) | Inline references | Content quality, structure | Newer entrant to web search |

---

## Principles

1. **Write for extraction, not just reading.** Every key claim should work as a standalone quote.
2. **Be the primary source.** Pages with original data get cited. Pages that summarize others don't.
3. **Structure is signal.** Tables, lists, and clear headings tell AI engines "this is organized knowledge."
4. **Specificity wins.** "Conversion rates improved 34% over 6 months" beats "results improved significantly."
5. **GEO amplifies SEO.** The same qualities that make content AI-citable also make it rank better traditionally.
