---
name: documentation-standards
description: Document new features and updates following the project documentation standards. Use when creating or updating documentation for features, significant refactors, complex business logic, project reports, defect tickets, or developer guides. Ensures proper directory structure, naming conventions, and consistent formatting across all document types. Triggers on requests to write docs, create a report, document a feature, write a ticket, or update project documentation.
---

# Documentation Standards

Create and maintain comprehensive documentation following the project's established directory structure, naming conventions, and formatting standards.

## Directory Structure

All documentation lives in `docs/` organized by purpose:

```
docs/
├── business/       # User-facing feature docs (audience: PMs, stakeholders, support)
├── technical/      # Implementation docs (audience: developers, DevOps)
├── reports/        # Observational docs: audits, status updates, retrospectives
├── guides/         # Prescriptive docs: plans, roadmaps, requirements, standards
└── tickets/        # Actionable defects and work items for developers to resolve
```

### What Goes Where

| Directory | Purpose | Audience | Examples |
|---|---|---|---|
| `business/` | User-facing features, workflows, business logic | PMs, stakeholders | `modal-component.md`, `navigation-system.md` |
| `technical/` | Architecture, implementation details, data flow | Developers, DevOps | `modal-implementation.md`, `design-tokens.md` |
| `reports/` | Audits, status updates, test results, retrospectives | All stakeholders | `dependency-audit-2026-03.md`, `sprint-3-status.md` |
| `guides/` | Plans, roadmaps, requirements, coding standards | Developers, agents | `project-brief.md`, `sprint-4-plan.md`, `requirements.md` |
| `tickets/` | Bug reports, defect tickets, work items | Developers | `bug-focus-trap-modal-2026-03.md`, `a11y-heading-hierarchy.md` |

## File Naming Conventions

All filenames use **lowercase kebab-case** within their directory:

| Directory | Pattern | Examples |
|---|---|---|
| `business/` | `[feature-name].md` | `modal-component.md`, `form-validation.md` |
| `technical/` | `[feature-name]-implementation.md` or `[topic].md` | `modal-implementation.md`, `shadow-dom-patterns.md` |
| `reports/` | `[topic]-[YYYY-MM].md` | `dependency-audit-2026-03.md`, `coverage-analysis-2026-03.md` |
| `guides/` | `[topic].md` | `project-brief.md`, `roadmap-q2-2026.md`, `coding-standards.md` |
| `tickets/` | `[type]-[description]-[YYYY-MM].md` | `bug-focus-trap-modal-2026-03.md` |

**Rules:**
- Date stamps use `YYYY-MM` format when the document is time-sensitive (reports, tickets)
- Technical docs for features use the `-implementation` suffix to distinguish from business docs
- No prefixes needed (the directory itself communicates the document type)

## Document Front Matter

Every document includes a YAML front matter block:

```markdown
---
title: Document Title
date: 2026-03-16
author: [agent-name or human author]
status: draft | active | archived
---
```

Additional fields by directory:

| Directory | Extra Fields |
|---|---|
| `tickets/` | `severity: critical / high / medium / low`, `component: [module]`, `assigned-to: [agent or role]` |
| `reports/` | `type: audit / status / retro / coverage / test-results` |
| `guides/` | `type: plan / roadmap / requirements / standards / adr` |

## When to Create Documentation

1. **New features** — any user-facing functionality or significant capability
2. **Significant refactors** — major architecture or implementation changes
3. **Complex business logic** — non-obvious rules, validations, or workflows
4. **API or component changes** — new public APIs, modified interfaces, breaking changes
5. **Bug discoveries** — defects found during testing (as tickets)
6. **Project milestones** — sprint plans, audits, status reports, retrospectives

## Documentation Workflow

### Step 1: Determine Document Type

- **Does this affect users or business processes?** → `business/`
- **Does this involve implementation details?** → `technical/`
- **Is this a finding, measurement, or status update?** → `reports/`
- **Is this a plan, standard, or requirement?** → `guides/`
- **Is this a defect or work item?** → `tickets/`
- **Multiple?** → Create a document in each relevant directory

### Step 2: Create or Update

**Create new** when adding a new feature, reporting new findings, or filing a new defect.

**Update existing** when enhancing a feature, changing behavior, or adding capabilities to a documented system.

### Step 3: Write Business Documentation

**Location:** `docs/business/[feature-name].md`

**Required sections:**

1. **Overview** — what the feature is (1-2 paragraphs)
2. **Business Purpose** — problem, solution, value
3. **User Workflows** — step-by-step user journeys
4. **Business Rules** — validation, access control, constraints
5. **Integration Points** — how the feature connects with others
6. **Success Metrics** — KPIs and measurement approach
7. **Future Enhancements** — planned improvements

### Step 4: Write Technical Documentation

**Location:** `docs/technical/[feature-name]-implementation.md`

**Required sections:**

1. **Architecture Overview** — high-level design
2. **Component Structure** — key components, custom elements, and their relationships
3. **Public API** — attributes, properties, methods, events
4. **Data Flow** — step-by-step operation flows
5. **Accessibility** — ARIA roles, keyboard navigation, screen reader behavior
6. **Performance Considerations** — optimization notes
7. **Testing Strategy** — how to test the feature
8. **Browser Support** — compatibility notes if relevant

### Step 5: Write Tickets

**Location:** `docs/tickets/[type]-[description]-[YYYY-MM].md`

**Required sections:**

1. **Summary** — one-sentence description
2. **Steps to Reproduce** — numbered steps
3. **Expected Behavior** — what should happen
4. **Actual Behavior** — what actually happens (include error output)
5. **Environment** — browser, OS, relevant dependencies
6. **Root Cause Analysis** — diagnosis based on source code
7. **Suggested Fix** — where to fix and what to change (do not write the fix)
8. **Related Tests** — link to failing test files
9. **Assigned To** — agent or team member

### Step 6: Update Existing Documentation

When updating docs, **integrate new information** rather than appending.

**Principles:**

- **Merge, don't duplicate** — update existing sections with new info
- **Preserve context** — keep relevant old information
- **Mark changes** — use version markers for significant updates
- **Deprecation** — strike through old content, note when deprecated

**Example — versioned workflow update:**

```markdown
## Create Component Workflow

**Current (v2.0+):**

1. Define custom element class extending HTMLElement
2. Create shadow DOM with template
3. Register observed attributes including new `variant` attribute (v2.0)
4. Define connectedCallback with slot handling

**Previous (v1.x):**

<details>
<summary>Original workflow without variants</summary>

1. Define custom element class extending HTMLElement
2. Create shadow DOM with template
3. Register observed attributes (no variant support)
</details>
```

## Documentation Quality Standards

### Clear and Concise

- Use simple language
- Avoid jargon unless necessary (then define it)
- One concept per paragraph
- Short sentences (prefer under 25 words)

### Structured and Scannable

- Use heading hierarchy (h2, h3, h4) — do not skip levels
- Bullet points for lists
- Code blocks with syntax highlighting
- Tables for comparisons
- Concrete examples for clarity

### Complete and Accurate

- Include all required sections for the document type
- Provide working code examples from the actual project
- Show both success and error cases
- Link to related documentation
- Keep documentation synchronized with code

### Maintained and Current

- Update when code changes
- Add version markers for significant updates
- Document deprecations clearly
- Review and archive stale documents

## Code Examples in Documentation

### Use Real, Working Code

```javascript
// ✅ Good — actual code from the project
class UBButton extends HTMLElement {
  static get observedAttributes() {
    return ['variant', 'disabled'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
    this.addEventListener('keydown', this._handleKeydown);
  }
}

// ❌ Bad — too simplified to be useful
class MyButton extends HTMLElement {
  // ... button logic
}
```

### Include Context

Show imports, type definitions, and necessary setup so examples are copy-pasteable:

```javascript
import { css, template } from '../utils/component-helpers.js';

const styles = css`
  :host {
    display: inline-flex;
    align-items: center;
    padding: var(--space-2) var(--space-4);
  }
  :host([disabled]) {
    opacity: 0.5;
    pointer-events: none;
  }
`;
```

### Annotate Key Lines

Add comments to explain important decisions:

```javascript
this.shadowRoot.adoptedStyleSheets = [styles]; // encapsulated — won't leak to light DOM
this.setAttribute('role', 'button'); // explicit ARIA for custom element
this.setAttribute('tabindex', '0'); // keyboard-focusable by default
```

## Related Skills

- **project-organization** — defines the broader project folder structure (where `docs/` sits alongside `src/`, `tests/`, config files, etc.). Use it when setting up a new project or deciding how the documentation directory fits into the overall repo layout.
