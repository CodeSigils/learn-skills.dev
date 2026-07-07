---
name: sequential-thinking
description: Structured step-by-step reasoning with a persistent, file-backed thought chain. Use for complex problems that need multi-step decomposition, mid-course revision of earlier assumptions, or exploring alternative solution branches — especially in long sessions where the reasoning chain should survive context compaction. Triggers include "think step by step", "sequential thinking", "顺序思考", "分步推理", "逐步分析", revising earlier reasoning, or replaying how a conclusion was reached.
---

# Sequential Thinking

Record your reasoning as an explicit, numbered chain of thoughts in a state
file, one CLI call per thought. This replaces the `sequential-thinking` MCP
server: same call → ack → next-thought rhythm, but the chain lives on disk,
so it survives context compaction and can be replayed later.

The script is at `scripts/think.py` **inside this skill's directory**. The
working directory at runtime is the user's project, so always invoke it by
absolute path (you know this skill's location from where you read this file):

```
python3 <this-skill-dir>/scripts/think.py <command> ...
```

## Workflow

1. **Start a chain** — one line stating the problem, plus a step estimate:

   ```
   think.py new "为什么 X 指标在 3 月下跌" --total 5
   ```

2. **Record every thinking step** as you produce it. Do the thinking in the
   argument itself — the thought text should carry real analysis, not a label:

   ```
   think.py add "候选原因有 A/B/C，其中 B 与时间线吻合……"
   ```

3. **Revise instead of forcing.** When an earlier step turns out wrong, don't
   bend later reasoning around it — mark the correction explicitly:

   ```
   think.py add "第 2 步的假设不成立，因为……" --revises 2
   ```

4. **Branch to explore alternatives** when two solution paths both look viable:

   ```
   think.py add "换个思路：如果从需求侧看……" --branch-from 3 --branch-id demand-side
   ```

5. **Adjust the estimate freely** with `--total N` on any `add` — it is an
   estimate, not a budget. Add more thoughts after the "last" one if needed.

6. **Finish** only when a hypothesis has been generated *and* verified against
   the chain, and you are satisfied with the answer:

   ```
   think.py add "结论：……，已对照第 1/3/5 步验证" --done
   ```

7. **Replay** at any time with `think.py show` (or `show --json`). Use this to
   recover the full reasoning chain after context compaction, or to review the
   chain before writing the final answer.

## Principles

- One thought per call; keep the ack rhythm. Each call returns
  `{thoughtNumber, nextThoughtNeeded, ...}` — while `nextThoughtNeeded` is
  true, keep thinking.
- Question earlier decisions; express uncertainty when it exists.
- Filter out irrelevant information rather than carrying it forward.
- Generate a solution hypothesis, then verify it against the chain of thought
  before `--done`. If verification fails, keep adding thoughts.

## State file

Resolution order — pick the most session-scoped option available:

1. **Preferred:** if your harness gives you a session-specific scratchpad or
   temp directory, pass `--file <scratchpad>/thoughts.json` on **every** call.
   This isolates concurrent sessions that share a working directory, and the
   chain still survives context compaction within the session.
2. **Fallback:** with no `--file`, state goes to
   `${XDG_STATE_HOME:-~/.local/state}/think/<cwd-hash>/thoughts.json` — one
   chain per working directory, nothing written into the user's project.
   Caveat: two concurrent sessions in the same directory would interleave
   into (and garble) one chain, so prefer option 1 whenever you can.

Rules either way:

- Always begin a task with `think.py new` — never `add` onto a chain you did
  not start. If an `add` ack contains a `warning` field (chain idle for
  hours), treat it as a stale leftover: run `new`.
- Thoughts are written to disk in plain text and outlive the session; do not
  put secrets (keys, credentials, private data) into thought text.
- `new` clears the previous chain; `reset` deletes the file; `where` prints
  the path.
