---
name: solution-design
description: "This skill should be invoked when the user knows the problem or goal and needs to brainstorm and prioritize strategic solutions (not code fixes). Triggers include 'what should I do about this', 'give me options', 'I need a strategy', 'how do I get more customers', 'how do I compete with [competitor]', 'what's our competitive advantage', 'what should I build next' (choosing between known options; for specifying a vague idea, use plan-interviewer), 'should we pivot', 'what's the highest-impact move', 'help me decide between approaches', 'how do we grow', or 'what should I try first' -- even if they just say 'I know the problem, now what', have completed a problem-analysis and need next steps, or state a goal and need a path to hit it. Not for engineering task lists or backlog prioritization (use task-breakdown), diagnosing what the problem is (use problem-analysis), marketing channel or campaign planning (use imc-plan), setting numeric targets (use funnel-planner), or designing tests to validate ideas (use experiment)."
license: MIT
metadata:
  author: hungv47
  version: "1.1.1"
---

# Solution Design

*Strategy — Step 2 of 4. Brainstorms targeted solutions and ranks them with evidence-backed scoring.*

**Core Question:** "What's the highest-impact thing we can do about this?"

## Inputs Required
- Root cause from `.agents/problem-analysis.md`

## Output
- `.agents/solution-design.md`

## Quality Gate
Before delivering, verify:
- [ ] Every initiative hypothesis explicitly names the root cause (not a generic growth lever)
- [ ] Every mechanic describes specific actions, not categories ("add interactive tour to first login" not "improve onboarding")
- [ ] **Anti-generic test:** Delete the root cause reference — does the idea still make sense for ANY company? If yes, it's generic. Rewrite.
- [ ] Mix includes ≥2 small, ≥2 medium, ≥1 large effort
- [ ] Every ICE score (I, C, E) has a one-sentence evidence citation — no naked numbers
- [ ] Scores are differentiated: no more than 2 initiatives share the same total ICE score
- [ ] ≤3 initiatives above cut line (force constraint even if team wants more)
- [ ] Each "proceed" initiative has: named owner, target metric with baseline, kill criteria

## Chain Position
Previous: `problem-analysis` | Next: `funnel-planner` | Cross-stack: `system-architecture` (from prod-skills — for initiatives requiring technical builds)

**Re-run triggers:** When root cause changes (re-diagnosis), when all "Proceed" initiatives are shipped or killed, or when new constraints emerge.

---

## Before Starting

### Step 0: Product Context

Check for `.agents/product-context.md`. If missing: **Strongly recommended:** run `icp-research` (from `hungv47/comms-skills`) first to create `.agents/product-context.md` — this skill works without it but produces significantly better analysis with it. If the user prefers not to, ask the user 8 product questions (what, who, problem, differentiator, proof points, pricing, objections, voice) and save to `.agents/product-context.md`.

If `.agents/problem-analysis.md` has a `date` field older than 30 days, recommend re-running `problem-analysis` before proceeding — the root cause landscape may have shifted.

### Required Artifacts
| Artifact | Source | If Missing |
|----------|--------|------------|
| `problem-analysis.md` | problem-analysis | **STOP.** "Run `problem-analysis` first to identify the root cause." |

### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `product-context.md` | icp-research (from hungv47/comms-skills) | Constraints and capabilities context |

### Root Cause Review
Read `.agents/problem-analysis.md`. Quote the root cause statement(s) and gap percentages. A root cause anchor is necessary because generic growth ideas produce low-impact, unfocused initiatives.

---

## Phase 1: Generate Initiatives

### Step 1: Understand Constraints

Interview for:
- **Root cause context**: Confirm the root cause and gap size
- **Constraints**: Budget ceiling? Team size? Hard deadlines?
- **Prior attempts**: What's been attempted? What worked/didn't?

### Step 2: Research + Generate

**WebSearch directive:** Search for how other companies solved this specific root cause:
- `"[root cause topic] case study"` (e.g., "ad targeting quality case study")
- `"how [company type] improved [metric]"` (e.g., "how SaaS improved trial conversion")
- `"[root cause] solution [industry]"` (e.g., "email deliverability fix SaaS")
- `site:reddit.com "[root cause topic]" what worked`

Use real examples to inspire specific, targeted ideas — not generic playbooks.

**Unconventional tactics to consider** (when standard approaches don't fit):

| Tactic | When to Use | Example |
|--------|------------|---------|
| **Pixel sharing** | Need reach without ad spend | Share remarketing audiences with complementary (non-competing) companies |
| **Contract buyouts** | Competing against entrenched incumbents | Pay to exit competitor contracts — "We'll cover your remaining [competitor] contract" |
| **Media acquisitions** | Need audience access fast | Buy an existing newsletter, podcast, or community in your space |
| **Influencer whitelisting** | Ads need authenticity | Run paid ads through an influencer's account (with permission) — their face, your budget |
| **"Powered by" marketing** | Product is embeddable or white-label | Free tier includes visible badge — every user becomes a marketing channel |
| **Free tool as lead gen** | Need high-volume top-of-funnel | Build a free calculator/analyzer that solves a related problem — gates results behind email |

These aren't default moves — use them when the standard ICE-scored initiatives don't adequately address the root cause or when you need asymmetric leverage.

For each idea:

| # | Name | Hypothesis | Mechanic | Target Metric | Effort |
|---|------|-----------|----------|---------------|--------|
| 1 | [Name] | If [action], then [outcome], because [root cause connection] | [2-3 sentences: specific steps, not categories] | [Metric] | S/M/L |

#### Rules

1. **Root cause anchor**: Reference the root cause in every hypothesis — untethered ideas drift into generic playbooks
2. **Anti-generic test**: For each idea, check: "Would this help ANY company, or only one with OUR root cause?" Generic → rewrite or cut
3. **Specific mechanic**: "Improve onboarding" is a category, not a mechanic. "Add 3-step interactive tour triggered on first login, guiding to first report export" is a mechanic
4. **Effort mix**: Include ≥2 Small (days, 1 person), ≥2 Medium (1-2 weeks, small team), ≥1 Large (month+, cross-team) — skewing all-small misses structural fixes; all-large stalls momentum
5. **Distinct approaches**: Each idea is a genuinely different approach

### Step 3: Refine

Present the list and gather feedback: *"Which resonate? Any to cut immediately? Any that spark a different idea?"*

---

## Phase 2: Prioritize with ICE

### Step 4: Rank BEFORE Scoring

Rank all initiatives from most to least promising FIRST, based on gut + evidence. Then assign scores — ranking before scoring prevents the "everything is a 6" clustering problem.

Interview for forced ranking: *"If you could only do ONE of these, which would it be? And after that one?"*

Force-rank all initiatives 1 through N before scoring.

### Step 5: Score Each Initiative

Score 1-10 on three dimensions. Attach a one-sentence evidence citation to every score — naked numbers invite arbitrary scoring.

| Dimension | 1-3 | 4-6 | 7-10 |
|-----------|-----|-----|------|
| **Impact** — How much will it move the target metric? | Minor, barely noticeable | Meaningful improvement | Significant or transformative |
| **Confidence** — How sure are we? | Gut feeling, no data | Some supporting data | Direct evidence, proven playbook |
| **Ease** — How easy to execute? | Multi-team, months | Moderate effort, manageable | Small team, quick turnaround |

**Confidence evidence thresholds** (most common source of arbitrary scoring):

| Score | Evidence Required | Example |
|-------|------------------|---------|
| 1-3 | Gut feeling only, no data | "I think this would work" |
| 4-5 | One data point (one past test, one customer quote, one competitor example) | "Competitor X did this and grew 20%" |
| 6-7 | Supporting pattern (2+ data points from different sources) | "3 customers requested this + competitor benchmark shows 30% lift" |
| 8-9 | Proven in similar context (same tactic worked 2+ times in same business type) | "We ran this last quarter and got 25% lift; industry case studies show 20-40% range" |
| 10 | Near-certain (proven playbook with 80%+ success rate in your exact context) | "We've done this 3 times before, same metric moved every time" |

Map your evidence to this grid before assigning the number. If two initiatives both land at "6" but one has customer quotes and the other has competitor data, the forced ranking from Step 4 should break the tie.

**Bad:** "Impact: 7"
**Good:** "Impact: 7 — paid traffic is 60% of signups, and the old targeting had 3.5% conversion vs. current 1.2%"

**WebSearch directive:** If the user lacks evidence for a score, search for supporting data: `"[tactic] conversion improvement case study"`, `"[similar company] [tactic] results"`, `"[metric] improvement benchmark"`

ICE Score = I + C + E (sum). Scores should reflect the forced ranking from Step 1 — if you ranked it #1, its ICE should be highest.

### Step 6: Cut Line

Interview for capacity: **"How many can you execute well simultaneously?"**

Push for honesty:
- Solo/2-person team: 1-2
- Small team (3-5): 2-3
- Growth team (5+): 3-4

For each initiative, assign a decision:

| Decision | Meaning |
|----------|---------|
| **Proceed** | Start this week. Has owner, metric, kill criteria. |
| **Park** | Promising, but can't resource now. Revisit after current batch. |
| **Kill** | Not worth doing. State why clearly. |

### Step 7: Validate "Proceed" Initiatives

For each "Proceed" initiative, confirm:
- [ ] Owner named (a person, not "the team")
- [ ] Target metric has a numeric baseline
- [ ] Kill criteria: "Stop if [metric] < [threshold] after [duration]"
- [ ] Can begin execution within 1 week

Resolve any failing checks before moving on — gaps in ownership or metrics cause stalled initiatives.

For "Proceed" initiatives requiring detailed execution plans, see [references/initiative-planning.md](references/initiative-planning.md) — 5-phase planning (Foundation, Strategy, Resources, Success Criteria, Risk Assessment) and proposal validation.

---

## Artifact Template

On re-run: rename existing artifact to `solution-design.v[N].md` and create new with incremented version.

```markdown
---
skill: solution-design
version: 1
date: {{today}}
status: draft
---

# Solution Design

**Root Cause:** [from problem-analysis.md]

## Phase 1: Initiatives

### 1. [Name] — Effort: S
**Hypothesis:** If [action], then [outcome], because [root cause connection].
**Mechanic:** [Specific steps — what you'd actually do, in order]
**Target Metric:** [metric]
**Anti-generic check:** [Why this only works for our specific root cause]

### 2. [Name] — Effort: S
[Same format]

### 3. [Name] — Effort: M
[Same format]

[...5-10 total]

## Phase 2: Prioritization

### Forced Ranking (gut + evidence)

1. [Name] — most promising because [reason]
2. [Name]
3. [Name]
...

### ICE Scoring

| Rank | Initiative | I | C | E | ICE | Key Evidence |
|------|-----------|---|---|---|-----|-------------|
| 1 | [Name] | [score] | [score] | [score] | [sum] | [One-sentence evidence for top-scoring dimension] |
| 2 | ... | ... | ... | ... | ... | ... |

### Decisions

| Initiative | Decision | Owner | Target Metric (Baseline) | Kill Criteria |
|------------|----------|-------|-------------------------|---------------|
| [Name] | Proceed | [Person] | [Metric]: [current] | Stop if [metric] < [threshold] after [duration] |
| [Name] | Park | — | — | — |
| [Name] | Kill | — | — | Reason: [why] |

**Cut line:** [N] initiatives proceeding. Team capacity: [context].

## Next Step

Run `funnel-planner` to set targets, then `experiment` to test.
If any "Proceed" initiative requires a technical build, also run `system-architecture` (from `hungv47/prod-skills`) with these initiatives as context.
```

---

## Worked Example

**Root Cause:** Signups declined because (1) ad targeting brought low-intent visitors (~55%) and (2) homepage redesign lost trust signals (~35%).

```markdown
# Solution Design

**Date:** 2026-03-13
**Skill:** solution-design
**Root Cause:** (1) Ad targeting quality (~55%), (2) Homepage trust/clarity (~35%)

## Phase 1: Initiatives

### 1. Restore + Refine Paid Targeting — Effort: S
**Hypothesis:** If we revert to original targeting and add a converters lookalike, then paid conversion returns to ≥3%, because the current broad targeting is bringing visitors outside our ICP.
**Mechanic:** Pull last 90d converters list → create 1% lookalike in Meta → A/B test current broad vs. lookalike targeting → 7-day test at $50/day per variant.
**Target Metric:** Paid visitor-to-signup rate
**Anti-generic check:** Only relevant because our specific targeting change caused the quality drop.

### 2. Restore Homepage Social Proof — Effort: S
**Hypothesis:** If we add back customer logos + testimonial above the fold, then homepage bounce rate drops to ≤40%, because the redesign removed the trust signals that were on the old page.
**Mechanic:** Screenshot old homepage via Wayback Machine → identify removed trust elements → add 3 customer logos + 1 short testimonial quote to new hero section → deploy.
**Target Metric:** Homepage bounce rate
**Anti-generic check:** Only relevant because our specific redesign removed these elements.

### 3. Landing Page per Ad Group — Effort: M
**Hypothesis:** If paid visitors land on a page matching their ad's promise, then paid conversion improves by 30%+, because the current generic homepage doesn't match specific ad copy.
**Mechanic:** Identify top 3 ad groups by spend → create 1 landing page per group with message-matched headline → redirect ad traffic → measure conversion per LP vs. homepage.
**Target Metric:** Ad-to-signup conversion by ad group
**Anti-generic check:** Addresses both root causes — targeting quality AND page clarity for specific audiences.

### 4. Homepage A/B: Old vs. New — Effort: S
**Hypothesis:** If the old homepage converts better, then the redesign itself is the problem, because we'll have direct evidence comparing the two.
**Mechanic:** Restore old homepage on a subdomain or via feature flag → split traffic 50/50 → run for 14 days → measure signup conversion.
**Target Metric:** Homepage-to-signup rate
**Anti-generic check:** Directly tests whether Root Cause 2 is the homepage design itself.

### 5. Intent-Qualifying Ad Creative — Effort: M
**Hypothesis:** If ad creative pre-qualifies intent (mentions price, mentions specific use case), then paid visitor quality improves even with broad targeting, because self-selection filters out low-intent clicks.
**Mechanic:** Write 3 new ad variants that mention pricing tier or specific use case → run alongside current ads → compare conversion rate of clickers.
**Target Metric:** Paid ad-to-signup conversion rate
**Anti-generic check:** Only relevant because broad targeting is bringing wrong audience.

### 6. Dedicated Onboarding for Paid Visitors — Effort: L
**Hypothesis:** If paid visitors get a tailored first-visit experience emphasizing the value prop they saw in the ad, then their conversion improves, because the gap between ad promise and site experience is what loses them.
**Mechanic:** Detect UTM source on landing → show contextual welcome message matching ad group → customize hero copy dynamically → build for top 3 ad groups.
**Target Metric:** Paid visitor activation + signup rate
**Anti-generic check:** Only needed because paid visitors have different expectations than organic.

## Phase 2: Prioritization

### Forced Ranking

1. Restore + Refine Paid Targeting — fastest fix for biggest root cause
2. Restore Homepage Social Proof — fast, addresses second root cause
3. Homepage A/B: Old vs New — definitive answer on redesign impact
4. Landing Page per Ad Group — higher effort but compounds with #1
5. Intent-Qualifying Ad Creative — interesting but less certain
6. Dedicated Onboarding for Paid — too complex for now

### ICE Scoring

| Rank | Initiative | I | C | E | ICE | Key Evidence |
|------|-----------|---|---|---|-----|-------------|
| 1 | Restore Paid Targeting | 8 | 8 | 9 | 25 | I:8 — paid is 60% of traffic, old targeting converted at 3.5% vs 1.2% now |
| 2 | Restore Social Proof | 7 | 7 | 9 | 23 | C:7 — Wayback shows old page had logos+testimonial that new page removed |
| 3 | Homepage A/B | 6 | 9 | 7 | 22 | C:9 — direct comparison eliminates guessing about redesign impact |
| 4 | LP per Ad Group | 7 | 6 | 5 | 18 | I:7 — message match lifts are well-documented (CXL: 20-50% improvement) |
| 5 | Intent Ad Creative | 5 | 4 | 6 | 15 | C:4 — no precedent with our audience, hypothesis only |
| 6 | Paid Onboarding | 7 | 3 | 3 | 13 | E:3 — needs eng + dynamic content, 4+ weeks |

### Decisions

| Initiative | Decision | Owner | Target Metric (Baseline) | Kill Criteria |
|------------|----------|-------|-------------------------|---------------|
| Restore Paid Targeting | **Proceed** | Sarah | Paid conversion: 1.2% | Stop if <2% after 10 days |
| Restore Social Proof | **Proceed** | James | Homepage bounce: 52% | Stop if >48% after 7 days |
| Homepage A/B | **Park** | — | — | Do after #1 and #2 ship |
| LP per Ad Group | **Park** | — | — | Revisit if paid targeting fix isn't enough |
| Intent Ad Creative | **Kill** | — | — | Too uncertain; paid targeting fix addresses the same root cause more directly |
| Paid Onboarding | **Kill** | — | — | Too complex for current team capacity |

**Cut line:** 2 initiatives proceeding. Team: 3-person growth team.

## Next Step

Run `funnel-planner` to set targets for Restore Paid Targeting and Restore Social Proof, then `experiment` to test.
```

---

## Anti-Patterns

**Generic initiatives** — "Improve SEO" or "Optimize onboarding" are categories, not initiatives. Every initiative must describe a specific mechanic tied to a specific root cause. The anti-generic test catches these: if ANY company could use this idea regardless of root cause, it's too generic.

When an initiative fails the anti-generic test, salvage it:
1. Identify the generic part ("Improve onboarding" = generic)
2. Anchor to the root cause ("Low feature adoption of export feature" = specific root cause)
3. Rewrite with a specific mechanic ("Add 3-step export walkthrough triggered on first file upload")
4. Re-test: delete the root cause — does the idea still make sense for any company? If so, go more specific

**Before/after examples:**

| Generic (fails test) | Still Generic (fails again) | Specific (passes) |
|---------------------|---------------------------|-------------------|
| "Improve onboarding" | "Improve onboarding with gamification" | "Add export walkthrough on first login because Root Cause = users never discover export" |
| "Better content marketing" | "Create more blog posts" | "Write 3 comparison articles targeting [competitor] keywords because Root Cause = losing deals at evaluation stage" |
| "Reduce churn" | "Send retention emails" | "Add pause-subscription option to cancel flow because Root Cause = 30% of cancellers cite 'temporary need change'" |

**Untethered ideas** — Ideas that sound good but don't connect to the confirmed root cause. Root cause anchoring prevents the brainstorm from drifting into a generic growth playbook.

**All-small or all-large efforts** — Skewing entirely toward quick wins misses structural fixes. Skewing entirely toward large initiatives stalls momentum. Include a mix: ≥2 Small, ≥2 Medium, ≥1 Large.

**"Everything is a 6" scoring** — When all ICE scores cluster together, the ranking is meaningless. Force-rank before scoring to create differentiation. If you ranked it #1, its ICE should be highest.

**Naked scores without evidence** — "Impact: 7" with no justification invites political scoring. Every score needs a one-sentence citation: what data or reasoning supports this number.

**Too many initiatives above cut line** — More than 3 active initiatives means none get full attention. Force the constraint even when the team pushes for more. Parked initiatives have their turn after the current batch ships.

**Missing kill criteria** — Initiatives without a "stop if" threshold run forever. Every "Proceed" initiative needs a specific metric, threshold, and duration that triggers a stop.

---

## References

- [references/hypothesis-framework.md](references/hypothesis-framework.md) — If/Then/Because templates
- [references/initiative-types.md](references/initiative-types.md) — Hero vs Support classification
- [references/ice-scoring-rubric.md](references/ice-scoring-rubric.md) — Detailed scoring calibration with scored examples
- [references/initiative-planning.md](references/initiative-planning.md) — Detailed execution planning for complex initiatives
- [references/churn-playbook.md](references/churn-playbook.md) — Cancel flow, dunning, health scores, exit-reason mapping (when root cause is churn)
- [references/churn-cancel-flow-templates.md](references/churn-cancel-flow-templates.md) — Email templates for cancel flow and dunning sequences
- [references/churn-health-score-guide.md](references/churn-health-score-guide.md) — Health score implementation and calibration
