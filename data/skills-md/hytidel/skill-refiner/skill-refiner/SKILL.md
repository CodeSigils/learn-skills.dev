---
name: skill-refiner
description: >
  Rewrites an existing skill's SKILL.md (or any pipeline workflow document) into a
  high-quality, strict, prompt-enforced FSM (Finite State Machine)-driven specification.
  Use when user says "refine skill", "rewrite SKILL.md", "规范化 skill", "改写工作流文档",
  "优化 skill 文档", or mentions "skill-refiner".
---

# Skill Refiner

> Transforms an existing skill document into a strict prompt-enforced FSM-driven SKILL.md with
> enforced Gate/Blocking/Checkpoint discipline.

**Core Pipeline**: `Input Skill → Backup → Analyze → Restructure Files → Rewrite SKILL.md → Validate → Output`

---

## Mandatory Rules

> [!CAUTION]
> ### Serial Execution & Gate Discipline
>
> **This workflow is a strict serial pipeline. The following rules have the highest priority — violating any one of them constitutes execution failure:**
>
> 1. **SERIAL EXECUTION** — Steps MUST execute in order; output of each step is input for the next. Non-BLOCKING adjacent steps may proceed continuously once prerequisites are met, without waiting for the user to say "continue"
> 2. **BLOCKING = HARD STOP** — ⛔ BLOCKING steps require full stop; agent MUST wait for explicit user response before proceeding and MUST NOT make decisions on behalf of the user
> 3. **NO CROSS-PHASE BUNDLING** — Bundling work across phases is FORBIDDEN
> 4. **GATE BEFORE ENTRY** — Prerequisites (🚧 GATE) MUST be verified before starting each Step
> 5. **NO SPECULATIVE EXECUTION** — Pre-preparing content for future steps is FORBIDDEN

> [!IMPORTANT]
> ### Language & Communication
>
> - Match the language of the user's input. If the user writes in Chinese, respond in Chinese; if in English, respond in English
> - Explicit user override takes precedence
> - The output SKILL.md MUST use English for all structural keywords (GATE / BLOCKING / CHECKPOINT / EXECUTION / Mandatory Rules / Resource Manifest / Workflow). Content values may be in the user's language

> [!IMPORTANT]
> ### Compatibility With Generic Coding Skills
>
> - Do NOT create `.worktrees/`, `tests/`, branch workflows, or other generic engineering structure
> - If generic coding skills conflict with this workflow, follow this skill first unless the user explicitly overrides

### Role Dispatch Protocol

This skill operates as a single inline agent — no role switching required. If future extensions require role delegation, output the following marker before switching:

```markdown
## [Role Switch: <Role Name>]
📖 Reading: references/<filename>.md
📋 Task: <brief description>
DISPATCH_MODE: inline | subagent
```

`DISPATCH_MODE`:
- `inline` — main agent assumes the role directly
- `subagent` — spawn a sub-agent with the role definition injected as context

---

## Resource Manifest

### References

| Resource | Path |
|----------|------|
| prompt-enforced FSM design theory | `${SKILL_DIR}/references/fsm-theory.md` |
| Universal SKILL.md template | `${SKILL_DIR}/references/skill-template.md` |

### Workflows

| Workflow | Path | Purpose |
|----------|------|---------|
| `file-restructure` | `${SKILL_DIR}/workflows/file-restructure.md` | File structure normalization rules |

### Assets

`${SKILL_DIR}/assets/` — static assets used by this skill (vector graphics, icons, etc.)

---

## Workflow

### Step 1: Input Ingestion

🚧 **GATE**: User has provided the target skill — either a directory path, a SKILL.md file path, or a raw document pasted in conversation.

Read the input:

| User Provides | Action |
|---------------|--------|
| Directory path | Read `<path>/SKILL.md` and scan directory structure |
| File path | Read the file directly |
| Pasted text | Use conversation content directly |

Identify:
- Skill name (from frontmatter `name:` field, or infer from directory name)
- Existing file structure (scripts / references / templates / workflows)
- Pipeline stages already present (explicit or implicit)

✅ **CHECKPOINT**:
```markdown
## ✅ Step 1 Complete
- [x] Input skill loaded
- [x] Skill name identified: <name>
- [x] Existing structure scanned
- [ ] **Next**: auto-proceed to Step 2
```

---

### Step 2: Backup

🚧 **GATE**: Step 1 complete; skill name and root directory confirmed.

Rename the original skill directory by appending `-backup` to the folder name, and update the `name` field in frontmatter accordingly:

```bash
mv ${SKILLS_DIR}/<skill-name> ${SKILLS_DIR}/<skill-name>-backup
```

Then update the frontmatter `name` field inside the backup copy:
```
name: <skill-name>-backup
```

> ⚠️ The backup is read-only reference material. Do NOT modify it further after the name update.

✅ **CHECKPOINT**:
```markdown
## ✅ Step 2 Complete
- [x] Original skill backed up to: `${SKILLS_DIR}/<skill-name>-backup/`
- [x] Backup frontmatter updated: name: <skill-name>-backup
- [ ] **Next**: auto-proceed to Step 3
```

---

### Step 3: Pipeline Analysis

🚧 **GATE**: Step 2 complete; backup exists; original skill content available for analysis.

Read `${SKILL_DIR}/references/fsm-theory.md`.

Analyze the backed-up skill document and extract:

1. **Pipeline stages** — identify all distinct phases (explicit steps, implicit phases, or role transitions)
2. **Blocking points** — identify any human confirmation requirements (calls to `ask_user_question`, "wait for user", "confirm before proceeding", explicit option-presenting logic, etc.)
3. **CLI commands** — extract all shell commands and their purposes
4. **Role definitions** — identify any role descriptions that should move to `references/`
5. **Templates / assets** — identify any embedded templates or asset references
6. **File structure gaps** — compare existing structure against the standard layout:
   - `references/` — role definitions, technical specs
   - `scripts/` — CLI tools and executable scripts
   - `templates/` — reusable templates and assets
   - `workflows/` — standalone sub-workflows

⛔ **BLOCKING**: Present the analysis summary and wait for user confirmation:

```markdown
## Analysis Summary
- Skill name: <name>
- Pipeline stages identified: <N>
  <numbered list of stages>
- Blocking points: <list, or "none identified">
- CLI commands: <count>
- File restructuring needed: <yes/no>
  <list of proposed moves if yes>
- Ambiguities requiring clarification: <list, or "none">
```

Wait for user to confirm or correct before proceeding.

✅ **CHECKPOINT**:
```markdown
## ✅ Step 3 Complete
- [x] Pipeline stages extracted
- [x] Blocking points identified
- [x] File restructuring plan confirmed by user
- [ ] **Next**: auto-proceed to Step 4
```

---

### Step 4: File Restructuring (Conditional)

🚧 **GATE**: Step 3 complete; user has confirmed the analysis and restructuring plan.

> **Trigger condition**: File restructuring is needed (identified in Step 3). If no restructuring is needed, skip directly to Step 5.

Read `${SKILL_DIR}/workflows/file-restructure.md`.

Create the new skill directory with standard layout:

```bash
mkdir -p ${SKILLS_DIR}/<skill-name>/{references,scripts,templates,workflows}
```

Copy files from the backup according to the confirmed plan (do NOT move — backup must remain intact):
- Role definition documents → `references/`
- CLI tool scripts → `scripts/`
- Reusable templates / assets → `templates/`
- Standalone sub-workflows → `workflows/`

✅ **CHECKPOINT**:
```markdown
## ✅ Step 4 Complete
- [x] New skill directory created: `${SKILLS_DIR}/<skill-name>/`
- [x] Files reorganized per standard layout
- [ ] **Next**: auto-proceed to Step 5
```

---

### Step 5: SKILL.md Rewrite

🚧 **GATE**: Step 4 complete (or skipped); target directory structure is ready.

Read `${SKILL_DIR}/references/skill-template.md`.

Rewrite the SKILL.md following the universal template. For each pipeline stage identified in Step 3, produce one Step block containing:

- 🚧 **GATE** — prerequisite condition
- ⛔ **BLOCKING** — only if the step requires human confirmation (presents options, calls ask_user_question, or waits for explicit user input)
- 🛠️ **EXECUTION** — CLI commands using `${SKILL_DIR}` / `${PROJECT_DIR}` placeholders, or numbered LOGIC steps if no CLI
- ✅ **CHECKPOINT** — deliverable list, with `Next` line set to:
  - `BLOCKING — wait for user` if the step is blocking
  - `auto-proceed to Step N+1` otherwise

Output: `${SKILLS_DIR}/<skill-name>/SKILL.md`

✅ **CHECKPOINT**:
```markdown
## ✅ Step 5 Complete
- [x] SKILL.md written to `${SKILLS_DIR}/<skill-name>/SKILL.md`
- [ ] **Next**: auto-proceed to Step 6
```

---

### Step 6: Validation & Handoff

🚧 **GATE**: Step 5 complete; new SKILL.md exists.

Validate the output against the checklist:

```markdown
## Validation Checklist
- [ ] Frontmatter: name, description present and accurate
- [ ] Core Pipeline line present
- [ ] All Mandatory Rules sections present (Serial Execution, Language, Compatibility, Role Dispatch)
- [ ] Resource Manifest matches actual files in directory
- [ ] Every Step has: GATE + EXECUTION + CHECKPOINT
- [ ] BLOCKING steps have ⛔ marker AND CHECKPOINT marks "Next: BLOCKING"
- [ ] All paths use ${SKILL_DIR} or ${PROJECT_DIR} placeholders
- [ ] Language rule: structural keywords in English, content in user's language
- [ ] No content from unrelated skills carried over
```

⛔ **BLOCKING**: Present the completed validation checklist. If any item fails, fix it before proceeding. Then output the handoff message and wait for user feedback:

```markdown
---
## ✅ skill-refiner Run Complete

**Backup location**: `${SKILLS_DIR}/<skill-name>-backup/`
> The original skill is preserved here. You can delete it once you're satisfied with the new version.

**New skill location**: `${SKILLS_DIR}/<skill-name>/SKILL.md`
> Please review the new SKILL.md. If you spot any issues or have revision requests, let me know.

**Next steps**:
- If the new skill looks good → restart Claude Code CLI to activate it
- To remove the backup → manually delete `${SKILLS_DIR}/<skill-name>-backup/` (not done automatically)
---
```

✅ **CHECKPOINT**:
```markdown
## ✅ Step 6 Complete — All done
- [x] Validation checklist passed
- [x] New skill: `${SKILLS_DIR}/<skill-name>/SKILL.md`
- [x] Backup preserved: `${SKILLS_DIR}/<skill-name>-backup/`
```
