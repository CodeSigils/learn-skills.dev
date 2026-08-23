---
name: explain-skill

description: Explain what a skill does, when to use it, how it behaves, and what it does not do. Use when you want to understand an available skill before using it.

metadata:

  disable-model-invocation: true

---

# Explain Skill

Explain the skill.

This skill explains an available skill in practical terms. Given a skill name, inspect its current definition and explain what it is for, when it should be used, how it behaves, and where its boundaries are.

Do not modify, execute, or improve the skill being explained.

## Step 1 — Find the skill

Identify the requested skill from the skills currently available to the agent.

Use the agent's native skill discovery or listing mechanism when available. If necessary, locate the corresponding `SKILL.md` through the current environment's skill locations.

Use the skill's current definition as the source of truth.

If the requested skill does not exist or cannot be found, say so clearly. Do not invent a description.

## Step 2 — Understand the skill

Read enough of the skill definition to determine:

- What problem it solves
- What triggers its use
- What it does
- What it does not do
- What information or context it depends on
- What output or behavior it produces
- Any important constraints or boundaries

Distinguish between explicit behavior defined by the skill and reasonable interpretation.

Do not claim capabilities that are not supported by the skill definition.

## How to explain

Explain the skill in terms a user can act on.

Format every reply as:

1. **What it is** — one or two sentences describing the skill's purpose.
2. **When to use it** — the situations where it is useful.
3. **What it does** — the main behavior or process.
4. **What it does not do** — important boundaries or misconceptions.
5. **Example** — one short example showing when it would be useful.

Keep the explanation proportional to the complexity of the skill.

For a simple skill, keep the explanation simple.

For a complex skill, explain the important behavior without merely reproducing the entire `SKILL.md`.

## Accuracy

- Use the current skill definition as the source of truth.
- Do not invent capabilities, dependencies, or behavior.
- Do not silently fill missing details with assumptions.
- Do not execute the skill being explained.
- Do not modify the skill.
- Do not rewrite the skill unless explicitly asked.

## When the skill is ambiguous

If the skill definition does not provide enough information to explain an important behavior, say that the behavior is unclear from the current definition.

Do not present assumptions as facts.

## Maintenance

This skill should remain focused on explaining existing skills.

Only update this file when its discovery process, explanation format, or accuracy rules need to change.