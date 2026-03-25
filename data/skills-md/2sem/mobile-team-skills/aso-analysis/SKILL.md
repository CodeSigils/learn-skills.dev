---
name: aso-analysis
description: Quick App Store optimization (ASO) checklist and keyword analysis for WhereWeGo. Use on main agent for lightweight ASO checks. Escalate to marketer subagent for full strategy, campaign planning, or detailed competitive analysis.
---

# ASO Analysis

## Overview

Fast App Store optimization check for the main agent. Covers metadata quality, keyword coverage, screenshot audit, and ratings health — without spawning a full marketer subagent.

**Announce at start:** "Using aso-analysis skill for this ASO check."

**Use this skill when:**
- Reviewing current App Store metadata (title, subtitle, description)
- Spot-checking keyword coverage
- Quick screenshot audit
- Checking ratings/review trends
- Answering "is our ASO healthy?" before a release

**Escalate to `marketer` subagent when:**
- Full marketing strategy or campaign planning
- User acquisition channel analysis
- Detailed competitive landscape report
- Seasonal campaign brief (summer, xmas)

---

## App Info

| Field | Value |
|-------|-------|
| App | WhereWeGo |
| Bundle ID | `com.2sem.wherewego` |
| Category | Travel |
| Primary market | Korea |
| Languages | ko, en, ja, zh-Hans, zh-Hant, de, es, fr, ru |

---

## ASO Health Checklist

### Metadata
- [ ] **Title** (30 chars max): Contains primary keyword (e.g. "Korea Tourism", "여행", "관광")
- [ ] **Subtitle** (30 chars max): Secondary keyword + value prop
- [ ] **Keywords field** (100 chars): No spaces after commas, no repeated words from title/subtitle
- [ ] **Description**: First 3 lines sell the app (visible without "More"), keywords woven in naturally

### Screenshots
- [ ] First screenshot shows the core value prop (map + nearby spots)
- [ ] Text overlays are translated per locale
- [ ] Shows at least one seasonal theme if relevant to current season
- [ ] No UI chrome showing time/battery that could look dated

### Ratings
- [ ] Average rating ≥ 4.0
- [ ] Recent reviews (last 30 days) trend positive
- [ ] Unanswered negative reviews in cs queue?

---

## Keyword Strategy — WhereWeGo

### Tier 1 (high intent, include in title/subtitle)
- Korean: 여행, 관광지, 한국여행, 주변 관광
- English: korea tourism, travel korea, nearby attractions

### Tier 2 (include in keywords field)
- Korean: 여행 앱, 관광 정보, 근처 여행지
- English: korea travel app, tourist spots, travel guide
- Japanese: 韓国旅行, 観光スポット
- Chinese: 韩国旅游, 景点

### Avoid
- Generic: travel, tourism (too broad, low conversion)
- Trademarked names

---

## Quick Audit Output Format

When running an ASO check, output:

```
## ASO Audit — WhereWeGo [date]

### Metadata Score: X/5
- Title: [pass/fail + note]
- Subtitle: [pass/fail + note]
- Keywords: [pass/fail + note]
- Description: [pass/fail + note]

### Screenshots Score: X/3
- [note per screenshot slot]

### Ratings Health
- Average: X.X ★ ([N] ratings)
- Trend: [improving/stable/declining]
- Unanswered reviews: [Y]

### Top 3 Quick Wins
1. [action]
2. [action]
3. [action]

### Escalate to marketer? [yes/no + reason]
```
