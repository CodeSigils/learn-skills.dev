---
name: handoff
description: |
  Gather the session-to-session baton for HANDOFF.md at repo root and hand it to encode-docs, which writes it — the baton for multi-phase PLAN.md execution. Captures current phase.task status, exact stopping point, next phase.task pointer, and watchouts. It will flip status and mark completion in PLAN.md if task is done. The cook skill invokes this at the end of every session; also triggers on "/handoff".
---

# handoff — session baton

The next session starts cold. HANDOFF.md is everything it must know that PLAN.md, SPEC.md, and git history do NOT already record. Never duplicate what those files say — point at them.

`handoff` GATHERS the baton content; it does NOT write `HANDOFF.md` directly. This skill collects the state below, then hands it to `encode-docs`.

## WHEN

- End of every working session.
- Context budget running low mid-phase.
- Before any risky long-running operation.
- User asks.

## GATHER → hand to encode-docs

Collect the facts below and pass them to `encode-docs`. It writes `HANDOFF.md` (repo root, overwritten in full — git keeps history) with its own lean template; do NOT reproduce that template here — encode-docs owns the shape.

- branch | last commit `<sha>` | tests `<pass N/N | FAIL: file+case>` `(<cmd>)`
- uncommitted: `<none | files + why>`
- done this session: `<F<n>.T<n>>: <one line> → <sha>`
- in progress: `<F<n>.T<n>>: <status: mid-edit | done>`, `mid-edit files: <paths | none>`
- next: `<F<n>.T<n>> | preconditions: <gates | none>`
- planning status: `done` when every `§T` row is `x` and the final-verify table holds; otherwise leave the value exactly as it is, because `cook` and `cater` own the `new` → `work-in-progress` flip. Hand the flip to `encode-docs` with the baton.
- deviations & decisions; watchouts
- final verification table

## RULES

1. **Uncommitted work is a first-class fact.** Name every uncommitted file and why it was left so. Prefer committing (even a `~` wip §T flip) over a dirty tree.
2. **Failing tests named exactly** — file + case — never "some failing".
3. **NEXT TASK is executable verbatim** by a cold agent: file, function, action — never "continue the phase". Reference done tasks and next as `F<n>.T<n>`.
4. **Only the final-verify phase fills the final verification table**; others leave the header row.
5. **Commit HANDOFF.md** — inside the session's final phase commit or its own, per repo conventions. A standalone baton commit goes through `encode-commit`: which phase closed, the next task, and the test state, in plain English. No phase ids, no encoding symbols, never a bare `docs: handoff`.

## NON-GOALS

- Not a status dashboard (PLAN §T is), not a changelog (CHANGELOG.md is), not a diary. State that helps the NEXT session act — nothing else.
