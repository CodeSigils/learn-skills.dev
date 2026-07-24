---
name: create-test
description: >-
  Standalone only — never in a flow, never autonomous. Writes durable
  behavior-lock tests for complex architectural parts (hooks, domain/business
  logic, facades, stateful classes). Locks deeply thought-through behavior so
  outside edits cannot silently break it. Use only when the user runs
  /create-test (only after /code-review or /pr-review recommends a lock).
  Not for coverage theater, trivial units, or /goal.
disable-model-invocation: true
---

# Create Test

**Variants:** [../pack-shared/variants.md](../pack-shared/variants.md) — this skill is **standalone-only** (no `flow.md`). If flow is requested, use the **no flow** missing-variant message.

**Standalone only.** Never call from `/goal`, never auto-invoke. **Only** `/code-review` and `/pr-review` may **recommend** a lock — and only the **user** starts `/create-test`. No other skill writes tests or invokes this skill.

Tests **lock behavior** of a complex architectural part — complex hooks, domain logic, facades, stateful classes — so outside edits cannot silently break already settled logic.

## When this skill applies

| Lock | Skip |
| --- | --- |
| Complex hook with non-obvious state/effects | Thin wrappers / one-liners |
| Domain / business logic with invariants | Pure formatters already covered elsewhere |
| Facade / orchestrator with ordering or guards | UI chrome / copy / layout |
| Stateful class / strategy with edge rules | Generated code, types-only files |
| Regression for a bug that revealed a missing invariant | Snapshot/coverage chasing |

If the target is trivial, say so and stop. Do not invent tests to look productive.

## Core doctrine

1. **Lock behavior, not implementation** — assert outcomes, invariants, and public contracts. Refactors that preserve behavior must not force a rewrite.
2. **Public entry point only** — exercise the simple exported surface callers use. Do not reach into private helpers, module internals, or implementation spies unless that spy *is* the contract (rare).
3. **Name the invariant** — every test title states the locked claim (`checkout rejects expired coupon`, not `works` / `handles case`).
4. **Why / What / How — grill, approve, then comment** — before writing code, lock answers with the user. Paste the approved three bullets as a short comment above each main test (see §2–§4).
5. **Characterization over theater** — capture what the deep logic *must* keep doing. Prefer a few high-conviction scenarios over dozens of shallow cases.
6. **Stable seams** — mock only true external boundaries (network, clock, storage, auth). Prefer real collaborators in-process when cheap. Brittle call-sequence mocks on every internal hop are forbidden.
7. **Fail on behavior drift** — a wrong outside edit must turn the test red. A rename/extract that preserves behavior must stay green.
8. **Mirror the repo** — use the existing test runner, folder layout, and helpers. Do not introduce a new framework.
9. **Narrow verify** — run the new/changed test file (or focused filter). No full-suite ritual unless the user asks or the narrow run is inconclusive.
10. **No `{ success: false }` bags in test helpers** — throw on setup failure; try/catch at boundaries. Match `/taste`.
11. **One file, one subject** — tests for `use-checkout.ts` live beside or under the project’s usual colocated pattern; do not dump unrelated locks into a junk drawer.

## Process

### 1. Pin the subject

User names a file, symbol, feature, or pastes a `/code-review` “needs lock” note. If missing, ask once.

Read:

- The public export(s) and call sites
- Existing tests for the same area (reuse fixtures/helpers)
- Nearby deep logic the lock must protect

State in one sentence: **what behavior is being locked** and **what outside edit this is meant to catch**.

### 2. Grill Why / What / How (blocking — must approve)

Every lock needs three answers. Draft them from the code first, then grill per [../pack-shared/asking.md](../pack-shared/asking.md) (batch, recommended marked) until solid.

| Bullet | Must answer |
| --- | --- |
| **Why** | Why this behavior must stay locked — the risk if an outside edit silently breaks it |
| **What** | What observable contract is locked (outcomes / invariants / must-nots) — not internals |
| **How** | How the test exercises it (public entry, key setup, what it asserts) |

Show every draft you need now, then **one Questions batch**:

```markdown
## Lock brief — <symbol>
- Why: …
- What: …
- How: …

## Questions
Reply like: 1a 2a

1. Approve Why / What / How for `<symbol>`?
   - a) yes ← recommended
   - b) no — say what to edit
2. (If another main test) Approve Why / What / How for `<other>`?
   - a) yes ← recommended
   - b) no — say what to edit
```

**Wait for the batch.** Edits → revise → follow-up batch for unresolved locks. Do **not** write test code until each required brief is approved.

If several main tests (distinct claims), put **all** their briefs + approve items in the **same** first batch — do not approve vague blurbs, and do not drip one symbol per message when several are ready.

Also keep a short contract list when useful (`Given/when/then`, invariants) — the Why/What/How brief is the hard gate.

### 3. Choose scenarios (few, high signal)

Pick the minimum set that locks the deep logic:

1. **Happy path** that proves the core outcome
2. **Critical guards** (auth, validation, empty/null, illegal order)
3. **Edge that bit (or would bit) production** — race, stale state, double-submit, timezone, partial failure
4. **Regression** if this lock comes from a real bug — name the bug in the test title

Skip combinatorial tables of equivalent inputs. Skip asserting every intermediate private call.

### 4. Write the lock

**Required comment** — paste the **approved** Why / What / How as three bullets immediately above each main test function (`it` / `test` / top-level `describe` callback that owns the claim — prefer the `it`/`test` that asserts the lock):

```ts
/**
 * Why: <approved why>
 * What: <approved what>
 * How: <approved how>
 */
it("checkout rejects expired coupon", () => {
  // ...
});
```

Use the repo’s comment style (`/** */` or `//` bullets) — keep it to those three lines only. No essays. Wording must match what the user approved (verbatim or trivial grammar polish only).

Then:

- Arrange through the public API (renderHook / class instance / pure function / facade).
- Act once per claim.
- Assert **observable results** (return value, state after act, thrown error, persisted write at the boundary).
- Keep setup DRY via local helpers; throw if fixture setup fails.
- No snapshots of huge trees unless the snapshot *is* a documented contract (almost never).

### 5. Prove it locks

1. Run the narrow test file — must pass.
2. Mentally (or with a tiny local sabotage you revert) confirm: breaking the invariant fails the test.
3. Confirm a harmless extract/rename would not require rewriting assertions.

### 6. Hand-off

Report:

- Approved Why / What / How (same bullets as in the comment)
- Files added/changed
- Commands run + pass/fail
- What an outside edit would need to do to turn these red (one line)

Do **not** start `/goal`, expand scope into refactors, or “improve” the subject while locking it — unless the user asked.

## Anti-patterns

- Invoking under `/goal`, or auto-starting without the user
- Writing tests before Why / What / How is **approved**
- Omitting the three-bullet comment above the main test
- Being auto-invoked by `/goal`, `/implement`, `/repair`, or any skill other than user-started after `/code-review` / `/pr-review` recommend
- Inventing Why / What / How in the comment that the user never saw
- Testing private functions because they are “easier”
- Mocking every collaborator so the test only proves the mock script
- Snapshot / coverage theater
- Asserting call order of internal helpers when only the outcome matters
- Tests that break on every rename while behavior is unchanged
- Locking trivial code “for completeness”
- Rewriting production code just to make it “more testable” without user ask
- Full-suite / lint / typecheck rituals after every file (CI owns those; narrow test run only)

## Relation to other skills

| Skill | Role |
| --- | --- |
| `/code-review` | May **recommend** “run `/create-test` on `<path>`” — does not run this skill |
| `/pr-review` | May **recommend** the same (chat and/or Nit) — does not run this skill |
| `/validate` | Runtime/path acceptance — not a substitute for behavior locks |
| `/repair` / `/implement` / `/goal` / others | **Never** write tests or invoke `/create-test` |
| `/taste` | Style contract for helpers and verify discipline |

## Failures

| Problem | Action |
| --- | --- |
| No test runner / unclear layout | Say what you found; ask once which command/folder to use |
| Subject too trivial | Refuse with reason; suggest skipping |
| Why / What / How rejected or fuzzy | Keep grilling — never write until approved |
| User declines the brief | Leave draft in chat; do not write tests |
| Narrow tests fail on existing code | Stop — report failure; do not “fix” production to green unless user asked |
| User wanted coverage % | Redirect: this skill locks behavior, not metrics |
