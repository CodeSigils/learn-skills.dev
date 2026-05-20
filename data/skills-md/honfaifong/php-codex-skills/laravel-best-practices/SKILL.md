---
name: laravel-best-practices
description: Write, review, and refactor Laravel code using established best practices for controllers, FormRequests, Eloquent, services or actions, authorization, Inertia, and tests.
---

# Laravel Best Practices Skill

Use this skill when the request is specifically about writing Laravel code cleanly, reviewing it against best practices, or tightening layering and tests.

## Goal

Keep Laravel code conventional, maintainable, and testable.

## Core rules

- Keep controllers thin and orchestration-focused.
- Move reusable or non-trivial validation to FormRequest classes.
- Use Policies or Gates for authorization.
- Keep business workflows in actions, services, jobs, or domain classes when that reduces controller sprawl.
- Prefer expressive Eloquent relationships, scopes, casts, and resources.
- Avoid queries in Blade views.
- Avoid `env()` outside config files.
- Add or update tests for changed behavior.

## Review checklist

- Is validation in the right boundary?
- Is authorization explicit?
- Is business logic misplaced in controllers, views, or models?
- Is there N+1 risk or poor eager loading?
- Are API responses or transforms duplicated?
- Does the change need feature tests, unit tests, or both?

## Inertia guidance

When the project uses Inertia:

- Prefer `useForm` for Inertia-driven forms.
- Use `Link` for internal navigation.
- Keep shared page data in the Inertia page context.
- Keep page components and feature components clearly separated.

## Output expectations

When completing a task with this skill:

- Name the Laravel best-practice rules applied.
- State whether behavior changed.
- Mention tests added or still needed.
- Call out follow-up refactors only when they are directly adjacent to the task.
