---
name: prototype
description: "Build throwaway code to answer a product, UI, state, API, or workflow question before committing to the real implementation. Use when the user asks to prototype, try a few options, sanity-check a model, explore a design, or make something playable."
---

# Prototype

A prototype answers one question. It is not production code.

## Shape

Pick the smallest artifact that lets the user judge the idea:

- Logic, state, API shape, or workflow: make a tiny runnable CLI, script, or local page that exposes the state and lets the user push it through cases.
- UI or interaction: make 2-4 meaningfully different variants, preferably inside the existing page or route they would affect.

If the question is unclear, state the assumption before building.

## Rules

- Write the question near the prototype so the reader knows why it exists.
- Put it near the relevant code and name it as a prototype.
- Use the project's existing runtime, router, styling, and task runner.
- Give the user one command or URL to run it.
- Keep state in memory or in obvious scratch data unless persistence is the question.
- Keep it small: no broad abstractions, production polish, or extra test harness.
- Make the moving parts visible: current state, selected variant, inputs, outputs, or transitions.
- When the question is answered, delete the prototype or fold the useful decision into real code.

Leave a short note with the result only when the answer is not captured elsewhere.
