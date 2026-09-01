---
name: test-design
description: Use when designing, reviewing, layering, adding, pruning, or refactoring tests, especially to decide what deserves coverage, what should not be tested, which layer should own a behavior, and how to build high-value, low-fragility test suites with established test design methods.
license: MIT
metadata:
  author: vowdemon
  version: "1.0"
---

# Test Design

Protect system contracts, reduce regression risk, and keep feedback fast and trustworthy.

Reject these failure modes:

- API tutorials disguised as tests
- Coverage theater
- Mechanical restatements of already-proven rules
- Fragile checks coupled to implementation trivia

Keep these invariants:

- Cover the highest risk at the lowest reasonable cost
- Choose the cheapest layer that can prove the contract
- Let each test prove one distinct contract where practical
- Prefer observable behavior over implementation details

## Reference Guide

Read the smallest matching reference file first. Load a second file only when the first one cannot resolve the tradeoff.

| Reference | Read when | Extract from it |
| --- | --- | --- |
| [references/01-strategy-and-test-portfolio.md](references/01-strategy-and-test-portfolio.md) | Decide whether to add, move, or delete coverage; choose unit vs integration vs E2E; discuss coverage mix | Layer selection rules, portfolio shape, anti-pattern corrections |
| [references/02-unit-tests-and-test-maintainability.md](references/02-unit-tests-and-test-maintainability.md) | Write or review unit tests; prune duplication; simplify brittle tests | Unit-test construction rules, deletion triggers, maintainability checks |
| [references/03-test-doubles-hermeticity-and-dependencies.md](references/03-test-doubles-hermeticity-and-dependencies.md) | Choose real vs fake vs stub vs mock; isolate external dependencies | Test-double decision order, hermetic boundary rules, dependency handling |
| [references/04-integration-contract-and-e2e.md](references/04-integration-contract-and-e2e.md) | Decide integration vs contract vs end-to-end coverage | Promotion rules, E2E scope limits, collaboration-risk coverage |
| [references/05-ui-automation-and-user-visible-behavior.md](references/05-ui-automation-and-user-visible-behavior.md) | Design browser, UI, or component interaction tests | Locator priority, user-visible assertions, setup and waiting rules |
| [references/06-stability-isolation-and-flaky-test-control.md](references/06-stability-isolation-and-flaky-test-control.md) | Diagnose timing, order, or environment sensitivity; handle flaky suites | Flake triage order, root-cause map, retry and quarantine policy |
| [references/07-suite-structure-and-runner-governance.md](references/07-suite-structure-and-runner-governance.md) | Organize large suites; set markers, lanes, and runner policy | Suite layout rules, local/CI parity, strictness and scheduling guidance |

## Start With Risk

Before writing, moving, or deleting a test, answer:

1. What contract is most likely to break?
2. Which failure would be most costly?
3. At what layer can this behavior be proven best?
4. Is the same semantic already covered elsewhere?
5. Does the new test cover a distinct risk, or just restate an existing conclusion?

If these answers are unclear, clarify the contract first.

If the answers point to a category-specific tradeoff, load the matching reference file before deciding.

## Test Design Techniques

### Equivalence Partitioning

Group inputs by meaning and sample a small number of representatives. Do not test many values from the same partition unless they trigger different rules.

### Boundary Value Analysis

Prioritize:

- Minimum and maximum values
- Just-before and just-after thresholds
- Empty, zero, and single-item cases
- Initialized and uninitialized states

### Decision Tables

When behavior depends on combinations of conditions, list conditions and outcomes first, then select the smallest set of combinations that still proves the rule. Do not brute-force every combination unless the combinatorial space is itself the risk.

### State Transition Testing

When an object or system has a lifecycle, focus on:

- Valid transitions
- Invalid transitions
- Behavior after terminal states
- Idempotency of repeated operations

### Error Guessing

Actively ask:

- What will users most likely do wrong?
- Where is call order most likely to break?
- What may be null, timed out, stale, disposed, or repeated?

### Regression Pinning

When a real bug appears, add the smallest regression test that fixes that exact failure mode in place. A regression test should point directly at the broken contract, not expand into a grab bag of nearby behavior.

## Core Invariants

### Own The Contract At The Correct Layer

- The owner of the contract should own the test.
- If a lower layer can prove the rule stably, do not restate it higher.
- If the interaction itself is the contract, test the interaction once at the layer that owns it.

### Test Behavior, Not Internals

Prefer assertions on:

- Outputs
- Observable side effects
- Lifecycle semantics
- Public contracts

Avoid coupling to:

- Private fields
- Temporary intermediate state
- Call order with no contract guarantee
- Internal structures that exist only for the current implementation

### One Test, One Contract

If a test depends on multiple rules being correct, failures become harder to diagnose. Split it unless the interaction itself is the contract.

### Use the Smallest Witness

Keep only the setup required to prove the semantic difference. Remove extra subscribers, extra value types, extra wrappers, extra comments, extra fixtures, and extra steps.

### Tests Must Be Stable

Avoid reliance on:

- Timing luck
- Randomness
- Ambient environment state
- Test order
- Hidden shared state

Fake, mock, or pin boundaries when needed. A test that cannot reproduce reliably is not meaningful protection.

### Names Must Be Honest

A test name should accurately describe:

- The trigger
- The execution path
- The contract being guaranteed

If the path uses `value=`, do not name it `set()`. If the test proves snapshot reads, do not call it a subscription test.

## When To Delete Tests

Delete or move a test when any of the following is true:

- Shared behavior is already covered in shared tests
- It only restates an existing rule in different clothes
- Its main value is teaching API usage
- The same contract already has stronger coverage in a more appropriate file
- The setup is heavy but adds no new semantic
- The name and assertions do not match, and correcting them reveals duplication
- Two independent tests already imply the conclusion, so the extra test is only a mechanical combination

## When To Move Tests

Move a test instead of keeping it in place when:

- The ownership of the behavior has changed
- The current file is only testing it incidentally
- The real subject is a shared abstraction, readonly view, extension method, or runtime mechanism rather than the current concrete type

Rule: the owner of the contract should own the test.

## Review Checklist

When reviewing a test suite, ask for each test:

- What unique contract does it protect?
- Is that contract worth protecting?
- Is it in the correct layer and file?
- Is equivalent coverage already present?
- Is the setup already minimal?
- Does it depend on internals?
- Is it stable, repeatable, and diagnosable?
- Would deleting it increase real risk?

## Quick Decisions

- If deleting it does not reduce semantic coverage, delete it.
- If another file owns the rule better, move it.
- If half the setup can be removed and the assertion still proves the same thing, the original test was bloated.
- If a lower layer can prove the rule stably, do not restate it at a higher layer.
- Confidence comes from representative boundaries and distinct contracts, not from repeating the same rule many times.
