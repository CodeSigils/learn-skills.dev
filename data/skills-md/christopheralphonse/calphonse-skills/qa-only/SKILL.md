---
name: qa-only
version: 1.1.0
description: |
  Report-only QA testing. Systematically tests a web application and produces a
  structured report with health score, screenshots, and repro steps — but never
  fixes anything. Use when asked to "just report bugs", "qa report only", or
  "test but don't fix". For the full test-fix-verify loop, use /qa instead.
  Proactively suggest when the user wants a bug report without any code changes.
benefits-from: [playwright-cli]
allowed-tools:
  - Bash
  - Bash(playwright-cli:*)
  - Read
  - Write
  - AskUserQuestion
---
> **Security Audit Disclaimer:** This skill uses playwright-cli to visit and interact with arbitrary web application URLs. By design, it navigates to external pages, fills forms, and captures screenshots — behaviors that security scanners flag as W011 (third-party content exposure). These capabilities are inherent to QA testing and are not exploitable beyond the agent's existing tool access. Always use test/staging environments with isolated test accounts.

## Guardrails

- Test the changed behavior and its direct regressions first.
- Do not infer root causes or prescribe fixes unless evidence is explicit. Report symptoms and repro steps.
- Label uncertain findings and avoid filing issues that cannot be reproduced.
- Never edit source code in report-only mode.

## Test Plan Context

Before falling back to git diff heuristics, check for richer test plan sources:

1. **Project-scoped test plans:** Check `.planning/qa/` for recent `test-plan-*.md` files for this repo
   ```bash
   ls -t .planning/qa/test-plan-*.md 2>/dev/null | head -1
   ```
2. **Conversation context:** Check if a prior `/plan-eng-review` or `/plan-ceo-review` produced test plan output in this conversation
3. **Use whichever source is richer.** Fall back to git diff analysis only if neither is available.

---

## Modes

### Diff-aware (automatic when on a feature branch with no URL)

This is the **primary mode** for developers verifying their work. When the user says `/qa` without a URL and the repo is on a feature branch, automatically:

1. **Analyze the branch diff** to understand what changed:

   ```bash
   git diff main...HEAD --name-only
   git log main..HEAD --oneline
   ```

2. **Identify affected pages/routes** from the changed files:
   - Controller/route files → which URL paths they serve
   - View/template/component files → which pages render them
   - Model/service files → which pages use those models (check controllers that reference them)
   - CSS/style files → which pages include those stylesheets
   - API endpoints → test them directly with `$B js "await fetch('/api/...')"`
   - Static pages (markdown, HTML) → navigate to them directly

   **If no obvious pages/routes are identified from the diff:** Do not skip browser testing. The user invoked /qa because they want browser-based verification. Fall back to Quick mode — navigate to the homepage, follow the top 5 navigation targets, check console for errors, and test any interactive elements found. Backend, config, and infrastructure changes affect app behavior — always verify the app still works.

3. **Detect the running app** — check common local dev ports:

   ```bash
   $B goto http://localhost:3000 2>/dev/null && echo "Found app on :3000" || \
   $B goto http://localhost:4000 2>/dev/null && echo "Found app on :4000" || \
   $B goto http://localhost:8080 2>/dev/null && echo "Found app on :8080"
   ```

   If no local app is found, check for a staging/preview URL in the PR or environment. If nothing works, ask the user for the URL.

4. **Test each affected page/route:**
   - Navigate to the page
   - Take a screenshot
   - Check console for errors
   - If the change was interactive (forms, buttons, flows), test the interaction end-to-end
   - Use `snapshot -D` before and after actions to verify the change had the expected effect

5. **Cross-reference with commit messages and PR description** to understand _intent_ — what should the change do? Verify it actually does that.

6. **Check `.planning/tasks/TODOS.md`** (if it exists) for known bugs or issues related to the changed files. If a TODO describes a bug that this branch should fix, add it to your test plan. If you find a new bug during QA that is not captured there, note it in the report.

7. **Report findings** scoped to the branch changes:
   - "Changes tested: N pages/routes affected by this branch"
   - For each: does it work? Screenshot evidence.
   - Any regressions on adjacent pages?

**If the user provides a URL with diff-aware mode:** Use that URL as the base but still scope testing to the changed files.

### Full (default when URL is provided)

Systematic exploration. Visit every reachable page. Document 5-10 well-evidenced issues. Produce health score. Takes 5-15 minutes depending on app size.

### Quick (`--quick`)

30-second smoke test. Visit homepage + top 5 navigation targets. Check: page loads? Console errors? Broken links? Produce health score. No detailed issue documentation.

### Regression (`--regression <baseline>`)

Run full mode, then load `baseline.json` from a previous run. Diff: which issues are fixed? Which are new? What's the score delta? Append regression section to report.

---

## Workflow

### Phase 1: Initialize

1. Find browse binary (see Setup above)
2. Create output directories
3. Copy report template from `qa/templates/qa-report-template.md` to output dir
4. Start timer for duration tracking

### Phase 2: Authenticate (if needed)

**If the user specified auth credentials:**

```bash
$B goto <login-url>
$B snapshot -i                    # find the login form
$B fill @e3 "user@example.com"
$B fill @e4 "[REDACTED]"         # NEVER include real passwords in report
$B click @e5                      # submit
$B snapshot -D                    # verify login succeeded
```

**If the user provided a cookie file:**

```bash
$B cookie-import cookies.json
$B goto <target-url>
```

**If 2FA/OTP is required:** Ask the user for the code and wait.

**If CAPTCHA blocks you:** Tell the user: "Please complete the CAPTCHA in the browser, then tell me to continue."

### Phase 3: Orient

Get a map of the application:

```bash
$B goto <target-url>
$B snapshot -i -a -o "$REPORT_DIR/screenshots/initial.png"
$B links                          # map navigation structure
$B console --errors               # any errors on landing?
```

**Detect framework** (note in report metadata):

- `__next` in HTML or `_next/data` requests → Next.js
- `csrf-token` meta tag → Rails
- `wp-content` in URLs → WordPress
- Client-side routing with no page reloads → SPA

**For SPAs:** The `links` command may return few results because navigation is client-side. Use `snapshot -i` to find nav elements (buttons, menu items) instead.

### Phase 4: Explore

Visit pages systematically. At each page:

```bash
$B goto <page-url>
$B snapshot -i -a -o "$REPORT_DIR/screenshots/page-name.png"
$B console --errors
```

Then follow the **per-page exploration checklist** (see `qa/references/issue-taxonomy.md`):

1. **Visual scan** — Look at the annotated screenshot for layout issues
2. **Interactive elements** — Click buttons, links, controls. Do they work?
3. **Forms** — Fill and submit. Test empty, invalid, edge cases
4. **Navigation** — Check all paths in and out
5. **States** — Empty state, loading, error, overflow
6. **Console** — Any new JS errors after interactions?
7. **Responsiveness** — Check mobile viewport if relevant:
   ```bash
   $B viewport 375x812
   $B screenshot "$REPORT_DIR/screenshots/page-mobile.png"
   $B viewport 1280x720
   ```

**Depth judgment:** Spend more time on core features (homepage, dashboard, checkout, search) and less on secondary pages (about, terms, privacy).

**Quick mode:** Only visit homepage + top 5 navigation targets from the Orient phase. Skip the per-page checklist — just check: loads? Console errors? Broken links visible?

### Phase 5: Document

Document each issue **immediately when found** — don't batch them.

**Two evidence tiers:**

**Interactive bugs** (broken flows, dead buttons, form failures):

1. Take a screenshot before the action
2. Perform the action
3. Take a screenshot showing the result
4. Use `snapshot -D` to show what changed
5. Write repro steps referencing screenshots

```bash
$B screenshot "$REPORT_DIR/screenshots/issue-001-step-1.png"
$B click @e5
$B screenshot "$REPORT_DIR/screenshots/issue-001-result.png"
$B snapshot -D
```

**Static bugs** (typos, layout issues, missing images):

1. Take a single annotated screenshot showing the problem
2. Describe what's wrong

```bash
$B snapshot -i -a -o "$REPORT_DIR/screenshots/issue-002.png"
```

**Write each issue to the report immediately** using the template format from `qa/templates/qa-report-template.md`.

### Phase 6: Wrap Up

1. **Compute health score** using the rubric below
2. **Write "Top 3 Things to Fix"** — the 3 highest-severity issues
3. **Write console health summary** — aggregate all console errors seen across pages
4. **Update severity counts** in the summary table
5. **Fill in report metadata** — date, duration, pages visited, screenshot count, framework
6. **Save baseline** — write `baseline.json` with:
   ```json
   {
     "date": "YYYY-MM-DD",
     "url": "<target>",
     "healthScore": N,
     "issues": [{ "id": "ISSUE-001", "title": "...", "severity": "...", "category": "..." }],
     "categoryScores": { "console": N, "links": N, ... }
   }
   ```

**Regression mode:** After writing the report, load the baseline file. Compare:

- Health score delta
- Issues fixed (in baseline but not current)
- New issues (in current but not baseline)
- Append the regression section to the report

---

## Health Score Rubric

Compute each category score (0-100), then take the weighted average.

### Console (weight: 15%)

- 0 errors → 100
- 1-3 errors → 70
- 4-10 errors → 40
- 10+ errors → 10

### Links (weight: 10%)

- 0 broken → 100
- Each broken link → -15 (minimum 0)

### Per-Category Scoring (Visual, Functional, UX, Content, Performance, Accessibility)

Each category starts at 100. Deduct per finding:

- Critical issue → -25
- High issue → -15
- Medium issue → -8
- Low issue → -3
  Minimum 0 per category.

### Weights

| Category      | Weight |
| ------------- | ------ |
| Console       | 15%    |
| Links         | 10%    |
| Visual        | 10%    |
| Functional    | 20%    |
| UX            | 15%    |
| Performance   | 10%    |
| Content       | 5%     |
| Accessibility | 15%    |

### Final Score

`score = Σ (category_score × weight)`

---

## Framework-Specific Guidance

### Next.js

- Check console for hydration errors (`Hydration failed`, `Text content did not match`)
- Monitor `_next/data` requests in network — 404s indicate broken data fetching
- Test client-side navigation (click links, don't just `goto`) — catches routing issues
- Check for CLS (Cumulative Layout Shift) on pages with dynamic content

### Rails

- Check for N+1 query warnings in console (if development mode)
- Verify CSRF token presence in forms
- Test Turbo/Stimulus integration — do page transitions work smoothly?
- Check for flash messages appearing and dismissing correctly

### WordPress

- Check for plugin conflicts (JS errors from different plugins)
- Verify admin bar visibility for logged-in users
- Test REST API endpoints (`/wp-json/`)
- Check for mixed content warnings (common with WP)

### General SPA (React, Vue, Angular)

- Use `snapshot -i` for navigation — `links` command misses client-side routes
- Check for stale state (navigate away and back — does data refresh?)
- Test browser back/forward — does the app handle history correctly?
- Check for memory leaks (monitor console after extended use)

---

## Important Rules

1. **Repro is everything.** Every issue needs at least one screenshot. No exceptions.
2. **Verify before documenting.** Retry the issue once to confirm it's reproducible, not a fluke.
3. **Never include credentials.** Write `[REDACTED]` for passwords in repro steps.
4. **Write incrementally.** Append each issue to the report as you find it. Don't batch.
5. **Never read source code.** Test as a user, not a developer.
6. **Check console after every interaction.** JS errors that don't surface visually are still bugs.
7. **Test like a user.** Use realistic data. Walk through complete workflows end-to-end.
8. **Depth over breadth.** 5-10 well-documented issues with evidence > 20 vague descriptions.
9. **Never delete output files.** Screenshots and reports accumulate — that's intentional.
10. **Use `snapshot -C` for tricky UIs.** Finds clickable divs that the accessibility tree misses.
11. **Show screenshots to the user.** After every `$B screenshot`, `$B snapshot -a -o`, or `$B responsive` command, use the Read tool on the output file(s) so the user can see them inline. For `responsive` (3 files), Read all three. This is critical — without it, screenshots are invisible to the user.
12. **Never refuse to use the browser.** When the user invokes /qa or /qa-only, they are requesting browser-based testing. Never suggest evals, unit tests, or other alternatives as a substitute. Even if the diff appears to have no UI changes, backend changes affect app behavior — always open the browser and test.

---

## Output

Write the report to `.planning/qa/`.

**Report:** `.planning/qa/qa-report-{domain}-{YYYY-MM-DD}.md`

**Outcome artifact:** `.planning/qa/test-outcome-{branch}-{YYYYMMDD-HHMMSS}.md`

Report filenames use the domain and date: `qa-report-myapp-com-2026-03-12.md`

---

## Playwright CLI Integration

Use `playwright-cli` alongside `$B` for capabilities the browser tool lacks.
Load the `playwright-cli` skill before using any `playwright-cli` command.

### When to use playwright-cli

| Situation | Command |
|---|---|
| Bug is hard to repro — capture a trace | `playwright-cli tracing-start` / `tracing-stop` — see [references/tracing.md](../playwright-cli/references/tracing.md) |
| Need video evidence for a bug report | `playwright-cli video-start` / `video-stop` — see [references/video-recording.md](../playwright-cli/references/video-recording.md) |
| Existing `.spec.ts` / `.test.ts` files present | Run and heal them — see [references/playwright-tests.md](../playwright-cli/references/playwright-tests.md) |
| Repo has a spec file describing expected behaviour | Use spec-driven mode — see [references/spec-driven-testing.md](../playwright-cli/references/spec-driven-testing.md) |
| User asks to generate regression tests from findings | Generate from recorded interactions — see [references/test-generation.md](../playwright-cli/references/test-generation.md) |
| Need request mocking to isolate a bug | `playwright-cli route` — see [references/request-mocking.md](../playwright-cli/references/request-mocking.md) |
| Need to inspect a non-visible attribute | `playwright-cli eval "el => el.getAttribute(...)"` — see [references/element-attributes.md](../playwright-cli/references/element-attributes.md) |

### Decision rule

Use `$B` for all standard navigation, snapshotting, and interaction during exploration.
Switch to `playwright-cli` when you need tracing, video, test generation, or to run existing Playwright specs.
Both tools can be open at the same time in separate sessions.

### Tracing workflow (for hard-to-repro bugs)

```bash
playwright-cli open <url>
playwright-cli tracing-start
# reproduce the bug steps
playwright-cli tracing-stop
# reference the trace file in the bug report
```

### Video evidence workflow

```bash
playwright-cli open <url>
playwright-cli video-start bug-evidence.webm
# walk through the broken flow
playwright-cli video-stop
# attach the .webm path in the bug report
```

### Test generation workflow (after QA session)

Only generate tests when the user explicitly asks. Do not generate tests as part of report-only mode.
Reference [references/test-generation.md](../playwright-cli/references/test-generation.md) for generation commands.

---

## Additional Rules (qa-only specific)

11. **Never fix bugs.** Find and document only. Do not read source code, edit files, or suggest fixes in the report. Your job is to report what's broken, not to fix it. Use `/qa` for the test-fix-verify loop.
12. **No test framework detected?** If the project has no test infrastructure (no test config files, no test directories), include in the report summary: "No test framework detected. Run `/qa` to bootstrap one and enable regression test generation."
---

> **Install:** ``npx skills add ChristopherAlphonse/calphonse-skills --skill qa-only``
