---
name: qa-metrics
description: >-
  Define test metrics and write test progress / completion reports per ISTQB CTFL v4.0
  §5.3 (Test Monitoring, Test Control and Test Completion). Use when: "test metrics,"
  "テストメトリクス," "test progress," "進捗レポート," "QA dashboard," "test completion
  report," "test summary report," "are we ready to release (by the numbers)," or
  monitoring/reporting a test effort. Produces a metric set + progress and completion
  report templates (design mode). Not for: defining the strategy, quality gates, or
  exit criteria up front — use test-strategy-doc, which this skill then monitors against.
  Related: test-strategy-doc, risk-based-testing, defect-report.
license: MIT
metadata:
  version: "1.0"
  istqb: "CTFL v4.0 §5.3"
  iso25010: [functional-suitability, performance-efficiency, compatibility, interaction-capability, reliability, security, maintainability, flexibility, safety]
  mode: [design]
---

# QA Metrics & Test Reporting

Track testing against the plan with metrics that drive decisions, and report status so
stakeholders can act — monitoring, control, and completion, not a wall of numbers.

## Objective

A decision-driving metric set (from the CTFL v4.0 §5.3.1 categories) plus a test
**progress** report (ongoing control) and a test **completion** report (at exit),
tied to the plan's exit criteria. The failure mode this prevents: "testing is going
fine" with no numbers, and a completion report that says "we tested a lot" instead of
"exit criteria met / not met, here's the residual risk."

## Organization-specific inputs (fill these in)

- **Which metrics matter here** and their thresholds (the exit-criteria numbers this
  effort is monitored against — usually defined by `test-strategy-doc`).
- **Cadence & audience**: progress-report frequency (daily/weekly) and who reads it;
  completion-report template and its broader audience.
- **Data sources / tooling**: test management + CI + defect tracker the metrics pull from.
- **Release-readiness rule**: what metric state means "go."

## Context Discovery

- What are the plan's exit criteria and targets? (this skill measures against them)
- What data is available (test runs, defects, coverage, risk register)?
- Who needs which report, how often, in what format?

## Instructions

1. **Select metrics from the CTFL §5.3.1 categories** — pick what informs a decision,
   not everything measurable:
   - **Project progress** (task completion, resource usage, effort)
   - **Test progress** (tests implemented, environment readiness, run/not-run,
     passed/failed, execution time)
   - **Product quality** (availability, response time, MTTF)
   - **Defect** (found/fixed counts and priorities, defect density, detection %)
   - **Risk** (residual risk level)
   - **Coverage** (requirements coverage, code coverage)
   - **Cost** (cost of testing, cost of quality)

2. **Monitor and control**: compare actuals vs the plan; when metrics deviate, act —
   re-prioritize (feed `risk-based-testing`), adjust schedule/scope, or escalate. Metrics
   without a resulting decision are vanity.

3. **Write test progress reports** (§5.3.2), regularly: test period; progress vs plan
   (ahead/behind, deviations); impediments and workarounds; the metrics; new/changed
   risks; what's planned next. Audience: usually same-team, frequent, can be informal.

4. **Write the test completion report** (§5.3.2) at exit (project/level/type complete,
   exit criteria ideally met): summary; quality/testing evaluation vs the original plan;
   deviations; impediments; unmitigated risks and unfixed defects; lessons learned.
   Audience: broader; follows a template; produced once.

5. **State release-readiness explicitly**: exit criteria met or not, with the numbers
   and the residual risk — not a subjective "looks good."

## Output Format

### design mode

```
# Metrics & Reporting Plan: {effort}
## Metric set (category → metric → source → target/threshold)
## Test Progress Report (template)
   - Period · progress vs plan · impediments · metrics · new risks · next period
## Test Completion Report (template)
   - Summary · quality vs plan · deviations · unmitigated risks / unfixed defects
   - Exit-criteria check (met? numbers) · lessons learned
```

## Anti-Patterns

- **Vanity metrics** — "1,200 tests run" with no pass/defect/coverage context. **Guard:**
  every metric ties to a decision or an exit criterion.
- **A single number** — test count alone, no defect or coverage view. **Guard:** cover
  the relevant §5.3.1 categories, not one.
- **Metrics with no control action** — reporting deviation but never acting. **Guard:**
  monitoring feeds control (re-prioritize/adjust/escalate).
- **Completion report without an exit-criteria check** — "we tested" ≠ "criteria met."
  **Guard:** the completion report states exit criteria met/not with numbers + residual risk.
- **No baseline** — metrics with nothing to compare against. **Guard:** measure vs the
  plan's targets (from `test-strategy-doc`).

## Related Skills

- `test-strategy-doc` — defines the exit criteria and quality gates this skill monitors
  against (strategy is up front; this is ongoing + at completion).
- `risk-based-testing` — supplies/consumes the risk metrics; deviations re-open risk.
- `defect-report` — the source of the defect metrics.

## References

- ISTQB CTFL v4.0 Syllabus §5.3 (Test Monitoring, Test Control and Test Completion):
  §5.3.1 metrics (seven categories), §5.3.2 test progress vs completion reports
- ISO/IEC/IEEE 29119-3 — templates/examples for test status (progress) and completion
  reports (referenced by the syllabus)
