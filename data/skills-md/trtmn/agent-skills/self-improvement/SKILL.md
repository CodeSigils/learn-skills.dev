---
name: self-improvement
description: Automatically logs corrections, errors, and learnings to .learnings/ and promotes the most valuable insights to permanent memory (project CLAUDE.md or user ~/.claude/CLAUDE.md) so every mistake is a one-time mistake. MUST use this skill whenever the user corrects Claude ("actually, it should be...", "don't do that", "I told you last time", "I keep having to correct you", "that's wrong"), a command or tool fails unexpectedly, the user asks Claude to remember something for future sessions ("log this", "remember that", "add this to your memory", "learn from this", "make sure we don't hit this again", "track this", "don't forget"), or the user wants to review GitHub PRs/issues for recurring patterns and lessons. Also trigger after substantial debugging sessions when the user wants to capture what went wrong, or when the user asks for an end-of-session review of what was learned. Do NOT trigger for normal coding tasks like writing scripts, refactoring, debugging, setting up projects, writing tests, or reviewing PR code quality — only trigger when the user wants to *persist a lesson* or when an error/correction should be tracked for future reference.
---

# Self-Improvement

This skill makes you better over time. When something goes wrong — a command fails, the user corrects you, you hit a knowledge gap — you log it and, when the insight is worth keeping, promote it to permanent memory so future sessions benefit.

The key difference from a passive "log things" approach: this is automatic. You don't wait to be asked. You log as things happen and promote as soon as something deserves it.

## Log Files

Maintain three structured markdown files in a `.learnings/` directory at the project root (create it if it doesn't exist):

- **`.learnings/LEARNINGS.md`** — Corrections, knowledge gaps, best practices
- **`.learnings/ERRORS.md`** — Command failures, exceptions, unexpected behaviors
- **`.learnings/FEATURE_REQUESTS.md`** — Capabilities the user asked for that you couldn't provide
- **`.learnings/CHANGELOG.md`** — Permanent, append-only record of every promotion (and reversion) to CLAUDE.md

## Automatic Logging

Log immediately — don't ask permission, don't wait for a pause. Context is freshest right after the event. After logging, briefly tell the user what you logged (one line, e.g., "Logged that port conflict to ERRORS.md"). Don't belabor it.

### What triggers a log entry

- **User corrections**: "Actually, it should be...", "No, don't...", "That's wrong because..." → LEARNINGS.md
- **Knowledge gaps**: You gave outdated info, missed a project convention, or had to be corrected → LEARNINGS.md
- **Command/tool failures**: A shell command failed, an API call errored, a file operation didn't work as expected → ERRORS.md
- **Feature requests**: The user asked for something you couldn't do → FEATURE_REQUESTS.md
- **Patterns repeating**: Same mistake made more than once in a session → LEARNINGS.md (bump to high priority)

### What does NOT need a log entry

Not every hiccup is worth recording. Skip logging for:
- Typos or trivial self-corrections that won't recur
- Failures caused by transient conditions (network blip, server momentarily down)
- Things already documented in the project's CLAUDE.md or README
- Minor misunderstandings clarified in one exchange with no broader lesson

The bar: "Would future Claude plausibly make this same mistake?" If yes, log it. If no, move on.

## Entry Format

### LEARNINGS.md
```markdown
## [LRN-YYYYMMDD-001] Short descriptive title
- **Timestamp**: ISO-8601
- **Priority**: low | medium | high | critical
- **Status**: pending | promoted
- **Area**: frontend | backend | infra | tests | docs | config | workflow | other
- **What happened**: Brief description of the correction or gap
- **Lesson**: The concrete takeaway
- **Source**: e.g., "User correction in conversation", "PR #42", "Issue #17"
- **Suggested fix**: Specific action or rule change
```

### ERRORS.md
```markdown
## [ERR-YYYYMMDD-001] Short descriptive title
- **Timestamp**: ISO-8601
- **Priority**: low | medium | high | critical
- **Status**: pending | resolved
- **Area**: (same categories as above)
- **Command/action**: What was attempted
- **Error**: The failure message or description
- **Root cause**: Why it failed (once known)
- **Fix**: What resolved it or what to do differently next time
- **Reproduction**: Steps to reproduce (if useful)
```

### FEATURE_REQUESTS.md
```markdown
## [FEAT-YYYYMMDD-001] Short descriptive title
- **Timestamp**: ISO-8601
- **Priority**: low | medium | high | critical
- **Status**: pending | implemented | promoted
- **Area**: (same categories)
- **Request**: What the user asked for
- **Context**: Why they needed it, what they were trying to accomplish
- **Workaround**: What was done instead, if anything
```

## Automatic Promotion

Promotion means writing an insight into a CLAUDE.md file so it persists across all future conversations. The old version of this skill waited until end-of-session and asked for permission — that was too passive. Now, promote immediately when the criteria are met.

### When to promote

Promote as soon as you recognize that an insight is:
1. **Broadly applicable** — it applies beyond this one conversation or file
2. **Likely to recur** — future Claude would plausibly hit the same issue
3. **Not already documented** — check the target CLAUDE.md first to avoid duplicates

You don't need all three to be strong. A single devastating mistake that's clearly going to repeat is enough. A mild preference that applies everywhere is enough. Use judgment.

### Where to promote

**Project CLAUDE.md** (in the project root) — for project-specific conventions, patterns, and pitfalls. Examples:
- "This codebase uses `pathlib.Path` everywhere — don't use `os.path.join`"
- "Tests require a running PostgreSQL instance, not mocks"
- "The `deploy.sh` script expects AWS_PROFILE=staging"

**User CLAUDE.md** (`~/.claude/CLAUDE.md`) — for cross-project knowledge that applies to this user's environment, preferences, or workflow regardless of which project they're in. Examples:
- "Port 5000 is taken by AirPlay on macOS — use 8888 for Flask"
- "User prefers terse responses, no trailing summaries"
- "Always use `op run` for secrets, never `eval $(op signin)`"

If you're unsure which file, ask yourself: "Would this matter if the user switched to a completely different project?" If yes → user CLAUDE.md. If no → project CLAUDE.md.

### How to promote

1. Read the target CLAUDE.md to find the right section (or create one if needed)
2. Write a concise, self-contained entry — it should make sense without the original conversation
3. Mark the source entry in `.learnings/` as `status: promoted`
4. Append an entry to `.learnings/CHANGELOG.md` (see format below)
5. Tell the user what you promoted and where (one line, e.g., "Promoted the pathlib convention to project CLAUDE.md")

### Promotion Changelog

Every promotion gets recorded in `.learnings/CHANGELOG.md` — a permanent, append-only audit trail. This lets the user (or future Claude) review what was promoted, when, where, and why, and revert anything that doesn't belong.

```markdown
## [PROMO-YYYYMMDD-001] Short title matching the source entry
- **Timestamp**: ISO-8601
- **Source**: LRN-20260323-001 (or ERR-, FEAT- reference)
- **Target**: project CLAUDE.md | user CLAUDE.md (~/.claude/CLAUDE.md)
- **Section**: Which section of the target file it was added to
- **What was promoted**: The exact text or a close summary of what was written
- **Why**: One sentence on why this deserved promotion
```

Never edit or delete changelog entries — if a promotion turns out to be wrong, add a new `[REVERT-YYYYMMDD-001]` entry explaining what was removed and why, then remove it from the target CLAUDE.md.

Keep promoted entries lean. A CLAUDE.md that's 90% promoted learnings becomes noise. Distill the insight down to one or two sentences with a concrete example if helpful.

### What NOT to promote

- One-off workarounds for temporary situations
- Things specific to a single file or narrow context
- Debugging steps that are already in the fix (the code is the documentation)
- Anything already captured in the target CLAUDE.md (check first!)

## Learning from GitHub PRs and Issues

When the user asks you to learn from GitHub history (PRs, issues, discussions), use `gh` CLI to analyze patterns:

```bash
# Fetch closed PRs with review comments
gh pr list --state closed --limit 50 --json number,title,reviews,comments

# Look at a specific PR's review feedback
gh pr view <number> --json reviews,comments,body
```

Extract:
- Recurring reviewer complaints → lessons for LEARNINGS.md
- Rejected approaches (and why) → patterns to avoid
- Common bug patterns from issues → entries for ERRORS.md
- Frequently requested features → FEATURE_REQUESTS.md

Focus on patterns that appear in multiple PRs/issues rather than one-off events. Always cite the source PR or issue number in the entry.

## Principles

**Be specific, not vague.** "Don't use deprecated APIs" is useless. "Don't use `os.path.join` in this codebase — it uses `pathlib.Path` everywhere (see utils.py)" is useful.

**Document the why.** Future Claude won't remember the context. Make the lesson self-contained enough that it makes sense without the original conversation.

**Don't over-log.** Not every stumble needs to be recorded. Use judgment — log things that are likely to recur or that reveal a genuine gap, not every minor uncertainty.

**Link related entries.** If an error connects to a learning or a feature request, cross-reference them.

**Act, don't ask.** The whole point of auto-logging and auto-promoting is to reduce friction. Log it, promote it, tell the user you did — don't ask permission each time. The user can always tell you to undo something, but they shouldn't have to remind you to do it.
