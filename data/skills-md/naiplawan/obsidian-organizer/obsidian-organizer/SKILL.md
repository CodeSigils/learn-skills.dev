---
name: obsidian-organizer
description: "Organize Obsidian notes and brownfield codebase documentation for AI retrieval, Spec Kit-style planning, and Excalidraw visualizations. Apply this skill whenever the user mentions organizing, restructuring, optimizing, visualizing, diagramming, or improving Obsidian vaults, knowledge bases, workflows, architectures, note collections, or brownfield project documentation. Use it when users say 'organize my notes', 'make notes AI-friendly', 'restructure for Claude retrieval', 'clean up knowledge base', 'read this codebase and document it', 'document this brownfield project', 'create Spec Kit docs', 'speckit documentation', 'generate specs from code', 'create diagrams', 'draw architecture', 'generate Excalidraw', 'visualize workflow', 'flowchart', 'mind map', or when working with MOCs, wikilinks, vault architecture, codebase documentation, and visual knowledge systems. This skill transforms scattered notes and existing repositories into atomic, interlinked, evidence-backed knowledge optimized for AI assistants, Claude Skills, RAG systems, Spec Kit-style delivery, and Excalidraw-based visual retrieval."
metadata:
  version: 2.2.5
  capabilities:
    - obsidian-organization
    - rag-optimization
    - wikilink-generation
    - frontmatter-standardization
    - knowledge-graph-optimization
    - excalidraw-generation
    - architecture-visualization
    - animated-diagrams
    - brownfield-codebase-documentation
    - spec-kit-style-documentation
    - evidence-backed-repository-analysis
    - evidence-ledger-reconciliation
    - claim-verification
    - human-first-documentation
---

# Obsidian Organizer + Excalidraw Visual Knowledge System

Transform scattered Obsidian notes into AI-ready, visually connected knowledge systems.

This skill combines:

* Structured Obsidian organization
* AI retrieval optimization
* RAG-friendly metadata
* Excalidraw visualization generation
* Architecture and workflow diagrams
* Visual concept mapping
* Brownfield codebase documentation
* Spec Kit-style specifications, plans, and task breakdowns

---

# Core Philosophy

> You are no longer organizing notes only for humans.
> You are organizing structured context for AI retrieval and visual reasoning.

AI systems benefit from:

* Atomic knowledge
* Explicit relationships
* Semantic consistency
* Structured metadata
* Visual representations
* Diagram-based contextual understanding
* Code references that tie documentation back to real implementation

This skill optimizes both:

1. Text retrieval
2. Visual comprehension

Humans also benefit from:

* Clear summaries before implementation detail
* Explicit assumptions and tradeoffs
* Stable names and predictable section ordering
* Actionable recommendations with owners
* Confidence labels that prevent over-trust

## Human-First Workflow

For person-facing outputs, use this structure:

1. Summary (short, plain language)
2. What changed and why
3. Risks / uncertainties / unknowns
4. Recommended next actions
5. Evidence (only if requested or required by audit mode)

Keep evidence IDs and file references in a dedicated section at the end.

### Person-Review Template (Default)

Add this block to each artifact that is shared with a non-technical reviewer:

```md
## For people

### Summary
- Who this helps:
- What this document answers:
- What changed:

### Why this matters
- Problem it addresses:
- Impact if ignored:

### Risks and unknowns
- Known risks:
- Unknowns / dependencies:
- Confidence:

### Recommended next actions
- Owner:
- Action:
- Deadline / trigger:

### Open questions
- ...
```

Use it before implementation details and before any evidence table.

### Copy-Paste Artifact Templates

### PROJECT-HOME.md

```md
---
title: Project Home
type: project-home
status: draft
confidence: medium
last_verified: YYYY-MM-DD
related: []
diagram:
evidence_confidence: medium
---

# Project Home

## For people

### Summary
- Who this helps:
- What this document answers:
- What changed:

### Why this matters
- Problem this solves:
- Expected benefit:

### Risks and unknowns
- Known risks:
- Unknowns / dependencies:
- Confidence:

### Recommended next actions
- Owner:
- Action:
- Deadline / trigger:

### Open questions
- ...

## Purpose
This is the one-page entry point for people and agents.

## What this project does

## Current implementation

## How to use the docs

## Evidence
- E000 references:
```

### architecture.md

```md
---
title: Architecture
type: architecture
status: draft
confidence: medium
last_verified: YYYY-MM-DD
related: []
diagram:
evidence_confidence: medium
---

# Architecture

## For people

### Summary
- Who this helps:
- What changed:
- Why this matters:

### Why this matters
- Problem this solves:
- Impact if ignored:

### Recommended next actions
- Owner:
- Action:
- Deadline / trigger:

## Purpose
Describe module/runtime structure in simple language first.

## Current behavior

## Data flow

## Operational behavior

## Evidence
- E000 references:
```

### specs/<capability>/spec.md

```md
---
title: Spec
type: spec
status: observed
confidence: medium
last_verified: YYYY-MM-DD
source_paths: []
evidence_confidence: medium
spec_artifact: spec
---

# [Capability] Spec

## For people

### Summary
- Who this helps:
- What this document answers:
- What changed:

### Why this matters
- Problem this solves:
- Impact if ignored:

### Risks and unknowns
- Known risks:
- Unknowns / dependencies:
- Confidence:

### Recommended next actions
- Owner:
- Action:
- Deadline / trigger:

## Purpose

## Current behavior

## Intended behavior

## Functional requirements

## Non-functional requirements

## Evidence
- E###:
```

### specs/<capability>/plan.md

```md
---
title: Plan
type: plan
status: draft
confidence: low
last_verified: YYYY-MM-DD
related: []
evidence_confidence: medium
spec_artifact: plan
---

# [Capability] Plan

## For people

### Summary
- Why we are planning this:
- What decision is needed:

### Why this matters
- Decision impact:
- Cost or risk if delayed:

### Recommended next actions
- Owner:
- Action:
- Deadline / trigger:

## Scope

## Current implementation summary

## Proposed changes

## Risks and migration notes

## Evidence
- E###:
```

### specs/<capability>/tasks.md

```md
---
title: Tasks
type: tasks
status: draft
confidence: medium
last_verified: YYYY-MM-DD
related: []
evidence_confidence: medium
spec_artifact: tasks
---

# [Capability] Tasks

## For people

### Summary
- Who owns execution:
- Expected outcome:
- Target date:

## Edge cases

## Current behavior

## Tasks
- [ ] T001 Inspect [path] to confirm current behavior
- [ ] T002 Update [path] for [specific change]
- [ ] T003 Add or update tests in [path]
- [ ] T004 Update docs and diagrams

## Evidence
- E###
```

### evidence-ledger.md

```md
---
title: Evidence Ledger
type: evidence-ledger
status: maintained
last_verified: YYYY-MM-DD
---

# Evidence Ledger

## For people

### Summary
- Why this ledger matters:
- Confidence posture:

## Claim Registry

| id | claim | evidence | confidence | status | verification_note |
| --- | --- | --- | --- | --- | --- |
| E001 | ... | `path:line-range` | medium | observed | ...
| E002 | ... | `path` + tests | high | observed | ...
```

### Human Readability Rules

* Prefer one-sentence purpose statements before detailed lists.
* Keep headings consistent across generated notes.
* Keep critical decisions grouped near the top of each long document.
* Define terms before use and avoid unexplained jargon.

### People-Focused Writing Rules

Use these output standards for mixed audiences (adapted from plain-language and developer style guidance):

* Write for the target audience first; define who the note is for before heavy detail.
* Put a short topic sentence at the start of each section.
* Use active voice and state what changed/what to do clearly.
* Use short paragraphs, simple words, and one core idea per section.
* Prefer sentence-case headings and consistent levels (`#`, `##`, `###`) without skipping levels.
* Keep headings action- or concept-focused and predictable across artifacts.
* Explain any unavoidable technical term at first use.

## Communication Modes

Choose mode explicitly based on the user and task:

### Human mode (default for mixed-audience users)

1. Start with `## For people`.
2. Include only concise context and impact statements.
3. Delay evidence tables until the end.
4. End with decisions and next steps (owner, trigger, due date).

### Technical mode (developer or implementation tasks)

1. Keep artifact templates but include full evidence traceability immediately where claims are made.
2. Keep section headings compact and task-oriented.
3. Include `claim` IDs and file references on first mention when available.

### Audit mode (when confidence is low or conflict is found)

1. State assumptions explicitly.
2. Separate `observed` vs `inferred` claims.
3. Mark open questions as unresolved and propose a follow-up pass.

## Brownfield + Human-Facing Artifact Pattern

When documenting codebase-derived artifacts for non-technical review, always generate (or recommend) this layer map:

1. `PROJECT-HOME.md` (one-page executive overview in plain language).
2. `architecture.md` (structure + diagram).
3. `/specs/<capability>/spec.md` (observed behavior).
4. `/specs/<capability>/plan.md` (what to do next).
5. `/specs/<capability>/tasks.md` (ownered checklist).
6. `evidence-ledger.md` (compact claims + confidence + source evidence).
7. Incident/decision/runbook notes for human-operational context.

For each artifact, include a short "for humans" summary block before any raw evidence section.

### Artifact Section Template (Brownfield)

For spec and project notes, keep this consistent structure:

```md
## Purpose
One-sentence purpose.

## Current behavior
- ...

## Intended behavior
- ...

## Decisions and tradeoffs
- ...

## Evidence
Reference `E###` IDs and source files.

## Risks and follow-ups
- ...
```

## Template Mapping

Use this exact mapping when generating artifacts:

| Artifact | Human block required | Technical block required | Minimal evidence requirement |
| --- | --- | --- | --- |
| `PROJECT-HOME.md` | required | required | one `## For people` + claim references |
| `architecture.md` | required | required | at least one `E###` claim row |
| `spec.md` | required | required | claim IDs for each major claim |
| `plan.md` | required | required | task-level claim references |
| `tasks.md` | required | required | path-scoped tasks plus claim references for behavior/integration assumptions |
| `evidence-ledger.md` | required | required | claim registry with evidence rows |

## Evidence Research Protocol

For all brownfield documentation, use an explicit evidence workflow:

1. Build a claim registry: `E001`, `E002`, ...
2. For every claim, attach at least one evidence source: file path (and line range when possible), symbol, test, or config.
3. Score confidence:
   - `high`: corroborated by two independent evidence types (e.g., code + test)
   - `medium`: supported by one strong evidence type
   - `low`: inferred from conventions or partial clues
4. Any claim not verified by code-level evidence remains `inferred`.
5. Keep an explicit `evidence-ledger.md` and treat unresolved items as follow-up tasks.
6. Do not publish claims marked `inferred` as required behavior in `spec.md`.

---

# Unified Workflow

## Slash Help / Mode Selection

When the user types `/`, `/help`, `/mode`, `/modes`, or asks what this skill can do, present this mode selector before taking action:

```text
Obsidian Organizer modes:

1. Knowledge Organization
   Clean up notes, split large files, fix frontmatter, add wikilinks, and improve retrieval metadata.

2. Visual Knowledge Generation
   Create Excalidraw diagrams, architecture maps, flowcharts, timelines, and mind maps.

3. Hybrid Knowledge System
   Combine structured Obsidian notes, linked concepts, metadata, and embedded diagrams.

4. Brownfield Codebase to Spec Kit-Style Docs
   Read an existing repository and generate evidence-backed PROJECT-HOME, constitution, architecture, spec, plan, tasks, contracts, and diagrams.

Reply with 1, 2, 3, or 4, or describe what you want organized.
```

If the user already clearly requested a mode, do not stop for selection. Continue with the matching workflow and state the selected mode briefly.

## Mode 1 — Knowledge Organization

Used for:

* Vault cleanup
* RAG optimization
* Frontmatter fixes
* Wikilink creation
* Note splitting
* Folder restructuring

## Mode 2 — Visual Knowledge Generation

Used for:

* Architecture diagrams
* Flowcharts
* Mind maps
* Relationship maps
* Timelines
* Animated Excalidraw exports

## Mode 3 — Hybrid Knowledge System (Recommended)

Combines:

1. Structured notes
2. Linked concepts
3. Excalidraw visualizations
4. Embedded diagrams
5. Retrieval metadata

Recommended for:

* Engineering knowledge bases
* Architecture documentation
* Incident management systems
* ADR repositories
* Operational intelligence vaults

## Mode 4 — Brownfield Codebase to Spec Kit-Style Docs

Used when the source material is an existing repository instead of an existing note set.

Combines:

1. Read-only codebase discovery
2. Evidence-backed architecture and behavior extraction
3. Spec Kit-style documentation artifacts
4. Obsidian-friendly wikilinks and metadata
5. Excalidraw diagrams for system structure and flows

Recommended for:

* Brownfield application onboarding
* Turning existing implementation into living specs
* Preparing AI agents to safely modify a legacy codebase
* Creating implementation-grounded plans before refactors
* Building project knowledge bases from source code

---

# Trigger Detection

## Organization Triggers

* organize my notes
* optimize for AI retrieval
* restructure vault
* split this note
* add wikilinks
* fix frontmatter
* clean up knowledge base
* make AI-friendly

## Brownfield / Spec Kit Triggers

* read this codebase and document it
* document this brownfield project
* organize documentation from the repo
* generate specs from code
* create Spec Kit docs
* speckit documentation
* spec-driven docs
* make a plan from the existing code
* extract architecture from this codebase
* create implementation-grounded tasks
* prepare this repo for AI coding agents

## Excalidraw / Visualization Triggers

* Excalidraw
* diagram
* architecture diagram
* flowchart
* mind map
* visualize
* workflow diagram
* flowchart
* mind map
* visualization
* standard excalidraw
* animate
* animated diagram
* Excalidraw animation

---

# Excalidraw Integration

## Output Modes

| Trigger                          | Mode     | Format      | Usage                       |
| -------------------------------- | -------- | ----------- | --------------------------- |
| Excalidraw / diagram / flowchart | Obsidian | .md         | Open directly in Obsidian   |
| standard excalidraw              | Standard | .excalidraw | Open in excalidraw.com      |
| animate / animated diagram       | Animated | .excalidraw | Use with excalidraw-animate |

---

# Diagram Type Selection Guide

| Type         | Use Case                         |
| ------------ | -------------------------------- |
| Flowchart    | Workflows, execution paths       |
| Mind Map     | Idea expansion, concept grouping |
| Hierarchy    | Systems, org structures          |
| Relationship | Dependencies, interactions       |
| Timeline     | Incidents, migrations, history   |
| Matrix       | Prioritization, comparisons      |
| Architecture | Services, infrastructure         |
| Freeform     | Brainstorming                    |

---

# Hybrid Knowledge Design Rules

## Every Major Concept Should Have:

1. Atomic markdown note
2. Metadata-rich frontmatter
3. Wikilinks
4. Related diagram
5. Searchable keywords
6. Stable naming

## Every Brownfield Documentation Claim Should Have:

1. Source file reference
2. Implementation evidence
3. Confidence level
4. Known gaps or assumptions
5. Relationship to specs, plans, tasks, or diagrams

---

# Visual Knowledge Rules

## Excalidraw Standards

### Text Rules

* Use `fontFamily: 5`
* Minimum readable sizes:

  * Title: 20-28px
  * Body: 16-18px
  * Notes: 14px minimum
* Replace punctuation only when explicitly required by a renderer, and only within Excalidraw `text` fields; never run global search/replace on markdown notes, code blocks, JSON, or URLs.

### Layout Rules

* Canvas: 0-1200 x 0-800
* Minimum spacing: 20px
* Padding: 50px minimum
* Avoid overlaps
* Avoid emoji usage

### Color Palette

#### Text Colors

| Purpose  | Color   |
| -------- | ------- |
| Title    | #1e40af |
| Subtitle | #3b82f6 |
| Body     | #374151 |
| Emphasis | #f59e0b |

#### Fill Colors

| Semantic   | Color   |
| ---------- | ------- |
| Primary    | #a5d8ff |
| Success    | #b2f2bb |
| Warning    | #ffd8a8 |
| Processing | #d0bfff |
| Critical   | #ffc9c9 |
| Planning   | #fff3bf |
| Data       | #c3fae8 |
| Analytics  | #eebefa |

---

# Visual Retrieval Optimization

## Diagrams Must:

* Reflect semantic structure
* Use explicit labels
* Show causal relationships
* Surface dependencies
* Match note terminology exactly

## Avoid:

* Ambiguous labels
* Decorative-only diagrams
* Inconsistent naming
* Overcrowded layouts

---

# Excalidraw JSON Requirements

## Required Structure

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://github.com/zsviczian/obsidian-excalidraw-plugin",
  "elements": [],
  "appState": {
    "gridSize": null,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```

## Required Element Fields

```json
{
  "id": "unique-id",
  "type": "rectangle",
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 50,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "roundness": {"type": 3},
  "seed": 123456,
  "version": 1,
  "isDeleted": false,
  "boundElements": null,
  "updated": 1,
  "link": null,
  "locked": false
}
```

---

# Diagram Embedding Strategy

## Recommended Pattern

Each major concept note should embed diagrams.

Example:

```md
---
title: Authentication Architecture
tags: [architecture, auth]
type: concept
---

# Authentication Architecture

![[authentication-flow.excalidraw]]

## Overview

JWT-based authentication flow.

## Related

- [[Session Management]]
- [[JWT Refresh Flow]]
```

---

# Organizational Workflow

## Step 1 — Quick Scan

Check:

* Frontmatter
* Wikilinks
* Large files
* Missing metadata
* Existing diagrams

## Step 2 — Structural Optimization

* Split large notes
* Normalize terminology
* Add metadata
* Create links

## Step 3 — Visual Extraction

Generate diagrams for:

* Architecture
* Incident timelines
* Data flow
* Service dependencies
* Debugging flows
* Operational procedures

## Step 4 — Diagram Linking

Connect:

* Notes ↔ diagrams
* Concepts ↔ architecture
* Incidents ↔ timelines
* ADRs ↔ tradeoff visuals

## Step 5 — Validation

Verify:

* Links resolve
* Diagrams open correctly
* Naming consistency
* Retrieval metadata quality

---

# Brownfield Codebase Documentation Workflow

Use this workflow when the user asks to read an existing codebase and organize documentation in a Spec Kit-like structure.

## Step 1 — Repository Discovery

Start with read-only inspection before writing docs:

* Identify language, framework, package manager, and entry points
* Locate routing, API boundaries, state management, data models, persistence, config, auth, jobs, integrations, and tests
* Read existing documentation first if present
* Build a file map with high-value source paths
* Note generated files, vendored files, build outputs, and ignored directories to avoid documenting noise

Prefer fast search tools:

```text
rg --files
rg "router|route|controller|handler|model|schema|service|repository|provider|bloc|cubit|store|migration|endpoint|auth"
```

## Step 2 — Evidence Ledger

Maintain an internal evidence ledger while analyzing:

| Claim | Evidence | Confidence |
| ----- | -------- | ---------- |
| What the system does | File paths, symbols, tests, config | high / medium / low |
| How data flows | Handlers, services, repositories, schemas | high / medium / low |
| External contracts | API routes, DTOs, OpenAPI, clients | high / medium / low |
| Operational behavior | env vars, jobs, scripts, deploy config | high / medium / low |

Do not invent requirements. If intent is unclear, mark it as inferred and explain the evidence.

Use this ledger shape:

```md
---
title: evidence-ledger
status: maintained
---

| id | claim | evidence | confidence | status | verification_note |
| --- | --- | --- | --- | --- | --- |
| E001 | ... | `backend/app.py:112-160` | medium | observed | Confirmed by handler + schema |
| E002 | ... | `tests/test_auth.py` | high | observed | Confirmed by positive/negative cases |
```

If two evidence sources conflict, record both, downgrade confidence, and surface the conflict as a documented gap before finalizing artifacts.

## Step 3 — Spec Kit-Style Artifact Set

Create artifacts that mirror Spec Kit habits while remaining useful in Obsidian.

Recommended structure:

```text
/Projects/<Project Name>/
├── PROJECT-HOME.md
├── constitution.md
├── architecture.md
├── glossary.md
├── evidence-ledger.md
├── /specs/
│   └── /<capability-or-feature>/
│       ├── spec.md
│       ├── plan.md
│       ├── tasks.md
│       ├── research.md
│       ├── data-model.md
│       ├── quickstart.md
│       └── /contracts/
├── /Diagrams/
│   ├── system-context.excalidraw
│   ├── architecture.excalidraw
│   └── critical-flow.excalidraw
├── /Runbooks/
├── /Decisions/
└── /Archive/
```

Use the existing vault structure if one exists. Do not force a new top-level layout when the repository already has a documentation convention.

## Step 4 — Artifact Responsibilities

### PROJECT-HOME.md

Purpose: entry point for AI and human readers.

Include:

* What the project does
* Primary user or system workflows
* Tech stack
* Main folders and entry points
* Key specs
* Key diagrams
* Current documentation confidence

### constitution.md

Purpose: stable engineering rules extracted from the codebase.

Include:

* Architectural principles currently followed
* Naming and module conventions
* Testing expectations
* Security and data handling constraints
* Integration boundaries
* Do-not-break contracts

Mark each item as:

* `observed` when directly supported by code
* `inferred` when derived from repeated patterns
* `proposed` when it is a recommendation

### architecture.md

Purpose: explain how the system is assembled.

Include:

* Runtime architecture
* Module boundaries
* Data flow
* External services
* Storage model
* Configuration and environment dependencies
* Test architecture
* Diagram embeds

### specs/<capability>/spec.md

Purpose: describe behavior already implemented or required.

Use this structure:

```md
---
title:
type: spec
project:
capability:
status: observed
confidence:
last_verified:
source_paths:
related:
---

# [Capability] Specification

## Summary

## User / System Goals

## Functional Requirements

## Non-Functional Requirements

## Current Behavior

## Edge Cases

## Acceptance Criteria

## Source Evidence
```

### specs/<capability>/plan.md

Purpose: implementation-aware delivery plan.

Include:

* Current implementation summary
* Target change or documentation goal
* Affected modules
* Data model or contract impact
* Test strategy
* Risks
* Rollout or migration notes

### specs/<capability>/tasks.md

Purpose: actionable task breakdown grounded in real files.

Use checkboxes:

```md
- [ ] T001 Inspect [path] to confirm current behavior
- [ ] T002 Update [path] for [specific change]
- [ ] T003 Add or update tests in [path]
- [ ] T004 Update documentation links and diagrams
```

Tasks should name concrete paths whenever possible.

### specs/<capability>/research.md

Purpose: capture unknowns and tradeoffs.

Include:

* Questions answered by code inspection
* Open questions
* Alternatives observed or considered
* Decisions needed from humans

### specs/<capability>/data-model.md

Purpose: document entities, schemas, DTOs, and persisted state.

Include:

* Entities
* Fields
* Relationships
* Validation rules
* Persistence layer
* Source evidence

### specs/<capability>/contracts/

Purpose: document API, event, file, CLI, or integration contracts.

Use markdown unless a formal schema already exists. Link to source route handlers, request/response types, generated clients, or tests.

## Step 5 — Brownfield Diagram Set

Generate diagrams when they clarify the codebase:

| Diagram | When to Create |
| ------- | -------------- |
| System Context | Project has external users, services, or APIs |
| Container / Module Map | Codebase has meaningful internal boundaries |
| Critical Flow | Auth, payment, sync, import/export, onboarding, or core business process |
| Data Model | Entities and relationships are central |
| Test Strategy Map | Tests are scattered or onboarding is difficult |

Embed diagrams from PROJECT-HOME.md, architecture.md, and relevant specs.

## Step 6 — Validation

Before finishing:

* Check every important claim has source evidence
* Mark unverified claims as inferred or unknown
* Ensure wikilinks resolve or clearly target planned notes
* Verify docs do not contradict existing README, tests, or code
* Keep generated docs separate from source code unless the user requested inline code comments
* Summarize files created or modified

Validation checklist (required):

1. Each claim in `PROJECT-HOME.md`, `constitution.md`, `architecture.md`, `spec.md`, `plan.md`, and `tasks.md` has an `E###` id.
2. Every `E###` row in `evidence-ledger.md` includes path-based evidence.
3. Claims at `low` confidence are explicitly marked as `inferred`.
4. No unresolved claim is presented as observed.
5. All contradictions are explicitly called out under "unknowns", "risks", or "open questions".

Human usability checklist:

1. Start with a short executive summary for non-technical readers.
2. Place decision points before detailed evidence.
3. Keep terminology aligned with existing vault naming.
4. Include a `## For people` block for every artifact shared with non-technical users.
5. Use the artifact section template for spec/plan/task notes.
6. Include at least one clear next step with owner or condition.
7. Avoid jargon-only sections unless explicitly requested.

---

# Recommended Vault Structure

```text
/vault
├── /Concepts
│   ├── /Architecture
│   ├── /Patterns
│   └── /Standards
├── /Diagrams
│   ├── /Architecture
│   ├── /Flows
│   ├── /Incidents
│   └── /Mindmaps
├── /Incidents
├── /Decisions
├── /Runbooks
├── /Projects
├── /Glossary
└── /Archive
```

---

# Visual Incident Intelligence

High-value incidents should include:

1. Incident note
2. Timeline diagram
3. Failure flow visualization
4. Recovery sequence
5. Dependency graph

Example:

```md
# PostgreSQL Deadlock Incident

![[postgres-deadlock-timeline.excalidraw]]

## Symptoms

- Transaction timeout
- CPU spike
- Retry storm

## Root Cause

Inconsistent lock acquisition ordering.
```

---

# Animated Diagram Support

## Animation Order Strategy

Recommended sequence:

1. Title
2. Main containers
3. Relationships
4. Supporting labels
5. Detailed annotations

Example:

```json
"customData": {
  "animate": {
    "order": 1,
    "duration": 500
  }
}
```

---

# Retrieval Optimization Rules

## Prefer Explicit Technical Terms

Prefer:

* PostgreSQL Connection Pool Exhaustion
* Kubernetes Readiness Probe Timeout
* JWT Refresh Token Rotation

Avoid:

* DB issue
* deployment problem
* auth stuff

---

# Metadata Standards

```yaml
---
title:
type:
domain:
stack:
services:
keywords:
status:
confidence:
last_verified:
related:
diagram:
visual_type:
brownfield:
source_paths:
spec_artifact:
evidence_confidence:
---
```

## New Visual Metadata Fields

| Field       | Purpose                        |
| ----------- | ------------------------------ |
| diagram     | Related Excalidraw file        |
| visual_type | architecture / flow / timeline |
| animation   | true/false                     |
| layout      | hierarchy / matrix / freeform  |

## Brownfield Metadata Fields

| Field               | Purpose                                      |
| ------------------- | -------------------------------------------- |
| brownfield          | true when generated from existing code       |
| source_paths        | Implementation files supporting the note     |
| spec_artifact       | home / constitution / spec / plan / task     |
| evidence_confidence | high / medium / low based on source support  |

---

# Knowledge Graph + Visual Graph

The vault should function as:

1. Semantic graph
2. Visual graph
3. Retrieval graph
4. Operational intelligence system

Diagrams should reinforce retrieval structure.

---

# Common Mistakes

## Organization Mistakes

* Giant mixed-topic notes
* Missing metadata
* Broken wikilinks
* Generic titles
* Stale knowledge

## Excalidraw Mistakes

* Tiny unreadable text
* Overlapping elements
* Low contrast colors
* Missing padding
* Decorative diagrams without semantics

---

# Output Requirements

## For Organization Tasks

Provide:

* Files modified
* Metadata added
* Notes split
* Links created
* Structure changes

## For Diagram Tasks

Provide:

* Diagram type selected
* File path
* Output format
* Embedding instructions
* Animation details if applicable

## For Brownfield Spec Kit-Style Documentation Tasks

Provide:

* Repository areas inspected
* Documentation structure created
* Spec Kit-style artifacts generated
* Key source paths used as evidence
* Diagrams generated or recommended
* Unknowns and inferred claims
* Validation performed

---

# Example Hybrid Output

```text
Generated:
- Authentication.md
- JWT Refresh Flow.md
- authentication-architecture.excalidraw
- auth-dependency-map.excalidraw

Changes:
- Added frontmatter
- Added wikilinks
- Split monolithic backend.md
- Created architecture visualization
- Added retrieval metadata
```

## Example Brownfield Output

```text
Generated:
- Projects/CheckName/PROJECT-HOME.md
- Projects/CheckName/constitution.md
- Projects/CheckName/architecture.md
- Projects/CheckName/evidence-ledger.md
- Projects/CheckName/specs/name-validation/spec.md
- Projects/CheckName/specs/name-validation/plan.md
- Projects/CheckName/specs/name-validation/tasks.md
- Projects/CheckName/Diagrams/system-context.excalidraw

Evidence:
- backend/api/routes.py
- backend/domain/name_checker.py
- frontend/src/features/check-name/
- tests/test_name_checker.py

Unknowns:
- Production deployment topology was not present in the repository.
- Rate limiting behavior is inferred from middleware naming and needs confirmation.
```

---

# High-Value Knowledge Priority

| Priority | Type                   |
| -------- | ---------------------- |
| 1        | Incidents              |
| 2        | Architecture diagrams  |
| 3        | ADRs                   |
| 4        | Debugging flows        |
| 5        | Failure visualizations |
| 6        | Operational runbooks   |
| 7        | Generic references     |

---

# Final Principle

> Great AI knowledge systems are both semantically structured and visually navigable.

Text explains.

Diagrams compress complexity.

Together they create high-quality retrieval systems for humans and AI.
