---
name: funnel-planner
description: "This skill should be invoked when the user needs to set numeric business targets, model a funnel, or validate whether the math works for a business goal. Triggers include 'set targets', 'plan a funnel', 'create OKRs', 'what business metrics should I track', 'how many users do I need to hit [goal]', 'will the numbers work', 'is my pricing sustainable', 'what conversion rate do I need', 'forecast', 'can we actually hit this number', 'scenario modeling', 'financial model', 'unit economics', 'pricing model', or 'path to profitability' -- even if they just say 'can we hit $X', state a revenue target and need the funnel math worked backward, or have prioritized initiatives that need numeric targets. Not for mapping activities to existing KPIs (use attribution), testing a specific price or variant with users (use experiment), defining experiment success metrics or sample sizes (use experiment), diagnosing why metrics are problematic (use problem-analysis), or benchmarking a specific page's conversion rate (use lp-optimization)."
license: MIT
metadata:
  author: hungv47
  version: "3.2.1"
---

# Funnel Planner — Target Setting

*Strategy — Step 3 of 4. Sets data-driven targets for each prioritized initiative.*

**Core Question:** "Do the numbers actually work?"

## Philosophy

Improvement factors and benchmarks here are evidence-backed starting points. Actual achievable improvement depends on baseline, team capability, and market context. Use the defaults as sanity checks, not ceilings or floors.

## Inputs Required
- Prioritized initiatives from `.agents/solution-design.md` (preferred)
- OR: A business with metrics that need targets

## Output
- `.agents/targets.md`

## Quality Gate
Before delivering, verify:
- [ ] Every target has a numeric baseline (zero "TBD" values)
- [ ] Every target cites a justification: historical data, benchmark, or calculated improvement factor
- [ ] 70% test passes: hitting 70% of each target is still valuable
- [ ] LTV:CAC ≥ 3:1 (if acquisition targets involved) — or flagged as unhealthy

## Chain Position
Previous: `solution-design` | Next: `experiment`

**Re-run triggers:** When baselines shift >20% from target table values, after experiments conclude with new data, or quarterly.

---

## Before Starting

### Step 0: Product Context

Check for `.agents/product-context.md`. If missing: **Strongly recommended:** run `icp-research` (from `hungv47/comms-skills`) first to create `.agents/product-context.md` — this skill works without it but produces significantly better analysis with it. If the user prefers not to, ask the user 8 product questions (what, who, problem, differentiator, proof points, pricing, objections, voice) and save to `.agents/product-context.md`.

If upstream artifacts' `date` fields are older than 30 days, recommend re-running upstream skills before proceeding — stale baselines produce unreliable targets.

### Required Artifacts
| Artifact | Source | If Missing |
|----------|--------|------------|
| `solution-design.md` | solution-design | **INTERVIEW.** Ask what initiatives to set targets for. |

### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `product-context.md` | icp-research (from hungv47/comms-skills) | Business model context for benchmark selection |

### Initiative Review
Read `.agents/solution-design.md` if it exists — set a target for each "Proceed" initiative. If it doesn't exist, interview for:
- What business type? (SaaS, e-commerce, B2B services, etc.)
- What stage? (Pre-launch, early traction, growth, mature)
- What metrics need targets?

---

## Step 1: Choose Funnel Model

| Model | Best For | Stages |
|-------|----------|--------|
| **AARRR** | SaaS, apps | Acquisition → Activation → Retention → Revenue → Referral |
| **AIDA** | E-commerce, D2C | Awareness → Interest → Desire → Action |
| **TOFU-MOFU-BOFU** | B2B, long sales | Top → Middle → Bottom |

See [references/funnel-models.md](references/funnel-models.md) for detailed stage definitions.

---

## Step 2: Collect Baselines

Collect the current number for each metric — baselines are necessary because targets without baselines become arbitrary guesses.

If user lacks data, use WebSearch to find industry benchmarks:
- `"[industry] [metric] benchmark [year]"` (e.g., "B2B SaaS trial conversion benchmark 2025")
- `"[business type] average [metric] by stage"` (e.g., "Series A SaaS average churn rate")
- `"[metric] good vs bad [industry]"` (e.g., "email open rate good vs bad SaaS")

See [references/benchmarks.md](references/benchmarks.md) for reference ranges. Note: benchmarks are starting points, not guarantees.

---

## Step 3: Set Targets

For each initiative/metric:

| Scenario | Improvement Factor |
|----------|-------------------|
| No optimization yet | 20-30% lift |
| Basic optimization done | 10-15% |
| Mature funnel | 5-10% |
| Major redesign or fix | 30-50% |

Typical ranges, not guarantees. A team fixing a known broken page may see 100%+ lift; a team optimizing an excellent funnel may see 2-3%. Ground targets in evidence (baseline + realistic improvement), not in this table.

**LTV:CAC sanity check** (for acquisition targets):
- LTV:CAC should be ≥ 3:1, ideally 5:1
- Payback < 12 months (SMB) or < 18 months (mid-market)
- If targets imply unhealthy economics, flag it explicitly

See [references/unit-economics.md](references/unit-economics.md) for formulas.

### Pricing Health Signals

If you're setting acquisition or revenue targets, check for pricing misalignment:

| Signal | What It Means | Action |
|--------|--------------|--------|
| Conversion rate >40% | Likely underpriced — you're not losing anyone on price | Test a 15-20% price increase |
| Churn <3% + no price complaints | Room to increase pricing | Test higher tier or annual pricing |
| Win rate drops when price discussed | Price objection is real | Improve value communication before raising |
| Competitors pricing 2x+ higher | Either they're overcharging or you're undervaluing | Run Van Westendorp survey to find optimal zone |

**Van Westendorp Price Sensitivity:** A 4-question survey to find the optimal price range. Ask:
1. At what price would this be too expensive? (ceiling)
2. At what price would this be too cheap / suspicious? (floor)
3. At what price is this expensive but acceptable? (upper bound)
4. At what price is this a great deal? (lower bound)

Plot the four curves — the intersections reveal the acceptable price range and optimal point.

### Speed-to-Lead (B2B targets)

If targets involve lead response or qualification:

| Response Time | Qualification Likelihood |
|--------------|------------------------|
| <5 minutes | 21x more likely to qualify |
| 5-30 minutes | Baseline |
| 30 min - 24 hours | 10x drop from baseline |
| >24 hours | Effectively cold |

If your funnel has a lead stage, include response time SLA as a target: contact within 4 hours, qualify/reject within 48 hours. Speed-to-lead is often the highest-leverage conversion lever in B2B funnels — it's free and just requires process discipline.

---

## Step 4: Validate

### Anti-Pattern Check

| Anti-Pattern | Detection |
|--------------|-----------|
| **Vanity Metric** | Doesn't connect to revenue → find the revenue-connected metric |
| **Sandbagging** | 100% confidence, zero stretch → add 30-50% |
| **Moonshot** | 10x improvement, no plan → work backwards from realistic |
| **Orphan Target** | Owner is "the team" → assign a person |
| **Input Trap** | Measuring activities ("publish 4 posts") → measure the output ("organic signups") |
| **Aspirational math** | Target significantly above good-tier benchmark (roughly >1.5x) without written justification for why your situation enables outperformance. The further above benchmark, the stronger the justification needs to be. |

See [references/anti-patterns.md](references/anti-patterns.md) for detailed detection.

### Stress Tests

1. **Revenue test:** If we hit this but revenue doesn't move, was it worth it?
2. **70% test:** If we hit 70%, is that still valuable? Context matters:
   - *Higher-is-better metrics* (conversion, retention): 70% of target is acceptable IF it's still above industry benchmark. If 70% puts you below benchmark, your target is too low.
   - *Lower-is-better metrics* (churn, CAC): 70% of target means you achieved only 70% of the reduction — almost always still worth doing.
   - *Binary thresholds* (LTV:CAC ≥3:1): 70% = 2.1:1 — this is still broken. Don't accept 70% on binary targets; they pass or fail.
3. **Ownership test:** Who owns this? What are they NOT doing to focus on it?
4. **Measurement test:** Can we check this weekly, or only at period end?

See [references/stress-tests.md](references/stress-tests.md) for stage-specific questions.

---

## Artifact Template

On re-run: rename existing artifact to `targets.v[N].md` and create new with incremented version.

```markdown
---
skill: funnel-planner
version: 1
date: {{today}}
status: draft
---

# Targets

**Funnel Model:** [AARRR / AIDA / TOFU-MOFU-BOFU]

## Target Table

| Initiative | Metric | Baseline | Benchmark (Good) | Target | Variance vs. Benchmark | Justification | Owner |
|-----------|--------|----------|-------------------|--------|----------------------|---------------|-------|
| [Name] | [Metric] | [Current] | [Industry ref] | [Goal] | [+X% above benchmark or within range] | [Why achievable — cite evidence] | [Person] |

If Variance > 50% above good-tier benchmark, flag: "This target requires significantly above-average performance. Justification: [why your situation is different]."

## Validation

### Anti-Patterns: [None detected / List any found + fixes]
### 70% Test: [Pass/fail per target]
### LTV:CAC Check: [Ratio] — [Healthy / Flag]

## Baseline Handoff to Experiment

Every target in this table becomes a baseline for `experiment`. When running `experiment`, the baseline MUST match the number in this table — if it doesn't, update this table first. Stale baselines produce incorrect sample size calculations and misleading lift targets.

## Next Step

Run `experiment` to design minimum viable tests before full rollout. Pass this artifact as required input — experiment should read baselines from this table, not re-interview for them.
```

---

## Worked Example

```markdown
# Targets

**Date:** 2026-03-13
**Skill:** funnel-planner
**Funnel Model:** AARRR

## Target Table

| Initiative | Metric | Baseline | Benchmark | Target | Justification | Owner |
|-----------|--------|----------|-----------|--------|---------------|-------|
| Restore Paid Targeting | Paid visitor signup rate | 1.2% | 3-5% (B2B SaaS median) | 3.0% | Was 3.5% before targeting change; conservative recovery with lookalike | Sarah |
| Restore Social Proof | Homepage bounce rate | 52% | 30-40% (B2B SaaS) | 40% | Old homepage was 35%; restoring trust signals should recover most of gap | James |
| Overall | Weekly signups | 200 | — | 300 | Combined effect: paid fix (150 → 225 from paid) + bounce fix (all sources) | Sarah (owner) |

## Validation

### Anti-Patterns: None detected. All targets have baselines, single owners, revenue connection.
### 70% Test: Hitting 70% (2.5% paid rate, 43% bounce, 270 signups) still represents meaningful recovery from 200.
### LTV:CAC Check: Current CAC $120, LTV $1,800 → 15:1 ratio. Healthy even if CAC rises 50%.

## Next Step

Run `experiment` to design A/B test for paid targeting and before-after for social proof restoration.
```

---

## References

| Reference | Use For |
|-----------|---------|
| [funnel-models.md](references/funnel-models.md) | Stage definitions, model selection |
| [benchmarks.md](references/benchmarks.md) | Industry benchmarks by stage |
| [anti-patterns.md](references/anti-patterns.md) | Target-setting pitfalls |
| [stress-tests.md](references/stress-tests.md) | Target validation questions |
| [unit-economics.md](references/unit-economics.md) | LTV:CAC, payback formulas |
