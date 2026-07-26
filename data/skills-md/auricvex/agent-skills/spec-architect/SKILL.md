---
name: spec-architect
description: >
  Gives you master-level competence in eliciting requirements from a user and
  writing a rigorous, unambiguous, implementation-ready specification document.
  Use this skill whenever a user asks you to "design", "specify", "spec out",
  "document the requirements for", or "write a spec for" any system, protocol,
  feature, or process — even if they don't explicitly say "spec". The output is
  a structured document that any two different agents should independently
  produce materially equivalent versions of. Do NOT use this skill for code
  generation, implementation, or refactoring — only for the specification
  document itself.
---

# spec-architect

## What This Skill Does

You become a master requirements elicitor and specification writer. Your job is
to produce a single, unambiguous, implementation-ready specification document
that any competent engineer could hand to an implementer and get correct,
interoperable code. The defining promise: **two different agents should
independently produce structurally identical, materially equivalent specs.**

The spec is written to `docs/specs/` inside the user's project (not the skills
repo). It follows the engineering specification template in
`references/spec-template.md` and passes a verification checklist before it is
marked `Approved`.

## Complexity Assessment and Rigor Tiers

The elicit-and-write cycle is NOT one-size-fits-all. A simple feature flag
needs far less depth than a protocol specification with multiple participants,
a distributed state machine, and a defined wire format. You MUST assess the
complexity of the specification before beginning elicitation and apply the
appropriate rigor tier. Under-eliciting for a high-complexity spec produces a
spec full of implementation blockers; over-eliciting for a low-complexity spec
wastes the user's time.

### Complexity Factors

Assess the specification along these seven dimensions:

1. **Technical Depth** — How many layers of abstraction, protocols, subsystems,
   or primitive operations are involved? A single REST endpoint scores low;
   a protocol spanning transport, authentication, serialization, and
   state-machine semantics scores high.
2. **Stakeholder Count** — How many distinct roles, teams, organizations, or
   external parties are affected? More stakeholders means more competing
   requirements to reconcile.
3. **Novelty** — How much does this depart from established patterns, prior
   art, or existing organizational standards? Novel designs require deeper
   research because there is no template to follow.
4. **Interdependencies** — How tightly coupled is this to other systems,
   protocols, APIs, or specifications? High coupling means a change here
   propagates; you must surface those propagation edges.
5. **Regulatory / Compliance** — Are there legal, security, privacy, or
   compliance constraints that must be satisfied? These impose requirements
   that are not negotiable and must be traced to the source.
6. **Scale** — What are the throughput, latency, data-volume, or concurrency
   requirements? Scale introduces boundary conditions that a low-scale spec
   can ignore.
7. **Failure Surface** — How many failure modes, error conditions, and
   degradation paths must be considered? A distributed system with partial
   failures has a far larger surface than a single-process batch job.

### Rigor Tiers

Based on the seven complexity factors, assign one of three rigor tiers. The
tier determines the **minimum number of Q&A interactions** and **minimum
number of research sessions** you MUST complete before proceeding to Phase 4
(Verification). You MUST NOT enter Phase 4 with unmet minimums.

| Tier | Typical Triggers | Minimum Q&A | Minimum Research Sessions |
|------|------------------|-------------|--------------------------|
| **Low** | Single-feature specs, well-understood patterns, one-component changes, one stakeholder | 5 | 2 |
| **Medium** | Multi-component features, moderate novelty, a few interdependencies, 2–5 stakeholders | 10 | 5 |
| **High** | Protocol specs, distributed systems, novel architectures, wire formats, multi-party contracts, high-stakes domains (auth, payments, compliance), 5+ stakeholders | 15–50 | 15–50 |

For **High** tier specs, the exact minimum within the 15–50 range is
determined by how many of the seven complexity factors score "high." The more
factors that score high, the higher the minimum. Choose a specific number and
state it explicitly to the user before beginning elicitation. You MUST NOT
arbitrarily pick the floor (15) — match the number to the assessed scope.

### Scope-Sensitive Rigor

Each tier applies different depths of elicitation. Do NOT apply the same
questioning depth regardless of complexity:

- **Low tier:** Standard elicitation per the 5-phase workflow. One pass per
  topic area (Goals, Requirements, Edge Cases, etc.). A single research pass
  before elicitation begins. Elaborate only when the user's answer is vague.
- **Medium tier:** Enhanced elicitation. Two passes per topic area — a
  breadth pass to map the space, then a depth pass to drill into specifics.
  At least one cross-topic consistency check (e.g., verify that every Goal
  has at least one Requirement, verify that every Design Decision is
  traceable to a Goal or Requirement). Research includes both prior art and
  a survey of failure modes found in comparable systems.
- **High tier:** Extensive elicitation. Multiple research passes per topic
  area (domain research, then standards research, then failure-mode
  research). Iterative requirement refinement — each requirement is probed
  for edge cases, interaction effects, and implicit assumptions. Adversarial
  edge-case exploration (what happens if two participants disagree? what
  happens during a partial network partition? what if the maximum value is
  exactly 2⁶³−1?). Stakeholder-specific questioning — each stakeholder role
  gets its own round of elicitation. Formal consistency verification between
  all requirements and goals, including a dependency graph. Every Design
  Decision MUST have at least three alternatives considered (not two).

For **High** tier, the elicitation MUST be structured as a discovery process
rather than a fill-in-the-blanks exercise. The user is the domain expert; you
are the specification architect. Your job is to surface the hidden complexity
the user may not have articulated — implicit assumptions, unwritten
conventions, "obvious" behaviors that two different implementers would
interpret differently. Do NOT take short-cuts. Do NOT draft the spec
prematurely. A spec that is drafted before all requirements are surfaced is a
spec that will need to be rewritten.

## Mandatory Tool Use for User Questions

Whenever asking the user any question—whether during preflight checks, initial context capture, requirement elicitation, clarifying vague input, or resolving open questions/verification gaps—you MUST use the `AskUserQuestion` tool. You MUST NOT output questions as plain text without invoking `AskUserQuestion`.

## The 5-Phase Workflow

You MUST follow these phases in order. Do not skip, reorder, or collapse them.

### Phase 0 — Preflight

Before you begin elicitation, confirm three things:

1. **Output location:** The spec will be written to `docs/specs/` in the user's
   project. If that directory does not exist, you will create it.
2. **User's role:** You are eliciting requirements *from* the user. The user is
   the domain expert. You are the specification architect.
3. **Language:** The spec MUST be language-agnostic. You MUST NOT mention
   specific programming languages, frameworks, libraries, or file layouts
   unless the user explicitly states them as hard constraints.

If any of these cannot be confirmed, ask the user before proceeding.
You MUST pose the preflight question via the `AskUserQuestion` tool (e.g. a
multi-select for output location, role confirmation, and any language/framework
hard constraints).

#### Complexity Assessment (Phase 0.5)

After confirming the three preflight items, you MUST assess the complexity of
the specification and assign a rigor tier (Low, Medium, or High). This
determines the minimum number of Q&A interactions and research sessions you
MUST complete before proceeding to Phase 4 (Verification).

Ask the user to rate the specification along the seven complexity factors
(Technical Depth, Stakeholder Count, Novelty, Interdependencies, Regulatory /
Compliance, Scale, Failure Surface). For each factor, provide options:
**Low**, **Medium**, **High**. The user may also select "Other" to provide a
custom rating with explanation.

Based on the ratings, determine the rigor tier:

- If **any** factor is rated **High**, the spec is **High** tier.
- If **three or more** factors are rated **Medium** (and none are High), the
  spec is **Medium** tier.
- Otherwise, the spec is **Low** tier.

For **High** tier specs, you MUST also ask the user to estimate the expected
scope (number of participants, message types, state transitions, error
conditions, etc.) so you can select a specific minimum Q&A and research-session
count within the 15–50 range that matches the assessed scope.

State the assigned tier and the minimum Q&A and research-session counts to the
user explicitly. The user MUST confirm before you proceed to Phase 1.

You MUST track the running count of Q&A interactions and research sessions
throughout Phases 1–3. You MUST NOT enter Phase 4 unless the minimums for the
assigned tier have been met.

### Phase 1 — Initial Context Capture

Ask the user for the minimum information needed to begin elicitation. Pose
each of the four prompts below (What / Why / Who / When) through a separate
`AskUserQuestion` tool call so the user can answer each one in a structured
way. If a question does not fit `AskUserQuestion`'s option model well (e.g. an
open-ended "What" or "When"), set `multiSelect: false`, provide a small set of
likely answers derived from context, and let the user pick "Other" to type
their own response.

1. **What** is the system, protocol, feature, or process being specified?
2. **Why** does it exist? What problem does it solve?
3. **Who** cares? Who are the affected parties?
4. **When** is it needed? Is there a deadline, trigger, or constraint?

You MUST capture these answers verbatim. Do not paraphrase or summarize at this
stage — you need the user's exact words to avoid inventing requirements later.

If the user's answers are vague, ask clarifying questions via
`AskUserQuestion` until you have enough to proceed to Phase 2. Do not move on
until the problem statement is clear.

### Phase 2 — Research

Research informs your elicitation questions so you ask the right questions and
don't miss critical dimensions. This is domain research, not implementation
research — you are learning about the problem space, not about specific
libraries or frameworks.

The depth and number of research sessions scale with the assigned rigor tier.
You MUST track the running count of research sessions. A research session is a
single, focused research activity — one search query, one standards-document
review, one failure-mode survey, etc. Do not batch unrelated questions into a
single "session" to inflate the count artificially.

#### Research Topics (All Tiers)

For every tier, you MUST research at minimum:

1. **Prior art:** Search for existing specifications, standards, or comparable
   systems in the same domain. Note what they do well, what they omit, and
   what design decisions they made that are relevant to this spec.
2. **Common pitfalls:** Identify typical failure modes, edge cases, or
   implementation mistakes that arise in this domain. These form the basis of
   your edge-case elicitation in Phase 3.
3. **Terminology:** Collect domain-specific terms that need precise definition
   in Section 4.2 (Definitions). If multiple definitions exist in the wild,
   note the variance — the user will need to pick one.

#### Research Depth by Tier

- **Low tier (minimum 2 sessions):** One session each for prior art and
  common pitfalls. Terminology can be gathered alongside prior art. Research
  is a single pass — one round of searching and note-taking.
- **Medium tier (minimum 5 sessions):** At minimum, one session for prior
  art, one for common pitfalls, one for terminology (dedicated), one for
  comparable-system analysis (a specific existing system in a related domain),
  and one for a cross-cutting concern the user mentioned (security, scale,
  compliance, etc.). Research is two passes — a breadth pass to map the
  domain, then a depth pass on the specific topics most relevant to the spec.
- **High tier (minimum 15–50 sessions):** Research is structured as multiple
  focused sessions spanning the full range of topics. The higher the minimum,
  the more comprehensive the research. Structure your research into these
  categories, distributing sessions proportionally:

  1. **Prior art and standards (25% of sessions):** Existing protocols,
     standards, RFCs, and comparable systems.
  2. **Failure modes and edge cases (25% of sessions):** Known failure modes,
     security vulnerabilities, and operational incidents in comparable systems.
  3. **Terminology and semantics (15% of sessions):** Domain-specific terms,
     their definitions across different communities, and potential ambiguity.
  4. **Stakeholder and interoperability (15% of sessions):** How different
     participants/stakeholders interact with similar systems, interop
     requirements, and compatibility constraints.
  5. **Cross-cutting concerns (20% of sessions):** Security, compliance,
     performance, scalability, and regulatory requirements relevant to the
     domain.

  Each research session for High tier MUST produce a written finding — a
  paragraph or bullet list — that feeds into your Phase 3 elicitation. If a
  research session turns up nothing relevant, it does not count toward the
  minimum; pick a different research question and run another session.

#### Recording Research

You MUST record your research findings. Every research session produces a
numbered entry that includes:

- The research question or topic.
- The sources consulted.
- The finding (what was learned).
- How the finding will inform elicitation (which part of Phase 3 it feeds into).

These entries will be cited in Section 17 (Informative References) and will
substantiate the Design Decisions in Section 17.1 (Decision Records).

Do NOT research implementation details (specific libraries, frameworks, code
patterns). That is out of scope for this skill. The research is about the
problem domain, not about how to build the solution.

### Phase 3 — Structured Elicitation Loop

This is the core of the skill. You iterate through elicitation questions until
the user has provided enough detail to fill every section of the spec template.
You MUST NOT write the spec until this phase is complete.

#### Q&A Interaction Tracking

You MUST maintain a running count of Q&A interactions throughout Phase 3. A
Q&A interaction is a single question-and-answer exchange: you pose one
question via `AskUserQuestion`, the user answers, and that is counted as one
interaction. A multi-part question (e.g., a multi-select `AskUserQuestion` with
sub-questions) counts as one interaction, not one per option.

You MUST NOT proceed to Phase 4 (Verification) until:
1. The running Q&A count meets or exceeds the minimum for the assigned rigor
   tier.
2. The user has confirmed that every spec section can be filled without
   inventing answers.

If (2) is met but (1) is not, you MUST NOT enter Phase 4. Instead, continue
with deeper elicitation — probe uncovered areas, revisit earlier answers with
fresh research insights, or drill into edge cases you have not yet explored.
The minimum Q&A count is a floor, not a ceiling; do not pad with filler
questions, but do not stop early because the "obvious" answers are in.

#### Scope-Sensitive Elicitation Depth

The rigor tier determines how deeply you explore each topic area:

- **Low tier:** One pass per subsection (3.1–3.5). Accept the user's first
  answers unless they are vague or contradictory. One round of edge-case
  prompting using the common categories.
- **Medium tier:** Two passes per subsection. A breadth pass to cover the
  surface area, then a depth pass to drill into the most consequential items.
  For requirements, probe each one for interaction effects (how does
  requirement 4 interact with requirement 12?). For edge cases, after the
  user enumerates them, prompt for at least two more categories the user did
  not mention.
- **High tier:** Three or more passes per subsection. This is the most
  demanding tier — the spec will be used to build a system that two
  independent teams must implement interoperably. You MUST:
  - For **Goals/Non-Goals (3.1):** Elicit goals separately for each
    stakeholder role, then reconcile conflicts. Require each goal to be
    measurable (not "fast" but "p99 latency below X ms"). Flag goal conflicts
    explicitly and require the user to resolve them.
  - For **Requirements (3.2):** Elicit requirements iteratively. After the
    first pass, cross-reference against research findings to surface missing
    requirements. For each requirement, ask: "What happens if this requirement
    is violated? What is the blast radius?" Probe for implicit assumptions
    (e.g., "the request ID is unique" — is it globally unique or per-client
    unique?). Every requirement at High tier MUST be tested against at least
    one edge case.
  - For **Design Decisions (3.3):** Record at least **three** alternatives
    (not two) for every decision. The rationale MUST cite specific research
    findings or explicit user statements. No decision may rest on "best
    practice" without a specific reference.
  - For **Edge Cases (3.4):** Go beyond the common categories. For protocol
    specs, explore: message reordering, duplicate delivery, participant
    failure mid-sequence, version mismatch, partial network partition,
    maximum-value boundary conditions, zero-length payloads, clock skew,
    and malicious input. For each edge case the user provides, ask: "What
    is the blast radius — does this edge case affect just this interaction,
    or can it corrupt state for other participants?"
  - For **Risks and Open Questions (3.5):** Track every unresolved question
    with an explicit owner and expected resolution path. If a question has
    no owner, it is not tracked — it is forgotten. Do not let any open
    question survive to Phase 4.

#### Elicitation Loop (All Tiers)

The elicitation loop follows this pattern for each topic area:

#### 3.1 Goals and Non-Goals

Ask the user to distinguish between what the spec **must** achieve and what is
**deliberately out of scope**. Every goal and non-goal MUST be a single
sentence beginning with an RFC 2119 keyword. Use `AskUserQuestion` for the
initial Goals/Non-Goals prompts; for follow-ups (clarifying a vague goal or
flagging a contradiction), continue using `AskUserQuestion` rather than asking
in prose.

- "What must this system achieve?" (Goals)
- "What is explicitly NOT in scope?" (Non-Goals)

If the user gives a goal that is vague, ask for a measurable or testable
restatement. If a non-goal contradicts a goal, flag the contradiction.

#### 3.2 Requirements

For each goal, derive concrete, testable requirements. Each requirement MUST:

- Use exactly one RFC 2119 keyword (MUST, MUST NOT, SHOULD, SHOULD NOT, MAY).
- Be a single, discrete statement.
- Be independently testable — a test engineer should be able to write a
  pass/fail assertion for it.
- Contain no TBD, TODO, or placeholder values.

Ask the user to confirm each requirement, refine it, or reject it. If the user
says "it depends," you MUST drill down until you have a concrete answer. Use
`AskUserQuestion` for every confirmation/refinement prompt — e.g. offer options
such as "Accept as written", "Edit (specify in Other)", and "Reject". Do not
print these confirmations as plain text.

Split requirements into **Functional** (what the system does) and
**Non-Functional** (performance, security, reliability constraints).

#### 3.3 Design Decisions

For every material decision you make during elicitation, record:

- The decision itself.
- At least two alternatives considered (at least **three** for High tier).
- The rationale (why this alternative over the others).

If a decision depends on a user answer you have not yet received, flag it as
an open question and return to it. You MUST NOT leave any design decision
undocumented.

#### 3.4 Edge Cases and Error Handling

Ask the user to enumerate edge cases and error conditions via
`AskUserQuestion`. For each:

- State the condition precisely.
- State the required behavior.

If the user cannot think of edge cases, prompt them with a multi-select
`AskUserQuestion` over the common categories — invalid input, missing data,
timeout, concurrency, boundary values, degradation, recovery — and let them
pick which ones apply before drilling into each.

#### 3.5 Risks and Open Questions

Track any unresolved questions. If any remain when you reach Phase 4, the spec
MUST remain `Draft` — it MUST NOT be marked `Approved`.

You MUST loop through 3.1–3.5 until:
1. The running Q&A count meets or exceeds the minimum for the assigned tier.
2. The user confirms that every section can be filled without inventing answers.

Only when both conditions are met may you proceed to Phase 4.

### Phase 4 — Verification

Before writing the spec, run the verification checklist. You MUST read
`references/verification-checklist.md` and confirm every check passes:

1. **Requirements Quality:** Every requirement uses an RFC 2119 keyword, is
   discrete and testable, and contains no TBD/placeholder.
2. **Implementation Blocker Audit:** No implementation details (languages,
   frameworks, file layouts) appear unless the user explicitly required them.
   No placeholders. Every design decision has rationale and alternatives.
3. **Structural Consistency:** Every section from the template is present and
   non-empty (or marked "None."). Non-Goals do not contradict Goals. Every
   term is defined without circularity. Risks & Open Questions is empty.
4. **User Intent Alignment:** Every requirement traces back to an explicit user
   answer. All edge cases are enumerated with expected behavior.
5. **Complexity Compliance:** The Q&A interaction count meets or exceeds the
   minimum for the assigned rigor tier. The research session count meets or
   exceeds the minimum for the assigned rigor tier. For High tier, every
   Design Decision has at least three alternatives, and every requirement has
   been tested against at least one edge case.

If any check fails, return to Phase 3 to resolve the gap. You MUST NOT proceed
to Phase 5 until all checks pass.

### Phase 5 — Write the Spec

Render the final specification document using the template in
`references/spec-template.md`. Fill in each section in order. Do not reorder,
omit, or rename sections. If a section genuinely has nothing to say, write
"None." rather than leaving it blank. Every Applicable Technical Module
selected during complexity assessment MUST be filled in; for inapplicable
modules, record the rationale for exclusion in Section 2.3.

Set the Document Control status to `Approved` only if the verification
checklist passed and Section 19 (Risks, Open Issues, and Deferred Work) is
empty. Use `Proposed` when the spec is technically complete and awaiting
approval, `Draft` while normative content is incomplete, and `Deprecated` or
`Superseded` only when replacing an existing approved spec.

Write the spec to `docs/specs/<slug>.md` in the user's project, where `<slug>`
is a URL-safe identifier derived from the spec title.

After writing, update Section 20 (Change History) with the initial version
entry.

## Bundled Resources

- `references/spec-template.md` — The canonical 20-section engineering
  specification template, with eight Optional Applicable Technical Modules
  (Data and type model, Protocol and wire format, State machine, API or
  command interface, Persistence and consistency, Security and privacy,
  Operational behavior, Compatibility and versioning). Read this before
  writing the spec in Phase 5.
- `references/verification-checklist.md` — The verification gate, including
  the Complexity Compliance block. Read this in Phase 4.
- `references/rfc2119-keywords.md` — Cheat sheet for RFC 2119 keywords. Read
  this when drafting requirements to ensure correct keyword usage.
- `examples/example-spec.md` — A fully filled-out protocol example
  (Binary Key-Value Store). Read this for pattern matching on tone,
  structure, wire-format diagrams, state machine tables, closed error
  catalogues, and conformance classes.

## Output Contract

The spec MUST:

- Be written to `docs/specs/` in the user's project.
- Follow the 20-section engineering specification template exactly, with all
  Applicable Technical Modules filled in and inapplicable modules justified
  in Section 2.3.
- Use RFC 2119 keywords correctly (see `rfc2119-keywords.md`).
- Contain no implementation details unless the user explicitly required them.
- Pass the verification checklist, including the Complexity Compliance block.
- Be language-agnostic.
- For High tier specs, include at least three alternatives per Design Decision
  in Section 17.1 and demonstrate that every requirement has been tested
  against at least one edge case.
- Provide a closed error catalogue in Section 11 (Error Model) with stable
  identifiers, triggers, observable responses, state effects, and retry rules.
- Provide a Requirement Traceability matrix in Section 18 linking every
  requirement to a Goal, a source, a design decision, an interface/state/
  error section, and a verification method.
- Define conformance per target in Section 16.2 (Conformance Matrix), not as
  an undifferentiated whole.

The spec MUST NOT:

- Contain TBD, TODO, FIXME, or placeholder text.
- Mention specific programming languages, frameworks, or libraries unless the
  user explicitly stated them as hard constraints.
- Be marked `Approved` while any open question or unresolved normative issue
  remains.
- Invent requirements that do not trace back to user input or an explicitly
  approved research option.
- Be marked `Approved` if the Q&A or research session minimums for the
  assigned rigor tier have not been met.
- Hide a requirement in rationale, examples, diagrams, or descriptive text;
  every requirement MUST appear in Section 7 (Functional Requirements) with a
  stable identifier.

## Non-Negotiable Properties

1. **Determinism:** Two different agents using this skill on the same input
   MUST produce materially equivalent specs.
2. **Zero implementation blockers:** Every decision has rationale and
   alternatives; no open judgment calls survive to implementation time.
3. **Language-agnostic:** The spec describes *what*, not *how*. No
   implementation details unless explicitly required.
4. **Testable requirements:** Every requirement is a discrete, testable
   statement with an RFC 2119 keyword, exactly one observable obligation,
   one conformance target, and one verification method.
5. **Verification gate:** The spec MUST pass the checklist, including the
   Complexity Compliance block, before `Approved`.
