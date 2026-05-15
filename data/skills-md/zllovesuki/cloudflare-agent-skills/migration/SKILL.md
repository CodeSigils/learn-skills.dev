---
name: migration
description: >
  Plan incremental migrations to Cloudflare from AWS, Azure, GCP, server-based apps, or existing databases using strangler patterns, service boundaries, R2 offload, Workers frontdoors, Hyperdrive, queues, workflows, shadow reads, rollback, and observability.
compatibility: "Cloudflare Workers TypeScript projects using Wrangler; verify current Cloudflare APIs, limits, and pricing before production use."
metadata:
  source: "Architecting on Cloudflare plus official Cloudflare Developer Platform docs"
  generated: "2026-04-28"
---
# Migration

Use this skill when moving an existing application or subsystem to Cloudflare.

## Migration stance

- Migrate incrementally and reversibly.
- Establish baselines before moving traffic.
- Do not rewrite everything just to match Cloudflare primitives.
- Use Workers as a frontdoor/strangler when it reduces risk.
- Keep the old system and new system observable during coexistence.

## Baseline first

Capture before migration:

- Request volume and routes.
- Latency percentiles.
- Error rates.
- CPU/memory and database load.
- Storage/egress costs.
- Top user flows.
- Operational pain points.

## Migration patterns

### Worker frontdoor

```text
Client -> Worker
  -> route migrated paths to Cloudflare-native code
  -> proxy unmigrated paths to existing origin
```

Use for gradual route-level migration, auth normalization, caching, and observability.

### R2 offload

```text
Existing app metadata remains in old DB
Worker handles upload/download
R2 stores blobs
Existing app receives R2 object keys
```

Good first migration when egress/blob cost is high.

### Hyperdrive coexistence

```text
Worker -> Hyperdrive -> existing Postgres/MySQL
```

Use when business data must stay in the existing database while edge routes move first.

### Async extraction

```text
Existing synchronous operation
  -> Worker validates request
  -> Queue/Workflow performs background steps
  -> D1/R2 stores job status/result
```

Use for exports, imports, notifications, AI pipelines.

## Shadow and cutover

- Shadow reads: compare Cloudflare result to old system without serving it.
- Shadow writes: write to new system for validation only, with clear conflict rules.
- Dual writes are risky; use idempotency and reconciliation.
- Cut over by route, tenant, or feature flag.
- Keep rollback path for each cutover unit.

## Migration plan template

```markdown
## Migration unit
- Scope:
- Existing owner/source of truth:
- New Cloudflare primitives:
- Baseline metrics:
- Data migration/backfill:
- Shadow validation:
- Cutover trigger:
- Rollback plan:
- Observability:
```

## Anti-patterns

- Big-bang rewrite with no coexistence.
- Moving database and application logic simultaneously without validation.
- No rollback because the old path was removed too early.
- Recreating cloud-specific services one-for-one instead of rethinking primitives.
- Migrating an unsuitable workload despite hard platform constraints.
