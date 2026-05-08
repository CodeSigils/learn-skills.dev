---
name: cold-outreach
description: "Writes and evaluates cold outreach — email, LinkedIn, Twitter/X, platform proposals — with signal-based personalization, channel-specific craft, and rubric scoring. Produces `.agents/mkt/cold-outreach/[slug].md` (+ `.rationale.md` + `.critic-score.md`). Handles first-touch compose and reply-to-inbound modes. Not for campaign orchestration or sequence design (compose touches individually, pass prior touches as context). Not for sourcing/list-building (start at 'here's who I'm reaching'). Brand voice: see brand-system. AI-sounding cleanup: humanize runs as terminal pass."
argument-hint: "[target/signal + channel + mode, or reply text to respond to]"
allowed-tools: Read Grep Glob Bash WebSearch WebFetch
license: MIT
metadata:
  author: hungv47
  version: "1.0.0"
  budget: deep
  estimated-cost: "$1-3"
promptSignals:
  phrases:
    - "cold email"
    - "cold outreach"
    - "cold dm"
    - "linkedin dm"
    - "linkedin outreach"
    - "upwork proposal"
    - "prospect email"
    - "reply to this prospect"
    - "first-touch email"
    - "follow-up email"
  anyOf:
    - "cold outreach"
    - "cold email"
    - "cold dm"
    - "prospect"
    - "outbound"
    - "upwork proposal"
    - "fiverr proposal"
    - "connection request"
  allOf:
    - [write, cold]
  noneOf:
    - "newsletter"
    - "lifecycle email"
    - "drip campaign"
    - "nurture sequence"
    - "transactional email"
  minScore: 6
routing:
  intent-tags:
    - cold-outreach
    - cold-email
    - cold-dm
    - prospect-message
    - platform-proposal
    - reply-handling
  position: horizontal
  produces:
    - mkt/cold-outreach/[slug].md
    - mkt/cold-outreach/[slug].rationale.md
    - mkt/cold-outreach/[slug].critic-score.md
  consumes:
    - product-context.md
    - icp-research.md
    - mkt/campaign-plan.md
  requires: []
  defers-to:
    - skill: copywriting
      when: "need headline, hook, or landing-page copy (not an outbound message)"
    - skill: campaign-plan
      when: "need channel strategy or multi-channel campaign orchestration across paid/owned/earned"
  parallel-with: []
  interactive: false
  estimated-complexity: heavy
---

# Cold Outreach — Orchestrator

*Communication — Horizontal. Ready-to-send outbound across email, LinkedIn, Twitter/X, platform proposals. Multi-agent strategy → draft → voice → critic → humanize pipeline.*

**Core Question:** "If I removed the personalization, would this email still make sense? If yes, the personalization isn't working."

## Philosophy

Cold outreach is not template-filling. It's writing as a sharp colleague who noticed something relevant — the reader's world dominates, not yours. Every sentence must earn its place. Frameworks (O→P→P→A, Q→V→A) are tools, not mandates. Test: would YOU reply to this?

The orchestrator separates strategy from craft: specialists pick angle/signal/proof/CTA in parallel, composer drafts with channel rules, voice-auditor strips vendor-speak, critic scores a 5-dimension rubric, `humanize` is the terminal pass for AI tells. Output is ready-to-send + rationale — not a draft to rewrite.

## Scope Boundary

**In scope:**
- First-touch compose: email / LinkedIn (DM + connection note) / Twitter/X (reply + DM) / platform proposals (Upwork, Fiverr, similar)
- Reply to inbound (objection handling + next-touch)
- Multi-touch coherence via optional `prior-touches` input
- Modes: services-sell (consulting/agency) / saas-sell / partnership-sell / community-sell

**Out of scope:**
- Sourcing, list-building, scraping (your tool stack)
- Multi-touch sequence as a single artifact (compose one at a time)
- Sequence diagnosis / A-B testing (future skill)
- Fundraise outreach (VC/warm-intro norms differ); hiring outreach (candidate-sourcing differs)
- Sending / tracking / inbox warmup (Instantly, Lemlist, Smartlead layer)
- Voice memos, cold-call scripts

## Inputs Required

**Always:**
- **Channel**: email | linkedin-dm | linkedin-connection | twitter-reply | twitter-dm | upwork-proposal | other-platform
- **Mode**: services-sell | saas-sell | partnership-sell | community-sell

**Strongly recommended (skill asks if missing and signal is weak):**
- **Target**: name + role + company (min); LinkedIn URL / context ideal
- **Trigger signal**: what prompted reach-out — funding, hiring, launch, tech-stack, individual post, referral, event
- **Your offer**: what you sell, for whom, what specific problem
- **Proof**: one concrete result, case study, or credibility anchor

**Optional but powerful:**
- **Prior touches** (touch 2/3/4+): paste prior verbatim so the skill keeps coherence
- **ICP artifact** auto-consumed from `research/icp-research.md` if present
- **Product context** auto-consumed from `research/product-context.md` if present
- **Prospect quote / language**: words from their post or profile — highest-signal fuel

## Output

Writes to `.agents/mkt/cold-outreach/`:

| File | Content |
|------|---------|
| `[slug].md` | Final ready-to-send draft (+ subject line for email, + connection-note variant for LinkedIn) |
| `[slug].rationale.md` | Angle chosen, framework used, signal selected, CTA logic, channel craft rules applied, anti-patterns avoided |
| `[slug].critic-score.md` | Rubric scorecard across 5 dimensions (for iteration) |

Slug is derived from target + channel (e.g., `jane-acme-email-t1`, `jane-acme-linkedin-dm`, `jane-acme-email-t2-followup`).

### Artifact Frontmatter (required)

Every `[slug].md` carries:

```yaml
---
skill: cold-outreach
version: 1
date: YYYY-MM-DD
status: done | done_with_concerns | blocked | needs_context
channel: email | linkedin-dm | linkedin-connection | twitter-reply | twitter-dm | upwork-proposal | other-platform
mode: services-sell | saas-sell | partnership-sell | community-sell
touch: integer | "breakup"   # 1, 2, 3, 4+, or "breakup"
route: compose | reply
critic_total: N/50
---
```

## Quality Gate

Before delivering, the **critic agent** verifies (5 dimensions, 0-10 each):

- [ ] **Peer voice** ≥ 6 — sharp human, no vendor-speak ("leverage", "synergy", "best-in-class", "I hope this finds you well")
- [ ] **Signal connection** ≥ 6 — personalization connects to the ask; remove-the-opener test passes (email shouldn't still make sense without it)
- [ ] **CTA friction** ≥ 6 — one ask, low-friction; no "30-min call" in first touch
- [ ] **You > me ratio** ≥ 6 — "you/your" dominates "I/we/our"; reader's world, not yours
- [ ] **Specificity** ≥ 6 — concrete proof (number, named outcome, named company); no "leading provider" / "trusted by many"

**Gate:** Total ≥ 35/50 **AND every dim ≥ 6**. Total 35-39 with all dims ≥ 6 = PASS as `DONE_WITH_CONCERNS`. Any dim < 6 = FAIL regardless of total.

Below threshold → full Layer 2 chain (composer → voice-auditor → critic) re-runs with feedback (max 2 cycles).

After critic PASS, `humanize` is the terminal pass. Orchestrator then re-runs critic's **Specificity dimension only** on humanized text — if Specificity drops ≥2 OR any named entity/number present pre-humanize is absent post-humanize, revert to critic-approved draft. Protects the specificity anchor the critic just scored.

## Chain Position

Horizontal — runs standalone or called by `campaign-plan` when outbound is part of a broader mix.

**Re-run triggers:** ICP changes materially, new trigger signal appears for same prospect, prior sequence got no reply and angle needs refresh.

### Skill Deference
- **LP headline / tagline / ad CTA?** → `copywriting` (writing craft, not outbound)
- **Multi-channel campaign across paid/owned/earned?** → `campaign-plan` first, then this skill for the touches
- **No persona, or ICP stale (>30d)?** → `icp-research` first
- **Sequence underperforming, need diagnosis?** → Not this skill (future `outbound-diagnose`)
- **Lifecycle / nurture / drip?** → NOT this skill. Those are warm, consent-based, different craft.

---

## Agent Manifest

| Agent | Layer | File | Focus |
|-------|-------|------|-------|
| Signal Analyst | 1a (solo, first) | `agents/signal-analyst.md` | Rates trigger-signal strength (1-5), drafts the observation line, flags weak/generic signals. Runs FIRST because strategist + proof-selector consume its `signal_strength` score. |
| Strategist | 1b (parallel) | `agents/strategist.md` | Picks framework (O→P→P→A, Q→V→A, Trigger→Insight→Ask, Story→Bridge→Ask, Declared-Need→Relevant-Proof→Specific-Next-Step, No-pitch connection note), angle, CTA shape. Receives `signal_strength` from 1a. |
| Proof Selector | 1b (parallel) | `agents/proof-selector.md` | Picks strongest proof asset from the `available_proof[]` pool: named case study > named logo + metric > specific claim > generic. Receives `signal_strength` from 1a for tie-breaking. |
| Composer | 2 (sequential, post-merge) | `agents/composer.md` | Drafts the message applying channel-specific craft rules (length, structure, subject line, formatting) |
| Voice Auditor | 2 (sequential) | `agents/voice-auditor.md` | Peer-voice audit — strips vendor-speak, enforces contractions, cuts filler, verifies "you > me" |
| Critic | 2 (sequential, gate) | `agents/critic.md` | Rubric scoring across 5 dimensions, PASS/FAIL with rewrite feedback. Reads `references/anti-patterns.md` for banned-phrase auto-fails. |
| Reply Classifier | 1 (reply mode) | `agents/reply-classifier.md` | Types inbound reply: not-interested / no-budget / send-info / wrong-person / curious / qualified / later / hostile / ambiguous |
| Reply Composer | 2 (reply mode) | `agents/reply-composer.md` | Drafts response per classification + next-touch logic |

### Shared References (read by multiple agents)

**Channel craft (channels/):**
- `references/channels/email.md` — subject lines, length targets, structure, formatting, breakup email
- `references/channels/linkedin.md` — connection-note (≤300 chars) vs post-accept DM vs InMail distinctions
- `references/channels/twitter.md` — public reply craft vs DM craft, demand-signal reading
- `references/channels/platform-proposals.md` — Upwork/Fiverr: pitching into declared need

**Mode defaults (modes/):**
- `references/modes/services.md` — consulting/agency: audit/loom/teardown CTAs, revenue-tied problems, value-based positioning
- `references/modes/saas.md` — product-led framing, trial/demo CTAs, ROI proof shapes
- `references/modes/partnership.md` — B2B partnership/collab/integration
- `references/modes/community.md` — low-ask value-first (helpful note, resource offer)

**Frameworks (frameworks/):**
- `references/frameworks/structures.md` — Observation→Problem→Proof→Ask and 4 other proven shapes
- `references/frameworks/personalization-signals.md` — 4-level signal system + trigger catalogue (funding, hiring, post, tech-stack, event)
- `references/frameworks/ctas.md` — low-friction asks, interest-based vs meeting-request, one-line-reply CTAs
- `references/frameworks/objections.md` — reply playbooks per classification

**Shared guardrails:**
- `references/anti-patterns.md` — AI tells, template smell, phrases that kill replies
- `references/proof-types.md` — proof hierarchy: named case study > named logo + metric > specific claim > generic

---

## Routing Logic

Classify the task, then follow the matching route.

### Route A: Compose (First-Touch or Follow-Up)

**When:** Outbound message — first touch, follow-up touch 2/3/4+, or cold DM on any channel.

```
1. Pre-dispatch: Gather context (Step 0)
   - Mode or channel missing → ask (AskUserQuestion)
   - Target + signal both missing → ask; if only signal missing and strong persona exists → proceed with weak-signal flag
   - Slug ends `-t2`/`-t3`/etc. OR user says follow-up → require prior_touches verbatim; BLOCK if missing (composer needs them to avoid angle repetition)
2. LAYER 1a — signal-analyst SOLO (must complete before 1b):
   - rates signal strength (1-5), drafts observation line
3. LAYER 1b — PARALLEL (both receive `signal_strength` from 1a):
   - strategist (framework + angle + CTA shape)
   - proof-selector (strongest proof from available_proof[])
4. MERGE: assemble Layer 1 outputs into a strategy brief
5. LAYER 2 — SEQUENTIAL:
   - composer (strategy brief + channel ref + mode ref)
   - voice-auditor (composer output)
   - critic (voice-audited draft + pre_writing verbatim, applies rubric)
6. Critic FAIL → re-dispatch FULL Layer 2 chain (composer → voice-auditor → critic) with feedback to composer (max 2 cycles). Never feed critic a raw composer draft without voice-auditor between.
6a. **Voice-auditor BLOCKED (separate from critic FAIL cycles):**
   - Returns `[BLOCKED: composer needs concrete proof ...]` → do NOT consume a critic rewrite cycle.
   - Re-dispatch composer with the block reason as feedback.
   - If the block names a proof gap, re-dispatch proof-selector in parallel with "need stronger proof" so composer has a better pool.
   - Same BLOCKED reason repeats on second pass → escalate as `NEEDS_CONTEXT` (name what's missing — usually a concrete client + number).
7. TERMINAL: invoke `humanize` with `content-type: "short-outbound"` + channel
8. POST-HUMANIZE REGRESSION: re-run critic's Specificity dim only. Drops ≥2 OR any named entity/number absent post-humanize → revert to critic-approved draft.
9. Write artifacts to `.agents/mkt/cold-outreach/[slug].md` (+ .rationale.md + .critic-score.md)
10. Deliver message + rationale inline; show scorecard only if user asks or any dim scored 6-7
```

### Route B: Reply Handling

**When:** User pastes an inbound reply and asks for a response.

```
1. Pre-dispatch: read reply text; confirm channel + mode
2. LAYER 1 — reply-classifier (types reply, extracts subtext)
3. LAYER 2 — SEQUENTIAL:
   - reply-composer (drafts per classification + next-touch logic)
   - voice-auditor (peer-voice pass)
   - critic (reply-specific rubric — see Reply Route Agent Flow below)
4. Critic FAIL → re-dispatch FULL Layer 2 (reply-composer → voice-auditor → critic) with feedback (max 2 cycles)
5. TERMINAL: `humanize` with `content-type: "short-outbound"`
6. POST-HUMANIZE REGRESSION (same as Route A step 8)
7. Write artifacts; deliver inline
```

### Route C: Called by Another Skill

**When:** Invoked by `campaign-plan` for outbound touches in a broader campaign.

```
1. Pre-dispatch: read campaign context from calling skill's artifact
2. Execute Route A per touch requested
3. Return annotated message + rationale to calling skill
```

---

## Pre-Dispatch

Run the Pre-Dispatch protocol (`meta-skills/references/pre-dispatch-protocol.md`). cold-outreach has the most elaborate Pre-Dispatch in the stack (5 questions + missing-input protocol with hard blocks for un-faithfulness).

**Needed dimensions:** mode (services-sell / saas-sell / partnership-sell / community-sell), channel (email / LinkedIn / Twitter DM / other), target (name + role + company), trigger (specific signal + strength 1-5), desired outcome (reply / call / resource open / connection accept), bridge (problem we solve that connects to trigger), proof (case studies + logos + metrics + testimonials).

**Read order:**
1. Pipeline: `research/product-context.md`, `research/icp-research.md`, `.agents/mkt/campaign-plan.md`. Read if present, do not block on missing.
2. Experience: `.agents/experience/{audience,product,business}.md`.

If `icp-research.md` / `product-context.md` >30 days old, warn and recommend re-running `icp-research` (soft gate — proceed with "stale ICP" header note).

**Warm Start** (target supplied + ICP exists + product proof in context):

```
Found:
- ICP context → "[primary persona from icp-research.md]"
- product proof → "[from product-context.md or experience/product.md]"

Need before dispatching: target (name + role + company), trigger
(specific signal + strength), and channel?
```

**Cold Start** (no upstream context, fresh outreach):

```
cold-outreach writes touch-based outbound that earns a reply, not a delete.
The composer needs precise inputs — generic prompts produce generic outreach.

1. **Mode** — services-sell / saas-sell / partnership-sell / community-sell?
2. **Channel** — email / LinkedIn (DM or InMail) / Twitter DM / other?
3. **Target** — name, role, company, seniority. What do they care about most?
4. **Trigger** — specific signal + strength (1-5 scale where 5 = individual
   post/quote/news, 1 = generic "companies like yours"). Why them, why now?
5. **Desired outcome** — single, specific: reply with interest / short call /
   open a resource / accept a connection?
6. **Bridge** — the problem we solve that connects to their trigger + situation.
7. **Proof** — list ALL candidates: case studies, named logos + metrics,
   specific claims, testimonials, credentials. Composer's proof-selector picks
   one primary + one backup. (No proof = uncheckable claims = critic fail.)

Answer 1-7 in one response. I'll dispatch.
```

### Missing-Input Hard Blocks

These dimensions cannot be substituted via fallback — composer fails without them:

- **Mode missing** → ask explicitly
- **Channel missing** → ask explicitly
- **Target missing + no ICP artifact** → ask for name/role/company; **BLOCK** if both blank
- **Signal missing** → proceed with weak-signal flag (strategist defaults to pain-first instead of trigger-first; critic weights Signal Connection more strictly)
- **Proof missing + no product-context** → ask for one concrete result; **BLOCK** if user insists "no proof" (uncheckable claims fail Specificity rubric)
- **Follow-up touch (touch 2+ or slug ends -t2/-t3) with no prior_touches** → ask for verbatim prior text; **BLOCK** if missing (composer needs them to avoid repetition)

**Write-back:**

| Q | File | Key |
|---|---|---|
| 7. Proof points | `product.md` | `Product — proof points` (durable across cold-outreach + copywriting + lp-brief runs) |
| 1, 2, 3, 4, 5, 6. Mode + channel + per-target dimensions | (run-specific, lives in the rationale.md artifact) |

If `research/icp-research.md` exists, pull VoC pain language. If `research/product-context.md` exists, pull voice adjectives + accuracy constraints. If prior touches exist, include verbatim so strategist avoids repetition and composer maintains tone.

---

## Dispatch Protocol

### How to spawn a sub-agent

Use the **Agent tool** (general-purpose or Explore) with a prompt built as:

1. **Read** the agent instruction file (e.g., `agents/strategist.md`) — include FULL content in the Agent prompt
2. **Append** pre-writing context + any prior layer's output
3. **Resolve paths to absolute** — rooted at this skill's directory. Example: `references/channels/email.md` → `<skill-root>/references/channels/email.md` (`<skill-root>` = install path, typically `marketing-skills/skills/cold-outreach/`). Tell the agent which references to read.
4. **Pass upstream artifacts by content, not path** — orchestrator reads `research/*.md` and `.agents/mkt/*.md` FIRST, includes excerpts (VoC quotes, voice adjectives, pain language) in pre-writing. Sub-agents do NOT read artifact files directly.
5. If **feedback** exists (critic FAIL), append at end with header "## Critic Feedback — Address Every Point"

### Single-agent fallback

If multi-agent dispatch unavailable, run each agent's instructions sequentially in-context:
- Layer 1: signal-analyst, strategist, proof-selector one at a time (independent)
- Layer 2: composer → voice-auditor → critic in order
- Terminal humanize: apply humanize instructions in-context if skill unreachable

Quality is equivalent — multi-agent optimizes parallelism and focus, not capability.

---

## Layer 1: Two-Stage Strategy Dispatch (Compose Route)

Signal-analyst runs SOLO first — strategist's framework selection and proof-selector's tie-breaking both consume its `signal_strength`. Parallel would force guessing.

### Layer 1a — Signal-analyst solo

| Agent | Instruction File | Pass These Inputs | Reference Files to Resolve |
|-------|-----------------|-------------------|---------------------------|
| Signal Analyst | `agents/signal-analyst.md` | pre-writing (esp. Q2 trigger) | `references/frameworks/personalization-signals.md` |

Wait for output. Extract `signal_strength` (1-5) before proceeding.

### Layer 1b — Strategist + Proof-Selector IN PARALLEL

Spawn both in a single message (multiple Agent tool calls).

| Agent | Instruction File | Pass These Inputs | Reference Files to Resolve |
|-------|-----------------|-------------------|---------------------------|
| Strategist | `agents/strategist.md` | pre-writing (all) + channel + mode + `signal_strength` from 1a | `references/frameworks/structures.md`, `references/frameworks/ctas.md`, `references/modes/{mode}.md` |
| Proof Selector | `agents/proof-selector.md` | pre-writing (esp. Q5 `available_proof[]`) + `signal_strength` from 1a | `references/proof-types.md` |

**For Reply Route:** Spawn only `reply-classifier` in Layer 1 (no 1a/1b split needed).

---

## Merge Step (Compose Route)

After all Layer 1 agents return, assemble a **strategy brief** for the composer:

```markdown
# Strategy Brief

## Target
[From pre-writing Q1]

## Signal (from signal-analyst)
- Strength: [1-5]
- Observation line (draft): [text]
- Notes: [weak/strong/specific/generic flags]

## Framework (from strategist)
- Structure: [e.g., Observation → Problem → Proof → Ask]
- Angle: [one sentence]
- CTA shape: [e.g., low-friction interest question, resource offer, 15-min intro]
- Subject line angle (email only): [direction, not final text]

## Proof (from proof-selector)
- Primary: [named case study / logo + metric / specific claim]
- Backup: [fallback if primary doesn't fit length]

## Channel Rules
[Resolved from references/channels/{channel}.md — length targets, structure constraints]

## Mode Defaults
[Resolved from references/modes/{mode}.md — CTA vocabulary, proof shape, offer framing]

## Prior Touches (if any)
[Verbatim prior messages — composer must avoid repeating angles/phrasing]
```

Merge is deterministic — no creative synthesis. If any Layer 1 agent returned BLOCKED, halt and surface to user.

---

## Layer 2: Sequential Refinement (Compose Route)

Agents run in order. Each receives the prior agent's output.

| Order | Agent | Instruction File | Input | Reference Files |
|-------|-------|-----------------|-------|-----------------|
| 1 | Composer | `agents/composer.md` | Strategy brief | `references/channels/{channel}.md`, `references/modes/{mode}.md` |
| 2 | Voice Auditor | `agents/voice-auditor.md` | Composer draft | `references/anti-patterns.md` |
| 3 | Critic | `agents/critic.md` | Voice-audited draft + `pre_writing` verbatim (ground truth for signal-fabrication check) | `references/anti-patterns.md` (banned-phrase source for auto-fail conditions) |

### Critic Gate

Critic returns:
- **PASS** — scorecard → proceed to terminal humanize
- **FAIL** — scorecard + rewrite feedback → re-dispatch composer (cycle 1 or 2)

After 2 failed cycles, surface: "Critic couldn't reach threshold — here's the best draft + scorecard + what's blocking. Your call."

---

## Terminal Pass: Humanize

After critic PASS, invoke `humanize` on the final draft:

1. Spawn agent with humanize's `SKILL.md` content
2. Pass:
   - Final message text
   - `content-type: "short-outbound"` (humanize's Content Type Calibration row: Light strip, Full voice, 0-10% compression — short outbound differs from marketing copy because further compression kills specificity)
   - Channel
   - `protected_tokens`: every named entity + number in the critic-approved draft (humanize must not remove or paraphrase)
3. Receive humanized output
4. **Regression check (automatic, not judgment):** re-run critic's **Specificity dimension only**. Revert to critic-approved draft if any of:
   - Specificity drops ≥ 2 points
   - Any named entity pre-humanize absent post-humanize
   - Any concrete number pre-humanize absent post-humanize
5. Otherwise ship humanized version.

Terminal pass is **automatic**, not opt-in. AI-sounding cold email is the biggest failure mode. Regression check protects against humanize silently stripping the specificity anchor.

---

## Reply Route Agent Flow

```
1. reply-classifier classifies inbound: not-interested / no-budget / send-info / wrong-person / curious / qualified / later / hostile / ambiguous
2. reply-composer drafts per classification + next-touch logic (uses references/frameworks/objections.md)
3. voice-auditor (same as compose route)
4. critic (reply-specific rubric — 5 dimensions, same total-≥35 AND per-dim-≥6 gate)
5. Terminal humanize + specificity regression check (same as Route A)
```

Reply-specific rubric (5 dims, two substitutions):
- "Signal connection" → **Tone match** — does the reply match their register (defensive → calm, curious → substantive, qualified → concrete)?
- "CTA friction" → **Next step clarity** — is the next action obvious without being pushy?
- Peer voice, You > me ratio, Specificity unchanged.
- **Hard gate (not scored):** never argue with a "no". Breakup mode is default for firm not-interesteds. Critic auto-fails any reply that re-pitches after clear rejection, regardless of dim scores.

---

## Anti-Patterns (Orchestrator-Level)

| Anti-pattern | Why it fails | Guardrail |
|--------------|--------------|-----------|
| Template-with-{{FirstName}} swap | Signal never connects; reader pattern-matches to spam | Signal analyst flags; critic "Signal Connection" dimension |
| "I hope this email finds you well" / "My name is X and I work at Y" | Zero-value opener; vendor telltale | voice-auditor auto-flags |
| "Quick 30-minute call?" in touch 1 | Ask is too expensive for zero trust | CTA Friction rubric; strategist defaults to interest-question CTAs |
| Feature dumps | One proof beats ten features; reads as desperation | proof-selector picks ONE; voice-auditor cuts lists |
| Fake Re:/Fwd: subject lines | Short-term open rate bump, long-term trust destruction, reply rate collapse | Banned in `references/channels/email.md`; voice-auditor auto-fails |
| Running humanize twice | Strips specificity, drifts toward generic | Terminal pass runs ONCE |
| Arguing with "no" in reply route | Burns goodwill, tanks domain reputation | reply-composer hard gate; critic auto-fails |
| Skipping ICP artifact when present | Re-asks user for what's already known | Step 0 enforces artifact check first |
| Multi-touch without prior-touches input | Touch 2 repeats touch 1's angle | Orchestrator prompts for prior touches when slug ends `-t2`, `-t3`, etc. |

---

## What This Skill Pulls From Elsewhere

- **coreyhaines/cold-email** (Claude skill by Corey Haines, ex-Baremetrics growth): structural frameworks (O→P→P→A), 4-level personalization, subject-line discipline, breakup protocol. → `references/frameworks/structures.md`, `references/frameworks/personalization-signals.md`, `references/channels/email.md`.
- **kostja94/cold-start-strategy** (Claude skill): "demand-signal outreach" — read posts/comments for expressed need rather than guessing pain. → `references/channels/twitter.md`, `references/channels/platform-proposals.md`.
- **Nick Saraev — Make More Money** (YouTube, AI Automation Agency playbook, 2023-2024): services-mode defaults — audit/loom-teardown CTAs, revenue-tied problems, value-based positioning, Upwork as legit top-of-funnel. → `references/modes/services.md`, `references/channels/platform-proposals.md`. Specific artifacts: "Loom Teardown" template, "$10k/month Upwork Playbook" series.

## Completion Status

Every run ends with explicit status:
- **DONE** — passed critic + humanize, ready-to-send
- **DONE_WITH_CONCERNS** — delivered, flags noted (stale ICP, weak signal, rubric 35-39)
- **BLOCKED** — missing target + ICP, or missing proof + product-context; state what's needed
- **NEEDS_CONTEXT** — recommend `icp-research` or provide prior touches

## Next Step

After receiving the message: send, wait for reply or cadence (7-14 days typical), re-invoke with prior touches for next touch. For reply, use Route B.

---

## References

- `references/channels/` — craft rules per channel
- `references/modes/` — defaults per business mode
- `references/frameworks/` — structures, signals, CTAs, objections
- `references/anti-patterns.md` — AI tells and template smell
- `references/proof-types.md` — proof hierarchy
