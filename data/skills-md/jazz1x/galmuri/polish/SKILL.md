---
name: polish
description: >
  Completion-claim gate. Before any "completed" / "done" / "passed" claim, output the self-check table. If ANY row is ✗, fix it first — do NOT report completion. Lean discipline-gate version (not the full quality-loop polish).
  Triggers: "polish", "완료 점검", "done check", "ready to ship", "PR ready", "완료 선언 전"
version: 0.1.0
ssl:
  scheduling:
    anti_triggers:
      - "Full production-quality polish loop (Phase 1 inspection × N + e2e + PR doc) — use oh-my-borory:polish"
      - "Session-action audit (philosophy/scope) — use galmuri:self-audit"
      - "SKILL.md SSL audit — use galmuri:skill-audit"
      - "Test-gap / coverage inspection — use galmuri:ralphi"
  structural:
    scenes: [Gather context, Run checklist, Halt-or-Pass]
    resumable: false
    branches:
      - "any row ✗ → halt + fix + re-run; do NOT emit completion claim"
      - "all rows ✓ → emit completion claim and link the commit"
      - "context budget > 80% used → write tmp/polish-handoff-<ts>.md, STOP, wait for 'continue'"
  logical:
    tools: [Bash, Read]
    side_effects:
      reads: ["git diff", "git status", "git log -1", "current branch name", "tokens / design-system file when present"]
      writes:
        - "tmp/polish-handoff-<ts>.md when context budget exceeded"
      deletes: []
      network: []
    idempotent: true
    rollback: null
---

# galmuri:polish — completion-claim gate

> "검증 없이 완료 선언하지 않는다." A short, hard gate to run **before** saying *done* / *완료* / *passed*. If any row is ✗, fix it; do not declare completion.

If invoked bare (no scope hint), ask: *"What are you about to declare complete? e.g. `feat/foo branch`, `UI refactor`, `migration 0042` — name the scope so the checklist evidence makes sense."*

This is the **discipline-gate** version. For the full quality-improvement loop (6-axis inspection × N + e2e + PR doc), use `oh-my-borory:polish`.

## Step 1: Gather context

Cheap reads only — no full-file scans.

```bash
git status --short
git diff --stat
git branch --show-current
git log -1 --pretty='%h %s'
```

Note the baseline branch + SHA explicitly — the checklist below references it.

## Step 2: Run the Self-Check Gate

Output **exactly** the following table. Every row must resolve to ✓ or ✗ — no `n/a`, no `pending`. If a row genuinely does not apply (e.g. no UI changes → testid row), mark it ✓ with `evidence: scope-not-applicable`.

```
| Check                                                          | Status | Evidence                                  |
|----------------------------------------------------------------|--------|-------------------------------------------|
| Branch is feature/* (not main/master/release/*)                | ✓/✗    | `git branch --show-current`               |
| Pre-commit hooks ran successfully                              | ✓/✗    | last hook exit code (or `.husky/pre-commit` ran) |
| Baseline branch + SHA explicitly stated for comparisons        | ✓/✗    | quote the SHA                             |
| No `withTimeout`, defensive `{ timeout }`, or silent try/catch | ✓/✗    | `rg 'withTimeout\|timeout:\s*\d+' diff`   |
| No hardcoded version field names (`v1.*`, `schema_v2`)         | ✓/✗    | `rg 'v\d+\.\w+\|schema_v\d' diff`         |
| testid constants are UPPER_SNAKE_CASE                          | ✓/✗    | `rg 'data-testid="[a-z]' diff`            |
| No raw px values outside design tokens                         | ✓/✗    | manual diff inspection / tokens file      |
| Long reports (>30 lines) written to docs/reports/ not chat     | ✓/✗    | inspect last chat output                  |
| Pixel-delta table present when claim is UI work                | ✓/✗    | path to pixel-delta artifact (or scope-not-applicable) |
| Locale separation respected (en/ko/jp files do not mix)        | ✓/✗    | `rg -l '[가-힣]\|[ぁ-ヿ]' *.md` filtered  |
```

### Token Efficiency

After the table:

- If the cycle exceeded **80% of context budget**, write a handoff note to `tmp/polish-handoff-<ts>.md` and STOP. Wait for an explicit "continue".
- Never restate the entire diff in chat — summarize and link to the commit hash.

## Step 3: Halt-or-Pass

- **Any ✗** → halt. List each ✗ row with the fix command, apply fixes, re-run Step 2. Do **not** emit a completion claim until all rows are ✓.
- **All ✓** → emit one line: `polish gate clean: {commit-hash} ready.` That is the *only* form of completion claim allowed.

## What this skill does NOT do

- ✗ Run inspections / write tests / generate PR docs (that's `oh-my-borory:polish` or `harnish:ralphi`)
- ✗ Modify any code by itself — it only verifies *what you already did*
- ✗ Replace `galmuri:self-audit` (which audits Claude's own session actions across all axes, not just completion claims)
