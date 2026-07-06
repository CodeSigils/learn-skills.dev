---
name: risk-based-testing
description: >-
  Perform product risk analysis and prioritize test effort by risk level
  (likelihood × impact), per ISTQB CTFL v4.0 §5.2. Use when: "risk-based testing,"
  "リスクベースドテスト," "risk analysis," "risk matrix," "what should we test first,"
  "limited time, where to focus testing," or scoping/prioritizing a test effort.
  Produces a product risk register + risk matrix that drives scope, levels, types,
  techniques, coverage, and effort — and feeds the test strategy. Output is a
  prioritization artifact (design mode). Not for: the full strategy document — use
  test-strategy-doc, which consumes this. Related: test-strategy-doc, exploratory-testing.
license: MIT
metadata:
  version: "1.0"
  istqb: "CTFL v4.0 §5.2"
  iso25010: [functional-suitability, performance-efficiency, compatibility, interaction-capability, reliability, security, maintainability, flexibility, safety]
  mode: [design]
---

# Risk-Based Testing

Focus limited test effort where failure is most likely and most damaging — by
analyzing product risk and letting risk level drive every scope decision.

## Objective

A product risk register where each risk has a likelihood, an impact, a derived risk
level, and a mitigation (the tests that reduce it), used to prioritize testing. Per
CTFL v4.0 §5.2.1, a risk is characterized by **risk likelihood** (probability of
occurrence) and **risk impact** (harm), and these combine into a **risk level**. Per
§5.2.3, product risk analysis focuses testing to minimize **residual** product risk.
The failure mode this prevents: spreading effort evenly and under-testing the one
high-likelihood, high-impact area that actually takes the release down.

## Context Discovery

- What can fail, and how bad is it? Map risks across functional areas, integrations,
  third-party dependencies, performance/security-sensitive paths, and new/changed code
  (churn + complexity are likelihood signals — read git history).
- Business/impact context: revenue paths, compliance exposure, user-facing criticality
  (drives impact scoring).
- Time/resource constraints: the tighter these are, the more prioritization matters.
- Who owns risk acceptance? Out-of-scope areas need a named owner who accepts the gap.

## Instructions

1. **Identify product risks**: enumerate potential failure areas. Tie each to an
   ISO/IEC 25010 quality characteristic so non-functional risks (security, performance,
   reliability, …) are considered, not just functional ones.

2. **Assess likelihood and impact** (§5.2.1): rate each on a defined scale (e.g.
   Low/Med/High or 1–5). Use concrete criteria, not gut feel — e.g. likelihood from
   code complexity/churn/novelty; impact from users affected × severity.

3. **Compute risk level and rank**: combine via a risk matrix (likelihood × impact).
   Sort by level to get the test-priority order.

4. **Derive testing from risk** (§5.2.3): risk level determines **scope**, **test
   levels/types**, **techniques**, **coverage depth**, **effort**, and **execution
   order** (highest-risk first, to find critical defects early). Each high/critical risk
   maps to specific mitigation tests.

5. **Control and monitor risk** (§5.2.4): mitigation = the planned tests; monitoring =
   re-assess as results arrive. If high-risk areas reveal few defects and low-risk
   areas reveal many, re-prioritize. Reserve effort for emerging/unknown risks.

6. **Record residual risk**: what remains untested and who accepted it.

## Output Format

### design mode

Product risk register / matrix:

```
| Risk ID | Risk (area / failure) | ISO 25010 char | Likelihood | Impact | Level | Priority | Mitigation tests | Owner | Residual |
| R-01 | Payment double-charge under retry | Functional Suitability | High | Critical | Critical | P1 | decision-table + state-transition on retry paths | QA lead | Low |
| R-07 | Slow search over large catalog | Performance Efficiency | Med | High | High | P2 | load test @ 10× volume | Perf | Med |
```

Plus a short narrative: prioritization order, what is out of scope and who accepted it,
and the monitoring trigger for re-assessment.

## Anti-Patterns

- **Static risk assessment** — analyzed once, never revisited as testing reveals
  reality. **Guard:** monitoring step (§5.2.4); re-rank when results contradict the
  initial scoring.
- **Vague, unmeasurable risks** — "performance is risky." **Guard:** state the risk
  concretely with a condition/threshold and a mitigation test.
- **Likelihood/impact from gut** — numbers with no rationale. **Guard:** score against
  defined criteria (churn/complexity for likelihood; users×severity for impact) and
  record the reason.
- **Risk without a mitigating test** — a Critical risk that nothing in the plan
  addresses. **Guard:** every high/critical risk maps to specific tests.
- **Only known risks** — ignoring unknown-unknowns. **Guard:** reserve effort (e.g.
  exploratory sessions) for emerging risks.

## Related Skills

- `test-strategy-doc` — consumes this register as its risk-based scope section (§5).
- `exploratory-testing` — charters aimed at the highest-risk areas.
- The test-design skills — execute the mitigation tests each risk calls for.

## References

- ISTQB CTFL v4.0 Syllabus §5.2 (Risk Management): §5.2.1 Risk Definition and Risk
  Attributes, §5.2.2 Project Risks and Product Risks, §5.2.3 Product Risk Analysis,
  §5.2.4 Product Risk Control
- ISO/IEC 25010:2023 — quality characteristics used to classify product risks
