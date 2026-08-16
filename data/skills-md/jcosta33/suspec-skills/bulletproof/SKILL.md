---
name: bulletproof
description: Fact-check claims and prove completed implementation against direct evidence. Use when claims need validation, cross-examination, or hardening, or completed work needs decisive command proof. Do not use as the owner of broad risk discovery, requirement conformance, or one-sided advocacy.
---

# Bulletproof

Trust nothing. Prove everything checkable.

## Method

Run the matching branch. Run both only when claims and completed implementation both need proof.

### Verification

1. Freeze the claim set, target, and state.
2. Expose every load-bearing assumption.
3. Define proof and falsification before searching.
4. Inspect authoritative local sources. Use primary sources for external facts.
5. Run safe checks against absent, stale, or indirect evidence.
6. Let evidence kill disagreement.

### Implementation Proof

Preserve decisive command facts after code or validation work.

## Output

For verification, return one rendered Markdown table:

| ID | Assessment | Evidence |
| --- | --- | --- |

Give every identifiable claim one row:

- `Supported`: decisive evidence establishes it.
- `Unsupported`: decisive evidence contradicts it.
- `Unverified`: available evidence cannot establish or contradict it.
- `Blocked`: required evidence exists but cannot be obtained.

Name the exact gap for `Unverified` and `Blocked`.

For implementation proof, return each decisive run once in chat: command, working directory, state
identifier, numeric exit, and the smallest untouched decisive output excerpt.

## Boundaries

Freeze the verification target. Acceptance and requirement conformance are outside this method.
