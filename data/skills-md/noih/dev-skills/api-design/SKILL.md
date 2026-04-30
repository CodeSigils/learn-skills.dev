---
name: api-design
description: API design conventions and best practices. Use when designing REST API endpoints, defining response shapes, planning pagination, or making API architecture decisions.
user-invocable: false
---

# API Design Conventions

## Naming Conventions

- **URL paths**: Plural nouns, kebab-case (`/user-profiles/:id/addresses`). Use nouns for resources, verbs only for actions (`/orders/:id/cancel`).
- **JSON fields**: Follow the project's language convention — `camelCase` for JS/TS, `snake_case` for Rust/Go. Be consistent within a project.
- **Query parameters**: Use kebab-case (`/api/v1/products?type=voucher&category=digital-points`). Do NOT use camelCase, snake_case, or other conventions for query filter names — always kebab-case.

## Consumer-Driven Design

Design APIs based on how consumers use the data. When page references are available (Figma, live URL via chrome-devtools MCP, or frontend source code), study the page structure first and let it guide your API shape. When no page reference is available, reason from the requirements about what data each use case needs.

## Endpoint Granularity

**List vs Detail separation**: If the feature involves browsing items and viewing individual ones, split into list and detail endpoints. The list endpoint returns only the fields the list view needs (e.g., id, title, thumbnail, summary). The detail endpoint returns the full resource. Never return all detail fields in a list response.

**Single purpose**: Each endpoint should serve one clear purpose. Avoid god endpoints that accept many optional parameters and behave differently based on parameter combinations — split them into semantically distinct endpoints.

**Performance-driven splitting**: Don't mix cheap and expensive operations. If a list page shows aggregate stats (counts, sums) that are expensive to compute, expose them as a separate stats endpoint so the client can fetch them in parallel without blocking the list.

## List Endpoints

- **Pagination**: Prefer cursor-based pagination over page-number offset. Cursor-based is more stable under concurrent writes and scales better. Use offset-based only when the UI explicitly requires jumping to arbitrary page numbers.
- **Filtering**: Consider what filters the list page needs — keyword search, status, category, date range, etc. Design query parameters accordingly.
- **Sorting**: Support sort field and direction (e.g., `sort=created_at&order=desc`). Default to a sensible sort order based on the use case.

### Pagination Response Format

```json
{
  "list": [],
  "hasNext": true,
  "anchor": "eyJpZCI6MTAwfQ"
}
```

- **list**: Array of items (`<T>[]`)
- **hasNext**: Whether more items exist after the current page
- **anchor**: Opaque cursor string for the next page. `null` when no more pages.
- **total**: Do NOT include by default — computing total count is expensive (`COUNT(*)` on large tables). Only add when the UI explicitly requires it (e.g., "showing 1-20 of 1,234 results").

## Action-Oriented Writes

Write operations should reflect business actions, not just CRUD mappings. When the operation has clear domain semantics, use an action endpoint:
- `POST /orders/:id/cancel` over `PATCH /orders/:id { status: 'cancelled' }`
- Action endpoints encapsulate validation, side effects, and business rules in one place.

## Idempotency

- **GET, PUT, DELETE** are idempotent by spec — repeating them produces the same result.
- **POST** is NOT idempotent. For critical writes (payments, orders), require an `Idempotency-Key` header. The server stores the key and returns the cached response on retries, preventing double-submit.
- Action endpoints (`POST /orders/:id/cancel`) are naturally idempotent if the action is a state transition — cancelling an already-cancelled order is a no-op, not an error.

## Resource Structure

- **Nested vs flat**: Use nested routes (`/users/:id/addresses`) for strong ownership. Use flat routes with query params (`/posts?author-id=:id`) for cross-cutting queries. Avoid nesting beyond two levels.
- **Response shape**: Never expose the DB model directly as the API response. Compose a response DTO with only the fields the consumer needs, hiding internal implementation details.

## Error Responses

Follow the project's existing error format. If none exists, use a flat structure:

```json
{
  "code": "0x0001",
  "name": "VALIDATION_ERROR",
  "message": "Email format is invalid",
  "details": [
    { "field": "email", "message": "must be a valid email address" }
  ]
}
```

- **code**: Hex error code (`0x0000`, `0x0001`, ...) for programmatic matching
- **name**: Human-readable error identifier for debugging
- **message**: User-facing description
- **details**: Optional array for field-level validation errors

Rules:
- **Production**: Never leak stack traces, internal paths, or SQL errors to clients
- **Development**: Include internal error details (stack trace, query, context) to aid debugging
- Use `details` array for validation errors — one entry per invalid field
- Keep `message` actionable — tell the user what to fix, not what went wrong internally

## HTTP Status Codes

Use status codes correctly — don't default everything to 200 or 400.

**Success:**
- `200` — OK (GET, PUT, PATCH, DELETE with response body)
- `201` — Created (POST that creates a resource)
- `204` — No Content (DELETE or action with no response body)

**Client errors:**
- `400` — Bad Request (malformed syntax, invalid JSON)
- `401` — Unauthorized (missing or invalid authentication)
- `403` — Forbidden (authenticated but insufficient permissions)
- `404` — Not Found (resource doesn't exist)
- `409` — Conflict (duplicate creation, invalid state transition)
- `422` — Unprocessable Entity (valid syntax but failed validation — prefer over 400 for validation errors)

**Server errors:**
- `500` — Internal Server Error (unexpected failure — never intentionally return this)
- `502` — Bad Gateway (upstream service returned an invalid response — e.g., calling GCP Storage or a payment gateway that errors out)
- `503` — Service Unavailable (server temporarily unable to handle requests — dependency down, overloaded). Use `Retry-After` header when possible.

## Timestamps

Use Unix epoch milliseconds (13 digits) for all timestamp fields. This keeps the wire format timezone-neutral, compact, and easy for common clients to parse.

```json
{
  "createdAt": 1709472000000,
  "updatedAt": 1709558400000
}
```

Store as UTC. Timezone display is the frontend's responsibility.

## Null Handling

- **`null`** — field is present, value is empty. Use for optional fields that have no value.
- **field omitted** — field does not exist in the response. Use for fields that are not applicable in this context (e.g., a field that only appears in the detail endpoint, not in the list endpoint).

For **PATCH** requests:
- Sending `null` means "clear this field"
- Omitting the field means "don't change this field"

See language skills for serialization behavior that affects `null` vs omitted fields.

## Async Operations

For long-running tasks (video transcoding, report generation, bulk imports), don't block the request:

1. **Accept**: Return `202 Accepted` immediately with a task reference
```json
{
  "taskId": "task_abc123",
  "status": "pending",
  "statusUrl": "/tasks/task_abc123"
}
```

2. **Poll**: Client polls the status endpoint until completion
```
GET /tasks/task_abc123
→ { "status": "processing", "progress": 65 }
→ { "status": "completed", "result": { ... } }
→ { "status": "failed", "error": { ... } }
```

Use polling for simplicity. If the project already has WebSocket or webhook infrastructure, those are valid alternatives for push-based notification.

## Versioning

Use URL path versioning (`/v1/users`) when breaking changes are unavoidable. For internal APIs consumed by your own frontend, versioning is usually unnecessary — just update both sides together. Reserve versioning for public/partner APIs with external consumers you can't coordinate with.

## Data Values

All stored data values (enum keys, category codes, status strings, type identifiers) must be in English. Never store display text or translated strings as data values. Translation is the frontend's responsibility — the frontend maps English keys to localized strings via i18n or a key-label mapping.
