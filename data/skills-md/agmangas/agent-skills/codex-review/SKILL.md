---
name: codex-review
description: Review implementation plans or local code changes with OpenAI Codex CLI. Use when the user wants a second opinion on a plan before implementation, or to validate local un-pushed code changes after implementation.
---

# Codex Plan & Code Review

Send the current implementation plan or local code changes to OpenAI Codex for review.

Default behavior is review-only: Claude gathers Codex feedback and shows it to the user without changing the plan or code.

If the user explicitly asks for iterative refinement, or invokes `/codex-review --iterate`, Claude may revise the plan (or code) and re-submit it until Codex returns `VERDICT: APPROVED` or 5 rounds are reached.

---

## When to Invoke

- When the user runs `/codex-review` during or after plan mode
- When the user runs `/codex-review code` or asks to review local changes
- When the user wants a second opinion on a plan or code from a different model
- When the user wants optional iterative refinement before implementation or committing

## Arguments

- Optional target: `/codex-review plan` or `/codex-review code`
- Optional model override: `/codex-review o4-mini`
- Optional iterative mode: `/codex-review --iterate`
- All together: `/codex-review code --iterate o4-mini`

If `--iterate` is not present and the user did not explicitly ask for automatic refinement, use review-only mode.

## Agent Instructions

When invoked, perform the following workflow:

### Step 1: Determine Mode, Model, and Target

1. Set `MODE=review-only` by default.
2. Switch to `MODE=iterate` only if the user explicitly asked for automatic revision/re-review, or provided `--iterate`.
3. Use `gpt-5.4` by default.
4. If the user supplied a model override, use that model instead.
5. Determine `TARGET`: `plan` or `code`. Default to `plan` unless the user explicitly asks to review code/changes, or provides the `code` argument.

Example initialization:

```bash
MODE=review-only
MODEL=gpt-5.4
TARGET=plan
ROUND=1
```

### Step 2: Generate Session ID

Generate a unique ID to avoid conflicts with other concurrent Claude Code sessions:

```bash
REVIEW_ID=$(uuidgen | tr '[:upper:]' '[:lower:]' | head -c 8)
```

Use this for all temporary paths:

- `/tmp/claude-plan-${REVIEW_ID}.md`
- `/tmp/claude-diff-${REVIEW_ID}.diff`
- `/tmp/codex-review-${REVIEW_ID}-round-1.md`
- `/tmp/codex-review-${REVIEW_ID}-round-N.md`
- `/tmp/codex-launch-${REVIEW_ID}.log`
- `/tmp/codex-session-${REVIEW_ID}.txt`

### Step 3: Register Cleanup Early

Register cleanup before any Codex command so temporary files are removed on success, failure, or cancellation:

```bash
cleanup() {
  rm -f /tmp/claude-plan-${REVIEW_ID}.md \
        /tmp/claude-diff-${REVIEW_ID}.diff \
        /tmp/codex-review-${REVIEW_ID}-round-*.md \
        /tmp/codex-launch-${REVIEW_ID}.log \
        /tmp/codex-session-${REVIEW_ID}.txt
}
trap cleanup EXIT
```

### Step 4: Capture the Target Content

**If TARGET is `plan`:**
1. If the user included a plan in the current request, use that plan.
2. Otherwise use the latest complete implementation plan from the current conversation.
3. If there are multiple candidate plans, partial drafts, or stale plan-mode notes, summarize the candidate plan and ask the user to confirm before sending it to Codex.
4. If there is no plan in context, ask the user what they want reviewed.
5. Once the plan is identified, write the full plan content to `/tmp/claude-plan-${REVIEW_ID}.md`.

**If TARGET is `code`:**
1. Run `git diff HEAD` to capture all uncommitted changes. If the user explicitly wants to review un-pushed commits, run `git diff @{u}..HEAD`.
2. Save the output to `/tmp/claude-diff-${REVIEW_ID}.diff`.
3. If the diff is empty, inform the user there are no changes to review and stop.

### Step 5: Initial Review (Round 1)

Run Codex CLI in non-interactive mode and capture both the review body and the launch metadata.

**If TARGET is `plan`:**
```bash
codex exec \
  -m ${MODEL} \
  -s read-only \
  -o /tmp/codex-review-${REVIEW_ID}-round-1.md \
  "Review the implementation plan in /tmp/claude-plan-${REVIEW_ID}.md. Focus on:
1. Correctness - Will this plan achieve the stated goals?
2. Risks - What could go wrong? Edge cases? Data loss?
3. Missing steps - Is anything forgotten?
4. Alternatives - Is there a simpler or better approach?
5. Security - Any security concerns?

Be specific and actionable. If the plan is solid and ready to implement, end your review with exactly: VERDICT: APPROVED

If changes are needed, end with exactly: VERDICT: REVISE" \
  2>&1 | tee /tmp/codex-launch-${REVIEW_ID}.log
```

**If TARGET is `code`:**
```bash
codex exec \
  -m ${MODEL} \
  -s read-only \
  -o /tmp/codex-review-${REVIEW_ID}-round-1.md \
  "Review the code changes in /tmp/claude-diff-${REVIEW_ID}.diff. Act as a Senior Software Engineer reviewing a Pull Request. Focus on:
1. Bugs and Logic flaws
2. Security vulnerabilities
3. Performance issues
4. Unhandled edge cases
5. Adherence to best practices

Be specific and actionable. If the code is solid and ready to commit, end your review with exactly: VERDICT: APPROVED

If changes are needed, end with exactly: VERDICT: REVISE" \
  2>&1 | tee /tmp/codex-launch-${REVIEW_ID}.log
```

Immediately parse the launch log, extract the exact `session id: <uuid>` value, and persist it to `/tmp/codex-session-${REVIEW_ID}.txt`.

Example:

```bash
REVIEW_ID="${REVIEW_ID}" python - <<'PY'
import os
from pathlib import Path
import re

review_id = os.environ["REVIEW_ID"]
launch_log = Path(f"/tmp/codex-launch-{review_id}.log")
session_file = Path(f"/tmp/codex-session-{review_id}.txt")
match = re.search(r"session id:\s*([0-9a-fA-F-]+)", launch_log.read_text())
if not match:
    raise SystemExit("Could not determine Codex session ID")
session_file.write_text(match.group(1) + "\n")
PY
```

Do not use `--last`, which may resume the wrong session if multiple reviews are running concurrently.

**Notes:**
- Use `gpt-5.4` as the default model unless the user overrides it.
- Use `-s read-only` so Codex can inspect context but cannot modify anything.
- Always capture review output to a file and read from that file rather than relying on truncated terminal output.

### Step 6: Read Review and Check Verdict

1. Read `/tmp/codex-review-${REVIEW_ID}-round-1.md`.
2. Present Codex's review to the user:

```
## Codex Review - Round N (model: [selected model], target: [plan/code])

[Codex's feedback here]
```

3. Check the verdict:
   - If **VERDICT: APPROVED** and `MODE=review-only` → go to Step 7
   - If **VERDICT: APPROVED** and `MODE=iterate` → go to Step 10
   - If **VERDICT: REVISE** and `MODE=iterate` → go to Step 8 (Revise and Re-submit)
   - If **VERDICT: REVISE** and `MODE=review-only` → stop after presenting the feedback
   - If there is no explicit verdict → treat the result as unresolved, not approved
   - If the output is incomplete, ambiguous, or truncated → report that to the user and stop or retry explicitly
   - If `MODE=iterate` and max rounds (5) are reached → go to Step 10 with a note that max rounds were reached

Approval must be explicit. Never infer approval from a generally positive tone.

### Step 7: Stop in Review-Only Mode

If `MODE=review-only`, end after round 1 with a concise summary:

```
## Codex Review - Final (model: [selected model])

**Status:** Review completed. No automatic changes were made.

[Short summary of Codex's main concerns or approval]
```

If Codex returned `VERDICT: APPROVED`, say so explicitly.
If Codex returned `VERDICT: REVISE`, say the plan/code was reviewed but not approved.
If the result was unresolved, say the verdict was unclear and manual follow-up is needed.

### Step 8: Revise the Plan/Code in Iterative Mode

If `MODE=iterate` and Codex returned `VERDICT: REVISE`, revise the target based on the feedback:

1. Address each actionable issue Codex raised.
2. Preserve the user's explicit requirements and constraints.
3. If a suggested change conflicts with the user's requirements, skip it and note that explicitly.
4. **If TARGET is `plan`:** Rewrite `/tmp/claude-plan-${REVIEW_ID}.md` with the revised plan.
5. **If TARGET is `code`:** Apply the fixes to the actual codebase files, then re-run `git diff HEAD > /tmp/claude-diff-${REVIEW_ID}.diff` to capture the updated state.
6. Briefly summarize what changed for the user:

```
### Revisions (Round N)
- [What was changed and why, one bullet per Codex issue addressed]
```

7. Inform the user that the revised plan/code is being sent back to Codex for re-review.

### Step 9: Re-submit to Codex (Rounds 2-5)

Resume the existing Codex session so it has full context of the prior review:

```bash
CODEX_SESSION_ID=$(REVIEW_ID="${REVIEW_ID}" python - <<'PY'
import os
from pathlib import Path
review_id = os.environ["REVIEW_ID"]
print(Path(f"/tmp/codex-session-{review_id}.txt").read_text().strip())
PY
)
```

**If TARGET is `plan`:**
```bash
codex exec resume ${CODEX_SESSION_ID} \
  "I've revised the plan based on your feedback. The updated plan is in /tmp/claude-plan-${REVIEW_ID}.md.

Here's what I changed:
[List the specific changes made]

Please re-review. If the plan is now solid and ready to implement, end with: VERDICT: APPROVED
If more changes are needed, end with: VERDICT: REVISE" \
  > /tmp/codex-review-${REVIEW_ID}-round-${ROUND}.md 2>&1
```

**If TARGET is `code`:**
```bash
codex exec resume ${CODEX_SESSION_ID} \
  "I've revised the code based on your feedback. The updated diff is in /tmp/claude-diff-${REVIEW_ID}.diff.

Here's what I changed:
[List the specific changes made]

Please re-review. If the code is now solid and ready to commit, end with: VERDICT: APPROVED
If more changes are needed, end with: VERDICT: REVISE" \
  > /tmp/codex-review-${REVIEW_ID}-round-${ROUND}.md 2>&1
```

Read the full round file `/tmp/codex-review-${REVIEW_ID}-round-${ROUND}.md` and then return to Step 6.

Do not pipe through `tail` or otherwise truncate the response. The verdict line must remain visible in the captured file.

If `resume ${CODEX_SESSION_ID}` fails, tell the user and either:

- stop with the latest available feedback, or
- fall back to a fresh `codex exec` that includes the latest revised plan/diff plus a concise summary of prior concerns

Do not silently continue without telling the user that session continuity was lost.

### Step 10: Present Final Result

Once approved (or max rounds reached):

```
## Codex Review - Final (model: [selected model], target: [plan/code])

**Status:** ✅ Approved after N round(s)

[Final Codex feedback / approval message]

---
**The [plan/code] has been reviewed and approved by Codex. Ready for your approval to [implement/commit].**
```

If max rounds were reached without approval:

```
## Codex Review - Final (model: [selected model], target: [plan/code])

**Status:** ⚠️ Max rounds (5) reached — not fully approved

**Remaining concerns:**
[List unresolved issues from last review]

---
**Codex still has concerns. Review the remaining items and decide whether to proceed or continue refining.**
```

## Loop Summary

```
Review-only:
Round 1: Claude sends plan/code -> Codex reviews -> Claude reports verdict and feedback

Iterative:
Round 1: Claude sends plan/code -> Codex reviews -> REVISE?
Round 2: Claude revises -> Codex re-reviews (resume session) -> REVISE?
Round 3: Claude revises -> Codex re-reviews (resume session) -> APPROVED
```

Max 5 rounds in iterative mode. Each round preserves Codex's conversation context via the stored session ID when resume succeeds.

## Rules

- Default to review-only mode unless the user explicitly asked for automatic refinement
- Default target is `plan` unless the user specifies `code` or asks to review changes
- Approval requires an explicit `VERDICT: APPROVED`
- `VERDICT: REVISE` means the plan/code is not approved yet
- No explicit verdict means unresolved, not approved
- Claude actively revises the plan/code only in iterative mode
- Default model is `gpt-5.4`. Accept model override from the user's arguments (e.g., `/codex-review o4-mini`)
- Always use read-only sandbox mode — Codex should never write files
- Max 5 review rounds to prevent infinite loops
- Show the user each round's feedback and revisions so they can follow along
- Persist the Codex session ID to a temp file immediately after round 1
- Read review output from files; never depend on truncated terminal output for verdict detection
- If session resume fails or output is ambiguous, tell the user instead of guessing
- If Codex CLI is not installed or fails, inform the user and suggest `npm install -g @openai/codex`
- If a revision contradicts the user's explicit requirements, skip that revision and note it for the user