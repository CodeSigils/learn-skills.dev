---
name: code-review
description: >-
  Use this skill whenever the user asks for a code review, package review, PR
  review, or architectural audit.
---

## Intent

- Perform analysis only unless the user explicitly asks for edits.
- Prioritize actionable, evidence-based findings over general advice.
- Optimize for high-signal findings, not exhaustive commentary.
- Default to review behavior that matches the active agent instructions unless
  the user asks for a different report shape.

## Communication Style

- Use plain language. Avoid jargon when a simpler phrase works.
- Keep each finding short and concrete.
- Do not offer alternate report versions unless the user explicitly asks.
- Do not defer actionable fixes to a follow-up format.
- Prefer concise output over exhaustive templates when the issue is simple.
- Put findings first. Summaries are secondary.
- Order findings by severity, then by confidence.
- Avoid hedging, consultancy tone, and explanatory filler.
- Do not pad findings with soft language such as "makes it hard to reason
  about", "the only real decision is", or similar framing.

## Scope Expectations

- For a package review, treat the package as a bounded unit and aim for deeper,
  more confident coverage within that boundary.
- For an application review, do not imply full file-by-file coverage unless you
  actually performed it. Prioritise entry points, boundaries, changed files,
  and the highest-risk areas, then state coverage limits only when they
  materially affect confidence in the findings.
- Treat the scope section as a boundary statement, not an investigation log.
- Do not list every file, route, controller, or component examined unless the
  user explicitly asks for that level of detail.
- Do not repeat file-level detail that is already covered in findings.
- Keep scope concise. State review type, coverage strategy, and meaningful
  exclusions or limits only.

## Review Workflow

1. **Define scope first**
   - Infer the target path, package, component, or changed files from the
     request. Ask only if the scope is genuinely unclear.
   - Note known exclusions explicitly before reviewing.
   - Identify the review mode:
     - `PR review` for changed files or a branch diff
     - `Package/component review` for a bounded subsystem
     - `Application audit` for broad maintainability or architecture review

2. **Explore before judging**
   - Read directory structure first.
   - Read key entry points and supporting files.
   - Avoid conclusions from a single file when behaviour spans multiple files.
   - Read local conventions and project guidance before flagging a pattern as a
     defect.
   - Check surrounding usage before calling something broken, dead, duplicated,
     or inconsistent.
   - In large repos, prioritise entry points, boundaries, and changed files
     over full traversal.

3. **Produce findings per the output template**
   - Weaknesses first, strengths optional and brief.
   - No generic advice without code evidence.
   - Prefer root-cause fixes over style-only commentary.
   - Only report issues you can defend with concrete code evidence or a clear
     behavioural risk.

## False-Positive Guard Rails

- Treat documented local patterns, overrides, and Gotime-first architecture as
  intentional unless there is direct evidence they are causing risk.
- Do not report a finding that conflicts with project guidance or a documented
  exception.
- If something looks suspicious but may be intentional, present it as a
  question or assumption, not a defect.
- Do not turn preference differences into findings.
- Do not flag missing abstraction, config-driven behavior, or refactors unless
  there is a concrete maintenance, correctness, or reuse problem.

## Core Dimensions

1. Architecture
2. Readability and clarity
3. Maintainability
4. Correctness and edge cases
5. Performance
6. Security

- Treat performance as a review dimension only when it is relevant to the
  request or there is concrete evidence of waste, scale risk, or unnecessary
  work.
- Treat security as a review dimension only when it is relevant to the request
  or there is concrete evidence of exposure, trust-boundary failure, or unsafe
  data handling.

## Convention Compliance

If an `agents.md` or similar conventions file exists at the project root, read
it before reviewing.

- Follow local project guidance before general framework preferences.
- When a local convention differs from Laravel, Livewire, or package defaults,
  treat that as intentional unless the code creates a real risk.
- Read `todo.md` at the project root if it exists and treat relevant
  feature-specific notes as known review context, not fresh findings, unless
  the user asks to revisit them or the risk has materially changed.
- Do not use `current-tasks.md` as review context. It is for active work only.

## Exclusions

- Respect user-provided exclusions exactly.
- If exclusions conflict with a requested output section, remove the section and
  note why.

## Evidence Standard

- Prefer exact file and line references when available.
- If line references are not practical, use file plus class, method, or view
  fragment.
- Describe the observed behaviour or failure mode, not just the code smell.
- Mention missing or weak tests when they materially increase risk.
- For cross-file issues, cite the smallest set of files needed to prove the
  point.

## Finding Discipline

- All findings must follow the same structure. Do not switch to ad hoc
  `Issue`/`Fix` blocks for some dimensions and a different format for others.
- Do not report low-value or repetitive findings that do not materially change
  risk, behaviour, or maintainability.
- Keep `Impact` to one sentence maximum.
- Keep `Fix` to one sentence maximum unless the issue is `Critical` and a
  longer recommendation is necessary to avoid ambiguity.
- Only include a `Trade-off` when there is a real downside, decision, or
  implementation risk that materially affects the recommendation.
- Recommendations should say what to change. Do not drift into design coaching
  unless the implementation choice is the actual issue.

## Default Output Template

Use this by default for chat responses and small reviews:

1. **Findings**
   - List findings first, ordered by severity.
   - Use this format:
     - `### Critical - Certificate endpoint has no ownership check`
     - `- **Impact:** ...`
     - `- **Evidence:** ...`
     - `- **Fix:** ...`
   - Use `Critical`, `High`, `Medium`, or `Low` exactly in the heading.
   - Keep the heading to one sentence.

2. **Open Questions or Assumptions**
   - Include only when needed to avoid false positives.

3. **Brief Summary**
   - Short overall assessment
   - Residual risk or testing gaps if no findings are present

## Extended Output Template

Use the extended structure only when the user asks for a written report or when
the scope is large enough to justify it, such as a package review or
application audit.

Always save the report as markdown file in the application root. Do this for
every review, not only when explicitly requested.

Use this structure in order for extended reviews:

1. **Scope Reviewed**
   - Review type and target
   - Coverage strategy or review boundary
   - Exclusions or meaningful limits
   - Keep this section to 2 to 4 bullets maximum

2. **Findings**
   - Ordered by severity, then by confidence.
   - Group by dimension only if it improves readability.
   - Use concise findings by default:
     - `### Critical - Certificate endpoint has no ownership check`
     - `- **Impact:** ...`
     - `- **Evidence:** ...`
     - `- **Fix:** ...`
     - `- **Trade-off:** ...` only when a real downside or decision matters
   - Expand only for high-risk issues where extra context materially helps.

3. **Top Architectural Risks** (up to 5, only for broad reviews)

4. **Top Refactor Priorities** (up to 5, only for broad reviews)

5. **Next Sprint Action Plan** (only for broad reviews)
   - 3 to 7 items, highest value first
   - For each item include:
     - **Action:** specific change to make
     - **Why now:** immediate benefit/risk reduction
     - **Effort:** `S`, `M`, or `L`
     - **First step:** exact starting task

6. **Maintainability Risk:** `Low`, `Moderate`, or `High` with reasoning

7. **Cross-Boundary Coupling Risk:** `Low`, `Moderate`, or `High` with
   reasoning

## No-Finding Reviews

- If no findings are discovered, say so explicitly.
- Still mention meaningful residual risks, unreviewed areas, or testing gaps.
- Do not pad the response with generic best practices.
