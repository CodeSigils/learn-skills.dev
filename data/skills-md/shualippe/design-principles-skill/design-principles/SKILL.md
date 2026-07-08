---
name: design-principles
description: >
  Apply universal design principles to UI/UX review, design feedback, and design documentation.
  Based on "Universal Principles of Design" (Lidwell, Holden, Butler) — 100 cross-disciplinary
  principles covering usability, perception, learning, appeal, and decision-making. Use this skill
  whenever the user asks to review a UI, critique a design, evaluate a mockup or wireframe, give
  design feedback, write a design spec or design doc, discuss design tradeoffs, improve a layout,
  or apply design thinking to a product decision. Also trigger when the user asks about specific
  design concepts like affordance, Fitts' Law, Hick's Law, progressive disclosure, visual hierarchy,
  Gestalt principles, cognitive load, or any named principle from the book. Even if the user doesn't
  say "design principles" explicitly, use this skill when they're asking for help with UI decisions,
  layout choices, interaction patterns, or user experience improvements.
---

# Universal Design Principles

A skill for applying 100 cross-disciplinary design principles to UI/UX work — design reviews, feedback, documentation, and decision-making.

## When to use this skill

- **Design review / critique**: User shares a UI, mockup, wireframe, or screenshot and wants feedback
- **Design docs / specs**: User is writing a design document and wants principled rationale
- **Design decisions**: User is weighing tradeoffs (e.g., flexibility vs. usability, aesthetics vs. function)
- **Concept explanation**: User asks about a specific design principle or wants to understand a pattern
- **Improvement suggestions**: User wants ideas for making a UI better

## Core behavior

When this skill triggers, read `references/principles.md` to access the full catalog of 100 principles with definitions, UI/UX applications, and cross-references. The reference file is your authoritative source — always consult it rather than relying on memory alone.

### Mode 1: Design Review & Feedback

When the user shares a design (screenshot, description, mockup, URL) for review:

1. **Identify what's working well** — lead with strengths, citing the principles they satisfy
2. **Surface potential issues** — flag problems through the lens of relevant principles
3. **Recommend improvements** — give concrete, actionable suggestions tied to principles
4. **Keep it focused** — cite 3–7 principles per review, not all 100. Pick the ones most relevant to the specific design. Prioritize principles that point to actionable changes.

Structure your feedback conversationally, not as a checklist. Weave principles in naturally:

> "The nav feels cluttered — there are 12 top-level items, which works against **Hick's Law** (more options = slower decisions). Grouping these into 4–5 categories with progressive disclosure would help."

Not like this:

> "**Hick's Law**: The navigation has too many items. **Progressive Disclosure**: Consider hiding some. **Chunking**: Group items together."

### Mode 2: Design Documentation

When the user is writing a design doc, spec, or rationale:

1. **Ground recommendations in principles** — provide principled justification for design choices
2. **Anticipate objections** — use principles to preempt "why not do it this other way?" questions
3. **Match the doc's tone** — formal for PRDs, conversational for Slack summaries
4. **Cross-reference related principles** — when one principle applies, its related principles often do too

### Mode 3: Concept Explanation

When the user asks about a specific principle or design concept:

1. **Define it clearly** — give the core definition first
2. **Make it concrete for UI/UX** — provide digital product examples, not just abstract theory
3. **Connect it** — mention 2–3 related principles that often work alongside it
4. **Keep it practical** — focus on "how to apply this" over academic history

## Five design questions

The 100 principles map to five key questions designers face. Use these to organize your thinking when reviewing a design holistically:

1. **How can I influence perception?** — Affordance, Alignment, Closure, Color, Consistency, Figure-Ground, Highlighting, Law of Pragnanz, Mapping, Orientation Sensitivity, Proximity, Signal-to-Noise Ratio, Similarity, Threat Detection, Uniform Connectedness, Visibility
2. **How can I help people learn?** — Advance Organizer, Chunking, Classical Conditioning, Comparison, Depth of Processing, Exposure Effect, Iconic Representation, Interference Effects, Inverted Pyramid, Layering, Legibility, Mental Model, Mnemonic Device, Operant Conditioning, Performance Load, Picture Superiority, Progressive Disclosure, Readability, Recognition Over Recall, Serial Position Effects, Shaping, Signal-to-Noise Ratio, Storytelling
3. **How can I enhance usability?** — 80/20 Rule, Accessibility, Aesthetic-Usability Effect, Affordance, Confirmation, Consistency, Constraint, Control, Cost-Benefit, Entry Point, Errors, Fitts' Law, Forgiveness, Hick's Law, Hierarchy, Iconic Representation, Immersion, Interference Effects, Inverted Pyramid, Layering, Mapping, Mental Model, Mimicry, Performance Load, Progressive Disclosure, Readability, Recognition Over Recall, Visibility, Wayfinding
4. **How can I increase appeal?** — Aesthetic-Usability Effect, Alignment, Archetypes, Attractiveness Bias, Baby-Face Bias, Classical Conditioning, Color, Exposure Effect, Face-ism Ratio, Fibonacci Sequence, Framing, Golden Ratio, Mimicry, Operant Conditioning, Prospect-Refuge, Rule of Thirds, Savanna Preference, Self-Similarity, Signal-to-Noise Ratio, Similarity, Storytelling, Symmetry, Top-Down Lighting Bias
5. **How can I make better design decisions?** — 80/20 Rule, Accessibility, Comparison, Convergence, Cost-Benefit, Development Cycle, Errors, Expectation Effect, Factor of Safety, Feedback Loop, Flexibility-Usability Tradeoff, Form Follows Function, Garbage In-Garbage Out, Hierarchy of Needs, Iteration, Life Cycle, Modularity, Normal Distribution, Ockham's Razor, Performance vs. Preference, Prototyping, Redundancy, Satisficing, Scaling Fallacy, Structural Forms, Uncertainty Principle, Weakest Link

## Principles to prioritize for UI/UX

While all 100 principles have value, these come up most often in digital product design:

**Interaction & usability**: Affordance, Constraint, Consistency, Fitts' Law, Hick's Law, Forgiveness, Progressive Disclosure, Recognition Over Recall, Mental Model, Feedback Loop, Control, Mapping

**Visual & layout**: Alignment, Hierarchy, Figure-Ground, Proximity, Similarity, Closure, Good Continuation, Signal-to-Noise Ratio, Color, Highlighting, Uniform Connectedness, Rule of Thirds

**Information & learning**: Chunking, Inverted Pyramid, Layering, Readability, Legibility, Iconic Representation, Advance Organizer, Serial Position Effects, Picture Superiority

**Strategic**: 80/20 Rule, Aesthetic-Usability Effect, Cost-Benefit, Hierarchy of Needs, Flexibility-Usability Tradeoff, Ockham's Razor, Performance Load, Accessibility

## Response guidelines

- Default to inline chat responses (conversational prose), not formatted reports
- Cite principles by name in **bold** when first introduced in a response
- Keep principle explanations brief unless the user asks for depth
- When reviewing a design, organize feedback by impact (high → low), not alphabetically by principle
- Avoid "principle dumping" — only cite what's genuinely relevant
- When principles conflict (e.g., Flexibility-Usability Tradeoff), acknowledge the tension and recommend a path based on context
- Use the cross-references in the principles file to connect related ideas
