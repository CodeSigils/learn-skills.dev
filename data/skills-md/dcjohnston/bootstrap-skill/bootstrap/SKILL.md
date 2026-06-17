---
name: bootstrap
description: Bootstrap a new Claude Code project from scratch — brainstorm, plan architecture, create sub-agents, install skills, write CLAUDE.md with orchestration guidance. Use when starting a greenfield project or restructuring an existing one for agent-driven development.
---

# Bootstrap Skill

Scaffold a new project for agent-driven development with Claude Code. This skill guides you through the full bootstrapping process: brainstorming, architecture, sub-agent creation, skill installation, and orchestrator CLAUDE.md setup.

## When to Use This Skill

- Starting a brand new project from scratch
- Restructuring an existing project for Claude Code agent workflows
- Adding sub-agent infrastructure to a project that doesn't have it
- User says "bootstrap", "scaffold", "set up a new project", "start a new project"

## When NOT to Use This Skill

- Project already has CLAUDE.md + sub-agents + skills set up
- User just wants to add a single feature to an existing project
- User wants to install a specific skill (use `npx skills find` instead)

## The Bootstrap Process

Follow these phases in order. Each phase builds on the previous one.

### Phase 1: Brainstorm & Scope

**Goal:** Understand what the user wants to build and nail down key decisions.

Ask the user about:
1. **What they're building** — elevator pitch, core functionality
2. **Tech stack** — language, framework, key libraries (or let them choose)
3. **Architecture** — monolith vs pipeline vs API vs CLI vs full-stack
4. **Key integrations** — external APIs, databases, services
5. **Scope** — hackathon MVP vs production system

Use `AskUserQuestion` to gather decisions efficiently. Present 2-4 options per question with clear tradeoffs. Don't over-ask — 3-5 questions max to get started.

**Output:** A clear mental model of what's being built and the major technical decisions.

### Phase 2: Design the Work Breakdown

**Goal:** Identify the independent workstreams that will become sub-agents.

Principles for splitting work into agents:
- Each agent should own a **coherent, independent** piece of the system
- Agents should communicate through **well-defined interfaces** (files, JSON, APIs)
- Aim for **3-6 agents** — fewer than 3 means you're not parallelizing enough, more than 6 means you're over-splitting
- Each agent needs a clear **scope boundary** — what files it owns, what it reads, what it writes

Common patterns:
| Project Type | Typical Agent Split |
|---|---|
| Data pipeline | One agent per stage (ingest, transform, output) |
| Full-stack app | frontend-agent, api-agent, db-agent |
| CLI tool | core-agent, io-agent, test-agent |
| Multi-service | One agent per service |
| ML project | data-agent, model-agent, eval-agent, serving-agent |

**Output:** A list of 3-6 agents with names, scopes, and owned files.

### Phase 3: Project Scaffolding

**Goal:** Create the project structure, package config, and entry points.

Steps:
1. Initialize the project with the appropriate package manager
2. Create the directory structure (see [project-structure.md](./references/project-structure.md))
3. **Set up code quality tooling** (linting, formatting, type checking)
4. Set up the entry point / CLI
5. Create placeholder files for each module
6. Create the test directory structure
7. Install dependencies
8. Verify all tools pass on the placeholder code

Language-specific setup:
| Language | Package Manager | Config File | Layout | Linter/Formatter | Type Checker |
|---|---|---|---|---|---|
| Python | `uv init --package` | `pyproject.toml` | `src/` layout | **ruff** (lint + format) | **mypy** (strict mode) |
| TypeScript | `npm init` / `pnpm init` | `package.json` + `tsconfig.json` | `src/` layout | **eslint** + **prettier** | **tsc** (`strict: true`) |
| Rust | `cargo init` | `Cargo.toml` | `src/` layout | **clippy** + **rustfmt** | Built-in (compiler) |
| Go | `go mod init` | `go.mod` | flat or `cmd/` + `internal/` | **golangci-lint** + **gofmt** | Built-in (compiler) |

#### Code Quality Tooling (Required)

Every bootstrapped project must include linting, formatting, and type checking from day one. This catches bugs early and keeps sub-agent output consistent.

**Python example** (`pyproject.toml`):
```toml
[dependency-groups]
dev = ["pytest>=8.0", "pytest-cov>=6.0", "ruff>=0.9", "mypy>=1.10"]

[tool.ruff]
src = ["src"]

[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP", "RUF"]

[tool.mypy]
strict = true
plugins = ["pydantic.mypy"]  # if using pydantic
```

**TypeScript example** (`tsconfig.json`):
```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true
  }
}
```

**Verify:** The project builds/runs with placeholder implementations, and `lint + typecheck` pass clean.

### Phase 4: Create Sub-Agents

**Goal:** Write agent definition files in `.claude/agents/`.

Create one `.md` file per agent in `.claude/agents/`. Each file follows this structure:

```markdown
---
name: {agent-name}
description: {One-line description of what this agent does.}
tools: Read, Write, Edit, Glob, Grep, Bash
skills: {comma-separated skill names}
model: sonnet
maxTurns: 25
---

{System prompt for the agent — see template}
```

The system prompt should include:
- **Scope** — what files the agent owns
- **Key files to read first** — so the agent gets oriented
- **What it builds** — specific functions/classes/modules
- **Design principles** — constraints and patterns to follow
- **Commands** — how to test and run its work

See [agent-template.md](./references/agent-template.md) for the full template.

### Phase 5: Install Skills

**Goal:** Give agents the specialized knowledge they need.

Search for relevant skills:
```bash
npx skills find {query}
```

Install skills that match the project's tech stack:
```bash
npx skills add {owner/repo@skill} -y
```

Common skills to consider:
| Domain | Search Query |
|---|---|
| Python tooling | `modern-python` |
| Data validation | `pydantic` |
| React/frontend | `react best practices` |
| Testing | `testing` |
| API design | `fastapi`, `api design` |
| TypeScript | `typescript` |

Only install skills that at least 2 agents will use, or that are central to the project. Don't over-install.

### Phase 6: Write CLAUDE.md

**Goal:** Create the orchestrator instructions that tie everything together.

The CLAUDE.md is the most important file. It tells Claude Code how to work on this project. It must include:

1. **Project description** — what it is, one paragraph
2. **Delegation instructions** — the orchestrator pattern (see [orchestrator-template.md](./references/orchestrator-template.md))
3. **Agent table** — all sub-agents with files, scope, and skills
4. **Architecture overview** — how the pieces fit together, data flow
5. **Project structure** — key directories and files
6. **Commands** — how to build, test, run, lint
7. **Key APIs / environment variables** — what external services are used

The delegation section is critical. It should include:
- When to delegate vs work directly
- How to delegate effectively (be precise, include context, specify verification)
- Anti-patterns to avoid
- Guidance on parallelizing agent work

### Phase 7: Verify

**Goal:** Confirm everything works before starting real implementation.

Checklist:
- [ ] Project builds/installs without errors
- [ ] Entry point runs (even if it just prints "not implemented")
- [ ] Tests pass (even if they're just placeholders)
- [ ] Linter passes clean (ruff / eslint / clippy)
- [ ] Type checker passes clean (mypy strict / tsc strict)
- [ ] Formatter produces no changes (ruff format / prettier)
- [ ] All agent files exist in `.claude/agents/`
- [ ] CLAUDE.md is complete and accurate
- [ ] CLAUDE.md commands section includes lint, format, and typecheck commands
- [ ] Skills are installed and accessible
- [ ] Seed data / config files exist

## Tips

- **Start with the agent split, not the code.** The architecture of your agents shapes everything else.
- **Agents should be embarrassingly parallel.** If agent A needs agent B's output to start, they're too coupled. Use file-based interfaces.
- **The CLAUDE.md delegation section pays for itself 100x.** Spend time on it. Bad delegation instructions = bad agent output.
- **Install skills early.** They inform how agents write code.
- **Seed data is underrated.** Having a `data/` directory with example inputs means you can test each stage independently from day 1.
