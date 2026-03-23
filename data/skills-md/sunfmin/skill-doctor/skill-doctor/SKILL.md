---
name: skill-doctor
description: >
  Diagnose and fix skills by analyzing session logs for friction events — user interruptions, rejected actions,
  wrong approaches, test failures, and manual corrections. Cross-references friction against the patient skill's
  SKILL.md to find missing rules or enforcement gaps, generates patches with regression tests, and submits a PR.
  Use this skill after any development session where a skill underperformed, when you want to audit a skill's
  effectiveness, when debugging why a skill keeps making the same mistakes, or when the user says things like
  "fix this skill", "why does it keep doing X", "audit the skill", "doctor", or "skill-doctor".
---

# Skill Doctor

A post-session diagnostic tool that analyzes Claude Code session logs to find friction events, diagnoses which
skill rules are missing or insufficient, generates concrete patches, and submits a PR to the patient skill's repo.

## Overview

The Skill Doctor operates on a **patient** — the skill that was active during a session that had problems. It
reads the raw JSONL session logs, extracts every moment where something went wrong, traces each friction event
back to a gap in the patient skill's instructions, and proposes a fix.

## When to use

- After a development session where a skill caused friction (wrong approach, user had to correct, tests failed)
- When the user notices a recurring pattern across multiple sessions
- When auditing a skill's effectiveness before publishing
- When the user invokes `/skill-doctor`

## Workflow

The skill-doctor workflow has 6 phases. Execute them in order. Do NOT skip the approval step (Phase 6).

---

### Phase 1: Parse Session Logs

Find and parse the latest JSONL session logs to extract friction events.

**How to find the right logs:**

1. Ask the user which skill is the "patient" (or infer from context)
2. Identify the project directory — session logs live in `~/.claude/projects/<project-path>/`
3. Find the most recent `.jsonl` files (by modification time) that are NOT in `subagents/`
4. Also parse subagent logs in `subagents/` — friction often happens in delegated work

**Run the parser:**

```bash
python3 SKILL_DIR/scripts/parse_session.py <session-jsonl-path> --output /tmp/skill-doctor-workspace/friction_events.json
```

If there are multiple session files to analyze (e.g., the user wants to look across sessions), run the parser
on each and combine the results:

```bash
python3 SKILL_DIR/scripts/parse_session.py <path1> <path2> ... --output /tmp/skill-doctor-workspace/friction_events.json
```

The parser extracts these friction signals from the JSONL:

| Signal | How it appears in logs |
|--------|----------------------|
| **User rejection** | `tool_result` with `is_error: true` + "rejected" or "doesn't want to proceed" |
| **User interruption** | `user` message with `[Request interrupted by user]` prefix |
| **User correction** | `user` message containing corrective language after an assistant action |
| **Test failure** | `tool_result` from Bash with exit code != 0, containing test/assertion failure patterns |
| **Wrong approach** | User says "no", "not that", "wrong", "instead" etc. after assistant took an action |
| **Repeated attempt** | Same tool called 3+ times on similar input (retry loop) |
| **Scope creep** | Assistant actions on files/areas the user didn't ask about, followed by correction |

**Output:** A JSON file with an array of friction events, each containing:
- `id`: Sequential identifier
- `type`: The friction signal type
- `line_number`: Position in the JSONL
- `timestamp`: When it occurred
- `context_before`: The 3 messages leading up to the friction
- `context_after`: The 2 messages after (showing how it was resolved)
- `tool_name`: Which tool was involved (if applicable)
- `user_message`: The user's corrective message (if applicable)
- `assistant_action`: What the assistant was trying to do

---

### Phase 2: Categorize Friction Events

Each friction event gets assigned a **root cause category**. Read `references/friction_taxonomy.md` for the
full taxonomy.

```bash
python3 SKILL_DIR/scripts/categorize.py /tmp/skill-doctor-workspace/friction_events.json --output /tmp/skill-doctor-workspace/categorized.json
```

The categorizer uses the context around each event to determine the root cause. It outputs the same events
with an added `category` and `explanation` field.

However, the automated categorizer is a first pass. After running it, **review the results yourself** and
refine any miscategorized events. The categories are:

| Category | Description | Example |
|----------|-------------|---------|
| `missing-rule` | Skill has no instruction covering this situation | Skill doesn't say how to handle monorepos |
| `insufficient-rule` | Rule exists but is too vague or weak | "Consider testing" vs "Always run tests before committing" |
| `wrong-scope` | Agent acted outside the requested scope | Fixed unrelated code while working on a bug |
| `skipped-step` | Agent skipped a required workflow step | Didn't run linter before committing |
| `wrong-approach` | Agent chose a suboptimal strategy | Used mocks when skill says use real DB |
| `missing-context` | Agent lacked project-specific knowledge | Didn't know about custom test runner |
| `premature-action` | Agent acted before gathering enough info | Started coding before reading existing code |
| `config-gap` | Missing configuration or environment setup | Didn't set required env vars |
| `communication-gap` | Agent didn't explain what it was doing | Made large changes without summarizing |
| `repetition` | Agent repeated a previously-corrected mistake | Same wrong approach in multiple sessions |

---

### Phase 3: Cross-Reference Against Patient Skill

Now read the patient skill's SKILL.md and any referenced files to find which rules are missing or insufficient.

```bash
python3 SKILL_DIR/scripts/cross_reference.py \
  /tmp/skill-doctor-workspace/categorized.json \
  <path-to-patient-skill/SKILL.md> \
  --output /tmp/skill-doctor-workspace/gaps.json
```

For each friction event, the cross-referencer:
1. Searches the patient SKILL.md for any existing rule that should have prevented this friction
2. If found: marks the rule as `insufficient` with a note on why it failed
3. If not found: marks it as `missing` with a suggested location in the SKILL.md

The output is a JSON array of gap objects:
- `friction_event_id`: Links back to the friction event
- `gap_type`: `missing` or `insufficient`
- `existing_rule`: The current rule text (if insufficient) or null
- `existing_location`: Line number / section in SKILL.md
- `suggested_fix`: Natural language description of what to add/change
- `occurrence_count`: How many times this pattern appeared across all analyzed sessions
- `severity`: `high` (>2 occurrences or user was frustrated), `medium` (2 occurrences), `low` (1 occurrence)

**Prioritize by occurrence count.** Patterns that appear multiple times are the most important to fix.

---

### Phase 4: Generate Patches

For each identified gap, generate a concrete diff that would prevent the friction.

```bash
python3 SKILL_DIR/scripts/generate_patches.py \
  /tmp/skill-doctor-workspace/gaps.json \
  <path-to-patient-skill/SKILL.md> \
  --output /tmp/skill-doctor-workspace/patches/
```

This creates individual `.patch` files in the output directory. Each patch:
- Targets a specific file in the patient skill (usually SKILL.md, but could be reference files or scripts)
- Includes a comment block explaining what friction it prevents
- Uses minimal, surgical changes — don't rewrite sections that are working fine
- Groups related gaps into a single patch when they affect the same section

**Patch format guidelines:**
- New rules should explain the **why**, not just the **what** — following the skill-creator's philosophy
- Avoid heavy-handed MUST/NEVER unless truly critical
- Prefer explaining reasoning so the model understands when to apply the rule
- Keep additions concise — a good rule is 1-3 sentences

---

### Phase 5: Generate Regression Tests

For each patch, create a test case that verifies the fix works.

```bash
python3 SKILL_DIR/scripts/generate_tests.py \
  /tmp/skill-doctor-workspace/gaps.json \
  /tmp/skill-doctor-workspace/patches/ \
  --output /tmp/skill-doctor-workspace/regression_tests.json
```

Each regression test contains:
- `test_id`: Matches the gap/patch it validates
- `prompt`: A realistic user prompt that would trigger the friction if the fix isn't applied
- `expected_behavior`: What the agent should do with the fix in place
- `anti_pattern`: What the agent used to do (the friction behavior)
- `assertion`: A verifiable check (e.g., "agent should read file X before editing it")

These tests are formatted to be compatible with the skill-creator's `evals/evals.json` schema, so they can
be added to the patient skill's test suite.

---

### Phase 6: Present Summary and Get Approval

**This step is mandatory. Do NOT apply patches without user approval.**

Present a summary table to the user:

```
## Skill Doctor Report: <patient-skill-name>
Analyzed: <N> session(s), <M> friction events found

| # | Friction Pattern | Occurrences | Category | Root Cause | Proposed Fix | Severity |
|---|-----------------|-------------|----------|------------|--------------|----------|
| 1 | User rejected file edit in monorepo | 3 | missing-rule | No guidance on monorepo structure | Add monorepo navigation rules | high |
| 2 | Tests failed due to missing env var | 2 | config-gap | No env setup step in workflow | Add env validation step | medium |
| ... | | | | | | |

### Patches to apply:
1. **SKILL.md** — Add monorepo navigation rules (prevents: user rejection when editing wrong package)
2. **SKILL.md** — Add env validation step (prevents: test failures from missing config)
3. **references/setup.md** — New file with environment checklist

### Regression tests to add: <N>

Apply all patches? [approve all / select specific / reject]
```

Wait for the user's response. They may:
- Approve all patches
- Select specific patches to apply
- Ask for modifications to specific patches
- Reject and ask for a different approach

---

### Phase 7: Apply and Submit PR

After approval:

1. **Locate the patient skill's source repo:**
   ```bash
   python3 SKILL_DIR/scripts/find_skill_repo.py <patient-skill-name> --json
   ```
   This checks `~/.agents/.skill-lock.json` first (which tracks source repos for all installed skills),
   then falls back to scanning the skill's README.md. If neither works, ask the user for the GitHub URL.

2. **Clone and branch:**
   ```bash
   # Clone the patient skill's repo to a temp directory
   gh repo fork <owner/repo> --clone --remote 2>/dev/null || git clone <repo-url> /tmp/skill-doctor-workspace/patient-repo
   cd /tmp/skill-doctor-workspace/patient-repo
   git checkout -b skill-doctor/fix-friction-$(date +%Y%m%d)
   ```

3. **Apply patches:**
   - Apply each approved patch to the cloned repo
   - Add regression tests to the skill's test suite (create `evals/` dir if needed)

4. **Commit and push:**
   ```bash
   git add -A
   git commit -m "fix: address friction patterns found by skill-doctor

   Analyzed N session(s), found M friction events.
   Key fixes:
   - <summary of each patch>

   Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
   git push -u origin HEAD
   ```

5. **Create PR:**
   ```bash
   gh pr create --title "fix: address N friction patterns from session analysis" --body "$(cat <<'EOF'
   ## Skill Doctor Report

   Analyzed session logs and found friction patterns that can be prevented with skill improvements.

   ### Friction → Fix Summary
   <table from Phase 6>

   ### Regression Tests Added
   <list of new test cases>

   ### How these were found
   Each fix traces back to a real friction event in session logs — a user interruption,
   rejected action, test failure, or manual correction. Patterns that occurred multiple
   times across sessions were prioritized.

   🩺 Generated by [skill-doctor](https://github.com/theplant/skill-doctor)
   EOF
   )"
   ```

6. **Report the PR URL to the user.**

---

## Important Notes

- **Privacy:** Session logs may contain sensitive information. The parser only extracts friction-relevant
  context (tool names, error messages, corrective user messages). It does NOT extract full conversation
  content, file contents, or credentials.
- **Multi-session analysis:** When the user asks to look at patterns across sessions, parse multiple JSONL
  files and aggregate. The cross-referencer will count occurrences across sessions and prioritize accordingly.
- **Subagent logs:** Always include subagent logs in the analysis — friction in delegated work is often the
  most impactful to fix because it affects autonomous operation.
- **Conservative patching:** When in doubt, make the patch smaller. It's better to add one precise rule than
  to rewrite a whole section. The user can always run skill-doctor again.
