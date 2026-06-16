---
name: performance-diagnosis
description: Diagnoses why campaigns, CRM journeys, media plans, funnels, landing pages, apps, or business KPIs are underperforming. Use when performance is below target, costs rise, conversion falls, delivery is weak, CRM response drops, creative fatigues, or leadership needs root-cause analysis. Also trigger when someone says "why is performance down?", "CPA is rising", "ROAS dropped", "leads are bad", "what happened?", "diagnose the campaign", or "performance recovery plan". Even casual phrasing like "something's broken", "numbers are off", "it stopped working", or "why aren't we hitting target?" should activate this skill.
---

# Performance Diagnosis

Find the real cause of underperformance across the growth supply chain: audience, media, creative, CRM, funnel, offer, data, tracking, operations, or market conditions. Use root-cause logic, not superficial reporting.

## How This Skill Orchestrates

This is a **3-script diagnostic pipeline** — run them in sequence:

1. **Script 1** (`scripts/funnel_gap_analyzer.py`): Trace the conversion funnel stage by stage, detect where the largest drop-off occurs vs benchmarks, identify the primary leakage point, and map initial root causes per stage
2. **Script 2** (`scripts/root_cause_ranker.py`): Take the leakage point + user-provided evidence signals and rank 24 root causes by evidence-weighted likelihood score (prior × evidence multiplier). Covers 8 domains: Media, Creative, Conversion, CRM, Strategy, Data, Operations, Market
3. **Script 3** (`scripts/corrective_action_prioritizer.py`): Generate prioritized corrective actions scored by Impact × Urgency × Feasibility. Classifies as immediate (24-72h), short-term (1-2 weeks), or structural (2-8 weeks)
4. **Reference lookup** (`references/diagnostic_framework.md`): Root-cause taxonomy (8 domains), funnel leakage map, 3 diagnostic decision trees (media/CRM/creative), evidence signal catalog, benchmark search protocol
5. **Reference lookup** (`references/corrective_action_playbook.md`): Corrective actions by domain, escalation rules (by severity), war room protocol (Hour 0 → Day 14), recovery measurement expectations
6. **Web search** (Claude — MANDATORY): Search benchmarks before diagnosing — "is this us-specific or market-wide?"
7. **Upstream context** (Claude): Pull control tower health from `weekly-control-tower`, media allocation from `media-routing-planner`, CRM metrics from `crm-journey-architect`, margin from `margin-simulation`
8. **Visual output** (Visualizer): Funnel leakage waterfall + root cause ranking + corrective action priority matrix

**Model decision**: **Anomaly detection (funnel gap vs benchmark) + rule-based classification (root cause ranking) + prioritization scoring** (Governance layer). Not ML — we're detecting where the funnel deviates from expected and scoring root causes by evidence weight. The root cause ranker uses a Bayesian-inspired prior × evidence multiplier, but it's a scoring heuristic, not a trained model.

## Quick Reference

| Resource | Purpose | Usage |
|----------|---------|-------|
| `scripts/funnel_gap_analyzer.py` | Stage-by-stage funnel analysis — 8 transitions with benchmarks, gap severity scoring, primary leakage identification, root cause mapping per stage | `python funnel_gap_analyzer.py --input funnel.json --output gaps.json` |
| `scripts/root_cause_ranker.py` | Evidence-weighted root cause ranking — 24 root causes across 8 domains, 22 evidence signals, prior × multiplier scoring, confidence assessment | `python root_cause_ranker.py --input signals.json --output ranked.json` |
| `scripts/corrective_action_prioritizer.py` | Action prioritization — Impact × Urgency × Feasibility scoring, timeline classification (immediate/short-term/structural), owner assignment, recovery timeline | `python corrective_action_prioritizer.py --input causes.json --output actions.json` |
| `references/diagnostic_framework.md` | Root-cause taxonomy (8 domains), funnel leakage map, 3 diagnostic decision trees, evidence signal catalog, benchmark search protocol | Read for diagnostic methodology |
| `references/corrective_action_playbook.md` | Corrective actions by domain (4 tables × 4 domains), escalation rules (6 severity levels), war room protocol (triage → diagnosis → action → recovery), recovery measurement expectations | Read for action planning and escalation |

### How to Use the Pipeline

```python
# Step 1: Funnel analysis
from scripts.funnel_gap_analyzer import FunnelGapAnalyzer
funnel_result = FunnelGapAnalyzer({
    "funnel_data": {
        "impressions": 2000000, "clicks": 28000, "visits": 24000,
        "engagement": 9600, "leads": 480, "qualified_leads": 120,
        "opportunities": 48, "sales": 12
    }
}).analyze()

# Step 2: Root cause ranking (add evidence signals)
from scripts.root_cause_ranker import RootCauseRanker
ranking_result = RootCauseRanker({
    "signals": ["ctr_declining_wow", "frequency_above_cap", "bounce_rate_above_70"],
    "funnel_root_causes": funnel_result.top_root_causes,
}).rank()

# Step 3: Corrective actions
from scripts.corrective_action_prioritizer import CorrectiveActionPrioritizer
actions = CorrectiveActionPrioritizer({
    "ranked_causes": ranking_result.ranked_causes[:3],
}).prioritize()
```

## Process

### Step 1 — Define the Gap
What is the KPI target vs actual? Quantify the gap. Is it delivery, cost, conversion, quality, or market?

### Step 2 — Run Funnel Analysis
Run `funnel_gap_analyzer.py` with available funnel data. Identify the primary leakage stage.

### Step 3 — Search Benchmarks
Search for current benchmarks by platform/industry/country before diagnosing. The gap may be "normal" for the market.

### Step 4 — Collect Evidence Signals
Ask for or identify supporting evidence: CTR trends, frequency data, page speed, CRM metrics, tracking status, market conditions. Each signal adjusts the root cause probabilities.

### Step 5 — Rank Root Causes
Run `root_cause_ranker.py` with signals + funnel leakage. The ranker scores 24 root causes by evidence weight.

### Step 6 — Separate Symptoms from Causes
"CPA increased" is a symptom. "Creative fatigue causing CTR decline causing CPA increase" is the causal chain. Always trace back to the root.

### Step 7 — Generate Corrective Actions
Run `corrective_action_prioritizer.py` on the top 3 root causes. Get prioritized actions with Impact × Urgency × Feasibility scores.

### Step 8 — Classify Actions by Timeline
Immediate (24-72h): quick wins, pauses, swaps. Short-term (1-2 weeks): rebuilds, tests. Structural (2-8 weeks): process changes, scope changes.

### Step 9 — Define Recovery Measurement
How will we know the fix worked? Define the metric, the target, and the review cadence. See playbook reference for recovery expectations.

### Step 10 — Produce the Diagnosis Report
Generate the full diagnosis with funnel map, root causes, actions, and executive summary.

## Output Format

Produce in TWO forms: **inline visual dashboard** (Visualizer) and **structured markdown report**.

### Visual Dashboard (Primary)

Render as inline HTML widget:

- **KPI gap header** — target vs actual with severity badge
- **Funnel leakage waterfall** — horizontal bar per stage showing actual rate vs benchmark, primary leakage highlighted in red
- **Root cause ranking** — top 5 causes as cards with domain badge, score, supporting signal count
- **Corrective action matrix** — 3 columns (immediate / short-term / structural) with actions prioritized by score
- **Evidence status** — signals provided vs needed (what data is missing?)
- **`sendPrompt()` buttons**: "Run control tower for full health check" → `weekly-control-tower`, "Design experiment to validate root cause" → `measurement-incrementality`, "Prepare recovery memo for leadership" → `executive-growth-memo`

### Markdown Report (Secondary)

```
## 🔍 PERFORMANCE DIAGNOSIS — [Campaign/Account] — [Client]

### Diagnosis verdict
[Most likely root cause with confidence level]

### KPI gap
| KPI | Target | Actual | Gap | Severity |

### Funnel leakage map
| Stage transition | Actual rate | Benchmark | Gap (pp) | Severity | Primary? |
[8 rows — highlight the leakage point]

### Root cause ranking
| Rank | Cause | Domain | Score | Supporting signals | Confidence |
[Top 5 causes]

### Corrective actions
#### Immediate (24-72h)
| Priority | Action | Root cause | Impact×Urgency×Feasibility | Owner |
#### Short-term (1-2 weeks)
| Priority | Action | Root cause | Score | Owner |
#### Structural (2-8 weeks)
| Priority | Action | Root cause | Score | Owner |

### Evidence gaps
[What data is missing? What signals would change the diagnosis?]

### Recovery measurement
| Metric | Current | Target | Expected recovery timeline |

### Executive summary
[2-3 sentences: what's wrong, why, what to do, when to expect recovery]
```

## Examples

**Example 1 — CPA rising:**
User: "CPA increased 40% WoW. Meta campaign. Budget unchanged."
→ Funnel: CTR dropped 25% (primary leakage at Impressions→Clicks). Signals: frequency_above_cap + ctr_declining_wow. Root cause #1: Creative fatigue (score 0.34). Immediate action: rotate creative. Short-term: brief new batch.

**Example 2 — Lead quality declining:**
User: "Getting leads but sales team says they're garbage. AcmeAuto MX."
→ Funnel: Leads→Qualified gap is 15pp below benchmark. Root cause #1: audience mismatch (wrong targeting). Root cause #2: form too simple (capturing unqualified). Actions: tighten targeting, add qualification questions.

**Example 3 — Full diagnosis with multiple issues:**
User: control tower shows health 45%, CPA anomaly, open rate declining.
→ Claude pulls control tower context. Funnel shows 2 leakage points (CTR + email engagement). Root causes: creative fatigue (media) + CRM frequency too high. Actions cascade: rotate creative (immediate), reduce email frequency (immediate), redesign journey (structural).

## Skill Chaining

| Direction | Skill | Connection |
|-----------|-------|------------|
| Upstream | `weekly-control-tower` | Health score + anomalies trigger diagnosis |
| Upstream | `media-routing-planner` | Media allocation context for media diagnosis |
| Upstream | `crm-journey-architect` | CRM journey data for CRM diagnosis |
| Upstream | `campaign-launch-qa` | QA gaps may explain performance issues |
| Downstream | `measurement-incrementality` | Design test to validate root cause |
| Downstream | `executive-growth-memo` | Frame diagnosis for leadership |
| Downstream | `creative-supply-planner` | If root cause is creative → plan new assets |
| Downstream | `change-order-generator` | If fix requires scope change → price it |
| Downstream | `media-routing-planner` | If root cause is media → re-optimize allocation |
