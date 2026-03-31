---
name: process-mapper
description: "Extract process flows from documents, build formal process maps, surface gaps through user interview, then score each step for automation potential. Classifies steps as RPA, one-shot LLM, agentic AI, human-in-the-loop, or human-only."
effort: max
user-invocable: true
triggers: "process map, map this process, process flow, workflow mapping, automation assessment, SIPOC, process extraction, map the steps"
---

# Process Mapper

Extract a formal process flow from source documents, surface gaps through structured interview, visualize as a Mermaid flowchart, and score each step for automation potential.

## When to Use

- You have SOPs, policy documents, meeting notes, or verbal descriptions of a process
- You want to understand the actual flow (not what people think it is)
- You want to identify which steps are candidates for automation, AI, or should stay human
- You are preparing to build agents or skills to automate parts of a workflow

## Five Phases

| Phase | What Happens | Output |
|-------|-------------|--------|
| 1. Intake & Scope | Read sources, produce SIPOC, user confirms boundary | `SIPOC.md` |
| 2. Process Extraction | Extract steps, actors, decisions, exceptions from sources | `process-steps.md` |
| 3. Gap Analysis & Interview | Surface missing information, user fills gaps | `gap-log.md` (updated `process-steps.md`) |
| 4. Visualization | Generate Mermaid flowchart, render to SVG | `process-map.mmd` + `.svg` |
| 5. Automation Assessment | Score each step, classify pathway, prioritize | `automation-assessment.md` |

---

## Phase 1: Intake & Scope (SIPOC)

### Step 1: Gather source material

Ask the user: "What documents describe this process? Point me to files, paste text, or describe it verbally."

Read all provided source material before proceeding. Do not start extracting until you have read everything.

### Step 2: Produce SIPOC table

From the source material, produce a SIPOC (Suppliers, Inputs, Process, Outputs, Customers) table:

```markdown
| Element | Description |
|---------|-------------|
| **Suppliers** | Who/what provides inputs to this process? |
| **Inputs** | What data, materials, or triggers start or feed the process? |
| **Process** | 3-7 high-level steps (not detailed — just the major phases) |
| **Outputs** | What does the process produce? |
| **Customers** | Who receives or uses the outputs? |
```

### Step 3: Confirm scope

Present the SIPOC to the user and ask:
- "Is this the right process boundary?"
- "Are there upstream or downstream steps I should include or exclude?"
- "Is there a specific part of this you want to focus on?"

Do not proceed to Phase 2 until the user confirms scope.

### Step 4: Create output directory

Create `process-[name]/` in the appropriate project directory (ask the user where if unclear). Write `SIPOC.md` with frontmatter:

```yaml
---
title: "[Process Name] - SIPOC"
created: YYYY-MM-DD
last_modified: YYYY-MM-DD
tags: [process-map, sipoc]
status: confirmed
---
```

---

## Phase 2: Process Extraction

### Step 1: Chain-of-thought extraction

Work through the source material using this sequence (do not skip steps):

1. **List all activities** mentioned in the source material. Include everything, even if the sequence is unclear. Tag each with its source reference (document name + section/page).

2. **Identify actors** for each activity. Use role names, not personal names. If the actor is unclear, mark as `[UNKNOWN ACTOR]`.

3. **Sequence the activities.** Identify what triggers each step and what its completion enables. Mark parallel steps and decision branches.

4. **Identify decision points.** What conditions determine the branch? What are the possible outcomes?

5. **Identify inputs and outputs** for each step. What data or artifacts flow between steps?

6. **Identify exception paths.** What can go wrong? What happens when it does? If the source material doesn't specify, mark as `[EXCEPTION PATH UNKNOWN]`.

### Step 2: Build the process steps table

Write `process-steps.md` with this structure:

```markdown
| Step | Activity | Actor | Trigger | Inputs | Outputs | Decision? | Exception Path | Confidence | Source |
|------|----------|-------|---------|--------|---------|-----------|---------------|------------|--------|
| 1 | Receive request | Intake coordinator | Email submission | Request form | Logged ticket | N | — | HIGH | SOP §2.1 |
| 2 | Triage request | Team lead | New ticket | Ticket details | Priority assignment | Y: Priority H/M/L | Incomplete form → return to requester | MODERATE | SOP §2.3 |
```

**Confidence levels:**
- **HIGH** — explicitly stated in source material with clear detail
- **MODERATE** — implied or partially described; reasonable inference
- **LOW** — inferred from context, not stated; needs user confirmation

### Step 3: Flag what you don't know

At the bottom of process-steps.md, add a section:

```markdown
## Known Gaps (to be resolved in Phase 3)
- [ ] Step 4: Approval criteria not specified
- [ ] Step 7: Actor unknown — who performs the technical review?
- [ ] Steps 8-10: Sequence assumed sequential, could be parallel
- [ ] No exception handling described for [specific scenario]
- [ ] Time/frequency data not available for any step
```

---

## Phase 3: Gap Analysis & User Interview

### Step 1: Present gaps

Show the user the Known Gaps list from Phase 2. Group by type:

1. **Missing decision logic** — "Step X says 'if approved' but doesn't specify criteria"
2. **Unspecified actors** — "Who performs the review in Step Y?"
3. **Missing exception paths** — "What happens if Z fails?"
4. **Assumed sequences** — "Steps A-C appear sequential but could be parallel"
5. **Missing metrics** — "How often does this run? How long does Step N take?"
6. **Scope questions** — "Is [adjacent process] in scope or out?"

### Step 2: Interview

Walk through each gap. Record the user's answers in `gap-log.md`:

```markdown
---
title: "[Process Name] - Gap Log"
created: YYYY-MM-DD
last_modified: YYYY-MM-DD
tags: [process-map, gap-analysis]
---

## Gap Resolution Log

| # | Gap | User Response | Date |
|---|-----|--------------|------|
| 1 | Step 4 approval criteria | "Director-level approval required for requests over $50K, manager for under" | YYYY-MM-DD |
| 2 | Step 7 actor | "The solution architect reviews, not the team lead" | YYYY-MM-DD |
```

### Step 3: Update process-steps.md

Incorporate user answers. Update confidence levels. Remove resolved gaps from the Known Gaps section.

### Step 4: Confirm completeness

Ask: "Are there any steps, decision points, or exceptions that we're still missing? Anything this process does in practice that isn't captured here?"

Iterate until the user confirms the process is sufficiently complete. Not every gap needs to be resolved — but the user should consciously accept any remaining unknowns.

---

## Phase 4: Visualization

### Step 1: Generate Mermaid flowchart

Convert the confirmed process-steps.md into a Mermaid flowchart.

**Rules:**
- Use `flowchart TD` (top-down) for most processes; `flowchart LR` (left-right) if very linear
- **Swimlane subgraphs** for each actor: `subgraph Actor_Name[Actor Name]`
- **Start/end:** Stadium-shaped nodes `([Start])` / `([End])`
- **Activities:** Rectangle nodes `[Activity description]`
- **Decisions:** Diamond nodes `{Decision question?}`
- **Color coding:**
  - `:::green` for HIGH confidence steps
  - `:::yellow` for MODERATE confidence
  - `:::red` for LOW confidence or unresolved gaps
- Keep node labels short (under 40 chars). Put detail in the process-steps table, not the diagram.

See `references/process-notation.md` for full Mermaid syntax guide.

### Step 2: Render

```bash
mmdc -i process-map.mmd -o process-map.svg -t neutral -b transparent
```

If the diagram is too dense or Mermaid struggles with layout (>20 steps), also generate a Graphviz DOT version:

```bash
dot -Tsvg process-map.dot -o process-map-graphviz.svg
```

### Step 3: Review with user

Show the rendered diagram. Ask: "Does this accurately represent the process flow? Any connections missing or wrong?"

---

## Phase 5: Automation Assessment

### Step 1: Score each step

Load `references/automation-rubric.md` for the full scoring criteria. Score each process step on four dimensions (1-5 scale):

| Dimension | 5 (most automatable) | 1 (least automatable) |
|-----------|---------------------|----------------------|
| **Structuredness** | Fully structured digital input, deterministic rules | Unstructured, requires interpretation |
| **Judgment** | No judgment, pure rule application | Significant professional judgment, context-dependent |
| **Volume/Frequency** | High-volume, daily or more | Rare, ad-hoc |
| **Error Consequence** | Low stakes, easily reversed | High stakes, irreversible, regulatory exposure |

### Step 2: Classify pathway

Based on the score profile, classify each step:

| Pathway | When |
|---------|------|
| **Full Automation** (RPA/script) | Structured 4-5, Judgment 4-5, Consequence 3-5 |
| **One-Shot LLM** | Structured 2-4, Judgment 2-4, Consequence 3-5. Single invocation, human reviews output |
| **Agentic AI** | Structured 2-4, Judgment 2-3, Volume 3-5, Consequence 3-5. Multi-step reasoning, tool use |
| **Human-in-the-Loop** | Judgment 1-2 OR Consequence 1-2. AI assists, human decides |
| **Human-Only** | Structured 1-2, Judgment 1, Consequence 1-2. Novel, relational, or ethical judgment |

### Step 3: Write automation-assessment.md

```markdown
---
title: "[Process Name] - Automation Assessment"
created: YYYY-MM-DD
last_modified: YYYY-MM-DD
tags: [process-map, automation-assessment]
---

## Assessment Summary

**Process:** [Name]
**Total steps:** X
**Automation candidates:** Y of X steps (Z%)

### Top 3 Opportunities

1. **Step N: [Activity]** — [Pathway]. [1-sentence rationale]. Estimated effort: [low/medium/high]
2. ...
3. ...

## Full Assessment

| Step | Activity | Structured | Judgment | Volume | Consequence | Pathway | Rationale |
|------|----------|-----------|----------|--------|-------------|---------|-----------|
| 1 | ... | 4 | 5 | 3 | 4 | Full Automation | Deterministic routing based on form fields |
| 2 | ... | 2 | 2 | 4 | 2 | Human-in-the-Loop | Requires professional review; regulatory implications |

## Next Steps

For each automation candidate, recommended action:
- [ ] **Step N** — Build [skill/agent/script]. Estimated scope: [description]
- [ ] **Step M** — Investigate further: [what needs to be understood before building]
```

### Step 4: Review with user

Present the assessment. Ask:
- "Do these scores feel right? Any step where the automation pathway surprises you?"
- "Which of the top opportunities would you want to build first?"

---

## Notes

**Where outputs go:** Process files go in the project directory, not vault-os. Ask the user if the location isn't obvious.

**Iteration:** The user can re-enter any phase. Common patterns:
- Re-run Phase 3 after observing the process in practice (new gaps discovered)
- Re-run Phase 5 after technology changes (new tools available)
- Add steps to process-steps.md as the process evolves

**Scope discipline:** If the user starts describing a different process during the interview, note it as a separate future mapping candidate. Don't expand scope mid-flow.

**What this skill does NOT do:** Execute the automation. It identifies and classifies opportunities. Building the actual agents, skills, or scripts is a separate step (use `/skill-creator` or `/agent-creator`).
