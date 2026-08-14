---
name: code-review
description: Use when reviewing a pull request, branch, worktree, diff, completed implementation, or proposed change before acceptance. Enforce the actual review target and comparison base, specification-backed evaluation, complete change coverage, change-level reasoning, evidence-supported high-signal findings, explicit disposition, and independent verification without inventing issues.
---

# Code Review

Review the actual current change independently against its governing behavior and the health of the affected system.
When a review materially creates or edits a technical artifact beyond the review output itself, `technical-writing` MUST govern that artifact.
If surrounding code, specifications, tests, dependencies, or history are not already sufficient to evaluate the change, `context-acquisition` MUST govern additional inspection.
When specifications, tests, implementation, or other contracts disagree, `spec-driven-development` MUST govern authority resolution.
When a validated finding requires a behavior-changing fix, `test-driven-development` and `implementation` MUST govern that fix.
When the review target includes executable code, configuration, dependencies, build or deployment logic, or reusable code examples, `secure-coding` MUST govern the security review. Its universal baseline always applies to that target; its security-impact assessment selects additional criteria and verification.

## Terms

A **review target** is the exact set of changes assigned for review.
A **comparison base** is the state against which the review target is compared.
A **finding** is an evidence-supported defect, requirement violation, regression risk, or material code-health problem attributable to the review target.
A **review limitation** is missing context, unavailable verification, unresolved authority, or another constraint that reduces review confidence without itself establishing a defect.

## Core Invariant

The reviewer MUST review the actual assigned change, not an assumed branch comparison or remembered implementation.
The comparison base MUST be established from the task, pull-request metadata, branch relationship, repository history, or another authoritative project signal.
`main`, `master`, or another default branch MUST NOT be assumed to be the comparison base.

A reported finding MUST be supported by concrete evidence or a specific reachable failure mechanism.
A finding quota MUST NOT be used.
The reviewer MUST NOT invent issues merely to make a review appear substantive.

Passing tests MUST NOT be treated as sufficient evidence that a change is correct, complete, maintainable, compatible, or secure.

## Establish Review Scope

Before reviewing findings:

1. Identify the requested review target.
2. Establish the actual comparison base when a comparison is required.
3. Identify committed, staged, unstaged, and relevant untracked changes that belong to the target.
4. Identify additions, modifications, deletions, renames, and moves that can affect behavior.
5. Identify generated or derived artifacts and their maintained sources.
6. Identify any explicit review exclusions or specialist-review boundaries.

When the task is to review the current branch or worktree, relevant staged, unstaged, and untracked changes MUST be included with the committed branch changes.
A branch review MUST NOT silently ignore current working-tree changes that belong to the task.
Deleted or moved behavior MUST NOT be ignored merely because little or no added text replaces it.

If the comparison base cannot be established, the reviewer MUST state the limitation and MUST NOT fabricate a base.
The review MAY continue over the change that can be established reliably.

Apply `references/review-scope.md` when branch ancestry, stacked changes, generated artifacts, or partial review scope make the target unclear.

## Establish Governing Behavior

The reviewer MUST identify the governing requirements, public contracts, accepted decisions, or other authoritative behavior that materially controls the change.
Tests MUST be treated as executable evidence unless the project explicitly declares them normative.
Author explanations and implementation rationale MUST NOT override a higher-authority contract.

If governing artifacts conflict, review of the affected behavior MUST pause until `spec-driven-development` resolves the authority conflict.
The reviewer MUST NOT choose whichever artifact makes the change appear correct.

## Review Independently

The reviewer MUST evaluate the final changed artifacts and observable behavior rather than rely on the author's implementation narrative.
A prior explanation MAY guide where to inspect, but it MUST NOT substitute for verification.

For significant self-review, a fresh reviewer or fresh review context SHOULD be used when available and proportionate.
This is house guidance intended to reduce anchoring on the implementation rationale; it is not a claim that fresh context guarantees independence.

The initial review MUST establish its findings before production fixes are applied, unless the user explicitly requests an iterative review-and-fix workflow.
This gate prevents the review target from changing while initial coverage is still incomplete.
If the task also authorizes fixes, validated findings MUST be handed to the applicable debugging, TDD, implementation, or specification workflow before code changes are made.
The changed result MUST be reviewed again for the addressed finding and any new affected behavior.

## Inspect the Change

Review coverage MUST include every changed human-authored line within the assigned review target unless the review scope explicitly assigns only a narrower aspect.
Changed-line coverage MUST NOT replace review of the change as a coherent behavior or design unit.
The reviewer MUST consider interactions across changed hunks, files, deletions, moves, and relevant unchanged code when those interactions can affect correctness.
Generated data, vendored content, machine-produced files, and large deterministic artifacts MAY be reviewed through their maintained source and generation contract when line-by-line inspection would not add material assurance.

Surrounding context MUST be acquired through `context-acquisition` only when it can change the interpretation of the changed code.
A changed line MUST NOT be judged in isolation when caller, callee, state, schema, requirement, test, or dependency context can materially change its meaning.

Review depth SHOULD increase with the potential impact of the change.
Changes involving data loss, authorization, security boundaries, concurrency, migrations, public APIs, compatibility, persistence, or irreversible effects SHOULD receive deeper scrutiny or specialist review when available.
When `secure-coding` applies to the review target, the reviewer MUST apply its universal baseline to the applicable target. When the change has security impact, the applicable impact-specific security criteria and verification MUST also be reviewed.

## Review Criteria

The review MUST consider the criteria that are material to the change.
Apply `references/review-criteria.md` for the detailed profile.

At minimum, review as applicable:

- conformance with governing requirements and contracts;
- functional correctness and reachable edge cases;
- design fit and unnecessary scope;
- complexity, duplication, speculative abstraction, and structural erosion;
- test correctness, usefulness, and missing behavior coverage;
- compatibility, migration, persistence, and state effects;
- error handling, concurrency, and failure behavior;
- the universal secure-coding baseline when `secure-coding` applies, plus security boundaries, authorization, sensitive data, sinks, and other impact-specific controls when applicable;
- naming, comments, documentation, and project style.

A criterion MUST NOT create a finding when it is irrelevant to the current change.
Personal preference MUST NOT be presented as a defect.

## Finding Gate

Before reporting a finding, verify that it identifies:

1. the affected location or behavior;
2. the violated requirement, invariant, contract, concrete failure mechanism, or concrete quality consequence;
3. the material consequence;
4. the evidence or reasoning that makes the issue credible;
5. whether the issue is blocking, recommended, optional, or unresolved.

A suspected issue that lacks enough evidence for a finding SHOULD be reported as a question or review limitation when it remains material.
Uncertainty MUST NOT be converted into certainty to increase finding count.
Finding severity MUST describe impact and likelihood; confidence in the finding MUST be reported separately when uncertainty is material.

When a finding can be verified safely with a focused check, reproduction, static analysis, compiler, or existing test, the reviewer SHOULD perform that verification when its cost is proportionate to the finding's impact.
A finding MUST NOT be rejected only because the existing test suite passes.

Apply `references/finding-quality.md` before reporting substantial findings.

## Scope of Findings

A review finding MUST be attributable to the review target or to behavior the target materially changes, exposes, or relies on.
An unrelated pre-existing defect MUST NOT be reported as a finding in a scoped change review unless the task explicitly requests a broader audit.
A pre-existing problem MAY be noted separately when it materially blocks evaluation of the current change.

Duplicate findings MUST be consolidated.
A style preference that is not required by a project rule SHOULD NOT block acceptance.
A suggestion for future work MUST be labeled non-blocking and MUST NOT be disguised as a defect in the current change.

## Finding Priority

The project's established severity or review-label scheme MUST be used when one exists.
When no project scheme exists, findings SHOULD be ordered by expected impact and likelihood, with correctness, security, data integrity, conformance, compatibility, and reliability ahead of polish.

Blocking language MUST be reserved for issues whose resolution is required before the change can be accepted safely or correctly.
Recommendations and optional suggestions MUST be labeled so that they cannot be mistaken for blockers.

Apply `references/finding-quality.md` for the local severity and disposition profile.

## Tests and Verification

Tests changed or added by the review target MUST themselves be reviewed as code.
The reviewer SHOULD ask whether each material test would fail for the incorrect behavior it claims to detect.
A test that merely mirrors the implementation or cannot fail under the relevant defect MUST NOT be treated as meaningful coverage.

When review confidence depends on runtime behavior, targeted verification SHOULD be run if it is safe and proportionate.
The reviewer MUST distinguish checks that were actually run from checks that were only inspected or inferred.

If the task specifically asks whether TDD was followed, `test-driven-development` MUST perform that process review.
General code review MUST NOT infer RED-before-GREEN history from the final diff alone.

## Review Output

Findings MUST be reported before non-blocking summary material.
Findings MUST be ordered by severity or material impact.
Each finding SHOULD identify the location, problem, consequence, and evidence concisely.

If no findings meet the finding gate, the reviewer MUST say that no findings were identified.
A no-findings result MUST NOT imply that unperformed verification or unavailable specialist review occurred.
Material review limitations and residual risks MUST be reported separately from findings.

The reviewer SHOULD avoid restating the entire diff or implementation when a concise finding-focused review is sufficient.

## Deviations

If the review target is too large to inspect reliably as one unit, the reviewer SHOULD partition it into coherent review slices when the task permits.
Coverage MUST NOT be silently reduced to make a large review fit available context.

If required context or verification is unavailable, the reviewer MUST report the limitation instead of guessing.
If a specialist domain exceeds the reviewer's available evidence or competence, the reviewer MUST state the need for specialist review rather than manufacture confidence.

Time pressure, passing CI, prior approval, author confidence, or the absence of obvious failures MUST NOT justify skipping the finding gate or the established review scope.

## Completion

Before substantial review work is reported complete, `references/review-checklist.md` MUST be applied.
A review MUST NOT be reported complete while its scope is unresolved, material in-scope change remains unreviewed, or a reported finding has not passed the finding gate.

## References

- `references/review-scope.md` — actual change target, comparison base, stacked branches, worktrees, and generated artifacts.
- `references/review-criteria.md` — functionality, design, complexity, tests, compatibility, documentation, and other review dimensions.
- `references/finding-quality.md` — evidence threshold, false-positive control, severity, and disposition.
- `references/review-process.md` — ISO/IEC 20246-informed lightweight work-product-review profile.
- `references/review-checklist.md` — completion review.
- `references/sources.md` — standards, practitioner guidance, research evidence, and house-policy boundaries.
