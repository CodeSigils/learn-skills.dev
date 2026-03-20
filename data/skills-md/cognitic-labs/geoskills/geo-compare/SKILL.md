---
name: geo-compare
description: Compare GEO scores across 2-3 competing websites side by side — identify where competitors lead and where you should focus optimization efforts. Use when the user asks to compare sites for AI visibility, benchmark against competitors, or mentions competitor analysis for AI search.
version: 1.0.0
---

# geo-compare Skill

You run parallel GEO audits on 2-3 websites and produce a side-by-side comparison matrix showing exactly where each site leads or falls behind in AI discoverability. The scoring methodology is identical to geo-audit — refer to `../geo-audit/references/scoring-guide.md` for the full rubric.

---

## Phase 1: Input Validation

### 1.1 Extract URLs

Parse 2-3 URLs from the user's input. Normalize each:
- Add `https://` if no protocol specified
- Remove trailing slashes
- Extract the base domain

Minimum 2 URLs, maximum 3. If more than 3 are provided, ask the user to select the top 3.

### 1.2 Identify Primary Site

Ask or infer which site is the user's own (the "primary"):
- If obvious from context ("compare my site X with competitor Y"), mark X as primary
- If unclear, treat the first URL as primary

Print:
```
GEO Compare: {primary_domain} vs {competitor_domains}
  Sites: {count}
  Running parallel audits...
```

---

## Phase 2: Parallel Audits

Run a full GEO audit on each site simultaneously. For each site, follow the geo-audit procedure:

1. Fetch homepage, detect business type, collect pages (up to 10 per site)
2. Launch 4 subagents per site (Technical, Citability, Schema, Brand)
3. Compute composite GEO Score

**Important**: Launch all site audits in parallel to minimize total time. Each site runs its own set of 4 subagents independently.

Read the subagent instructions from `../geo-audit/references/agents/` directory:
- `geo-technical.md`
- `geo-citability.md`
- `geo-schema.md`
- `geo-brand.md`

---

## Phase 3: Comparison Matrix

### 3.1 Score Comparison Table

```markdown
## GEO Score Comparison

| Dimension | {primary} | {competitor_1} | {competitor_2} | Leader |
|-----------|-----------|----------------|----------------|--------|
| Technical Accessibility | {t1}/100 | {t2}/100 | {t3}/100 | {domain} |
| Content Citability | {c1}/100 | {c2}/100 | {c3}/100 | {domain} |
| Structured Data | {s1}/100 | {s2}/100 | {s3}/100 | {domain} |
| Entity & Brand | {b1}/100 | {b2}/100 | {b3}/100 | {domain} |
| **GEO Score** | **{g1}/100** | **{g2}/100** | **{g3}/100** | **{domain}** |
| **Grade** | **{grade1}** | **{grade2}** | **{grade3}** | |
```

### 3.2 Sub-dimension Breakdown

For each of the 4 dimensions, show the sub-score comparison:

```markdown
### Technical Accessibility Detail

| Sub-dimension | {primary} | {comp_1} | {comp_2} |
|---------------|-----------|----------|----------|
| AI Crawler Access | {x}/40 | {x}/40 | {x}/40 |
| Rendering & Delivery | {x}/25 | {x}/25 | {x}/25 |
| Speed & Accessibility | {x}/20 | {x}/20 | {x}/20 |
| Meta & Headers | {x}/15 | {x}/15 | {x}/15 |
```

Repeat for Citability, Schema, and Brand.

### 3.3 Gap Analysis

Identify where the primary site falls behind competitors:

```markdown
## Gap Analysis: {primary_domain}

### Behind Competitors

| Area | Your Score | Best Competitor | Gap | Priority |
|------|-----------|----------------|-----|----------|
| {sub-dimension} | {x} | {y} ({domain}) | -{delta} | Critical |
| {sub-dimension} | {x} | {y} ({domain}) | -{delta} | High |
| ... | | | | |

### Ahead of Competitors

| Area | Your Score | Closest Competitor | Lead |
|------|-----------|-------------------|------|
| {sub-dimension} | {x} | {y} ({domain}) | +{delta} |
| ... | | | |
```

### 3.4 Competitive Advantages

Highlight the primary site's unique strengths:

```markdown
## Your Competitive Advantages

1. **{Advantage}**: {primary} scores {x} vs competitor avg {y} — {why this matters}
2. **{Advantage}**: ...
```

---

## Phase 4: Recommendations

### 4.1 Priority Fix List

Based on the gap analysis, recommend fixes ordered by competitive impact:

```markdown
## Priority Fixes (Competitive Impact)

| # | Fix | Current | Target | Competitor Benchmark | Impact |
|---|-----|---------|--------|---------------------|--------|
| 1 | {fix description} | {current_score} | {target} | {competitor} has {score} | +{points} pts |
| 2 | {fix description} | ... | ... | ... | ... |
```

### 4.2 Quick Wins vs Competitor

Identify fixes where the primary site can overtake a competitor with minimal effort:

```markdown
## Quick Wins to Overtake {competitor}

1. {Fix}: Close the {x}-point gap in {dimension} — estimated {effort}
2. ...
```

---

## Phase 5: Output

### 5.1 Generate Report File

Create a file named: `GEO-COMPARE-{primary_domain}-{YYYY-MM-DD}.md`

The report includes all sections from Phase 3 and Phase 4.

### 5.2 Print Summary

```
GEO Compare: {primary} vs {competitors}

| Site | GEO Score | Grade |
|------|-----------|-------|
| {primary} | {score}/100 | {grade} |
| {competitor_1} | {score}/100 | {grade} |
| {competitor_2} | {score}/100 | {grade} |

Biggest gaps: {top 3 areas where primary trails}
Quick wins: {top 3 fastest improvements}

Full report: GEO-COMPARE-{primary}-{date}.md
Export: To generate PDF/Word, ask "export as PDF" or "export as Word"
```

---

## Quality Gates

1. **Site limit**: Maximum 3 sites per comparison
2. **Page limit**: Maximum 10 pages per site (30 total)
3. **Parallel execution**: All site audits must run simultaneously
4. **Consistent scoring**: Use identical rubric across all sites
5. **Rate limiting**: 1 second between requests to the same domain
6. **Timeout**: 30 seconds per URL fetch
7. **Respect robots.txt**: Report restrictions as findings, do not bypass
