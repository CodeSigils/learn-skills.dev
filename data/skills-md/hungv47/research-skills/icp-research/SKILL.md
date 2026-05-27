---
name: icp-research
description: "Builds ideal customer profiles and buyer personas — analyzes demographics, pain points, jobs-to-be-done, and segmentation for a target market. Produces `research/icp-research.md`. Not for competitive positioning (use prioritize) or campaign planning (use campaign-plan). For brand identity from audience data, see brand-system. For market sizing and competitor landscape, see market-research."
argument-hint: "[product or target market]"
allowed-tools: Read Grep Glob Bash WebSearch WebFetch
license: MIT
metadata:
  author: hungv47
  version: "3.0.0"
  budget: deep
  estimated-cost: "$1-3"
promptSignals:
  phrases:
    - "customer profile"
    - "buyer persona"
    - "target audience"
    - "who is my customer"
    - "ideal customer"
    - "customer segment"
  allOf:
    - [audience, research]
    - [customer, segment]
  anyOf:
    - "persona"
    - "demographic"
    - "psychographic"
    - "jobs-to-be-done"
    - "jtbd"
    - "voc"
  noneOf:
    - "competitor analysis"
    - "market size"
    - "tam"
  minScore: 6
routing:
  intent-tags:
    - audience-research
    - voc-research
    - persona-development
    - customer-profiling
  position: foundation
  lifecycle: canonical
  produces:
    - research/product-context.md
    - research/icp-research.md
  consumes: []
  requires: []
  defers-to:
    - skill: market-research
      when: "need competitive landscape, not audience research"
  parallel-with:
    - market-research
  interactive: false
  estimated-complexity: heavy
---

# ICP Research — Orchestrator

*Communication — Step 1 of 4. Foundational skill for all stacks. Coordinates sub-agents to build audience intelligence from real research, not assumptions.*

**Core Question:** "Who exactly are we talking to and what keeps them up at night?"

---

## Critical Gates — Read First

Non-negotiable constraints before dispatching any agent:
1. **No guessed personas — VoC or interview evidence only.** Every attribute traces to product context, brief, user input, or VoC quotes. Fabricated personas mislead 13+ downstream skills.
2. **Don't skip habitat mapping.** IMC planning needs specific community names with density and engagement type. "They're on LinkedIn" is not actionable.
3. **Max 2 personas.** More dilutes focus for 13+ downstream skills. If research reveals 4+ segments, force-rank by revenue potential.
4. **Stale product context (>30 days) → recommend re-running.** If `research/product-context.md` `Date` field is older than 30 days, warn and recommend re-run. If user proceeds, note "stale product context" in artifact header.

---

## Philosophy

Research structure, not rigid formula. Minimums for channels, quotes, and platforms ensure thoroughness — they're not arbitrary. If overwhelming evidence surfaces in 2 channels, a third isn't needed. Let evidence dictate depth. Orchestrator dispatches specialists per concern; critic ensures every section meets the bar.

## Inputs / Output
**Inputs:** Product context from `research/product-context.md` (or willingness to answer product questions).
**Outputs:** `research/icp-research.md` + `research/product-context.md` (foundational — written on first run, updated on re-run).

## Quality Gate
Critic agent verifies before delivery:
- [ ] Every VoC quote includes platform name and traces to a real source (not agent-generated)
- [ ] Each persona has a habitat map with specific channels and supporting evidence. Aim for 3+; document why if fewer.
- [ ] Each emotional driver traces to at least 2 specific quotes
- [ ] Decision psychology names specific cognitive biases and objections (not generic "they need trust")
- [ ] At least 15 VoC quotes across categories
- [ ] Maximum 2 personas

## Chain Position
Previous: none (or any skill needing audience context) | Next: `campaign-plan`, `brand-system` (marketing-skills).

**Foundational role:** Creates `research/product-context.md`, used by 13+ downstream skills across all 4 stacks (comms, strategy, prod, design). Run first for significantly better downstream output.
**Re-run triggers:** Audience pivot, new market entry, major product changes, or quarterly for active products.

### Skill Deference
- Competitive analysis / market sizing → `market-research`
- Campaign planning from personas → `campaign-plan`
- Brand identity using audience data → `brand-system`
- Diagnose a business problem (not audience) → `diagnose`

---

## Agent Manifest

| Agent | Layer | File | Focus |
|-------|-------|------|-------|
| Persona Agent | 1 (parallel) | `agents/persona-agent.md` | Demographics, role, goals, frustrations — builds persona cards |
| VoC Collector Agent | 1 (parallel) | `agents/voc-collector-agent.md` | Voice-of-customer quote collection from multiple platforms |
| Habitat Agent | 1 (parallel) | `agents/habitat-agent.md` | Platform/community mapping — where the ICP lives online |
| Pain Analysis Agent | 2 (sequential) | `agents/pain-analysis-agent.md` | Surface → Hidden → Emotional pain classification from VoC evidence |
| Decision Psychology Agent | 2 (sequential) | `agents/decision-psychology-agent.md` | Trigger events, research behavior, cognitive biases, objections |
| Synthesis Agent | 2 (sequential) | `agents/synthesis-agent.md` | Merges all fragments into coherent ICP profile |
| Critic Agent | 2 (final) | `agents/critic-agent.md` | Quality gate — PASS/FAIL evaluation with rewrite routing |

---

## Routing Logic

Classify the task, then follow the matching route.

### Route A: Quick ICP
**When:** Focused ICP, minimal scope — single persona, known audience, time-constrained.

```
1. Pre-dispatch: Gather context (Step 0)
2. Scope interview (Step 1)
3. LAYER 1 IN PARALLEL: persona-agent, voc-collector-agent
4. LAYER 2 SEQUENTIAL:
   - pain-analysis-agent (receives persona + VoC)
   - synthesis-agent (all upstream — skips habitat + decision psychology)
   - critic-agent
5. Critic FAIL → re-dispatch named agent(s) with feedback (max 2 cycles)
6. Deliver artifact
```

**Note:** Skips habitat-agent and decision-psychology-agent. Use when speed > depth. Artifact has empty Habitat Map and Decision Psychology sections — note as limitation.

### Route B: Full ICP
**When:** Comprehensive ICP research — full persona profiles, habitat mapping, decision psychology.

```
1. Pre-dispatch: Gather context (Step 0)
2. Scope interview (Step 1)
3. LAYER 1 IN PARALLEL: persona-agent, voc-collector-agent, habitat-agent
4. LAYER 2 SEQUENTIAL:
   - pain-analysis-agent (persona + VoC)
   - decision-psychology-agent (pain-analysis output)
   - synthesis-agent (ALL upstream)
   - critic-agent (synthesis output)
5. Critic FAIL → re-dispatch named agent(s) with feedback (max 2 cycles)
6. Deliver final artifact
```

### Route C: Called by Another Skill
**When:** Invoked by `campaign-plan`, `brand-system`, `copywriting`, or another skill needing audience context.

```
1. Pre-dispatch: Read context from caller's artifacts
2. Check research/icp-research.md:
   - Fresh (<30 days) → return existing
   - Stale (>30 days) → warn caller, recommend re-run
   - Missing → run Route B
3. Return artifact to caller
```

---

## Pre-Dispatch

Run the Pre-Dispatch protocol (`references/_shared/pre-dispatch-protocol.md`). icp-research is the canonical producer of `research/product-context.md` — Pre-Dispatch answers seed the artifact, then Layer 1 agents flesh it out.

**Needed dimensions:** product (1-line), primary buyer (role + size + B2B/B2C), top 1-2 pains, geo focus, route (Quick ICP / Full ICP).

**Read order:**
1. **Auto-scan first** (skill-specific): README.md, marketing site, pricing page, /docs, package.json. Extract product/buyer/pricing/voice signals to fill in what you can before asking.
2. Pipeline: existing `research/product-context.md` if present (re-run case).
3. Experience: `.agents/experience/{product,audience}.md`.

After scan + read, present findings and ask only about the gaps.

**Warm Start** (rich auto-scan or re-run with existing artifact):

```
Auto-scan / existing context found:
- product → "[1-line]"
- buyer → "[role + size]"
- pains → "[top 1-2]"

Need before dispatching: geo focus (US / EU / global / specific) and route (Quick ICP / Full ICP)?
```

**Cold Start** (no scan signal, no prior context):

```
icp-research builds the canonical product-context + audience profile that
13+ downstream skills read. To start:

1. **Product** — one sentence: what it does, who pays for it.
2. **Primary buyer** — role + company size + B2B/B2C.
3. **Top 1-2 pains** they articulate (verbatim if possible).
4. **Geo focus** — US / EU / global / specific.
5. **Route** — Quick ICP (single persona, fast) or Full ICP (full personas + habitats + decision psychology)?

Answer 1-5 in one response. I'll auto-scan README + marketing + pricing pages
to enrich, then dispatch Layer 1.
```

**Write-back:**

| Q | File | Key |
|---|---|---|
| 1. Product | `product.md` (also `research/product-context.md` as canonical) | `Product — one-line` |
| 2. Buyer | `audience.md` | `Audience — primary persona` |
| 3. Pains | `audience.md` | `Audience — pain points (primary)` |
| 4. Geo | `audience.md` | `Audience — geo focus` |
| 5. Route | (routing only, not persisted) |

---

## Step 0: Product Context Artifact

After Pre-Dispatch, generate or update `research/product-context.md` — the canonical product-context record other skills read:

```markdown
# Product Context

**Date:** [today]

## Product
[One sentence: what you sell]

## Buyer
[Primary buyer: role, company type, situation]

## Problem
[The pain it solves — in their words, not yours]

## Differentiator
[What's different — something a competitor CANNOT claim]

## Social Proof
[Best testimonial or most repeated praise]

## Model
[Price, pricing model, free trial availability]

## Voice
[3 adjectives: e.g., "direct, technical, warm"]

## Primary CTA
[What should people do next: e.g., "Start free trial"]

## Canonical Terminology
| Term | Definition | Don't use |
|------|-----------|-----------|
| [canonical term] | [precise definition] | [synonyms to avoid] |
```

Canonical Terminology defines shared vocabulary for product and domain. Downstream skills (campaign-plan, copywriting, humanize, lp-brief, design-brief) reference this for consistent language. Populate during scope interview — ask: "What do you call your users? Pricing tiers? Main workspace?" If no strong preferences, propose defaults from codebase (variable names, UI labels, docs).

All marketing skills read this file for product context.

### Required Artifacts
| Artifact | Source | If Missing |
|----------|--------|------------|
| `product-context.md` | icp-research | **INTERVIEW** for 8 product dimensions, save to `research/product-context.md`. |

### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `diagnose.md` | diagnose (hungv47/research-skills) | Problem context sharpens audience research |

---

## Step 1: Scope Interview

Interview for:
1. **Who are we researching?** (Role, mindset, community, or use case)
2. **What decisions will this inform?** (Messaging? Channels? Positioning? All three?)
3. **B2C or B2B?** Geography? Segments to focus or exclude?

Answers determine route (A, B, or C) and populate the brief passed to agents.

---

## Dispatch Protocol

### How to spawn a sub-agent

For each agent dispatched below, use the **Agent tool** with a prompt built as follows:

1. **Read** the agent instruction file (e.g., `agents/persona-agent.md`) — include FULL content in the Agent prompt
2. **Append** brief and context after instructions
3. **Resolve paths to absolute**: replace relative paths with absolute paths rooted at this skill's directory (e.g., `references/voice-of-customer.md` → `/path/to/icp-research/references/voice-of-customer.md`). Tell agent: "Read reference file at [absolute path] for domain knowledge."
4. **Pass upstream artifacts by content, not path**: orchestrator reads `research/product-context.md` first, then includes relevant excerpts (product, buyer, problem, differentiator) in context. Sub-agents do NOT read artifacts directly — orchestrator curates.
5. If **feedback** exists (critic FAIL cycle), append at end with header "## Critic Feedback — Address Every Point"

### Single-agent fallback

If multi-agent dispatch unavailable (no Agent tool, single-agent runtime, context constraints), execute each agent's instructions sequentially in-context:
- **Layer 1:** Run each agent's instructions one at a time — persona, VoC collection, habitat mapping
- **Layer 2:** Apply pain analysis to Layer 1 outputs, then decision psychology, then synthesis
- **Critic:** Self-evaluate using critic-agent quality gate
- Produce the complete artifact as if all agents had run

Output quality is equivalent — multi-agent pattern optimizes parallelism and focus, not capability.

---

## Layer 1: Parallel Research Agents

Spawn **IN PARALLEL** (multiple Agent tool calls in one message). Follow Dispatch Protocol above.

| Agent | Instruction File | Pass These Inputs | Reference Files to Resolve |
|-------|-----------------|-------------------|---------------------------|
| Persona Agent | `agents/persona-agent.md` | brief + product context | — |
| VoC Collector Agent | `agents/voc-collector-agent.md` | brief + product context | `references/voice-of-customer.md`, `references/customer-interviews.md` |
| Habitat Agent | `agents/habitat-agent.md` | brief + product context | `references/habitat-mapping.md` |

**Quick ICP (Route A):** Dispatch only persona-agent and voc-collector-agent. After Layer 1, orchestrator holds all outputs (persona cards, VoC library, habitat map) ready for Layer 2.

---

## Layer 2: Sequential Analysis Chain

Dispatch **ONE AT A TIME, IN ORDER** via Dispatch Protocol. Each receives the previous agent's output (plus relevant Layer 1 outputs) as `upstream`.

```
pain-analysis-agent → decision-psychology-agent → synthesis-agent → critic-agent
```

| Step | Agent | Instruction File | Receives |
|------|-------|-----------------|----------|
| 1 | Pain Analysis Agent | `agents/pain-analysis-agent.md` | persona-agent output + voc-collector-agent output |
| 2 | Decision Psychology Agent | `agents/decision-psychology-agent.md` | pain-analysis-agent output |
| 3 | Synthesis Agent | `agents/synthesis-agent.md` | ALL upstream: persona + VoC + habitat + pain + psychology |
| 4 | Critic Agent | `agents/critic-agent.md` | synthesis-agent output |

**Quick ICP (Route A):** Skip decision-psychology-agent. Pain-analysis feeds directly to synthesis, then critic.

---

## Critic Gate

Critic returns one of two verdicts:

### PASS
Artifact meets all quality standards. Deliver synthesis output to `research/icp-research.md`.

### FAIL
Critic returns:
- Which gate failed and what's wrong
- Specific fix instructions
- Which agent to re-dispatch

**Rewrite loop:**
1. Read failure report
2. Re-dispatch ONLY the named agent(s) with critic feedback as `feedback` input
3. If fix affects downstream agents, re-run chain from fixed agent forward
4. Run modified output back through critic
5. **Max 2 rewrite cycles.** After 2 failures, deliver with annotations and flag: "ICP scored below quality gate — manual review recommended on [specific sections]."

---

## Artifact Template

```markdown
---
skill: icp-research
version: 1
date: [today's date]
status: done | done_with_concerns | blocked | needs_context
---

# ICP Research

**Date:** [today]
**Skill:** icp-research
**Product:** [from product-context.md]

## Persona 1: [Name/Archetype]

**Demographics:** [Age, role, industry, company size]

### Pain Profile
1. **[Pain name]** — [description]
   - Trigger: [what causes acute pain]
   - Impact: [daily/financial/professional]
   - Quote: "[exact quote]" — [Platform, context]
   - Quote: "[exact quote]" — [Platform, context]

2. **[Pain name]** — [description]
   [Same format]

3. **[Pain name]** — [description]
   [Same format]

### Decision Psychology
- **Trigger:** [what event starts their search]
- **Research path:** [where they go 1st → 2nd → 3rd]
- **Key biases:** [which cognitive biases are strongest]
- **Objections:** (1) [objection] — root: [psychological reason]. (2) [objection] — root: [reason]. (3) [objection] — root: [reason].
- **Trust signals:** [what they trust]
- **Distrust triggers:** [what kills credibility]

### Habitat Map
| Platform | Community | Density | Engagement | Role |
|----------|-----------|---------|-----------|------|
| [Specific] | [Specific] | H/M/L | [Type] | [Role] |

## Persona 2: [Name/Archetype]
[Same format]

## Top 3 Emotional Drivers
1. **[Driver]** — [explanation]. Quotes: "[quote 1]" ([source]), "[quote 2]" ([source])
2. **[Driver]** — [explanation]. Quotes: ...
3. **[Driver]** — [explanation]. Quotes: ...

## Red Flags
- [Language/positioning that triggers skepticism and why]

## Next Step
Run `campaign-plan` to turn these insights into a communication plan.

> On re-run: rename existing artifact to `icp-research.v[N].md` and create new with incremented version.
```

---

## Worked Example — Full ICP (Route B)

**Brief:** "Research my ICP for a project management tool aimed at engineering teams."

### Step 0: Pre-Dispatch
Product context scanned from README.md and pricing page. Saved to `research/product-context.md`:
- Product: ProjectSync — async project visibility for engineering teams
- Buyer: Engineering managers at mid-size SaaS companies
- Problem: Hours lost to status updates nobody reads

### Step 1: Scope Interview
- "Who?" → Engineering managers at mid-size SaaS companies (50-200 engineers)
- "What decisions?" → Messaging and channel strategy for launch
- "B2B/B2C?" → B2B, US and EU
- **Route selected:** B (Full ICP — comprehensive research needed for launch)

### Layer 1: Parallel Dispatch

Three agents dispatched simultaneously:

**Persona agent** returns:
> ### Persona 1: The Overwhelmed EM
> **Demographics:** 30-38, Engineering Manager, B2B SaaS, 50-200 engineers
> **Goals:** (1) Ship on schedule without burning out the team. (2) Give leadership visibility without micromanaging.
> **Frustrations:** "I spend more time telling people what I did than actually doing it." "Our standups are 45 minutes of reading Jira tickets aloud."
> **Day-in-the-life:** Monday 9am — Sarah opens Slack to 47 unread messages, half status updates she needs to compile for her VP by 10am.

**VoC collector agent** returns:
> 18 quotes across 5 categories from r/ExperiencedDevs, r/engineeringmanagers, G2, Twitter, LinkedIn. Key mechanism quote: "No single tool shows me what my team actually shipped this week — I have to check Jira, GitHub, and Slack separately and piece it together."

**Habitat agent** returns:
> | Platform | Community | Density | Engagement | Role |
> |----------|-----------|---------|-----------|------|
> | Reddit | r/ExperiencedDevs | H | Engager | Trust |
> | Reddit | r/engineeringmanagers | M | Lurker | Trust |
> | LinkedIn | #engineeringmanagement feed | M | Creator | Discovery |
> | Twitter/X | #engmanagement | L | Lurker | Discovery |
> | Slack | Rands Leadership Slack | H | Engager | Trust |

### Layer 2: Sequential Dispatch

**Pain analysis agent** receives persona + VoC output. Returns:
> #### 1. Status Update Theater — hours lost compiling updates nobody reads
> - **Level:** Surface → Hidden (spreadsheet workarounds) → Emotional (fear of looking disorganized)
> - **Trigger:** Monday 9am — VP expects status email by 10am
> - **Impact:** 6-8 hrs/week on reporting. Career: EMs who can't show visibility get passed over.
> - **Mechanism:** No single system aggregates team activity. The EM becomes the human integration layer.

**Decision psychology agent** receives pain analysis output. Returns:
> - **Trigger:** Promoted to manage second team — reporting overhead doubles
> - **Research path:** 1st Reddit (r/ExperiencedDevs) → 2nd G2 comparisons → 3rd free trial
> - **Key biases:** Status-quo bias (invested in current Jira setup), loss aversion (fear of losing data in migration)
> - **Objections:** (1) "We already have Jira" — root: sunk cost + status-quo bias. (2) "My team won't adopt another tool" — root: diffusion of responsibility. (3) "How is this different from Monday.com?" — root: category fatigue.

**Synthesis agent** receives all upstream. Merges into complete ICP artifact matching the template. Adds:
> ## Top 3 Emotional Drivers
> 1. **Fear of being perceived as unable to scale** — EMs who can't produce visibility for leadership fear being passed over for promotion or labeled as "not ready for director." Quotes: "My skip-level keeps asking me for updates I can't produce fast enough" (r/engineeringmanagers), "I got feedback that I 'lack strategic visibility' and I don't even know what that means" (r/ExperiencedDevs)

### Critic Gate → PASS
All 7 gates pass. 18 quotes with attribution. Habitats are specific. Biases are named. Drivers traced to 2+ quotes each. Artifact delivered to `research/icp-research.md`.

---

## Anti-Patterns

**Guessing personas without evidence** — Inventing "Sarah, 34, EM" because it sounds right, without VoC quotes or brief details. INSTEAD: Persona agent builds from product context and brief; pain analysis agent validates against VoC.

**Skipping habitat mapping for speed** — Dropping habitat agent because "we know they're on Reddit." INSTEAD: Use Route A (Quick ICP), which explicitly skips habitats and notes the limitation. Don't silently omit sections.

**Fabricating VoC quotes** — Generating plausible quotes when research returns thin results. INSTEAD: Document gaps honestly, flag confidence LOW, recommend user provide customer quotes, support tickets, or sales call notes.

**Too many personas** — 3+ personas because research surfaced distinct segments. INSTEAD: Force-rank to 2 max by revenue potential. Document who was cut and why in Segment Rationale.

**Platform-level habitat mapping** — "They're on LinkedIn" without naming the group, hashtag, or content type. INSTEAD: Every entry names a specific community. Habitat agent enforces this.

**Recycling stale research** — Reusing personas and VoC without re-validation. INSTEAD: Check artifact date. If >30 days, recommend re-run. Markets shift, competitors launch, pain points evolve.

**Ignoring critic FAIL** — Delivering a failed artifact because "close enough." INSTEAD: Re-dispatch named agent with critic feedback. Max 2 cycles, then deliver with annotations.

---

## Completion Status

Every run ends with explicit status:
- **DONE** — full ICP synthesized, critic PASS, all 5-7 dimensions populated with quoted evidence
- **DONE_WITH_CONCERNS** — critic PASS but Route A (Quick ICP) used so habitat/decision-psychology omitted, OR VoC quote density thin (flagged in artifact)
- **BLOCKED** — irreconcilable persona contradictions surfaced (e.g., two distinct buyers with no merge path); needs user scope decision
- **NEEDS_CONTEXT** — `research/product-context.md` missing AND user can't describe product/audience; recommend interview sub-flow first

---

## Agent Files

### Sub-Agent Instructions (agents/)
- [agents/persona-agent.md](agents/persona-agent.md) — Demographics, role, goals, frustrations — persona card builder
- [agents/voc-collector-agent.md](agents/voc-collector-agent.md) — VoC quote collection from multiple platforms
- [agents/habitat-agent.md](agents/habitat-agent.md) — Platform/community mapping with density and engagement
- [agents/pain-analysis-agent.md](agents/pain-analysis-agent.md) — Surface → Hidden → Emotional pain classification
- [agents/decision-psychology-agent.md](agents/decision-psychology-agent.md) — Triggers, biases, objections, trust/distrust signals
- [agents/synthesis-agent.md](agents/synthesis-agent.md) — Merges fragments into coherent ICP artifact
- [agents/critic-agent.md](agents/critic-agent.md) — Quality gate — PASS/FAIL with rewrite routing
- [agents/_template.md](agents/_template.md) — Reusable template for creating new agent files

### Shared References (references/)
- [references/voice-of-customer.md](references/voice-of-customer.md) — VoC collection patterns, quote categories, platform tips (voc-collector-agent)
- [references/customer-interviews.md](references/customer-interviews.md) — Win/loss interview methodology, support ticket analysis (voc-collector-agent)
- [references/habitat-mapping.md](references/habitat-mapping.md) — Density definitions, engagement types, cross-persona analysis (habitat-agent)
- [references/icp-to-imc-handoff.md](references/icp-to-imc-handoff.md) — How to package outputs for IMC planning (synthesis-agent)
