---
name: rust-cli
description: 'Umbrella guide for the rust-cli skill family: route Rust CLI Skill work through intake, description, scaffolding, feature extension, validation, and publish/release while preserving the constitution, package layout contract, and packaging boundaries.'
---

# rust-cli

Use this umbrella skill when you need one entrypoint for the full rust-cli
development workflow and want to resume from the current stage instead of
re-reading every operation document from scratch.

This file is the router and shared contract for the rust-cli skill family. The
phase-specific skills under `stages/` hold the stage instructions. Treat
`constitution.md`, `instructions/*.md`, and the release runbook assets as the
canonical detailed references.

## Phase Skill Family

| Phase skill                                                    | Use it when                                                                                                                                                                                  | Canonical references                                                                                                                                                                                                                                         | Primary outcome                                                                                                                                      |
| -------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`rust-cli-intake`](stages/rust-cli-intake/SKILL.md)           | You need to classify the work as scaffold, extend, validate, or publish; confirm required inputs; and load the shared rules before changing a project.                                       | [`constitution.md`](constitution.md), [`instructions/new.md`](instructions/new.md), [`instructions/add-feature.md`](instructions/add-feature.md), [`instructions/validate.md`](instructions/validate.md)                                                     | The next stage is selected with the required inputs assembled.                                                                                       |
| [`rust-cli-description`](stages/rust-cli-description/SKILL.md) | The workflow needs one authoritative description contract before scaffold, extend, validate, or publish surfaces change.                                                                     | [`instructions/new.md`](instructions/new.md), [`instructions/add-feature.md`](instructions/add-feature.md), [`constitution.md`](constitution.md)                                                                                                             | The approved purpose summary, positioning statement, and downstream description surfaces are aligned.                                                |
| [`rust-cli-scaffold`](stages/rust-cli-scaffold/SKILL.md)       | You are creating a new Rust CLI Skill project from this package and already have an approved description contract from the earlier `description` stage.                                      | [`instructions/new.md`](instructions/new.md), [`constitution.md`](constitution.md)                                                                                                                                                                           | A new scaffolded project exists, reuses the approved description contract, and is ready for validation.                                              |
| [`rust-cli-extend`](stages/rust-cli-extend/SKILL.md)           | You are adding `stream` or `repl` support to an existing scaffolded project.                                                                                                                 | [`instructions/add-feature.md`](instructions/add-feature.md), [`constitution.md`](constitution.md)                                                                                                                                                           | The requested feature is added without breaking the shared runtime contract.                                                                         |
| [`rust-cli-validate`](stages/rust-cli-validate/SKILL.md)       | You need to audit an existing project, or you have just scaffolded or extended one and need a compliance report.                                                                             | [`instructions/validate.md`](instructions/validate.md), [`constitution.md`](constitution.md)                                                                                                                                                                 | A validation report states whether the project is compliant, usable with warnings, or blocked by errors.                                             |
| [`rust-cli-publish`](stages/rust-cli-publish/SKILL.md)         | You are closing the workflow after validation, preparing a release, rehearsing the destination mirror, checking destination configuration, or following the supported real publication path. | [`docs/release/skill-release-runbook.md`](docs/release/skill-release-runbook.md), [`.github/workflows/release.yml`](.github/workflows/release.yml), [`release/skill-release.config.json`](release/skill-release.config.json), [`package.json`](package.json) | The package ends in `report_only`, dry-run review, rehearsal, or the supported GitHub Actions release path with the right destination configuration. |

## Shared Guardrails

- Treat `constitution.md` as the top-level ruleset whenever an instruction file
  leaves room for interpretation.
- Reuse `instructions/new.md`, `instructions/add-feature.md`, and
  `instructions/validate.md` as the source of truth for detailed step lists,
  exact checks, and file-level expectations.
- Preserve the shared runtime contract in every generated or modified project:
  plain-text `--help`, structured `help`, stable structured errors,
  user-scoped runtime directories, and the Active Context surface.
- Keep one approved description contract across Cargo metadata, `SKILL.md`,
  README, help text, and publish-facing summaries. The `description` stage owns
  that contract.
- Keep the generated package layout explicit: generated skills may include
  package-local packaging-ready metadata or support fixtures when a supported
  capability requires them, but repository-owned CI workflows, release scripts,
  and release automation remain outside generated skill outputs.
- Do not invent workflows beyond the package's supported capability boundary:
  create a new project, extend it with `stream` or `repl`, validate it, or
  publish it through the documented release assets.
- When resuming work, return to the earliest incomplete stage instead of
  stacking new work on top of a broken scaffold.
- After scaffolding or extending a project, finish with validation before
  reporting the work as complete.
- Treat local `release:dry-run`, exact-mirror rehearsal, and the real GitHub
  Actions release workflow as different stages of confidence. Do not describe
  a local dry run or rehearsal as if it performed the production publish.

## Stage Selection

Choose the phase skill using the user request plus the current project state:

1. Use `intake` when the request is ambiguous, when inputs are incomplete, or
   when you need to decide whether the work is `new`, `extend`, `validate`, or
   `publish`.
2. Use `description` after `intake` whenever the work creates a new generated
   skill or changes the generated skill's user-facing contract.
3. Use `scaffold` when the user wants a brand-new Rust CLI Skill project and no
   valid project directory exists yet for that work, after the `description`
   stage has approved the description contract.
4. Use `extend` when a scaffolded project already exists and the user wants to
   add `stream` or `repl`, or when description-impacting work must continue
   into feature changes after the `description` stage.
5. Use `validate` when the user explicitly asks for compliance checking, or
   after scaffold/extend work to verify the result.
6. Use `publish` when validation has succeeded and the workflow needs its final
   closure, or when the user explicitly wants a release, a release dry run, a
   destination-config check, or an exact-mirror rehearsal.

If more than one phase seems plausible, inspect the target directory and route
to the earliest stage that is not clearly complete.

Successful validation still routes into `publish` by default. When the user did
not ask for release side effects, `publish` becomes a report-first closure
stage instead of stopping at `validate`.

## Resume Rules

- If the target project directory does not exist yet, resume at `scaffold`.
- If the directory exists but is missing the core scaffolded files required by
  `instructions/add-feature.md`, do not force feature work through; return to
  `scaffold` or treat the project as not ready for extension.
- If the directory exists and the request is to add `stream` or `repl`, resume
  at `extend`.
- If the project was just scaffolded or extended, always continue into
  `validate`.
- If the user wants a release but the latest substantive change has not been
  validated yet, return to `validate` before entering `publish`.
- If validation is current and no explicit release action was requested, still
  continue into `publish` so the workflow ends with `report_only` readiness or
  no-publish closure.
- If validation is already current and the work is about `release:dry-run`,
  destination configuration, rehearsal, or the documented release path, resume
  at `publish`.
- If validation exposes structural issues that prevent later work from being
  trustworthy, step back to the phase that owns the failing surface and fix it
  there before re-running validation.

## Routing Examples

- New project request: route `intake` -> `description` -> `scaffold` ->
  `validate` -> `publish` when no project directory exists yet.
- Feature extension request: route `intake` -> `extend` -> `validate` ->
  `publish` when the target project exists and the requested feature is
  `stream` or `repl`, unless the request also changes the public description
  contract.
- Description-impacting update request: route `intake` -> `description` ->
  `extend` -> `validate` -> `publish` when an existing generated skill changes
  purpose, positioning, or user-facing contract.
- Validation-oriented request: route `intake` -> `validate` -> `publish` when
  the user wants an audit or a post-change compliance pass.
- Publish-oriented request: route `intake` -> `publish` only when validation is
  current; otherwise send the workflow back through `validate` first.
- Ambiguous mixed request: choose the earliest incomplete stage instead of
  skipping ahead to a later phase mentioned in the same prompt.

## End-to-End Flow

Typical development flows are:

1. New project: `intake` -> `description` -> `scaffold` -> `validate` -> `publish`
2. Add feature: `intake` -> `extend` -> `validate` -> `publish`
3. Description-impacting update: `intake` -> `description` -> `extend` -> `validate` -> `publish`
4. Release preparation: `intake` -> `validate` -> `publish`
5. Validation-only audit: `intake` -> `validate` -> `publish`

Move across phases without pausing unless the current phase needs missing user
inputs or hits a blocking precondition that cannot be resolved from the repo.

## Shared Artifacts

Carry these references across phases:

- [`constitution.md`](constitution.md)
- [`instructions/new.md`](instructions/new.md)
- [`instructions/add-feature.md`](instructions/add-feature.md)
- [`instructions/validate.md`](instructions/validate.md)
- [`docs/release/skill-release-runbook.md`](docs/release/skill-release-runbook.md)
- [`.github/workflows/release.yml`](.github/workflows/release.yml)
- [`release/skill-release.config.json`](release/skill-release.config.json)
- [`package.json`](package.json)
- the target project path, if one exists
- the selected optional feature, if the work is an extension
- the validation report from the latest pass

Each phase may recover missing state from the filesystem, but it should prefer
already known paths and user-confirmed intent when available.
