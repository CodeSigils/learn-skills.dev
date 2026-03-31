---
name: lessons-learned
description: Structured retrospective for incidents, mistakes, and near-misses. Transforms problems into systematic improvements encoded in the right place.
use_when: After incidents, mistakes, rollbacks, workflow failures, or when analyzing what went wrong. Triggers on "lessons learned", "post-mortem", "what went wrong", "how do we prevent this", "that didn't work".
effort: normal
---

# Lessons Learned

Transform problems into systematic improvements through structured retrospective analysis.

## Why This Matters

Mistakes repeat when we only fix symptoms. With structured retrospectives:
- Root causes get addressed, not just symptoms
- Fixes are encoded in the right place (project configuration, task management, skills, workflows)
- Each problem makes the system stronger
- You never hear "we should have thought about that first"

## Integration with Your System

Fixes from retrospectives go to the appropriate location:

| Fix Type | Destination |
|----------|-------------|
| Claude behavior change | Project configuration update |
| Recurring task adjustment | Task management system notes |
| Workflow improvement | Skill creation/update |
| Knowledge gap | Reference doc |
| Tool configuration | Relevant config file |

## Quick Start

1. Define the incident factually
2. Build a timeline
3. Find root cause with 5 Whys
4. Identify contributing factors
5. Implement fixes (don't just recommend them)
6. Define verification criteria

## Process

### Phase 1: Incident Definition

**Capture facts first, analysis later.**

```markdown
## Incident Summary

**What happened:** [Factual description - no blame, no interpretation]
**When:** [Date/time or session context]
**Impact:** [What was affected - deliverable, relationship, time, quality]
**Resolution:** [How it was fixed or mitigated]
**Time to resolution:** [How long to fix]
```

### Phase 2: Timeline Reconstruction

| Time/Step | Action | Actor | Outcome |
|-----------|--------|-------|---------|
| [When] | [What was done] | [Who - User/Claude/System] | [Result] |

**Key questions:**
- What was the trigger?
- Where did things diverge from expected?
- What was the point of no return?
- Were there warning signs we missed?

### Phase 3: Root Cause Analysis (5 Whys)

1. Why did [incident] happen?
   → Because [immediate cause]

2. Why did [immediate cause] happen?
   → Because [deeper cause]

3. Why did [deeper cause] happen?
   → Because [systemic issue]

4. Why did [systemic issue] exist?
   → Because [process gap]

5. Why did [process gap] exist?
   → Because [root cause]

**Root Cause:** [The fundamental issue to address]

### Phase 4: Contributing Factors

| Category | Factor | Contribution |
|----------|--------|--------------|
| **Process** | Missing checkpoint | [How it contributed] |
| **Communication** | Unclear instructions | [How it contributed] |
| **Context** | Missing information | [How it contributed] |
| **Tools** | System limitation | [How it contributed] |
| **Assumptions** | Unstated expectation | [How it contributed] |

### Phase 5: Fix Classification

| Fix Type | When to Use | Where to Encode |
|----------|-------------|-----------------|
| **Configuration rule** | Claude behavior needs adjustment | Project configuration |
| **Skill update** | Workflow needs structure | Your skills directory |
| **New skill** | Recurring workflow unstructured | Your skills directory |
| **Task (one-time)** | One-time action needed | Task management system |
| **Task (recurring)** | Periodic check needed | Task management system (recurring) |
| **Reference doc** | Knowledge gap | Your reference docs directory |
| **Project state file** | Project-specific context | Active project state files |

### Phase 6: Fix Implementation

**Don't just recommend fixes—implement them in this session.**

| Fix | Type | Location | Status |
|-----|------|----------|--------|
| [Description] | Configuration | [Section] | Implemented |
| [Description] | Skill | [Path] | Created/Updated |
| [Description] | Task management | [Task name] | Created |

### Phase 7: Verification

```markdown
**Test scenario:** [How to test the fix works]
**Success criteria:** [What "fixed" looks like]
**Review date:** [When to check if working - add to task management if needed]
```

## Output Template

```markdown
---
title: "Lessons Learned - [Incident Title]"
created: YYYY-MM-DD
last_modified: YYYY-MM-DD
tags: [lessons-learned, retrospective]
status: resolved | monitoring | open
---

# Lessons Learned: [Incident Title]

**Date:** YYYY-MM-DD
**Severity:** Low | Medium | High | Critical
**Status:** Resolved | Monitoring | Open

## Incident Summary
[Brief description - facts only]

## Timeline
| Step | Action | Outcome |
|------|--------|---------|

## Root Cause
[The fundamental issue - one sentence]

## 5 Whys Chain
1. → 2. → 3. → 4. → 5. [Root]

## Contributing Factors
- Factor 1
- Factor 2

## Fixes Implemented
| Fix | Type | Location | Status |
|-----|------|----------|--------|

## Prevention
[How this prevents recurrence - be specific]

## Verification
- **Test:** [How to verify]
- **Success:** [What good looks like]
- **Review:** [When to check]

## Key Lessons
1. [Takeaway 1]
2. [Takeaway 2]
```

## Common Patterns in the Vault

### Premature Action
**Symptom:** Action taken before confirmation
**Typical fix:** Add explicit approval gate to project configuration or skill

### Context Carryover
**Symptom:** Assumptions from prior session caused issue
**Typical fix:** Add to session startup checklist or project state file requirements

### Missing Information
**Symptom:** Didn't have context needed for good decision
**Typical fix:** Update auto-load triggers in project configuration or add to reference docs

### Scope Creep
**Symptom:** Did more than requested
**Typical fix:** Add "confirm scope before proceeding" rule

### Tool/System Mismatch
**Symptom:** Used wrong tool or created something that already exists
**Typical fix:** Strengthen PAUSE protocol or add to tool integration docs

## Anti-Patterns

| Anti-Pattern | Problem | Instead |
|--------------|---------|---------|
| Blame assignment | Misses systemic issues | Focus on process |
| Single-cause thinking | Oversimplifies | Use 5 Whys |
| Recommendation without action | Lessons forgotten | Implement during retrospective |
| Vague fixes | "Be more careful" doesn't work | Encode specific changes |
| Fix in wrong place | Gets lost or ignored | Match fix type to destination |

## Where to Save

Retrospective documents go to: `./Archived/Lessons Learned/YYYY-MM-DD - [Topic].md` (or your preferred archive location)

(Archived because the value is in the implemented fixes, not the document itself)

## Invocation

Automatic triggers:
- Something went wrong that we want to prevent
- User expresses frustration with outcome
- Workflow failure or unexpected result

Manual: `/lessons-learned` or "let's do a retrospective on that"

## Success Criteria

- [ ] Incident clearly defined with timeline
- [ ] Root cause identified (not just symptoms)
- [ ] Contributing factors documented
- [ ] At least one fix implemented (not just recommended)
- [ ] Fix encoded in appropriate location
- [ ] Verification criteria defined
- [ ] Retrospective document saved to archive
