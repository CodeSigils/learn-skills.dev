---
name: drizzle-best-practices
description: Use this skill when writing or optimizing Drizzle ORM queries for performance (relations, transactions, batching, prepared statements, indexes, and avoiding N+1).
---

# Drizzle ORM Best Practices & Performance (Freelancerino)

Use this skill when optimizing Drizzle queries for correctness and performance. Always combine with tenant-isolation rules from `.github/skills/drizzle-tenant-queries/SKILL.md`.

## Golden rules

1. **Select only what you need** — reduces serialization, payload, and bandwidth.
2. **Parallelize independent reads** — `Promise.all` where queries don't depend on each other.
3. **Avoid N+1** — use relational queries (`with`) or `inArray` for batch lookups.
4. **Use prepared statements** for hot paths (repeated queries).
5. **Prefer cursor pagination** over offset for large datasets.
6. **Index hot columns** — `workspace_id`, foreign keys, timestamps, status.

## Relational queries (`db.query`)

Drizzle's relational queries usually emit a **single SQL statement** using lateral joins. This typically avoids N+1, but still validate payload size and query plans for deep nests.

### Setup

```ts
// Prefer using the project's canonical db instance:
//   import { db } from '@/db';

// If you need manual setup (e.g., a standalone script), match db/index.ts:
import 'server-only';

import { neon } from '@neondatabase/serverless';
import { drizzle } from 'drizzle-orm/neon-http';
import * as schema from '@/db/schema';

const sql = neon(process.env.DATABASE_URL!);
const db = drizzle(sql, { schema });
```

### Load related data in one query

```ts
// Single query with nested relations — no N+1
const invoices = await db.query.invoices.findMany({
  where: eq(invoices.workspaceId, workspaceId),
  with: {
    client: true,
    items: true,
  },
});
```

### Partial select (limit columns)

```ts
// Fetch only needed columns at DB level
const clients = await db.query.clients.findMany({
  where: eq(clients.workspaceId, workspaceId),
  columns: {
    id: true,
    name: true,
    // email, address, etc. excluded from query
  },
});
```

### Filter and limit nested relations

```ts
const projects = await db.query.projects.findMany({
  where: eq(projects.workspaceId, workspaceId),
  with: {
    timeEntries: {
      where: (entries, { gte }) => gte(entries.date, startDate),
      limit: 100,
      orderBy: (entries, { desc }) => [desc(entries.date)],
    },
  },
});
```

### Computed fields via `extras`

```ts
const clients = await db.query.clients.findMany({
  where: eq(clients.workspaceId, workspaceId),
  extras: {
    projectsCount: db.$count(projects, eq(projects.clientId, clients.id)),
  },
});
```

## Partial select (SQL builder)

Use when you need precise column control or custom expressions.

```ts
// Only fetch id and name
const result = await db
  .select({ id: users.id, name: users.name })
  .from(users)
  .where(eq(users.workspaceId, workspaceId));

// Exclude password using getTableColumns
import { getTableColumns } from 'drizzle-orm';
const { password, ...rest } = getTableColumns(users);
await db.select({ ...rest }).from(users);

// Dynamic/conditional select
async function selectClients(includeNotes: boolean) {
  return db
    .select({
      id: clients.id,
      name: clients.name,
      ...(includeNotes ? { notes: clients.notes } : {}),
    })
    .from(clients)
    .where(eq(clients.workspaceId, workspaceId));
}
```

## Batch operations

### Insert multiple rows

```ts
await db.insert(timeEntries).values([
  { workspaceId, projectId, date, durationMinutes: 60 },
  { workspaceId, projectId, date, durationMinutes: 90 },
  { workspaceId, projectId, date, durationMinutes: 45 },
]);
```

### Upsert (on conflict)

```ts
// Do nothing on conflict
await db
  .insert(settings)
  .values({ workspaceId, key: 'theme', value: 'dark' })
  .onConflictDoNothing({ target: [settings.workspaceId, settings.key] });

// Update on conflict
await db
  .insert(settings)
  .values({ workspaceId, key: 'theme', value: 'dark' })
  .onConflictDoUpdate({
    target: [settings.workspaceId, settings.key],
    set: { value: 'dark', updatedAt: new Date() },
  });
```

### Batch lookup with `inArray`

```ts
import { inArray } from 'drizzle-orm';

// ✅ Single query for batch IDs
const projectIds = [uuid1, uuid2, uuid3];
const rows = await db
  .select()
  .from(projects)
  .where(
    and(eq(projects.workspaceId, workspaceId), inArray(projects.id, projectIds))
  );
```

### `$count` helper

```ts
// Simple count
const total = await db.$count(clients, eq(clients.workspaceId, workspaceId));

// Count as subquery
const clientsWithProjects = await db
  .select({
    ...getTableColumns(clients),
    projectsCount: db.$count(projects, eq(projects.clientId, clients.id)),
  })
  .from(clients)
  .where(eq(clients.workspaceId, workspaceId));
```

## Transactions

Use transactions for multi-step mutations that must succeed or fail together.

> **⚠️ CRITICAL: Driver requirements for transactions**
>
> `db.transaction()` does **NOT** work with `drizzle-orm/neon-http` (HTTP is stateless).
>
> For interactive transactions, use `drizzle-orm/neon-serverless` with `Pool`:
>
> ```ts
> import { neonConfig, Pool } from '@neondatabase/serverless';
> import { drizzle } from 'drizzle-orm/neon-serverless';
>
> // Bun has native WebSocket - no 'ws' package needed
> neonConfig.webSocketConstructor = WebSocket;
>
> const pool = new Pool({ connectionString: process.env.DATABASE_URL! });
> const db = drizzle(pool, { schema });
> // Now db.transaction() works!
> ```
>
> See `tests/drizzle.transactions.integration.test.ts` for verified examples.

```ts
await db.transaction(async (tx) => {
  // All queries use the transaction connection
  await tx
    .update(invoices)
    .set({ status: 'finalized' })
    .where(
      and(eq(invoices.id, invoiceId), eq(invoices.workspaceId, workspaceId))
    );

  await tx.insert(invoiceSnapshots).values({
    invoiceId,
    workspaceId,
    snapshotData: JSON.stringify(snapshot),
  });
});
```

### Rollback on business logic failure

```ts
await db.transaction(async (tx) => {
  const [invoice] = await tx
    .select()
    .from(invoices)
    .where(
      and(eq(invoices.id, invoiceId), eq(invoices.workspaceId, workspaceId))
    );

  if (invoice.status === 'finalized') {
    tx.rollback(); // Throws, rolls back entire transaction
  }

  await tx.update(invoices).set({ status: 'finalized' }).where(...);
});
```

### Relational queries in transactions

```ts
await db.transaction(async (tx) => {
  const client = await tx.query.clients.findFirst({
    where: and(eq(clients.id, clientId), eq(clients.workspaceId, workspaceId)),
    with: { projects: true },
  });
  // ...
});
```

### Transaction isolation level (PostgreSQL)

```ts
await db.transaction(
  async (tx) => {
    /* ... */
  },
  {
    isolationLevel: 'serializable', // or 'read committed', 'repeatable read'
  }
);
```

## Prepared statements

For hot paths (e.g., lookups called many times), prepared statements avoid repeated query compilation.

Note: benefits depend on the driver. With the default `drizzle-orm/neon-http` (stateless HTTP), server-side prepare/cursor behavior may not apply the same way as pooled WebSocket/Node Postgres drivers. When in doubt, focus on reducing queries, selecting fewer columns, and adding indexes.

```ts
import { sql } from 'drizzle-orm';

// Prepare once at module level
const getClientById = db
  .select()
  .from(clients)
  .where(
    and(
      eq(clients.id, sql.placeholder('id')),
      eq(clients.workspaceId, sql.placeholder('workspaceId'))
    )
  )
  .prepare('get_client_by_id');

// Execute many times
const client = await getClientById.execute({ id: clientId, workspaceId });
```

### Prepared relational queries

```ts
import { placeholder } from 'drizzle-orm';

const getInvoiceWithItems = db.query.invoices
  .findFirst({
    where: (inv, { and, eq }) =>
      and(
        eq(inv.id, placeholder('id')),
        eq(inv.workspaceId, placeholder('workspaceId'))
      ),
    with: { items: true, client: true },
  })
  .prepare('invoice_with_items');

const invoice = await getInvoiceWithItems.execute({ id, workspaceId });
```

## Pagination

### Offset pagination (simple, fine for small data)

```ts
const page = 2;
const pageSize = 20;

await db
  .select()
  .from(timeEntries)
  .where(eq(timeEntries.workspaceId, workspaceId))
  .orderBy(desc(timeEntries.date))
  .limit(pageSize)
  .offset((page - 1) * pageSize);
```

### Cursor pagination (better for large data)

Offset pagination degrades as offset grows (scans all skipped rows). Cursor pagination scales better because it avoids large offsets.

```ts
// First page
const first = await db
  .select()
  .from(timeEntries)
  .where(eq(timeEntries.workspaceId, workspaceId))
  .orderBy(desc(timeEntries.date), desc(timeEntries.id))
  .limit(20);

// Next page using cursor (last row's date + id)
const cursor = first[first.length - 1];
const next = await db
  .select()
  .from(timeEntries)
  .where(
    and(
      eq(timeEntries.workspaceId, workspaceId),
      or(
        lt(timeEntries.date, cursor.date),
        and(eq(timeEntries.date, cursor.date), lt(timeEntries.id, cursor.id))
      )
    )
  )
  .orderBy(desc(timeEntries.date), desc(timeEntries.id))
  .limit(20);
```

## Indexes

Define indexes in schema for hot filters (workspace_id, FKs, timestamps, status).

```ts
import { pgTable, uuid, index, timestamp } from 'drizzle-orm/pg-core';

export const timeEntries = pgTable(
  'time_entries',
  {
    id: uuid('id').primaryKey().defaultRandom(),
    workspaceId: uuid('workspace_id').notNull(),
    projectId: uuid('project_id').notNull(),
    date: timestamp('date').notNull(),
    // ...
  },
  (table) => [
    index('time_entries_workspace_id_idx').on(table.workspaceId),
    index('time_entries_project_id_idx').on(table.projectId),
    index('time_entries_date_idx').on(table.date),
    // Composite for common query pattern
    index('time_entries_workspace_date_idx').on(table.workspaceId, table.date),
  ]
);
```

Validate migrations:

```bash
bun run db:generate
bun run db:migrate
```

## Iterator for large results (streaming)

For very large result sets, avoid loading all rows into memory:

Note: streaming/iterators may still materialize large results depending on driver/transport (especially with HTTP). Prefer cursor pagination + chunked processing for predictable memory usage.

```ts
const iterator = await db
  .select()
  .from(timeEntries)
  .where(eq(timeEntries.workspaceId, workspaceId))
  .iterator();

for await (const row of iterator) {
  processRow(row); // One row at a time
}
```

## Type inference

```ts
// Infer types from schema
type Client = typeof clients.$inferSelect;
type NewClient = typeof clients.$inferInsert;

// Or use utility types
import { InferSelectModel, InferInsertModel } from 'drizzle-orm';
type Client = InferSelectModel<typeof clients>;
type NewClient = InferInsertModel<typeof clients>;

// Partial for updates
type ClientUpdate = Partial<typeof clients.$inferInsert>;
```

## Anti-patterns (avoid)

| ❌ Don't                                | ✅ Do instead                                      |
| --------------------------------------- | -------------------------------------------------- |
| `for (...) await db.query...` (N+1)     | Use `with` relations or `inArray` batch            |
| `db.select().from(table)` (all columns) | Partial select: `{ id, name }` only needed fields  |
| Sequential independent reads            | `Promise.all([query1, query2])`                    |
| Large offset pagination                 | Cursor pagination for large datasets               |
| Rebuilding queries in hot loops         | Prepared statements                                |
| Ignoring nullable columns in results    | Handle `| null` types; use TypeScript strict mode  |
| `tx.rollback()` without catching        | Know it throws; let transaction wrapper handle     |
| Caching queries without tenant in key   | Always include `workspaceId` in cache keys         |

## Neon connection tips

- **HTTP driver** (`drizzle-orm/neon-http`): Best for single queries in serverless (faster cold starts).
- **WebSocket driver** (`drizzle-orm/neon-websockets`): Required for interactive transactions.
- Use pooled connection string from Neon console.

## Cost & performance notes

- Fewer queries = lower latency + lower cost on Vercel.
- Parallelization (`Promise.all`) reduces wall-clock time.
- Partial selects reduce serialization + network payload.
- Indexes prevent full table scans on large tables.
- Prepared statements eliminate repeated query parsing.

See also: `.github/skills/nextjs-cost-performance/SKILL.md`

## Validation

```bash
bun run lint
bun run typecheck
bun run test
bun run build
```

## References

- Drizzle docs: https://orm.drizzle.team/docs
- Relational queries: https://orm.drizzle.team/docs/rqb
- Query performance: https://orm.drizzle.team/docs/perf-queries
- Transactions: https://orm.drizzle.team/docs/transactions
- Schema: `db/schema.ts`
- Tenant isolation: `.github/skills/drizzle-tenant-queries/SKILL.md`
