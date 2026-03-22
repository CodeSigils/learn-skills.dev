---
name: api-designer
description: Design RESTful APIs with clear endpoints, proper HTTP methods, and consistent response formats. Use when planning or building APIs.
---

# API Designer

You help design clean, consistent RESTful APIs.

## Steps

1. Identify the resources and their relationships.
2. Define endpoints using proper HTTP methods.
3. Design request/response schemas.
4. Document error handling.

## Conventions

### URL Structure

```
GET    /api/v1/users          # List users
POST   /api/v1/users          # Create user
GET    /api/v1/users/:id      # Get user
PUT    /api/v1/users/:id      # Update user
DELETE /api/v1/users/:id      # Delete user
```

### Response Format

```json
{
  "data": { ... },
  "meta": { "page": 1, "total": 100 }
}
```

### Error Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email is required",
    "details": [{ "field": "email", "reason": "required" }]
  }
}
```

## Rules

- Use plural nouns for resources: `/users` not `/user`.
- Use kebab-case for multi-word paths: `/user-profiles`.
- Use query params for filtering: `?status=active&sort=-created_at`.
- Return 201 for creation, 204 for deletion, 200 for everything else.
- Always include pagination for list endpoints.
