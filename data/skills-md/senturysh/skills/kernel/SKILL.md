---
name: kernel
description: >
  Implements a stateless autonomous agent loop where you operate like a CPU cycle:
  waking up with no memory, checking a task manager, reading memory logs, executing programs, and
  tagging all output so future cycles can resume seamlessly. Use this skill whenever the user wants
  you to run autonomously across sessions, persist state between runs, manage tasks across cycles,
  collaborate with other agents, or simulate a 24/7 always-on AI agent system. Trigger on phrases
  like "run as agent", "autonomous loop", "kernel", "task manager cycle", "persistent agent", or
  "continue from last run".
---

# Agent Loop Skill

## Concept

You operate as a **stateless CPU cycle**. Each run:
1. Starts with zero memory of previous runs
2. Recovers state by reading the Task Manager and Memory Log
3. Executes programs defined in HBP format
4. Tags every output so the next cycle can resume exactly where this one left off

All output is logged. The log is shared across all cycles.

---

## Startup Sequence (Every Cycle)

Execute these steps in order at the start of every run:

### Step 0 — Check What Happened in Previous Run
Read the previous memory for the last 50–200 lines.

```
[SYSTEM] Reading Memory...
memory_recent(lines=100)
```

### Step 1 — Check Task Manager
Read the Task Manager to discover all active tasks from previous cycles.

```
[SYSTEM] Checking Task Manager...
task_list(status=running)
task_list(status=blocked)
task_list(status=pending)
```

### Step 2 — Load Memory for Each Active Task
For each active task, load prior memory using the `[program][task]` tag.

```
[SYSTEM] Loading memory for [program][task]...
memory_read_program_task(program, task, limit=50, order=desc)
```

### Step 3 — Execute Programs
Resume or start execution for each task. Begin all output with the task tag.

### Step 4 — End-of-Cycle Summary
Generate a short, concise summary tagged with `[program][task]` so the next cycle can orient quickly.

---

## Output Tagging Format

Every line of substantive output must begin with:
```
[program-name][START] Now i am starting to execute...
[program-name][task-name]
[program-name][END]
```

Example:
```
[make-website][START] Now i am starting to execute...
[make-website][build-frontend] Continuing CSS grid layout. Setting up responsive breakpoints at 768px and 1200px.
[make-website][build-frontend] Header component complete. Starting navigation bar.
[make-website][END]
```

This tag is how future cycles find relevant memory entries. Without it, continuity breaks.

---

## Task Manager

The Task Manager is a persistent list of all programs and tasks. Update it any time a task is created, completed, or changed.

### Task Entry Format
```
[program][task] | status: pending | running | done | blocked | raised
```

### Task Lifecycle
- **Create**: Add entry when starting a new program/task — before executing
- **Update**: Record progress, blockers, and state in `description` and `references`
- **Complete**: Mark `status: done` — do not delete (memory must stay searchable)

### Task Fields
- `status`: `pending` | `running` | `done` | `blocked` | `raised`
- `priority`: `low` | `normal` | `high` | `critical`
- `resolvedAt`: auto-set when `done`, cleared when status changes
- `parentId`: links subtasks to parent task

### Task Description Best Practices
The description field is indexed for search — use concrete, searchable terms.

```
✓ GOOD: "API integration: auth done, working on rate limiting (Redis)"
✗ BAD:  "working on it"

✓ GOOD: "waiting on brand guidelines from design team"
✗ BAD:  "paused"
```

### Example Task Manager State
```
[make-website][build-frontend]  | status: running  | description: grid layout done, starting nav
[make-website][write-copy]      | status: blocked  | description: waiting on brand guidelines
[data-pipeline][fetch-sources]  | status: done     | description: 3 sources integrated
```

---

## MCP Tool Reference

**Use MCP tools exclusively.**

### Inbox / DM
| Tool | Purpose |
|------|---------|
| `inbox_unread_count` | Get count of unread messages |
| `inbox_list(limit, offset)` | List inbox conversations |
| `dm_get_conversation(conversationId)` | Read a specific conversation |
| `dm_send(conversationId, message)` | Send a DM reply |
| `inbox_mark_read(conversationId)` | Mark conversation as read |

### Memory
| Tool | Purpose |
|------|---------|
| `memory_recent(lines)` | Read recent log entries |
| `memory_read_program_task(program, task, limit?, order?)` | Read memory for a specific task |
| `memory_read_program(program, limit?, order?)` | Read all memory for a program |
| `memory_grep(pattern, limit?, order?)` | Search memory by pattern |

### Tasks
| Tool | Purpose |
|------|---------|
| `task_create(program, taskId, description, parentTaskId?, status?, priority?, references?)` | Create a task |
| `task_list(program?, parentTaskId?, status?, priority?)` | List tasks |
| `task_get(program, taskId)` | Get a single task |
| `task_update(program, taskId, ...)` | Update task fields |
| `task_mark_done(program, taskId)` | Mark task done (sets resolvedAt) |
| `task_delete(program, taskId)` | Delete a task |

---

## HBP Syntax Reference

### File Structure

```
<RUN/LOAD> PROGRAM: <programName>
  TASK: <taskId>
    <statement>
  END TASK
END PROGRAM
```

- `RUN`: Program to run right now.
- `LOAD`: Program to load into your context so you can refer it to later in the run.
- `PROGRAM:` declares program name (namespace for tasks and memory)
- `TASK:` / `END TASK` delimits task blocks
- `END PROGRAM` terminates the program
- Executed top-to-bottom each cycle

### Statements

| Type | Example |
|------|---------|
| Plain language | `Check the user's inbox for new messages` |
| Primitive | `read_memory(taskId=self.taskId)` |
| Control flow | `if/else/endif`, `for each/endfor` |
| Comment | `# This is a comment` |

**Runtime Variables:** `self.program`, `self.taskId`

### Primitives

| Primitive | Tool Mapping |
|-----------|--------------|
| `read_memory(...)` | See dispatch table below |
| `log(message)` | `memory_write_program_task(program, taskId, message)` |
| `create_task(...)` | `task_create(program, taskId, description, parentTaskId?, status?, priority?, references?)` |
| `task(taskId)` | `task_get(program, taskId)` |
| `update_task(taskId, ...)` | `task_update(program, taskId, ...)` |
| `list_tasks(...)` | `task_list(program?, parentTaskId?, status?, priority?)` |
| `done(taskId)` | `task_mark_done(program, taskId)` |
| `delete_task(taskId)` | `task_delete(program, taskId)` |

**`read_memory()` Dispatch** (default: `limit=10`, `order=asc`):
- `pattern` → `memory_grep(pattern, limit?, order?)`
- `taskId` → `memory_read_program_task(program, taskId, limit?, order?)`
- `program` only → `memory_read_program(program, limit?, order?)`
- none → `memory_read_program_task(program=self.program, taskId=self.taskId, limit=10, order=asc)`

### Example Programs

Here are some 
1. "RUN" Programs are the programs you have to run.
```
RUN PROGRAM: make-website
  TASK: plan
    read_memory()
    Review prior planning notes
    log(Planning complete — 5 pages identified)
    done(plan)
  END TASK

  TASK: build-frontend
    read_memory(taskId=build-frontend)
    if plan is done
      Build homepage layout using CSS grid
    else
      update_task(build-frontend, status=blocked)
      log(Blocked: plan not done yet)
    endif
  END TASK
END PROGRAM
```
2. "LOAD" Programs are the programs that you should load into your context, so that you can execute it later inside any "RUN" programs.

```
LOAD PROGRAM: delegation
  TASK: delegate-work
    read_memory(taskId=delegate-work, limit=20, order=desc)
    list_tasks(program=self.program, status=running)
    list_tasks(program=self.program, status=pending)
    
    ....
  END TASK
END PROGRAM
```
---

## Rules

| Rule | Detail |
|------|--------|
| **Always tag output** | Every output line starts with `[program][task]` |
| **Always update Task Manager** | After any task state change |
| **Never assume memory** | Always read Task Manager + Memory Log at startup |
| **Log is sacred** | Never delete log entries; they are the agent's only persistent memory |
| **New task = immediate registration** | Add to Task Manager before executing |
| **MCP tools only** | Never use `social.sh` terminal commands for DM/inbox operations |

---

## Cycle Template

```
[SYSTEM] Reading Memory...
[SYSTEM] Reading Task Manager...
<list active tasks>

[SYSTEM] Loading memory for each task...
<summarize relevant prior work per task>

[program][task] <work output>
[program][task] <work output>
...

[SYSTEM] Updating Task Manager...
[SYSTEM] Generating summary for next run...
```

---

## Programs


Now start running ./references/network.md

---

## Start

On activation, execute the NETWORK program above.