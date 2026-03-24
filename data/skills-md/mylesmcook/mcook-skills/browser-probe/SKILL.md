---
name: browser-probe
description: Exploratory browser QA for real web apps. Use when you want a smoke test, scoped verification, exploratory testing, or a balanced read on what works, what feels off, and what is blocked.
---

# Browser Probe

Use this skill for exploratory browser QA that is lighter than a formal repro package.

## Workflow

1. Pick a mode: `smoke`, `balanced`, or `bug-hunt`.
2. Create one named `agent-browser` session and reuse it for the whole run.
3. Model the app or scoped feature.
4. Generate likely failure hypotheses and likely strengths.
5. Execute focused checks with proportional evidence.
6. Report confirmed issues, verified strengths, flakes, and blocked areas.

## References

Read these in order:
- `references/stage-1-model.md`
- `references/stage-2-hypothesize.md`
- `references/stage-3-execute.md`
- `references/stage-4-report.md`

Use these only when needed:
- `references/session-preflight.md`
- `references/recovery.md`
- `references/patterns/*`

## Guardrails

- Keep one live browser session per run.
- Re-snapshot after DOM-changing actions.
- Route repro-heavy handoff requests to a more formal bug workflow.
