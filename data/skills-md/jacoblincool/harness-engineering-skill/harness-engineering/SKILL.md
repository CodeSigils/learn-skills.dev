---
name: harness-engineering
description: Bootstrap or migrate a repository into an agent-first harness-engineering knowledge store modeled on OpenAI's Harness engineering article. Use when Codex needs to set up AGENTS.md plus a structured docs/ system of record for a new repository, or audit an existing repository's documentation against the real codebase, rewrite mismatched docs, retire stale docs, and re-home surviving docs into a predictable agent-readable structure.
---

# Harness Engineering

## Overview

Turn repository documentation into a maintained system of record for agents.
Keep `AGENTS.md` short, store durable knowledge in versioned Markdown, and remove stale docs instead of preserving legacy navigation.

## Required Outcome

Leave the target repository with:

- a short `AGENTS.md` that acts as a table of contents
- a top-level `ARCHITECTURE.md`
- a structured `docs/` knowledge store
- explicit treatment of doc drift in `docs/QUALITY_SCORE.md` and `docs/exec-plans/tech-debt-tracker.md`
- a passing run of `scripts/validate_harness_docs.py`

## Workflow Selection

Choose one of two flows:

1. **Bootstrap**
- Use for a new repository or one with little or no durable documentation.
- Copy the always-required templates first, then add only the conditional templates that match the real repo surface.

2. **Migration**
- Use for an existing repository with docs that may be stale, duplicated, or scattered.
- Inventory current docs against code, configs, schemas, tests, and runtime entrypoints before writing anything.

Read these references before executing:

- `references/knowledge-store-contract.md`
- `references/document-contracts.md`
- `references/bootstrap-playbook.md` or `references/migration-playbook.md`
- `references/harness-engineering-article.md` when you need the rationale behind a rule

## Bootstrap Flow

1. Inspect the real repository surface.
- Identify runtime entrypoints, package managers, app domains, UI surfaces, API surfaces, data stores, and any product-spec or design-doc needs.
- Do not create conditional docs unless the repo actually has that surface.

2. Copy the always-required templates from `assets/templates/always/`.
- Materialize `AGENTS.md`, `ARCHITECTURE.md`, `docs/PLANS.md`, `docs/QUALITY_SCORE.md`, `docs/RELIABILITY.md`, `docs/SECURITY.md`, `docs/references/index.md`, and `docs/exec-plans/`.

3. Copy only matching conditional templates from `assets/templates/conditional/`.
- `design-docs/` when the repo needs durable design rationale.
- `product-specs/` when the repo has user-facing features or workflow specs.
- `DESIGN.md` when visual or interaction rules matter.
- `FRONTEND.md` when there is a browser, desktop, or app UI surface.
- `PRODUCT_SENSE.md` when product tradeoffs should be encoded for agents.
- `generated/db-schema.md` when the repo owns a database schema or migrations.

4. Rewrite template placeholders so they describe the actual repository.
- Replace generic text with real domains, components, constraints, and commands.
- Update `AGENTS.md` so it links to every required doc and every conditional doc that now exists.

5. Seed continuous maintenance.
- Add initial grades and gaps to `docs/QUALITY_SCORE.md`.
- Add follow-up doc debt items to `docs/exec-plans/tech-debt-tracker.md`.

6. Validate mechanically.
- Run `python3 <skill-dir>/scripts/validate_harness_docs.py <target-repo>`.
- Fix findings before claiming the setup is complete.

## Migration Flow

1. Build a doc inventory before editing.
- Find all repository docs that influence implementation, onboarding, architecture, specs, and runbooks.
- Compare each doc to code, config, schemas, migrations, tests, and current entrypoints.

2. Classify every doc using exactly one status:
- `keep-and-move`: still true, but needs relocation into the new structure
- `rewrite`: topic is still needed, but content is materially wrong or underspecified
- `replace`: existing doc shape is counterproductive; create a fresh document with the same responsibility
- `delete`: obsolete, misleading, duplicated, or no longer justified

3. Rewrite the knowledge store around current truth.
- Create the required harness structure.
- Move or rewrite surviving documents into the contract layout.
- Remove stale docs from active navigation immediately. Do not leave compatibility breadcrumbs to misleading content.

4. Rebuild navigation.
- Keep `AGENTS.md` short and link only to living sources of truth.
- Update directory indexes so they cover all sibling docs and do not point at deleted files.

5. Record debt and freshness.
- Add any remaining doc gaps to `docs/QUALITY_SCORE.md`.
- Add concrete cleanup items to `docs/exec-plans/tech-debt-tracker.md`.

6. Validate mechanically.
- Run the validator and clear every finding.

## Execution Rules

Enforce these rules in both flows:

- Prefer repository truth over prior documentation.
- Delete or replace stale docs instead of preserving backward compatibility.
- Keep knowledge in-repo and versioned; if an agent cannot discover it in the repo, treat it as missing.
- Encode invariants as structure, links, and checks instead of long prose.
- Keep `AGENTS.md` as a map, not an encyclopedia.

## Resource Map

- `references/harness-engineering-article.md`: section-by-section paraphrase of the OpenAI article and the rationale behind the workflow.
- `references/knowledge-store-contract.md`: required layout, navigation rules, and conditional surfaces.
- `references/document-contracts.md`: what each target doc must contain and when to omit it.
- `references/bootstrap-playbook.md`: ordered instructions for greenfield setup.
- `references/migration-playbook.md`: ordered instructions for audit, rewrite, and retirement.
- `assets/templates/always/`: base templates that every harness-style repo should start with.
- `assets/templates/conditional/`: optional templates that are copied only when the repo needs them.
- `scripts/validate_harness_docs.py`: mechanical validator for topology, links, index freshness, and `AGENTS.md` mapping drift.
