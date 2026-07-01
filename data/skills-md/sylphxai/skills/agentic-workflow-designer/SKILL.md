---
name: agentic-workflow-designer
description: Design agentic workflows, AI agent operating loops, delegation patterns, human gates, tool boundaries, handoffs, evals, memory, review checkpoints, failure recovery, observability, and autonomy levels for product, engineering, research, support, marketing, operations, and skill-factory work. Use when creating repeatable workflows for AI agents or improving multi-step agent execution quality.
---

# Agentic Workflow Designer

Use this skill to design reliable agent workflows that produce auditable work instead of uncontrolled automation.

## Workflow

1. Identify goal, user, risk, autonomy level, tools, data, output artifact, and acceptance evidence.
2. Read `references/agentic-workflow-systems.md`.
3. Split workflow into deterministic steps, judgment steps, tool steps, review gates, and human approval gates.
4. Define memory/context, failure recovery, observability, evals, and handoff artifacts.
5. Produce a workflow spec with state machine, roles, tool contract, and validation plan.

## Guardrails

- Do not automate irreversible, payment, legal, secret, production, or customer-impacting actions without explicit approval gates.
- Do not rely on hidden chain-of-thought or tribal memory as workflow state.
- Require machine-readable outputs where downstream agents depend on them.

## Output format

```text
Workflow goal:
Autonomy level:
Inputs/tools:

Workflow states:
- <state> -> action, evidence, owner, failure path

Approval gates:
- <gate> -> why, approver, artifact

Evals/observability:
- <check or metric>
```
