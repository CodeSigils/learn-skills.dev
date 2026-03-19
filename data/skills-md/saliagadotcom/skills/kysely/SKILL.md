---
name: kysely
description: "Kysely type-safe SQL query builder for TypeScript — start here for type system, database interface setup, or when unsure which Kysely sub-skill to use."
---

# Kysely

Type-safe TypeScript SQL query builder with zero runtime overhead. Immutable builders, full autocompletion, and compile-time error detection.

## Sub-Skill Routing

| Need | Load Skill | Trigger Phrases |
|------|-----------|----------------|
| SELECT, joins, where, expressions, aggregates | `kysely-querying` | selectFrom, innerJoin, eb(), fn.count, where, having |
| INSERT, UPDATE, DELETE, upserts, transactions | `kysely-writes-transactions` | insertInto, updateTable, deleteFrom, onConflict, transaction, savepoint |
| Schema DDL, migrations, Migrator setup | `kysely-schema-migrations` | createTable, addColumn, Migrator, FileMigrationProvider, migration |
| Cross-dialect portability, feature detection | `kysely-dialect-portability` | PostgresDialect, MysqlDialect, supportsReturning, jsonArrayFrom, plugin |
| CTEs, window functions, raw SQL, streaming | `kysely-advanced-sql` | with(), sql\`\`, DynamicModule, CASE, over(), stream, CTE |

**Load the specific sub-skill** for detailed patterns and examples. This router skill covers the mental model, type system, and non-negotiable rules.

## Mental Model

```
Kysely<DB>                               ← one instance per database
  ├── .selectFrom() / .insertInto() ...  ← returns immutable query builder
  ├── .schema                            ← returns SchemaModule for DDL
  ├── .fn                                ← FunctionModule for aggregates
  ├── .dynamic                           ← DynamicModule for runtime refs
  ├── .transaction()                     ← callback-based (auto-commit/rollback)
  ├── .startTransaction()                ← controlled (manual commit/rollback)
  └── .destroy()                         ← close connection pool
```

**Every builder method returns a new immutable instance.** You must capture the return value:

```ts
// ✅ Correct
let query = db.selectFrom('person').selectAll()
if (filter) query = query.where('age', '>', 18)

// ❌ Wrong — result is discarded
const query = db.selectFrom('person').selectAll()
query.where('age', '>', 18)  // returns new builder, original unchanged
```

## Architecture

```
User code → QueryCreator → OperationNode AST
  → plugins.transformQuery() → QueryCompiler → SQL + params
  → ConnectionProvider → Driver → DB
  → plugins.transformResult() → typed result
```

## Type System Quick Reference

See [reference/type-system.md](reference/type-system.md) for the full guide.

### Database Interface

```ts
import { type Generated, type ColumnType, Kysely } from 'kysely'

interface PersonTable {
  id: Generated<number>                    // optional on insert, required on select
  first_name: string                       // required everywhere
  last_name: string | null                 // nullable
  created_at: ColumnType<Date, string | undefined, never>  // Date on select, optional string on insert, excluded from update
}

interface Database {
  person: PersonTable   // key = exact SQL table name
}

const db = new Kysely<Database>({ dialect })
```

### ColumnType Decision Tree

| Column behavior | Type to use |
|----------------|-------------|
| Same type everywhere | `string`, `number`, etc. |
| DB-generated default (auto-increment, UUID, NOW()) | `Generated<T>` |
| Always DB-generated, never set manually | `GeneratedAlways<T>` |
| Different types per operation | `ColumnType<SelectType, InsertType, UpdateType>` |
| JSON column (parsed on select, string on write) | `JSONColumnType<ParsedType>` |
| Nullable column | `T | null` |

### Row Type Extraction

```ts
import { type Selectable, type Insertable, type Updateable } from 'kysely'

type Person = Selectable<PersonTable>           // { id: number, first_name: string, ... }
type NewPerson = Insertable<PersonTable>        // { id?: number, first_name: string, ... }
type PersonUpdate = Updateable<PersonTable>     // { id?: number, first_name?: string, ... }
```

## Non-Negotiable Rules

1. **Always call `.execute()`** — builders are inert until executed
2. **Capture builder returns** — methods return new instances, never mutate
3. **Use `Kysely<any>` in migrations** — never reference your current DB interface
4. **Call `db.destroy()` on shutdown** — releases connection pool
5. **Use `eb()` callbacks for complex expressions** — not string concatenation
6. **Validate dynamic input** — `sql.ref()`, `sql.table()`, `sql.id()` do NOT escape; whitelist user input
7. **Use `returning()`/`returningAll()` on Postgres/SQLite** — not available on MySQL (use separate SELECT)
8. **Pass values as parameters** — `sql\`col = ${val}\`` auto-parameterizes; never use `sql.raw()` with user data

## Query Terminators

| Method | Returns | Use when |
|--------|---------|----------|
| `.execute()` | `T[]` | Need all rows |
| `.executeTakeFirst()` | `T \| undefined` | Expect 0–1 rows |
| `.executeTakeFirstOrThrow()` | `T` | Must have exactly 1 row |
| `.stream(chunkSize?)` | `AsyncIterableIterator<T>` | Large result sets |
| `.compile()` | `{ sql, parameters }` | Inspect SQL without executing |

## Common Patterns

### Repository Function

```ts
async function findPersonById(db: Kysely<Database>, id: number) {
  return db
    .selectFrom('person')
    .where('id', '=', id)
    .selectAll()
    .executeTakeFirst()
}
```

### Conditional Queries with $if

```ts
db.selectFrom('person')
  .selectAll()
  .$if(nameFilter != null, (qb) => qb.where('first_name', '=', nameFilter!))
  .execute()
```

### Transaction (Callback)

```ts
await db.transaction().execute(async (trx) => {
  await trx.insertInto('person').values(data).execute()
  await trx.updateTable('audit').set({ updated: true }).execute()
})
```
