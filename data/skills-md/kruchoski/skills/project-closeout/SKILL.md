---
name: project-closeout
description: Lightweight project archival process. Captures final state, lessons forward, archives project state files, cleans up task management, and cross-references deliverables. Complements lessons-learned (which handles incidents/failures) by covering routine successful completions.
use_when: A project is complete or being shelved. Triggers on "close out project", "archive project", "project is done", "project closeout", "wrap up project".
effort: normal
---

# Project Close-Out

Archive completed projects with a consistent, lightweight process. Captures what matters, cleans up what doesn't, and leaves a clear trail for future reference.

## When to Use

- Project deliverables are complete and accepted
- Project is being shelved (paused indefinitely or deprioritized)
- Engagement/contract has ended
- You're cleaning up old projects during a periodic review

**Not for:** Incidents or failures (use `/lessons-learned` instead).

## Process Overview

Seven steps, 5-10 minutes. Claude walks through interactively.

```
1. Identify scope       → What project? Where are its artifacts?
2. Capture final state  → Update README with outcome summary
3. Lessons forward      → What worked, what to repeat, what to skip next time
4. Archive WM           → Move Working Memory to Archived/
5. Task management      → Close project, disposition remaining tasks
6. Cross-reference      → Final PROJECT-LOG entry, link to archived WM
7. Mark archived        → Update frontmatter status across project files
```

---

## Step-by-Step

### Step 1: Identify Scope

Confirm the project's footprint before touching anything.

**Ask/verify:**
- Project folder path (e.g., `./projects/DAF-EITRM/`)
- Project state file (e.g., a Working Memory or active context file) — may not exist
- Task management project (if configured) — may not exist
- Key deliverable locations (vault, external repos, client systems)

### Step 2: Capture Final State

Update the project's `README.md` with a completion block:

```markdown
## Project Outcome

**Status:** Completed | Shelved | Transferred
**Closed:** YYYY-MM-DD
**Outcome:** [1-2 sentence summary of what was delivered/achieved]
**Key Deliverables:**
- [Deliverable 1] — [location or link]
- [Deliverable 2] — [location or link]
```

If the project has no README, create a minimal one with this block.

### Step 3: Lessons Forward

This is the proactive complement to `/lessons-learned`. Not "what went wrong" but "what's worth remembering."

**Ask three questions:**

1. **What worked well?** — Approaches, tools, patterns, or collaborations worth repeating
2. **What would you do differently?** — Not failures, just refinements for next time
3. **Any reusable patterns?** — Frameworks, templates, or processes that could become skills or reference docs

Capture responses in the archived Working Memory file (Step 4) under a "Lessons Forward" section. Keep it brief — 3-5 bullets total is ideal.

**If lessons suggest systemic changes:** Encode them in the appropriate location per the lessons-learned integration table:

| Fix Type | Destination |
|----------|-------------|
| Claude behavior change | Project configuration update |
| Recurring task adjustment | Task management system notes |
| Workflow improvement | Skill creation/update |
| Knowledge gap | Reference doc |
| Tool configuration | Relevant config file |

### Step 4: Archive Working Memory

If a Working Memory file exists:

1. Add a `## Final Outcome` section before the Archive Notes:
   ```markdown
   ## Final Outcome
   **Closed:** YYYY-MM-DD
   **Outcome:** [Same summary from README]
   **Lessons Forward:**
   - [From Step 3]
   - [From Step 3]
   **Deliverables:** [Links to key outputs]
   ```

2. Update frontmatter: `status: archived`

3. Move file:
   ```
   From: [your project state file location]
   To:   [your archive directory]/Working Memory - [Project] - YYYY-MM-DD.md
   ```

If no Working Memory file exists, skip this step.

### Step 5: Task Management Cleanup

If a task management project exists (e.g., in Asana, Linear, or similar):

1. **Review open tasks** — For each:
   - Complete if actually done
   - Move to a backlog/future project if still relevant
   - Close with a note if no longer applicable
2. **Mark project complete** (or archive it)
3. **Note:** Don't bulk-close without reviewing. Tasks may contain context worth preserving.

If no task management project exists, skip this step.

### Step 6: Cross-Reference

Add a final entry to `PROJECT-LOG.md`:

```markdown
### YYYY-MM-DD - Project Closed
- **Status:** Completed | Shelved | Transferred
- **Outcome:** [Brief summary]
- **Archived WM:** [Link to archived WM file, if applicable]
- **Lessons Forward:** [1-2 key takeaways, or "see archived WM"]
```

### Step 7: Mark Archived & Move Folder

Update frontmatter `status: archived` on:
- Project README.md
- PROJECT-LOG.md
- Any other active project files that have frontmatter

**Move the project folder** (non-repo projects only):
```
From: ./projects/[project-name]/
To:   ./projects/_archived/[project-name]/
```

**Git repo projects** (have their own `.git/` or remote tracking) stay in `./projects/` — moving them would break remote tracking. They rely on `status: archived` in frontmatter to indicate completion.

---

## Output Checklist

Before declaring close-out complete, verify:

- [ ] README.md has outcome summary and deliverable links
- [ ] Lessons forward captured (even if brief)
- [ ] Project state file archived (if it existed)
- [ ] Task management project closed/archived (if it existed)
- [ ] PROJECT-LOG has final closure entry
- [ ] Frontmatter status updated to `archived`
- [ ] Project folder moved to `./projects/_archived/` (non-repo projects only)
- [ ] Log close-out to today's daily note via `log-to-daily`

---

## Quick Mode

For small projects without a project state file or task management presence, collapse to four steps:

1. Update README with outcome summary
2. Add closure entry to PROJECT-LOG
3. Update frontmatter to `archived`
4. Move folder to `./projects/_archived/` (non-repo projects only)

---

## Invocation

**Manual:** `/project-closeout` or "close out [project name]" or "archive [project name]"

**Automatic triggers:**
- "project is done", "wrap up project", "we're finished with"
- "archive project", "close out project", "shelve project"
- During weekly review when identifying completed projects
