---
name: deal-review
description: Analyze a deal's health with MEDDIC scoring, risk flags, missing stakeholders, and recommended next actions.
triggers: ["review deal", "deal review", "deal health", "MEDDIC", "analyze deal", "deal score"]
---

# Deal Review

## What this skill does
Given a deal summary — stage, stakeholders, use case, timeline, and budget signals — this skill produces a structured deal health assessment. It scores the deal against the MEDDIC framework, surfaces risk flags, identifies stakeholder gaps, and recommends prioritized next actions to advance or save the deal.

## How to invoke
/deal-review [deal name or company] — [current stage] — [deal summary or CRM notes]

## Workflow steps

### Step 1 — MEDDIC Scorecard
Score each MEDDIC dimension on a 0–2 scale (0 = unknown/missing, 1 = partially confirmed, 2 = fully confirmed). Provide a brief justification for each score based on the deal inputs.

| Dimension | Score (0–2) | Status | Evidence / Gap |
|---|---|---|---|
| **M** — Metrics | | | |
| **E** — Economic Buyer | | | |
| **D** — Decision Criteria | | | |
| **D** — Decision Process | | | |
| **I** — Identify Pain | | | |
| **C** — Champion | | | |

Compute a total MEDDIC score (out of 12) and a deal health label: **Strong** (10–12), **Developing** (6–9), **At Risk** (0–5).

### Step 2 — Risk Flags
Identify the top 3–5 risk signals in the deal. Common risk categories:
- **Stakeholder risk** — No access to economic buyer; single-threaded into one contact
- **Timeline risk** — No triggering event; artificial or vague close date
- **Competitive risk** — Incumbent entrenched; evaluation started with a competitor
- **Champion risk** — Champion lacks authority or internal credibility
- **Budget risk** — No confirmed budget; deal size misaligned with company profile
- **Process risk** — Procurement or legal involvement not scoped; unknown approval steps

For each flag, note severity (High / Medium / Low) and the specific signal from the deal that triggered it.

### Step 3 — Stakeholder Map
List all known stakeholders with their role, level of engagement (Champion / Supporter / Neutral / Blocker / Unknown), and last touch date if available. Then identify the critical missing stakeholders that should be engaged before the deal closes: typically the economic buyer, a technical validator, and a procurement/legal contact.

### Step 4 — Deal Momentum Assessment
Assess whether the deal has forward momentum or is stalling. Look for: time since last meaningful touchpoint, whether the prospect has completed their agreed next steps, whether the close date has slipped, and whether the champion is actively selling internally. Classify as **Advancing**, **Stalled**, or **At Risk of Going Dark**.

### Step 5 — Recommended Next Actions
Provide 3–5 prioritized next actions ranked by impact on deal health. For each action include: what to do, who owns it (rep, champion, AE), and the goal it addresses (MEDDIC gap, risk mitigation, or momentum). Format as a short action table with a suggested completion date.

## Example outputs
A structured deal review document with a completed MEDDIC scorecard and total score, a ranked risk flag list with severity labels, a stakeholder map with engagement status, a momentum classification, and a prioritized next-actions table. Suitable for pipeline reviews, forecasting calls, or deal strategy sessions with a manager.
