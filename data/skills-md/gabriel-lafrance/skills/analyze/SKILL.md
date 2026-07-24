---
name: analyze
description: >-
  Task analysis that writes findings under a scoped workspace, supports
  explicit promotion to a /goal, and evaluates named code-review Fix-now
  blockers before remediation. No ticket write by default. Use for a task,
  idea, or review backlog; /write-ticket and /code-review may call it.
disable-model-invocation: true
---

# Analyze

**Variants:** [../pack-shared/variants.md](../pack-shared/variants.md) — **standalone-only** (no `flow.md`). If flow is requested, use the **no flow** message.

**Standalone by default.** The sole in-goal exception is a code-review **review remediation analysis** of named Fix-now blockers. It does **not** write Linear/GitHub — that is `/write-ticket`.

**Read:** [doctrine.md](doctrine.md) · [../pack-shared/workspace-roots.md](../pack-shared/workspace-roots.md) · **Ask style:** [../pack-shared/asking.md](../pack-shared/asking.md) · **Taste / structure:** `/taste`, `/architecture` when relevant.

**Subagent model:** omit Task `model`. Wait for Task results — never sleep/poll for subagents.

## Process (outline)

1. Resolve `analysis_root` / `analyses_container` (always write)
2. Parallel `explore` Tasks → synthesize
3. Write `ANALYSIS.md` (required)
4. Optional sharpen Questions batch
5. Hand-off batch (done / sharpen / promote / write-ticket / promote+goal)
6. For review remediation, describe each named Fix-now issue/current behavior, root cause, smallest fix, touch surface, non-goals, and verification before an explicit promotion choice
7. Promote only on explicit yes — see doctrine

Unsure which skill next → `/ask-gabriel`.
