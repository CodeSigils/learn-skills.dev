---
name: start
description: Initialize a new project by creating the .project/ directory structure. Run this first before any other skill. Creates the foundation for all subsequent work.
triggers:
  - start a new project
  - init project
  - setup project
  - initialize
  - create project structure
user-invocable: true
---

# /start — Project Initialization

Creates the `.project/` directory structure. This is the foundation — run this first before any other skill.

## When This Skill Fires

| User Says | Activation |
|-----------|------------|
| "start a new project" | Full initialization |
| "init project" | Full initialization |
| "setup project" | Full initialization |
| Any first command in a fresh project | Auto-detect → initialize |

## What This Skill Does

1. **Creates the `.project/` directory** at the root of the project
2. **Initializes all required subdirectories**:
   - `.project/idea/` — for idea documents
   - `.project/architecture/` — for design documents
   - `.project/plans/` — for implementation plans and slices
3. **Creates the master `index.md`** — the active document that tracks project state
4. **Confirms readiness** for `/idea` to be run next

## Execution Steps

### Step 1: Check Current State

Check if `.project/` already exists:
- If exists and has content → ask user: "Project already initialized. Run /idea to capture your idea, or /plan to see existing plans?"
- If doesn't exist → proceed to create

### Step 2: Create Directory Structure

Create the following:
```
.project/
├── index.md
├── idea/
│   └── .gitkeep
├── architecture/
│   └── .gitkeep
└── plans/
    └── .gitkeep
```

### Step 3: Create index.md

Write the initial index.md:

```markdown
---
created: {{CURRENT_DATE}}
status: initialized
phase: 0
---

# Project: {{PROJECT_NAME}}

**Status:** Initialized
**Phase:** 0 — Ready to capture idea
**Last Updated:** {{CURRENT_DATETIME}}

## Quick Links

- [Idea](./idea/idea.md)
- [Architecture](./architecture/design.md)
- [Plans](./plans/)

## Current Phase

Project initialized. Run `/idea` to capture what you want to build.
```

### Step 4: Update index.md

After creating structure, update `.project/index.md` to reflect the initialized state.

### Step 5: Output Confirmation

Show the user:
```
/start complete.
> Project structure created at .project/
> Next: /idea — capture your idea
```

## Data Read

None — this is the first skill, runs on fresh state.

## Data Written

```
.project/
├── index.md              # Master document with project state
├── idea/                 # (empty, ready for /idea)
├── architecture/         # (empty, ready for /architect)
└── plans/                # (empty, ready for /plan)
```

## Supporting Files

### Scripts

- `scripts/init.sh` — Alternative script to create .project structure programmatically
  - Usage: `bash scripts/init.sh "Project Name"`
  - Creates all directories and index.md automatically

### Templates

- `templates/index.md` — Template for index.md with all fields documented

## Important Notes

- **Always run this first** — No other skill should run before `/start`
- **Check before creating** — Don't overwrite existing `.project/` without asking
- **Human owns index.md** — This is an active document that all skills update
- **Naming** — Use folder name "start" (lowercase, as per agentskills.io spec)