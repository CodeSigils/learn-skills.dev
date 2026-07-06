---
name: cross-browser-testing
description: >-
  Implement cross-browser and cross-device test coverage with Playwright projects
  (Chromium, Firefox, WebKit, mobile emulation). Use when: "cross-browser,"
  "クロスブラウザ," "works in Safari?", "mobile viewport testing," browser-specific
  bugs, or whenever a web app's E2E suite runs on only one browser. Covers the
  ISO 25010:2023 Compatibility characteristic (co-existence, interoperability of the
  UI across engines). Not for: visual pixel diffs — use a dedicated visual-regression tool.
  Related: flexibility-testing.
license: MIT
metadata:
  version: "1.0"
  istqb: "CTFL v4.0 §2.2.1 (test types: non-functional)"
  iso25010: [compatibility]
  mode: [implementation]
---

# Cross-Browser Testing

Run the right subset of E2E tests across rendering engines and viewports, catching
engine-specific defects without tripling CI time.

## Objective

A Playwright project matrix where critical user journeys run on Chromium + Firefox +
WebKit and at least one mobile viewport, while the long tail runs on Chromium only.
The failure mode this prevents: "works on my Chrome" shipping Safari-breaking date
inputs, flexbox gaps, and clipboard/permission API differences.

## Context Discovery

- Which browsers/devices do real users use? (check analytics; don't guess — testing
  IE-era targets nobody uses wastes CI, skipping WebKit when 30% of traffic is iOS
  Safari is negligence)
- Which flows are business-critical? Only these get the full matrix.
- CI budget: total pipeline time available for the browser matrix.

## Instructions

1. **Define the project matrix** in `playwright.config.ts`: `chromium`, `firefox`,
   `webkit`, plus `devices['iPhone 15']` (or the analytics-dominant device). Tag
   critical-path specs with `@critical`.

2. **Tier the execution**: `@critical` runs on all projects every PR; everything else
   runs Chromium-only on PR and the full matrix nightly. Encode this with `grep` /
   `grepInvert` per project, not by duplicating specs.

3. **Write engine-neutral tests**: role-based locators (`getByRole`), no
   `waitForTimeout`, no engine-specific CSS selectors. Engine differences should fail
   assertions about *behavior*, not break the test plumbing.

4. **Isolate known engine differences explicitly**: where behavior legitimately
   differs (e.g. WebKit date-picker UI), branch with `browserName` and document why —
   an undocumented `if (browserName === 'webkit')` is a bug magnet.

5. **Report per-engine**: configure the HTML/JUnit reporter to split results by
   project so a WebKit-only failure is visible as such, not buried in an aggregate.

## Output Format

`playwright.config.ts` canonical shape:

```ts
export default defineConfig({
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox',  use: { ...devices['Desktop Firefox'] }, grep: /@critical/ },
    { name: 'webkit',   use: { ...devices['Desktop Safari'] },  grep: /@critical/ },
    { name: 'mobile-safari', use: { ...devices['iPhone 15'] },  grep: /@critical/ },
  ],
});
```

Spec tagging: `test('checkout completes @critical', async ({ page }) => { ... })`

## Anti-Patterns

- **Full matrix for everything** — 4× CI time, flake surface quadruples, team disables
  the matrix within a month. **Guard:** tiered execution; matrix size is a budget
  decision recorded in the config comments.
- **Hallucinated device names** — `devices['iPhone 17']` that doesn't exist in the
  installed Playwright version. **Guard:** verify device keys against
  `playwright.devices` in the installed version before writing config.
- **Skipping WebKit because local setup is annoying** — WebKit is where the defects
  are. **Guard:** if WebKit can't run locally, it must run in CI; never delete the
  project to green the build.
- **Engine-conditional assertions without a comment** — future maintainers can't tell
  intended difference from papered-over bug. **Guard:** every `browserName` branch
  cites the engine behavior it accommodates.

## Related Skills

- `flexibility-testing` — server/OS/install-level portability rather than browser engines.

## References

- ISO/IEC 25010:2023 — Compatibility (co-existence, interoperability)
- ISTQB CTFL v4.0 §2.2.1 — non-functional test types apply at every test level
