---
name: geo-monitor
description: Re-audit a website and compare scores against a previous GEO audit baseline to track improvement over time. Use when the user asks to re-audit, check progress, track GEO score changes, monitor improvements, or compare before and after optimization.
version: 1.0.0
---

# geo-monitor Skill

You re-audit a website and compare the new scores against a previous GEO audit report, producing a clear before/after comparison that shows what improved, what regressed, and what still needs work. The scoring methodology is identical to geo-audit — refer to `../geo-audit/references/scoring-guide.md` for the full rubric.

---

## Phase 1: Input

### 1.1 Extract Parameters

Accept two inputs:
- **URL** — The site to re-audit
- **Baseline** — Path to a previous GEO audit report (Markdown file)

If no baseline file is provided:
- Search the current directory for files matching `GEO-AUDIT-{domain}-*.md`
- If found, use the most recent one
- If not found, inform the user this will be a first audit (no comparison available) and run a standard geo-audit instead

### 1.2 Parse Baseline Report

Extract from the baseline Markdown file:
- Audit date
- GEO composite score and grade
- Dimension scores (Technical, Citability, Schema, Brand)
- Sub-dimension scores
- Issue list with priorities

Print:
```
GEO Monitor: {domain}
  Baseline: {date} — GEO Score {score}/100 (Grade {grade})
  Running new audit...
```

---

## Phase 2: Re-Audit

Run a full GEO audit on the site following the geo-audit procedure:

1. Fetch homepage, detect business type, collect pages (up to 10)
2. Launch 4 subagents in parallel (Technical, Citability, Schema, Brand)
3. Compute composite GEO Score

Read the subagent instructions from `../geo-audit/references/agents/` directory:
- `geo-technical.md`
- `geo-citability.md`
- `geo-schema.md`
- `geo-brand.md`

---

## Phase 3: Delta Analysis

### 3.1 Score Comparison

```markdown
## Score Comparison

| Dimension | Baseline ({date1}) | Current ({date2}) | Change |
|-----------|-------------------|-------------------|--------|
| Technical Accessibility | {t1}/100 | {t2}/100 | {+/-delta} |
| Content Citability | {c1}/100 | {c2}/100 | {+/-delta} |
| Structured Data | {s1}/100 | {s2}/100 | {+/-delta} |
| Entity & Brand | {b1}/100 | {b2}/100 | {+/-delta} |
| **GEO Score** | **{g1}/100 ({grade1})** | **{g2}/100 ({grade2})** | **{+/-delta}** |
```

Use visual indicators for changes:
- Improvement: `+{n}`
- Regression: `-{n}`
- No change: `0`

### 3.2 Sub-dimension Breakdown

For each dimension, show sub-score changes:

```markdown
### Technical Accessibility: {old} → {new} ({+/-delta})

| Sub-dimension | Baseline | Current | Change |
|---------------|----------|---------|--------|
| AI Crawler Access | {x}/40 | {y}/40 | {+/-} |
| Rendering & Delivery | {x}/25 | {y}/25 | {+/-} |
| Speed & Accessibility | {x}/20 | {y}/20 | {+/-} |
| Meta & Headers | {x}/15 | {y}/15 | {+/-} |
```

Repeat for all 4 dimensions.

### 3.3 Issue Resolution Tracking

Compare the issue lists:

```markdown
## Issue Tracking

### Resolved Issues
| Issue | Priority | Points Recovered |
|-------|----------|-----------------|
| {issue from baseline no longer present} | {priority} | +{points} |

### New Issues
| Issue | Priority | Points Lost |
|-------|----------|------------|
| {issue in current not in baseline} | {priority} | -{points} |

### Remaining Issues
| Issue | Priority | Points at Stake |
|-------|----------|----------------|
| {issue still present} | {priority} | {points} |
```

### 3.4 Improvement Velocity

```markdown
## Improvement Summary

- **Days since baseline**: {n} days
- **Score change**: {+/-delta} points
- **Grade change**: {grade1} → {grade2}
- **Issues resolved**: {n} of {total}
- **New issues introduced**: {n}
- **Net improvement rate**: {delta/days} points/day
```

---

## Phase 4: Next Steps

### 4.1 Remaining Priority Fixes

List issues still unresolved, ordered by impact:

```markdown
## Still to Fix

| # | Issue | Priority | Potential Gain |
|---|-------|----------|---------------|
| 1 | {issue} | Critical | +{points} pts |
| 2 | {issue} | High | +{points} pts |
```

### 4.2 Projected Score

```markdown
## Projected Score After Remaining Fixes

If all Critical + High issues are resolved:
  Projected GEO Score: {x}/100 (Grade {grade})
  Projected improvement: +{delta} points from current
```

---

## Phase 5: Output

### 5.1 Generate Report File

Create a file named: `GEO-MONITOR-{domain}-{YYYY-MM-DD}.md`

### 5.2 Print Summary

```
GEO Monitor: {domain}

Score: {old}/100 → {new}/100 ({+/-delta})
Grade: {old_grade} → {new_grade}

| Dimension | Change |
|-----------|--------|
| Technical | {+/-delta} |
| Citability | {+/-delta} |
| Schema | {+/-delta} |
| Brand | {+/-delta} |

Issues: {resolved} resolved, {new} new, {remaining} remaining
Days since baseline: {n}

Full report: GEO-MONITOR-{domain}-{date}.md
Export: To generate PDF/Word, ask "export as PDF" or "export as Word"
```

---

## Quality Gates

1. **Consistent methodology**: Use identical scoring rubric as baseline
2. **Page limit**: Maximum 10 pages per audit
3. **Baseline validation**: Verify baseline file is a valid geo-audit report
4. **Date tracking**: Always record audit date for future comparisons
5. **Rate limiting**: 1 second between requests to the same domain
6. **Timeout**: 30 seconds per URL fetch
7. **Respect robots.txt**: Report restrictions as findings, do not bypass
