---
name: qa-test
version: 1
description: >-
  Orchestrate multi-dimension QA — functional, network, performance, responsive, console, visual/DOM diff — with `chrome-devtools-axi` as driver (snapshot loop, Lighthouse, CWV, heap, emulation) and `agent-browser` for what AXI lacks (visual `diff`, HAR, auth vault, multi-session, cloud, iOS). Trigger on "QA this feature", "regression on X", "check Lighthouse on Y", or `/qa-test`. Sibling of `agent-browser` — pick that for one-off browsing; pick this for a structured plan under `./.plans/qa-test/<run-id>/`. Resumable; reads prior state first; never generates test code.
---

# qa-test

QA-test web applications against user instructions, picking the right CLI per dimension. `chrome-devtools-axi` is the default driver: snapshot+ref loop with loud `STALE_REF` errors, Lighthouse, Core Web Vitals insights (LCP/INP/CLS), heap snapshots, and built-in emulation — plus contextual `help[N]` planning hints after each command. `agent-browser` handles only what AXI lacks: visual/DOM `diff` family (Myers + pixel), HAR export, encrypted auth vault, multi-session isolation, cloud providers, iOS Simulator, and the `find text|label|role|placeholder|testid` semantic locator fallback when AXI refs churn. Runs are resumable: every test step is a three-state checkbox in `./.plans/qa-test/<run-id>/PLAN.md`, and the workflow reads prior state before acting.

## Core rules

1. **One run = one directory under `./.plans/qa-test/<run-id>/`.** `<run-id>` is `YYYY-MM-DD-HHMM-<slug>`. Never write outside this dir except for global CLI artefacts. Project-scoped only — fail if not inside a git repo.
2. **Read state before write.** On every invocation, list existing `./.plans/qa-test/`, summarise prior runs, and ask before resuming, starting fresh, or overwriting. Apply the [RESUMING.md](RESUMING.md) protocol verbatim.
3. **Default to `chrome-devtools-axi`; reach for `agent-browser` only when AXI lacks the capability.** AXI handles functional, network, console, performance, screenshot, emulation, multi-page. Switch to `agent-browser` for: visual/DOM `diff` family, HAR export, encrypted auth vault, multi-session isolation, cloud providers, iOS Simulator, and the `find text|label|role|placeholder|testid` ref-stability fallback. Full mapping in [TOOL-MATRIX.md](TOOL-MATRIX.md). Mixing both in one run is normal — keep separate sessions per CLI.
4. **Honour the non-negotiables in [RULES.md](RULES.md).** Stale-ref recovery, network-capture priming, `wait` content over `wait` timeouts, no `eval` with secrets, one perf trace per page.
5. **Three-state checkboxes only.** `[ ]` pending, `[x]` complete, `[~] — <reason>` skipped. Skipped items preserve the audit trail; never silently delete.
6. **Evidence goes to disk, never to context.** Screenshots, HARs, Lighthouse reports, heap snapshots, response bodies all land under `./.plans/qa-test/<run-id>/evidence/`. Reference paths in `RESULTS.md`; do not inline binaries.
7. **Auto-install on first run.** If either CLI is missing, run `scripts/preflight.sh` which installs `chrome-devtools-axi` and `agent-browser` globally via npm and runs `agent-browser doctor --offline --quick --json`. Surface install + doctor output before proceeding.
8. **Pin behaviour, not versions, in CI.** Inside the per-run dir, write the resolved CLI versions into `ENV.md` so reruns are reproducible. Do not pass `@latest` in the auto-install command — the script pins what it installs.

## Workflow

### 0. Sanity

Verify `git rev-parse --show-toplevel` succeeds (project-scoped state requires a repo). List `./.plans/qa-test/`; if prior runs exist, apply [RESUMING.md](RESUMING.md) before starting intake.

### 1. Intake

Collect: target URL(s), feature/flow under test, auth strategy (none / vault / `--auto-connect` / session), QA dimensions in scope (functional, visual, network, performance, responsive, console), pass/fail criteria, baseline references for diffs (if any). Bundle 2–4 questions per round if anything is missing.

### 2. Preflight

Run `bash scripts/preflight.sh` — auto-installs missing CLIs, probes `chrome-devtools-axi --help` to verify the binary is functional, runs `agent-browser doctor --offline --quick --json`, writes installed versions into `ENV.md`. Exit codes: `0` ready; `1` install attempted, doctor passed (continue); `2` install failed or AXI binary not functional (stop and report); `3` not in a git repo (stop); `4` doctor reported failures (show output and ask the user whether to continue).

### 3. Plan

Create `./.plans/qa-test/<run-id>/PLAN.md`. Group steps by dimension; each step is a three-state checkbox with the exact CLI command and the assertion. Concrete example in [WORKFLOW.md](WORKFLOW.md) §3.

### 4. Execute

Walk `PLAN.md` top-to-bottom. For each `[ ]` item: run the command, capture evidence under `evidence/`, mark `[x]` on pass, `[~] — <reason>` on intentional skip, or leave `[ ]` and append a failure note for hard failures. Console errors captured during functional steps are soft fails unless the step explicitly expects errors. Tool-selection rules and per-dimension idioms in [TOOL-MATRIX.md](TOOL-MATRIX.md). Stale-ref recovery and network-prime sequencing in [RULES.md](RULES.md).

### 5. Resume (when re-invoked)

Apply [RESUMING.md](RESUMING.md): read `PLAN.md`, summarise `[x]` / `[~]` / `[ ]` counts, ask whether to resume from the first `[ ]`, restart a specific step, or open a new run.

### 6. Report

Write `RESULTS.md` in the run dir: pass/fail per dimension, links to evidence files, list of soft failures (console errors, perf-budget misses), and the `STATUS.md` rollup (`pass` / `fail` / `partial`). Surface the run-dir path in the user-facing summary.

## Companion files

- [RULES.md](RULES.md) — non-negotiables (stale-ref recovery, network prime, networkidle gotcha, perf-trace constraints, eval safety).
- [TOOL-MATRIX.md](TOOL-MATRIX.md) — per-dimension tool selection + canonical command snippets for both CLIs.
- [WORKFLOW.md](WORKFLOW.md) — step-by-step execution with worked examples per QA dimension.
- [RESUMING.md](RESUMING.md) — state-file schema and resume protocol.
- `scripts/preflight.sh` — install + doctor preflight; structured exit codes.
