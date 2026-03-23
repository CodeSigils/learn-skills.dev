---
name: create-plan
description: >
  Generate self-contained, agent-executable Execution Plans (ExecPlans) from PRD files.
  Use this skill whenever the user wants to "create a plan", "generate an execution plan",
  "turn a PRD into a plan", "write an ExecPlan", "create an implementation plan from a PRD",
  "break down a PRD into steps", "make a plan from requirements", "convert PRD to plan",
  or mentions "ExecPlan", "execution plan", or "implementation plan" in the context of
  producing one from a requirements document. Also triggers when the user has a PRD.md
  file and wants actionable next steps, says "plan the implementation", "create milestones
  from this PRD", or "how do I implement this PRD". This skill produces plans that a
  stateless coding agent or human novice can follow from top to bottom to deliver working,
  observable results.
---

# Create Plan

Transform a Product Requirements Document (PRD) into one or more self-contained Execution Plans (ExecPlans) that a coding agent or human novice can follow end-to-end without any prior context.

## Why ExecPlans matter

A PRD defines *what* to build and *why*. An ExecPlan defines *how* — the exact sequence of file edits, commands to run, and outputs to observe. The gap between a PRD and working code is where agents drift, retry, and produce noisy pull requests. An ExecPlan closes that gap by making every step explicit, every term defined, and every outcome verifiable.

The bar is high: a stateless agent reading only the ExecPlan file (with no memory of prior conversations, no access to the PRD, no external docs) should be able to produce working, observable results. If the plan requires knowledge that isn't in the plan itself, it fails this bar.

## How to run this skill

### Step 1: Locate and read the PRD

Ask the user for the PRD file path if not provided. Read it thoroughly — every section matters. Pay special attention to:

- **Epics and phase plan** — these become your milestones
- **Acceptance criteria** — these become your validation steps
- **Tech stack decisions** — these constrain your concrete steps
- **Build/run/validate commands** — these go directly into your ExecPlan
- **Architecture and repo boundaries** — these orient the reader
- **Non-goals and forbidden approaches** — these prevent scope creep

If the PRD has an ambiguity log with unresolved items, flag them to the user before proceeding. Unresolved ambiguity in the PRD becomes dangerous guesswork in the ExecPlan.

### Step 2: Decide the plan structure

A single PRD may produce one ExecPlan or several, depending on scope.

**One ExecPlan per epic** is the default when:
- The PRD has multiple epics that are independently deliverable
- Each epic takes more than a few file changes to implement
- Different epics touch different parts of the codebase

**One ExecPlan for the whole PRD** works when:
- The PRD describes a single cohesive feature
- The epics are tightly coupled and can't be implemented independently
- The total scope is small enough to fit in one plan without losing clarity

Ask the user which approach they prefer if it isn't obvious. When producing multiple ExecPlans, each must be fully self-contained — don't say "as described in ExecPlan 1"; repeat the context.

### Step 3: Research the codebase

Before writing anything, understand the current state of the repository. For each area the plan will touch:

1. Read the relevant source files to understand existing code structure
2. Identify the exact file paths, function names, module boundaries
3. Note any patterns the codebase follows (naming conventions, test organization, error handling)
4. Check for existing tests that cover the area you'll modify

This research is what makes the ExecPlan concrete rather than hand-wavy. You can't write "edit the handler function" — you need to write "in `src/api/handlers/user.ts`, modify the `createUser` function (line ~45) to add validation".

### Step 4: Write the ExecPlan

Use the skeleton from `references/exec-plan-guidelines.md` as your structural backbone. Every mandatory section must appear. Here is how to fill each one:

#### Title
Short, action-oriented. "Add JWT authentication to the API" not "Authentication Feature Implementation Plan".

#### Living document notice
State that this ExecPlan is a living document and that the Progress, Surprises & Discoveries, Decision Log, and Outcomes & Retrospective sections must be kept up to date as work proceeds.

#### Purpose / Big Picture
Two to four sentences explaining what someone gains after this change and how they can see it working. Write from the user's perspective: "After this change, you can..." followed by "To see it working, run X and observe Y." Pull this directly from the PRD's problem statement and acceptance criteria.

#### Progress
Start with all steps unchecked. Use checkboxes. Each step should be granular enough that checking it off is unambiguous. Group steps under milestone headings if there are multiple milestones.

#### Surprises & Discoveries
Start empty with a note: "No discoveries yet — this section will be populated during implementation."

#### Decision Log
Pre-populate with decisions already made in the PRD (tech stack choices, architectural decisions, rejected alternatives). Format each as: Decision, Rationale, Source (e.g., "PRD Section 8").

#### Outcomes & Retrospective
Start empty with a note: "To be completed at major milestones and at plan completion."

#### Context and Orientation
This is where self-containment lives or dies. Explain the current state of the repository as if the reader has never seen it. Name every file and module that matters, by full path. Define every non-obvious term. If the plan touches multiple areas, include an orientation paragraph explaining how those areas connect.

Do not say "see the architecture docs" or "as described in the PRD." Embed the knowledge here. If the PRD says the project uses Next.js with App Router, explain what that means for file organization in this specific project.

#### Plan of Work
Prose description of the sequence of edits and additions. For each change, name:
- The file (full repository-relative path)
- The location within the file (function, class, module)
- What to insert, modify, or remove
- Why this change is needed (connecting it back to the user-visible outcome)

Keep it concrete but don't paste entire code blocks here — that's what Concrete Steps is for. This section tells the story; Concrete Steps provides the recipe.

#### Concrete Steps
The exact commands to run and where to run them. Show working directory. When a command produces output, show a short expected transcript so the reader can compare. Use indented blocks for command output (not nested code fences).

Structure this as a numbered sequence. Each step should include:
1. What to do (plain language)
2. The exact command or edit
3. What you should see (expected output)
4. How to tell if it worked

#### Validation and Acceptance
Pull directly from the PRD's acceptance criteria, but translate them into concrete, runnable checks. "The API returns HTTP 200 with a valid JWT" becomes:

    curl -X POST http://localhost:3000/api/auth/login \
      -H "Content-Type: application/json" \
      -d '{"email": "test@example.com", "password": "test123"}'

    Expected: HTTP 200 with JSON body containing "token" field.

Include the project's test commands and expected pass counts. If the PRD specifies tests that should fail before and pass after, include both scenarios.

#### Idempotence and Recovery
Write steps so they can be run multiple times without damage. If a step creates a file, note that re-running will overwrite it. If a migration is destructive, spell out the rollback path. If a step can fail halfway, explain how to retry.

#### Artifacts and Notes
Include the most important terminal transcripts, short diffs, or log snippets as indented examples. Keep them focused on what proves success.

#### Interfaces and Dependencies
Name every library, module, and service the plan depends on, with versions where relevant. Specify the function signatures, types, and interfaces that must exist after implementation. Use stable, fully-qualified names.

### Step 5: Self-review the ExecPlan

Before presenting it to the user, verify against these criteria:

- **Self-contained**: Could someone with only this file and the repo produce working results? No references to "the PRD", "the architecture doc", or "as discussed earlier."
- **Novice-accessible**: Are all terms defined? Are file paths complete? Are commands copy-pasteable?
- **Outcome-focused**: Does every milestone end with something observable? Can the reader tell success from failure?
- **Idempotent**: Can steps be re-run safely?
- **Validated**: Are there concrete test commands with expected outputs?
- **Living-ready**: Are all four living sections present (Progress, Surprises, Decision Log, Outcomes)?

If any check fails, fix it before presenting.

### Step 6: Write the file

Save the ExecPlan as a `.md` file. Naming conventions:
- Single plan: `PLAN.md` in the project root (or wherever the user specifies)
- Multiple plans: `plans/PLAN-E<N>-<short-name>.md` (e.g., `plans/PLAN-E1-auth-setup.md`)

When writing the file, omit the outer triple-backtick fence (since the file content *is* the ExecPlan). Use indented blocks instead of nested code fences for any commands, transcripts, or code snippets within the plan.

### Step 7: Summarize to the user

After writing, give the user a brief summary:
- How many ExecPlans were created and where they were saved
- The milestones in each plan
- Any assumptions you made that they should verify
- Any PRD ambiguities that need resolution before execution

## Common pitfalls to avoid

**Vague steps**: "Update the configuration" tells the reader nothing. "In `config/database.ts`, add a `pool` property to the `DatabaseConfig` interface with `min: 2, max: 10`" tells them everything.

**Missing context**: Don't assume the reader knows what Next.js App Router is, where API routes live, or what `prisma generate` does. Define it or explain it, every time.

**Internal-only acceptance**: "Added a HealthCheck struct" is not acceptance. "After starting the server, `GET /health` returns HTTP 200 with body `OK`" is acceptance.

**External references**: "See the Prisma docs for migration syntax" fails the self-containment test. Embed the specific syntax needed, in your own words.

**Skipping the living sections**: These aren't optional bureaucracy — they're how the next contributor (or the same agent after context loss) picks up where you left off.

## Reference files

- `references/exec-plan-guidelines.md` — The complete ExecPlan specification with formatting rules, requirements, and the skeleton template. Read this for the authoritative rules on what makes a good ExecPlan.
