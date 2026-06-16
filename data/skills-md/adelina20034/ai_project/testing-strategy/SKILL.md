---
name: testing-strategy
description: Create a testing plan tied to PRD acceptance criteria with a coverage matrix (AC→tests), deterministic fixtures/factories, and mocked externals. Use when adding tests for a feature/fix and ensuring every acceptance criterion is covered.
---

# Testing Strategy

## Inputs

- PRD acceptance criteria (`docs/prds/`)
- Design doc (`docs/architecture/`)
- Test conventions/commands (`PROJECT.md`)

## 1. Coverage Matrix

Create a table:

- Acceptance criterion → test type (unit/integration/e2e) → location → status

**Expected**: Every acceptance criterion has ≥1 test.

## 2. Choose Test Types

- Unit: pure logic
- Integration: API + DB + critical boundaries
- E2E: only critical happy paths + major regression risks

**Expected**: Minimal, reliable tests with maximum signal.

## 3. Determinism and Isolation

- Use factories/fixtures (no brittle hardcoded data).
- Mock external services (never call real APIs).
- Avoid time/network flakiness; control randomness.

**Expected**: Tests are deterministic, parallel-safe, CI-friendly.

## 4. Negative & Edge Coverage

- Validation errors
- Permissions/authz boundaries
- Empty states
- Partial failures (retries/idempotency if relevant)

**Expected**: Critical failure modes are covered.

## 5. Run Tests

Run the test commands from `PROJECT.md`.

**Expected**: All tests pass.

## 6. Summary Report

After running, provide:

### Passed Checks

- [ ] Coverage matrix complete
- [ ] External services mocked
- [ ] Tests deterministic
- [ ] Tests pass

### Gaps / Follow-ups

For each gap:
1. **Acceptance criterion**: ...
   - Missing test type: ...
   - Suggested test location: ...
   - Suggested fix: ...

