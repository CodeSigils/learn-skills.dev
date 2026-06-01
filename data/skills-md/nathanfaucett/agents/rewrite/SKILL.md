---
name: rewrite
description: |
  Performs a structured, opinionated, and safety-conscious full rewrite
  that intentionally introduces breaking changes. Invoke when a repository,
  package, or service needs a clean-start architecture and preserving
  backward compatibility is not a requirement.
---

## Summary

Use this skill to plan and execute a deliberate, well-documented, and
risk-aware full rewrite of a codebase or package. Rewrites are opinionated
and may break APIs, repository layout, or deploy-time contracts; they are
appropriate when technical debt, architecture constraints, or product
direction make incremental refactors impractical.

## When to use

- The team has decided a behavior-preserving refactor is insufficient.
- The repository suffers from pervasive architectural issues or
  unfixable legacy constraints.
- Backward compatibility may be broken but migration paths are acceptable.
- A new target architecture, platform, or runtime is required (e.g., move
  from monolith → services, Python2 → Python3+, callback → async).
- The user explicitly requests a "clean start" and accepts migration work.

## When not to use

- For small improvements or clarifying renames — prefer the `refactor` skill.
  - Example: renaming a helper or splitting one large function.
- When API compatibility must be preserved without migration windows.
  - Example: patch release commitments that cannot break external clients.
- When tests or deployment pipelines are absent and risk is unacceptable.
  - Example: service rewrites without baseline CI or rollback automation.

## Inputs

- `scope`: files, packages, services, or directories to rewrite. If omitted,
  ask for clarification.
- `goals`: target architecture, quality attributes, performance targets,
  and constraints.
- `migration`: desired migration strategy and target compatibility level.
- `timeline`: delivery cadence, release windows, and acceptable downtime.
- `tests_ci`: commands or expectations for tests and CI verification.
- `stakeholders`: list of owners, release managers, and integrators to notify.
 
## Outputs

- A concrete rewrite plan with milestones, risks, and rollback strategies.
- A patched repository implementing the new architecture (one or more commits).
- A migration guide and compatibility matrix for downstream users.
- Tests, CI updates, and a release checklist demonstrating readiness.
 
## Procedure

1. Ask one concise clarifying question if `scope` or `goals` are missing.
2. Create a short, high-level migration plan with milestones and rollback
   criteria (design doc or PR description).
3. Identify invariants and critical behavior that must be preserved
   (contracts, data formats, public APIs).
4. Establish a test and CI baseline: list required tests and add coverage
   checks that must pass before merging.
5. Implement the rewrite in small, reviewable PRs where practical. Each PR:
   - Implements a single concept (layout, core module, API surface).
   - Includes tests and CI changes.
   - Updates documentation and the migration guide.
6. Provide a dedicated migration/upgrade path: compatibility shims,
   feature flags, compatibility packages, or upgrade scripts.
7. Coordinate with stakeholders about timelines, deprecations, and release
   windows; document breaking changes in a changelog.
8. Run integration and smoke tests in an isolated environment; validate
   rollback procedure.
9. Merge and publish following the release checklist; tag breaking-change
   versions clearly.
10. After release, monitor errors, gather feedback, and publish migration
    follow-ups or hotfixes as needed.

## Best practices and constraints

- Prefer incremental, reversible changes even inside a rewrite; keep each
  change reviewable and small when possible.
- Preserve documented invariants and validate them with tests.
- Provide clear, automated migration steps; assume downstream users will
  rely on scripts and examples.
- Avoid simultaneous large unrelated changes (dependency bumps, format).
- Keep communications proactive: announce the rewrite, the migration
  timeline, and the expected impact in repo docs and release notes.
- Keep commits focused and atomic to ease review and reversion.

## Gotchas and edge cases

- Rewrites without stakeholder sign-off often fail at release time.
- Migration guides that are too abstract cause downstream upgrade failures.
- Running multiple major rewrites at once increases coordination risk.
- Untested rollback procedures can turn recoverable incidents into outages.

## Examples

- "Rewrite the authentication service from Express → Fastify and split
  handlers into typed modules; provide migration shims for middleware."
- "Migrate the monolithic CLI from synchronous I/O to an async plugin
  architecture and document changes to plugin API."
- "Replace an internal ORM with a smaller data-access layer and provide
  data-migration scripts and a compatibility layer for legacy queries."

## Commit & PR Templates

- Commit title format: `rewrite(<scope>): Short summary` (e.g.,
  `rewrite(auth): migrate to typed services`).
- PR description should include: motivation, migration plan, list of
  breaking changes, rollout steps, rollback instructions, and test matrix.

## Acceptance Criteria

- Migration guide and compatibility matrix exist and are reviewed.
- Tests and CI run green for the new implementation and the migration
  verification steps.
- Stakeholders have approved the release plan and rollback criteria.
- The rewrite is delivered in clear, reviewable commits with changelog.

## Notes for Agents

- Ask exactly one clarifying question when `scope` or `goals` are missing.
- Prefer producing a small design doc (README or PR description) before
  editing large amounts of code.
- Avoid speculative architectural changes without explicit stakeholder
  approval.

## References

- Follow repository conventions in AGENTS.md and use the `refactor` skill
  for behavior-preserving alternatives.

