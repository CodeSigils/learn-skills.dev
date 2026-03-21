---
name: dialectic
description: "Hegelian dialectic reasoning — Electric Monk subagents for structured contradiction analysis and synthesis. Use when the user wants to stress-test an idea, resolve a genuine tension, build a deeper mental model, or make a high-stakes decision where the tradeoffs are unclear. Works across any domain — technical architecture, product strategy, philosophy, personal decisions, risk analysis, policy, creative direction."
---
<!-- compact: SKILL-compact.md -->

# The Electric Monks — Dialectic Skill

An **artificial belief system** for building deeper understanding through productive contradiction.

Two subagent sessions — the Electric Monks — *believe* fully committed positions so you don't have to. The orchestrator performs structural analysis of their contradiction and generates a synthesis (Aufhebung) that transforms the question itself. The user orchestrates from a belief-free position, freed from the cognitive load of holding either position.

**Why this works:** The bottleneck in human reasoning isn't intelligence — it's *belief.* Once you believe a position, you can't simultaneously hold its negation at full strength. The Electric Monks carry the belief load at full conviction, freeing you for structural analysis. (See `references/theory.md` → Rao for the full framework.)

## When to Use This Skill

Use when:
- The user wants to **stress-test** an idea against the strongest possible counter-argument
- The user is **torn between two positions** and the tension feels genuine, not just a preference
- A **decision has real stakes** and the tradeoffs are unclear
- The user wants to **build a deeper mental model** of a domain, not just pick an answer
- Requirements genuinely conflict and can't be resolved by simple tradeoff analysis

Do NOT use when:
- The question is purely empirical (just look up the answer)
- One side is obviously correct and doesn't need dialectical treatment
- The user wants a quick recommendation, not deep analysis

<core_concepts>
## Core Concepts

Three frameworks drive every phase. Internalize them before proceeding.

**Rao: This is an Artificial Belief System, not AI.** The monks aren't thinking for the user — they're *believing* for the user. A hedging monk has failed its one job: if it doesn't fully believe, the user picks up the dropped belief weight and their cognitive agility collapses. Anti-hedging is a functional requirement, not a stylistic preference.

**Hegel: How contradictions resolve.** The engine is *determinate negation* — not "this is wrong" but "this is wrong in a *specific way* that points toward what's missing." Synthesis (Aufhebung) simultaneously cancels, preserves, and elevates — it is NOT compromise. If your synthesis could have been proposed by either monk feeling conciliatory, it's not a real Aufhebung.

**Boyd: How creativity works.** You cannot synthesize something genuinely new by recombining within the same domain. You must first *shatter* existing wholes into atomic parts (destruction), then find cross-domain connections to build something new (creation). This is why recursive rounds often need new research from *outside* the original domains.

See `references/theory.md` for the complete theoretical foundations.
</core_concepts>

<overview>
## How It Works: Overview

You are the **orchestrator**. You conduct the elenctic interview, generate the monk prompts, spawn the Electric Monks as subagents, perform the structural analysis, and produce the synthesis.

```
You (Orchestrator)
├── Phase 1: Elenctic Interview + Research (you, with the user)
│   ├── 1a: Explain the process — set expectations, emphasize user as co-pilot
│   ├── 1b: Understand what the user wants (stress-test vs opposition)
│   ├── 1c: Elenctic probing — surface hidden assumptions
│   ├── 1c′: Identify the user's belief burden and calibrate monk roles
│   ├── 1d: Ground the monks (research or deep interview, domain-dependent)
│   ├── 1e: Write context briefing document to file
│   └── 1f: Confirm framing with user — ask about gaps
├── Phase 2: Generate Electric Monk prompts (reference briefing file)
├── Phase 3: Spawn the Electric Monks (parallel subagents, BELIEVE fully)
│   ├── Decorrelation check: did monks genuinely diverge in framework?
│   └── User checkpoint: gaps in coverage?
├── Phase 4: Determinate Negation (structural analysis, saved to file)
│   ├── 4.0: Internal tensions — where does each position undermine itself?
│   └── 4.5: Boydian decomposition — shatter, find cross-domain connections
├── Phase 5: Sublation / Aufhebung (synthesis, saved to file)
│   └── Abduction test: does synthesis make the contradiction *predictable*?
├── Phase 6: Validation
│   ├── Monks A & B evaluate — elevated or defeated?
│   ├── Hostile Auditor: fresh agent attacks (uses references/auditor-prompt.md)
│   └── Refine: present improvements individually to user
└── Phase 7: Recursion — propose 2-4 directions, user chooses
    ├── Queue unexplored contradictions
    └── Repeat from Phase 2 (or 1 if new research needed)
```

The user can intervene at any point. The user never has to *believe* anything — that's the monks' job.
</overview>

<phase1>
## Phase 1: Elenctic Interview + Research

This is the most important phase. Everything downstream depends on it.

### 1a. Explain the Process to the User

**Before anything else, tell the user what's about to happen and why.** Deliver something like:

> Here's how this works. We're going to use a structured process to dig into this topic.
>
> **Step 1: Interview.** I'll ask you questions to understand what you're really wrestling with underneath the surface framing.
>
> **Step 2: Research.** I'll do research on the topic so I'm genuinely knowledgeable about the landscape.
>
> **Step 3: Two "Electric Monks."** I'll create two AI agents, each of which will *fully believe* one side of the tension. They won't hedge — they'll each make the absolute strongest case for their position.
>
> **Step 4: Structural analysis and synthesis.** I'll analyze *how* each position fails, find the deeper question underneath, and build a synthesis that transforms the question itself.
>
> **Step 5: We keep going.** Each synthesis generates new tensions. We'll do multiple rounds. The first round is calibration — real breakthroughs usually come in rounds 2 and 3.
>
> **The most important thing: YOU are the source of the best insights here.** Interrupt me constantly. Correct wrong assumptions. The value comes from the collision between structured analysis and your actual knowledge.

Adapt the language to the user — this is a template, not a script.

### 1b. Understand What the User Wants

Determine:
- **Mode A (Stress-Test):** User has one idea they want to challenge. Identify the strongest antithesis.
- **Mode B (Opposition):** User has two positions in tension. Refine both to steelman forms.

### 1c. Elenctic Probing

Interview using Socratic technique. Surface:
- Hidden assumptions they haven't articulated
- The *deepest* version of the contradiction
- What domain type this is (empirical, normative, personal, creative)
- What specific parameters of their mental model they want updated

Key questions:
- "What's your strongest intuition here? Where does it break down?"
- "What would change your mind?"
- "What are you actually optimizing for?"
- "What's the version of the opposing view that worries you most?"
- "Is this a decision you need to make, or understanding you want to build?"

### 1c′. Identify the User's Belief Burden

During the interview, pay attention to what the user is stuck believing. Read `references/belief-burdens.md` for the full catalog of common belief burdens and how they map to monk roles.

Don't announce your typing to the user. Just use the pattern to calibrate:
1. Which belief load is heaviest? That determines what monks must hold.
2. What must Monk A validate? (Always validate the dominant function first.)
3. What must Monk B present that the user can't natively hold?

### 1d. Ground the Monks (Domain-Adaptive)

**Research depth is the main knob.** Calibrate based on how much you already know:

- **Novel/obscure domain:** Full parallel research — 2-3 subagents, 150-250K tokens. Spawn research agents via the Agent tool with `run_in_background: true`.
- **Well-known domain:** Skip or minimize research. Write the briefing from your own knowledge with 2-3 targeted searches.
- **Known domain, novel angle:** Light research — a few targeted searches on the specific angle.

**Don't default to full research out of caution.** Unnecessary research wastes the user's time, which is the scarcest resource.

#### External-Research Domains

Run 2-3 parallel research subagents:
1. **Side A's strongest literature**
2. **Side B's strongest literature**
3. **Broader landscape/context** (give this agent specific targeting to avoid scope creep)

Research agents should be given *specific* search targets — not "research this topic" but "search for X's argument about Y, specifically the part about Z."

#### Personal and Values Domains

The grounding comes from *the user themselves.* The interview IS the research. Map:
- The full landscape of commitments
- History and patterns of past decisions
- Stakeholders and their actual capacities
- Values hierarchy
- Constraints (which are real, which are assumed)

**Spend 6-10 exchanges on this.** For personal domains, the interview should be roughly twice as long.

#### In All Cases

You need to know the domain well enough to:
- Identify likely **degenerate framings** (the obvious/boring version of the dialectic)
- Generate **specific research directives** for each subagent
- Write **framing corrections** that steer monks away from shallow takes
- Identify the **deepest available contradiction**

### 1e. Write the Context Briefing Document

**First, resolve the output directory to an absolute path.** Slugify the topic: lowercase, spaces to hyphens, max 40 characters. Recommended: prefix with `YYYY-MM-DD-`. Create the directory and store the absolute path — use it in all subsequent file references and subagent prompts.

**Synthesize everything into a single neutral briefing document and save it** to `[OUTPUT_DIR]/context_briefing.md`.

For external-research domains: key evidence, sources, arguments, landscape, empirical data, specific framing.
For personal/values domains: commitment landscape, history, stakeholders, values hierarchy, constraints.
For mixed domains: both sections.

Both monks will read this file before writing.

### 1f. Confirm with the User — USER CHECKPOINT

Before proceeding, summarize back:
- "Here's how I understand the two positions..."
- "Here's what I think the real tension is..."
- "Here's what I'll have each agent research and argue..."
- **"Are there companies, thinkers, comparison classes, or evidence we're missing?"** — This question consistently produces the highest-leverage interventions.

Get confirmation or correction. If the user identifies gaps, run supplementary research and update the briefing.
</phase1>

<phase2>
## Phase 2: Generate the Electric Monk Prompts

Generate two prompts — one for each Electric Monk. Each monk must *believe* its position at full conviction. This is the functional core of the artificial belief system.

**Read `references/monk-prompt-template.md` for the full 7-section prompt template.** Calibrate based on Phase 1c′: what must each monk believe, what must Monk A validate, what must Monk B hold that the user can't natively hold.

Key principles (always apply, even without re-reading the template):
- Anti-hedging is non-negotiable — a hedging monk forces the user back into belief-space
- Framing corrections preempt degenerate versions of the dialectic
- Research directives must be *targeted*, not broad
- 1500-2000 words Round 1, 1000-1500 words recursive rounds
</phase2>

<phase3>
## Phase 3: Spawn the Electric Monks

Spawn Monk A and Monk B as separate subagent sessions using the Agent tool. Each gets a clean context with full belief commitment.

**Spawn both monks in parallel** using two Agent tool calls in a single message:

```
Agent tool call 1:
  description: "Electric Monk A — [position]"
  subagent_type: "general-purpose"
  prompt: [MONK A PROMPT from Phase 2]
  run_in_background: true

Agent tool call 2:
  description: "Electric Monk B — [position]"
  subagent_type: "general-purpose"
  prompt: [MONK B PROMPT from Phase 2]
  run_in_background: true
```

**After both complete:** Write the returned text to files:
- `dialectics/[topic-name]/monk_a_output.md`
- `dialectics/[topic-name]/monk_b_output.md`

**Decorrelation check:** Verify the monks actually diverged. Check:
- Do the monks cite *different* evidence, or substantially overlapping sources?
- Do they frame the problem using *different* conceptual vocabularies?
- Do their unstated assumptions *diverge*?
- Would a reader recognize these as genuinely *different perspectives*?

If decorrelation is low, consider reformulating the belief burdens to force genuinely different conceptual frames.

**If a monk hedges or is off-base:** Prefer restarting with a revised prompt over nudging. Fresh context with better instructions produces better results.

### Present to User — USER CHECKPOINT

Present both outputs with a brief re-explanation:

> Here are two essays — each one fully committed to one side of the tension. They're called "Electric Monks" because their job is to *believe* these positions so you don't have to.
>
> **A few important things:**
> - **These will get things wrong.** That's expected — especially in the first round.
> - **Correct them freely.** "That's not how it works" or "they're missing that..." are the most valuable input.
> - **The first round is the least insightful.** Each subsequent round gets sharper.

Then ask:
1. Do these capture the positions accurately?
2. **"Is there a claim either monk makes that should be tested against evidence neither has considered?"**

If the user identifies a testable claim, run a targeted research agent to check it.
</phase3>

<phase4>
## Phase 4: Determinate Negation

This is the structural analysis phase. You (the orchestrator) perform this yourself — do NOT delegate to a subagent. You need continuity with the elenctic interview and research.

Read both monks' outputs from their files and analyze the contradiction using this structure. Write your analysis to `dialectics/[topic-name]/determinate_negation.md` as you go.

**Important: treat monk output as testimony, not evidence.** Monks pushed to full conviction will sometimes overstate mechanisms. Work with the *structure* of their arguments, not their rhetoric.

**Before you begin: write down your current best guess at the synthesis in one sentence.** Set it aside. Compare at the end of Phase 5. If they're substantially similar, you may be pattern-matching rather than genuinely synthesizing.

### 4.0 Internal Tensions (Self-Sublation)

Before comparing the monks to each other, analyze each essay *in isolation.* Where does each position's own logic undermine its own premises? These internal fractures point toward what each position is *trying to become* — which is often where the synthesis lives.

### 4.1 Surface Contradiction

State the apparent disagreement in its simplest form.

### 4.2 Shared Assumptions

Identify what BOTH agents implicitly agree on that they don't realize they agree on. Probe:
- Do both assume the same unit of analysis?
- Do both assume the same problem is central?
- Do both assume a particular model of how their domain works?
- What frame constrains both of their visions?

### 4.3 Determinate Negation

For each agent, identify the SPECIFIC way it fails:
- "Monk A fails because [SPECIFIC FAILURE], which reveals [SPECIFIC MISSING THING]"
- "Monk B fails because [SPECIFIC FAILURE], which reveals [SPECIFIC MISSING THING]"
- The failures are COMPLEMENTARY — each agent's blind spot is something the other partially sees.

This is NOT:
- "Monk A is wrong" (abstract negation — useless)
- "Both have merits" (compromise — useless)

### 4.4 The Hidden Question

Articulate the deeper question the contradiction is ACTUALLY about — the question neither agent asked because they were too committed to their answers.

### 4.5 Boydian Decomposition (Destruction Phase)

**Before attempting synthesis, shatter both positions into atomic parts.**

1. **Identify the generic space** — the abstract relational structure both positions share.
2. **List the atomic components** — individual claims, mechanisms, evidence, assumptions, metaphors, principles — stripped of which agent said them.
3. **Look for surprising connections** between parts from different positions. What mechanisms from A illuminate evidence from B?
4. **Ask: what material from adjacent domains** might connect to these liberated parts?

**Emergent structure test:** The synthesis must have organizational properties in *neither* input. If every element is attributable to one monk, you've recombined, not created.

### 4.6 Sublation Criteria

Before attempting synthesis, specify what it must accomplish:
- It must preserve [specific insight from A]
- It must preserve [specific insight from B]
- It must dissolve [the shared assumption both are trapped in]
- It must answer [the hidden question]

**Separating criteria from synthesis prevents pattern-matching to a pre-formed compromise.**
</phase4>

<phase5>
## Phase 5: Sublation (Aufhebung)

Generate the synthesis. Do additional research if needed. Write to `dialectics/[topic-name]/sublation.md`.

The synthesis must:

1. **CANCEL** both original positions as complete truths
2. **PRESERVE** the genuine insight in each position
3. **ELEVATE** to a new concept that TRANSFORMS THE QUESTION ITSELF

### What Sublation is NOT

- "Use A for some cases and B for others" — division of labor
- "Build something that combines the best of A and B" — compromise
- "It depends on the context" — surrender
- Policy recommendations — not reconceptualization
- "Both sides have valid points" — absence of thinking

### What Sublation IS

- A reconceptualization of what the thing IS — potentially changing the unit of analysis
- Concrete enough to act on or sketch architecturally
- Something neither Monk could have proposed from within their frame
- Something that, once stated, makes it hard to go back to the old terms
- **Has the closure property:** can serve as input to the next dialectical round

### Abduction Test

The synthesis is an abductive hypothesis. Does it make the original contradiction *a matter of course*? If someone heard your synthesis first, would they predict both monks' positions?

**Assess your abduction type:**
- **(a) Selective:** Choosing from existing frameworks. Weakest.
- **(b) Conditional-creative:** New relationship between known concepts. Moderate.
- **(c) Propositional-conditional-creative:** Genuinely new concept. Strongest.

Aim for (c) but accept (b). If you're at (a), push harder.

### Draft Validation Predictions

Draft what you *expect* each monk to say:
- Monk A should say: "Yes, this preserves my core insight about [X], but I now see I was wrong about [Y]"
- Monk B should say: same pattern

**If you can't draft convincing versions, your sublation isn't good enough.** Revise before Phase 6.

### New Contradictions

Identify what NEW contradictions this sublation generates. A genuine sublation is fertile, not final.

### Frame as Model Update

End with: "Before this dialectic, the assumption was X. The contradiction revealed Y. The updated model is Z, because..."

### Present to User — USER CHECKPOINT

> Here's my synthesis. Does this ring true? Does it miss something? Is there a part that feels like hand-waving or compromise rather than genuine insight? Push back on anything that doesn't land.

Revise before proceeding to Phase 6.
</phase5>

<phase6>
## Phase 6: Validation by the Electric Monks

The synthesis must be validated by the original monks. This is how Hegelian dialectics works: each position must recognize itself as preserved-but-elevated.

**Read `references/validation-prompts.md` for the full validation prompt templates and auditor orchestration.** Also read `references/auditor-prompt.md` for the hostile auditor prompt (required — Phase 6 cannot complete without it).

Key principles (always apply):
- Spawn both monk validation agents **in parallel** with `run_in_background: true`
- Use fresh agents with argument summaries — persona persistence is unreliable
- A properly elevated monk *believes more*, not less — it sees its original position as partial truth within a larger truth
- Give the hostile auditor ONLY monks' essays + synthesis — no Phase 4 analysis
- Auditor always in Round 2+, optional in Round 1

### Interpreting Results

- **Both monks elevated:** Sublation is valid. Proceed.
- **One defeated:** Synthesis is biased. Revise Phase 5 to better preserve the defeated monk's insight.
- **Both defeated:** Synthesis killed beliefs without replacing them. Return to Phase 4.
- **Auditor proposes harder contradiction:** Often becomes the best recursion direction.
- **Auditor finds shared assumptions:** Frequently the most valuable recursion targets.
- **Auditor flags compromise-as-transcendence:** Return to Phase 5.

### Refine the Synthesis

After collecting feedback, **present improvements one at a time to the user:**

1. Summarize feedback briefly (2-3 sentences)
2. Present ONE improvement. Wait for response. Then next.
3. Revise synthesis with accepted improvements
4. Present recursion directions from remaining feedback
</phase6>

<phase7>
## Phase 7: Recursion — Where the Real Value Lives

**Recursion is not optional cleanup. It is the engine of the skill.** The first round produces a synthesis. Recursive rounds force that synthesis to confront its own limitations.

**When transitioning to recursion:**

> That was Round 1. **That round was the least insightful we'll get.** It was calibration. Each subsequent round gets sharper. The process is like focusing a lens. Ready for Round 2?

**Default: recurse at least once.** Only stop if:
- Synthesis generated no significant new contradictions (rare)
- User explicitly wants to stop
- New contradictions are outside scope

### Proposing Recursive Directions

Generate a **burst of 5-8 candidate concepts/directions** — contradictions, mechanisms, novel framings, vulnerabilities. Then cluster into **2-4 coherent directions:**

> The synthesis generated three fertile contradictions:
> 1. **The formation problem:** The synthesis says X — but who does Y? (internal tension)
> 2. **The authority problem:** The synthesis argues from Z, but decisions are made by W (vs. domain reality)
> 3. **The scalability problem:** This works small — does it survive contact with scale? (vs. feasibility)
>
> Which would you like to pursue? (Or we can queue multiple.)

**Write the queue to `dialectics/[topic-name]/dialectic_queue.md`** — a running list of contradictions with source round and status (explored, queued, deferred).

### Running Recursive Rounds

- **New research is often essential.** Each synthesis opens conceptual space the original research didn't cover.
- **Fresh agents are usually better** than resumed sessions for recursion — the contradiction has shifted.
- **Re-read the relevant phase sections** before executing (use the XML tags for selective extraction). At minimum re-read `<core_concepts>`, `<phase2>`, `<phase4>`, `<phase5>`, and `<phase6>` each round.
- **Pass all prior context** to new agents as background.
- Use **1000-1500 word essays** for recursive rounds.
- Validation can be abbreviated in recursive rounds.

### When to Stop

Stop when:
- Queued contradictions show diminishing returns
- Latest synthesis requires fundamentally different expertise
- The user has what they need

**Err on the side of one more round.** The marginal insight is often the most powerful.

When stopping, present the **final dialectic queue** — explored, open, and deferred contradictions.
</phase7>

## Domain Adaptation & Output Format

**Read `references/domain-adaptation.md`** for the full domain type table, domain-specific failure modes, and output format specification.

Quick reference — grounding mode by domain:
- **Empirical/Risk:** external research
- **Personal:** deep interview (the interview IS the research)
- **Normative/Creative:** mixed

The final deliverable includes: dialectical trace, model update ("Before/After/Because"), actionable output (domain-dependent), and the dialectic queue. All files in `dialectics/[topic-name]/`.
