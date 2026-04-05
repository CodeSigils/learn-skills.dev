---
name: drizzle-orm
description: Drizzle ORM query patterns for TypeScript. Use when writing, reviewing, or debugging Drizzle queries, especially when choosing between relational queries and the SQL builder, building dynamic filters, loading relations, or fixing Drizzle query-shape and type mismatches. Also apply during code review when a file contains non-trivial query construction with `drizzle-orm`.
---

# Drizzle ORM patterns

These patterns assume modern Drizzle projects using relational queries v2 (`db.query.*`) alongside the SQL builder. If the codebase is still on older relational query APIs, verify the installed Drizzle version before applying the examples below.

For formatting of relational queries and SQL builder chains, especially when a query mixes `columns`, `where`, and `with` or builder helpers like `.select()` and `.where()`, read [references/formatting.md](references/formatting.md). Use that layout consistently in generated examples and code review suggestions because deep Drizzle configs get hard to scan when everything is packed onto a few lines.

## Relational API vs SQL builder

Drizzle has two distinct query APIs. Choosing the wrong one causes TypeScript errors.

**Use the relational API** (`db.query.table.findFirst/findMany`) when:

- Fetching a single record or a simple list
- Loading nested relations in one query
- The filter conditions are known at compile time

**Use the SQL builder** (`db.select().from().where()`) when:

- Building WHERE conditions dynamically at runtime
- Running aggregations (`count()`, `sum()`, etc.)
- The query has joins that depend on runtime input

---

## Relational API

### In relational queries v2, `where` takes an object

```typescript
// ✅ Correct — object matching column names to values
const item = await db.query.items.findFirst({
  where: {
    id
  }
})

const category = await db.query.categories.findFirst({
  where: {
    slug
  }
})

const approved = await db.query.items.findMany({
  where: {
    status: 'approved'
  }
})

// ❌ Wrong in relational queries v2 — this causes a query-shape type mismatch
const item = await db.query.items.findFirst({
  where: eq(items.id, id)
})
```

Use `eq()` and similar helpers in SQL builder queries. In relational queries v2, `where` is an object that maps column names to expected values.

### Select only needed columns

```typescript
const brand = await db.query.brands.findFirst({
  columns: {
    id: true,
    name: true,
    slug: true
  }, // exclude updatedAt, createdAt, etc.

  where: {
    slug
  }
})
```

### Load nested relations with `with`

```typescript
const category = await db.query.categories.findFirst({
  columns: {
    id: true,
    name: true,
    slug: true
  },

  where: {
    slug
  },

  with: {
    properties: {
      columns: {
        id: true,
        name: true,
        dataType: true,
        unit: true
      },

      with: {
        enumOptions: {
          columns: {
            id: true,
            name: true,
            slug: true
          }
        }
      }
    }
  }
})
```

### Filter nested relations inside `with`

```typescript
const brand = await db.query.brands.findFirst({
  columns: {
    id: true,
    name: true,
    slug: true
  },

  where: {
    slug
  },

  with: {
    items: {
      columns: {
        id: true,
        name: true
      },

      where: {
        status: 'approved'
      }, // filter applied to the nested relation

      with: {
        category: {
          columns: {
            name: true,
            slug: true
          }
        }
      }
    }
  }
})
```

---

## SQL builder

### Dynamic WHERE conditions

Build conditions into an array, then spread into `and()`:

```typescript
import { and, eq, ilike } from 'drizzle-orm'

const conditions = [
  eq(items.status, 'approved')
]

if (categoryId) {
  conditions.push(eq(items.categoryId, categoryId))
}

if (search) {
  const escaped = search
    .replaceAll('%', String.raw`\%`)
    .replaceAll('_', String.raw`\_`)

  conditions.push(
    ilike(items.name, `%${escaped}%`)
  )
}

const results = await db
  .select({
    id: items.id,
    name: items.name
  })
  .from(items)
  .where(and(...conditions))
  .limit(limit)
  .offset((page - 1) * limit)
```

**Always escape user input** before passing to `ilike()` — `%` and `_` are wildcards in SQL LIKE patterns.

### Count query (aggregation)

`count()` returns exactly one row at runtime, but with `noUncheckedIndexedAccess` TypeScript still treats indexed access as possibly `undefined`. Avoid array destructuring here and read the first row safely.

```typescript
import { count } from 'drizzle-orm'

const countRows = await db
  .select({ total: count() })
  .from(items)
  .where(
    and(...conditions)
  )

const total = countRows[0]?.total ?? 0
```

### Parallel data + count queries

Run independent queries with `Promise.all` to avoid sequential round-trips.

> **Note:** `count()` always returns exactly one row but TypeScript (with `noUncheckedIndexedAccess`) sees array element access as `T | undefined`. Use `[0]?.total ?? 0` to stay type-safe.

```typescript
const [rows, countRows] = await Promise.all([
  db
    .select()
    .from(items)
    .where(
      and(...conditions)
    )
    .limit(limit)
    .offset(offset),

  db
    .select({ total: count() })
    .from(items)
    .where(
      and(...conditions)
    )
])

const total = countRows[0]?.total ?? 0

return {
  items: rows,
  total,
  page,
  limit
}
```

### Joins in the SQL builder

```typescript
import { eq } from 'drizzle-orm'

const results = await db
  .select({
    brandName: brands.name,
    id: items.id,
    name: items.name
  })
  .from(items)
  .innerJoin(brands, eq(items.brandId, brands.id))
  .where(
    eq(items.status, 'approved')
  )
```
