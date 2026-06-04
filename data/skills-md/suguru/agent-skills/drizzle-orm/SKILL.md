---
name: drizzle-orm
description: Build, migrate, debug, and review Drizzle ORM projects in TypeScript. Use when working with drizzle-orm or drizzle-kit schemas, migrations, configuration, database adapters, SQL-like queries, relational query API, transactions, seeds, validation schemas, serverless databases, or migrations to or from Drizzle.
---

# Drizzle ORM

Use this skill to make correct, type-safe Drizzle changes while protecting database state.

## Start

- Identify the dialect and runtime from `package.json`, Drizzle imports, `drizzle.config.*`, env names, and deployment target.
- Locate the moving parts with `rg "drizzle\\(|defineConfig|pgTable|mysqlTable|sqliteTable|relations\\("` and `rg --files -g '*drizzle*' -g '*schema*' -g 'migrations/**'`.
- Check installed `drizzle-orm` and `drizzle-kit` versions before picking syntax. If exact behavior matters, consult current official Drizzle docs before coding.
- Treat live database writes as externally visible. Do not run `drizzle-kit push`, `drizzle-kit migrate`, destructive SQL, seeds, or Studio against a nonlocal database without explicit confirmation.

## Choose The Workflow

- Schema, table, relation, enum, index, or generated type changes: read [schema-and-relations.md](references/schema-and-relations.md).
- Migration, introspection, `drizzle.config.*`, or CLI work: read [migrations-and-config.md](references/migrations-and-config.md).
- CRUD, joins, relational query API, transactions, prepared statements, or raw SQL: read [query-patterns.md](references/query-patterns.md).
- Driver, runtime, serverless, Next.js, edge, worker, or connection setup: read [adapters.md](references/adapters.md).

## Implementation Rules

- Prefer existing project patterns: schema file organization, column casing, migration folder, env loading, db singleton, relation naming, and driver.
- Import schema builders from the dialect-specific package and operators from `drizzle-orm`. Do not mix `pg-core`, `mysql-core`, and `sqlite-core` in the same table model.
- Use `typeof table.$inferInsert` and `typeof table.$inferSelect` or existing type aliases for row types instead of duplicating TypeScript interfaces.
- Preserve generated migrations. Do not edit old migrations unless the project already does so or the user explicitly asks for migration repair.
- Generate a new migration for schema changes, then review the SQL before applying it, especially for renames, drops, enum changes, default changes, and indexes.
- Use `relations()` for application-level relational queries. Keep `references()` or explicit foreign keys in table definitions when the database should enforce constraints.
- Prefer the SQL-like query builder for precise joins, aggregates, `returning`, and complex predicates. Prefer `db.query.*` relational queries for nested graph reads after `drizzle(client, { schema })`.
- Keep raw `sql` fragments typed and localized. Do not concatenate untrusted values into raw SQL; use Drizzle SQL templates and placeholders.

## Validation

- Run the narrowest available checks: typecheck, lint, and relevant tests.
- When config and database access are available, run non-destructive Drizzle checks such as `drizzle-kit check` or `drizzle-kit generate` and inspect the generated SQL.
- Apply migrations only to disposable or local databases unless the user confirms the target.
- If the repo has no validation scripts, at least run `tsc --noEmit` when TypeScript is configured, or report the gap.
