---
name: implementation
description: >-
    Apply minimal, style-matched code and config changes with clear scope boundaries,
    evidence-backed verification, and handoffs to testing, debugging, and release
    skills.
---

# Implementation Skill

This skill governs **how** to change a codebase: tight scope, consistent style,
verifiable outcomes, and safe collaboration with other skills and subagents. It follows
the **Agent Skills** model ([agentskills.io](https://agentskills.io/what-are-skills)):
**discovery** uses only this file’s YAML `name`/`description`; **activation** loads full
instructions below; optional **`references/`**, **`scripts/`**, or **`assets/`** in the
same folder can hold project-specific conventions—load them when the task requires local
detail.

## Scope

### In scope

- Implementing or adjusting **application code**, **tests**, **build config**, and
  **small doc updates** tied to the change (e.g. README snippet for a new flag).
- **Minimal diffs**: one logical change set; avoid drive-by refactors and unrelated
  formatting sweeps.
- **Matching** existing patterns: imports, naming, error handling, module layout, and
  test style.

### Out of scope (hand off)

- **Architecture** or boundary decisions you cannot justify from existing code → involve
  **Architect** subagent or **planning** skill first.
- **Security-sensitive** auth, crypto, or secret handling paths → **Security Reviewer**
  subagent.
- **Integration contracts**, idempotency, or webhook semantics → **Integrationist**
  subagent.
- **Large refactors** or wide renames → **refactoring** skill with an explicit plan.
- **Production incidents** or SLO breaches → **incident-responder** skill before deep
  code changes.

If the user’s request mixes implementation with design debate, **split**: capture
decisions under **planning**, then return here for execution.

## Branching: choose a path early

Use this decision tree at skill activation:

1. **Requirements clear and files identified?**
    - **Yes** → proceed to **Evidence ladder** (read → edit → verify).
    - **No** → stop; use **discovery** skill to map the repo, or **planning** to lock
      tasks and acceptance criteria.

2. **Change touches a public API, DB migration, or cross-team contract?**
    - **Yes** → add an explicit **contract note** (request/response, migration rollback,
      feature flag) in the output; consider **Integrationist** + **planning** before
      merging.

3. **Change is a bugfix without a repro?**
    - **No repro** → use **debugging** skill first; implementation comes after a failing
      test or logged stack trace.

4. **Only tests or only prod code?**
    - Prefer **tests first** when fixing behavior (failing test → fix → green). If only
      docs/config, still list **verification** commands that prove validity (e.g. config
      parse, dry-run).

Document the branch you took in the **Output** section so reviewers and future agents
see why you did not explore other paths.

## Evidence ladder (strongest proof first)

Build confidence in this order; stop when the user’s risk level is satisfied:

1. **Failing test** (or new test) that demonstrates the bug or missing behavior.
2. **Typecheck / compile** for typed stacks.
3. **Linter** on touched paths (or project default).
4. **Targeted test run** (unit/integration) for changed modules.
5. **Full test suite** or CI parity when the change is broad or high-risk.
6. **Runtime smoke** (local server, CLI `--help`, sample request) when behavior is not
   fully covered by tests.

If a step cannot run (missing toolchain, long CI), record **why** and the **weakest
acceptable substitute** (e.g. static review + partial tests), never silent omission.

## Failure modes and responses

<!-- prettier-ignore-start -->
| Symptom                              | Likely cause        | Response                                                     |
|--------------------------------------|---------------------|--------------------------------------------------------------|
| Diff balloons across unrelated files | Scope creep         | Revert unrelated hunks; split follow-up tasks                |
| Tests pass locally, fail in CI       | Env, timing, OS     | Reproduce CI matrix or read logs; use **debugging**          |
| “Works” but behavior wrong           | Missing requirement | Add characterization test; re-read user goal                 |
| Merge conflicts after long branch    | Delayed integration | Smaller PRs; rebase early; **planning** for sequencing       |
| Performance regression               | Hot path change     | **Performance Investigator** subagent; baseline before/after |
| Secret in diff                       | Accidental commit   | Remove, rotate secret, **Security Reviewer** pattern         |
<!-- prettier-ignore-end -->

## Cross-stack notes

Apply only what matches the repository; do not invent stack-specific files.

- **JavaScript / TypeScript:** Match bundler, ESLint/Prettier, and module resolution
  (`import` vs `require`). Prefer explicit types at boundaries.
- **Python:** Follow existing typing discipline; virtualenv/poetry/uv as per repo;
  respect `ruff`/`black` if configured.
- **Ruby / Rails:** Follow framework conventions; keep migrations reversible; avoid N+1
  in hot paths.
- **Go:** Run `go fmt`; watch error wrapping patterns; small interfaces.
- **Rust:** `cargo fmt`/`clippy` if present; respect `unsafe` policy (escalate if
  unsure).
- **Mobile / native:** Platform toolchains and simulators may be heavy—document what you
  could not run.

When uncertain, **read** neighboring files and tests as the source of truth, not generic
style guides.

## Worked example A — Bugfix with regression test

**Situation:** User reports “export CSV truncates large rows.”

1. **Discovery:** Search for export/csv code path; read one caller test if any.
2. **Hypothesis:** Buffer size, streaming vs load-all, or string length limit.
3. **Implementation:** Add a **failing test** with a large payload that reproduces
   truncation; fix minimal code (e.g. stream rows instead of joining in memory).
4. **Verification:** Run module tests + quick manual export if feasible.
5. **Output:** List files, summarize fix mechanism, note any **API** or **memory**
   implications for **documentation** skill.

## Worked example B — Small feature behind flag

**Situation:** Add optional `?verbose=1` to an internal API for operators.

1. **Planning slice:** Confirm authz (operators only); default off.
2. **Implementation:** Parse query param; gate extra logging; avoid PII in verbose
   branch (**Security Reviewer** checklist).
3. **Verification:** Tests for on/off; lint; optional curl example in PR description
   (not committed secrets).
4. **Composes-with:** **documentation** for runbook snippet; **release** if flag must
   roll out coordinated.

## Worked example C — Config-only change

**Situation:** Increase worker concurrency in `docker-compose` or Helm values.

1. **Read** current comments and sibling services for conventions.
2. **Change** single value or small block; do not reshuffle unrelated keys.
3. **Verify:** Render chart (`helm template`) or validate YAML parser; note
   **operational** risk (memory).
4. **Hand off:** **incident-responder** playbook if production needs staged rollout.

## Composes-with (other skills and subagents)

- **planning** — Before large or ambiguous implementation; produces ordered tasks and
  verification.
- **discovery** — When you do not know where logic lives or how the repo builds.
- **testing** — When to add which tests, property tests, or flaky-test discipline beyond
  this skill’s verification ladder.
- **debugging** — When behavior is wrong but cause unknown; produces repro before
  speculative edits.
- **refactoring** — When the change is intentionally broad or structural; keep
  implementation slices small after plan approval.
- **documentation** — User-facing or operator-facing follow-up after behavior or flags
  change.
- **release** — Shipping, versioning, and rollout coordination after implementation is
  merged.

Subagents: **Architect** (boundaries), **Reviewer** (PR quality), **Security Reviewer**
(sensitive paths), **Integrationist** (external contracts), **Performance Investigator**
(latency/resource regressions).

## Progressive disclosure (Agent Skills)

- **At discovery:** Agents see only `name` + `description` in YAML—keep `description`
  accurate so the right tasks activate this skill.
- **At activation:** Load this full file; then open **repository files** and optional
  `references/` in this folder for team-specific checklists.
- **Optional layout** (per
  [Agent Skills layout](https://agentskills.io/what-are-skills)):

```text
implementation/
├── SKILL.md           # This file (required)
├── references/        # Optional: ADRs, coding standards excerpts
├── scripts/           # Optional: repo-specific verify.sh helpers
└── assets/            # Optional: templates, snippets
```

Do not duplicate long prose from `references/` inside `SKILL.md`—link or say “read
`references/STYLE.md` when editing frontend.”

## Execution checklist (during implementation)

- [ ] Goal and **non-goals** stated (or copied from user/plan).
- [ ] Files to touch **listed** before editing; scope frozen unless user expands.
- [ ] **Existing** patterns inspected in at least one neighboring file or test.
- [ ] **Minimal** diff; no unrelated renames or “cleanup.”
- [ ] **Imports** and **exports** updated; dead code not left behind without intent.
- [ ] **Errors** handled consistently with surrounding code (no silent catches unless
      local pattern).
- [ ] **Verification** run or explicitly skipped with reason.

## Output contract

Always end with:

**Files:** `path1`, `path2`, …

**Changes:** Short bullet summary tied to user intent (not a raw diff dump).

**Verification:** Commands run and outcomes; or “Not run:” with reason and residual
risk.

**Follow-ups:** Optional tasks for **testing**, **docs**, **release**, or other
skills/subagents.

## Trigger phrases

- “implement”, “patch”, “add a function”, “minimal change”, “fix this”, “wire up”,
  “small PR”

## Skill verification (meta)

- Touch list matches actual edited paths.
- Summary matches diff scope; no hidden scope.
- Verification section is honest; substitute evidence labeled as such.
- Handoffs named when out-of-scope work was deferred.

## Completion checklist (before you say “done”)

- [ ] User-visible behavior matches stated intent (or tests prove it).
- [ ] No secrets, tokens, or private URLs committed.
- [ ] Tests/lint/typecheck appropriate to change size were run or waived with reason.
- [ ] Rollback story clear for risky changes (flag, migration, config).
- [ ] Related skills/subagents notified in **Follow-ups** when work continues elsewhere.

## PR and review alignment

Implementation quality is judged twice: by **machines** (tests, linters) and by
**humans** (reviewers). Make reviewer work mechanical:

- **Commit narrative:** One logical change per PR when possible; if stacked, number
  branches and state dependencies in the description.
- **Risk callout:** Bullet “Risk:” with blast radius (who/what breaks if wrong).
- **Screenshots / logs:** Only when UI or CLI output changes materially; avoid noisy
  images for tiny tweaks.
- **Reviewer map:** If touching security-sensitive or high-churn files, @-mention or
  note **Security Reviewer** / **Architect** expectations in the PR text so the right
  eyes arrive early.

## When to pause and ask the user

Stop coding and ask rather than guessing when:

- Requirements **contradict** each other or existing behavior.
- **Business rules** are ambiguous (refunds, permissions, pricing).
- **Breaking change** is unavoidable and no migration path was agreed.
- You need **secrets** or **production-only** data you cannot access.

Record the question and **proposed default** so the user can approve in one reply.

## Metrics mindset (lightweight)

Not every change needs benchmarks. Use a proportionate bar:

- **Hot paths** (requests/sec, large batches): note before/after latency or throughput
  if you touched them; escalate to **Performance Investigator** if unsure.
- **Allocations** in tight loops: prefer measurements over intuition.
- **DB migrations:** estimate row counts and lock risk; point **release** skill at
  maintenance windows if needed.
