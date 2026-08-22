---
name: core-web-vitals
description: Measures and remediates LCP, INP, and CLS with evidence from lab/field tools. Use when page experience or CWV regressions are suspected or reported.
---

# Core Web Vitals

## Overview

Measure first, then fix the vitals that evidence shows are failing.

## When to Use

- Slow LCP, poor INP, layout shift, PSI/CrUX regressions

**Not for:** Inventing scores without tool output.

## Official sources

- https://developers.google.com/search/docs/appearance/core-web-vitals
- https://developers.google.com/search/docs/appearance/page-experience

## Process

1. Measure with PageSpeed Insights / CrUX / RUM — record LCP, INP, CLS.
2. Run `python skills/core-web-vitals/scripts/cwv_audit.py <url>` when network is available (PSI API).
3. Prioritize fixes per metric (image/TTFB for LCP; long tasks for INP; dimensions for CLS).
4. Require `width`/`height` (or aspect-ratio reserved space) on content images.
5. Re-measure after changes; keep lab vs field distinction clear.
6. Use `references/cwv-checklist.md`.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I can estimate LCP without tools." | Measure with PSI/CrUX/RUM — never invent scores. |
| "Lab scores are what Google uses." | Field data is the ranking-relevant signal when available; lab guides debugging. |
| "CLS fixes can wait." | Unsized media causes layout shift — set dimensions when shipping images. |

## Red Flags

- Inventing ranking factors not documented by Google
- Skipping verification ("looks fine")
- Advising spammy shortcuts (cloaking, doorways, link schemes)

## Verification

- [ ] Numeric evidence before and after (or explicit tool error documented)
- [ ] Fixes mapped to the failing metric
- [ ] No fake scores asserted
