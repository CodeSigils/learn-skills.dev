---
name: experiment-design
description: Use before changing a model, loss, optimizer, dataset pipeline, augmentation, or evaluation protocol for deep learning research work
---

# Experiment Design

Turn a rough research idea into a falsifiable experiment plan before writing code.

## Hard Gate

Do not change code, configs, or launch runs until these are clear:

- hypothesis
- baseline
- success metric
- dataset and split
- compute budget

## Workflow

1. Inspect the current baseline: code path, configs, last known results, open uncertainties.
2. Ask clarifying questions one at a time.
3. State the hypothesis in one sentence: "If we change X, metric Y should improve because Z."
4. Propose 2-3 approaches and recommend one.
5. Define the first experiment as the smallest test that could disprove the idea.
6. Write an experiment card to `docs/experiments/specs/YYYY-MM-DD-<topic>.md`.
7. Get user approval before moving to `experiment-planning`.

## Experiment Card

Every design doc should include:

- goal
- baseline to beat
- exact metric and selection rule
- train/val/test or benchmark split assumptions
- minimal code/config changes expected
- sanity checks before full training
- failure modes and what evidence would invalidate the idea
- next decision after the first run

## Guardrails

- Do not hide evaluation changes inside modeling changes.
- Do not compare against a weak or mismatched baseline.
- Do not treat one lucky run as evidence.
- If the idea touches multiple subsystems, split it into separate experiments.
