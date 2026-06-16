---
name: dashboard-designer
description: Design data-heavy admin and dashboard screens for B2B tools, including KPI cards, filters, search, tables, sorting, pagination, bulk actions, detail panels, status badges, useful charts, and complete UI states. Use for SaaS operations, CRM/ERP, developer tools, productivity products, and internal systems that must show what is happening, what needs attention, and what users can do next.
---

# Dashboard Designer

## When to Use This Skill

Use this skill when planning or substantially revising an operational dashboard, admin index, monitoring view, analytics overview, work queue, or other data-heavy screen.

Design the information architecture and interaction model before implementation. Generate code only when explicitly requested.

## Core Questions

Every dashboard must help the intended user answer:

1. What is happening?
2. What needs attention?
3. What can I do next?

Remove or demote elements that do not support these questions or a documented secondary task.

## Inputs

Identify:

- user role, decisions, and task frequency
- entities, metrics, statuses, and relationships
- freshness, latency, and source of the data
- action permissions and destructive operations
- expected row count, filter cardinality, and search behavior
- default time range and comparison period
- mobile, export, audit, and compliance requirements

State assumptions when metric definitions or business rules are missing. Do not invent authoritative KPI formulas.

## What to Design

- KPI cards and trend context
- global and local filters
- keyword search and query scope
- tables, column priority, sorting, and pagination
- row selection and bulk actions
- row actions and detail panels
- status badges and attention indicators
- charts only when they improve comparison, trend, composition, or anomaly detection
- empty, loading, error, stale, partial, no-result, and permission states

## Decision Rules

1. Begin with user decisions and actions, then select metrics and visualizations.
2. Show KPI cards only for metrics that change user understanding or action. Include label, value, time context, and comparison when meaningful.
3. Put the most frequently scanned or identifying columns first. Keep actions predictable and avoid excessive visible columns.
4. Use search for known-item retrieval and filters for attribute-based narrowing.
5. Keep applied filters visible, removable, and reflected in the result count. Provide a clear reset path.
6. Use server-side sorting, filtering, and pagination when data volume or freshness makes client-side behavior unreliable.
7. Preserve filters, sort, pagination, and selection when opening and closing contextual details.
8. Use bulk actions only for operations valid across the selected set. Show selection count and consequences.
9. Require stronger confirmation for destructive, external, costly, or difficult-to-reverse actions.
10. Use status badges with concise semantic labels and non-color cues. Limit the status vocabulary.
11. Use a chart when visual encoding answers a question faster than a table. Pair charts with exact values or accessible summaries.
12. Prefer a drawer for quick contextual detail and a dedicated page for deep investigation or editing.
13. Distinguish an empty dataset, no search results, unavailable data, stale data, and permission denial.
14. Show data freshness and timezone when recency affects decisions.
15. Keep the primary next action visible without turning every row or card into a competing CTA.

## Data Component Guidance

- **KPI cards:** Limit to the smallest useful set and order by decision importance.
- **Tables:** Define column purpose, formatting, sortability, truncation, responsive priority, and row actions.
- **Filters:** Separate high-frequency filters from advanced filters; use appropriate controls for cardinality.
- **Pagination:** Choose page-based navigation for stable browsing and cursor or incremental loading for large changing feeds.
- **Charts:** Specify the question, chart type, units, time range, comparison, tooltip content, and no-data behavior.
- **Detail panels:** Preserve list context and show the entity identity, status, key facts, history, and relevant actions.

## Output Format

Use these headings in this order:

### Dashboard Purpose

State the user, decisions, core questions, data freshness, and success criteria.

### Information Architecture

Describe metric priority, attention hierarchy, entity relationships, and reading order.

### Recommended Layout

Describe the application shell, KPI area, controls, data region, detail experience, and responsive behavior.

### Data Components

Specify cards, tables, charts, badges, pagination, and detail panels with the question each component answers.

### Actions and Controls

Specify search, filters, sorting, row actions, bulk actions, permissions, confirmation, and state preservation.

### States

Define loading, empty, no-result, error, partial, stale, permission, and success states with an appropriate next action.

### Implementation Notes

Document likely reusable components, token constraints, server/client responsibilities, accessibility needs, and unresolved data-contract questions. Do not include code unless requested.

## Anti-Patterns to Avoid

- Filling the top of the page with vanity metrics.
- Using charts as decoration or duplicating the same data in multiple forms.
- Showing every available column by default.
- Hiding active filters or changing results without feedback.
- Resetting list context after viewing a record.
- Placing destructive bulk actions beside harmless actions without distinction.
- Relying on color alone for status.
- Treating all missing-data states as one generic empty state.
- Using infinite scroll when users need stable position, selection, comparison, or auditability.
- Designing dense desktop tables with no narrow-screen strategy.
