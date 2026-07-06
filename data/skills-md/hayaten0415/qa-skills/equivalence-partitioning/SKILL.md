---
name: equivalence-partitioning
description: >-
  Design and implement equivalence partitioning (EP) tests — divide each input/output
  into classes processed the same way, then test one representative per class plus
  every invalid class. Use when: "equivalence partitioning," "同値分割," "test classes,"
  "which inputs to test," "reduce redundant test cases," or before boundary-value
  analysis (EP identifies the partitions whose edges BVA then tests). Produces a
  partition table (design mode) and parameterized tests, one per class
  (implementation mode). Not for: testing the edges of the classes — use
  boundary-value-analysis. Related: boundary-value-analysis, decision-table-testing.
license: MIT
metadata:
  version: "1.0"
  istqb: "CTFL v4.0 §4.2.1"
  iso25010: [functional-suitability]
  mode: [design, implementation]
---

# Equivalence Partitioning

Divide input and output data into classes the system treats identically, so one test
per class gives coverage without redundant cases — and no class is left untested.

## Objective

A partition set for each parameter where valid AND invalid classes are enumerated,
each with one representative test, plus the traceability from class → requirement. Per
CTFL v4.0 §4.2.1, all elements of a partition are expected to be processed the same
way, so a defect found by one value should be found by any value in that partition —
making one value per partition sufficient (and more redundant). The failure mode this
prevents: dozens of tests all inside the same valid class, and zero for invalid input.

## Context Discovery

Infer from spec/code before asking:

- What are the inputs/outputs and their valid domains? Read validation code, schemas,
  and API/type definitions — partitions come from the specified behavior, not guesses.
- Are there output partitions too? (e.g. "discount tier" outputs) — partition outputs,
  not just inputs.
- Implementation mode: which framework/language? (detect: pytest/Jest/Vitest/JUnit.)

## Instructions

1. **Identify partitions per parameter**: split each input's domain into classes that
   are handled the same way. Cover the whole domain — every possible value falls in
   exactly one partition. Include both **valid** partitions (accepted) and **invalid**
   partitions (rejected). Partition outputs where behavior differs by result band.

2. **Pick one representative per partition**: any interior value (BVA handles the
   edges). Avoid boundary values here to keep the two techniques distinct.

3. **Cover every invalid partition with its own test**: and assert the *specific*
   expected behavior (error code/message), not merely "rejected." Test one invalid
   partition at a time so a failure localizes to one cause.

4. **Trace class → requirement**: tag each partition/test with the requirement it
   derives from, so coverage is auditable and gaps are visible.

5. **Hand off edges to BVA**: note which partition boundaries need boundary-value
   analysis; EP + BVA together give efficient, high-coverage functional testing.

## Output Format

### design mode

| Param | Partition | Valid? | Representative | Expected Result | Trace |
|---|---|---|---|---|---|
| age | 18–65 | valid | 40 | accepted | REQ-12 |
| age | < 18 | invalid | 10 | 400 AGE_TOO_LOW | REQ-12 |
| age | > 65 | invalid | 80 | 400 AGE_TOO_HIGH | REQ-12 |

### implementation mode

One parameterized case per partition (pytest idiom; adapt to the repo's framework):

```python
@pytest.mark.parametrize("age,expected_status,code", [
    (40, 201, None),            # valid: 18–65
    (10, 400, "AGE_TOO_LOW"),   # invalid: < 18
    (80, 400, "AGE_TOO_HIGH"),  # invalid: > 65
])
def test_age_partitions(client, age, expected_status, code):
    ...
```

## Anti-Patterns

- **Only valid partitions** — LLMs enumerate accepted classes and skip rejected ones.
  **Guard:** every parameter yields at least one invalid partition with a specific
  expected error before the set is complete.
- **Redundant intra-partition tests** — five tests all inside "valid 18–65." **Guard:**
  one representative per partition; more values in the same class add no coverage.
- **Partitions from assumption, not spec** — inventing classes the requirement doesn't
  define. **Guard:** cite the requirement/schema each partition derives from.
- **Incomplete domain** — partitions that don't cover the whole input space (a value
  belongs to no class). **Guard:** classes must be exhaustive and non-overlapping.

## Related Skills

- `boundary-value-analysis` — tests the edges of the partitions EP identifies; run EP
  first, then BVA on each ordered partition's boundaries.
- `decision-table-testing` — when the outcome depends on combinations of conditions.

## References

- ISTQB CTFL v4.0 Syllabus §4.2.1 (Equivalence Partitioning)
- ISO/IEC 25010:2023 — Functional Suitability (functional correctness)
