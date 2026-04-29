---
name: plan
description: Write a plan file for a multi-step task (Step 3 of /task). Runs one brainstorming round then writes ai-workspace/plans/<name>.md from TEMPLATE.md. Skipped for one-sentence scope. Does NOT review — that is /review (Step 4).
---

# /plan

Write a plan file for the current task. Requires /orient to have run first.

## Sequence

1. **Check prerequisites.** Confirm a worktree exists and /orient has identified the task. If not, stop and tell the user.
2. **Brainstorm (one round).** Invoke `/brainstorming` with the task description. One round only — capture direction, do not iterate.
3. **Read the template.** Read `ai-workspace/plans/TEMPLATE.md` from the repo root.
4. **Write the plan.** Create `ai-workspace/plans/<branch-slug>.md` with ALL template fields:

| Field | How to fill |
|---|---|
| **Branch** | Current branch name |
| **Created** | Today's date (YYYY-MM-DD) |
| **Status** | `In Progress` |
| **Threat model** | See selection table below |
| **Scope ceiling** | Keep template defaults (400/6 soft, 800/10 hard) |
| **Task** | 1-3 sentences: what and why |
| **Steps** | Checkbox list of concrete implementation steps |
| **Confidence Scaffold** | Required for `adversarial`. Recommended for complex `advisory`. |
| **Outcomes & Learnings** | Leave empty — populated by /archive |

## Threat model selection

| Signal | Model |
|---|---|
| Internal tooling, refactor, docs, tests, config | `advisory` |
| Auth, secrets, input validation, CI, hooks, permissions | `adversarial` |
| Unsure | `adversarial` |

## Guardrails

- Do NOT review the plan. That is /review (Step 4).
- Do NOT start implementation. The plan is the deliverable.
- Do NOT skip any template field.
- If brainstorming reveals the task is one-sentence scope, say so and skip.
- Scope ceiling values are fixed — do not change them.
- Steps must be concrete actions with checkboxes, not vague phases.
- Include test steps explicitly.

## Output

After writing, report:

```
Plan written: ai-workspace/plans/<name>.md
Threat model: advisory|adversarial
Steps: <count>
Next step: /review
```
