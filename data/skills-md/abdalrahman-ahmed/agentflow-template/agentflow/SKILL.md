---
name: agentflow
description: "Autonomous multi-step agent flow sequencer and command router. Intercepts /agentflow <text> invocations, expands short instructions into execution-grade engineering briefs using workspace rules, classifies tasks, routes to the optimal model, executes autonomously, runs dynamic stack-based post-execution validation, and updates project documentation."
risk: none
source: self
date_added: "2026-07-01"
date_updated: "2026-07-01"
---

# AgentFlow Sequencer

## Purpose

A workspace-resident autonomous skill that intercepts slash-prefixed commands of the form:

```text
/agentflow <instruction>
```

It then performs an **8-step pipeline**:

1. **Intercept** — parse skill name, raw instruction, and workspace context
2. **Project Context Load** — discover and load workflow files from `.agents/workflows/`
3. **Expand** — transform the short instruction into a full engineering brief (enriched with workflow context)
4. **Classify & Route** — choose the best execution model based on domain
5. **Execute** — run the task fully autonomously, no confirmation needed
6. **Validate** *(MANDATORY)* — run post-execution verification checks based on the tech stack (automatic detection of package.json/go.mod/etc. or custom validation rules in `task-rules.md`)
7. **Memory Loop** — persist state so execution resumes after interruptions
8. **Output Contract + Workflow Sync** — return a structured result block and update workflow docs

> **Step 6 (Validate) is non-optional.** A task is NOT considered complete until validation passes. If validation fails, the agent MUST self-correct and re-validate before proceeding to Step 7.

---

## Trigger Condition

**ONLY activate when the user message starts exactly with:**

```text
/agentflow
```

Otherwise remain completely inactive.

---

## Control Commands

While a task is in progress, the following commands are recognized:

| Command | Action |
|---|---|
| `/stop` | Immediately halt current execution |
| `/pause` | Pause and save current state |
| `/resume` | Resume from last saved state |
| `/status <task-id>` | Print current execution stage and last log entry |
| `/retry <task-id>` | Re-execute the last failed step from state |

---

## Agent Protocol (Step-by-Step)

When this skill is invoked via `/agentflow <instruction>`, follow these steps:

### Stage 1: Command Interception & CLI Dispatching
Do NOT expand or execute the instruction directly in the current turn. Instead:
1. Extract the raw instruction.
2. Run the CLI dispatch script via the terminal:
   ```bash
   node .agents/skills/agentflow/scripts/agentflow.mjs "<instruction>" --conv-id <CONVERSATION_ID>
   ```
   *(Replace `<instruction>` with the raw instruction and `<CONVERSATION_ID>` with the active Conversation ID).*
3. Wait for the script to execute successfully and dispatch the expanded prompt back to the conversation.
4. Stop calling tools to end the turn.

### Stage 2: Dispatched Task Execution
When a message prefixed with `[AGENTFLOW DISPATCH]` is received in the conversation:
1. Extract the `Model`, `Domain`, and `Task ID` from the dispatch header.
2. Load relevant workflow files from `.agents/workflows/` (Step 2 below).
3. Execute the task autonomously (Step 5 below), run validation (Step 6 below), write runtime execution state to `.agents/skills/agentflow/state/<task-id>.json` (Step 7 below), and sync the updated workflows (Step 8 below).

---

### Step 2 — Project Context Load (Workflows Discovery)

**This step is mandatory before any expansion or execution.**

#### 2a — Discover Workflows Directory

Check if `.agents/workflows/` exists at the workspace root:

```
<workspace_root>/.agents/workflows/
```

#### 2b — Workflows Exist → Load and Apply

If the directory exists and contains `.md` files:

1. **List all workflow files** in the directory.
2. **Select relevant files** based on the task domain (see table below).
3. **Read and internalize** the content of selected files BEFORE writing any code.
4. **Strictly follow** any patterns, conventions, data models, or architectural decisions documented within these files. They represent the **ground truth** for this project.

**Workflow file → task domain mapping:**

| File | Use when |
|---|---|
| `project-overview.md` | Any task — always load for general context |
| `architecture.md` | Multi-file, backend, infra, design tasks |
| `database.md` | Any DB model creation, migration, or query change |
| `api-map.md` | Adding/modifying API endpoints |
| `coding-patterns.md` | Always load alongside implementation tasks |
| `task-history.md` | For context on what was previously done |
| `folder-structure.md` | Creating new files or directories |
| `workflow.md` | Lifecycle rules (local dev, review, commit, release) |
| `task-rules.md` | Custom tests and validation rules |

> **IMPORTANT:** If a workflow file documents a model, schema, or API pattern that contradicts what you would normally do, ALWAYS defer to the workflow file. It represents established, reviewed decisions for this specific project.

#### 2c — Workflows Do Not Exist → Create the Directory and Files

If `.agents/workflows/` does **not** exist, or the directory is empty:

1. **Create the directory**: `.agents/workflows/`
2. **Scan the workspace** to understand the project structure:
   - Read `README.md`, `package.json`, `go.mod`, `Cargo.toml`, etc.
   - List directories at depth 1–2 to identify tech stack and modules.
3. **Create standard workflow files** (like `project-overview.md`, `coding-patterns.md`, `folder-structure.md`, `task-history.md`, and `task-rules.md`) based on what you discover. Do **not** create placeholder files with dummy content. Every file must contain accurate information derived from actual workspace inspection.

---

### Step 3 — Prompt Expansion Engine

Transform the short instruction into an execution-grade prompt using this exact template, **enriched with context loaded from Step 2**:

```
ROLE:
<Select the most appropriate agent role for this task>

OBJECTIVE:
<Restate the user's goal as a precise, unambiguous engineering objective.
Infer missing context. Convert vague phrases into concrete targets.>

PROJECT CONTEXT:
<Summarize the relevant codebase context: tech stack, affected modules,
existing patterns, file paths, and architectural constraints.>
<Include key facts from workflow files: DB models, API conventions, coding patterns>

TASK BREAKDOWN:
1. <Atomic sub-task>
2. <Atomic sub-task>
3. <Atomic sub-task>
...

IMPLEMENTATION RULES:
- <Rule 1: follow patterns from coding-patterns.md>
- <Rule 2: respect DB schema documented in database.md>
- <Rule 3: match API conventions from api-map.md>
- <Rule 4: no breaking changes without verification>
- <Rule 5: mandatory validation after every change>

FILES TO CREATE/MODIFY:
- <path/to/file.ext> — <what changes and why>

VALIDATION PLAN:
- Test commands to run (automatically inferred or custom rules)
- Edge cases to check

EXPECTED OUTPUT:
- <Exact artifacts: code files, config changes, migration scripts, docs>
```

---

### Step 4 — Domain Classification & Model Routing

Classify the task domain then select the optimal model:

| Domain | Trigger Signals | Target Model |
|---|---|---|
| **Complex Implementation** | implement, build, refactor, fix bug, security, multi-file | `claude-opus-4.6-thinking` |
| **Standard Coding** | add, write, create function, update, patch | `claude-sonnet-4.6-thinking` |
| **Code Analysis / Audit** | audit, review, find bugs, inspect, analyze, trace | `claude-opus-4.6-thinking` |
| **Architecture / Design** | design, plan, schema, structure, diagram, model | `claude-opus-4.6-thinking` |
| **Frontend / UI** | UI, component, screen, layout, style, mockup, CSS | `claude-sonnet-4.6-thinking` |
| **Multimodal / Image** | generate image, visualize, sketch, wireframe | `gemini-3.5-flash-high` |
| **DevOps / Infra** | deploy, CI/CD, Docker, Kubernetes, env, pipeline | `gemini-3.5-flash-medium` |
| **Scripting / Automation** | script, automate, shell, task runner, cron | `gemini-3.5-flash-medium` |
| **Documentation** | document, write docs, README, changelog, explain | `gemini-3.5-flash-medium` |
| **Simple QA** | what is, explain, list, difference, describe, how does | `gemini-3.5-flash-medium` |

Routing decision logic:

```
analyze(instruction)
  → classify(domain)
  → assess(complexity: simple | standard | complex)
  → choose(target_model)
  → if multi_domain → chain(model_a → model_b)
```

---

### Step 5 — Autonomous Execution

Execute with the expanded prompt. Rules:

- **No confirmation dialogs** — proceed directly
- **No blocking** — do not wait for user approval unless explicitly required
- **Continue until:**
  - Validation (Step 6) passes
  - Blocked by truly missing external data (credentials, secrets, API keys)
  - User issues `/stop`
- **On error:** attempt self-correction up to 3 times before surfacing to user
- **Safe file modifications:** always read before writing; preserve unrelated content

---

### Step 6 — Post-Execution Validation (MANDATORY)

> **THIS STEP IS MANDATORY. A task is NOT complete until validation passes.**
> **Never skip, never summarize as "should work". Run the actual commands.**

Immediately after execution, run validation checks. The commands to execute are determined by the workspace environment and rules defined in `task-rules.md`.

#### 6a — Tech Stack Auto-Detection

If `task-rules.md` does not specify validation commands, dynamically run checks based on workspace triggers:

- **Go Project** (detected via `go.mod` or `.go` files modified):
  ```bash
  go build ./...
  go vet ./...
  ```
- **TypeScript / JavaScript Project** (detected via `tsconfig.json` or `.ts`/`.tsx` files modified):
  ```bash
  npx tsc --noEmit
  ```
- **Rust Project** (detected via `Cargo.toml`):
  ```bash
  cargo check
  ```
- **Python Project** (detected via `pyproject.toml` or `requirements.txt`):
  ```bash
  pytest
  ```

#### 6b — Custom Validation (task-rules.md)

If `.agents/workflows/task-rules.md` is present and contains validation instructions under a `# Verification` or `# Validation` section, prioritize and run those custom verification commands instead.

#### 6c — Self-Correction Protocol

If validation fails:

```
attempt = 1

while attempt <= 3:
  analyze error output
  identify root cause
  apply targeted fix (read file before editing)
  re-run validation command
  if passes → break
  attempt += 1

if attempt > 3:
  surface error to user with full context
  do NOT update workflow files
  mark task as "failed" in state
```

#### 6d — Validation Result Recording

After validation passes, record the outcome:

```json
{
  "validation": {
    "commands": ["npm test", "npx tsc --noEmit"],
    "self_corrections": 0,
    "status": "passed"
  }
}
```

---

### Step 7 — Memory + Context Loop

Persist execution state to:

```
.agents/skills/agentflow/state/<task-id>.json
```

If execution is interrupted, reload this file and resume from `steps_pending`.

---

### Step 8 — Output Contract + Workflow Sync

#### 8a — Workflow File Update (MANDATORY on success)

After a task completes **successfully and validation passes**, you **MUST** update the relevant workflow files in `.agents/workflows/` to reflect the changes made. This is non-optional.

**Update rules:**

| What changed | Which file to update |
|---|---|
| New DB table or model field added | `database.md` — add the table/field documentation |
| New API endpoint added or modified | `api-map.md` — add/update the route documentation |
| New coding pattern established | `coding-patterns.md` — document the pattern |
| Architecture decision made | `decisions.md` — add an ADR entry |
| Completed task | `task-history.md` — append a new task entry |
| New directory or file structure change | `folder-structure.md` — update the tree |

**task-history.md entry format** (always append, never overwrite existing entries):

```markdown
## Task N: <Short Title>
- **Objective**: <What was the goal>
- **Key Changes**:
  - **<Area>**:
    - [filename](file:///absolute/path): <What changed and why>
- **Verification**:
  - Commands run and exit code status
  - Self-corrections needed: <N>
```

> **Do not update workflow files if the task failed or was stopped.** Only update on confirmed successful completion with passing validation.

#### 8b — Output Block

Always return this exact structured block upon completion:

```
[SKILL]
agentflow

[INTERPRETED TASK]
<Plain-English restatement of what was understood>

[EXPANDED PROMPT]
<The full ROLE / OBJECTIVE / TASK BREAKDOWN / etc. block>

[SELECTED AGENT]
Model: <target_model>
Domain: <domain>
Confidence: <0.0–1.0>

[EXECUTION PLAN]
1. <Step>
2. <Step>
3. <Step>

[VALIDATION]
- Commands run: <commands list>
- Self-corrections: <N>
- Status: PASSED ✅ | FAILED ❌

[RESULT]
<Summary of what was done, files changed, and validation outcome>
```

> If validation FAILED, the `[RESULT]` block must include the error output and a clear explanation of why the task could not be completed.

---

## Script Integration

This skill also ships with a standalone CLI script for terminal-based invocation:

```bash
node .agents/skills/agentflow/scripts/agentflow.mjs \
  "<instruction>" \
  --conv-id <CONVERSATION_ID>
```

The script:
1. Expands the prompt locally
2. Classifies domain using Gemini via `agy`
3. Dispatches the expanded brief back via `agentapi send-message`

---

## References

- [`references/expansion-templates.md`](references/expansion-templates.md) — Domain-specific prompt expansion templates
- [`references/execution-examples.md`](references/execution-examples.md) — Concrete invocation and output examples
- [`scripts/agentflow.mjs`](scripts/agentflow.mjs) — CLI dispatch script
- [`state/`](state/) — Runtime execution state directory
- [`.agents/workflows/`](../../workflows/) — Project workflow documentation (auto-created/updated)
