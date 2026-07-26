---
name: explainer
description: Hemant's house style for self-contained technical HTML explainers. Use for long-form explanatory pages that need clear prose, strong structure, tasteful editorial design, and no private-context leakage.
---

# explainer

Write the page a thoughtful human would want to read cold. The reader has not seen the chat, the source file, the outline, or your private reasoning. The article must stand on its own.

This skill exists to produce coherent, beautiful explanatory pages. Not styled memos. Not tutorial sludge. Not clever thesis fragments arranged inside nice typography.

## North Star

Clarity before style. Sequence before density. Reader footing before cleverness.

The reader should always know:

- what is being explained
- why it matters
- what question the current section is answering
- what to carry forward

Do not make the reader reconstruct the missing context from your notes. If a sentence only makes sense because the agent has already inspected the source material, it belongs in the working notes, not the article.

## Voice

Write like a sharp engineer with literary taste. Plain when orienting, precise when explaining, vivid only when the literal meaning is already secure.

Prefer concrete language over memo language. If "evidence" means proof of work, say proof of work. If "fit model" means how the options were ranked, say that. If "outreach ordering" means who to email first, say that.

Do not argue with a thought the reader has not had yet. Negation and reversal are powerful tools, but only after the piece has created the model being corrected.

Avoid consultant abstractions, motivational filler, and lyrical fog. Words like "lever", "axis", "strategic", "signal", and "conversion" must earn their place or leave.

## Working Method

Before building, privately find the spine:

- the central object under inspection
- the reader's real reason to care
- the questions the page answers, in order
- the claims that are sourced, measured, or clearly judgment-based
- the ending the reader needs: decision, next action, or next thing to understand

Then write the page from the reader's side of the glass. The outline is scaffolding; the article is architecture.

## Prose

Every paragraph should do useful work: orient, explain, compare, justify, warn, or transition.

Cut sentences that sound wise but do not move the reader forward. Do not defend the structure of the article before the reader understands the problem the article solves. Do not introduce internal labels before their referents are clear.

The opening should feel obvious in hindsight: a clean entrance into the subject, not a flourish that requires prior context. It can be stylish, but it cannot be cryptic.

## Technical Grounding

Mechanism matters. For technical topics, ground the explanation in real internals: code, syscalls, structs, bytecode, traces, benchmarks, protocol states, timing, or architecture. If a number matters, measure it or cite it. Never invent numbers.

For advising, planning, or decision explainers, ground the page in the decision being made: constraints, tradeoffs, ranked options, risks, and next actions. Do not force low-level systems metaphors onto material that needs practical judgment.

Use Go analogies when they genuinely reduce load for Hemant. Do not use them as decoration.

## Structure

Let section titles help the reader navigate by question or decision. Prefer human-facing labels over author-facing machinery.

Good section energy:

- who to contact first
- why this option fits
- what the first email should say
- what could go wrong
- what to do next

Weak section energy:

- fit model
- tactical notes
- strategic need
- axis comparison

Tables are for real comparisons. Callouts are for mental models, risks, and traps. Pull quotes are rare and should isolate a sentence worth remembering, not decorate an ordinary point.

End with what the reader should take forward. Then give a bridge: the next specific thing to read, build, verify, decide, or send.

## Visual Design

The page should feel like premium digital journalism: calm, readable, editorial, and built with care. Visual taste serves comprehension.

Default materials:

- static HTML, inline CSS, vanilla JS
- serif for narrative; mono for code and labels
- warm paper-and-ink or restrained editorial palettes
- no Inter, Roboto, Helvetica, purple/violet accents, gradient text, glowing/pulsing effects, or emoji
- header identity and theme toggle for substantial pages
- reading progress only for long reads

Choose one visual direction and commit. Variety matters, but it is subordinate to clarity.

Useful directions:

- Paper/ink
- Blueprint
- Forest paper
- Reykjavik winter
- Marrakech
- Kyoto twilight

## Visuals And Interaction

Every visual must earn its place. Use a diagram when it carries topology, simultaneity, causality, timing, or comparison better than prose. Do not draw a picture of a paragraph.

Use interaction only for progressive disclosure: stepping through time, revealing causality, comparing variants, or asking the reader to predict before reveal. Every widget should make sense before anyone touches it.

Keep JavaScript small. Vanilla first.

## Cold Read

Before shipping, read as a stranger:

- Does the opening work without the chat, notes, source file, or outline?
- Does the prose introduce referents before relying on them?
- Are memo words translated into reader words?
- Does every paragraph move the reader forward?
- Are claims sourced, measured, or clearly framed as judgment?
- Does each visual do work prose cannot do as well?
- Does the ending make the next step or takeaway clear?

If the page sounds impressive but a cold reader would feel behind, it failed.
