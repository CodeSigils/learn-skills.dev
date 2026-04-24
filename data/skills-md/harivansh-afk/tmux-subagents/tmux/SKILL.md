---
name: tmux
description: Orchestrate Devin CLI subagents as background workers using tmux windows. Use when the user asks to spawn, coordinate, fan-out, or delegate work to multiple parallel agents, run background Devin sessions, or orchestrate long-running autonomous tasks from inside an existing Devin session.
compatibility: Devin CLI (devin), tmux >= 3.0, macOS or Linux
---

# tmux Subagent Orchestration

Run Devin CLI subagents in parallel by giving each one its own tmux window. The
parent agent delegates a task, waits for a completion signal, reads the
subagent's output file, and closes the window.

## When to Use

- Fan out independent research, refactors, or test runs across several agents.
- Keep a long-running Devin session alive in the background while continuing
  other work.
- Coordinate multiple agents that each own a distinct task/context.

## Setup (do once per session)

Before any tmux operation, resolve two values and reuse them:

1. `TMUX=$(which tmux)` - absolute path to the tmux binary.
2. `SESSION=$("$TMUX" display-message -p '#S')` - current session name.

If `TMUX` is unset in the environment, you are not inside a tmux session and
the helper scripts will refuse to run. Start tmux first (`tmux new -s work`)
and relaunch Devin inside it.

## Helper Scripts

Use these for all standard operations. Run them from this skill directory
(`skills/tmux/`). All scripts print `Done` on success or an `error:` line on
failure, and exit non-zero on error.

| Script | Usage | Description |
|---|---|---|
| `scripts/spawn_subagent.sh` | `<window-name> [command]` | Create a new window and start a subagent. Default command: `devin --permission-mode dangerous` |
| `scripts/send_command.sh` | `<window-name> <command>` | Send literal text to the window, wait 1s, press Enter |
| `scripts/exit_subagent.sh` | `<window-name>` | Send `/exit`, wait 1s, kill the window if still present |

## Subagent Workflow

```bash
# 1. Spawn (defaults to `devin --permission-mode dangerous`)
./scripts/spawn_subagent.sh agent-research-1

# 2. Send the task. Tell the subagent to write its output to a file
#    and notify the parent when finished.
./scripts/send_command.sh agent-research-1 \
  "Research X and write the result to /tmp/agent-research-1.md. When done, run: tmux display-message -d 5000 'agent-research-1: done'"

# 3. Wait for the notification (display-message or agentmail).
#    DO NOT poll capture-pane in a loop.

# 4. Read /tmp/agent-research-1.md

# 5. Clean up
./scripts/exit_subagent.sh agent-research-1
```

## Mandatory Requirements

1. Use tmux **windows**, never panes.
2. Window names MUST follow `agent-{task}-{number}` (e.g. `agent-refactor-2`).
3. Wait for subagent notifications via `display-message` or agentmail. Do
   **not** poll `capture-pane` in a loop.
4. Use `spawn_subagent.sh` to spawn, `send_command.sh` to send input, and
   `exit_subagent.sh` to stop. Fall back to raw `tmux` commands only for
   debugging or edge cases.
5. Each subagent task MUST write its result to a known file path (e.g.
   `/tmp/<window-name>.md`). Do not scrape it from the pane.

## Completion Signal

When a subagent finishes, have it run:

```bash
tmux display-message -d 5000 "<window-name>: <short message>"
```

The parent agent receives the message in its tmux status line and can proceed.

## Common Subagent Commands

Commands to send into a Devin subagent window with `send_command.sh`:

| Command | Description |
|---|---|
| `/exit` | Exit the agent gracefully |
| `/clear` | Clear the agent's context window |
| `/compact handoff:<info>` | Compact context, preserving handoff notes |

## Raw tmux Reference (edge cases only)

See `references/tmux-commands.md` for the raw `tmux` command cheat sheet used
for debugging (listing windows, capturing pane output, sending Ctrl-C, etc.).
