---
name: grill-me
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me".
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time.

If a question can be answered by exploring the codebase, explore the codebase instead.

When we have worked through all branches and reached shared understanding, close the session by emitting a structured summary block in this exact format:

<!-- GRILL-SUMMARY-START -->
**Problem statement:** <one-sentence description of the problem being solved>

**Proposed solution:** <one-paragraph description of the agreed approach>

**Key decisions:**
- <decision and rationale>
- <decision and rationale>

**Open questions:**
- <any unresolved questions, or "None" if all were resolved>
<!-- GRILL-SUMMARY-END -->
