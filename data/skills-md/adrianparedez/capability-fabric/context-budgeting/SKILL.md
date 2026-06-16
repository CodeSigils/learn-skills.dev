---
name: context-budgeting
description: Deliberately manages the context window to cut token cost and prevent quality decay on long runs. Use when a task is long-running, involves large files or many tool outputs, the context feels full, or cost matters. For finding external info efficiently use progressive-research; for surviving multi-session work use sustained-execution.
license: Apache-2.0
metadata:
  author: Adrian Paredez
  version: "1.0"
  tier: "1"
  layer: meta/control
compatibility: Any agent runtime with filesystem read and shell access. Enhanced by, but does not require, compaction, sub-agents, or hooks.
---

# Context budgeting

Treat the context window as a finite, *degrading* resource you spend on purpose. Resting
cost is small and permanent; active cost is large and compounds. Optimize the active
window.

## Use this when
- The session is long, or context "feels" more than half full.
- You're about to read large files, fetch many pages, or accumulate tool output.
- Cost/latency matters, or the model is starting to drift/forget earlier facts.
- **Do NOT** micro-optimize short tasks, the discipline costs tokens too.

## The budget (keep this in your working state)

```
window_limit : <model context size>
soft_ceiling : ~50-60%  -> start offloading payloads to files, keep pointers
hard_ceiling : ~75-80%  -> compact: write a digest, reinitialize, reload essentials
keep_always  : goal, success criteria, current plan step, open decisions, pointers
offload_first: raw tool output, finished steps, reference dumps, long logs
```

## Core rules

1. **Pointers, not payloads.** Load IDs, paths, URLs, and line ranges. Fetch the payload
   only at the moment you act on it. Re-deriving a pointer is cheap; re-holding a payload
   is expensive.
2. **Peek before you read.** Use `grep`/search and `head`/line-ranges to pull the few
   lines you need instead of reading whole files into context.
3. **Extract then discard.** When you do read something large, immediately distill the
   needed facts into a short note and let the source fall out of working memory.
4. **Clear consumed tool output.** Once a command's result is acted on, don't keep
   re-quoting it. Summarize the outcome in one line.
5. **Offload at the soft ceiling.** Move completed work, raw logs, and reference material
   to files (a notes/ledger file). Keep only `keep_always` in context.
6. **Compact at the hard ceiling.** Write a high-fidelity digest (see template), then
   continue from goal + plan-step + digest + pointers. Never compact away `keep_always`.
7. **Protect the reasoning surface.** Optimize the substrate (dumps, logs, finished
   steps), never the goal, active plan step, open questions, or the verification of the
   result you're about to ship.

## Workflow

```
- [ ] State the budget ceilings for this model/run.
- [ ] Before each large read/fetch: can I peek (grep/head) instead?  (rule 2)
- [ ] After each large output: extract facts, drop the raw text.     (rules 3,4)
- [ ] At soft ceiling: offload payloads to a file; keep pointers.    (rule 5)
- [ ] At hard ceiling: write digest -> reinitialize -> reload core.  (rule 6)
- [ ] Before compaction of a critical result: run verifying-reasoning. (rule 7)
```

## Quick decision

| Situation | Do |
|---|---|
| Need info from a 2k-line file | grep for the symbol, read ±20 lines, not the file |
| Tool dumped 500 lines of JSON | extract the 3 fields you need, drop the rest |
| 10 search results | keep titles+URLs (pointers), open 1-2, discard the rest |
| Context ~75% full mid-task | checkpoint digest, reinitialize, reload goal+plan+pointers |
| About to summarize a result you'll ship | verify it first, then compact around it |

## Runtime adaptation
- **Minimum:** filesystem read + shell. Offload/notes use a plain file.
- **If compaction is automatic** (some runtimes): still write your own digest file first
  so *you* control what survives, not just the summarizer.
- **If sub-agents exist:** push wide/noisy exploration into them and keep only conclusions
  (see `composing-skills`). If not, do the exploration, then aggressively extract+discard.
- Never depend on a specific tool name; these rules are about *what* to do, not *which*
  tool does it.

## Files
- `references.md`, the cost model, the 7 techniques, deeper rationale.
- `examples.md`, worked before/after token traces.
- `templates/digest.md`, the compaction digest format.
- `templates/budget-state.md`, the working budget block to copy.
- `checklists/pre-compaction.md`, what to preserve before compacting.
- `benchmarks/`, how to measure tokens-to-completion and peak context.
