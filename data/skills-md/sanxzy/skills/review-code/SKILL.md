---
name: review-code
version: 4
description: >-
  Validate an implementation report against its plan and actual commits — reads each AC's diff and checks the code satisfies the promise. Triggers: "review the implementation", "review phase X", "verify the report", "did the implementation match the plan". Detects missing ACs, hallucinated SHAs, scope creep, FP-discipline violations, complexity mismatches, and (UI) design-decision gaps. Writes a verdict to `.plans/<feature>/reviews/{with-design,code}/<phase>.md`. One invocation = one phase.
---

# Review-code

Validate a single implementation report produced by an implementation skill. The skill reads the report, the plan it references, and the actual git commits, then renders a verdict per acceptance criterion plus cross-cutting findings. Output is a review report on disk; no code changes.

## Inputs and outputs

- **Plan input:** `<cwd>/.plans/<feature>/plan.md`.
- **Report input:** `<cwd>/.plans/<feature>/implementations/{with-design,code}/{feat,fix,refactor}/<phase_number>.md` produced by an implementation skill. The `with-design` vs `code` subdirectory marks whether the phase was UI or non-UI — UI checks run only against `with-design` reports.
- **Code input:** the git history. Every AC in the report cites at least one commit SHA (default mode) or 2–3 SHAs (TDD mode: `[red]`, `[green]`, optional `refactor`). Read each commit's diff with `git show <sha>` and inspect changed files in their post-commit state.
- **Review output:** `<cwd>/.plans/<feature>/reviews/{with-design,code}/<phase_number>.md` — verdict per AC, cross-cutting issues, recommended follow-ups. Mirrors the implementation report's directory variant so a single phase has paired implementation + review artefacts.

## Mandatory preconditions

Run **before** writing any verdict, in this order:

1. **Discover the plan.** Glob `<cwd>/.plans/*/plan.md`. If multiple, AskUserQuestion which `<feature>`. If zero, hard-stop and tell the user there is no plan to review against.
2. **Discover the report.** Glob `<cwd>/.plans/<feature>/implementations/{with-design,code}/{feat,fix,refactor}/*.md`. If multiple match the requested phase number, AskUserQuestion which one to review (rare — usually means the user re-ran an implementation under a different intent). If zero, hard-stop and tell the user there is no implementation report for that phase yet.
3. **Pick the phase.** If the user supplied "phase N", use it. Otherwise list all reports with their phase numbers and AskUserQuestion. **Hard-stop:** the report exists but no AC in it cites any commit SHA → flag the report as unreviewable and stop. (A partial gap — some ACs cite SHAs, some don't — is a critical finding logged in step 5, not a hard-stop.)
4. **Verify report ↔ plan alignment.** Extract every AC from the plan's chosen phase (ACs are checkbox items — `- [ ]` or `- [x]` — under the `## Phase N:` heading) and every AC from the report. Each plan AC must appear verbatim in the report; each report AC must trace back to the plan. If the plan has no phase matching the report's number, flag a malformed report and stop. Other mismatches are not failures — they are findings to record under "Cross-cutting issues" and to flag per-AC. Continue the review.
5. **Verify commit SHAs resolve.** For every SHA the report cites, run `git cat-file -e <sha>` (or `git show --no-patch <sha>`). Any unresolved SHA is a critical finding; record it and continue with the remaining ACs.
6. **Detect mode from the report.** If commit messages follow `test:` / `feat:` / `refactor:` prefixes with `[red]` / `[green]` markers, treat it as TDD-mode and apply the TDD-specific checks (see CHECKLIST.md). Otherwise default mode.
7. **Working tree note.** Run `git status --short`. The review does not require a clean tree (it makes no commits), but if the tree has unstaged changes that touch files under review, note this in the report so the reader knows the working-tree state may differ from the reviewed commit state. (`git show <sha>` always reflects the commit state, never the working tree.)

Only proceed to the review loop after 1–7 are complete.

## Review loop (per acceptance criterion)

For each AC the report claims to satisfy, in plan order:

1. **Read the commit(s).** `git show <sha>` for each cited SHA. In TDD mode, read the `[red]` test commit, the `[green]` production commit, and (if present) the `refactor` commit. The `[red]` commit must contain only test source (no production code in the diff) **and** the production symbol the test exercises must not yet exist at that SHA — verify with `git show <red_sha>:<production_path>` — `git show` exits with a fatal error if the path is not in that commit's tree, and that error is the expected outcome (do not treat a legitimately empty file as proof of absence). The `[green]` commit must contain only production code and the same `git show` against the post-green SHA must return the new symbol. Static-only — do not `git checkout` the SHA.
2. **Trace files.** List every file touched across the commit(s) for this AC. Check that the files actually exist in the current tree (the next AC's commits may have moved or renamed them — note if so).
3. **Verify the AC promise.** Read each touched file in its post-AC state. The code must:
   - Implement the AC's verb-led promise (a "validates X" AC must contain validation logic, not just a stub).
   - Pass the narrowest automated check the implementation skill required (unit / integration / e2e). If the implementation report claims a test exists, locate it and verify it actually exercises the new code path.
   - Stay scoped — files not plausibly related to the AC are scope creep; flag them.
4. **Apply the per-AC checklist** in [CHECKLIST.md](CHECKLIST.md) — AC promise, test evidence, FP discipline, atomic-commit hygiene (no `git add -A` smell, no unrelated diff), complexity claims, scope discipline. For UI ACs (from a `with-design`-variant report), also run the UI sub-checklist (Absolute Bans, type / palette / spacing / motion discipline, all key states present).
5. **Render a per-AC verdict** in one of: `pass`, `concern`, `fail`. Definitions:
   - **pass** — AC is fully satisfied, code is correct, no checklist items violated.
   - **concern** — AC is satisfied but something is off (FP discipline missed, complexity claim slightly wrong, comment rot, weak test, scope creep that does not break behaviour). Reviewer can ship; author should know.
   - **fail** — AC is not satisfied, a referenced SHA does not contain the claimed change, the test does not exercise the code path, an Absolute Ban (UI) is shipped, or commits mix unrelated work.

## Cross-cutting checks (run once per phase, after all ACs)

- **Plan coverage** — every plan AC in the chosen phase is addressed by at least one report AC. Missing ACs are critical.
- **Report coverage** — every report AC traces to a plan AC (or is documented as a deviation with reasoning).
- **Deviations** — each entry in the report's "Deviations from the plan" section is justified and the resulting code matches the deviation, not the original AC.
- **Open follow-ups** — each entry is real (a measurable next step), not a hand-wave. Flag any vague items.
- **FP decisions** — the report's claims match what the diffs show. If the report says "extracted a pure function," the function should actually exist and be pure. Cross-language: check the OOP-native / OOP-heavy classification was applied (see the FP discipline section in [CHECKLIST.md](CHECKLIST.md) for the language list); the report should have called out OOP-native or OOP-heavy fallbacks explicitly.
- **Complexity notes** — every Big-O claim in the report holds against the actual code. Flag any unannotated non-trivial loop, recursion, or data-structure choice.
- **Design decisions (UI / `with-design`-variant only)** — palette in OKLCH, font pairing rationale, theme rationale, key states, Absolute-Bans-avoided list — all present and verifiable in the diff. Missing or unverifiable entries are concerns; shipped Absolute Bans are fails.
- **Security surface** — no secrets, tokens, or credentials in any diff (including comments and test fixtures); new user-controlled inputs are validated or sanitised before use in DB queries, shell commands, or HTML output; new authentication / authorisation checks are present where the AC requires restricted access; no new dependency with a known unmaintained / abandoned status pulled in to satisfy the AC. Violations are critical. Full rubric in [CHECKLIST.md](CHECKLIST.md).
- **TDD discipline (TDD-mode reports only)** — for each AC, the `[red]` commit's test references the new symbol but the symbol does not yet exist in that commit's tree (proving the test would fail for the right reason, not an import error); the `[green]` commit contains the minimum code; refactor commits do not introduce new behaviour. "Don't test" carve-outs in the report must match the legitimate-cases catalogue in [CHECKLIST.md](CHECKLIST.md).

Full rubric in [CHECKLIST.md](CHECKLIST.md).

## Review report format

Write to `<cwd>/.plans/<feature>/reviews/{with-design,code}/<phase_number>.md`. If the file already exists for this phase, append a new dated section rather than overwriting — preserves audit trail across re-reviews. Date the header in ISO 8601 (`YYYY-MM-DD`). Sections:

- **Header** — feature name, phase number, mode (default / TDD), variant (with-design / code), report path under review, date.
- **Overall verdict** — one of `pass`, `pass with concerns`, `fail`. Single sentence rationale.
- **Acceptance criteria** — one block per AC: AC text verbatim, cited SHAs, verdict (`pass` / `concern` / `fail`), evidence (files inspected, what the code does), findings if any.
- **Cross-cutting issues** — bulleted list of phase-wide findings, each tagged `critical` / `concern` / `nit`.
- **Recommended follow-ups** — concrete actions the author should take before the phase is considered done. Each item names the AC it addresses (or "phase-wide").
- **Reviewer notes** — anything that informed the verdict but is not actionable (e.g., "tree had unstaged changes in `src/foo.ts` during review; verdict reflects last commit, not working state").

Do not edit the implementation report, the plan, or the source code. The review is read-only.

## What NOT to do

- **Don't review more than one phase per invocation.** If the user asks to review phases 2 and 3, review the lowest-numbered phase and hard-stop with an instruction to re-invoke.
- **Don't skip preconditions.** Especially the report ↔ plan alignment (step 4) and SHA resolution (step 5) — both surface critical findings the rest of the loop assumes are handled.
- **Don't fix the code.** This skill produces verdicts and follow-ups, not patches. If the user wants the issues fixed, they re-invoke an implementation skill with the follow-ups as a new mini-plan.
- **Don't invoke any other skill.** This reviewer is intentionally self-contained — UI checks come from CHECKLIST.md, not from re-loading design tools.
- **Don't trust the report's word over the diff.** When the report and the commit disagree, the commit wins. The whole point of the review is to catch reports that overclaim.
- **Don't rate an AC `pass` when the cited test does not exercise the new code path.** A green test that touches none of the AC's files is a `concern` at minimum, often a `fail`.
- **Don't `git checkout` or otherwise mutate the working tree.** Use `git show <sha>:<path>` to read a file at a specific commit without checking out. TDD red-commit verification is also static-only — confirm the production symbol's absence with `git show <red_sha>:<path>` rather than checking out and running the test.
- **Don't delete or overwrite a prior review report.** If a review already exists for the phase, append a new section dated today rather than replacing — preserves audit trail across re-reviews.
