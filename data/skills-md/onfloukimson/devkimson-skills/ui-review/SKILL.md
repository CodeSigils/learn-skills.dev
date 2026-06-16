---
name: ui-review
description: Review existing UI screens, components, screenshots, or frontend implementations and provide structured, prioritized visual feedback. Use for B2B SaaS, admin dashboards, developer tools, productivity tools, CRM/ERP, and internal tools when evaluating hierarchy, spacing, consistency, readability, responsive behavior, accessibility basics, calls to action, or UI states.
---

# UI Review

## When to Use This Skill

Use this skill when the user asks to review, audit, critique, or improve an existing interface. Accept screenshots, design files, rendered pages, component code, or a combination of these as evidence.

Do not redesign the product by default. Review the current interface first and preserve established product and design-system constraints. Generate implementation code only when the user explicitly asks for code changes.

## Inputs

Inspect the available artifacts and identify:

- target users and their primary task
- page or component purpose
- viewport sizes and responsive requirements
- existing design-system components and tokens
- product constraints, permissions, and important states

If business context is missing, state the minimum assumptions needed to complete the review.

## What to Inspect

Review each relevant area:

- **Visual hierarchy:** Confirm the page title, primary information, supporting information, and primary action have distinct emphasis.
- **Spacing and alignment:** Check container widths, grid alignment, repeated gaps, vertical rhythm, and edge alignment.
- **Component consistency:** Compare buttons, inputs, cards, tables, badges, icons, labels, borders, and interaction patterns.
- **CTA visibility:** Verify the primary action is easy to find, clearly labeled, and not competing with secondary actions.
- **Readability:** Check typography scale, line length, density, contrast, truncation, scanability, and content grouping.
- **Responsive layout:** Check stacking order, overflow, table behavior, touch targets, navigation, and action availability.
- **Accessibility basics:** Check semantic structure, visible focus, keyboard access, labels, contrast, and non-color status cues.
- **UI states:** Check empty, loading, error, success, disabled, and partial-data states.

## Decision Rules

1. Judge issues against the user's task, not personal aesthetic preference.
2. Treat blocked tasks, hidden primary actions, inaccessible controls, and missing error recovery as high priority.
3. Treat inconsistent patterns that recur across the product as system-level issues, not isolated cosmetic defects.
4. Prefer changes using existing React components, Tailwind tokens, shadcn/ui primitives, or Radix UI behavior.
5. Recommend a new component or token only when reuse cannot solve the issue or the pattern repeats.
6. Distinguish observed facts from assumptions. Cite the screen, region, component, or code path when possible.
7. Give concrete recommendations with expected user impact. Avoid comments such as "make it cleaner" or "improve hierarchy."
8. Preserve information density when expert users need it; improve grouping and scanability before removing data.
9. Evaluate desktop and mobile separately when responsive evidence is available.
10. Rank findings as `Critical`, `High`, `Medium`, or `Low`.

## Output Format

Use these headings in this order:

### Summary

State the interface purpose, overall assessment, evidence reviewed, and important assumptions.

### Strengths

List effective choices worth preserving. Tie each strength to usability or consistency.

### Issues

For each issue include:

- severity
- location
- observation
- user or business impact
- supporting evidence

### Recommendations

Map each recommendation to an issue. Describe the intended change and expected result without generating code unless requested.

### Priority Fixes

Provide the smallest ordered set of fixes with the highest impact. Separate immediate blockers from later polish.

## Anti-Patterns to Avoid

- Giving subjective feedback without evidence or user impact.
- Recommending a full redesign for localized issues.
- Focusing on color and polish while ignoring task completion.
- Inventing arbitrary spacing, colors, radii, or component variants.
- Removing useful density from data-heavy tools without understanding user frequency and expertise.
- Treating desktop screenshots as proof of responsive quality.
- Ignoring loading, empty, error, permission, or partial-data states.
- Reporting accessibility as compliant after only a visual inspection.
