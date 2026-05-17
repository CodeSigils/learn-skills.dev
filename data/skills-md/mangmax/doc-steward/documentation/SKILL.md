---
name: documentation
description: "Use when bootstrapping docs or when a task may change public behavior, APIs, CLI commands, configuration, environment variables, schemas, setup, deployment, operations, architecture, release notes, durable project decisions, README, reference docs, changelog, ADRs, playbooks, or agent guidance."
---

# Documentation Skill

## Goal

Keep documentation synchronized with the project state. Treat stale documentation as a project bug, but do not create documentation churn for internal-only changes that do not affect users, operators, contributors, architecture, or future agents.

## Default Workflow

1. Inspect relevant existing documentation before editing docs, and before code changes when docs may influence the implementation.
2. Identify whether the task changes interface, structure, or project knowledge.
3. Make the code or project change.
4. Update only the affected documentation.
5. Check for contradictions between code, README, docs, changelog, and agent guidance.
6. Summarize documentation work in the final response.

## Decide Whether To Update Docs

Always check for documentation impact. Update docs only when at least one answer is "yes":

- **Interface:** Did public behavior, APIs, routes, CLI commands, config, env vars, schemas, file formats, installation, or usage change?
- **Structure:** Did architecture, module responsibilities, dependency boundaries, deployment, operations, or contributor workflow change?
- **Knowledge:** Was an important decision made, a long-lived tradeoff accepted, a limitation discovered, or technical debt made visible?

Usually do not update docs for purely internal refactors, tests, formatting, small implementation fixes with no visible behavior change, or mechanical cleanup unless existing docs would become misleading.

## Evidence Before Editing

Base documentation on verifiable project evidence:

- README, existing docs, AGENTS.md, CLAUDE.md, or package-level READMEs
- package scripts, Makefile, task files, CI config, Docker files, deployment manifests
- source exports, route definitions, CLI parsers, config schemas, env validation, database migrations
- tests, fixtures, examples, sample configs, release metadata
- explicit user instructions

Do not invent commands, support status, APIs, performance claims, compatibility promises, or deployment steps. If something cannot be verified, write it as an open question or omit it.

## Production Guardrails

- Keep documentation changes proportional to the project change.
- Prefer surgical edits over broad rewrites, reorganizations, or style-only churn.
- Preserve warnings, limitations, compliance notes, security guidance, and operational runbooks unless verified project changes make them obsolete.
- Do not document secrets, private credentials, internal tokens, or sensitive customer data.
- Do not duplicate generated or authoritative sources of truth; link to OpenAPI specs, schemas, package metadata, or generated reference docs when those are canonical.
- Do not create empty files, placeholder sections, blank tables, or speculative roadmap items.
- Do not rename or move established docs unless the user asked or the existing structure is clearly broken.

## Update Map

Apply every matching row, but keep the edit as small as the change allows.

| Change | Update |
|---|---|
| New public feature | README or usage docs; reference docs if there are commands, APIs, config, or schemas |
| Public API, route, CLI, config, env, or file-format change | Reference docs; README if common usage changes |
| Breaking change or deprecation | README migration note; CHANGELOG if present; reference docs |
| Setup, install, or development workflow change | README; getting-started or development docs; AGENTS.md if present |
| Deployment, operations, or incident response change | Operations docs or playbook; README only if users need the entry point |
| Architecture or dependency-boundary change | Architecture docs; ADR only when the decision is durable and has meaningful tradeoffs |
| Important limitation or follow-up | Roadmap, `docs/known-issues.md`, decisions, or the nearest existing planning document |
| Release preparation | CHANGELOG or release notes; README only if current status or usage changed |

For detailed structures and examples, read [references/document-map.md](references/document-map.md).

## Bootstrap Rules

When documentation is missing or nearly empty, create the smallest useful set based on project size:

- Tiny script: `README.md`; update existing agent guide only if present.
- Small library or CLI: `README.md`, optional `CHANGELOG.md`, and one focused docs file if README would become too large.
- App, service, infrastructure project, or monorepo: `README.md` plus only the docs that can be filled with real information now.

Do not create empty placeholder docs. Prefer a short accurate README over a large template with blanks.

For bootstrap templates, read [references/bootstrap.md](references/bootstrap.md).

## Decision Records

Record an ADR only for decisions that are durable, difficult to reverse, cross module or operational boundaries, introduce important dependencies, or encode a tradeoff future agents must understand.

Do not create ADRs for routine implementation choices, local cleanup, small bug fixes, or choices already obvious from code.

For the ADR template, read [references/adr.md](references/adr.md).

## Existing Project Rules

- Preserve the project's current documentation style and file organization when it is coherent.
- Prefer updating existing docs over introducing new files.
- For large documentation sets, inspect and update only the docs related to the change unless a contradiction requires broader cleanup.
- If a project already has `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, or package-level agent guidance, update the existing file that owns the rule.
- Create a new `AGENTS.md` only during documentation bootstrap or when the user asks for agent guidance.
- In monorepos, keep workspace-level docs at the root and package-specific usage/API docs inside the package.

## Freshness Check

Before finishing, fix documentation that:

- describes removed behavior, commands, files, config keys, routes, or setup steps
- omits a newly required step, env var, migration, or operational procedure
- contradicts source code, examples, tests, or package metadata
- makes unverifiable claims
- contains TODOs that are now wrong or obsolete

## Final Response

End with a short documentation summary:

```txt
Documentation updated:
- README.md: updated usage for the new import command
- docs/reference.md: added API parameters
```

If no documentation changed, say:

```txt
Documentation checked; no updates were needed because behavior, APIs, setup, and architecture did not change.
```
