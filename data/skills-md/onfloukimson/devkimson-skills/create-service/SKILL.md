---
name: create-service
description: Use when creating or refactoring backend service-layer logic; requires business rules, incidents, transaction boundaries, idempotency, and verification review.
---

# Purpose

Reusable workflow for backend service implementation.

# Required Knowledge

- `ai-workspace/70-knowledge/company/`
- `ai-workspace/70-knowledge/teams/ai-agents/conventions.md`
- `ai-workspace/70-knowledge/domains/{domain}/business-rules.md`
- `ai-workspace/70-knowledge/domains/{domain}/edge-cases.md`
- `ai-workspace/70-knowledge/incidents/`

# Inputs

- service name or domain flow
- business rule
- persistence requirements
- transaction requirements
- external integration behavior
- verification expectation

# Workflow

1. Load required knowledge.
2. Validate business rule ownership.
3. Identify transaction, rollback, and idempotency requirements.
4. Check related incidents.
5. Implement the smallest service change.
6. Keep controller and persistence concerns separated when the project style supports it.
7. Add or update tests for success, failure, and edge cases.
8. Verify behavior.
9. Append logs if necessary.

# Safety Rules

- Never bury business rules in unrelated helper methods.
- Do not broaden transaction scope without reason.
- Consider duplicated execution, timeout, retry, and partial failure.
- Do not change persistence semantics without explicit task scope.

# Incident References

- Check incidents for duplicated processing, retry loops, reconnect duplication, and rollback failures.

# Output

- service implementation
- verification summary
- edge-case notes

# Verification

- Service behavior covered by tests or documented manual checks.
- Transaction and failure behavior reviewed.
- Related incidents checked or marked unavailable.
