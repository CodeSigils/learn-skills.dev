---
name: experiment
description: "This skill should be invoked when the user has a business idea or initiative and wants to validate it with a test before fully committing (not code testing or QA). Triggers include 'how do I test this', 'should I run an A/B test', 'prove this works first', 'how do I know if this will work', 'validate this idea with data', 'design an experiment', 'de-risk this launch', 'test our pricing', 'beta test', 'pilot program', 'soft launch', 'smoke test', or 'what's the cheapest way to learn' -- even if they are about to launch something and want confidence it will work, want to de-risk an idea with data, or have targets set and need to test before full rollout. Not for strategic prioritization (use solution-design), market sizing or feasibility research (use icp-research), modeling whether pricing math works (use funnel-planner), auditing an existing page's conversion (use lp-optimization), or diagnosing why metrics are declining (use problem-analysis)."
argument-hint: "[initiative to test]"
license: MIT
metadata:
  author: hungv47
  version: "1.2.1"
---

# Experiment Design

*Strategy — Step 4 of 4. Designs minimum viable tests with clear success/iterate/kill rules.*

**Core Question:** "What's the cheapest way to learn if this works?"

## Philosophy

Experimental rigor matters — but the level should match the stakes. Sample size tables assume 95% confidence / 80% power, appropriate for high-stakes decisions. For lower-stakes tests (social creative, email subjects), 90% confidence may suffice. Define acceptable risk upfront.

## Inputs Required
- An initiative with hypothesis and target metric (from `.agents/solution-design.md` + `.agents/targets.md`)
- Baselines from `.agents/targets.md` (required for sample size calculation and lift targets)
- OR: User describes what they want to test

## Output
- `.agents/experiment-[name].md`

## Quality Gate
Before delivering, verify:
- [ ] Executable in ≤2 weeks
- [ ] Costs <10% of full initiative budget (or $0 for internal-only changes)
- [ ] Success threshold is a specific number (not "significant improvement" or "we'll know it when we see it")
- [ ] Sample size is sufficient (checked against table below) — or test type adjusted if insufficient
- [ ] Guardrail metrics defined (metrics that must NOT get worse — e.g., support ticket rate, error rate, refund rate)

## Chain Position
Previous: `funnel-planner` | Next: implement winning variant, or re-diagnose with `problem-analysis` if inconclusive

**Re-run triggers:** When prior experiment results become stale (>60 days), when testing a new initiative from solution-design, or when baselines in targets.md are updated.

---

## Before Starting

### Step 0: Product Context

Check for `.agents/product-context.md`. If missing: **Strongly recommended:** run `icp-research` (from `hungv47/comms-skills`) first to create `.agents/product-context.md` — this skill works without it but produces significantly better analysis with it. If the user prefers not to, ask the user 8 product questions (what, who, problem, differentiator, proof points, pricing, objections, voice) and save to `.agents/product-context.md`.

If upstream artifacts' `date` fields are older than 30 days, recommend re-running upstream skills before proceeding — stale baselines invalidate sample size calculations.

### Required Artifacts
| Artifact | Source | If Missing |
|----------|--------|------------|
| `solution-design.md` | solution-design | **INTERVIEW.** Ask what to test. |
| `targets.md` | funnel-planner | **INTERVIEW.** Ask for baseline metrics. Baselines are required — without them, sample size and lift calculations are meaningless. |

### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `product-context.md` | icp-research (from hungv47/comms-skills) | Test design context |

### Initiative & Target Review
Read `.agents/solution-design.md` and `.agents/targets.md` if they exist. If not, interview for:
1. "What are you trying to test? What's your hypothesis?"
2. "What metric are you measuring? What's the current baseline?"
3. "What would success look like? What would make you stop?"

A hypothesis, a target metric, and a baseline number are the minimum required inputs — without them, success criteria become subjective.

---

## Step 1: Choose Test Type

| Type | When | Rigor |
|------|------|-------|
| **A/B Test** | Can split traffic randomly; enough volume | High — controls for time |
| **Before-After** | Can't split (infrastructure change, whole-site change) | Medium — time effects confound |
| **Cohort** | Testing on a specific segment first | Medium — segment differences |
| **Pilot** | New capability; need qualitative signal first | Low — directional only |

If unsure: check sample size (Step 3). Not enough volume for A/B in 2 weeks → use Before-After or Pilot.

---

## Step 2: Define Decision Rules

Define specific numeric thresholds — vague thresholds cause endless "let's give it one more week" cycles.

| Outcome | Threshold | Action |
|---------|-----------|--------|
| **Success** | [metric] ≥ [number] | Scale: roll out fully |
| **Iterate** | [metric] between [X] and [Y] | Change ONE variable: [specify which]. Rerun for [duration]. Max 2 iterations. |
| **Kill** | [metric] < [number] after [full duration] | Archive learnings. Re-diagnose using `problem-analysis`. |

**Guardrail check — response protocol:**

| Situation | Decision | Action |
|-----------|----------|--------|
| Primary succeeds, guardrails hold | **Success** | Scale as planned |
| Primary succeeds, guardrail breached slightly (<20% degradation) | **Conditional Success** | Reduce variant scope (e.g., show to 50% instead of 100%), rerun 7 days. If guardrail recovers and primary holds, scale. |
| Primary succeeds, guardrail breached severely (>20% degradation) | **Iterate** | The approach works but has side effects. Change the implementation to protect the guardrail, then retest. |
| Primary succeeds, guardrail breach is inherent to approach | **Kill** | The primary gain isn't worth the guardrail cost. Archive why and try a different approach via `solution-design`. |

---

## Step 3: Sample Size Check

For A/B tests — minimum visitors PER VARIANT:

| Baseline Rate | 20% Relative Lift | 50% Lift |
|--------------|-------------------|----------|
| 1% | ~40,000 | ~6,400 |
| 5% | ~8,000 | ~1,300 |
| 10% | ~4,000 | ~640 |
| 25% | ~1,600 | ~260 |

Assumes 95% confidence, 80% power. For exploratory tests, 90% confidence reduces required sample by ~25%. For critical decisions, consider 99%.

**Quick math:** [Your daily traffic] × [test days] ÷ 2 = visitors per variant. Compare against table.

If insufficient for A/B: use Before-After, or make a bigger change (aim for 50%+ lift instead of 20%).

See [references/sample-size-guide.md](references/sample-size-guide.md) for full tables.

---

## Artifact Template

On re-run: rename existing artifact to `experiment-[name].v[N].md` and create new with incremented version.

```markdown
---
skill: experiment
version: 1
date: {{today}}
status: draft
---

# Experiment: [Name]

**Initiative:** [from prioritized list]

## Design

| Field | Value |
|-------|-------|
| Hypothesis | If [action], then [metric] changes from [baseline] to [target], because [reason] |
| Test Type | A/B / Before-After / Cohort / Pilot |
| Duration | [≤2 weeks] |
| Budget | [$X or $0] |
| Primary Metric | [metric name] |
| Baseline | [current value] |
| Guardrail Metrics | [metrics that must NOT degrade — e.g., support tickets, error rate, refund rate] |
| Guardrail Thresholds | [acceptable range for each guardrail — e.g., support tickets ≤ current +10%] |

## Decision Rules

| Outcome | Threshold | Action |
|---------|-----------|--------|
| Success | [metric] ≥ [X] | [Scale how] |
| Iterate | [metric] between [X-Y] | Change: [one specific variable]. Rerun: [duration]. |
| Kill | [metric] < [X] after [duration] | Archive. Next: [what to try instead] |

## Sample Size Check

- Daily traffic: [N]
- Test duration: [days]
- Visitors per variant: [N × days ÷ 2]
- Required for [X%] lift at baseline [Y%]: [from table]
- **Sufficient?** Yes / No → [if no, adjusted approach]

## Results

[Filled in after experiment concludes]
- **Outcome:** Success / Iterate / Kill
- **Primary metric result:** [actual value]
- **Duration:** [actual days run]
- **Key finding:** [one sentence — what did we learn?]

## Post-Mortem

[Filled in for Kill decisions]
- **What we tested:** [summary]
- **Why it failed:** [root cause of failure]
- **What we learned:** [insight for future initiatives]
- **Next action:** Run `solution-design` for alternatives / Run `problem-analysis` to re-diagnose

## Next Step

[When to check results. What to do with each outcome.]
```

---

## Worked Example 1: A/B Test

```markdown
# Experiment: Paid Targeting Lookalike Test

**Date:** 2026-03-13
**Skill:** experiment
**Initiative:** Restore + Refine Paid Targeting

## Design

| Field | Value |
|-------|-------|
| Hypothesis | If we use a 1% converters lookalike audience, then paid signup rate increases from 1.2% to ≥3%, because the lookalike matches our ICP better than current broad targeting |
| Test Type | A/B — split paid budget 50/50 between current and lookalike |
| Duration | 10 days |
| Budget | $500 (redirecting existing $50/day spend) |
| Primary Metric | Paid visitor-to-signup rate |
| Baseline | 1.2% |

## Decision Rules

| Outcome | Threshold | Action |
|---------|-----------|--------|
| Success | ≥2.5% signup rate | Roll out lookalike to 100% of paid budget |
| Iterate | 1.5-2.5% | Narrow lookalike from 1% to 0.5%, add interest-based exclusions. Rerun 10 days. |
| Kill | <1.5% after 10 days | Targeting isn't the primary issue. Test homepage messaging next. |

## Sample Size Check

- Daily paid traffic: ~300 visitors
- 10 days: 3,000 total → 1,500 per variant
- At 1.2% baseline, need ~1,300 per variant for 50% lift detection
- **Sufficient?** Yes — 1,500 > 1,300. Can detect a 50%+ relative lift (1.2% → 1.8%+).
```

---

## Worked Example 2: Before-After

```markdown
# Experiment: Homepage Social Proof Restoration

**Date:** 2026-03-13
**Skill:** experiment
**Initiative:** Restore Homepage Social Proof

## Design

| Field | Value |
|-------|-------|
| Hypothesis | If we restore customer logos + testimonial to homepage hero, then bounce rate drops from 52% to ≤42%, because the redesign removed trust signals that reduced visitor confidence |
| Test Type | Before-After — change affects all visitors |
| Duration | 7 days after deployment |
| Budget | $0 (copy/design work only) |
| Primary Metric | Homepage bounce rate |
| Baseline | 52% |

## Decision Rules

| Outcome | Threshold | Action |
|---------|-----------|--------|
| Success | Bounce ≤ 42% | Keep changes. Explore further trust signal additions. |
| Iterate | 42-48% bounce | Add more proof: case study snippet, user count, or G2 rating badge. Rerun 7 days. |
| Kill | >48% after 7 days | Social proof alone isn't enough. Run full Homepage A/B (old vs new) from parked list. |

## Sample Size Check

- Daily homepage visitors: ~800
- 7 days: 5,600 visitors
- Before-After with 52% baseline: 5,600 is ample to detect a 10-point bounce rate change
- **Sufficient?** Yes
```

---

## Loop-Back Protocol

When an experiment concludes, follow the appropriate path:

### Kill Decision
1. Append learnings to the experiment file under `## Post-Mortem`
2. Check: Is the root cause (`.agents/problem-analysis.md`) still valid?
   - **Yes → Route to solution design:** Run `solution-design` with constraint: "[Failed approach] did not work because [reason]. Generate alternatives that avoid this failure mode."
   - **No → Route to problem analysis:** Problem may have shifted. Re-diagnose using `problem-analysis`.
3. Update `.agents/solution-design.md` — move killed initiative to "Kill" status with reason.

### Iterate Decision
1. Change exactly ONE variable from the original test
2. Maximum 2 iterations allowed before triggering Kill protocol
3. Document iteration rationale in experiment file under `## Iterations`

### Scale Decision
1. Document final results in experiment file under `## Results`
2. Move to full execution — no further testing needed for this initiative
3. Map the scaled initiative to KPIs and track attribution

---

## After the Experiment

| Result | Do This |
|--------|---------|
| **Success** | Scale. Set full targets via `funnel-planner`. Celebrate briefly, then test the next initiative. |
| **Iterate** | Change ONE variable. Document what and why. Max 2 iterations before escalating to kill/pivot. |
| **Kill** | Archive in the experiment file: what you tested, what happened, what you learned. Return to `solution-design` with the new learning. |

---

## Anti-Patterns

**Testing the wrong level** — Most teams test CTA button colors when they should test entirely different angles. Creative testing hierarchy by impact: Concept/angle (biggest swing) → Hook/headline → Visual style → Body copy → CTA. Start at the top of the hierarchy, not the bottom.

**Testing multiple variables** — Changing the hook, CTA, and format simultaneously makes results uninterpretable. Change exactly ONE element per variant — the learning is more valuable than the lift.

**Insufficient sample rationalization** — "We don't have enough traffic for statistical significance, so let's just go with what feels right." If you can't reach sample size for a 20% lift, either aim for a bigger change (50%+ lift) or use Before-After — don't abandon rigor entirely.

**Novelty effect as success** — New things get clicks initially. A variant that "wins" in 3 days may lose after 2 weeks once the novelty wears off. Run tests long enough for the novelty to normalize.

**Metrics without baselines** — "Let's test if this improves conversions" without knowing the current conversion rate. Every experiment requires a numeric baseline — without one, you can't calculate lift, sample size, or whether the result is meaningful.

**Testing without guardrails** — A test can "succeed" on the primary metric while degrading support ticket rates, error rates, or refund rates. Define guardrail metrics before launching — see Quality Gate.

**Survivorship bias in iteration** — Iterating only on winners while ignoring what failures teach. Kill decisions should feed learnings back to `solution-design` — the failure mechanism often reveals a better approach.

---

## References

- [references/experiment-templates.md](references/experiment-templates.md) — Templates for landing page, email, ad creative, feature flag tests
- [references/sample-size-guide.md](references/sample-size-guide.md) — Full sample size tables and common mistakes
