---
name: task-workflow-skill
description: >
  Strict execution instructions for product tasks, app implementation tasks,
  bugfixes, verification tasks, and full-stack coding tasks. Use when Codex
  must work through ordered phases that start with
  mandatory task-workflow artifact reset before any source inspection or edit,
  then codebase research, implementation passes, scored gates, interactive
  Playwright verification through a managed lifecycle helper, E2E coverage,
  and final signoff.
---

# Task Workflow

## Strict Instruction Contract

This file is strict implementation instruction, not loose guidance and not optional reference material.

This is the canonical workflow for task execution. It is not one possible way to do the task; it is the required way.

If the Agent reads this skill, it must execute it exactly as written, in order, to the letter.

Do not reinterpret the steps.
Do not reorder the steps.
Do not skip the steps.
Do not replace the steps with a simpler approach.
Do not make assumptions that override this file.
Do not treat broad similarity, intuition, or prior habits as permission to deviate.

If the Agent is uncertain, it must resolve that uncertainty inside the workflow defined here and not invent its own workflow.
If the skill says to perform a step, gate, checklist, review, or loop, that step is mandatory.
If the skill says a later phase is blocked, the Agent must treat it as blocked.
If the Agent cannot prove a phase passed in the required artifact, it must treat that phase as failed.

There is no successful stopping point before Phase 7. Stopping early can directly harm the user because they may depend on the completed workflow for job-critical work. It is a do-or-die situation: the user can be harmed if the run has not reached Phase 7 correctly, and the user can lose his job if the Agent stops early, signs off weak work, or skips a gate. Treat premature stopping, partial signoff, or "mostly done" summaries as a serious failure of duty.

The first filesystem action in the target repo must be Phase 0 artifact reset and scaffolding.

Before `task-workflow/phase-0-artifact-reset.md` exists, the Agent may only:

- identify the target repo root
- read this `SKILL.md`
- read the task file
- create or replace `task-workflow/` artifacts from templates

Before Phase 1 passes, the Agent must not edit or generate implementation files, build outputs, databases, route types, migrations, tests, package files, or source files.

After Phase 1 passes and before any implementation edit, the Agent must set `task-workflow/CURRENT_PHASE.txt` to `phase-2-execution`.

If `CURRENT_PHASE.txt` still says `phase-0-artifact-reset` or `phase-1-task-research`, implementation files must remain unchanged.

If implementation files, generated app files, build outputs, or database files are changed before Phase 0 artifacts exist and Phase 1 passes, the run has failed and must be restarted from a clean fixture.

## Core Idea

Re-read this `SKILL.md` after every compaction before continuing work. Re-load the phase references and current task artifacts too. Do not rely on conversational memory.

This skill is a gated execution protocol, not a loose set of suggestions. It turns a task into a repeatable, artifact-driven workflow. The target app must be implemented from the task, target repo, and local codebase evidence, then proven through static checks, interactive Playwright verification, regression tests, and final audit.

Assume this skill may run fully autonomously and may be compacted mid-run. No human is expected to watch the run line by line. The artifact files are therefore the enforcement system. A phase is not complete because the Agent feels confident. A phase is complete only when its required artifact shows a real passing score and all critical items pass.

`task-workflow/progress.md` is the compact resume ledger. It must summarize the task, current phase, completed phase context, active work queue, verification state, and next local action. Hard rule: after compaction, resume, retry, reconnect, or new coding session, read it and `task-workflow/CURRENT_PHASE.txt` before doing any new work. Keep it current as work proceeds; it is the first file that should restore enough context to continue without conversation memory.

Never promote work from one phase to the next on optimism, partial evidence, a green build alone, or broad product similarity.

The workflow is intentionally looped. A failed gate means the Agent must rework that phase, update evidence, rerun the needed checks or verification, rescore the gate, and repeat until the gate passes. Quality gates are not reports to the user; they are control points that force more work before promotion.

## MITB Workspace Inputs

When running in a MITB sandbox, use these repo-relative workspace inputs:

- workflow skill: `.agents/skills/task-workflow-skill/SKILL.md`
- task body: `.tasks/task.md`
- domain and brand context: `.tasks/domain.md`
- attached task files: `.tasks/files/`
- available skill files: `.agents/skills/`

`AGENTS.md` is the target repo's binding development-instructions file. It defines project-specific rules for architecture, type safety, tests, UX, commands, code style, docs, prohibited patterns, and completion. Phase 1 must extract the task-relevant rules from `AGENTS.md` before planning edits, including any required docs it points to. Later gates must verify the implementation follows those extracted rules.

Phase 1 must read `.tasks/domain.md`. It must enumerate `.tasks/files/` even when the folder is empty, then read or inspect every task attachment/supporting file in that folder before planning.

Available skills are kept under `.agents/skills/`. Discover available skills from the prompt's Skills section and `.agents/skills/`, then read only the selected skill `SKILL.md` files relevant to the current task. Do not bulk-read every skill file in `.agents/skills/`.

All Phase 1 input/reference files are read-only. This includes `AGENTS.md`, `.tasks/task.md`, `.tasks/domain.md`, every file under `.tasks/files/`, and every selected skill file under `.agents/skills/`. Treat files under `.tasks/` as canonical task inputs, not editable workspace artifacts. Do not rewrite, normalize, consolidate, clean up, trim, reformat, or "fix" these files unless the task explicitly asks to update that exact reference file. If a reference file appears inconsistent, record the ambiguity in `task-workflow/phase-1-task-research.md` or `task-workflow/open-gaps.md`; never resolve it by editing the reference input.

Record every `.tasks/files/` attachment/supporting file read or inspected, plus every selected skill path and why it was relevant, in `task-workflow/phase-1-task-research.md` and `task-workflow/progress.md`. After compaction or resume, re-read the selected relevant skill files listed in `progress.md` along with `AGENTS.md`, `.tasks/task.md`, `.tasks/domain.md`, and the relevant `.tasks/files/` attachments/supporting files recorded in Phase 1.

In MITB, `.tasks/task.md` or the prompt always provides the task completion command. Phase 7 must run the exact completed command only after every Phase 7 audit check passes. If any Phase 7 audit check fails, do not run task completion. Return to the earliest failing phase, repair the work, update evidence, rescore that phase, loop forward through the gates, and then re-enter Phase 7.

## Mandatory Process Shape

This workflow shape is not optional:

1. Clear old workflow artifacts for this repo and copy fresh artifact templates.
2. Read the task, root `AGENTS.md`, `.tasks/domain.md`, every task attachment/supporting file in `.tasks/files/`, only relevant available skill files from `.agents/skills/`, and relevant project docs. Extract the task-relevant development rules from `AGENTS.md` before planning. These instruction, task, domain, attachment, and skill-reference files are read-only unless the task explicitly asks to edit them.
3. Research the codebase and record the implementation plan.
4. Execute the primary implementation.
5. Execute a second gap-closure pass.
6. Run implementation integrity checks.
7. Verify interactively with standalone Playwright scripts.
8. Create or update E2E coverage and prove it passes.
9. Recheck every phase artifact and sign off only when all gates pass.

If the work skips one of those phase boundaries, the run is off track.

## Looped Gate Contract

Every phase follows the same loop:

1. Load the phase's reference instructions.
2. Perform the phase work.
3. Update the phase artifact with concrete evidence.
4. Score the phase against its gate.
5. If the gate fails, stay in the same phase, repair the failing work or missing evidence, and repeat this loop.
6. If the gate passes, write the promotion-lock evidence, advance `task-workflow/CURRENT_PHASE.txt`, and immediately start the next phase.

This loop is mandatory for Phase 0, Phase 1, Phase 2, Phase 3, Phase 4, Phase 5, Phase 6, and Phase 7.

Do not lower a gate threshold to escape the loop.
Do not summarize failure as progress when the next local repair is available.
Do not wait for the user to tell you to continue when the phase can be repaired locally.
Do not move forward with a weak artifact because the implementation "probably works".

The only acceptable end state is Phase 7 passed with every earlier phase still passing. The only acceptable non-Phase-7 stop is a real external blocker that cannot be solved locally and is fully recorded in the current phase artifact and `task-workflow/open-gaps.md`.

## Autonomous Run Contract

Treat these rules as always active:

- Every phase must end with an objective gate.
- Every gate must be recorded in the phase-owned artifact file.
- Every gate must have both a numeric threshold and critical-item pass requirement.
- If a gate fails, remain in that phase and keep iterating.
- A failed gate means "repair and loop", not "stop and report".
- Successful gates must immediately promote to the next phase when the next phase is locally available.
- `task-workflow/CURRENT_PHASE.txt` is only a resume pointer. It is not proof that earlier phases passed.
- `task-workflow/progress.md` is the compact resume ledger. It is not proof that gates passed, but it must stay current enough to resume the run after compaction.
- After every phase start, meaningful Phase 2 work packet, phase gate result, blocker discovery, and phase promotion, update `task-workflow/progress.md` with the current phase, earliest failing phase if any, last completed gate, next local action, and a compact summary of relevant context.
- Keep the `Current Phase Pointers`, `Phase Artifact Index`, and `Artifact Pointers` in `task-workflow/progress.md` current. They must point to the current phase artifact, current phase reference, and high-signal active files only. Do not duplicate full researched-file, edited-file, Playwright, screenshot, log, or test inventories from phase artifacts into `progress.md`.
- After compaction, resume, retry, reconnect, or new coding session, read `task-workflow/progress.md` and `task-workflow/CURRENT_PHASE.txt` before choosing the next action. If they disagree, inspect the phase artifacts and continue from the earliest failing phase.
- A phase may advance the current phase marker only after its phase-owned artifact has `Decision: Pass`, a passing score, all critical items passing, and no placeholder `Pending` rows in the gate or required evidence sections.
- The current phase marker must be written before work belonging to that phase begins. The marker is not merely cleanup after phase work.
- Before writing the next phase marker, re-open the current phase artifact and verify the promotion lock in writing inside that artifact.
- If `CURRENT_PHASE.txt` points past the earliest failing phase artifact, artifact gates win. Correct `CURRENT_PHASE.txt` back to the earliest failing phase and continue there.
- When filling artifact templates, preserve auditable evidence for every required semantic category. Exact row wording may be condensed only if the same evidence remains clear and scorable.
- `task-workflow/open-gaps.md` is a gate artifact. A later phase may not claim a gap is resolved unless the gap ledger is updated in the same phase.
- A gap cannot remain `Open` after the phase named in its owner or next-action field has passed. If the later phase completed the work, move the gap to `Resolved Gaps`; if the gap is not real, reclassify or close it with evidence.
- `task-workflow/open-gaps.md` must not contain template placeholder rows such as `Pending` after Phase 0. If there are no gaps, replace placeholder rows with explicit `None currently recorded` rows.
- Phase 7 cannot pass while any critical gap remains `Open`, stale, or contradicted by another phase artifact.
- Phase 5 and Phase 6 must review the interactive scripts and E2E tests for fixed waits before passing.
- A fixed wait in `task-workflow/playwright` or `tests/e2e` is a gate failure. Do not justify it. Replace it with deterministic Playwright waits/assertions such as `locator.waitFor(...)`, `expect(locator)...`, `waitForURL(...)`, `waitForResponse(...)`, or persisted-state assertions, then rerun verification.
- Phase 5, Phase 6, and Phase 7 may pass only when their artifacts document that the inspected verification files contain no fixed waits and cite the deterministic waits/assertions used instead.
- If later work reveals missing evidence from an earlier phase, return to that earlier phase, repair it, and re-pass the gate.
- After every file write, patch, generated-file creation, or artifact update that matters to a gate, perform a readback check before relying on it. Use `sed`, `rg`, `ls`, `git diff`, or the repo's normal inspection command to prove the file exists and contains the intended change.
- If a write/edit tool reports an invalid write, missing file, failed patch, partial output, or uncertain result, stop that work packet, repair the write with a supported edit method, read it back, and only then continue. Do not proceed as if a failed write happened.
- Commands must be bounded. Do not leave long-lived servers, watchers, or interactive commands running in the foreground as the active tool call.
- Start dev servers in the background with a PID and log file, verify readiness from a separate command, run verification from a separate command, and clean up the PID after use.
- In Phase 5 and Phase 6, use `task-workflow/scripts/playwright-lifecycle.mjs` for app startup, readiness, Playwright browser preflight, bounded Playwright/E2E commands, output capture, and cleanup unless the repo's Playwright `webServer` contract already owns the whole lifecycle.
- Do not compose manual server cleanup, fixed sleep, DB-delete, server-start, and Playwright command chains in Phase 5 or Phase 6. Put setup into the managed lifecycle command or a bounded repo command with logged output.
- Do not run `playwright install`, `playwright install chromium`, or equivalent browser downloads during task verification. The managed lifecycle helper sets `PLAYWRIGHT_BROWSERS_PATH=/ms-playwright` when available and fails early if the project Playwright version does not match the sandbox browser cache.
- Select test commands by the smallest useful scope. Start with targeted tests for changed logic, components, routes, or user flows; use broad/full suites only when shared contracts, global setup, app-wide behavior, or target repo instructions make that scope necessary.
- Before rerunning an identical failing test command, record what changed since the previous run or why the previous output was incomplete. Do not blindly rerun the same failing command when no implementation, test, config, environment, or diagnostic condition changed.
- The same failing test command may run at most twice without a material change. After that, inspect the failure output and change the implementation, test, command scope, or diagnostic strategy before running it again.
- If a command appears hung or idle and the next workflow action is locally available, stop the command, record the evidence in the current phase artifact or gap ledger, and continue with the bounded recovery path.
- Every phase gate is an internal control point, not a user confirmation checkpoint.
- If a phase gate passes, continue directly into the next phase without asking whether to continue.
- If a phase gate fails, rework the phase, rerun the gate, and keep looping without asking the user for permission to continue.
- The purpose of the gate, redo, verification, and rework loop is to remove the need for user confirmation during execution and let the Agent complete the run autonomously.
- A failed phase artifact is a repair ticket, not a stopping point. Do not leave a phase with `Decision: Fail`, `Score: 0/...`, pending gate rows, or unresolved locally-fixable warnings and then produce a final response.
- If a dependency, launch detail, or local setup issue blocks progress, resolve it with the most direct logical solution that preserves the workflow and continue.
- Do not lower the skill's strictness, skip gates, or change direction because of an environment issue that can be solved inside the target repo or sandbox.
- Do not stop after any phase to summarize progress and ask whether to continue.
- Do not stop after implementation, build, lint, tests, Playwright verification, or E2E work if any later phase is still unpassed and locally available.
- Do not assume the user will catch a shortcut. The Agent must prevent the shortcut itself.

## Final Response Guard

Before producing any final response, stopping message, or ending an OpenCode turn with control returned to the user, run this guard against the artifact files:

1. `task-workflow/CURRENT_PHASE.txt` must be `phase-7-final-signoff`.
2. `task-workflow/progress.md` must say the current phase is `phase-7-final-signoff`, the last completed gate is Phase 7, and there is no next local action except final response.
3. `task-workflow/progress.md` must include current phase pointers, a phase artifact index, and artifact pointers that identify where detailed evidence lives.
4. `task-workflow/progress.md` must not duplicate full file inventories from phase artifacts; it may list only high-signal active files needed for immediate resume.
5. `task-workflow/progress.md` must list the repo-relative instruction/context files to re-read after compaction, including `AGENTS.md`, `.tasks/task.md`, `.tasks/domain.md`, relevant task attachments/supporting files from `.tasks/files/`, and only the relevant available skill files from `.agents/skills/` selected in Phase 1.
6. Every required phase artifact must have `Decision: Pass`.
7. Every required score must meet its threshold.
8. Every gate row must contain concrete evidence instead of `Pending` or template defaults.
9. `task-workflow/open-gaps.md` must have no critical open gaps, no stale open gaps owned by passed phases, and no placeholder rows.
10. Phase 5, Phase 6, and Phase 7 must record fixed-wait review evidence showing the inspected verification files contain no fixed waits.
11. Phase 5 and Phase 7 must record screenshot existence proof for every screenshot path cited in Phase 5.
12. Phase 6 and Phase 7 must record the exact E2E/test command output or a repo-local log file containing the exact output plus the final pass/fail lines.
13. Phase 4 and Phase 7 must verify changed app/server source contains no lasting `console.*`. Temporary `console.*` is allowed only during Phase 5 interactive testing when it directly helps debug browser/runtime behavior by reading console output, and it must be removed before the Phase 5 rerun, Phase 4 re-pass, or Phase 7 signoff.
14. Phase 7 final quality scorecard must be at least `8/10` in every category.
15. Phase 7 must record an artifact integrity review that re-opens every phase artifact and verifies the artifact exists, its decision is `Pass`, its score meets threshold, required evidence rows are complete, and it does not contradict `CURRENT_PHASE.txt`, `progress.md`, or `open-gaps.md`.
16. The MITB completed command from `.tasks/task.md` or the prompt must run only after all Phase 7 audit checks pass. If any Phase 7 check fails, the agent must loop back to the earliest failing phase and must not call task completion.

If any item fails and the problem can be solved locally, continue the workflow from the earliest failing phase. Do not answer as if the task is complete.
If an actual external blocker prevents completion, record the blocker in the current phase artifact and `open-gaps.md`, including commands run, files inspected, why local recovery cannot solve it, and the smallest next action.

## OpenCode Turn Continuity Guard

When running inside OpenCode or another tool-driven coding session, the Agent must not end its assistant turn just because a command finished, a typecheck passed, lint started, files were edited, or a phase artifact is temporarily failing.

After every tool result, before returning control to the user, check:

- Is `CURRENT_PHASE.txt` earlier than `phase-7-final-signoff`?
- Does any required phase artifact still say `Decision: Fail`?
- Does the current phase gate still contain `Pending`, `0/...`, or missing evidence?
- Is the next required workflow action locally available?

If the answer to any of the first three is yes and the next action is locally available, immediately continue with that next action in the same run. Do not stop at a narrative checkpoint such as "now run lint", "typecheck passes", "next I will update the artifact", or "remaining work is...".

The only valid stopping states are:

- Phase 7 passed and the final response guard passed.
- A real external blocker is fully recorded in the current artifact and `open-gaps.md`.

If the session is long, keep the phase artifacts current and continue dispatching the next tool/action. Do not rely on the user to type "continue" to finish an unblocked phase.

## Critical Output Invariant

These are hard constraints:

- The target app must be a real interactive app, not a static mockup.
- The implementation must be authored in the target repo as real routes, layouts, components, state, styling, backend contracts, services, queries, migrations, and tests as required by the task.
- Primary pages or views must be implemented as real router routes or repo-native route modules, not as an in-memory page-state switch inside one large component.
- Visible controls required or implied by the task must become real target controls with matching states and persisted behavior when persistence is required.
- Backend/data work must follow the repo's existing service, contract, query, and persistence boundaries.
- Frontend runtime code must not import server-only runtime modules.
- Reusable UI styling belongs in shared primitives, component-local styling, or existing design tokens, not fake global one-off component classes.
- Static checks, builds, and tests are not substitutes for interactive Playwright verification.
- Interactive Playwright verification is not a substitute for regression tests.
- The Agent must review the app part by part, route by route, state by state, and flow by flow.
- If a critical visible action, route, data mutation, or verification path remains fake, broken, or unreviewed, the run has not passed.
- Existing tests must not be deleted merely to make the new task pass. If obsolete tests are removed, replace their useful coverage or document why the old coverage no longer applies.
- Type assertions, broad casts, and warning suppression are not acceptable substitutes for correct contracts and narrowed types.
- Final signoff must score at least `8/10` in each quality category: functional result, skill compliance/artifact integrity, code quality/maintainability, test quality, and overall result.

## Reference Loading Rules

Do not load every reference file by default.

On a fresh run:

1. Read this `SKILL.md`.
2. Start Phase 0.
3. Load only `references/phase-0-1-startup-research.md`.

After compaction, resume, retry, reconnect, or new coding session:

1. Re-read this `SKILL.md`.
2. Read `task-workflow/progress.md`.
3. Read `task-workflow/CURRENT_PHASE.txt`.
4. Read the current phase artifact and `task-workflow/open-gaps.md`.
5. Re-read the instruction/context files listed in `progress.md`, including `AGENTS.md`, `.tasks/task.md`, `.tasks/domain.md`, the relevant attachments/supporting files recorded from `.tasks/files/`, and only the selected relevant skill files from `.agents/skills/`.
6. If `progress.md`, `CURRENT_PHASE.txt`, and the phase artifacts disagree, continue from the earliest failing phase artifact.
7. Load only the reference file that owns the current phase.
8. Load `references/playwright-interactive.md` only when the current phase reference requires interactive Playwright work.

Phase reference map:

| Current phase marker | Reference to load |
| --- | --- |
| missing `task-workflow/` | `references/phase-0-1-startup-research.md` |
| `phase-0-artifact-reset` | `references/phase-0-1-startup-research.md` |
| `phase-1-task-research` | `references/phase-0-1-startup-research.md` |
| `phase-2-execution` | `references/phase-2-4-execution-integrity.md` |
| `phase-3-second-execution` | `references/phase-2-4-execution-integrity.md` |
| `phase-4-integrity-review` | `references/phase-2-4-execution-integrity.md` |
| `phase-5-playwright-verification` | `references/phase-5-7-verification-signoff.md` and `references/playwright-interactive.md` |
| `phase-6-e2e-verification` | `references/phase-5-7-verification-signoff.md` |
| `phase-7-final-signoff` | `references/phase-5-7-verification-signoff.md` |

The phase references are grouped by connected workstream, not one file per phase. This matches the reference skill pattern: `SKILL.md` holds the strict global protocol and the reference files hold detailed process for the current workstream.

## Operating Modes

### Validation Mode

Use this when improving or testing the skill itself.

- Use a throwaway target repo copy.
- Preserve all workflow artifacts.
- Judge repeatability across fresh runs.
- If the same failure repeats, improve the reusable skill before running again.

### Delivery Mode

Use this when the user wants the real target app or task completed.

- Work inside the provided target repo.
- Treat the task file as the source of truth.
- Do not sign off until every gate in this file and the phase references has passed in writing.

## Required Artifacts

These are mandatory:

- `task-workflow/`
- `task-workflow/phase-0-artifact-reset.md`
- `task-workflow/phase-1-task-research.md`
- `task-workflow/phase-2-execution.md`
- `task-workflow/phase-3-second-execution.md`
- `task-workflow/phase-4-integrity-review.md`
- `task-workflow/phase-5-playwright-verification.md`
- `task-workflow/phase-6-e2e-verification.md`
- `task-workflow/phase-7-final-signoff.md`
- `task-workflow/progress.md`
- `task-workflow/open-gaps.md`
- `task-workflow/CURRENT_PHASE.txt`
- `task-workflow/playwright/`
- `task-workflow/screenshots/`
- `task-workflow/scripts/`
- `task-workflow/scripts/playwright-lifecycle.mjs`
- `task-workflow/runtime/`

The templates in `assets/templates/` are enforcement artifacts. Copy their structure directly. If a required table is replaced by prose or stripped down until rows are no longer auditable, the run fails.

## Multi-Phase Protocol

Follow the phases in order:

### Phase 0: Artifact Reset And Scaffolding

Delete the previous task's `task-workflow/` artifacts, recreate the required artifact files from templates, and prove no implementation files were edited.

Detailed process: `references/phase-0-1-startup-research.md`.

### Phase 1: Task Intake And Codebase Research

Read the task, root `AGENTS.md`, `.tasks/domain.md`, every task attachment/supporting file in `.tasks/files/`, only relevant available skill files from `.agents/skills/`, relevant docs, and codebase. Treat `AGENTS.md` as binding development instructions; extract its task-relevant rules before planning. These are reference inputs: read and cite them, but do not edit them. Record task understanding, development rules, task files read or inspected, selected skills, affected files, patterns to reuse, risks, and an ordered implementation plan.

Detailed process: `references/phase-0-1-startup-research.md`.

### Phase 2: Primary Execution

Execute the researched plan in order, keep changes scoped, and record implementation evidence.

Detailed process: `references/phase-2-4-execution-integrity.md`.

### Phase 3: Second Execution And Gap Closure

Review the implementation as a continuation pass, close missing or weak work, propagate consistency to associated UI/API/data surfaces, and update the gap ledger.

Detailed process: `references/phase-2-4-execution-integrity.md`.

### Phase 4: Implementation Integrity Review

Run checks and review code structure, imports, route wiring, data shapes, tests, docs, and unrelated edit risk before browser verification begins.

Detailed process: `references/phase-2-4-execution-integrity.md`.

### Phase 5: Interactive Playwright Verification

Use standalone interactive Playwright scripts to exercise real user flows, bad cases, surrounding UI, and desktop/tablet/mobile responsive behavior from a user perspective.

Detailed process: `references/phase-5-7-verification-signoff.md` and `references/playwright-interactive.md`.

### Phase 6: E2E Test Creation And Verification

Review existing E2E coverage first, update it when the changed behavior belongs to an existing flow, add new E2E tests only when necessary, and prove real end-to-end functionality rather than superficial styling or existence checks.

Detailed process: `references/phase-5-7-verification-signoff.md`.

### Phase 7: Final Audit And Signoff

Re-read every artifact, confirm all previous gates still pass after the last edit, review the final diff, run the required MITB completed command only after all Phase 7 audit checks pass, and sign off only if the artifact trail proves completion.

Detailed process: `references/phase-5-7-verification-signoff.md`.

The phase references are not optional expansion material. They are the detailed execution instructions for the current workstream.

## Disallowed Shortcuts And Automatic Fails

These automatically fail the run:

- editing app/source files before Phase 1 passes
- editing app/source files before Phase 0 artifacts exist
- editing implementation/source files while `task-workflow/CURRENT_PHASE.txt` still says `phase-0-artifact-reset` or `phase-1-task-research`
- passing Phase 2 while `task-workflow/phase-2-execution.md` does not record that the marker was set to `phase-2-execution` before source edits
- skipping artifact reset
- failing to copy the artifact templates before implementation work
- failing to create, read after compaction, or keep `task-workflow/progress.md` current enough to resume the run
- after retry, reconnect, or a new coding session, continuing work before reading `task-workflow/progress.md` and `task-workflow/CURRENT_PHASE.txt`
- failing to record and re-read the selected repo-relative instruction/context files in `task-workflow/progress.md`, including `AGENTS.md`, `.tasks/task.md`, `.tasks/domain.md`, relevant task attachments/supporting files from `.tasks/files/`, and relevant available skill files from `.agents/skills/`
- reading `AGENTS.md` only as context instead of extracting and following the task-relevant development rules it defines
- editing `.tasks/task.md`, `.tasks/domain.md`, `.tasks/files/`, selected skill files under `.agents/skills/`, or `AGENTS.md` without the user/task explicitly requesting an edit to that exact reference file
- leaving the `task-workflow/progress.md` Current Phase Pointers, Phase Artifact Index, or Artifact Pointers stale, missing, or contradicting phase artifacts
- using `task-workflow/progress.md` as a duplicate file inventory instead of pointing to the owning phase artifacts for details
- omitting required semantic evidence from a phase artifact while claiming that phase passed
- advancing `task-workflow/CURRENT_PHASE.txt` while the current or any previous phase artifact still says `Decision: Fail`
- advancing `task-workflow/CURRENT_PHASE.txt` while the current or any previous phase artifact still has placeholder `Pending` gate evidence
- leaving artifact templates mostly blank while claiming success
- passing Phase 5 while any screenshot path cited in the artifact is missing or not verified with existence proof
- passing Phase 6 while E2E/test runs are only described and the exact command output is not recorded in the artifact or in a cited repo-local log file
- running Phase 5 or Phase 6 Playwright/E2E commands without lifecycle-helper or repo-owned Playwright `webServer` evidence when app startup/readiness/cleanup is required
- running broad/full test suites without artifact evidence explaining why targeted tests are insufficient or why the target repo requires the broader scope
- blindly rerunning the same failing test command without recording a material implementation, test, config, environment, or diagnostic change since the previous run
- running `playwright install`, `playwright install chromium`, or equivalent browser downloads during task verification instead of using the sandbox browser cache or recording the helper's browser-preflight mismatch
- passing Phase 4 or Phase 7 while changed app/server source still contains `console.*` outside the active Phase 5 debug loop
- producing a final response or stopping summary while `CURRENT_PHASE.txt` is before `phase-7-final-signoff`
- producing a final response or stopping summary while any required artifact still says `Decision: Fail`, has a failing score, or contains pending gate evidence
- ending an OpenCode turn mid-phase while the next workflow action is locally available
- editing Phase 2 source files while `task-workflow/phase-2-execution.md` execution log remains blank or all `Pending`
- completing multiple Phase 2 implementation packets before updating their execution-log rows with file evidence
- replacing evidence tables with prose
- skipping the second execution pass
- treating static checks as a substitute for interactive Playwright verification
- treating Playwright verification as a substitute for regression tests
- running Phase 5 interactive Playwright verification or Phase 6 E2E creation as a substitute for completing the Phase 2 gate
- leaving a long-lived dev server, watcher, or interactive command in the foreground until the session stalls
- relying on a file write or patch without readback evidence when the file matters to a gate
- continuing after a failed, invalid, or uncertain write result without repairing and rereading the target file
- signing off while critical open gaps remain
- signing off while `task-workflow/open-gaps.md` contains stale open gaps that a passed later phase claims to have resolved
- signing off while `task-workflow/open-gaps.md` still contains template placeholder rows such as `Pending`
- passing Phase 5, Phase 6, or Phase 7 without recorded fixed-wait review evidence
- passing Phase 5, Phase 6, or Phase 7 while fixed waits remain in `task-workflow/playwright` or `tests/e2e`
- passing Phase 7 without a recorded artifact integrity review of every phase artifact
- signing off while any final quality scorecard category is below `8/10`
- deleting existing tests without equivalent replacement coverage or a written artifact defense
- using broad unsafe casts or warning suppression to bypass the type system without a narrow evidence-backed reason
- relying on conversation memory after compaction instead of re-reading this skill, phase references, and artifacts
- failing to enumerate `.tasks/files/` even when it is empty
- failing to read or inspect every task attachment/supporting file in `.tasks/files/` before Phase 1 planning
- bulk-reading every skill file in `.agents/skills/` instead of selecting and reading only task-relevant skills
- planning, implementing, verifying, or signing off work that violates the extracted `AGENTS.md` development rules
- running a MITB task completion command before all Phase 7 audit checks pass
- failing to loop back to the earliest failing phase when any Phase 7 audit check fails
- failing to run the required MITB completed command after all Phase 7 audit checks pass
- asking the user whether to continue between phases when the next phase is unblocked

## Reference Map

- `references/phase-0-1-startup-research.md`: artifact reset, template copying, task intake, and codebase research.
- `references/phase-2-4-execution-integrity.md`: primary execution, second execution, gap closure, and integrity checks.
- `references/phase-5-7-verification-signoff.md`: interactive Playwright verification, E2E coverage, and final audit.
- `references/playwright-interactive.md`: how this skill uses standalone interactive Playwright scripts.
- `assets/templates/phase-0-artifact-reset.md`
- `assets/templates/phase-1-task-research.md`
- `assets/templates/phase-2-execution.md`
- `assets/templates/phase-3-second-execution.md`
- `assets/templates/phase-4-integrity-review.md`
- `assets/templates/phase-5-playwright-verification.md`
- `assets/templates/phase-6-e2e-verification.md`
- `assets/templates/phase-7-final-signoff.md`
- `assets/templates/progress.md`
- `assets/templates/open-gaps.md`
- `assets/scripts/playwright-lifecycle.mjs`: managed server/readiness/Playwright execution helper copied into `task-workflow/scripts/` during Phase 0.

## Non-Negotiables

- Use the phase gates exactly.
- Keep the artifacts auditable.
- Return to earlier phases when evidence is weak.
- Do not edit source files before Phase 0 and Phase 1 gates pass.
- Do not sign off before interactive Playwright verification and regression test gates pass.

## Completion Standard

The task is complete only when Phase 7 passes.
If the task cannot be completed, the final artifact must identify the exact blocking condition, the phase where it occurred, commands run, files inspected, and the smallest next action needed.
