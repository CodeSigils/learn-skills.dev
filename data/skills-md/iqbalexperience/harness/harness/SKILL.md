---
name: harness
description: "The team-architecture factory for AI agents — turns a domain description into an agent team and their skills for any project. Use when asked to 'build a harness', 'design an agent team', 'harness engineering', 'scaffold agents and skills', or when auditing and extending existing multi-agent harnesses."
---

# Harness — Agent Team & Skill Architect (Open Agent Skills Ecosystem)

A meta-skill that turns a single-sentence domain description into a coordinated agent team and the procedural skills they use.

**Core Principles:**
1. **Scaffold Agent Definitions & Skills:** Generate agent role definitions (`.agents/agents/` or `.claude/agents/`) and procedural skills (`.agents/skills/` or `.claude/skills/`).
2. **Prioritize Agent Teams:** Default to multi-agent team mode for collaborative task execution with direct peer communication and shared task lists.
3. **Register Harness Pointer in AGENTS.md / CLAUDE.md:** Keep context lean by recording only minimal pointers (trigger rules + change log) in `AGENTS.md` (or `CLAUDE.md`).
4. **Continuous Harness Evolution:** Treat harnesses as evolving systems that adapt based on execution feedback, updating agents, skills, and documentation iteratively.

## Workflow

### Phase 0: Audit & Current State Assessment
When triggered, inspect the existing harness configuration:
1. Read `.agents/agents/` (or `.claude/agents/`), `.agents/skills/` (or `.claude/skills/`), and `AGENTS.md` (or `CLAUDE.md`).
2. Determine execution branch:
   - **New Scaffold:** Directories are empty or missing → Run full pipeline from Phase 1.
   - **Extension:** Harness exists and new agents/skills requested → Execute relevant phases based on extension matrix.
   - **Operations / Maintenance:** Audit, sync, or fix existing harness → Follow Phase 7-5 workflow.
3. Detect schema or documentation drift between agent files and pointer logs.
4. Present audit summary and get plan confirmation from the user.

### Phase 1: Domain Analysis
1. Analyze user request to extract target domain and project scope.
2. Identify core task categories (generation, verification, editing, analysis, deployment).
3. Check code base structure (tech stack, data models, major modules).
4. Detect user expertise level and adjust communication tone accordingly.

### Phase 2: Team Architecture Design
#### 2-1. Select Execution Mode
- **Agent Team (Default):** For 2+ agents requiring real-time coordination, direct messaging, and shared task boards.
- **Subagents (Alternative):** For isolated single-agent subtasks where only return values matter.
- **Hybrid:** Mix modes per phase (e.g., parallel subagents for data collection → agent team for consensus integration).

#### 2-2. Select Architecture Pattern
Choose from 6 pre-defined patterns (see `skills/harness/references/agent-design-patterns.md`):
1. **Pipeline:** Sequential dependent tasks.
2. **Fan-out / Fan-in:** Parallel independent tasks merged at end.
3. **Expert Pool:** Context-driven selection of specialized agents.
4. **Producer-Reviewer:** Generator + Quality Assurance checker loop.
5. **Supervisor:** Central controller managing state and dynamic dispatch.
6. **Hierarchical Delegation:** Recursive parent-child delegation tree.

### Phase 3: Agent Definition Generation
- Check for duplicate existing agents in `.agents/agents/` or `.claude/agents/`.
- Every agent MUST be defined in `.agents/agents/{name}.md` (or `.claude/agents/{name}.md`).
- Define role, core principles, input/output protocols, error handling, and team communication contracts.

### Phase 4: Skill Generation
Create procedural skills following the Open Agent Skills standard (`.agents/skills/{name}/SKILL.md` or `.claude/skills/{name}/SKILL.md`).
- **Structure:**
  ```text
  skill-name/
  ├── SKILL.md (Required: YAML frontmatter + markdown instructions)
  └── Bundled Resources (Optional: scripts/, references/, templates/)
  ```
- **Progressive Disclosure:** Keep `SKILL.md` lean (<500 lines), moving detailed reference guides to `references/`.
- **Pushy Descriptions:** Write active, explicit trigger descriptions so agents invoke skills reliably.

### Phase 5: Integration & Orchestration
- Scaffold an orchestrator skill connecting agents, data passing protocols, and error fallback handlers.
- Register harness pointer (trigger rules + change log) in `AGENTS.md` (or `CLAUDE.md`).

### Phase 6: Validation & Testing
- Validate file structure, trigger boundaries (should-trigger vs should-not-trigger near-miss queries), dry-run execution, and baseline comparison.
