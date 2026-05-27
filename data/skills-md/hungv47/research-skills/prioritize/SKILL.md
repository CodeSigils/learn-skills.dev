---
name: prioritize
description: "Brainstorms and prioritizes strategic solutions when the problem or goal is already clear — generates options, scores trade-offs, and recommends a path forward. Produces `.agents/skill-artifacts/meta/sketches/prioritize-*.md`. Not for diagnosing what the problem is (use diagnose) or engineering task lists (use task-breakdown). For setting numeric targets after prioritizing, see funnel-planner. For technical architecture of chosen initiatives, see system-architecture."
argument-hint: "[problem or goal to solve]"
allowed-tools: Read Grep Glob Bash WebSearch WebFetch
license: MIT
metadata:
  author: hungv47
  version: "2.0.0"
  budget: deep
  estimated-cost: "$1-3"
promptSignals:
  phrases:
    - "what to build first"
    - "what should we build next"
    - "which to build first"
    - "prioritize initiatives"
    - "ice score"
    - "which solution"
    - "strategic options"
    - "rank the options"
  allOf:
    - [what, build, prioritize]
    - [solution, prioritize]
    - [initiative, rank]
  anyOf:
    - "prioritize"
    - "ice"
    - "initiative"
    - "solution"
    - "trade-off"
  noneOf:
    - "market research"
    - "buyer persona"
  minScore: 6
routing:
  intent-tags:
    - prioritize
    - prioritization
    - ice-scoring
    - initiative-planning
    - strategic-options
  position: pipeline
  lifecycle: sketch
  produces:
    - .agents/skill-artifacts/meta/sketches/prioritize-*.md
  consumes:
    - product-context.md
    - market-research.md
    - .agents/skill-artifacts/meta/records/diagnose-*.md
  requires: []
  defers-to:
    - skill: discover
      when: "need to clarify HOW to build, not WHAT to pursue"
    - skill: system-architecture
      when: "need technical design, not strategic prioritization"
  parallel-with: []
  interactive: false
  estimated-complexity: heavy
---

# Solution Design — Orchestrator

*Strategy — Step 2 of 4. Brainstorms targeted solutions and ranks them with evidence-backed scoring.*

**Core Question:** "What's the highest-impact thing we can do about this?"

---

## Critical Gates — Read First

1. **Every initiative hypothesis MUST name the root cause.** Generic growth ideas produce low-impact, unfocused initiatives. If the hypothesis "because" clause doesn't reference the confirmed root cause, the initiative is untethered.
2. **Force-rank BEFORE scoring — ranking prevents "everything is a 6."** The forced ranking sets the ceiling for ICE scores. If you ranked it #1, its ICE should be highest.
3. **Anti-generic test is mandatory — "would this help ANY company?"** Delete the root cause reference from an initiative. If it still makes sense for any company, it's generic. Rewrite.
4. **≤3 initiatives above cut line — force the constraint.** More than 3 active initiatives means none get full attention. Parked initiatives have their turn after the current batch ships.

---

## Inputs Required
- Root cause from `.agents/skill-artifacts/meta/records/diagnose-*.md`

## Output
- `.agents/skill-artifacts/meta/sketches/prioritize-*.md`

## Chain Position
Previous: `diagnose` | Next: `funnel-planner` | Cross-stack: `system-architecture` (from product-skills — for initiatives requiring technical builds)

**Re-run triggers:** When root cause changes (re-diagnosis), when all "Proceed" initiatives are shipped or killed, or when new constraints emerge.

---

## Pre-Dispatch

This skill is **hard-gated** on `.agents/skill-artifacts/meta/records/diagnose-*.md`. No cold-start questioning — diagnose IS the upstream interview. Full Pre-Dispatch pattern: `references/_shared/pre-dispatch-protocol.md`.

**Hard gate:** `.agents/skill-artifacts/meta/records/diagnose-*.md` must exist. If missing → return **NEEDS_CONTEXT** and recommend running `diagnose` first. Do not substitute via interview — initiative ranking only makes sense against a validated root cause.

**Read order (post-gate):**
1. Pipeline: `.agents/skill-artifacts/meta/records/diagnose-*.md` (required). `research/product-context.md` (optional, for impact estimation). `research/icp-research.md` (optional, for audience-fit scoring).
2. Experience: `.agents/experience/{goals,business,product}.md`.

**Warm Start** (after gate passes):

```
Found:
- diagnose verdict → "[top root causes from diagnose.md]"
- product → "[from product-context.md]"

Generating initiatives against these root causes. Override or proceed?
```

If user proceeds, dispatch. No cold-start — diagnose has already done that work.

**Write-back:** none. prioritize doesn't seed dimensions to experience/ — initiatives are project-specific tactics, not stable user-profile state.

---

## Agent Manifest

| # | Agent | Layer | Focus | Input | Output |
|---|-------|-------|-------|-------|--------|
| 1 | [research-agent](agents/research-agent.md) | L1 | Root cause validation, case studies via WebSearch | Problem statement + root cause | Validated root cause, case studies, constraints |
| 2 | [initiative-generator-agent](agents/initiative-generator-agent.md) | L1.5 (parallel) | Standard initiative generation | Research-agent output | 5-10 initiatives with hypotheses |
| 3 | [unconventional-agent](agents/unconventional-agent.md) | L1.5 (parallel) | Asymmetric/non-obvious tactics | Research-agent output | 2-4 unconventional initiatives |
| 4 | [ranking-agent](agents/ranking-agent.md) | L2 (sequential) | Force-ranking all initiatives | Merged initiatives | Strict 1-through-N ranking |
| 5 | [ice-scoring-agent](agents/ice-scoring-agent.md) | L2 (sequential) | Evidence-backed ICE scoring | Ranked initiatives | Scored initiatives |
| 6 | [cut-line-agent](agents/cut-line-agent.md) | L2 (sequential) | Proceed/Park/Kill decisions | Scored initiatives | Decision table with validation |
| 7 | [critic-agent](agents/critic-agent.md) | L2 (sequential) | 8-point quality gate | Complete analysis | PASS or FAIL with fix routing |

---

## Routing Logic

### Route A: Full Analysis (Default)

For any non-trivial solution design. This is the default route.

```
Layer 1:        research-agent
                     ↓
Layer 1.5:      initiative-generator-agent + unconventional-agent (parallel)
                     ↓ merge
Layer 2:        ranking-agent → ice-scoring-agent → cut-line-agent → critic-agent
```

### Route B: Quick Design

When the root cause is well-established, constraints are known, and speed matters.

```
research-agent → initiative-generator-agent → ranking-agent → ice-scoring-agent → cut-line-agent → critic-agent
```

Skip unconventional-agent. Use when:
- The user has already identified approaches and wants prioritization
- Time is critical and the user confirms skipping unconventional scan
- The problem space is well-understood with clear standard solutions

---

## Dispatch Protocol

### Pre-Dispatch: Context Gathering

#### Step 0: Product Context

Check for `research/product-context.md`. If missing: **Strongly recommended:** run `icp-research` (from `hungv47/research-skills`) first to create `research/product-context.md` — this skill works without it but produces significantly better analysis with it. If the user prefers not to, ask the user 8 product questions (what, who, problem, differentiator, proof points, pricing, objections, voice) and save to `research/product-context.md`.

If `.agents/skill-artifacts/meta/records/diagnose-*.md` has a `date` field older than 30 days, recommend re-running `diagnose` before proceeding — the root cause landscape may have shifted.

#### Required Artifacts
| Artifact | Source | If Missing |
|----------|--------|------------|
| `diagnose.md` | diagnose | **STOP.** "Run `diagnose` first to identify the root cause." |

#### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `product-context.md` | icp-research (from hungv47/research-skills) | Constraints and capabilities context |
| `market-research.md` | market-research | Market gaps and competitive intelligence sharpen initiative generation |

#### Root Cause Review
Read `.agents/skill-artifacts/meta/records/diagnose-*.md`. Quote the root cause statement(s) and gap percentages. This anchor is necessary because generic growth ideas produce low-impact, unfocused initiatives.

#### Constraint Interview
Interview for:
- **Root cause context**: Confirm the root cause and gap size
- **Constraints**: Budget ceiling? Team size? Hard deadlines?
- **Prior attempts**: What's been attempted? What worked/didn't?

#### Route Selection
- Default → Route A (Full Analysis)
- If user requests speed OR problem has clear standard solutions → Route B

### Single-Agent Fallback

If the full orchestration is unnecessary (simple problem, few initiatives, user already has a ranked list), you may run the analysis inline without dispatching agents. Apply the same quality gate (8-point checklist) before delivering.

---

## Layer 1 — Research

Dispatch **research-agent**.

### research-agent
- **Input:** Problem statement, root cause from diagnose.md, gap percentages, constraints, prior attempts
- **References:** `references/_shared/hypothesis-framework.md` (use Framing B — Predictive), `references/initiative-types.md`
- **Expected output:** Validated root cause, 3-6 case studies with quantified results, unconventional tactic scan, constraint summary

---

## Layer 1.5 — Parallel: Initiative Generation

After research-agent returns, dispatch **initiative-generator-agent** and **unconventional-agent** simultaneously.

### initiative-generator-agent
- **Input:** Research-agent output (case studies, validated root cause, constraints)
- **References:** `references/_shared/hypothesis-framework.md` (use Framing B — Predictive), `references/initiative-types.md`, `references/initiative-planning.md`, `references/churn-playbook.md` (if root cause is churn)
- **Expected output:** 5-10 initiatives with hypotheses, mechanics, effort sizing, anti-generic checks

### unconventional-agent
- **Input:** Research-agent output
- **References:** `references/initiative-types.md`
- **Expected output:** 2-4 unconventional initiatives with risk assessments

### Layer 1.5 Merge

After both agents return:
1. Combine standard and unconventional initiatives into a single numbered list
2. Verify effort mix across the combined list: ≥2 Small, ≥2 Medium, ≥1 Large
3. If effort mix fails, send feedback to initiative-generator-agent to adjust
4. Present the full list to the user: *"Which resonate? Any to cut immediately? Any that spark a different idea?"*
5. Incorporate user feedback before passing to Layer 2

---

## Layer 2 — Sequential: Rank → Score → Cut → Critic

### Step 1: ranking-agent
- **Input:** Merged initiative list + user feedback
- **References:** `references/ice-scoring-rubric.md`
- **Expected output:** Strict 1-through-N forced ranking with reasoning per rank
- **Interview prompt:** *"If you could only do ONE of these, which would it be? And after that one?"*

### Step 2: ice-scoring-agent
- **Input:** Ranking-agent output + initiative list
- **References:** `references/ice-scoring-rubric.md`
- **Expected output:** ICE scores (1-10 each) with evidence citations, differentiation check

### Step 3: cut-line-agent
- **Input:** ICE-scoring-agent output
- **References:** `references/initiative-planning.md`
- **Expected output:** Proceed/Park/Kill decisions, capacity assessment, Proceed validation
- **Interview prompt:** *"How many can you execute well simultaneously?"*

### Step 4: critic-agent
- **Input:** Complete merged analysis
- **Expected output:** PASS or FAIL against 8-point quality gate

---

## Critic Gate

**Maximum 2 rewrite cycles.** If the critic returns FAIL:

1. Read the critic's failure report — it names the specific gate, the fix, and the agent to re-dispatch
2. Re-dispatch ONLY the named agent(s) with the critic's feedback
3. Re-merge and send back to critic-agent
4. If FAIL again after 2 cycles: deliver the artifact with a "Known Issues" section listing unresolved gate failures

## Out-of-Scope Persistence

After delivering the artifact, write killed initiatives to `.agents/skill-artifacts/meta/out-of-scope/` so future sessions don't re-analyze them:

For each initiative marked **Kill** in the Decisions table:

```markdown
# [Initiative Name]
**Decided:** [date]
**Context:** [root cause and goal that prompted this analysis]
**Decision:** Killed because [reason from Kill criteria]
**Revisit if:** [condition that would change the decision — e.g., "team grows to 5+", "root cause shifts to retention"]
```

Save as `.agents/skill-artifacts/meta/out-of-scope/[kebab-case-name].md`. Create the directory if it doesn't exist.

**Why:** Prevents re-debating settled decisions in future sessions. Navigate and discover read this directory before recommending workflows or asking about features already rejected.

---

## Artifact Template

On re-run: rename existing artifact to `prioritize.v[N].md` and create new with incremented version.

```markdown
---
skill: prioritize
version: 1
date: {{today}}
status: done | done_with_concerns | blocked | needs_context
---

# Solution Design

**Root Cause:** [from diagnose.md]

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

Run `funnel-planner` to set numeric targets for the proceeding initiatives.
If any "Proceed" initiative requires a technical build, also run `system-architecture` (from `hungv47/product-skills`) with these initiatives as context.
```

---

## Worked Example

**Root Cause:** Signups declined because (1) ad targeting brought low-intent visitors (~55%) and (2) homepage redesign lost trust signals (~35%).

### Layer 1: research-agent

Validates root cause, searches for case studies: "ad targeting quality case study", "homepage trust signals conversion case study". Finds 4 case studies with quantified results. Confirms constraints: 3-person growth team, no budget ceiling, prior attempts = none.

### Layer 1.5: Parallel Dispatch

**initiative-generator-agent** produces 6 standard initiatives:
1. Restore + Refine Paid Targeting (S)
2. Restore Homepage Social Proof (S)
3. Landing Page per Ad Group (M)
4. Homepage A/B: Old vs New (S)
5. Intent-Qualifying Ad Creative (M)
6. Dedicated Onboarding for Paid Visitors (L)

**unconventional-agent** produces 1 unconventional initiative:
- U1. Pixel Sharing with Complementary SaaS (M)

**Merge:** 7 initiatives total. Effort mix: 3S, 2M, 1L + 1M unconventional = passes (3S ≥2, 3M ≥2, 1L ≥1).

### Layer 2: Sequential

**ranking-agent** force-ranks 1-7. #1 = Restore Paid Targeting (biggest root cause, fastest fix).

**ice-scoring-agent** scores all 7. #1 gets ICE 25, #7 gets ICE 13. No more than 2 initiatives share a total.

**cut-line-agent** draws line: 2 Proceed (Restore Paid Targeting, Restore Social Proof), 2 Park, 3 Kill. Validates owners, baselines, kill criteria.

**critic-agent**: PASS — all 8 gates satisfied.

### Final Artifact

```markdown
# Solution Design

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

[...5 more initiatives]

## Phase 2: Prioritization

### Forced Ranking
1. Restore + Refine Paid Targeting — fastest fix for biggest root cause
2. Restore Homepage Social Proof — fast, addresses second root cause
3. Homepage A/B: Old vs New — definitive answer on redesign impact
4. Landing Page per Ad Group — higher effort but compounds with #1
5. Intent-Qualifying Ad Creative — interesting but less certain
6. Pixel Sharing with Complementary SaaS — unconventional, needs partner
7. Dedicated Onboarding for Paid — too complex for now

### ICE Scoring

| Rank | Initiative | I | C | E | ICE | Key Evidence |
|------|-----------|---|---|---|-----|-------------|
| 1 | Restore Paid Targeting | 8 | 8 | 9 | 25 | I:8 — paid is 60% of traffic, old targeting converted at 3.5% vs 1.2% now |
| 2 | Restore Social Proof | 7 | 7 | 9 | 23 | C:7 — Wayback shows old page had logos+testimonial that new page removed |
| 3 | Homepage A/B | 6 | 9 | 7 | 22 | C:9 — direct comparison eliminates guessing about redesign impact |
| 4 | LP per Ad Group | 7 | 6 | 5 | 18 | I:7 — message match lifts are well-documented (CXL: 20-50% improvement) |
| 5 | Intent Ad Creative | 5 | 4 | 6 | 15 | C:4 — no precedent with our audience, hypothesis only |
| 6 | Pixel Sharing | 4 | 3 | 5 | 12 | C:3 — requires finding willing partner, untested |
| 7 | Paid Onboarding | 7 | 3 | 3 | 13 | E:3 — needs eng + dynamic content, 4+ weeks |

### Decisions

| Initiative | Decision | Owner | Target Metric (Baseline) | Kill Criteria |
|------------|----------|-------|-------------------------|---------------|
| Restore Paid Targeting | **Proceed** | Sarah | Paid conversion: 1.2% | Stop if <2% after 10 days |
| Restore Social Proof | **Proceed** | James | Homepage bounce: 52% | Stop if >48% after 7 days |
| Homepage A/B | **Park** | — | — | Do after #1 and #2 ship |
| LP per Ad Group | **Park** | — | — | Revisit if paid targeting fix isn't enough |
| Intent Ad Creative | **Kill** | — | — | Too uncertain; paid targeting fix addresses the same root cause more directly |
| Pixel Sharing | **Kill** | — | — | Requires partner development; revisit if standard approaches underperform |
| Paid Onboarding | **Kill** | — | — | Too complex for current team capacity |

**Cut line:** 2 initiatives proceeding. Team: 3-person growth team.

## Next Step

Run `funnel-planner` to set targets for Restore Paid Targeting and Restore Social Proof.
```

---

## Anti-Patterns

**Generic initiatives** — "Improve SEO" or "Optimize onboarding" are categories, not initiatives. INSTEAD: Every initiative must describe a specific mechanic tied to a specific root cause. Run the anti-generic test: delete the root cause — does the idea still work for ANY company?

**Untethered ideas** — Ideas that sound good but don't connect to the confirmed root cause. INSTEAD: Every hypothesis "because" clause must reference the root cause. Root cause anchoring prevents the brainstorm from drifting into a generic growth playbook.

**All-small or all-large efforts** — Skewing entirely toward quick wins misses structural fixes; all-large stalls momentum. INSTEAD: Enforce effort mix: ≥2 Small, ≥2 Medium, ≥1 Large.

**"Everything is a 6" scoring** — When all ICE scores cluster together, the ranking is meaningless. INSTEAD: Force-rank before scoring to create differentiation. If you ranked it #1, its ICE should be highest.

**Naked scores without evidence** — "Impact: 7" with no justification invites political scoring. INSTEAD: Every score needs a one-sentence citation: what data or reasoning supports this number.

**Too many initiatives above cut line** — More than 3 active initiatives means none get full attention. INSTEAD: Force the ≤3 constraint. Parked initiatives have their turn after the current batch ships.

**Missing kill criteria** — Initiatives without a "stop if" threshold run forever. INSTEAD: Every "Proceed" initiative needs a specific metric, threshold, and duration that triggers a stop.

**Skipping the unconventional scan** — Only considering standard approaches when the root cause may need asymmetric leverage. INSTEAD: Run unconventional-agent alongside initiative-generator-agent unless Route B is explicitly chosen.

---

## Completion Status

Every run ends with explicit status:
- **DONE** — initiatives generated, ICE-scored, ranked, cut-line drawn (≤3 above), kill criteria attached, critic PASS
- **DONE_WITH_CONCERNS** — ranking complete but with sizing/impact uncertainty flagged at item level (e.g., effort estimates speculative, ICE inputs from interview not data)
- **BLOCKED** — `.agents/skill-artifacts/meta/records/diagnose-*.md` missing AND no other root-cause source available; STOP gate per skill body — recommend `diagnose` first
- **NEEDS_CONTEXT** — diagnose available but `research/product-context.md` missing for impact estimation; recommend `icp-research`

---

## References

- [references/_shared/hypothesis-framework.md](references/_shared/hypothesis-framework.md) — If/Then/Because structure and templates by initiative type (use Framing B — Predictive)
- [references/initiative-types.md](references/initiative-types.md) — Hero vs Support classification
- [references/ice-scoring-rubric.md](references/ice-scoring-rubric.md) — Detailed scoring calibration with scored examples
- [references/initiative-planning.md](references/initiative-planning.md) — Detailed execution planning for complex initiatives
- [references/churn-playbook.md](references/churn-playbook.md) — Cancel flow, dunning, health scores, exit-reason mapping (when root cause is churn)
- [references/churn-cancel-flow-templates.md](references/churn-cancel-flow-templates.md) — Email templates for cancel flow and dunning sequences
- [references/churn-health-score-guide.md](references/churn-health-score-guide.md) — Health score implementation and calibration
