---
name: project-documentation
description: Generate a complete, internally-consistent project documentation suite — eight standardized markdown files written to a docs/ folder (PRD, software architecture, functional spec, database architecture, admin panel spec, REST API spec, engineering guidelines, project blueprint). Use this whenever the user wants to document a software project, bootstrap docs for a new or existing codebase, or produce any of those documents — a PRD, an architecture doc, an API spec, a database design, engineering guidelines, a project blueprint. Trigger on phrases like "project documentation", "design docs", "spec docs", "documentation suite", "write the docs", "document this app/service/system", or a request for just one of the eight docs (the suite is designed to be generated together so the documents stay consistent with each other). Also trigger when the user has been building or describing a software project in the conversation and now wants it written up formally.
---

# Project Documentation Suite

Generate eight standardized markdown documents into a `docs/` directory. The suite is designed to be produced together: later documents reference decisions made in earlier ones, and consistency across all eight is the main thing that makes the suite valuable rather than eight disconnected templates.

## What this produces

All files go in `docs/` at the project root:

| File | Document |
|------|----------|
| `docs/01-prd.md` | Product Requirements Document |
| `docs/02-software-architecture.md` | Software Architecture |
| `docs/03-functional-specification.md` | Functional Specification |
| `docs/04-database-architecture.md` | Database Architecture |
| `docs/05-admin-panel-specification.md` | Admin Panel Specification |
| `docs/06-rest-api-specification.md` | REST API Specification |
| `docs/07-engineering-guidelines.md` | Engineering Guidelines |
| `docs/08-project-blueprint.md` | Project Blueprint |

The detailed structure for each document lives in `references/<same-filename>` inside this skill. Read the relevant reference file immediately before writing that output document — do not write a document from memory of this overview.

## Workflow

### Step 1 — Gather context before writing anything

Good documentation is downstream of good inputs. Pull what you can from the environment first, then ask the user only for what's genuinely missing.

**Pull from context first (reduce what you have to ask):**
- If a codebase is present, inspect it: `package.json` / `pyproject.toml` / `go.mod` / `Cargo.toml` for stack and dependencies, directory layout for structure, `.env.example` for environment variables, any existing README or `docs/`, migration files or schema for the data model, route/controller files for API surface.
- If the project was discussed earlier in this conversation, extract the name, features, stack, and constraints from there.

**Then ask the user — in a single consolidated message — for the gaps.** Don't drip-feed one question at a time; present a short structured intake so they can answer in one pass. Adapt the list to what you already know (skip anything you've already established from the codebase or conversation):

> **Project basics**
> - Project name + one-line description (the elevator pitch)
> - What problem it solves / why it exists
> - Stage: idea, in development, or live in production
>
> **Users & roles**
> - Primary user types / personas (1–4)
> - Permission levels / roles (e.g. end user, staff, admin, super-admin) — this drives the admin doc
>
> **Scope**
> - Core features (the must-haves), as a list
> - Explicit non-goals / out of scope (optional but valuable)
>
> **Technical**
> - Frontend stack (or "none / API-only / CLI")
> - Backend language & framework
> - Database(s) and where they're hosted
> - Hosting / deployment target (e.g. Vercel, AWS, a VPS, Cloud Run)
> - Auth approach (e.g. JWT, OAuth, session cookies, Supabase Auth, none)
> - External integrations / third-party APIs
> - Does it expose a public or internal REST API? (drives doc 06)
> - Is there a separate admin panel? (drives doc 05)
> - Rough scale expectations (users, requests, data volume) — even an order of magnitude helps the architecture and risk sections
>
> **Process & meta**
> - Team size / who builds it
> - Existing conventions if any (language version, package manager, linter, git workflow)
> - Output language for the docs (default: English)

**Handling missing answers — this matters.** The user will not have every answer, and that is fine. Never block, and never invent specifics to fill a gap. Instead:
- For an unknown fact, write `[TBD: <what's needed and who decides>]`.
- For something you can reasonably infer but weren't told, write `[ASSUMPTION: <the assumption>]` so it's visibly a placeholder, not a stated fact.
- Do **not** fabricate names, metrics, OKR targets, stakeholder lists, API endpoints, table columns, or third-party services that the user never mentioned. Inventing plausible-looking specifics is the most damaging failure mode for this skill — a reader cannot tell a real decision from a guess, and the docs lose their authority. A document with honest `[TBD]` markers is far more useful than one that reads complete but is partly fictional.

Confirm the intake back to the user in a few lines before generating, so they can correct anything. Keep it brief.

### Step 2 — Establish canonical facts (consistency anchor)

Before writing the documents, lock down a small set of canonical facts and reuse them **verbatim** across all eight files. This is what stops the suite from drifting (the entity called `Listing` in one doc silently becoming `Item` or `product` in another). Hold these fixed:

- **Naming:** project name, and the exact spelling/casing of every domain entity (e.g. `Listing`, `User`, `Order`). Pick one term per concept and never vary it.
- **Stack:** the exact framework and version strings. Don't write "React" in one doc and "Next.js" in another unless both are true and the relationship is stated.
- **Roles:** the exact set of permission levels, used identically in the PRD, functional spec, admin spec, and API spec.
- **Entities:** the core data entities. These must line up across the functional spec's data dictionary (doc 03), the database tables (doc 04), and the API resources (doc 06). Same names, same fields.

If something is `[TBD]`, keep it `[TBD]` consistently everywhere rather than guessing differently in each doc.

### Step 3 — Generate all eight documents, in order

Create `docs/` if it doesn't exist. Generate the files **in numerical order (01 → 08)** — the order is dependency-aware: personas defined in the PRD are referenced by the functional spec; entities in the architecture and database docs are referenced by the API spec; etc.

For **each** document:
1. Read its reference file: `references/01-prd.md` through `references/08-project-blueprint.md`. Each reference gives the required sections (in order), per-section guidance, table schemas, a fillable skeleton, and a doc-specific quality bar.
2. Write a real `.md` file at the matching `docs/` path. Use whatever file-creation tool your environment provides; the deliverable is a real file on disk, not chat output.
3. Apply the canonical facts from Step 2.

Generate them as a batch — do all eight, don't stop after one and ask whether to continue (the user asked for the full suite).

### Step 4 — Hand off

After all eight files exist, give the user a short summary: which files were created, and a consolidated list of every `[TBD]` and `[ASSUMPTION]` marker across the suite so they know exactly what still needs a human decision. This list is the most useful single thing you can hand back — it turns the docs into an actionable checklist. If the environment has a file-presentation tool, present the files so the user can open them.

## House style (applies to every document)

These conventions keep the suite looking like one coherent set of documents:

- **Header block.** Start every document with: an `#` H1 title, a one-line purpose, and a metadata line — `Status: Draft · Owner: [TBD] · Last updated: <date>`. Use today's date.
- **Table of contents.** For any document longer than roughly one screen, add a short bulleted TOC after the header block.
- **Tables for tabular data.** Where a reference calls for a table (tech stack, data dictionary, dependencies, endpoints), use a real GitHub-flavored markdown table, not prose.
- **Right-size to the project.** A weekend side project does not need the same depth as a multi-team platform. Scale the detail to the project's actual complexity. If a whole section genuinely doesn't apply (e.g. no admin panel, no public API), say so explicitly and describe the minimal real surface that *does* exist — do not delete the document, and do not pad it with invented content to look complete. An honest "This project exposes no public API; the only programmatic surface is X" is correct and useful.
- **No fabrication.** Reiterated because it's the core risk: every concrete claim should trace to user input, the codebase, or a clearly-marked `[ASSUMPTION]`. When unsure, mark it, don't invent it.

### ASCII diagrams

Docs 02 (architecture) and 04 (ERD) call for ASCII diagrams. Keep them **simple and legible** — a diagram that's hard to read is worse than a clear bulleted breakdown. Favor a handful of boxes and labeled arrows over dense art. Wrap every diagram in a fenced code block so monospacing is preserved. Example of the level of detail to aim for:

```
┌──────────┐      HTTPS      ┌──────────────┐      SQL      ┌────────────┐
│  Browser │ ───────────────▶│  API Server  │ ─────────────▶│  Postgres  │
│  (React) │ ◀─────────────── │  (Express)   │ ◀───────────── │            │
└──────────┘   JSON (REST)   └──────┬───────┘               └────────────┘
                                    │ queue
                                    ▼
                             ┌──────────────┐
                             │  Worker(s)   │
                             └──────────────┘
```

If a relationship is too complex to render cleanly in ASCII, describe it in prose or a table and note that a rendered diagram (e.g. Mermaid, draw.io) is recommended for the final version.

## Quick reference — what each doc covers

For triggering and orientation only; the authoritative structure is in each reference file.

1. **PRD** — executive summary, vision/goals, personas, user stories, feature priority, acceptance criteria, OKRs, stakeholders.
2. **Software Architecture** — system overview, ASCII architecture diagram, component breakdown, data flow, tech stack table, cross-cutting concerns, deployment, risks.
3. **Functional Specification** — user workflows (trigger → flow → alternatives), UI specs, business rules, data dictionary, error scenarios, integrations.
4. **Database Architecture** — textual ERD, table definitions (columns/types/constraints/indexes), relationships, enums, migration strategy, backup, security/RLS.
5. **Admin Panel Specification** — admin roles/permissions, dashboard, user management, content management, settings, audit log, analytics, UI/UX, security.
6. **REST API Specification** — auth method, standard response envelope & error codes, pagination, rate limiting, webhooks, versioning, endpoint spec per resource.
7. **Engineering Guidelines** — coding standards, naming conventions, git workflow (Conventional Commits), PR process, testing strategy, CI/CD, error handling, security.
8. **Project Blueprint** — project structure tree, quick start, environment variables, scripts, environments, dependency table, decision log, roadmap.
