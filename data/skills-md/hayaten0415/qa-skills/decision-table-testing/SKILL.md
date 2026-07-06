---
name: decision-table-testing
description: >-
  Design and implement decision table tests for logic where combinations of conditions
  produce different outcomes — business rules, pricing, eligibility, permissions. Use
  when: "decision table," "デシジョンテーブル," "business rules," "combinations of
  conditions," "if X and Y then Z" logic, or feature flags/pricing/eligibility matrices.
  Produces a collapsed decision table (design mode) and one parameterized test per rule
  (implementation mode). Not for: single-parameter ranges — use equivalence-partitioning
  / boundary-value-analysis; for event-ordered behavior — use state-transition-testing.
  Related: equivalence-partitioning, state-transition-testing.
license: MIT
metadata:
  version: "1.0"
  istqb: "CTFL v4.0 §4.2.3"
  iso25010: [functional-suitability]
  mode: [design, implementation]
---

# Decision Table Testing

Record complex conditional logic as conditions × actions, and test each rule — so no
combination of business conditions ships unverified.

## Objective

A decision table capturing the requirement's condition combinations, collapsed to the
feasible/distinct rules, with one test per rule. Per CTFL v4.0 §4.2.3, decision tables
test how *combinations of conditions* result in different outcomes — an effective way
to record complex logic such as business rules. The failure mode this prevents: code
that handles the obvious combinations but mishandles an unusual-but-valid one nobody
tabulated.

## Context Discovery

- Where is the rule specified? (requirements, a pricing/eligibility matrix, policy
  docs, or the conditional code itself.) The conditions and actions come from the spec.
- How many conditions, and are they binary or multi-valued? This sizes the table.
- Are some combinations infeasible or "don't care"? Capture them to collapse the table.
- Implementation mode: framework/language (detect from the repo).

## Instructions

1. **List conditions and actions**: conditions = the inputs that affect the outcome;
   actions = the resulting outcomes/effects. Draw them from the specification.

2. **Enumerate rules (columns)**: a full table has one column per condition combination
   (2ⁿ for n binary conditions). Each column is a **rule**: a unique combination of
   condition values and its associated actions.

3. **Collapse the table**: merge columns where a condition is irrelevant to the outcome
   ("don't care", `–`) and drop infeasible combinations — with a note on why. This
   controls the 2ⁿ explosion without losing coverage of distinct behaviors.

4. **Derive one test per rule**: minimum coverage is at least one test case per column
   of the collapsed table. Assert the exact action(s) for that rule, not just "passes."

5. **Flag contradictions**: if the spec yields two rules with the same conditions but
   different actions, that is a requirements defect — surface it.

## Output Format

### design mode

Conditions in rows, rules in columns (`Y`/`N`/`–` for don't-care):

```
Conditions            R1  R2  R3  R4
  Registered user?    Y   Y   N   N
  Cart > $100?        Y   N   Y   N
Actions
  Free shipping       X   -   -   -
  Standard shipping   -   X   X   X
```

| Rule | Registered | Cart>$100 | Expected action | Trace |
|---|---|---|---|---|
| R1 | Y | Y | free shipping | REQ-30 |

### implementation mode

One case per rule (pytest idiom; adapt to the repo):

```python
@pytest.mark.parametrize("registered,over_100,expected", [
    (True,  True,  "FREE"),      # R1
    (True,  False, "STANDARD"),  # R2
    (False, True,  "STANDARD"),  # R3
    (False, False, "STANDARD"),  # R4
])
def test_shipping_rules(registered, over_100, expected):
    assert shipping(registered, over_100) == expected
```

## Anti-Patterns

- **Combinatorial explosion** — generating all 2ⁿ columns for many conditions without
  collapsing. **Guard:** merge don't-cares and drop infeasible combos; test the
  distinct rules, not every raw permutation.
- **Missing rules** — tabulating the obvious combinations and omitting an odd one.
  **Guard:** the table must cover every feasible condition combination before collapse.
- **Conditions from memory** — inventing rules the spec doesn't state. **Guard:** each
  condition/action cites the requirement or rule source.
- **Only "all-true" combinations** — testing the happy combination and not the mixed
  ones where bugs hide. **Guard:** every collapsed rule, including all-false, gets a test.

## Related Skills

- `equivalence-partitioning` — partition each condition's values before tabulating.
- `state-transition-testing` — when behavior depends on event order, not just a
  snapshot of conditions.

## References

- ISTQB CTFL v4.0 Syllabus §4.2.3 (Decision Table Testing)
- ISO/IEC 25010:2023 — Functional Suitability (functional correctness, completeness)
