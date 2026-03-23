---
name: supabase-database
description: Manage Postgres databases, including diffing, dumping, pulling, and pushing schemas. Triggered by phrases like "diff database", "dump schema", "pull remote db", or "push database changes".
---

# Supabase Database Skill

## Goal
Manage the database schema and data operations.

## Instructions
1.  Identify the command needed based on user intent.
2.  Open the relevant rule file:
    - `supabase db diff` -> [.agent/rules/supabase/commands/db/diff.md](../../rules/supabase/commands/db/diff.md)
    - `supabase db dump` -> [.agent/rules/supabase/commands/db/dump.md](../../rules/supabase/commands/db/dump.md)
    - `supabase db pull` -> [.agent/rules/supabase/commands/db/pull.md](../../rules/supabase/commands/db/pull.md)
    - `supabase db push` -> [.agent/rules/supabase/commands/db/push.md](../../rules/supabase/commands/db/push.md)
    - `supabase db reset` -> [.agent/rules/supabase/commands/db/reset.md](../../rules/supabase/commands/db/reset.md)
3.  Check [00_global_policy.md](../../rules/supabase/00_global_policy.md) for destructive operation safety gates (especially for `db reset`).
4.  Ensure the project is correctly linked before running `pull` or `push`.

## Examples
- "Compare local schema with remote" -> Use `supabase db diff`
- "Pull latest changes from production" -> Use `supabase db pull`
- "Export local database content" -> Use `supabase db dump`
