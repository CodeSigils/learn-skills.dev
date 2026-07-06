---
name: exploratory-testing
description: >-
  Plan and run structured exploratory testing using session-based test management
  (SBTM) — charters, time-boxes, and session sheets — to find defects scripted tests
  miss. Use when: "exploratory testing," "探索的テスト," "ad-hoc testing done right,"
  "session-based testing," "test charter," "let's poke at the new feature," or when a
  feature is new/underspecified and you need learning + discovery, not just checking.
  Produces a charter set and session-sheet template (design mode). Not for: repeatable
  regression coverage — use the scripted test-design skills. Related: risk-based-testing,
  test-strategy-doc.
license: MIT
metadata:
  version: "1.0"
  istqb: "CTFL v4.0 §4.4.2"
  iso25010: [functional-suitability]
  mode: [design]
---

# Exploratory Testing

Design, execute, and evaluate tests simultaneously while learning the product — but
structured with charters and time-boxes so it is accountable, not random clicking.

## Objective

A set of chartered exploratory sessions and a session-sheet format that make discovery
repeatable and traceable. Per CTFL v4.0 §4.4.2, in exploratory testing tests are
simultaneously designed, executed, and evaluated while the tester learns about the test
object; it is often conducted as **session-based testing** structured with a **test
charter** within a **time-box**. The failure mode this prevents: either no exploration
at all (only scripted checks that confirm what you already expected) or unstructured
poking that produces no record of what was covered.

## Context Discovery

- What is new, changed, risky, or underspecified? Exploration pays off most there —
  pair with `risk-based-testing` to aim charters at high-risk areas.
- What is already covered by scripted tests? Explore the gaps and the assumptions, not
  what automation already verifies.
- What quality aspects matter here (functionality, UX, edge data, error handling,
  security-adjacent behavior)? Charters target aspects, not just screens.
- Time budget and who runs the sessions (human tester, or an agent driving the app).

## Instructions

1. **Write charters, not scripts**: each charter states a *mission* — what to explore
   and why — e.g. "Explore checkout with invalid/edge payment data to discover
   error-handling and data-validation defects." Keep it focused enough for one session.

2. **Time-box sessions** (SBTM): fixed sessions (e.g. 60–90 min) per charter. A
   time-box forces prioritization and produces comparable session records.

3. **Explore then branch**: start with the charter mission; when you find something
   interesting, follow it with focused tests, then return to the charter. Record test
   ideas that fall out of scope as new charters.

4. **Capture as you go** in a session sheet: charter, areas covered, test notes,
   **bugs**, **issues/questions**, and a rough split of time (testing vs setup vs
   investigation). The record is what makes exploratory testing auditable.

5. **Debrief and feed back**: turn confirmed defects into reports, open questions into
   spec clarifications, and valuable paths into scripted regression tests (hand off to
   the test-design skills).

## Output Format

### design mode

Charter set:

```
| Charter ID | Mission (explore … to discover …) | Target areas | Risk | Time-box |
| EXP-01 | Explore bulk CSV import with malformed/edge files to discover parsing and error-handling defects | import, validation | High | 90m |
```

Session sheet template (SBTM):

```
Charter:        EXP-01
Tester / Date:  …
Time-box:       90m   (Test 60 / Setup 15 / Bug investigation 15)
Areas covered:  …
Test notes:     … (what was tried, observations)
Bugs:           BUG-… (title, repro)
Issues/Questions: … (spec gaps, things to clarify)
New charter ideas: …
```

## Anti-Patterns

- **"Exploratory = unstructured/random"** — the most common misuse; clicking around
  with no mission or record. **Guard:** every session has a charter, a time-box, and a
  session sheet; without them it is not exploratory testing, just poking.
- **No documentation** — findings and coverage vanish after the session. **Guard:**
  capture areas covered + bugs + issues as you go; the sheet is a deliverable.
- **Replacing scripted testing entirely** — exploration complements, not replaces,
  regression coverage. **Guard:** feed valuable paths back into scripted test-design.
- **Claiming exploration without interacting** — an agent asserting it "explored" from
  reading code alone. **Guard:** exploratory findings must come from actually
  exercising the running product; cite what was done, not what was inferred.

## Related Skills

- `risk-based-testing` — prioritizes which areas get exploratory charters.
- `test-strategy-doc` — reserves exploratory time in the overall approach.
- Scripted techniques (`equivalence-partitioning`, `state-transition-testing`, …) —
  where confirmed exploratory findings become repeatable tests.

## References

- ISTQB CTFL v4.0 Syllabus §4.4 (Experience-based Test Techniques), §4.4.2 (Exploratory Testing)
- ISO/IEC 25010:2023 — Functional Suitability (and cross-characteristic discovery)
