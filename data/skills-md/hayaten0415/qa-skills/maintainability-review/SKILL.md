---
name: maintainability-review
description: >-
  Assess and improve maintainability and testability for the ISO/IEC 25010:2023
  Maintainability characteristic (modularity, reusability, analysability,
  modifiability, testability). Use when: "maintainability," "testability," "保守性,"
  "テスト容易性," "is this code testable," "mutation testing," "cyclomatic
  complexity," "test suite effectiveness," "why is coverage high but bugs still ship,"
  or reviewing code for change-risk. Produces a testability/maintainability review
  with objective metrics (design mode) and mutation-testing / static-analysis gates
  (implementation mode). Not for: measuring statement/branch coverage — use
  white-box-coverage; reviewing work products for defects — use static-review; or
  functional test-case design — use the test-design skills. Related:
  white-box-coverage, boundary-value-analysis, test-strategy-doc.
license: MIT
metadata:
  version: "1.0"
  istqb: "CTFL v4.0 §2.2.1 (maintainability testing)"
  iso25010: [maintainability]
  mode: [design, implementation]
---

# Maintainability Review

Judge how safely the code can change — and how well the test suite actually protects
it — with objective metrics, not opinion.

## Objective

A review of the five ISO 25010:2023 Maintainability sub-characteristics — modularity,
reusability, analysability, modifiability, **testability** — anchored to measurable
signals (complexity, duplication, coupling, coverage, mutation score). Because
maintainability is an internal quality, the QA angle is **testability + test-suite
effectiveness**. The failure mode this prevents: "90% coverage" that still ships bugs
because the tests assert almost nothing.

## Context Discovery

- **Where does change hurt?** Ask which modules are churned + defect-prone (git log +
  bug tracker) — target the review there, not uniformly.
- **Existing metrics**: is complexity/duplication/coverage already measured (SonarQube,
  CI reports)? Read them before generating new ones.
- **Test-suite trust**: does the team trust the suite to catch regressions? Distrust is
  the symptom mutation testing quantifies.
- **Stack**: language selects tooling (Stryker/PIT, radon, ESLint, SonarQube).

## Instructions

1. **Testability review** — the QA-central sub-characteristic. Assess three properties
   per unit under review:
   - **Controllability** — can inputs/state be driven from a test? (hidden globals,
     hard-wired clocks/IO reduce it)
   - **Observability** — can outputs/effects be observed? (fire-and-forget side effects
     reduce it)
   - **Isolatability** — can it be tested without spinning up the world? (tight
     coupling forces heavyweight tests)
   Low scores predict brittle, slow, or absent tests — flag with the refactor (inject
   dependencies, extract pure functions, seams for IO).

2. **Measure test-suite effectiveness with mutation testing**: coverage proves lines
   *ran*, not that a bug would be *caught*. Run mutation testing; a low mutation score
   with high coverage means assertions are weak. Target the critical modules first
   (mutation testing is slow).

3. **Objective code metrics** (analysability/modifiability/modularity):
   - **Cyclomatic complexity** (McCabe) — flag high-complexity functions (harder to
     test and change; more paths to cover).
   - **Duplication** — duplicated blocks multiply change cost and drift risk.
   - **Coupling/cohesion** — high coupling → a change ripples (hurts modularity).
   - **Maintainability Index** as a rolled-up trend signal (not an absolute verdict).

4. **Coverage as a floor, not a goal**: use branch coverage to find *untested* code,
   then mutation score to judge whether the covering tests are meaningful. Never report
   coverage alone as quality.

5. **Prioritize by change-risk**: recommend refactors where complexity/duplication
   overlaps with high churn and low mutation score — that intersection is where
   maintainability defects actually cost money.

## Output Format

### design mode

```
# Maintainability & Testability Review: {module/service}
## Metrics snapshot
   | Module | Cyclomatic (max/avg) | Duplication % | Branch cov | Mutation score | Churn |
## Testability findings (controllability / observability / isolatability + refactor)
## Change-risk hotspots (complexity × churn × weak tests)
## Recommendations (prioritized) and target thresholds
```

### implementation mode

Mutation-testing + static-analysis gates. StrykerJS example:

```jsonc
// stryker.conf.json — gate CI on mutation score for critical paths
{ "testRunner": "vitest", "coverageAnalysis": "perTest",
  "mutate": ["src/pricing/**/*.ts", "src/auth/**/*.ts"],
  "thresholds": { "high": 80, "low": 70, "break": 60 } }   // build fails below 60
```

Also wire complexity/duplication thresholds (SonarQube quality gate, ESLint
`complexity` rule, or `radon cc` for Python). Verify tool/config keys against installed
versions.

## Anti-Patterns

- **Coverage as the quality metric** — the classic trap; 100% coverage with
  assertion-free tests catches nothing. **Guard:** pair coverage with a mutation score;
  report both.
- **Metrics without change-risk context** — refactoring a complex-but-stable module
  nobody touches. **Guard:** weight findings by churn; act where complexity meets churn.
- **Testability judged by feel** — "this looks testable." **Guard:** score
  controllability/observability/isolatability explicitly with the reason.
- **Hallucinated thresholds as standards** — presenting "complexity must be < 10" as an
  ISO rule. **Guard:** ISO 25010 defines characteristics, not numeric limits; label
  thresholds as team policy, and cite the metric's real source (McCabe, MI).
- **Gaming the Maintainability Index** — chasing a single composite number. **Guard:**
  treat MI as a trend, not a target; look at the underlying complexity/duplication.

## Related Skills

- `boundary-value-analysis` and other test-design skills — mutation testing reveals
  which of their assertions are too weak.
- `test-strategy-doc` — sets whether maintainability is an explicit quality goal.

## References

- ISO/IEC 25010:2023 — Maintainability (modularity, reusability, analysability, modifiability, testability)
- ISO/IEC 25023:2016 — measurement of product quality (maintainability measures)
- Cyclomatic Complexity (McCabe, 1976); Maintainability Index (Oman & Hagemeister)
- Tools: Stryker/StrykerJS, PIT (Java), SonarQube, ESLint (complexity), radon (Python)
