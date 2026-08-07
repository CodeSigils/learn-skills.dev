---
name: experiment-readout
description: Use when reading out an A/B test or quasi-experiment and the AI should communicate effect, uncertainty, guardrails, limitations, and recommended action.
source: perlytics-skill
version: 1.0.0
---

# Experiment Readout

## Purpose

Turn test results into a disciplined decision memo rather than a celebratory summary.

## When to use

Use this skill when:

- reading out an A/B test
- summarizing a quasi-experiment
- deciding whether to ship, hold, or investigate further

## When not to use

Do not use this skill when:

- the metric definitions are still unresolved
- the available evidence is too weak to call the result a test readout

## Required thinking discipline

- State the primary metric first.
- Separate observed lift from business impact interpretation.
- Include guardrails and negative signals.
- Be honest about uncertainty, power, and external validity.
- **Evidence constraint:** Every conclusion must cite specific data — a number, a rate, a segment, or a timeframe. Do not speculate without evidential basis. If data is insufficient, state what is missing rather than asserting an unsupported inference.

## Workflow

1. Define the test, population, and decision question.
2. Summarize the primary metric result.
3. Summarize important guardrails.
4. Note sample size, duration, and material limitations.
5. State the practical decision recommendation.
6. Call out what remains uncertain.

## Output format

- Decision question
- Primary metric result
- Guardrail summary
- Confidence and limitations
- Recommendation
- Follow-up actions

## Good example

> Primary metric improved +3.8%, guardrails were neutral, but the test only covered mobile web and ran during a promotion period. Recommendation: ship to mobile web, hold broader rollout until desktop validation.

## Bad example

> The experiment won, so we should launch everywhere.

Why this is bad:

- uncertainty is missing
- rollout scope is not considered
- guardrails are ignored

## Practical notes

- Include absolute baseline and relative lift where possible.
- Avoid treating "not significant" as evidence of no effect.

## Optional variants

- Product tests: include user-experience or trust guardrails.
- Pricing tests: include revenue quality and fairness risks.
