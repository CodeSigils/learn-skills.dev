---
name: multi-tenant
description: >
  Design multi-tenant Cloudflare applications with tenant isolation, D1 row/database boundaries, Durable Object-per-tenant patterns, R2 key prefixes, KV cache keys, authz, noisy-neighbor controls, and migration paths. Use for SaaS and platform code.
compatibility: "Cloudflare Workers TypeScript projects using Wrangler; verify current Cloudflare APIs, limits, and pricing before production use."
metadata:
  source: "Architecting on Cloudflare plus official Cloudflare Developer Platform docs"
  generated: "2026-04-28"
---
# Multi-Tenant Design

Use this skill when building SaaS or any application serving multiple tenants, workspaces, organizations, or customers.

## Isolation ladder

Choose the lowest isolation level that satisfies security, compliance, scale, and operational needs.

1. **Row-level isolation**: shared D1/database tables with `tenant_id` on every row.
2. **Schema/table/database per tenant group**: stronger blast-radius control and data movement options.
3. **Durable Object per tenant/entity**: serialized coordination and private per-object state.
4. **Separate buckets/namespaces/resources**: higher isolation and operational overhead.
5. **Separate Workers/accounts/platform model**: strongest isolation, highest management complexity.

## Mandatory tenant rules

- Every request must resolve a principal with `tenantId` before data access.
- Every D1 table that stores tenant data must include `tenant_id` unless physically isolated.
- Every query must include a tenant predicate or use a tenant-specific database/binding.
- Every R2 key should include a tenant prefix or tenant-isolated bucket.
- Every KV key must include tenant and schema/version dimensions.
- Durable Object names should include tenant ID for tenant-scoped coordination.

## D1 query pattern

```ts
async function getProject(env: Env, tenantId: string, projectId: string) {
  return env.DB.prepare(
    `SELECT id, tenant_id, name, created_at
     FROM projects
     WHERE tenant_id = ? AND id = ?`
  ).bind(tenantId, projectId).first<Project>();
}
```

## R2 key pattern

```ts
const key = `tenants/${tenantId}/files/${fileId}`;
```

## Durable Object key pattern

```ts
const object = env.TENANT_COORDINATOR.getByName(`tenant:${tenantId}`);
```

## Noisy-neighbor controls

- Rate-limit by tenant and user.
- Partition Durable Objects by entity, not just tenant, if a tenant can be very large.
- Track per-tenant storage, queue, workflow, and AI usage.
- Add quotas before enterprise customers demand them.
- Use separate resources for large/high-compliance tenants when required.

## Review checklist

- [ ] Tenant ID is derived from authenticated identity, not trusted from request body.
- [ ] All D1 queries include tenant scope.
- [ ] Cache keys include tenant scope.
- [ ] R2 object access checks metadata/DB authorization before download.
- [ ] Queue messages include tenant ID and are validated.
- [ ] AI prompts/retrieval cannot include another tenant's data.
- [ ] Logs avoid cross-tenant sensitive data leakage.

## Anti-patterns

- Frontend hides other tenants but backend queries do not scope by tenant.
- KV key `settings` shared across all tenants.
- R2 object key generated from user-supplied filename only.
- Agent or AI tool can search across tenants without hard filters.
- One Durable Object serializes all tenants.
