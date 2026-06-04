---
name: objection-handler
description: Generate responses to common sales objections — price, timing, competitor, need — with reframe scripts and follow-up questions.
triggers: ["handle objection", "objection response", "deal objection", "they said too expensive", "overcome objection"]
---

# Objection Handler

## What this skill does
Given a specific objection raised by a prospect, this skill generates a structured response playbook. For each objection type it produces an acknowledgment opener, a reframe that shifts the conversation, a proof point or bridge, and a follow-up question to re-engage and advance the deal. Covers price, timing, competitor, and need objections.

## How to invoke
/objection-handler [objection text or type] — [deal context (optional)]

## Workflow steps

### Step 1 — Classify the Objection
Identify the objection category and root cause:
- **Price** — "Too expensive," "Not in budget," "Need a discount"
- **Timing** — "Not now," "Bad timing," "Maybe next quarter"
- **Competitor** — "We're evaluating X," "We already use Y," "X is cheaper"
- **Need** — "We don't need this," "We can do it ourselves," "Status quo works fine"
- **Stakeholder** — "Need to get buy-in," "My boss won't approve," "Procurement is slow"

State the classification and the most likely underlying concern (cost pressure, risk aversion, relationship with incumbent, etc.).

### Step 2 — Acknowledge & Validate
Write a 1–2 sentence opener that acknowledges the objection without arguing or immediately pivoting. This builds credibility and trust. Example pattern: "I hear that — [restate their concern]. A lot of [role/company type] we talk to share the same concern at this stage."

### Step 3 — Reframe Script
Write a reframe that repositions the objection. For each objection type:
- **Price** → Shift from cost to cost of inaction or ROI; anchor to value delivered
- **Timing** → Surface the hidden cost of delay; tie to a triggering event or deadline
- **Competitor** → Acknowledge competitor strengths, then sharpen the differentiated wedge
- **Need** → Revisit confirmed pain; use their own words from discovery
- **Stakeholder** → Enable the champion; provide content to sell internally

### Step 4 — Proof Point or Bridge
Provide one relevant proof point: a customer story, benchmark, statistic, or analogy that reinforces the reframe. Keep it brief (2–3 sentences) and directly tied to their concern.

### Step 5 — Follow-up Question
Write 2–3 follow-up questions that re-engage the prospect and move the conversation forward. Questions should be open-ended and designed to either confirm the reframe landed or surface the real underlying objection if this one was a smokescreen.

## Example outputs
A response playbook with five labeled sections per objection: classification and root cause, acknowledge opener, reframe script, proof point, and follow-up questions. Can handle one objection in depth or generate a comparison table for multiple objections at once.
