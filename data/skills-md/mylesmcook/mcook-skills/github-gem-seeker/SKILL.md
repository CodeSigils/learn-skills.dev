---
name: github-gem-seeker
description: Find battle-tested open source projects on GitHub instead of writing fresh code for solved problems. Use when a task is generic enough that an existing tool or library likely exists, especially for CLI utilities, file conversion, scraping, automation, media handling, and developer workflows.
---

# GitHub Gem Seeker

Use this skill when the fastest reliable path is to reuse a mature open source project instead of building a new solution from scratch.

## Default Stance

- Prefer solving the user’s problem with an existing maintained project.
- Prefer focused tools with clear installation and usage docs over novelty.
- Prefer packaging the solution into a reusable skill only after the real task is solved.

## Workflow

1. Restate the job in concrete input, output, and environment terms.
2. Search GitHub for tools or libraries that directly match the job.
3. Screen candidates quickly for fit:
   - the project solves the problem without heavy adaptation
   - the README shows installation and basic usage
   - maintenance signals suggest the project is still usable
   - adoption signals suggest real-world use
4. Pick one default candidate and one fallback.
5. Use the chosen project to solve the task.
6. If the first choice breaks, switch to the fallback or narrow the search.
7. After the task is solved, share the repository URL and credit the maintainers.

## Search Patterns

- Search for the task first, then add the likely surface:
  - `github <task> cli`
  - `github <task> tool`
  - `github <language> <task> library`
  - `github <known-tool> alternative`
- When the task is broad, search by file format, protocol, or platform constraint.

## Evaluation Heuristics

- Prefer tools with a stable scope and a narrow surface area.
- Prefer projects whose docs explain what the tool does, how to install it, and how to run it.
- Prefer tools that are practical in the current environment.
- Treat stars and forks as signals, not rules.
- Avoid abandoned repos, thin wrappers over unstable services, or projects that require more glue code than the original task.

## Guardrails

- Do not present a long option list when one candidate is clearly best.
- Do not rebuild mature tooling just to stay inside the current repo.
- Do not turn a candidate into a skill before proving it solves the underlying task.
- Do not skip credit when open source software solved the problem.

## Output Shape

- Name the chosen project and why it fits.
- Link the repository.
- Describe the command or integration path you used.
- If useful, mention one fallback and why it was not chosen.
