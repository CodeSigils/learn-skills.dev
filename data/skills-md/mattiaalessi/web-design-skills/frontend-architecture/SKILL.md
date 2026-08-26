---
name: frontend-architecture
description: "Design and implement a maintainable frontend architecture for professional websites: stack choice, routing, rendering, components, data, forms, errors, state, dependencies, security boundaries, and responsive behavior. Use before substantial implementation."
version: 1.0.0
---

# Frontend Architecture

Choose the smallest architecture that satisfies the product blueprint. Do not add a framework, animation library, state manager, or client-side data layer because it is familiar. Every dependency must have a reason, owner, version policy, and removal cost.

## Architecture decision record

Before coding, record:

- framework and version;
- rendering model: static, server-rendered, hybrid, or client-rendered;
- routing and canonical URL strategy;
- data sources and source-of-truth boundaries;
- CMS/API/authentication integrations;
- styling and design-token strategy;
- form and validation approach;
- error, loading, empty, offline, and permission behavior;
- caching and revalidation rules;
- image, font, and asset pipeline;
- testing tools and quality gates;
- deployment target and environment model.

Prefer server/static rendering for public content. Isolate client interactivity to the smallest component that needs state, effects, browser APIs, or event handlers.

## Project structure

Organise by product boundaries rather than arbitrary file type when the project is large enough:

- routes/pages;
- shared layout and navigation;
- design system primitives;
- feature components;
- data access and schemas;
- integrations;
- utilities;
- tests and fixtures;
- configuration and deployment.

Keep domain logic out of presentational components. Keep secrets and privileged calls server-side. Define public versus private environment variables explicitly.

## Component contracts

Every reusable component should document:

- purpose and semantic element;
- typed props and defaults;
- controlled/uncontrolled behavior;
- loading, empty, error, disabled, and permission states;
- keyboard behavior and focus rules;
- responsive behavior;
- analytics events, if any;
- visual reference and design tokens used.

Do not create a component solely to wrap one element unless it establishes a meaningful contract.

## Data and forms

- Validate untrusted data at the boundary with a schema.
- Keep server authorization independent of client visibility.
- Use explicit request states: idle, loading, success, empty, validation error, authorization error, network error, timeout, and retrying.
- Prevent duplicate submissions and preserve user input after recoverable errors.
- Associate every field with a label, instructions, constraints, and error message.
- Never expose API keys, tokens, internal IDs, stack traces, or sensitive data to the client unnecessarily.

## Rendering and performance

- Fetch independent data in parallel.
- Avoid client waterfalls for public content.
- Reserve image dimensions and use responsive sources.
- Load only required font weights.
- Lazy-load below-fold heavy media and optional integrations.
- Split code only when the saved payload exceeds the overhead.
- Animate with the rules in `motion-system.md`.

## Resilience

Define behavior for:

- API timeout and rate limit;
- third-party outage;
- stale or malformed CMS content;
- missing image or translation;
- no search results;
- expired event or offer;
- browser without a modern feature;
- JavaScript disabled where a public task should remain accessible.

Every external integration needs a user-facing fallback and an owner for monitoring.

## Code quality

Use strict typing where the language supports it, linting, formatting, dependency lockfiles, meaningful names, small pure utilities, and reviewable commits. Do not suppress errors without a documented reason. Keep generated code and hand-written code distinguishable when that helps maintenance.

## Handoff

Pass architecture decisions to `cms-integrations`, `web-accessibility`, `web-seo-performance`, `web-privacy-security`, `qa-release`, and `deploy-operations`.
