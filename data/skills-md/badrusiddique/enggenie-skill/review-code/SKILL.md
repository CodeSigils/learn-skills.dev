---
name: review-code
description: Use when requesting or receiving code review - dispatches reviewer subagent or processes human PR feedback with technical evaluation
---

# review-code

## Overview

Handle both sides of code review: requesting it (dispatching a reviewer subagent) and receiving it (processing feedback from humans or external reviewers). In both cases, the standard is technical evaluation, not emotional performance. Fix what is wrong. Push back on what is not. Skip the theater.

## Announcement

When this skill activates, announce:

> I'm using enggenie:review-code to [request a review / process review feedback].

Pick the correct variant based on the trigger.

---

## Jira Ticket Entry

When the user references a Jira ticket for review (e.g., "Review PROJ-1234", "Check the PR for PROJ-1234"):

1. Read the Jira ticket using MCP tools
2. Find the "Dev Handoff" comment — extract the PR link, what was built, spec deviations, and known limitations
3. Find the spec link — understand what was supposed to be built so you can review against requirements, not just code quality
4. Open the PR from the Dev Handoff and use it as the review target

This gives the reviewer full context: what was specified (PM), what was planned (Architect), and what was built (Dev). Review against all three, not just the diff.

If Jira MCP is not available, ask: "I can't read PROJ-1234 directly. Can you share the PR link and spec?"

---

## Entry Condition

This skill activates when:

1. A dev-implement task completes and needs review (automatic in subagent flow)
2. Human PR review feedback is received
3. User explicitly requests a code review
4. User references a Jira ticket for review

---

## Mode A: Requesting Review

When you need a review of completed work, dispatch a Code Reviewer subagent.

### Step 1 -- Get Git SHAs

```bash
BASE_SHA=$(git merge-base HEAD main)
HEAD_SHA=$(git rev-parse HEAD)
```

Use the actual base branch if it is not `main`. The diff between these two SHAs is what gets reviewed.

### Step 2 -- Dispatch Code Reviewer Subagent

Provide the subagent with:

1. **The diff** -- `git diff $BASE_SHA $HEAD_SHA`
2. **The spec/requirements** -- inline the full task description or ticket. Do not pass a file reference.
3. **Review checklist:**
   - Does the implementation match the spec?
   - Is anything specified but missing?
   - Is anything present but not specified? (scope creep)
   - Are edge cases handled?
   - Clean code: readable, well-named, no dead code
   - No bugs: null checks, error handling, boundary conditions
   - Good tests: meaningful assertions, edge cases, no testing implementation details
   - YAGNI: nothing built that was not asked for

The reviewer follows the prompt template at `agents/code-reviewer-agent.md`.

### Step 3 -- Act on Reviewer Feedback

Categorize each item and act accordingly:

| Severity | Action |
|----------|--------|
| **Critical/Blocking** | Fix immediately. Do not proceed until resolved. |
| **Important** | Fix before moving to the next task. |
| **Minor/Nitpick** | Note for later. Do not block progress. |
| **Wrong** | Push back with reasoning. See "Push Back When Justified" below. |

---

## Mode B: Receiving Review (Human or External Reviewer)

When feedback arrives from a human reviewer or external tool.

### Source Trust Levels

Not all review feedback is equal:

- **Your user (human partner):** Trusted. Implement their feedback after understanding it. They know the codebase context.
- **Team reviewers (PR comments):** Mostly trusted. Verify against codebase before implementing - they may not have full context.
- **External reviewers (automated tools, AI reviewers):** Verify everything. They lack project context. Check if suggestions are appropriate for THIS codebase.

### Step 1 -- Read Everything First

Read ALL feedback before acting on any of it. Do not start fixing the first comment while there are unread comments below it. Context from later comments may change how you handle earlier ones.

### Step 2 -- Evaluate Each Item

For each piece of feedback:

1. **Understand** -- What specifically is the reviewer asking for? If unclear, mark it for clarification.
2. **Verify** -- Check the codebase. Is the reviewer correct about the current state? Reviewers sometimes comment on stale diffs or misread context.
3. **Evaluate** -- Is this change technically correct for THIS codebase? Not in theory. Not in general. Here, now, with these constraints.

### Verification Checklist for External Feedback

Before implementing any suggestion from a team reviewer or external tool, run through this checklist:

1. **Technically correct for THIS codebase?** -- Does the suggestion work with our patterns, dependencies, and constraints?
2. **Breaks existing functionality?** -- Will applying this change break callers, consumers, or integrations?
3. **Reason for current implementation?** -- Is there a reason the code was written this way? Check git blame, PR descriptions, and comments.
4. **Works across all contexts?** -- Does it work in all environments, platforms, and versions we support?
5. **Reviewer has full context?** -- Does the reviewer understand the full picture, or are they commenting on an isolated snippet?

If you cannot verify a suggestion: say so. "I cannot verify this without [specific thing]. Should I [investigate further / ask the reviewer / proceed with caution]?" Admitting uncertainty is better than implementing blindly.

### Step 3 -- Clarify Before Implementing

If ANY item is unclear: **STOP.**

Ask for clarification on ALL unclear items at once. Do not implement some items while waiting for clarification on others. Partial implementation based on partial understanding creates more review cycles.

### Step 4 -- Implement in Order

Once all items are understood:

1. **Blocking issues** first
2. **Simple fixes** next (typos, naming, formatting)
3. **Complex changes** last

### Step 5 -- Test Each Fix

Test each fix individually. Do not batch fixes and hope they all work.

### Step 6 -- Verify No Regressions

Run the full test suite after all fixes are applied. New fixes must not break existing behavior.

---

## Technical Evaluation, Not Emotional Performance

Review is a technical process. Treat it like one.

### Never Do This

- "You're absolutely right!" -- Just fix it.
- "Great point!" or "Excellent feedback!" -- Performative. Skip it.
- "Thanks for catching that!" -- Gratitude is not a code review action.
- Agree before understanding -- Check if the suggestion is technically correct for THIS codebase first.

### Acknowledging Feedback

Good:

- "Fixed. [Brief description of what changed]."
- "Good catch -- [specific issue]. Fixed in [location]."
- Fix it silently. The commit speaks for itself.

Bad:

- "You're absolutely right!"
- "Great point!"
- "Thanks for catching that!"
- Any gratitude expression dressed up as a review response.

### Correcting Your Own Pushback

When you pushed back and the reviewer was right:

Good: "You were right -- I checked [X] and it does [Y]. Implementing now."

Bad: Long apology. Defending why you pushed back. Over-explaining your reasoning for being wrong.

---

## When Feedback Conflicts

If review feedback contradicts:
- **Prior user decisions:** STOP. Show the user both the feedback and the prior decision. Let them decide.
- **Other review comments:** Group the conflicting items. Present them together. Ask which direction to take.
- **Existing codebase patterns:** Note the conflict. Ask: "The reviewer suggests X, but the codebase consistently uses Y. Which should we follow?"

Never silently resolve conflicts by picking a side.

---

## Push Back When Justified

Not every review comment is correct. Push back when:

1. **Breaks existing functionality** -- "This change would break [specific thing] because [reason]. The current approach handles [edge case] that the suggested approach does not."
2. **Reviewer lacks context** -- "This looks wrong in isolation, but [module X] depends on this behavior. See [file:line]."
3. **Violates YAGNI** -- "This abstraction is not needed yet. Only one caller exists. Extracting it adds indirection without value."
4. **Technically incorrect** -- "This would actually cause [specific problem] because [technical reason]."

Be specific. Cite code. Do not push back with vibes.

**When pushing back feels uncomfortable:** If pushing back publicly in a PR thread would create friction or political problems, flag the concern privately to your user instead. Let the user decide how to handle it. Silence is not politeness -- it is a bug that ships.

---

## YAGNI Check

When a reviewer suggests "implementing properly" or "adding an abstraction" or "future-proofing":

```bash
grep -r "FunctionOrClassName" --include="*.{ts,js,py,cs,go}" .
```

- **If unused or single caller:** "This is only called from [one place]. Adding an abstraction here adds indirection without value. Remove it? (YAGNI)"
- **If multiple callers:** The reviewer has a point. Implement properly.

Do not build for hypothetical future callers. Build for the callers that exist.

Both you and the reviewer serve the user's goals. If a feature is not needed, the user decides whether to add it -- not the reviewer. Escalate YAGNI disagreements to the user rather than debating in the PR thread.

---

## GitHub Thread Handling

When replying to inline PR comments, reply in the thread:

```bash
gh api repos/{owner}/{repo}/pulls/{pr}/comments/{comment_id}/replies \
  -f body="Fixed. [description]"
```

Do NOT post a top-level comment when responding to an inline review comment. The reviewer left feedback on a specific line. Reply on that line.

---

## Gut Check -- Are You Doing Review Right?

Pause and check yourself:

- **Saying "You're absolutely right!"** -- Stop. Just fix it.
- **Implementing without understanding** -- Stop. Ask what they mean.
- **Agreeing with everything** -- Stop. Check if it is technically correct for THIS codebase.
- **Afraid to push back** -- If it breaks something, say so. Silence is not politeness. It is a bug.
- **Partially implementing** -- Stop. Clarify ALL unclear items first, then implement.
- **Writing a paragraph where a sentence would do** -- Stop. "Fixed." is a complete response.

---

## Subagent Prompt Template

The Code Reviewer subagent follows the prompt template at:

```
agents/code-reviewer-agent.md
```

When dispatching, load the template and inject the task-specific context (diff, spec, checklist) into the designated sections.

---

## Subagent Context Preservation

When the Code Reviewer subagent completes, explicitly capture its findings back to the main conversation:

- All review items with severity (critical, important, minor, wrong)
- Specific file paths and line numbers referenced
- Whether blocking issues were found

Do not assume the orchestrating agent retains subagent context automatically. Extract the full review before acting on it.

---

## Recommended Model

**Primary:** sonnet
**Why:** Code review requires understanding patterns, spotting bugs, and evaluating design decisions. Sonnet provides sufficient depth without the cost of opus.

This is a recommendation. Ask the user: "Confirm model selection or override?" Do not proceed until the user responds.

---

## Exit Condition

Review is complete when:

- All blocking and important items are resolved
- All fixes are tested individually
- Full test suite passes with no regressions
- All GitHub threads are replied to (if applicable)

After exit, resume the calling workflow.
