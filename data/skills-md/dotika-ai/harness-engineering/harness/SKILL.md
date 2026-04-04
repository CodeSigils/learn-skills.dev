---
name: harness
description: "Complexity-aware development router with built-in knowledge capture. Accepts a task description, a PRD file path, or pasted requirements. Classifies complexity (simple/medium/hard), dispatches to the right orchestration (direct/plan/3-agent harness), verifies with real interactions (browser, API, DB), and documents solutions for compounding knowledge. Use when starting any development task."
argument-hint: "[Task description, PRD file path, or pasted requirements]"
---

# Harness

One skill. Classify, execute, verify, document.

## Input

<input> #$ARGUMENTS </input>

### Input Triage

Determine what was provided:

| Input type | How to detect | Action |
|-----------|--------------|--------|
| **PRD / spec file path** | Input is a path to an existing file (`.md`, `.txt`, `.yaml`, etc.) | Read the file. Use its content as the task source. Store path for reference |
| **Pasted requirements** | Input is multi-line, contains sections like "Requirements", "Acceptance Criteria", "User Stories", etc. | Treat as inline PRD. Save to `docs/specs/[slug]-prd.md` for traceability |
| **Task description** | Input is a short prompt (1-4 sentences) | Use directly as task description |
| **Empty** | No input | Ask: "What do you want to build or fix? You can describe the task, paste requirements, or drop a PRD file path." |

When the input is a PRD (file or pasted):
1. Read it fully
2. Summarize the key deliverables in 2-3 bullets
3. Classify complexity from the PRD content (not from the PRD length)
4. The PRD becomes the source of truth — reference it throughout execution

---

## Phase 0: Bootstrap & Classify

### First-Run Bootstrap

On first use in a project, set up the scaffolding:

**1. Create directories** (skip what already exists):
- `docs/plans/`
- `docs/solutions/`
- `docs/specs/`
- `docs/verification/`

**2. Set up CLAUDE.md as a table of contents.**

> "We tried the 'one big AGENTS.md' approach. It failed. Context is a scarce resource. Instead of treating AGENTS.md as the encyclopedia, we treat it as the table of contents."

Read the project's CLAUDE.md (or AGENTS.md):

| State | Action |
|-------|--------|
| **Doesn't exist** | Create CLAUDE.md with the table-of-contents structure below |
| **Exists but wall of text** | Propose restructuring. Show diff, ask approval |
| **Exists and structured** | Add `docs/` pointers if missing. Leave the rest |

**Table-of-contents structure** (adapt to what the project already has):

```markdown
# [Project Name]

## Quick Start
[How to run — 2-3 lines]

## Architecture
[1-2 sentence overview, pointer to deeper doc]

## Project Knowledge
docs/plans/        — implementation plans
docs/solutions/    — solved problems (searchable by module/tags/problem_type)
docs/specs/        — sprint contracts and technical specs
docs/verification/ — QA evidence (screenshots, API results)

Search docs/solutions/ before debugging in documented areas.

## Development
[Test, lint, build commands — just the commands]
```

~100 lines max. Pointers, not content. Ask confirmation before writing.

### Classify Complexity

Read `references/complexity-router.md` for the full matrix.

| Signal | Tier |
|--------|------|
| 1-2 files, clear, low risk | **Simple** |
| 3-10 files, some design decisions | **Medium** |
| 10+ files, cross-cutting, architectural, high-risk | **Hard** |

**Overrides:** "just do it" -> Simple. "plan this" -> Medium. "harness"/"full mode" -> Hard.

State the tier and reasoning in one sentence. If unsure, ask.

---

## Tier 1: SIMPLE — Direct Execution

### Execute
1. Read affected files
2. Implement the change, follow existing patterns
3. Commit

### Verify

<critical_requirement>
Verify with real interactions, not generated test files.
</critical_requirement>

| Change type | Verification |
|------------|-------------|
| UI | **Browser** — open the page (claude-in-chrome, Playwright, computer use), interact, confirm |
| API | **API call** — hit endpoint with valid + invalid inputs, check responses |
| Data | **DB query** — verify state after operation |
| Logic/config | **Existing tests** — run them if they exist. Don't create new ones |

### Done -> Jump to Phase 4 (Document)

---

## Tier 2: MEDIUM — Plan Then Execute

### 2.1 Plan

If `ce:plan` is available, delegate to it. Otherwise, inline plan:
1. Scan affected files and patterns
2. Check `docs/solutions/` for related past solutions
3. Draft: goal, files, approach, verification strategy
4. Present to user for approval (`AskUserQuestion` in Claude Code)

### 2.2 Execute with Checkpoints

For each step:
1. Implement
2. **Verify after each meaningful change:**
   - UI -> browser automation
   - API -> call the endpoint
   - Data -> query the database
3. Commit logical units

### 2.3 Final Verification

- Boot the app, walk through affected flows via browser
- Hit all affected API endpoints
- Run existing test suite if one exists
- Check logs for errors

### Done -> Jump to Phase 4 (Document)

---

## Tier 3: HARD — 3-Agent Harness

Full Planner -> Generator -> Evaluator. The generator never grades its own work.

Read `references/sprint-contract.md` for contract format.
Read `references/verification-strategies.md` for evaluator methods.

> "Separating the agent doing the work from the agent judging it proves to be a strong lever."

### 3.1 Planner

Launch `harness-engineering:planner` (or delegate to `ce:plan` then write sprint contracts on top).

Produces:
- **Spec** -> `docs/specs/[feature]-spec.md`
- **Sprint contracts** -> `docs/specs/[feature]-sprint-[N]-contract.md`

Present to user for approval before proceeding.

### 3.2 Generator-Evaluator Loop

For each sprint:

**Generator:**
1. Read sprint contract
2. Implement features in scope
3. Self-check: boot the app, try the feature, fix obvious issues
4. Commit and signal ready

**Evaluator:**
Launch `harness-engineering:evaluator` with the sprint contract + access to browser automation, terminal, logs.

The evaluator tests each criterion through **real interaction** — opens pages, calls APIs, queries databases. Skeptical by default. Writes QA report to `docs/verification/[feature]/qa-report.md`.

| Result | Action |
|--------|--------|
| PASS | Next sprint |
| FAIL | Specific feedback -> generator iterates -> re-evaluate |
| FAIL x3 | Escalate to user |

### 3.3 Cross-Sprint Regression

After each sprint, verify previous sprints still work.

### Done -> Jump to Phase 4 (Document)

---

## Phase 4: Document the Solution

After successful execution on any tier, capture the knowledge.

### 4.1 Assess Documentation Value

| Condition | Action |
|-----------|--------|
| Trivial change (typo, config, rename) | Skip documentation |
| Non-trivial bug fix | Document |
| New pattern or practice discovered | Document |
| User says "that worked" / "it's fixed" | Document |
| Hard tier (always non-trivial) | Document |

If unclear, ask: "Worth documenting this for future reference?"

### 4.2 Extract Context

From the conversation history and work just completed, extract:

1. **Classify track** — Read `references/schema.yaml`:
   - Bug fix -> Bug track (requires symptoms, root_cause, resolution_type)
   - Practice/pattern -> Knowledge track (lighter requirements)

2. **Extract fields:**
   - Module and component affected
   - Problem type (from schema enum)
   - Severity
   - Track-specific fields (symptoms, root_cause for bugs; applies_when for knowledge)

3. **Search for related docs** — Grep `docs/solutions/` for similar issues:
   - If high overlap found (same problem + same solution) -> update existing doc instead of creating duplicate
   - If moderate overlap -> create new doc, note the relationship
   - If none -> create new doc

### 4.3 Write the Solution

Read `assets/resolution-template.md` for the template.

1. Generate filename: `[sanitized-problem-slug]-[YYYY-MM-DD].md`
2. Build YAML frontmatter — validate against `references/schema.yaml`
3. Fill the template sections from extracted context
4. Create directory if needed: `mkdir -p docs/solutions/[category]/`
5. Write the file

### 4.4 Discoverability Check

Check that the project's CLAUDE.md/AGENTS.md would lead an agent to find `docs/solutions/`. If not, propose adding a pointer (same logic as the first-run bootstrap, but only the `docs/` section).

### 4.5 Report

**After work + documentation:**
```
Done. [1-sentence description of the work]
Verified: [browser check / API call / evaluator QA report / etc.]
Documented: docs/solutions/[category]/[filename].md
```

**After work only (documentation skipped):**
```
Done. [1-sentence description]
Verified: [how]
```

---

## Auto-Invoke Triggers

This skill's documentation phase (Phase 4) can also be triggered by these phrases after any work session:

- "that worked"
- "it's fixed"
- "working now"
- "problem solved"

When triggered this way, skip Phase 0-3 and go directly to Phase 4 to document the solution from the current conversation context.

---

## Verification Principles (All Tiers)

1. **Browser automation first** — For UI changes, open the page and interact. Screenshots are evidence.
2. **API calls for backend** — Hit real endpoints. Don't mock.
3. **Database checks for data** — Query real state.
4. **Existing tests are a bonus** — Run what exists. Don't generate new test files.
5. **Logs and observability** — Read console messages, check server logs.
6. **Boot the app** — For non-trivial changes, the app should be running during verification.
