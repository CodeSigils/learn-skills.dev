---
name: project-init
description: "This skill initializes new software projects through a structured discovery, research, and documentation workflow. It should be used when the user wants to create/initialize a new project, start a new app, scaffold a new codebase, or plan a new software product. Triggered by requests like 'create a new project', 'initialize a new app', 'start a new project for X', 'I want to build X'. The skill does NOT generate code — it produces a project directory with comprehensive documentation (SPEC.md, STYLES.md, ROADMAP.md) that serves as the blueprint for implementation."
---

# Project Init

## Overview

This skill transforms a project idea into a fully scoped, documented project blueprint through structured discovery, research, and user collaboration. The output is a project directory containing comprehensive documentation that serves as the source of truth for implementation.

## Workflow

The workflow has two major stages: **Discovery** (understanding what to build) and **Initialization** (creating the project documentation). Complete Discovery fully before moving to Initialization.

---

## Stage 1: Discovery

### Step 1: Gather Project Details

Begin by understanding the project at a high level. Ask the user to describe:

- **What** the project is (purpose, problem it solves, target users)
- **Core features** and functionality
- **Tech stack** preferences (languages, frameworks, databases, infrastructure)
- **Project-type-specific details**:
  - Web apps: pages/routes needed, authentication, data models
  - CLI tools: example commands/usage, input/output formats
  - APIs: endpoints, data schemas, integrations
  - Mobile apps: screens, navigation flow, platform targets
  - Libraries/SDKs: public API surface, target consumers
  - Games: mechanics, platforms, networking model

Use the `AskUserQuestion` tool to gather this information. Start with broad questions, then drill into specifics based on answers. Do not overwhelm — ask 1-3 focused questions per round.

### Step 2: Research

Conduct online research using the `WebSearch` tool to investigate:

- **Similar projects** — find existing implementations, open-source examples, and established patterns for this type of project
- **Technical best practices** — architecture patterns, library choices, common pitfalls for the chosen tech stack
- **Trade-offs** — evaluate alternative approaches discovered during research
- **Implementation details** — specific APIs, protocols, or techniques the project will need

Synthesize findings internally. Identify anything the user may have missed, potential risks, and areas needing clarification.

### Step 3: Self-Reflection

Before proceeding to the interview, pause and reason through:

- Connections between user requirements and research findings
- Gaps in the current understanding
- Architectural implications of the stated requirements
- Potential scope risks or technical challenges
- Questions where the answer is NOT obvious from prior context

### Step 4: Interview

Use the `AskUserQuestion` tool to clarify anything unresolved from Steps 1-3. Topics may include:

- Technical implementation choices surfaced by research
- UI/UX decisions (for visual projects)
- Concerns or trade-offs discovered during research
- Feature prioritization (MVP vs. nice-to-have)
- Design preferences and constraints
- Integration requirements
- Deployment and infrastructure needs

Rules for the interview:
- Do NOT ask questions whose answers are obvious from previous responses or research
- Do NOT ask about preferences already documented in `references/user-preferences.md` — read and apply those directly
- Continue interviewing until confident that the project is fully understood
- Each round should surface genuinely new information

Read `references/user-preferences.md` for standing preferences that apply to all projects (monorepo structure, Docker, Makefiles, Bash scripts). Apply these automatically without asking.

---

## Stage 2: Initialization

Proceed only after reaching full confidence in the project understanding. Initialization creates the project directory and documentation files — nothing else.

### Step 1: Create Project Directory

```bash
mkdir -p <project-name>/docs
```

Create only the project root and `docs/` directory. Do NOT run any framework initializers, package managers, or scaffolding tools — those are roadmap tasks.

### Step 2: Create SPEC.md

Write `<project-name>/docs/SPEC.md` containing:

- **Project Overview** — name, purpose, problem statement, target users
- **Architecture** — high-level system design, component diagram (ASCII/Mermaid), data flow
- **Tech Stack** — languages, frameworks, databases, infrastructure with rationale for each choice
- **Project Structure** — directory layout following monorepo conventions (see `references/user-preferences.md`)
- **Core Modules** — description of each major module/component, its responsibilities, and interfaces
- **Data Models** — key entities, schemas, relationships
- **API Surface** — endpoints, contracts, or public interfaces (as applicable)
- **External Integrations** — third-party services, APIs, dependencies
- **Key Decisions** — architectural decisions made during discovery with rationale

### Step 3: Create STYLES.md (Conditional)

Only create this file for projects with a visual/frontend component (web apps, mobile apps, desktop apps, games with UI).

Write `<project-name>/docs/STYLES.md` containing a concise styling specification for a modern, professional, Apple-esque design:

- **Design Philosophy** — clean, minimal, purposeful, premium feel
- **Color Palette** — primary, secondary, accent, semantic colors (success/warning/error/info), neutral scale, dark mode variants
- **Typography** — font families (system stack or specific), size scale, weight scale, line heights
- **Spacing & Layout** — spacing scale, grid system, breakpoints, max-widths, container padding
- **Component Styling** — buttons, inputs, cards, modals, navigation patterns, hover/focus/active states
- **Motion & Animation** — transition durations, easing curves, animation principles
- **Iconography** — icon style, library recommendation, sizing
- **Shadows & Elevation** — shadow scale, usage guidelines
- **Border Radius** — radius scale and usage

Base recommendations on modern design trends: clean whitespace, subtle depth through shadows, refined color palettes, smooth micro-interactions.

### Step 4: Create ROADMAP.md

Read `references/roadmap-format.md` for the canonical format, phase structure, and action item template.

Write `<project-name>/docs/ROADMAP.md` following these rules:

**Header**: `# <project-name> Development Roadmap` followed by `---`

**Phases** (in order):

1. **Phase 1: Project Setup** — Infrastructure, tooling, project scaffolding. Must include tasks for:
   - Running framework initializers (e.g., `npx create-next-app@latest`, `go mod init`)
   - Monorepo directory structure creation
   - Makefile with standard targets (`dev`, `run`, `test`, `check`, plus project-specific targets)
   - Docker and docker-compose setup
   - CI/CD pipeline configuration
   - Linting, formatting, pre-commit hooks
   - For frontend apps: global styles setup, shared component library scaffold, page stubs with "X Page Coming Soon" text
   - Environment configuration templates

2. **Phase 2: Research** (optional) — Only include for complex projects requiring deep technical investigation before implementation. Each task produces a deliverable in `./research/`. Skip for straightforward projects.

3. **Phase 3: MVP** (or Phase 2 if Research is skipped) — Core features required for initial launch. Break into logical subsections with numbered action items.

4. **Phase 4: Nice to Have** (or Phase 3) — Features, polish, and production hardening that elevate the project beyond MVP.

5. **Phase 5: Future** (or Phase 4) — High-level directions, not scoped tasks. Uses the Description/Features/Rationale format instead of Description/Requirements/Implementation Notes.

**Action item format for Phases 1-4**: Each item gets exactly 3 subsections:
- **Description**: What and why
- **Requirements**: `- [ ]` checklist of concrete deliverables
- **Implementation Notes**: Technical guidance, references, trade-offs

**Action item format for Future phase**: Each item gets exactly 3 subsections:
- **Description**: What this direction is about
- **Features**: Potential features and capabilities
- **Rationale**: Why this direction is worth pursuing

Number action items as `<phase>.<item>` (e.g., `1.1`, `1.2`, `3.1`, `3.2`). Give each item a descriptive title after the number (e.g., `### 1.1 Monorepo Structure and Tooling`).

Action items should be granular enough to be individually actionable but broad enough to avoid excessive fragmentation. Target 3-8 action items per phase for most projects.
