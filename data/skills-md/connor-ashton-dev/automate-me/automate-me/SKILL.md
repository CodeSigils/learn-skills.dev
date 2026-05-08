---
name: automate-me
description: Helps non-technical users find, plan, and build lightweight automations for repeated work tasks. Use when choosing scripts, integrations, websites, workflows, or agents.
---

# Automate Me

## Overview

Help people turn one repeated workflow into the smallest useful automation. Start with the user's job-to-be-done, keep the conversation plain-English, choose the simplest build shape that can work, and leave enough documentation that a future agent can maintain it without pulling in the dev team.

## Reference Docs

- `references/automation-plan-template.md` - use when writing the review plan.
- `references/automation-recipe-card-template.md` - use when leaving maintenance notes.
- `references/evaluation-scenarios.md` - use when changing this skill.

## Core Rules

- Start with the workflow, not the technology.
- Ask one decision question at a time. Keep factual follow-up batches to 1 to 3 questions.
- Translate technical choices into everyday tradeoffs.
- Prefer the first simple option that solves the problem.
- Require a reviewable markdown plan before implementation.
- Keep a human approval step for sends, deletes, payments, customer-facing messages, permission changes, compliance-sensitive data, and uncertain outputs.
- Document setup, test examples, failure modes, and rollback before calling the automation done.
- Prefer not automating yet when the workflow lacks examples, ownership, safety, or a clear measurable win.
- Capture important workplace terms in the plan so future agents use the user's language consistently.

## Workflow

### 1. Find Or Sharpen The Idea

If the user already has an idea, restate it in plain language and ask what happens today. If they do not have an idea, help them discover one by asking about repetition:

- What task do you repeat every day or every week?
- What part of your job do you wish you never had to do again?
- What apps, emails, spreadsheets, files, or systems are involved?
- What does "done correctly" look like?
- What mistakes would be embarrassing, expensive, customer-facing, or hard to undo?
- How often does this happen, and roughly how much time does it take?

Ask for 5 to 10 real examples when possible, including weird or messy cases.

### 2. Narrow The First Version

Reduce broad requests to one starter workflow:

- One trigger
- One owner
- One output
- One approval point
- One run mode
- One measurable win

If the request is "automate my whole job" or "make an agent that handles everything," choose the highest-repetition, lowest-risk slice first.

### 3. Confirm The Working Location

Before writing plans, code, or docs, confirm where the automation should live.

- Inspect the current directory, repo name, README, and obvious project files.
- Decide whether the current repo is the right destination for the automation.
- If the automation belongs in another app, repo, folder, or standalone workspace, say so plainly and ask before writing files.
- If the current repo is only for planning, write the plan here only when that matches the user's intent.
- If the destination is not already a git repo and will contain implementation files, initialize one or ask before doing so when ownership is unclear.
- Do not create implementation files in the current repo just because it is where the chat started.

State the working-location assumption in plain English:

```text
I'm currently in <repo/folder>. This looks like <purpose>. I'll put <plan/code/docs> in <destination> because <reason>.
```

### 4. Choose The Simplest Build Shape

Before choosing a build shape, decide whether the work should stay manual for now. Stop at a checklist, handoff, or plan when:

- The workflow is rare or has no measurable win.
- The user cannot provide representative examples or approval rules.
- The task depends on judgment, trust, legal review, or policy interpretation that cannot be captured safely.
- Arbitrary external text could trigger sends, deletes, payments, permission changes, or customer-visible actions.
- No clear person owns access, maintenance, or failures.

Choose one run mode for the first version:

| Run Mode | Use When |
| --- | --- |
| Manual | The user runs it by hand and reviews the output before acting. |
| Supervised | The automation prepares or performs work only after explicit approval each run. |
| Scheduled | It runs on a timer with visible status, logs, failure notification, and high-impact actions still gated. |
| Autonomous | It runs without per-run approval only for low-risk, reversible actions with clear ownership and monitoring. |

Default to manual or supervised for first versions unless the workflow is low-risk and reversible.

Pick the first option on this ladder that can solve the narrowed workflow:

| Shape | Use When |
| --- | --- |
| Prompt or checklist | The user only needs repeatable guidance or a better handoff. |
| Spreadsheet formula/template | The work already lives in a sheet and the output is simple. |
| Native app automation | One app already has the needed automation feature. |
| No-code integration | The main job is moving data between existing apps. |
| Local script | The task is private, repeatable file or CSV work. |
| Scheduled script | The same script should run on a routine schedule. |
| Slack/email bot | The workflow already happens in messages or approvals. |
| Small internal web page | People need structured intake, editing, filters, permissions, or a review queue. |
| Durable workflow | The work is long-running, stateful, retry-heavy, or approval-heavy. |
| Agent with tools | The path cannot be fully predicted and the automation must choose actions or tools. |
| MCP/API surface | Other agents or technical users need reusable access before a custom UI exists. |

Avoid building a website, dashboard, database, multi-agent system, or custom framework unless the workflow clearly needs it.

### 5. Write The Plan Before Building

Create a markdown plan before implementation. Use `references/automation-plan-template.md`.

Default path:

```text
automation-plans/YYYY-MM-DD-<short-workflow-name>.md
```

If the repo already has a docs convention, use the closest existing place, such as `docs/automation-plans/`.

The plan must be understandable to a non-technical reviewer. After writing it, stop and ask for approval:

```text
I wrote the plan at <path>. Please review it and tell me what to change. I will wait for your approval before building.
```

Do not implement until the user approves or explicitly asks to skip the plan gate.

### 6. Build The Smallest Approved Version

After approval:

- Keep the implementation scoped to the approved first version.
- Use existing project patterns, tools, and connectors when available.
- Avoid asking the user to choose frameworks unless the choice affects their day-to-day use.
- Add dry-run or preview mode before any high-impact action.
- Add visible status, logs, or failure notification before scheduling or sending anything.
- Make errors specific enough that a future agent can diagnose them.
- Include a tiny set of real or representative test examples.

### 7. Leave A Recipe Card

Every automation needs a maintenance note. Use `references/automation-recipe-card-template.md`.

Default path:

```text
automation-docs/<short-workflow-name>.md
```

Include how to run it, what credentials or environment variables it needs, how to test safely, known limits, failure modes, rollback steps, and example inputs/outputs.

## Anti-Patterns

### Automating Before Examples

Do not build from vibes. If the user cannot provide representative inputs, expected outputs, and messy cases, stop at a checklist, handoff, or plan until examples exist.

### Building In The Repo Where The Chat Started

Do not treat the current repo as the implementation destination by default. Confirm the working location and version control before writing plans, code, or docs.

### Quiet Scheduled Automation

Do not schedule work that fails silently. Scheduled automations need visible status, logs, failure notification, a safe disable path, and a named owner.

## Good Defaults

- Prefer visible files over hidden notes when the documentation is meant for the user or future agents.
- Prefer one plain command over a complex setup flow.
- Prefer manual approval over fully automatic action for the first version.
- Prefer logs or simple output files over a new database unless history/search matters.
- Prefer a form or sheet over a web app when structured input is enough.
- Prefer a script over a service when one person runs it occasionally.

## What To Avoid

- Do not turn a vague request into a broad autonomous agent.
- Do not make non-technical users answer framework, hosting, database, queue, or model-routing questions unless necessary.
- Do not skip examples; successful automation depends on real inputs and edge cases.
- Do not hide maintenance details in the chat only.
- Do not let arbitrary external text trigger sends, deletes, payments, or customer-visible actions without review.
- Do not call the work complete until the user has clear run steps and future agents have clear repair notes.

## Skill Maintenance

When changing this skill, spot-check it against `references/evaluation-scenarios.md`.
