---
name: state-transition-testing
description: >-
  Design and implement state transition tests for systems with modes/statuses where
  behavior depends on history and events — order lifecycles, auth/session states,
  wizards, connection state machines. Use when: "state transition," "状態遷移,"
  "state machine," "status workflow," "order/payment lifecycle," "valid/invalid
  transitions," or any status field with allowed moves. Produces a state table +
  transition cases including invalid events (design mode) and event-sequence tests
  (implementation mode). Not for: stateless combinational logic — use
  decision-table-testing. Related: decision-table-testing, boundary-value-analysis.
license: MIT
metadata:
  version: "1.0"
  istqb: "CTFL v4.0 §4.2.4"
  iso25010: [functional-suitability]
  mode: [design, implementation]
---

# State Transition Testing

Model states, events, and transitions, then test both the valid moves and the invalid
events — because "what happens when this event fires in the wrong state" is where state
machines break.

## Objective

A state model (diagram or table) and a test set covering all states, all valid
transitions, and the invalid-event handling for each state. Per CTFL v4.0 §4.2.4, a
transition is initiated by an **event**, optionally qualified by a **guard condition**,
and may produce an **action** — labeled `event [guard] / action`. The failure mode this
prevents: a lifecycle that allows an illegal move (e.g. refunding an unpaid order)
because only the happy path was tested.

## Context Discovery

- What are the states and events? Read the status enum, the transition/guard code, and
  the lifecycle spec. Missing transitions in code vs spec are a defect finding.
- Are there guard conditions (a transition allowed only if X)? Capture them.
- What should happen on an **invalid** event (ignored? error? no state change?) — the
  spec must define it; if it doesn't, that gap is a finding.
- Coverage target: valid transitions only (0-switch) or transition sequences (n-switch)?

## Instructions

1. **Build the state model**: enumerate states, events, transitions, guards, and
   actions. Represent as a state table (states × events) — empty cells are invalid
   (or undefined) transitions and must be examined.

2. **Cover all valid transitions (0-switch / Chow's coverage)**: one test per valid
   state→event→state edge, asserting the resulting state AND any action/output.

3. **Test invalid events deliberately**: for each state, fire events with no defined
   transition; assert the specified behavior (rejected/ignored, correct error, state
   unchanged). This is the half most suites skip.

4. **Exercise guard conditions**: test the guard true and false paths — same event,
   different outcome by guard.

5. **Add sequence coverage where risk warrants (n-switch)**: test paths of consecutive
   transitions (e.g. created→paid→shipped→delivered) to catch defects that only appear
   after a specific history.

6. **Trace to requirements** and flag any state with no defined exit (dead state) or an
   unreachable state.

## Output Format

### design mode

State table (cell = target state, `—` = invalid event in that state):

```
State \ Event   pay        ship       cancel     refund
Created         Paid       —          Cancelled  —
Paid            —          Shipped    Cancelled  Refunded
Shipped         —          —          —          Refunded
```

| TC | From | Event [guard] | To / Result | Valid? | Trace |
|---|---|---|---|---|---|
| ST-01 | Created | pay | Paid | valid | REQ-40 |
| ST-07 | Created | refund | rejected, stays Created | invalid | REQ-41 |

### implementation mode

Drive event sequences and assert state + rejection of invalid events:

```python
def test_refund_before_payment_is_rejected():
    order = Order.create()                       # state: Created
    with pytest.raises(InvalidTransition):
        order.refund()                           # invalid event
    assert order.state == "Created"              # unchanged
```

## Anti-Patterns

- **Only valid transitions** — testing the happy lifecycle and never the illegal event.
  **Guard:** every state gets at least one invalid-event test asserting rejection +
  unchanged state.
- **States tested, transitions not** — asserting a state is reachable but not the
  event that gets there or its action. **Guard:** the transition (edge) is the unit of
  coverage, not the state.
- **Guards ignored** — testing the event but only one side of its guard. **Guard:**
  cover guard true and false.
- **Model from memory** — inventing transitions the code/spec doesn't define. **Guard:**
  build the table from the status enum + transition code; reconcile spec vs code.

## Related Skills

- `decision-table-testing` — for guard conditions that are themselves condition
  combinations.
- `boundary-value-analysis` — for guards based on numeric thresholds.

## References

- ISTQB CTFL v4.0 Syllabus §4.2.4 (State Transition Testing)
- ISO/IEC 25010:2023 — Functional Suitability (functional correctness)
