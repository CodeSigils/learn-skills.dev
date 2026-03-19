---
name: attribution
description: "This skill should be invoked when the user wants to evaluate whether marketing activities are producing results. Triggers include 'is my marketing working', 'what's driving results', 'which content matters', 'are we wasting money', 'what's our marketing ROI', 'marketing report', 'where are our customers coming from', 'how do I track my marketing', 'what's working and what's not', 'should I keep doing X', or 'which campaigns should we cut' -- even if they just say 'I can't tell what's working' or 'we're doing a lot but nothing moves the needle.' Not for setting new KPIs or future targets (use funnel-planner), creating new content (use content-create), or diagnosing why a specific channel underperforms (use seo for search, lp-optimization for pages)."
license: MIT
metadata:
  author: hungv47
  version: "2.2.1"
---

# Attribution Mapping

*Communication — Step 4 of 4. Validates the system — every initiative and content piece connects to a KPI, with action items for every gap.*

**Core Question:** "Can we trace every initiative to a measurable outcome?"

## Inputs Required
- KPIs from `.agents/targets.md` or existing OKRs
- Initiatives from `.agents/solution-design.md`
- Content from `.agents/mkt/imc-plan.md` or `.agents/mkt/content/`

## Output
- `.agents/mkt/attribution.md`

## Quality Gate
Before delivering, verify:
- [ ] Every KPI has ≥1 initiative mapped or is explicitly flagged with an action item
- [ ] Every initiative maps to a KPI or has a "Kill" recommendation with reason
- [ ] Every recommendation is a verb (Create / Kill / Rebalance / Test) — not an observation ("this seems low")
- [ ] Review date is set (~4 weeks from today)

## Chain Position
Previous: `content-create` | Next: Monthly review (re-run this skill)
**Re-run triggers:** Monthly review cycle (set review date ~4 weeks from creation), after experiments conclude, when KPIs or initiatives change.

### Cross-Track Prerequisites
This skill maps content → initiatives → KPIs. For full-stack attribution:
1. **Strategy stack first** (optional): Run `problem-analysis` → `solution-design` → `funnel-planner` to generate `.agents/solution-design.md` (initiatives) and `.agents/targets.md` (KPIs).
2. **Comms stack**: Run `icp-research` → `imc-plan` → `content-create` to generate content artifacts.
3. **Then attribution**: Maps content to initiatives to KPIs with gap analysis.

Without strategy artifacts, this skill interviews for KPIs and initiatives directly — it still works, but cross-stack alignment is stronger with upstream artifacts.

---

## Before Starting

### Step 0: Product Context
Check for `.agents/product-context.md`. If available, read for product context. If missing, strongly recommend running `icp-research` first — attribution mapping is significantly more accurate with product context.
If `.agents/targets.md`, `.agents/solution-design.md`, or `.agents/mkt/imc-plan.md` `date` fields are older than 30 days, recommend re-running upstream skills — stale data produces inaccurate attribution maps.

### Required Artifacts
None — can build from scratch by interviewing.

### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `targets.md` | funnel-planner | KPI baselines |
| `solution-design.md` | solution-design (from hungv47/strategy-skills) | Initiative list to map |
| `imc-plan.md` | imc-plan | Content plan to audit |
| Previous `attribution.md` | attribution | Check progress on prior action items |
| `experiment-*.md` | experiment (from strategy-skills) | Experiment outcomes as confidence adjustments — concluded experiments update contribution confidence |

Read upstream files if they exist: `.agents/targets.md`, `.agents/solution-design.md`, `.agents/mkt/imc-plan.md`. If previous `.agents/mkt/attribution.md` exists, read it — check progress on prior action items before building the new map.

### Interview
If no upstream files exist, interview for:
1. "What's your North Star metric?"
2. "What are your 3-5 primary KPIs?"
3. "What initiatives are you running or planning?"
4. "What content are you producing?"

---

## Step 1: KPI Hierarchy

**Source of truth:** `funnel-planner` SETS targets (baselines + goals); `attribution` MAPS content and initiatives to those targets. If `funnel-planner` has been run, use its targets as the KPI hierarchy — don't re-interview for KPIs that already exist in `.agents/targets.md`.

```
North Star: [metric] — [current] → [target]
├── KPI 1: [metric] — [current] → [target] — Owner: [person]
├── KPI 2: [metric] — [current] → [target] — Owner: [person]
└── KPI 3: [metric] — [current] → [target] — Owner: [person]
```

---

## Step 2: Map Initiatives → KPIs

| Initiative | Primary KPI | Contribution | Confidence |
|------------|-------------|-------------|------------|
| [Name] | [KPI] | ~X% of target | H/M/L |

**Unknown contributions:** Mark "Unknown" and add action item: "Run `experiment` to measure actual impact."

### Experiment Outcome Integration
If `.agents/experiment-*.md` files exist with concluded results:
- **Success** → Upgrade Confidence to H for that initiative's contribution
- **Iterate** → Keep Confidence at M, note iteration in progress
- **Kill** → Remove initiative from map, note reason in Orphan Initiatives

### Flag Orphans

| Orphan Initiative | Action |
|-------------------|--------|
| [Name] | **Kill** — no KPI connection / **Reframe** — target [KPI] / **Test** — run experiment |

---

## Step 3: Map Content → Initiatives

| Content | Initiative | Type | Channel |
|---------|-----------|------|---------|
| [Piece] | [Initiative] | Reach / Trust / Conversion | [Channel] |

### Flag Orphan Content

| Orphan Content | Action |
|----------------|--------|
| [Piece] | **Assign** to [initiative] / **Repurpose** for [initiative] / **Sunset** |

---

## Step 4: Gap Analysis → Action Items

This is the core deliverable. Every gap produces a specific action.

| Gap | Action | Owner | Deadline |
|-----|--------|-------|----------|
| [KPI X uncovered] | **Create:** Run `solution-design` targeting this KPI | [Who] | [When] |
| [Initiative Y orphaned] | **Kill:** Archive, remove from roster | [Who] | Now |
| [Content Z unassigned] | **Rebalance:** Redirect to support [initiative] | [Who] | [When] |
| [Contribution unknown] | **Test:** Design experiment via `experiment` | [Who] | [When] |
| [Stage imbalanced] | **Rebalance:** Shift X% effort from [over] to [under] | [Who] | [When] |

---

## Re-Run Protocol

Review and refresh attribution maps on a regular cadence:

1. **Monthly review cycle:** Set review date ~4 weeks from creation
2. **On re-run:**
   - Read previous `.agents/mkt/attribution.md`
   - Check status of each prior action item (Done / In Progress / Blocked / Dropped)
   - Rename previous file to `attribution.v[N].md`
   - Rebuild map with current state
   - Compare: Did action items move the needle? Which KPIs improved?
3. **Escalation:** If same gaps persist across 2+ reviews, escalate from "Rebalance" to "Kill" or "Create"

---

## Artifact Template

```markdown
---
skill: attribution
version: 1
date: [today's date]
status: draft
---

# Attribution Map

**Date:** [today]
**Skill:** attribution
**Review date:** [today + 4 weeks]

## KPI Hierarchy

​```
North Star: [metric] — [current] → [target]
├── KPI 1: [metric] — [current] → [target] — Owner: [person]
├── KPI 2: ...
└── KPI 3: ...
​```

## Initiative → KPI Mapping

| Initiative | KPI | Contribution | Confidence |
|------------|-----|-------------|------------|
| ... | ... | ... | ... |

### Orphan Initiatives
| Initiative | Action |
|------------|--------|
| ... | ... |

## Content → Initiative Mapping

| Content | Initiative | Type | Channel |
|---------|-----------|------|---------|
| ... | ... | ... | ... |

### Orphan Content
| Content | Action |
|---------|--------|
| ... | ... |

## Action Items

| # | Gap | Action | Owner | Deadline |
|---|-----|--------|-------|----------|
| 1 | ... | ... | ... | ... |

## Previous Review Progress

| # | Prior Action | Status | Outcome |
|---|-------------|--------|---------|
| 1 | [action from last review] | Done / In Progress / Parked / Dropped | [Result if Done: what metric moved? If not done: blocker or reason] |

Status definitions:
- **Done** — shipped AND outcome measured. If no outcome data, it's In Progress.
- **In Progress** — started but not complete. Note blocker if any.
- **Parked** — deprioritized deliberately. Note what changed.
- **Dropped** — decided not to pursue. Note explicit reason.

If the same action appears as "Parked" or "Dropped" across 2+ reviews, escalate: either commit to doing it or kill the underlying initiative.

> On re-run: rename existing artifact to `attribution.v[N].md` and create new with incremented version.
```

---

## Worked Example

```markdown
# Attribution Map

**Date:** 2026-03-13
**Skill:** attribution
**Review date:** 2026-04-10

## KPI Hierarchy

​```
North Star: Weekly Signups — 200 → 350
├── KPI 1: Paid signup rate — 1.2% → 3.0% — Owner: Sarah
├── KPI 2: Homepage bounce rate — 52% → 40% — Owner: James
└── KPI 3: Organic signups — 80/wk → 120/wk — Owner: (unassigned)
​```

## Initiative → KPI Mapping

| Initiative | KPI | Contribution | Confidence |
|------------|-----|-------------|------------|
| Restore Paid Targeting | Paid signup rate | ~55% of total gap | H |
| Restore Social Proof | Homepage bounce | ~35% of total gap | M |

### Orphan Initiatives
None — both initiatives map to KPIs.

## Content → Initiative Mapping

| Content | Initiative | Type | Channel |
|---------|-----------|------|---------|
| Status Update Carousel | (none — brand awareness) | Reach | LinkedIn |

### Orphan Content
| Content | Action |
|---------|--------|
| Status Update Carousel | **Rebalance:** Add CTA linking to product page, reframe as supporting Paid Targeting initiative |

## Action Items

| # | Gap | Action | Owner | Deadline |
|---|-----|--------|-------|----------|
| 1 | KPI 3 (organic) uncovered | **Create:** Run `problem-analysis` on organic traffic stagnation | James | 2026-03-20 |
| 2 | KPI 3 has no owner | **Assign:** Name an owner for organic signups KPI | Marketing lead | 2026-03-14 |
| 3 | Carousel content orphaned | **Rebalance:** Add product CTA to carousel, track as Paid Targeting support | Content lead | 2026-03-17 |
```

---

## Anti-Patterns

**Vanity metrics as KPIs** — Tracking impressions or followers as primary KPIs. These metrics feel good but don't connect to business outcomes. KPIs must be metrics that, if improved, move the North Star.

**Mapping everything to revenue** — Forcing every content piece to show direct revenue impact ignores the awareness and trust stages of the funnel. Map content to its appropriate funnel stage metric, not just revenue.

**Ignoring time lag** — Expecting attribution results within days for strategies that take weeks or months to show impact. Set appropriate measurement windows — brand content may take 8-12 weeks to influence pipeline.

**Orphan content without initiative links** — Content that exists because "we should post something" rather than supporting a specific initiative. Every piece should trace to an initiative and KPI — orphan content is wasted effort.

**Static attribution maps** — Building the map once and never updating it. Attribution maps decay as initiatives ship, KPIs shift, and new content is produced. Set a review cadence (monthly minimum).

**Attribution without tracking infrastructure** — Mapping content to KPIs on paper while having no event tracking, UTM parameters, or analytics in place. The map becomes theoretical without implementation. See [references/tracking-guide.md](references/tracking-guide.md) for minimum viable tracking.

**Wrong attribution model for the business** — Using last-touch attribution for a B2B product with 90-day sales cycles attributes everything to the final touchpoint and misses the content that created awareness. Match model to buying cycle length. See [references/attribution-models.md](references/attribution-models.md).

**Metrics without owners** — Every KPI and initiative must have a named person (not "the team"). Unowned metrics don't get improved — they get reported on and shrugged at.

---

## References

- [references/attribution-examples.md](references/attribution-examples.md) — Worked examples across business types
- [references/attribution-models.md](references/attribution-models.md) — Model selection guide by business type and buying cycle
- [references/tracking-guide.md](references/tracking-guide.md) — Event naming conventions, UTM standards, minimum viable tracking stack
