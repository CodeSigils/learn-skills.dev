---
name: tldr
description: Use when the user wants a TL;DR, quick recap or brief summary.
---

# TL;DR

## Overview

Summarize the current matter at hand in the shortest form that still preserves the point.

Optimize for fast orientation, not completeness.

## When to Use

Use this skill when the user asks for:

- A TL;DR
- A quick recap
- A brief summary
- The current status or state of play
- "What are we dealing with?"
- "Where do things stand?"

Do not summarize the entire conversation unless that is what the current matter requires.

## Output Shape

Choose the lightest format that fits:

- One sentence for simple matters
- Short bullets for multi-part status, decisions, blockers, or next steps
- A short paragraph for verdicts, reports, or summaries that need a little connective tissue

You may combine formats when that reads better, but keep it tight.

## What to Include

Focus on the parts that matter most right now:

- What the matter is
- Current status
- Key blocker, decision, or implication
- Next step, if useful

If something is unclear or unresolved, say so plainly.

## Style

- Be concise
- Prefer concrete language over setup or framing
- Avoid repeating details the user already has unless they help orient the summary
- Avoid unnecessary background
- Do not pad the answer with generic conclusions

## Examples

**Simple matter:**

> We need to add a small `tldr` skill that gives a concise summary of the current issue, and the design is already approved.

**Multi-part matter:**

- Task: add a new `tldr` skill
- Status: design approved
- Next step: create `skills/tldr/SKILL.md`

**Verdict/report matter:**

> The main issue is that the current summary is too verbose for the situation. A short paragraph works best here because it needs to communicate both the conclusion and why it matters without turning into a full report.
