---
name: accessibility-audit
description: >-
  Audit and test web UI accessibility against WCAG 2.2 — the testable basis for the
  ISO/IEC 25010:2023 Interaction Capability characteristic (notably Inclusivity and
  Operability). Use when: "accessibility," "a11y," "アクセシビリティ," "WCAG,"
  "screen reader," "keyboard navigation," "color contrast," "ADA/Section 508
  compliance," or auditing a UI for users with disabilities. Produces a WCAG 2.2
  conformance audit with prioritized findings (design mode) and automated + manual
  test suites, e.g. @axe-core/playwright (implementation mode). Not for: cross-engine
  rendering bugs — use cross-browser-testing. Related: cross-browser-testing.
license: MIT
metadata:
  version: "1.0"
  istqb: "CTFL v4.0 §2.2.1 (non-functional test types)"
  iso25010: [interaction-capability]
  mode: [design, implementation]
---

# Accessibility Audit (WCAG 2.2)

Verify people with disabilities can perceive, operate, understand, and reliably access
the UI — measured against WCAG 2.2 success criteria, not vibes.

## Objective

A WCAG 2.2 conformance assessment at a stated level (typically **AA**), combining
automated scans with the manual testing that automation cannot replace, and producing
findings mapped to specific success criteria. The failure mode this prevents: shipping
a UI that passes an automated scanner (which covers only ~30–40% of criteria) while
being unusable by keyboard or screen reader.

## Context Discovery

- **Target conformance level**: A, AA, or AAA? Default **AA** (the legal/de-facto
  baseline for ADA, Section 508, EN 301 549, European Accessibility Act).
- **Scope**: which flows/pages? Prioritize critical journeys (signup, checkout, core
  task) — these must be fully accessible.
- **Tech stack**: React/Vue/etc. and existing E2E tooling (Playwright/Cypress) — the
  automated layer plugs into it.
- **Assistive tech to test with**: NVDA (Windows), VoiceOver (macOS/iOS) at minimum.

## Instructions

1. **Automated scan first** (cheap, catches machine-detectable issues): run axe-core
   over each page/state. It finds missing alt text, ARIA misuse, contrast, missing
   form labels — but explicitly know it covers only part of WCAG; never report a clean
   scan as "accessible."

2. **Keyboard-only pass** (no mouse): Tab/Shift-Tab/Enter/Space/arrows through every
   interactive element. Verify visible focus (SC 2.4.7), logical focus order (2.4.3),
   no keyboard traps (2.1.2), focus not obscured (2.4.11, new in 2.2), and that
   drag-only actions have a single-pointer/keyboard alternative (2.5.7, new).

3. **Screen reader pass**: with NVDA/VoiceOver, verify every control announces a
   correct name, role, and value (SC 4.1.2); headings/landmarks are structured; images
   have meaningful text alternatives; dynamic updates use live regions.

4. **Perception checks**: color contrast ≥ 4.5:1 for text / 3:1 large text / 3:1
   non-text (SC 1.4.3, 1.4.11); 200% zoom (1.4.4) and 400% reflow to 320px without
   two-dimensional scrolling (1.4.10); information not conveyed by color alone (1.4.1).

5. **WCAG 2.2 additions**: check the new criteria — Target Size (Minimum) 24×24 CSS px
   (2.5.8), Consistent Help (3.2.6), Redundant Entry (3.3.7), Accessible Authentication
   (3.3.8, no cognitive-function test like solving a puzzle to log in).

6. **Report against criteria**: each finding cites the exact SC, level, severity, and a
   remediation. Map to Interaction Capability sub-characteristics (Inclusivity,
   Operability, User error protection) for the ISO 25010 traceability appendix.

## Output Format

### design mode

```
# WCAG 2.2 Accessibility Audit: {product} — target level AA
## Summary: pass rate, blocking issues, conformance statement
## Findings
   | ID | WCAG SC | Level | Page/Component | Severity | Issue | Remediation |
## Manual test coverage (keyboard / screen reader / zoom) — what was tested
## ISO 25010 mapping (Interaction Capability sub-characteristics)
```

### implementation mode

Automated gate with @axe-core/playwright (fails CI on violations):

```ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('checkout page has no WCAG 2.2 AA violations', async ({ page }) => {
  await page.goto('/checkout');
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa'])
    .analyze();
  expect(results.violations).toEqual([]);
});
```

Plus a documented **manual test checklist** (keyboard + screen reader) per critical
flow — automation is a floor, not the audit. Other tools: Pa11y (CI), Lighthouse,
WAVE.

## Anti-Patterns

- **"Automated scan is green = accessible"** — the single most common false claim;
  scanners miss keyboard traps, illogical focus order, meaningless alt text, bad SR
  announcements. **Guard:** every audit includes a manual keyboard + screen-reader pass.
- **Alt text that describes nothing** — `alt="image"` passes presence checks but fails
  users. **Guard:** assert alt text conveys purpose; decorative images use `alt=""`.
- **Hallucinated SC numbers** — citing WCAG criteria that don't exist or wrong levels.
  **Guard:** cite exact SC number+name from WCAG 2.2; verify level (A/AA/AAA).
- **Contrast checked on one state** — hover/focus/disabled states often fail. **Guard:**
  check contrast across interactive states, not just default.
- **AAA promised, AA delivered** — conformance level claimed without testing its
  criteria. **Guard:** state the tested level; AA requires all A + AA criteria.

## Related Skills

- `cross-browser-testing` — assistive tech behaves differently per engine; coordinate.
- `test-strategy-doc` — sets the target conformance level and in-scope flows.

## References

- WCAG 2.2 — W3C Recommendation, 2024-12-12 — https://www.w3.org/TR/WCAG22/
  (4 POUR principles; levels A/AA/AAA; 87 success criteria)
- ISO/IEC 25010:2023 — Interaction Capability (Inclusivity, Operability, User error protection)
- Tools: axe-core / @axe-core/playwright, Pa11y, Lighthouse, WAVE; screen readers NVDA, VoiceOver
