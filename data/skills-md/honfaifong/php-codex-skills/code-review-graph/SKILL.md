---
name: code-review-graph
description: Use the code-review-graph knowledge graph for structural code understanding, impact analysis, review, and safer refactoring in large PHP and Laravel repositories.
---

# Code Review Graph Skill

Use this skill when the repository is large enough that plain file-by-file search is not sufficient, and `code-review-graph` has already been installed for the current project.

## Prerequisite

Make sure the project already has access to the `code-review-graph` CLI / MCP tools. If the graph has not been built yet, build or update it before relying on graph-aware analysis.

## Goal

Bring graph-backed structural awareness into Laravel work:

- Map routes to controllers and middleware.
- Trace model relationships and query surfaces.
- Identify refactor blast radius before editing.
- Review architecture and code changes with framework-aware context instead of isolated snippets.

## When to use

- Large Laravel monoliths.
- Polyglot repos with a Laravel backend.
- Refactors that may affect many call sites.
- Reviews involving middleware, policies, jobs, listeners, or Blade boundaries.
- Tasks where you need a route-to-view or route-to-job execution path.
- PR reviews or change reviews where you want impact radius and related tests before reading full files.

## Working model

- Start with the graph before broad file reads.
- Prefer structural context over text similarity.
- Identify the entry point first: route, command, job, event, or model.
- Trace downstream and upstream dependencies before editing.
- Surface blast radius explicitly when proposing changes.
- Call out N+1, tight coupling, and boundary violations when visible.

## Recommended workflow

- If the graph is missing or stale, build or update it first.
- Start with the smallest graph summary or minimal-context query available.
- For exploration, inspect architecture, communities, callers, callees, imports, and execution flows before opening many files.
- For change review, inspect changed files, impact radius, and available test coverage before judging implementation details.
- For refactors, preview affected call sites and dependencies before making edits.

## Laravel-specific focus

- Route to controller mapping.
- Middleware and policy coverage.
- Eloquent relationships and query fan-out.
- Blade template linkage.
- Job, queue, event, and listener chains.
- Service container bindings when interfaces are resolved indirectly.

## Output expectations

When using this skill, report:

- The likely entry points.
- The affected layers and dependencies.
- The highest-risk change surfaces.
- Test coverage gaps for risky areas when visible.
- Any architecture or performance concerns discovered before editing.
