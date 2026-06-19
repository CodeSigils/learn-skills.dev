---
name: spec-skill
description: "Comprehensive specification-driven development system for structured project planning and execution. Slash commands: /new-project, /plan, /execute, /verify, /health, /help, /next, /quick, /transition, /map-codebase. Use when starting new projects, managing complex tasks, or ensuring code quality. ENFORCES a strict 'Ask-Plan-Execute' workflow where user confirmation is REQUIRED before code generation."
---

# Specification Driven Development

## Overview

Spec-driven-dev is a structured development system that transforms vague ideas into executable plans through systematic questioning, research, planning, and verification. Inspired by get-shit-done (GSD), it provides templates and workflows for managing software projects from conception to completion.

**CRITICAL RULE**: You must **STOP and WAIT** for user confirmation at specific checkpoints. Do not rush from planning to execution in a single turn.

## Commands

All commands are invoked as `/spec-<name>` (e.g., `/spec-new`, `/spec-plan 1`). Commands automatically load the relevant workflow docs.

### Core Workflow Commands

| Command | Alias | What it does |
|---------|-------|--------------|
| `/spec-new` | `/new-project` | Full initialization: questions → requirements → roadmap. Creates `.planning/` structure |
| `/spec-plan <N>` | `/plan`, `/plan-phase` | Research + create executable PLAN.md for phase N |
| `/spec-execute <N>` | `/execute`, `/execute-phase` | Execute all plans for phase N in parallel waves |
| `/spec-verify <N>` | `/verify`, `/verify-work` | Verify phase N completion: must_haves check, UAT, gap analysis |
| `/spec-transition` | `/transition` | Complete current phase, update context, prepare next phase |
| `/spec-next` | `/next` | Auto-detect current state and run the next logical step |

### Utility Commands

| Command | What it does |
|---------|--------------|
| `/spec-health [--repair]` | Validate `.planning/` directory integrity. `--repair` auto-fixes missing files |
| `/spec-help` | Show all commands and usage guide |
| `/spec-quick <task>` | Execute ad-hoc task with atomic commits, skip full planning |
| `/spec-map-codebase [area]` | Analyze existing codebase for brownfield projects |
| `/spec-config` | Show or update `.planning/config.json` settings |

### Command Workflow Mapping

| Command | Loads Workflow | Produces |
|---------|---------------|----------|
| `/spec-new` | `workflows/health.md` (init check) | PROJECT.md, REQUIREMENTS.md, ROADMAP.md, STATE.md, config.json |
| `/spec-plan <N>` | `references/questioning.md` | `NN-CONTEXT.md`, `NN-RESEARCH.md`, `NN-MM-PLAN.md` |
| `/spec-execute <N>` | `workflows/execute-plan.md` | Code changes, atomic commits, `NN-MM-SUMMARY.md` |
| `/spec-verify <N>` | `workflows/verify-work.md` | `NN-VERIFICATION.md`, `NN-UAT.md`, fix plans if needed |
| `/spec-transition` | `workflows/transition.md` | Updated PROJECT.md, ROADMAP.md, STATE.md |
| `/spec-health` | `workflows/health.md` | Health report, auto-repairs if `--repair` |
| `/spec-quick` | *(inline lightweight)* | Quick plan + summary in `.planning/quick/` |
| `/spec-map-codebase` | `templates/codebase/*.md` | `.planning/codebase/*.md` analysis documents |

### Quick Usage Examples

```
/spec-new                          # Start fresh project
/spec-plan 1                       # Plan phase 1
/spec-execute 1                    # Execute phase 1
/spec-verify 1                     # Verify phase 1
/spec-transition                   # Move to phase 2
/spec-health --repair              # Fix missing planning files
/spec-quick "Add dark mode toggle" # Ad-hoc task
/spec-map-codebase api             # Analyze API layer
```

## Configuration

Project settings are stored in `.planning/config.json`. Key settings:

| Setting | Options | Default | Purpose |
|---------|---------|---------|---------|
| `mode` | `interactive`, `yolo` | `interactive` | Confirm vs auto-approve at each step |
| `granularity` | `coarse`, `standard`, `fine` | `standard` | Phase granularity (3-5 / 5-8 / 8-12 phases) |
| `workflow.discuss_mode` | `discuss`, `assumptions` | `discuss` | Interview vs codebase-first discovery |
| `workflow.research` | boolean | `true` | Research domain before planning |
| `parallelization.enabled` | boolean | `true` | Run independent plans simultaneously |

See `templates/config.json` for the full schema with all workflow toggles, gates, safety settings, and parallelization controls.

## Core Workflow

### 1. Project Initialization
Start by creating the foundational project context:

```bash
# Create project planning structure
mkdir -p .planning/phases
```

**Key documents created:**
- `.planning/PROJECT.md` - Project vision and context
- `.planning/REQUIREMENTS.md` - Scoped feature requirements
- `.planning/ROADMAP.md` - Phase decomposition
- `.planning/STATE.md` - Project memory and decisions
- `.planning/config.json` - Workflow preferences

### 2. Requirements Discussion (Interactive - BLOCKING)
**Goal**: Fully understand the user's intent before generating any files. **You MUST engage in a dialogue.**

**Resources**:
- Refer to `references/questioning.md` for questioning strategies and mental models.

**Actions**:
1. **Start Open**: Ask "Tell me about what you want to build."
2. **Loop (Ask -> Wait -> Ask)**:
   - Ask clarifying questions about features, constraints, and tech stack.
   - **WAIT** for the user's answer.
   - Challenge vagueness and clarify boundaries based on the answer.
   - **REPEAT** until you have a clear mental model.
3. **Summarize**: Present a summary of requirements and scope.
4. **STOP**: Ask "Do we have enough details to proceed to planning? Or should we discuss more?"
5. **WAIT**: Do not generate any Roadmap or Plan files until the user explicitly says "Proceed to Plan".

### 3. Roadmap Planning
**Only proceed here after user confirmation.**
Decompose the confirmed requirements into a phased roadmap:

**Phase structure:**
- **Integer phases** (1, 2, 3): Planned milestone work
- **Decimal phases** (2.1, 2.2): Urgent insertions
- **Dependency tracking**: Clear phase dependencies
- **Success criteria**: Observable behaviors for verification

### 4. Per-Phase Analysis & Discussion (BLOCKING)
Before planning **every phase**, re-analyze context and run a focused discussion loop.

**Resources**:
- Refer to `references/questioning.md` for phase-level clarification patterns.

**Actions**:
1. **Analyze Phase Context**: Review `.planning/PROJECT.md`, `.planning/ROADMAP.md`, `.planning/STATE.md`, and dependency phases.
2. **Loop (Ask -> Wait -> Ask)**:
   - Ask phase-specific clarifying questions about scope, constraints, interfaces, and acceptance criteria.
   - **WAIT** for the user's answer.
   - Refine unclear assumptions and identify missing decisions.
   - **REPEAT** until phase boundaries are unambiguous.
3. **Summarize**: Present phase scope, risks, decisions, and success criteria.
4. **STOP**: Ask "Do we have enough details for this phase plan?"
5. **WAIT**: Do not create/update this phase's `PLAN.md` until the user explicitly says "Proceed to Phase Plan".

### 5. Phase Planning & Review (BLOCKING)
Create the detailed execution plan for the current phase, but **do not execute yet**. This step repeats for each phase.

**Resources**:
- Refer to `references/verification-patterns.md` to define goal-backward verification criteria.

**Actions**:
1. Create/Update `.planning/phases/XX-phase/XX-PLAN.md`.
2. **Define Verification (must_haves)**: In the YAML frontmatter, define `must_haves` (`truths`, `artifacts`, `key_links`) based on the phase goal.
3. **Plan Tasks**: Break down implementation steps to satisfy verification criteria. Use `<read_first>` tags in tasks to define files that must be read before execution, and `<acceptance_criteria>` for grep-verifiable conditions.
4. **Review**: Check plan against the "Plan Verification Checklist".
5. **STOP**: Present the full plan content to the user.
6. **ASK**: "Here is the detailed plan. Does this look correct? Shall I proceed with execution?"
7. **WAIT**: Do not write any code until the user explicitly says "Yes" or "Proceed".

### 6. Phase Execution
**Only proceed here after user confirmation of the PLAN.**
Execute the **approved** plan step-by-step.

**Resources**:
- Refer to `workflows/execute-plan.md` for the complete execution workflow including pre-execution checks, task execution order, verification rules, atomic commit strategy, and error recovery.
- Refer to `templates/continue-here.md` for session handoff when pausing mid-execution.

**Plan components:**
- **Tasks**: Specific, actionable implementation steps with concrete values
- **Dependencies**: Plan-to-plan dependency graphs managed via wave groups
- **Waves**: Parallel execution groups — independent plans run together
- **Verification**: Executing the defined verification and acceptance criteria
- **Checkpoints**: User interaction points (decisions, visual verification)
- **user_setup**: External service configuration the user must complete

### 7. Verification & Summary
Ensure quality and document outcomes:

**Resources**:
- Refer to `workflows/verify-work.md` for the complete verification workflow: automated checks, must-haves verification, UAT generation, and gap handling.
- Refer to `workflows/transition.md` for phase completion and transition to the next phase.
- Refer to `workflows/health.md` for planning directory integrity checks and auto-repair.
- Refer to `references/verification-patterns.md` for verification types and workflows.
- Refer to `templates/verification-report.md` for the verification report template.
- Refer to `templates/UAT.md` for user acceptance testing documentation.

**Verification types:**
- **Automated**: Tests, linting, build checks
- **Manual**: User verification of UI/UX via checkpoint tasks
- **Must-Haves**: Goal-backward verification (truths, artifacts, key_links)
- **Integration**: System integration testing
- **Documentation**: Update project context

After verification, refer to `workflows/transition.md` for the phase completion checklist and preparation for the next phase.

## Templates & Patterns

All templates are in the `templates/` directory. See `templates/README.md` for the canonical artifact registry — the authoritative index of all `.planning/` artifacts.

### Core Planning Templates
- `templates/PROJECT.md` — Project vision, requirements, constraints, key decisions
- `templates/ROADMAP.md` — Phase decomposition with success criteria and progress tracking
- `templates/STATE.md` — Cross-session memory: position, decisions, blockers, performance
- `templates/REQUIREMENTS.md` — Scoped functional requirements with traceability
- `templates/config.json` — Workflow configuration (gates, parallelization, quality settings)

### Phase Execution Templates
- `templates/PLAN.md` — Executable phase plan with XML task structure, must_haves, user_setup
- `templates/SUMMARY.md` — Post-execution summary with frontmatter for context assembly
- `templates/discovery.md` — Phase discussion decisions and context capture
- `templates/VALIDATION.md` — Validation architecture with Given/When/Then scenarios
- `templates/UAT.md` — User acceptance testing results with issue tracking
- `templates/verification-report.md` — Post-execution verification against must_haves
- `templates/continue-here.md` — Session handoff for paused work

### Brownfield Analysis Templates
- `templates/codebase/structure.md` — Directory organization and key modules
- `templates/codebase/architecture.md` — Design patterns and component relationships
- `templates/codebase/stack.md` — Technology stack with versions
- `templates/codebase/conventions.md` — Coding conventions and patterns
- `templates/codebase/integrations.md` — External services and dependencies
- `templates/codebase/testing.md` — Testing approach and coverage
- `templates/codebase/concerns.md` — Known issues and technical debt

### Workflow Documentation
- `workflows/execute-plan.md` — Step-by-step plan execution with verification and error recovery
- `workflows/verify-work.md` — Phase completion verification including must_haves checking
- `workflows/transition.md` — Phase completion, context updates, and next phase preparation
- `workflows/health.md` — Planning directory integrity validation and auto-repair

### Project Template (PROJECT.md)
See `templates/PROJECT.md` for the full template with guidelines, evolution rules, and brownfield support.

### Phase Plan Template (PLAN.md)
See `templates/PLAN.md` for the full template with frontmatter fields, XML task structure, must_haves verification, user_setup for external services, TDD plans, and parallel execution patterns.

### Roadmap Template (ROADMAP.md)
See `templates/ROADMAP.md` for the full template with phase numbering, decimal insertions, milestone grouping, and progress tracking.

## Implementation Examples

### Example 1: New Web Application
```
User: "I want to build a todo app with user authentication"

Workflow:
1. Initialize project: Create PROJECT.md with core value "Simple, reliable todo management"
2. Requirements Discussion: Clarify "user authentication" (Email/Password? OAuth? JWT?)
3. Roadmap: Phase 1 (Auth), Phase 2 (Todo CRUD), Phase 3 (Advanced features)
4. Per-Phase Discussion (Phase 1): Reconfirm auth boundaries and constraints
5. Plan Review (Phase 1): Present Phase 1 plan for user approval
6. Execution (Phase 1): Implement auth with verification tests
7. Repeat steps 4-6 for each subsequent phase
```

### Example 2: API Service
```
User: "Build a REST API for inventory management"

Workflow:
1. Initialize: PROJECT.md with value "Reliable inventory tracking API"
2. Requirements Discussion: Define API surface, database choice, and auth strategy
3. Roadmap: Phase 1 (Basic CRUD), Phase 2 (Search), Phase 3 (Auth), Phase 4 (Reporting)
4. Per-Phase Discussion (Phase 1): Confirm endpoint scope and data model details
5. Plan Review (Phase 1): Confirm endpoints and data models
6. Execution (Phase 1): Implement endpoints with tests
7. Repeat steps 4-6 for each subsequent phase
```

## Best Practices

### 1. Context Management
- **Discuss before planning**: Ensure alignment on requirements via `workflows/transition.md` and `templates/discovery.md`
- **Confirm before executing**: User must approve the plan
- **Keep STATE.md updated** with all key decisions
- **Use SUMMARY.md** for each completed plan with full frontmatter for automatic context assembly
- **Reference dependencies** explicitly in phase plans via `depends_on` and `wave` fields
- **Maintain clean separation** between planning and execution
- **Session continuity**: Use `templates/continue-here.md` when pausing mid-work

### 2. Verification Strategy
- **Goal-backward verification**: Define `must_haves` (truths, artifacts, key_links) in the plan frontmatter before implementation. See `templates/PLAN.md` for the full structure.
- **Task-level verification**: Define grep-verifiable `acceptance_criteria` for each `<task>`
- **Automated checks**: Tests, linting, type checking — see `workflows/verify-work.md`
- **User verification**: Checkpoints for UI/UX validation via `checkpoint:human-verify` tasks
- **Integration testing**: End-to-end workflow validation
- **Verification reporting**: Use `templates/verification-report.md` to document results

### 3. Phase Design
- **Small, focused phases**: 2-3 plans per phase (~50% context max per plan)
- **Clear dependencies**: Explicit phase-to-phase and plan-to-plan dependencies via wave groups
- **Measurable outcomes**: Each phase delivers testable functionality with success criteria
- **Progressive disclosure**: Build complexity gradually
- **Parallel execution**: Independent plans run in same wave — see `templates/PLAN.md` for parallel patterns
- **External services**: Declare in `user_setup` frontmatter — AI can't create API keys or configure dashboards

## Resources

This skill includes resource directories for commands, templates, references, and scripts:

### commands/
Slash command definitions that trigger specific workflows. Each command file describes the workflow, inputs, outputs, and rules for that operation.

**Commands in this skill:**
- `commands/spec/new.md` — `/spec-new`: Initialize a new project
- `commands/spec/plan.md` — `/spec-plan <N>`: Plan a phase
- `commands/spec/execute.md` — `/spec-execute <N>`: Execute a phase
- `commands/spec/verify.md` — `/spec-verify <N>`: Verify phase completion
- `commands/spec/transition.md` — `/spec-transition`: Complete and prepare next phase
- `commands/spec/next.md` — `/spec-next`: Auto-detect next step
- `commands/spec/help.md` — `/spec-help`: Show command reference
- `commands/spec/quick.md` — `/spec-quick`: Execute ad-hoc task
- `commands/spec/health.md` — `/spec-health [--repair]`: Check directory integrity
- `commands/spec/map-codebase.md` — `/spec-map-codebase`: Analyze existing codebase
- `commands/spec/config.md` — `/spec-config`: Manage configuration

### workflows/
Executable code (Python/Bash/etc.) that can be run directly to perform specific operations.

**Scripts in this skill:**
- `scripts/init_project.py` - Initialize a spec-driven project structure from templates.
  - Usage: `python scripts/init_project.py <project_name>`
  - Run when: Starting a new project or reinitializing missing planning scaffolding.
- `scripts/validate_project.py` - Validate required planning files, directory structure, and phase artifacts.
  - Usage: `python scripts/validate_project.py [project_path]`
  - Run when: Before phase execution, after major planning updates, and before handoff.
- `scripts/package_skill.py` - Package this skill into a distributable zip with manifest metadata.
  - Usage: `python scripts/package_skill.py [skill_path]`
  - Run when: Releasing or sharing the skill.

**Appropriate for:** Python scripts, shell scripts, or any executable code that performs automation, data processing, or specific operations.

**Note:** Scripts may be executed without loading into context, but can still be read for patching or environment adjustments.

### workflows/
Step-by-step workflow documentation for each phase of the spec-driven process. Load these into context when executing specific workflows.

**Workflows in this skill:**
- `workflows/execute-plan.md` — Task execution, atomic commits, verification, error recovery
- `workflows/verify-work.md` — Must-haves verification, UAT, gap handling
- `workflows/transition.md` — Phase completion, context updates, next phase preparation
- `workflows/health.md` — Directory integrity validation and auto-repair

### scripts/
Executable code (Python/Bash/etc.) that can be run directly to perform specific operations.

**Scripts in this skill:**
- `scripts/init_project.py` - Initialize a spec-driven project structure from templates
- `scripts/validate_project.py` - Validate required planning files, directory structure, and phase artifacts
- `scripts/package_skill.py` - Package this skill into a distributable zip with manifest metadata

**Appropriate for:** Python scripts, shell scripts, or any executable code that performs automation, data processing, or specific operations.

### references/
Documentation and reference material intended to be loaded into context to inform Claude's process and thinking.

**Examples from other skills:**
- Product management: `communication.md`, `context_building.md` - detailed workflow guides
- BigQuery: API reference documentation and query examples
- Finance: Schema documentation, company policies

**Appropriate for:** In-depth documentation, API references, database schemas, comprehensive guides, or any detailed information that Claude should reference while working.

### assets/
Files not intended to be loaded into context, but rather used within the output Claude produces.

**Examples from other skills:**
- Brand styling: PowerPoint template files (.pptx), logo files
- Frontend builder: HTML/React boilerplate project directories
- Typography: Font files (.ttf, .woff2)

**Appropriate for:** Templates, boilerplate code, document templates, images, icons, fonts, or any files meant to be copied or used in the final output.

---

**Any unneeded directories can be deleted.** Not every skill requires all three types of resources.
