---
name: review-plan
title: "Review Plan"
description: "Dispatch a sub-agent to audit planning artifacts for cross-document disconnections, vague/underspecified design points, spec violations, and architecture depth — then independently judge each finding before fixing."
disable-model-invocation: true
---

# Skill: review-plan

A **review gate** run after planning artifacts (`prd.md` / `design.md` / `implement.md`) exist but before `task.py start`. You dispatch a sub-agent to run a structured four-dimension **planning audit**, then independently judge its findings — accepting those that hold up to evidence, and rejecting false positives with a concrete reason.

This prevents two failure modes: (1) disconnections / vagueness / spec conflicts shipping into implementation undetected, and (2) over-reacting to sub-agent misreads by accepting every reported issue at face value.

---

## Step 1: Gather context

Before dispatching, collect the exact file paths the sub-agent needs. These are the **context items**:

| Category | What to include |
|---|---|
| **Task artifacts** | `prd.md`, `design.md`, `implement.md` — the three documents being audited |
| **Reference files** | Any external design reference (e.g. `ref/layout/1.md` for a UI task), current source code the task modifies |
| **Relevant specs** | Every `.trellis/spec/game/*.md` that the design touches (minimum: `theming.md`, `navigation.md`, `game-state.md`; add domain-specific specs as needed) |
| **Architecture vocabulary** | Load the `codebase-design` skill for its leading words (**module**, **interface**, **depth**, **seam**, **locality**, **leverage**, **deletion test**); the sub-agent must use these terms when reporting architecture depth findings (Dimension D) |
| **Process docs** | `.trellis/workflow.md` — for task-planning quality standards |

List each file with its absolute path. **Completion criterion**: every file the sub-agent must read is explicitly listed; no "check the spec dir for anything relevant" vagueness.

---

## Step 2: Dispatch the review sub-agent

Use a `general` sub-agent type (it supports multi-step analysis). The dispatch prompt has a fixed structure — fill in the bracketed portions:

```
Active task: <path from `task.py current`>

You are reviewing the planning artifacts for a <one-line task summary>. Do NOT modify any files. Only read and produce a structured review report.

## Task Context
<one-paragraph description of what this task builds, enough for the sub-agent to orient>

## Files to Read (read ALL of these)
### Task Artifacts
<list each prd/design/implement with full paths>

### Reference <if applicable>
<list reference files and current source code with full paths>

### Relevant Specs (check for conflicts)
<list each spec file with full paths and a 3-5 word note on what to check>

### Trellis Process
 `.trellis/workflow.md`

## Review Criteria (focus ONLY on these 4 dimensions)

### A. Cross-document Disconnections
Are there contradictions between prd.md / design.md / implement.md?
- PRD requires X, design omits X, implement doesn't list X
- implement lists a step not grounded in design
- Numbers/values differ between documents
- PRD acceptance criteria have no corresponding implement verification step

### B. Vague Points
What would confuse a trellis-implement agent?
- Undefined values (colors, sizes, limits) the implementer would have to invent
- Behaviors described as "X or Y" without a decision
- Component interactions left unspecified (e.g. "expand on click" without what expands or how)
- Missing states (empty, loading, edge cases)

### C. Spec Conflicts
Does the design/PRD contradict any spec?
- Font rules violated (theming.md: Song=serif/story, Hei=sans/system)
- Navigation rules (pager, overlays) compromised
- State access rules bypassed (UI touching state directly)
- Enum backward-compat rules broken
- Any "MUST" / "never" / "single channel" spec line contradicted

### D. Architecture Depth
Does the design.md describe **deep modules** (small interface, large implementation) or **shallow** ones (interface ≈ implementation)?
Use the `codebase-design` vocabulary — module, interface, depth, seam, locality, leverage, deletion test:

- **Module boundaries** — are components clearly named with distinct responsibilities? Watch for catch-all names ("Utils", "Helpers", "Manager") that signal no real boundary.
- **Interface < implementation** — is each component's public surface decisively smaller than what it does internally? Large parameter lists, many public functions, or one-function-per-class = red flag.
- **Seam clarity** — can each component be tested in isolation? Are dependencies explicit (constructor parameters) rather than hidden (file-level imports pulled from ambient context)?
- **Locality** — does understanding one concept require reading one file, or bouncing across 3+? Designs that scatter related logic across many small files break locality.
- **Deletion test** — if this component were removed from the design, would complexity concentrate elsewhere (pass — it was a real module) or merely relocate (fail — it was a pass-through)?
- **Leverage** — does a small amount of interface code produce a large amount of functionality? Or does every behavior require its own dedicated public function?

## Output Format
Produce a single structured report:
| # | Severity | Dimension | Location | Issue |
(Use HIGH/MED/LOW. Dimension = A/B/C/D. Be specific with section/line references. If a dimension has no findings, state "None found.")
```

**Completion criterion**: sub-agent returns a report with findings in all four dimensions (even if some are "None found").

---

## Step 3: Judge findings independently

For **every** finding the sub-agent reports, apply independent judgment with evidence:

1. **Read the cited spec / line yourself.** Do not trust the sub-agent's characterization — verify against the actual file.
2. **Classify each finding:**
   - **Accept** — the finding is real. The sub-agent correctly identified a disconnection, vagueness, or spec violation. Fix it.
   - **Reject** — the finding is inaccurate after your own inspection. Write a one-line reason (e.g. "pre-existing since C2, not introduced by this task", "sub-agent misread the spec — the cited rule applies to X, not Y", "out of scope for this task").
   - **Defer** — the finding is real but belongs to a different task or phase. Note it and move on.

Key rejection signals (from guides/index.md §54-65):
- **Trust-boundary confusion** — the sub-agent flags internal data as untrusted external input
- **Ignoring design comments** — the sub-agent flags intentional behavior documented in comments as bugs
- **Variable misreading** — the sub-agent didn't trace a variable to its definition

**Completion criterion**: every finding has a verdict (accept/reject/defer) with a one-line rationale grounded in evidence, not opinion.

---

## Step 4: Fix accepted findings

For each accepted finding, edit the planning documents (`prd.md` / `design.md` / `implement.md`) to close the gap. Prefer the Edit tool over rewriting — each fix should be a targeted string replacement.

Priority order: **HIGH first** (spec conflicts), then MED (vagueness the implement agent would guess wrong), then LOW (minor polish).

After all accepted fixes, do a final cross-check: verify the fixed documents no longer contradict each other on the key decisions that were changed.

**Completion criterion**: every accepted finding maps to a concrete edit; design ↔ implement ↔ prd are consistent on all resolved points.

---

## Reference: Review Dimension Details

### A. Disconnections — common patterns

| Pattern | Example |
|---|---|
| PRD requires, design omits | PRD says "cooldown fills card background", design shows independent progress bar |
| Numbers diverge | PRD says "110dp log height", implement says "120dp" |
| Acceptance without verification | PRD AC says "card ≤40% button width", no implement step measures it |
| File mismatch | Design says "embed LogList component", implement says "render log inline" |

### B. Vague points — what implementers guess

| Void | Risk |
|---|---|
| Undefined color/font/spacing value | Implementer picks a default that differs from design intent |
| "X or Y" not decided | Implementer picks the wrong branch, wasting a review cycle |
| Missing state description | Implementer doesn't handle empty/loading/error, ships a crash |
| Unclear trigger action | "expand on click" — click what exactly? The row? An icon? |

### C. Spec conflicts — red lines

These are the highest-severity findings because they violate locked **cross-cutting decisions** (parent task D1-D3) or canonical **spec contracts** written in earlier phases. A spec violation that ships becomes tech debt; one caught here costs nothing.

Always verify by reading the spec file directly — sub-agents sometimes misattribute which rule a design line violates.

### D. Architecture depth — from codebase-design vocabulary

These principles apply to design.md's architecture (component split, data flow, dependency graph), even before a single line of code exists:

| Principle | What to check | Red flag |
|---|---|---|
| **Module** | Named, distinct responsibility | "Utils", "Helpers" |
| **Interface** | Small public surface vs internal logic | One function per class; large param lists |
| **Depth** | Interface ≪ implementation | "Thin wrapper" over a library with no added semantics |
| **Seam** | Testable in isolation; explicit dependencies | Hidden file-level imports; ambient context |
| **Locality** | Concept understood from one file | Scattered logic across 3+ files for one concept |
| **Leverage** | Small interface → large functionality | Every behavior = new public function |
| **Deletion test** | Would removal concentrate complexity? | Removal just relocates identical logic |

> **Calibration for UI tasks**: zone-based composables (e.g. `CampFooter`, `CampHeader`) may legitimately have broader interfaces than domain modules — their depth comes from **responsibility partitioning** (each zone owns one region of the screen, one category of user interaction), not from individual composable depth. A footer with 4 sub-concerns (population, workers, log, vibration) that passes the deletion test IS deep at the layout level. Flag only when a single composable mixes *unrelated* responsibilities (e.g. card rendering AND network fetching), or when the partition is so fine that understanding one zone requires reading 3+ files (locality violation).

The sub-agent must use these terms — not drift into "component", "service", "API", or "boundary".

---

## Quality Bar

- [ ] Sub-agent received all context items and produced a report in the four dimensions.
- [ ] Every finding has an independent verdict (accept/reject/defer) with evidence-based rationale.
- [ ] Accepted HIGH findings are fixed; accepted MED/LOW findings are fixed or explicitly deferred with reason.
- [ ] The three planning documents are internally consistent on all resolved points.
