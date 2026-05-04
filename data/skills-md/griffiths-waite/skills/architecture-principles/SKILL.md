---
name: architecture-principles
description: |
  Apply when making or reviewing architectural decisions, writing or reviewing Architecture
  Decision Records (ADRs), designing new systems, or defining non-functional requirements.
  Use this skill whenever someone is designing a system or component, reviewing a proposal
  for coupling or resilience, asking what NFRs to capture, or producing architecture
  documentation — even if they don't use the words "architecture principles".
  Covers: intentional decision recording, ADR creation and review, designing for change,
  NFRs as first-class concerns, and architecture accountability.
metadata:
  category: Architecture
  version: "1.0.0"
  source: principles
---

# Architecture Principles

Our engineering principles for making architectural decisions, recording them, and designing
systems that are resilient to change and grounded in business value.

## When to Apply

Apply this skill when:
- Making or reviewing a significant architectural decision
- Writing or reviewing an Architecture Decision Record (ADR)
- Designing a new system or reviewing an existing architecture
- Defining non-functional requirements (NFRs) for a system
- Reviewing whether a system is designed to accommodate change without costly rewrites
- Assessing whether architecture documentation is current and accessible

## Principles Overview

| Principle | Coverage | Reference |
|-----------|----------|-----------|
| Decisions Are Intentional and Recorded | Full guidance | `principles/decisions-are-intentional-and-recorded.md` |
| Design for Change, Not Certainty | Full guidance | `principles/design-for-change-not-certainty.md` |
| Non-Functional Requirements Are First Class | Full guidance | `principles/non-functional-requirements-are-first-class.md` |
| Architecture is a Collaborative Responsibility | Process reminder | See below |
| Architecture is Accountable Throughout | Process reminder | See below |
| Business Driven Architecture | Process reminder | See below |

## Quick Review Checklist

Use this for a fast adherence scan. Load individual principle files for detailed guidance.

### Decisions Are Intentional and Recorded
- [ ] Significant architecture decisions are documented with rationale and trade-offs
- [ ] Decision records are accessible, current, and version-controlled
- [ ] Superseded decisions are clearly marked and linked to their replacements

### Design for Change, Not Certainty
- [ ] Dependencies are loosely coupled and can be replaced without system-wide rewrites
- [ ] Abstractions are used at the right level — not too early, not too late

### Non-Functional Requirements Are First Class
- [ ] NFRs (performance, security, availability) are defined alongside functional requirements with agreed acceptance criteria
- [ ] NFRs are tracked and reviewed as part of delivery, not deferred to the end

## Process Reminders

The following principles are primarily about team culture, governance, or process. Surface these as awareness prompts rather than directly enforcing them in code.

> **Architecture is a Collaborative Responsibility**: Architecture decisions must be reached through open discussion with the people building and operating the systems — not designed in isolation and handed down.

> **Architecture is Accountable Throughout**: Architects remain engaged through delivery and into production, continuously validating the system against original intent and documenting any conscious deviations.

> **Business Driven Architecture**: Technology choices are made only where they create clear business value; trade-offs are framed in terms of business impact, not technical preference.

## How to Use

Load the relevant principle file when you need detailed guidance:

```
principles/decisions-are-intentional-and-recorded.md    — when writing or reviewing ADRs
principles/design-for-change-not-certainty.md           — when reviewing coupling, extensibility, or design flexibility
principles/non-functional-requirements-are-first-class.md — when defining or reviewing NFRs
```
