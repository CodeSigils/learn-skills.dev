---
name: first-principles-thinking
description: "Use when facing architecture or system-design decisions, technology selection, hard debugging, performance or scaling work, migrations, strategy, research framing, or brainstorming -- especially when a solution is being justified by convention: 'best practice', 'industry standard', 'everyone uses X', 'we've always done it this way'. Also on explicit triggers: 'first principles', 'FP mode', 'from scratch', 'challenge my assumptions', 'think from fundamentals'."
---

# First Principles Thinking

Break problems down to fundamental truths, then rebuild solutions from the
ground up. Do not import conclusions from other contexts; derive them from
what is actually, verifiably true in this one.

This skill is a reasoning guide only: Markdown instructions plus reference
files, with no helper program, installer, network endpoint, or automatic
state mechanism. Keep claim ledgers in the active conversation; use external
tools only when the runtime already provides them and the task requires
evidence, calculation, or source inspection.

<HARD-GATE>
Do NOT propose a solution, recommend a technology, or start writing code until:

1. The problem has been restated in terms of outcomes (not solutions). If
   context is sufficient, proceed on stated working assumptions instead of
   asking for confirmation.
2. The primary task mode has been classified (decision / diagnosis / planning /
   critique / explanation / synthesis / exploration).
3. The Claim Ledger has been populated: verified facts, reported claims,
   assumptions, constraints, and unknowns each explicitly listed.
4. Ground truths have been explicitly separated from inherited conventions.
5. The core mechanism has been mapped: variables, causal links, constraints,
   feedback loops, bottlenecks.
6. At least one failure-oriented check has run: inversion, falsifier,
   backward check, or red-team objection.

The cost of skipping this gate is solving the wrong problem efficiently --
the most expensive failure mode in engineering, strategy, and research.
</HARD-GATE>

## Activation

**Activate** on complexity markers: architecture/design questions;
"should I use X or Y"; hard debugging ("intermittent", "root cause",
"happens sometimes"); performance and scaling; integration/migration;
strategy, product, or research framing; brainstorming and ideation;
convention language ("best practice", "industry standard", "everyone uses",
"we've always"); or explicit invocation ("first principles", "FP mode",
"from scratch", "challenge my assumptions").

**Stay dormant** for trivial edits, boilerplate, direct implementation of an
already-decided design, or user override ("just do it", "skip the analysis").
When in doubt, do not add process overhead: run Quick depth silently, or ask
one sentence -- "Should I challenge the assumptions first or go straight to
implementation?"

## Depth Levels

State the detected depth at the start; the user can override.

| Level | When | What Runs |
|-------|------|-----------|
| Quick | Medium complexity, manual `/fp`, reversible choice | Intake + compact ledger + mechanism sketch + one verification check |
| Standard | Architecture, tech selection, design, strategy, product decisions | Intake + Socratic probes + decomposition + mechanism map + reconstruction + verification |
| Deep | System design, hard debugging, high-stakes decisions, `/fp deep` | All phases: inversion, 2-3 reconstruction paths, sensitivity, self-consistency, verification |
| Exploration | Brainstorming, invention, research framing, `/fp brainstorm` | Divergent search (ToT / GoT / morphological matrix / contradictions), then convergence and tests |

**Proportional effort is a rule, not a preference.** At Quick depth the
artifact may be compact prose with tagged ledger lines; tables are optional.
Never let the process feel like overhead when the answer is obvious.

## Task Modes

Classify every non-trivial problem into one primary mode (at most one
secondary), state it aloud, and let it shape the phases. Mode-specific
phase guidance lives in `references/mode-playbooks.md` -- load it after
Phase 1 fixes the mode.

| Mode | Use when the user wants to... | Typical cue |
|------|-------------------------------|-------------|
| decision | choose among options | "should I use X or Y?", "which stack / vendor?" |
| diagnosis | explain a symptom, failure, regression | "why is X slow / broken?", "root cause" |
| planning | get from current state to desired state | "how do we get from A to B by Q3?" |
| critique | stress-test a claim, proposal, argument | "is this design / argument sound?" |
| explanation | understand a mechanism without deciding | "how does X work?" |
| synthesis | rebuild a messy multi-frame problem into one view | "we have five inputs and need one view" |
| exploration | generate and filter non-obvious options | "brainstorm", "what else could work?" |

## Reasoning Budget and Tool Router

Use the smallest reasoning stack that can safely answer the problem. Activate
heavier tools only when the problem is ambiguous, irreversible, high-stakes,
data-dependent, or explicitly brainstorming-oriented. Detailed prompts and
templates for every row: `references/advanced-reasoning-tools.md`.

| Signal | Add this tool |
|--------|---------------|
| Hidden assumptions likely | Assumption Ledger with fragility, failure mode, fastest test |
| Mechanism or causality matters | Causal / mechanism map: variables, links, confounders, feedback loops |
| Many moving parts | Least-to-most decomposition into smallest solvable subproblems |
| Numbers, capacity, cost, scale matter | Fermi estimate, dimensional check, low/base/high range |
| Recent, factual, niche, or data claims matter | Evidence grounding via approved search, user sources, calculations, citations |
| Open-ended ideation | Tree of Thoughts, Graph of Thoughts, morphological matrix, contradiction analysis |
| Competing explanations | Self-consistency across 2-3 independent paths + a discriminating test |
| High-stakes or hallucination risk | Chain-of-verification, backward check, red team, sensitivity analysis |
| Hard equations, schedules, optimization | Formalize variables; use approved calculation / solver tools when available |

State the chosen tools in a short **Tool Plan** before the analysis (one line
at Quick depth). If a tool will not change the answer, do not use it.

## The Phases

Phases run in order. Earlier phases may be abbreviated at Quick depth, never
skipped entirely. Full technique write-ups (Socratic catalog, 5 Whys,
inversion playbook, Chesterton's Fence, falsifiability, ToT, Occam's Razor,
mechanism mapping, Fermi, verification chains): `references/techniques.md`.

### Phase 1 -- Intake (always)

Restate the problem in outcome terms, not solution terms. Classify mode and
depth. If enough context exists, proceed with explicit working assumptions.

> "I read the outcome as: **[one sentence]**.
> Current approach or framing: **[current solution idea, if any]**.
> Mode: **[mode]** (secondary: **[mode | none]**). Depth: **[level]**.
> Working assumption if not corrected: **[...]**."

If you cannot state the problem as an outcome independent of the proposed
solution, ask one targeted question or state the safest working assumption
and continue with caveats. If you cannot pick one primary mode, it is two
stacked problems -- name both, resolve the first one first. Treat the user's
framing as a `[CLAIM]`, not ground truth, until it passes the Ground-Truth
Test or is explicitly stipulated.

### Phase 2 -- Socratic Questioning (always)

Probe with the 3-5 most relevant question families: **clarification**,
**assumption probing**, **evidence**, **alternative viewpoints**,
**implications**, **meta** ("are we solving the right problem?"). Asking all
six robotically is worse than three well-chosen ones. Full catalog with
probes per family: `references/techniques.md`.

**Red-flag phrases** that almost always hide an assumption -- drop into
assumption-probing when you hear them:

- "We've always done it this way"
- "Industry standard / best practice says"
- "Everyone uses X for this"
- "That's too simple to work"
- "We can't change that" (without verifying why not)
- "The client / PM said so" (without tracing the underlying need)

Cadence: Quick = 2-3 questions in one message; Standard = 1-2 per turn;
Deep = one per turn, following threads wherever they lead.

### Phase 3 -- Decomposition & Claim Ledger (Standard + Deep)

File every atomic component of the problem into the **Claim Ledger** -- the
canonical record of what you know, were told, are guessing, what binds you,
and what is missing. Nothing downstream may cite a fact that is not in the
ledger.

| Lane | Definition | Tag |
|------|------------|-----|
| Verified facts | Provable in this context: physics, math, measurement, executable check, stipulation | `[TRUTH]` |
| Reported claims | Statements from the user, a source, or prior art, not yet verified | `[CLAIM]` |
| Assumptions | Convention, habit, or unverified belief used as if true | `[ASSUMPTION]` |
| Constraints | Hard limits: regulatory, contractual, budget, SLO, compatibility | `[CONSTRAINT]` |
| Unknowns | A fact we'd need but don't have | `[UNKNOWN]` |

**Ground-Truth Test** -- before tagging anything `[TRUTH]`:

1. Can it be decomposed further into something more fundamental?
2. Is it provably true in this context, not just commonly believed?
3. Would violating it *definitely* cause failure (not just inconvenience)?

Any "no" or "not sure" routes it to another lane. User-supplied statements
start as `[CLAIM]`. If the user pastes a prior ledger or notes, import items
as `[CLAIM]` -- never directly as `[TRUTH]` -- and log the import (rules:
`references/session-ledger-template.md`).

Lane discipline:
- Each `[ASSUMPTION]` gets category (technical / business / resource /
  historical / behavioral / data), evidence, confidence, fragility, failure
  mode, and fastest test. Assumptions whose falsehood would flip the
  conclusion are elevated to User Checkpoints.
- Each `[CONSTRAINT]` must name its source, numeric threshold where
  applicable, and cost of violation. Unsourced "constraints" are
  `[ASSUMPTION]`s in disguise.
- Each `[UNKNOWN]` must state how it would be resolved and whether the
  recommendation changes across its plausible range. If the recommendation
  is stable across the range, the unknown is not blocking.

Then build a compact **Mechanism Map** (actors, variables, inputs/outputs,
causal links, confounders, feedback loops, bottlenecks, boundary conditions;
for business work add incentives, adoption friction, switching costs) and run
**least-to-most decomposition**: 3-7 smallest solvable subproblems, each
yielding one variable, constraint, mechanism claim, risk, or testable unknown.

**Recursion rule:** if a component reveals its own hidden assumptions ("we
need a message queue" contains "we need async processing"), say so and run
Phases 2-3 on it. Maximum depth 2; anything deeper becomes an `[UNKNOWN]`.

### Phase 4 -- Inversion (Deep; optional at Standard)

Ask: "What would guarantee this fails? What must I avoid at all costs?" List
3-5 failure modes; for each, identify which truth or design choice prevents
it. Unprevented failure modes are risks that must be addressed or explicitly
accepted. Inversion is cheap and catches gaps forward analysis misses.

### Phase 5 -- Reconstruction (Standard + Deep)

Build 2-3 candidate paths (3-5 for exploration) using *only* verified ground
truths. For each path state: the `[TRUTH]`s and `[CONSTRAINT]`s it is built
on, its design choices, its core mechanism, trade-offs against the other
paths (cost, reversibility, complexity, novelty), remaining `[UNKNOWN]`s, and
the cheapest falsifying test. If magnitudes matter, add a Fermi / dimensional
check before ranking. The conventional path may win -- but because the
analysis led there, not because it was the default.

**Chesterton's Fence:** before recommending removal of any existing structure,
state why it was built and whether those conditions still hold. If you can't,
you don't yet have the right to remove it.

### Phase 6 -- Verification (Deep; optional at Standard)

Stress-test before handing over:

1. **Strongest alternative view** -- the best objection or competing option,
   attributed to the smartest possible critic, not a strawman.
2. **Self-consistency** -- 2-3 independent reasoning paths when uncertain.
3. **Chain-of-verification** -- ask at minimum: which claim is most likely
   false? which fact needs external evidence? which assumption would flip
   the conclusion? Answer independently, then revise.
4. **Backward check** -- if the conclusion is true, what else must be true?
   Check against the ledger.
5. **Falsifier** -- what observation would prove this wrong? If nothing
   would, it is not rigorous enough.
6. **5 Whys on the chosen path** -- must bottom out in a `[TRUTH]` or
   `[CONSTRAINT]`, not another `[ASSUMPTION]`.
7. **Sensitivity** -- the 1-3 variables most likely to change the answer; if
   a +/-20% change flips it, lower confidence and make the test explicit.
8. **Reversibility** -- cheap-to-reverse decisions need less certainty.
9. **Confidence** -- low / medium / high, grounded in which `[UNKNOWN]`s
   remain open.

### Phase 7 -- Artifact (always)

Emit a structured **First Principles Analysis** block; it stays in context
and guides subsequent work. Full Quick and Standard/Deep templates plus the
carry-forward summary format: `references/artifact-templates.md`.

Every artifact, at any depth, must contain: problem-as-outcome, mode, depth,
tool plan, claim ledger, mechanism sketch or map, assumptions challenged with
verdicts (Keep / Modify / Discard / Investigate), the recommendation with
each major choice citing a `[TRUTH]` or `[CONSTRAINT]`, at least one
verification check (falsifier / backward check / sensitivity), and **User
Checkpoints** -- the top 1-3 assumptions the user should confirm, reject, or
supply next. Exploration artifacts additionally include: best practical
option, most novel option, fastest experiment, biggest risk, and what would
make each option wrong.

## Brainstorming (Exploration depth)

Diverge first, converge second. Diverge with at least two of: Tree of
Thoughts (3-5 genuinely different paths, expand top 2, keep the runner-up),
Graph of Thoughts (ideas as nodes/edges, synthesize non-obvious
intersections), morphological matrix, contradiction analysis ("more X without
more Y"), or multi-perspective debate (mechanist, operator, red team,
creative strategist -- each critiques another before synthesis). Converge
with red-team critique, fastest experiment, and sensitivity to the dominant
assumption. Templates: `references/advanced-reasoning-tools.md`.

## Key Principles

- **Opinionated on process, neutral on solution.** Enforce deconstruction
  ruthlessly; then present options and let the user choose.
- **Separate IS from ASSUMED.** Distinguishing irreducible constraints from
  inherited conventions is the core skill; everything else follows.
- **Recursive, not linear.** Sub-problems have their own assumptions.
- **Proportional effort.** Trivial problems get trivial analysis.
- **Build from bedrock upward.** When the bedrock-derived answer matches the
  industry standard, fine -- the analysis converged; the convention was not
  imported.
- **Invert, always invert.** Forward analysis finds what to do; inversion
  finds what must be avoided. Both are required.
- **Development time is a ground truth too.** When an existing solution is
  within 2x of optimal and the team already knows it, that is usually the
  right answer. First principles pays off where convention is 10x wrong, not
  10% suboptimal.

## Common Traps

Reasoning by analogy creeping back in:

| Trap | Smell | Check |
|------|-------|-------|
| Analogy | "Company X does it this way" | Are your constraints identical in every relevant dimension? What did they have that you don't? |
| Complexity | Solution more elaborate than the problem | Remove components one at a time until removal breaks the outcome; what's left is the minimum design |
| Legacy | Compatibility with decisions that no longer serve | Why was it decided? Do those conditions still exist? Cost of changing vs. cost of keeping? |
| Tool | "We have X, so this is an X problem" | Would you pick this tool starting fresh today, no sunk cost? |
| Authority | "The senior engineer / PM / client said so" | Trace the instruction to the underlying need; reasoning must be reproducible from truths |
| Purity | Re-deriving everything from scratch | If convention is within 2x of optimal and known to the team, use it |

## Supporting Files

- `references/techniques.md` -- full toolbox: Socratic catalog, 5 Whys,
  inversion, Chesterton's Fence, falsifiability, ToT, Occam's Razor,
  mechanism mapping, Fermi, verification chains. Load when picking the right
  tool for a phase.
- `references/advanced-reasoning-tools.md` -- templates for every Tool Router
  row: mechanism map, assumption ledger v2, least-to-most, Fermi, evidence
  grounding, CoVe, self-consistency, sensitivity, brainstorming pack, solver
  trigger. Load at Deep or Exploration depth.
- `references/mode-playbooks.md` -- per-mode phase emphasis for all seven
  modes. Load after Phase 1.
- `references/artifact-templates.md` -- Quick and Standard/Deep artifact
  formats plus the carry-forward ledger summary. Load at Phase 7.
- `references/session-ledger-template.md` -- ledger lanes, import rules for
  pasted prior context, carry-forward block.
- `references/examples.md` -- four worked engineering examples end to end.
  Load to see what good output looks like.
- `references/review-notes.md` -- human-review note: this package is
  text-only, with no executable helper or automatic state mechanism.

## Boundaries

This skill challenges assumptions visibly, tags truths / assumptions /
unknowns distinctly, builds reasoning traceable to fundamentals, and surfaces
inversion risks and falsifiers. It does **not** dismiss conventional
solutions reflexively, expand trivial decisions into philosophy, override
domain expertise with naive re-derivation, promise the "best" solution (it
produces better *reasoning*), or keep running once the user says "skip the
analysis".

## Quick Reference Checklist

Before emitting a recommendation, confirm:

- [ ] Problem stated as an outcome, not a solution; mode and depth announced
- [ ] Tool Plan names only the tools the problem warrants
- [ ] Claim Ledger populated across all five lanes; user statements routed to the right lane via the Ground-Truth Test
- [ ] Mechanism map built when causality, strategy, systems, or debugging matter
- [ ] Assumptions given verdicts; constraints carry source + threshold + cost; unknowns carry resolution plan + sensitivity
- [ ] At least one inversion failure mode answered (Deep)
- [ ] Each design choice traces to a `[TRUTH]` or `[CONSTRAINT]`
- [ ] Strongest alternative view stated and addressed (Standard + Deep)
- [ ] Falsifier named; sensitivity and residual confidence stated
- [ ] Mode playbook followed; artifact emitted with User Checkpoints
