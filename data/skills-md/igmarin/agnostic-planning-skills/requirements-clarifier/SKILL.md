---
name: requirements-clarifier
type: atomic
license: MIT
description: Transform vague task descriptions into actionable specifications with user stories, acceptance criteria, and identified edge cases — NEVER write implementation code. Output requirements only. Use when clarifying, defining scope, refining vague requests.
metadata:
  version: 1.0.0
  user-invocable: "true"
  output: Clarified requirements with user stories, acceptance criteria, edge cases, open questions
  constraints: "NO CODE — produces requirements only."
---
# Requirements Clarifier

Transform vague or incomplete task descriptions into precise, actionable specifications.

## HARD-GATE
- No code, no implementation, no editing of files.
- Output clarified requirements as structured text.
- If asked for implementation, respond: "I produce requirements, not code."

## Core Process
1. Analyze the request — identify what is stated, implied, and missing.
2. Ask clarifying questions about:
   - Target users, success criteria, dependencies, constraints, out-of-scope boundaries.
3. Structure output using template:

```markdown
## Clarified Requirements

### Summary
One-paragraph synthesis.

### Scope
**In scope:** bullet list.
**Out of scope:** bullet list.

### User Stories
- As a [user], I want [goal] so that [benefit]. *(Priority: P0/P1/P2)*

### Acceptance Criteria
**Story: [title]**
- [ ] Given [context] when [action] then [expected result]

### Edge Cases & Constraints
- Technical, business, behavioral.

### Open Questions
1. …
```

4. Validate: can an engineer build it? can QA write tests? are at least 3 edge cases identified?

## Guidelines
- Use testable, verifiable acceptance criteria (Given/When/Then).
- State what is out of scope clearly.
- Identify at least 3 edge cases.
- No implementation details.

## Integration
- **create-prd** after clarification
- **product-owner** persona for discovery phase
