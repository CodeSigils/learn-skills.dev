---
name: funnel-analysis
description: Use when a user journey has sequential steps and the AI should identify where conversion breaks, how denominators change, and what segments matter.
source: perlytics-skill
version: 1.0.0
---

# Funnel Analysis

## Purpose

Analyze stage-by-stage progression through a sequential flow without losing denominator discipline.

## When to use

Use this skill when:

- users move through defined steps
- conversion can fail at multiple points
- the team needs to know where and for whom the drop occurs

## When not to use

Do not use this skill when:

- the journey is not sequential
- the question is about long-term retention rather than step conversion

## Required thinking discipline

- Define every stage clearly.
- Keep entity and denominator explicit.
- Distinguish stage conversion from cumulative conversion.
- Separate volume issues from conversion-rate issues.
- **Evidence constraint:** Every conclusion must cite specific data — a number, a rate, a segment, or a timeframe. Do not speculate without evidential basis. If data is insufficient, state what is missing rather than asserting an unsupported inference.

## Workflow

1. Define the funnel entity and steps.
2. Confirm what counts as step completion.
3. Calculate stage volume, stage conversion, and cumulative conversion.
4. Compare with baseline or prior period.
5. Break the funnel by important segments.
6. Highlight the first meaningful break and any downstream effects.

## Output format

- Funnel definition
- Stage table
- Largest breakpoints
- Segment differences
- Likely explanations
- Recommended next checks

## Good example

> Signup-to-paid funnel, user-level entity, weekly grain. The biggest break is trial start to first session for mobile-acquired users, where stage conversion fell from 62% to 49%.

## Bad example

> The funnel is weak in the middle.

Why this is bad:

- stage names are vague
- denominator is missing
- no segment or baseline context

## Practical notes

- Include absolute counts and rates together.
- Watch for a top-of-funnel mix shift that changes downstream rates.
- If steps changed definition, call that out before interpretation.

## Optional variants

- Ecommerce: focus on product view, add to cart, checkout, payment success.
- SaaS: focus on signup, activation event, return usage, paid conversion.
