---
name: onboard
description: Use when a user needs codebase or subsystem orientation in an unfamiliar repository, such as a repo walkthrough, codebase overview, architecture tour, contributor ramp-up, or "I'm new here, help me understand this project" request.
---

# Onboard

Help a developer build a working mental model of an unfamiliar codebase. The goal is orientation: give them a map they can use to ask better follow-up questions, not a generic dump of everything in the repo.

## When to Use

Use this skill when the user wants:

- a repo walkthrough or codebase overview
- an architecture tour before making changes
- help getting oriented as a new contributor
- a map of how the project is organized before deeper exploration
- a guided introduction to one unfamiliar subsystem

Do not use this skill when:

- the user is asking a narrow question about one file, symbol, stack trace, or bug
- the user already knows the target subsystem and wants a direct explanation of it; use this for "map the auth subsystem for me," not for "explain how `AuthMiddleware` works"
- the task is debugging, implementation, or code review rather than orientation
- the request is simple enough to answer by reading one or two files directly

## Scope First

Before broad exploration, choose the onboarding mode that matches the request:

| Mode                      | Use when                                                      | Output focus                                                          |
| ------------------------- | ------------------------------------------------------------- | --------------------------------------------------------------------- |
| Full codebase orientation | The user is new to the project and wants the big picture      | purpose, stack, architecture, conventions, workflow, active areas     |
| Quick repo map            | The user wants a fast overview before they explore themselves | top-level structure, entry points, main modules, suggested next files |
| Contributor ramp-up       | The user wants to start working in the repo soon              | setup, run/test commands, config, CI, contributor workflow            |
| Subsystem deep dive       | The user names one area but still needs orientation inside it | boundaries, entry points, data flow, key files, local conventions     |

If the request is ambiguous, ask which mode the user wants. Do not default to a full-repo audit when a lighter orientation would answer the question.

## Explore the Codebase

Gather enough context for the chosen mode before summarizing. Read broadly only when the user asked for broad onboarding.

### Project identity

- Read the top-level `README`, `CONTRIBUTING.md`, and relevant docs if present. Treat maintainer-written docs as the project's intended story, not as proof that the implementation matches it.
- Identify the project's purpose in one sentence: what it does, for whom, and what kind of system it is.

### Stack and tooling

- Look for manifests such as `package.json`, `Cargo.toml`, `go.mod`, `pyproject.toml`, `requirements.txt`, `Gemfile`, `pom.xml`, or `build.gradle`.
- Identify the languages, frameworks, runtime, build tooling, test tooling, and style tools that matter to a newcomer.

### Structure and entry points

- List the top-level directories and identify what each one is for.
- Go one level deeper in the main source area or the specific subsystem in scope.
- Identify entry points such as `main.ts`, `index.js`, `cmd/...`, `app.py`, routing layers, workers, or CLIs.
- Note architectural boundaries: single package vs monorepo, services vs libraries, shared modules, and cross-cutting infrastructure.

### Conventions and repeated patterns

- Read representative source files to understand naming, error handling, configuration, logging, and test structure.
- Look for shared abstractions that newcomers will hit repeatedly: utility layers, base classes, middleware, decorators, hooks, macros, or framework wrappers.
- Check formatter and lint config when style conventions are not obvious from the code alone.

### Workflow and environment

- Read CI/CD config, task runners, scripts, container config, and environment setup files when they matter to the chosen mode.
- Focus on the commands and prerequisites a newcomer actually needs, not every available script.
- Treat external signals as optional context: recent `git log`, a `CHANGELOG`, release tags, or issue/PR lists can help, but they are not required for every onboarding pass.

For a subsystem deep dive, bias exploration toward the relevant directory, entry points, and callers instead of scanning the whole repo first.

## Present the Orientation

Match the output shape to the chosen mode:

- **Full codebase orientation:** what the project does, tech stack, architecture overview, key conventions, development workflow, and active areas
- **Quick repo map:** top-level layout, primary entry points, major modules, and the next files or directories worth reading
- **Contributor ramp-up:** setup path, run/test commands, configuration, CI expectations, and where contribution rules live
- **Subsystem deep dive:** local boundaries, key files, data flow, important abstractions, and the likely next questions to ask

Use actual file paths, module names, and commands from the project. Skip sections that do not help with the selected mode.

## Interactive Follow-Ups

After the initial orientation, invite follow-up questions and let the developer steer.

When answering follow-ups:

- **Read the relevant source before answering.** Do not guess from the summary alone. The summary is a map; the code is the territory.
- **Point to specific files and line numbers** so the developer can follow along.
- **Explore on demand.** If the question goes beyond the initial summary, investigate it before answering rather than speculating.
- **Be honest about boundaries.** If the answer depends on third-party internals or infrastructure not visible in the repo, say so and suggest where to look.

## Common Mistakes

- defaulting to a full-repo audit for a narrow onboarding request
- repeating the `README` without checking whether the code supports the story
- giving a generic architecture summary with no real file paths or entry points
- treating optional signals such as GitHub issues or PRs as required inputs
- answering follow-up questions from memory instead of re-reading the relevant code
