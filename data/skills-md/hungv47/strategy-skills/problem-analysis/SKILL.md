---
name: problem-analysis
description: "This skill should be invoked when the user faces a business or strategic problem (not code bugs) they don't fully understand and needs structured diagnosis. Triggers include 'why is this happening', 'something is wrong', 'diagnose this', 'root cause', 'our numbers are down', 'revenue dropped', 'churn is high', 'growth stalled', 'we're bleeding money', 'no traction', 'our CAC is too high', 'I'm stuck on a business problem', or 'something changed and I don't know what' -- even if they just describe symptoms without asking for analysis, share data and expect you to spot the issue, or frame it as a competitive threat ('competitor is eating our lunch'). Not for code refactoring (use code-cleanup), diagnosing a specific page's conversion issues (use lp-optimization), brainstorming solutions when the problem is already clear (use solution-design), or setting funnel targets (use funnel-planner)."
license: MIT
metadata:
  author: hungv47
  version: "1.1.1"
---

# Problem Analysis

*Strategy — Step 1 of 4. Defines the problem, forms testable hypotheses, and identifies root causes.*

**Core Question:** "What's actually causing this, and what does the evidence prove?"

## Inputs Required
- A problem (metric decline, performance gap, strategic question)

## Output
- `.agents/problem-analysis.md`

## Quality Gate
Before delivering, verify:
- [ ] Problem statement contains two numbers (current state AND target state)
- [ ] Logic tree has 2-3 levels with ≥3 leaf nodes
- [ ] Each leaf is a testable cause (not a restatement like "conversion is low")
- [ ] MECE: fixing one branch doesn't auto-fix another; no cause is missing
- [ ] Every hypothesis follows If/Then/Because format
- [ ] Every "then" clause names a specific metric or observable data point
- [ ] Every hypothesis has a named data source (not "check analytics" — which tool, which report)
- [ ] Hypotheses are ranked by testability (easiest to test first)
- [ ] Every hypothesis has a verdict: Confirmed, Rejected, or Inconclusive
- [ ] Every verdict cites a specific number or data point (not "seems like" or "probably")
- [ ] Root cause statement includes gap percentage (e.g., "explains ~60% of gap")
- [ ] Every Inconclusive item has a concrete next step (what data, where, who)

## Chain Position
Previous: none | Next: `solution-design`

### Skill Deference
- **Have a METRIC that's underperforming** (X is at Y, should be Z)? → Use this skill.
- **Have a FEATURE IDEA to spec out?** → Use `plan-interviewer` (from prod-skills) instead — it structures feature requirements, not metric diagnosis.

**Re-run triggers:** When the metric shifts significantly from the last analysis, when new data surfaces that could change verdicts, or when a solution-design initiative is killed.

---

## Before Starting

### Step 0: Product Context
Check for `.agents/product-context.md`. If missing: **Strongly recommended:** run `icp-research` (from `hungv47/comms-skills`) first to create `.agents/product-context.md` — this skill works without it but produces significantly better analysis with it. If the user prefers not to, interview for 8 product dimensions (what, who, problem, differentiator, proof points, pricing, objections, voice) and save to `.agents/product-context.md`.

### Required Artifacts
None — this is the entry point for the Strategy track.

### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `product-context.md` | icp-research (from hungv47/comms-skills) | Industry context for better tree construction and benchmark selection |

---

## Phase 1: Define the Problem

### Problem Interview
If the user describes a vague problem ("things aren't going well", "growth is slow"):
1. Ask for the specific metric and its current value
2. Ask for the target value and who set it
3. If user doesn't know the baseline, use WebSearch: `"[industry] [metric] benchmark [year]"` or `"[business type] average [metric]"`
4. Metric name + current number + target number are necessary before proceeding — without all three, the logic tree has no anchor and branches become speculation

### Step 1: Define the Problem Statement

> **[Metric] is [current number] instead of [target number]**

Interview:
1. What metric specifically? (Not "growth" — which metric?)
2. What's the current number?
3. What's the target? Who set it?
4. When did it change? Was there an inflection point?
5. How big is the gap in absolute and relative terms?

### Step 2: Build a Logic Tree

#### Choose Tree Type

| Type | When | Example Root |
|------|------|-------------|
| **Math Tree** | Metric can be decomposed into formula | Revenue = Traffic × Conversion × AOV |
| **Issue Tree** | Multi-factor, non-mathematical | "Why are customers churning?" |
| **Yes/No Tree** | Binary decision points | "Is the problem supply-side or demand-side?" |

#### Build It

1. Put the problem statement at the top
2. Break into 2-4 mutually exclusive categories
3. For each category, break into 2-3 sub-factors
4. Stop at 2-3 levels deep
5. MECE check: Verify branches cover everything. If fixing A auto-fixes B, there is overlap — restructure

**WebSearch directive:** Use WebSearch to understand what factors typically drive this metric — generic trees miss industry-specific drivers. Search: `"[metric] decomposition" OR "[metric] drivers" OR "what affects [metric]"`

### External Factor Check

Before finalizing the tree, rule out external causes that could explain the metric change without any internal failure:

| Factor | Search For | Example |
|--------|-----------|---------|
| **Competitor launch** | `"[competitor] launch OR announce [date range]"` | Competitor launched free tier, pulling traffic |
| **Market/seasonal shift** | `"[industry] [metric] trend [year]"` | Industry-wide conversion drop in Q4 |
| **Platform algorithm change** | `"[platform] algorithm update [date range]"` | Google core update tanked organic traffic |
| **Regulatory/policy change** | `"[industry] regulation OR policy [year]"` | GDPR enforcement reduced EU email signups |
| **Economic conditions** | `"[industry] spending [quarter] [year]"` | Budget freezes across the industry |

Add an "External Factors" branch to the logic tree if any of these are plausible. External causes are often the fastest to confirm or reject — and missing them leads to treating a symptom (your site) when the cause is environmental.

---

## Phase 2: Form Hypotheses

For each leaf of the logic tree:

> **If** [this cause is true], **then** we'd see [specific observable evidence], **because** [mechanism that explains why].

### What Makes a Strong Hypothesis

| Element | Weak | Strong |
|---------|------|--------|
| **If** | "onboarding is bad" | "onboarding emails are being spam-filtered since the domain migration on Jan 15" |
| **Then** | "conversion drops" | "day-1 email open rate dropped below 20% (was 45%)" |
| **Because** | "emails matter" | "the new sending domain has no reputation, triggering ESP spam filters" |

The "then" must be something you can look up in a specific tool. The "because" must explain the mechanism — it's what you learn from if the hypothesis is wrong.

### Map Data Requirements

For each hypothesis:

| Hypothesis | Deciding Data Point | Confirming Evidence | Rejecting Evidence | Source (Tool → Report) | Owner |
|------------|-------------------|--------------------|--------------------|----------------------|-------|
| [If/Then/Because] | [Single data point that decides] | [What you'd see if true] | [What you'd see if false] | [e.g., "GA4 → Acquisition → Traffic by source"] | [Person] |

Use WebSearch before finalizing — search `"[topic] common causes" OR "[metric] drop reasons [industry]"` to catch missing high-probability hypotheses. Also search `"[competitor name] [recent change]"` if external factors might be at play.

### Rank by Testability

Rank hypotheses by: (a) how quickly you can get the data, AND (b) how much of the gap it would explain if confirmed.

| Priority | Hypothesis (short name) | Data Available Now? | Potential Gap Explained | Test Time |
|----------|------------------------|--------------------|-----------------------|-----------|
| 1 | [Easiest + highest impact] | Yes / Partial / No | ~X% | [Hours/Days/Weeks] |
| 2 | ... | ... | ... | ... |

**Logic:** Test what you can test TODAY first. Eliminate hypotheses fast. Don't spend weeks on #4 when #1 takes an hour to check.

---

### Data Gathering Pause

**"Share what you found for each hypothesis — data, screenshots, reports, CSVs, or describe what you saw."**

If user provides data files, read and analyze them directly — don't ask the user to summarize data you can read yourself.

If user hasn't gathered data yet:
- Use WebSearch for publicly available evidence: `"[competitor] launch [date range]"`, `"[industry] [metric] trend [year]"`, `"[tool name] outage [date]"`
- Point them to the specific sources listed in the hypotheses table

---

## Phase 3: Root Cause Verdict

### Step 1: Verdict Per Hypothesis

For each hypothesis:

| Verdict | Criteria | What to Write |
|---------|----------|--------------|
| **Confirmed** | Evidence matches the "then" clause and supports the "because" | "[Data point] confirms: [what it shows]. Mechanism supported." |
| **Rejected** | Evidence contradicts the "then" clause | "[Data point] shows [opposite of prediction]. Cause eliminated." |
| **Inconclusive** | Evidence is ambiguous or insufficient | "[What we found]. Need: [specific additional data], from [source], owned by [who]." |

**Prioritize Inconclusive verdicts by impact:** Not all Inconclusive results deserve follow-up. Rank them:

| Potential Gap Explained | Action |
|------------------------|--------|
| **>50% of gap** (high-impact) | **Must resolve** before moving to solution-design. Specify: data needed, source, access barrier, timeline, owner. |
| **10-50% of gap** (medium-impact) | **Should resolve** if data is available within 1 week. Otherwise, note as risk and proceed. |
| **<10% of gap** (low-impact) | **Skip** — proceed to solution-design. Note as unexplained variance. |

Designing solutions around an incomplete diagnosis is expensive. A high-impact Inconclusive hypothesis that explains 50%+ of the gap means your root cause statement is missing the biggest driver — solutions will target the wrong thing.

Be direct. "The data doesn't support this" is useful. "It's hard to tell" is not.

### Step 2: Root Cause Statement

Synthesize confirmed hypotheses:

> **Root Cause 1 (~X% of gap):** [Cause], evidenced by [specific data]. [Mechanism].
> **Root Cause 2 (~Y% of gap):** [Cause], evidenced by [specific data]. [Mechanism].
> **Unexplained (~Z%):** [What's still unknown]. Next step: [what to investigate].

Gap percentages should roughly sum to 100%. They don't need to be precise — "~60%" is fine. The point is to show which cause matters most.

### Step 3: Next Steps

| Situation | Action |
|-----------|--------|
| Clear root cause(s) identified | "Run `solution-design` to brainstorm and prioritize solutions targeting: [root cause]" |
| Inconclusive items remain | "Before generating solutions, gather: [specific data]. Then re-run Phase 3." |
| Multiple root causes, different sizes | "Address Root Cause 1 first (~X% of gap). It's the highest-leverage fix." |

---

## Artifact Template

On re-run: rename existing artifact to `problem-analysis.v[N].md` and create new with incremented version.

```markdown
---
skill: problem-analysis
version: 1
date: {{today}}
status: draft
---

# Problem Analysis

## Phase 1: Problem Definition

### Problem Statement

[Metric] is [current] instead of [target], a gap of [X%/X units].
Started: [when]. Inflection point: [if known].

### Logic Tree

[Tree type: Math / Issue / Yes-No]

​```
[Problem statement]
├── [Branch 1]
│   ├── [Leaf 1a]
│   ├── [Leaf 1b]
│   └── [Leaf 1c]
├── [Branch 2]
│   ├── [Leaf 2a]
│   └── [Leaf 2b]
└── [Branch 3]
    ├── [Leaf 3a]
    └── [Leaf 3b]
​```

### MECE Check

- Mutually Exclusive: [confirm no overlaps]
- Collectively Exhaustive: [confirm no gaps]

## Phase 2: Hypotheses (Ranked by Testability)

### 1. [Short name] — Priority: HIGH
**If** [cause], **then** [observable evidence], **because** [mechanism].
- **Deciding data:** [specific data point]
- **Source:** [Tool → Report → Metric]
- **Owner:** [person/team]
- **Confirming:** [what you'd see if true]
- **Rejecting:** [what you'd see if false]
- **Potential gap explained:** ~X%

### 2. [Short name] — Priority: HIGH
[Same format]

### 3. [Short name] — Priority: MEDIUM
[Same format]

## Phase 3: Root Cause Verdict

### Verdict Table

| # | Hypothesis | Verdict | Evidence | Gap |
|---|-----------|---------|----------|-----|
| 1 | [Short name] | Confirmed / Rejected / Inconclusive | [Specific data cited] | ~X% |
| 2 | ... | ... | ... | ... |

### Root Cause Statement

**Root Cause 1 (~X% of gap):** [Cause], evidenced by [data].
[One sentence explaining the mechanism.]

**Root Cause 2 (~Y% of gap):** [Cause], evidenced by [data].
[One sentence explaining the mechanism.]

**Unexplained (~Z%):** [Description]. Next data needed: [what], from [where].

## Next Step

Run `solution-design` targeting:
1. [Root cause 1 — specific aspect to solve]
2. [Root cause 2 — specific aspect to solve]
```

---

## Worked Example

**User:** "Our signups are declining."

**Phase 1 Interview:**
- "What's the current signup rate?" → "About 200/week, down from 350/week"
- "When did it start?" → "About 8 weeks ago"
- "Any changes around that time?" → "We launched a new homepage and changed our ad targeting"

**Phase 2 Hypotheses formed:**
1. Tracking broken on new homepage — Priority: HIGH (fastest to test, explains 100% if true)
2. Ad targeting change reduced quality — Priority: HIGH (paid is 60% of traffic)
3. Homepage redesign reduced conversion — Priority: MEDIUM (bounce rate up across all sources)

**Data Gathering Pause — user returns with data:**
- "Checked DB vs GA4 — both show the same drop. Tracking is fine."
- "Paid traffic conversion dropped from 3.5% to 1.2%. Organic is still at 4.1%."
- "Homepage bounce rate increased from 35% to 52% for all traffic."

**Phase 3 Verdict:**

```markdown
# Problem Analysis

**Date:** 2026-03-13
**Skill:** problem-analysis

## Phase 1: Problem Definition

### Problem Statement

Weekly signups are 200 instead of 350, a gap of 43%.
Started: ~8 weeks ago. Inflection point: homepage redesign + ad targeting change.

### Logic Tree

Math Tree

​```
Weekly signups declining (200 → 350 target)
├── Traffic volume declining (fewer people arriving)
│   ├── Paid traffic: ad targeting change reduced volume/quality
│   ├── Organic traffic: SEO impact from homepage redesign
│   └── Referral/direct: brand or word-of-mouth decline
├── Conversion rate declining (same traffic, fewer signups)
│   ├── Homepage redesign reduced clarity/trust
│   ├── Signup flow friction increased
│   └── Value proposition no longer resonates
└── Measurement change (signups happening but not counted)
    ├── Tracking code broken on new homepage
    └── Attribution model changed
​```

### MECE Check

- Mutually Exclusive: Traffic volume vs. conversion rate vs. measurement are independent
- Collectively Exhaustive: All signup decline must come from fewer visitors, lower conversion, or miscounting

## Phase 2: Hypotheses (Ranked by Testability)

### 1. Tracking broken on new homepage — Priority: HIGH
**If** the homepage redesign broke the signup tracking pixel, **then** GA4 shows a sudden drop in recorded signups coinciding with the deploy date while server-side signup records remain stable, **because** the new page template may not include the tracking script.
- **Deciding data:** Compare GA4 signup events vs. database signups for the last 8 weeks
- **Source:** GA4 → Events → sign_up AND production database signup count
- **Owner:** Engineering
- **Confirming:** GA4 shows drop but DB signups are flat
- **Rejecting:** GA4 and DB both show the same drop
- **Potential gap explained:** ~100% (if tracking, not real decline)

### 2. Ad targeting change reduced quality — Priority: HIGH
**If** the ad targeting change brought lower-intent visitors, **then** paid traffic volume stayed flat but paid visitor signup rate dropped, **because** broader targeting reaches people less likely to convert.
- **Deciding data:** Signup rate by traffic source (paid vs organic) before/after change
- **Source:** GA4 → Acquisition → Traffic source → Conversion rate
- **Owner:** Marketing (paid team)
- **Confirming:** Paid conversion rate dropped; organic stable
- **Rejecting:** Both paid and organic dropped equally
- **Potential gap explained:** ~50%

### 3. Homepage redesign reduced conversion — Priority: MEDIUM
**If** the new homepage is less clear or trustworthy, **then** homepage-to-signup conversion rate dropped for ALL traffic sources equally, **because** the new design may lack social proof or clear value proposition.
- **Deciding data:** Homepage → signup conversion rate, by traffic source, before/after
- **Source:** GA4 → Pages → Homepage → Next page flow
- **Owner:** Product/Design
- **Confirming:** All-source conversion dropped on homepage specifically
- **Rejecting:** Conversion dropped only for paid traffic (→ targeting issue, not homepage)
- **Potential gap explained:** ~40%

## Phase 3: Root Cause Verdict

### Verdict Table

| # | Hypothesis | Verdict | Evidence | Gap |
|---|-----------|---------|----------|-----|
| 1 | Tracking broken | **Rejected** | GA4 and DB both show same drop (200/week). Tracking is working correctly. | 0% |
| 2 | Ad targeting reduced quality | **Confirmed** | Paid conversion dropped from 3.5% to 1.2% (66% decline). Organic stable at 4.1%. Paid traffic is 60% of total. | ~55% |
| 3 | Homepage redesign reduced conversion | **Confirmed** | Bounce rate up from 35% to 52% across ALL sources. Even organic visitors are bouncing more, suggesting the page itself is the problem. | ~35% |

### Root Cause Statement

**Root Cause 1 (~55% of gap):** Ad targeting change brought low-intent visitors, evidenced by paid conversion dropping 66% while organic held steady. The broader targeting reaches people outside the ICP.

**Root Cause 2 (~35% of gap):** Homepage redesign reduced trust/clarity, evidenced by bounce rate rising 17 points across all traffic sources. The new page likely lacks the social proof or clear value prop of the old design.

**Unexplained (~10%):** Minor variance, possibly seasonal. No action needed.

## Next Step

Run `solution-design` targeting:
1. Paid targeting — restore or improve audience quality
2. Homepage — restore trust signals and clarify value proposition
```

---

## Anti-Patterns

**Too-shallow tree** — Stopping at one level produces branches that are categories, not testable causes. Always decompose to at least 2 levels; the leaf should be something you can look up in a specific data source.

**Overlapping branches** — If fixing Branch A would automatically fix Branch B, the tree is not mutually exclusive. Restructure until each branch is independently testable.

**Restatements as causes** — "Conversion is low because conversion dropped" restates the problem. Every leaf must name a *mechanism* — what specifically changed and why.

**Missing measurement branch** — Most trees cover demand-side and supply-side but forget instrumentation errors. Always include a "measurement/tracking" branch — it's the fastest to test and explains 100% of the gap when true.

**Single tree type for everything** — Math trees work for decomposable metrics; issue trees work for multi-factor problems. Choosing the wrong type forces awkward branches. Match tree type to problem shape.

**Unfalsifiable hypotheses** — "If onboarding is bad, then users churn" cannot be tested because "bad" has no measurable threshold. Every "then" clause must name a specific metric and direction.

**Testing everything at once** — Running 5 tests simultaneously makes it impossible to attribute results. Rank by testability and test sequentially — fast eliminations narrow the field.

**Confirmation bias in evidence selection** — Choosing only data sources likely to confirm the hypothesis. Every hypothesis must define both confirming AND rejecting evidence before gathering data.

**Premature verdicts** — Declaring "Confirmed" after seeing one data point that loosely supports the hypothesis. Every verdict requires evidence that specifically matches or contradicts the "then" clause.

**Confusing correlation with causation** — "Signups dropped when we changed the homepage, so the homepage caused it." Correlation identifies candidates; causation requires the mechanism to hold. Check: does the "because" clause explain the data?

**Skipping the "because" clause** — Omitting the mechanism makes hypotheses unfalsifiable. The "because" explains *why* the cause produces the effect — it's what you learn from when the hypothesis is wrong.

**Ignoring inconclusive results** — Marking ambiguous evidence as "Rejected" to simplify the analysis. Inconclusive is a valid verdict — it means more data is needed, and the next step must specify what data, from where.

**Gap percentages that don't add up** — If root causes explain 140% of the gap (or only 30%), the analysis has double-counting or missing causes. Percentages should roughly sum to 100%.

---

## References

- [references/watanabe-framework.md](references/watanabe-framework.md) — MECE principles and tree-building
- [references/logic-tree-examples.md](references/logic-tree-examples.md) — 4 worked examples (SaaS churn, e-commerce, content ROI, B2B pipeline)
- [references/hypothesis-guide.md](references/hypothesis-guide.md) — If/Then/Because templates by problem type
