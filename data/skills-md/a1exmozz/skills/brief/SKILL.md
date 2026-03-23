---
name: brief
description: "Structured discovery process for starting new work. Aligns on goals, success criteria, and key design decisions through a two-phase interview: goal clarification then systematic resolution of design questions with options, tradeoffs and recommendations. Use when kicking off a new project or feature."
---

# Follow these instructions below, in order, one at a time.

## Vibe Check

1. Ask: “What are we doing and why?”
2. Restate the goal/use-case in your own words, then ask: “Is this correct?”
3. Ask: “Roughly speaking, what would success or 'good enough' look like?”

## Questions

1. Identify the key design questions first, prioritising the most constraining or irreversible decisions. Output the complete list under the heading “Key Design Questions”.
2. For each design question, first ask whether it is a real constraint, a preference or accidental process baggage. Remove or downgrade anything that does not materially affect the design.
3. Do your own research to answer questions, before asking any.
4. For each remaining question, ask them one at a time and:
   i. Clearly state the design question
   ii. Present 3 viable options
   iii. Give your current recommendation with reasoning
   iv. List the main tradeoffs
   v. State whether the decision is reversible or hard to unwind
   vi. If your confidence is low, state it and explain exactly how the uncertainty should be resolved
5. Convert answers into provisional decisions, not fixed doctrine. Revisit earlier decisions if later answers materially change the design.
6. Review decisions for ambiguity, conflicts, hidden dependencies or unnecessary constraints. Then ask clarifying follow-ups.

## Output

1. _After_ completing the above, produce the `Brief` using the template [here](./references/brief-template.md)
2. Show the completed `Brief` in full.
