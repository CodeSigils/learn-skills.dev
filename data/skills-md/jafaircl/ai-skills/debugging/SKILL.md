---
name: debugging
description: Use when a defect, unexpected failing test, runtime error, unexpected output, regression, intermittent failure, or production symptom needs diagnosis before a fix is known. Enforce evidence-driven diagnosis, direct-evidence fast paths, falsifiable hypotheses when needed, distinguishing experiments, observed runtime evidence when material, causal discipline, and handoff to test-driven-development for behavior-changing fixes.
---

# Debugging

Diagnose failures from evidence before changing production behavior.
When this workflow creates a durable debugging report or materially edits technical documentation, `technical-writing` MUST govern that prose.
If the current context is insufficient to establish expected behavior, reproduce the symptom, or distinguish causes, `context-acquisition` MUST govern additional acquisition.
If expected behavior is absent, ambiguous, or conflicted, `spec-driven-development` MUST resolve it before the diagnosis is used to define a fix.
When resolution requires a change to executable behavior, `test-driven-development` MUST govern the fix after the defect and intended behavior are sufficiently established.

## Terms

A **symptom** is an observed deviation from expected behavior.
A **trigger** is an input, event, state, or condition that exposes a failure.
A **hypothesis** is a falsifiable causal explanation for the observed failure.
A **distinguishing experiment** is an observation or intervention whose result differs meaningfully depending on whether a hypothesis is true.
A **root cause** is a defect or causal condition whose correction explains and prevents the observed failure under the relevant conditions.
A **contributing factor** changes the likelihood, severity, or visibility of a failure without necessarily being its root cause.

## Core Invariant

A production fix MUST NOT be selected only from intuition, code appearance, correlation, or a plausible story.
An expected TDD RED failure that fails for the expected reason MUST NOT be treated as a debugging trigger. An unexpected or unexplained failure that requires causal diagnosis MUST be handled by this workflow before production repair.
The diagnosis MUST be supported by observed evidence that connects the suspected cause to the symptom.

When practical, the failure SHOULD be reproduced before the fix is implemented.
When deterministic reproduction is not practical, the diagnosis MUST use the strongest available evidence and MUST state the remaining uncertainty.
When runtime state can safely distinguish remaining explanations, observed runtime evidence SHOULD be preferred over model simulation.

If direct evidence uniquely establishes the defect mechanism, the agent MAY proceed without a hypothesis loop.
The direct evidence MUST connect the causal condition to the symptom and MUST be strong enough to exclude material alternative explanations.

When the cause is not established directly, a causal hypothesis MUST be tested before it is presented as an established root cause.
A symptom location, failing line, stack frame, or correlated event MUST NOT be labeled the root cause without causal evidence.

## Establish Expected and Observed Behavior

Before root-cause analysis:

1. Identify the expected behavior and its authority.
2. Record the observed behavior.
3. Identify the smallest known trigger or conditions that expose the symptom.
4. Separate verified facts from assumptions and hypotheses.

Expected behavior MUST NOT be invented from the current implementation.
If the expected behavior is unclear, authority resolution MUST be handed to `spec-driven-development`.

A failing test MAY provide the observed symptom, but a stale or incorrect test MUST NOT define expected behavior over a higher-authority specification.

## Reproduce and Bound the Failure

A stable reproduction SHOULD be created when it can be obtained safely and proportionately.
The reproduction SHOULD isolate the smallest conditions that still exhibit the symptom.

Reproduction work MUST preserve information required to explain the actual failure.
An oversimplified reproduction MUST NOT be accepted when it removes a material condition and changes the failure mechanism.

For intermittent failures, the agent SHOULD establish frequency, timing, concurrency, environment, input, or state conditions that distinguish failing from passing runs.
For regressions, the agent MAY use history comparison or permitted binary-search techniques to narrow the change window.

Apply `references/scientific-debugging.md` when the failure cannot be reproduced directly.

## Hypothesis Loop

Apply this loop when direct evidence has not already established the defect mechanism.
Before testing one hypothesis, identify material alternative explanations that the current evidence still supports.
The agent SHOULD NOT enumerate speculative alternatives that have no evidence-bearing connection to the symptom.

For each unresolved failure:

1. State one causal hypothesis precisely enough to be falsified.
2. Record the evidence that makes the hypothesis plausible.
3. Identify an observation that is expected to differ if the hypothesis is true versus false.
4. Choose the lowest-cost safe experiment that can distinguish those outcomes.
5. Run the experiment.
6. Record the result as supporting, weakening, or refuting the hypothesis.
7. Update or replace the hypothesis from the new evidence.
8. Repeat until the evidence is sufficient for the owning workflow to proceed.

An experiment SHOULD discriminate among plausible explanations rather than merely collect more data.
One causal variable SHOULD be changed at a time when doing so makes the result interpretable.
Negative results MUST be retained when they eliminate a plausible cause or constrain the search.

The agent MUST NOT repeatedly change production code to see whether a failure disappears.
A speculative patch MUST NOT substitute for a distinguishing experiment.

## Runtime Evidence

When actual runtime state can distinguish hypotheses safely, observed runtime evidence SHOULD be preferred over mentally simulating the program.
Relevant evidence MAY include:

- debugger state;
- execution traces;
- logs with adequate provenance;
- metrics;
- crash dumps;
- request or event traces;
- database or queue state;
- controlled diagnostic instrumentation.

Runtime observations MUST be tied to the failing conditions when those conditions affect interpretation.
A model-generated prediction of runtime state MUST NOT be presented as observed evidence.

Diagnostic instrumentation MAY be added when existing observability cannot answer a material hypothesis.
Temporary instrumentation MUST be removed after diagnosis unless a governing requirement or accepted observability decision makes it permanent.

Apply `references/runtime-evidence.md` before adding invasive instrumentation or relying on inferred runtime behavior.

## Causal Discipline

The diagnosis MUST distinguish symptom, trigger, root cause, and contributing factors when the distinction affects the fix.
A cause SHOULD explain the observed evidence, the relevant execution path, and why the symptom appears under the known trigger conditions.

A counterfactual or intervention SHOULD be used when practical: change or isolate the suspected causal condition and observe whether the predicted behavior changes.
Correlation alone MUST NOT establish causation.
A candidate patch that makes the symptom disappear MUST NOT, by itself, establish the root cause when the patch changes multiple conditions, masks the symptom, or has other plausible effects.

The agent MUST NOT force a single root cause when evidence supports multiple sufficient causes, interacting causes, or unresolved alternatives.
When several interventions can independently repair the failure, the report SHOULD identify that causal ambiguity rather than invent a unique explanation.

## Production and High-Cost Environments

Production evidence SHOULD be preserved before actions that can destroy or overwrite it.
Risky or destructive experiments MUST NOT be performed in production merely to improve diagnostic confidence.
A safer reproduction or observation path SHOULD be preferred when it can answer the same hypothesis.

When only production exposes the failure, the agent SHOULD prefer read-only evidence, bounded instrumentation, sampling, tracing, or other low-risk observations.
Operational safety, privacy, security, and availability constraints MUST take precedence over diagnostic convenience.

Apply `references/production-debugging.md` when diagnosis requires production-only evidence or stateful interventions.

## Handoff to TDD

When resolution requires a change to executable behavior, the agent MUST hand the fix to `test-driven-development` after expected behavior and the defect mechanism are sufficiently established.
The debugging reproduction MAY satisfy TDD RED only when it meets the TDD skill's requirements for a valid failing behavior check.
Debugging evidence MUST NOT be treated as permission to patch production behavior before the TDD gate.
When the resolution is operational or otherwise does not change executable behavior, the applicable owning workflow MUST govern the corrective action.

The handoff SHOULD identify:

- the expected behavior;
- the reproduced symptom or strongest failing evidence;
- the established or best-supported cause;
- the trigger conditions;
- evidence that supports the diagnosis;
- remaining uncertainty that can affect the fix.

Patch design and RED-GREEN-REFACTOR MUST remain owned by `test-driven-development` and `implementation`.

## Classification and Records

When a project requires structured anomaly records, IEEE 1044-2009-informed terminology MAY be applied through `references/anomaly-classification.md`.
Classification MUST NOT delay diagnosis when the project does not require it.
An anomaly category MUST NOT be used as a substitute for a causal explanation.

A durable debugging note SHOULD be recorded when the root cause, diagnostic method, or environmental condition is likely to prevent repeated investigation.
Trivial investigation history SHOULD NOT create permanent documentation noise.

## Deviations

If a stable reproduction cannot be obtained, the agent MAY proceed from converging evidence when waiting for reproduction is impractical.
The remaining uncertainty MUST be stated.

If no hypothesis can be distinguished with available evidence, the agent MUST report what is known, what has been ruled out, and what evidence is missing.
The agent MUST NOT manufacture certainty to unblock implementation.

If investigation reveals that the apparent defect is actually undefined or conflicting required behavior, debugging MUST stop and authority resolution MUST return to `spec-driven-development`.

## Completion

Before substantial debugging work is reported complete, `references/review-checklist.md` MUST be applied.
A diagnosis MUST NOT be reported as established while material causal uncertainty remains hidden or the claimed cause lacks the evidence required by the applicable direct-evidence or hypothesis path.

## References

- `references/scientific-debugging.md` — falsifiable hypotheses and distinguishing experiments.
- `references/runtime-evidence.md` — dynamic evidence, instrumentation, and inference boundaries.
- `references/production-debugging.md` — production-safe diagnosis and evidence preservation.
- `references/anomaly-classification.md` — optional IEEE 1044-informed anomaly terminology.
- `references/review-checklist.md` — debugging completion review.
- `references/sources.md` — research evidence, standards provenance, and house-policy boundaries.
