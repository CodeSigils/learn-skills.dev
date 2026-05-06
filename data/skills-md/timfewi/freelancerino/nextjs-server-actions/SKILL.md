---
name: nextjs-server-actions
description: Use this skill when you implement or review Next.js 16 Server Actions or server-side data fetching that touches workspace data (Clerk + Drizzle + next-intl, tenant-safe).
---

# Server Actions & Data Fetch Skill (Freelancerino)

Use this skill whenever you add or review server actions, server components fetching data, or route handlers that touch workspace data. Optimized for Next.js 16 + React 19 + TypeScript + Clerk + Drizzle.

## Core rules

- Tenancy is solo MVP: derive workspace from Clerk user; never trust client-provided IDs. Every query **must** filter by `workspace_id`.
- Server Actions only for internal mutations. Route Handlers only for webhooks/external. Keep secrets server-side.
- Money stored as integer cents + currency code. Time stored in UTC.
- i18n: URLs are `/{locale}/...` (en|de). Use next-intl for formatting.

## Required steps for any mutation

1. "use server" at top. Import `auth` from `@clerk/nextjs/server` and `requireWorkspaceCached()` from `@/lib/workspace`.
2. Auth check: `const { workspace, userId } = await requireWorkspaceCached();`
3. Validate inputs (zod or guards). Reject unexpected fields; prefer typed inputs.
4. Perform Drizzle query with `workspace.id` in `where` clause. Never query unscoped tables.
5. Revalidate relevant paths or tags (e.g., `revalidatePath('/[locale]/(dashboard)/clients')`).
6. Return the shared `ActionResult` union (`lib/actions/action-result.ts`). Use **stable error identity**:

- set `code` using `AppError.*` from `@/lib/errors/codes` (don’t hardcode strings)
- prefer `messageKey` for UI localization; keep `message` as a safe fallback
- do not throw raw errors across the RSC boundary

## Data fetching (Server Components)

- Default to server components. Use `cache()` for shared read helpers.
- Always include `workspace_id` filter. Derive workspace via `requireWorkspaceCached()`.
- For dynamic data, use `fetch(..., { cache: "no-store" })`. For ISR/tagged data, use `next: { revalidate, tags }`.
- Do not import server-only modules into client components.

## Route Handlers (webhooks/external)

- Prefer `requireWorkspace()` (non-React cached) in Route Handlers.
- Still scope every DB query/mutation by `workspace_id`.

## PDF and snapshots

- Finalized invoices must render from `invoice_snapshots`; drafts render from current state.
- Finalization must create snapshot (seller/client/items/totals/locale/template) and lock edits.

## Clerk & tenancy

- Solo MVP: personal workspace only; no org switching. Guard all dashboard routes/actions.
- Do not rely on `orgId` for tenancy in MVP.

## Patterns

- Helper example:

  ```ts
  import { cache } from "react";
  import { db } from "@/db";
  import { clients } from "@/db/schema";
  import { eq } from "drizzle-orm";

  export const getClientsByWorkspace = cache(async (workspaceId: string) => {
    return db.query.clients.findMany({
      where: eq(clients.workspaceId, workspaceId),
      orderBy: (c, { desc }) => desc(c.createdAt),
    });
  });
  ```

## Edge cases checklist

- Prevent cross-tenant access: every query filters `workspace_id`.
- Money: never use floats; keep cents integer.
- Time: UTC storage; convert at display.
- Locale: ensure path includes locale; format currency/dates with next-intl.
- Do not expose sequential IDs; use UUIDs in routes.

## Revalidation tips

- Use `revalidatePath` for route segments, `revalidateTag` for tagged fetches.
- Revalidate after create/update/delete of clients, projects, time entries, invoices, expenses.

## Cost & performance notes (Vercel-friendly)

- Prefer **one Server Action per user intent** (avoid multi-action waterfalls).
- Prefer **narrow invalidation**:
  - `revalidateTag()` is usually cheaper than broad `revalidatePath()`.
  - Avoid invalidating large route subtrees “just to be safe”.
- Avoid sequential independent reads in a Server Component/Action—use `Promise.all`.
- Use React `cache()` for shared read helpers (request-level de-dupe) and ensure `workspaceId` is part of the inputs.

Deep dive reference: `.github/skills/nextjs-cost-performance/SKILL.md`

## Testing

- Add integration/unit tests for tenant isolation and snapshot immutability.
- Type-check with `bun run lint` and `tsc --noEmit`.

## References

- Project PRD: `docs/PRD.md`
- Schema: `db/schema.ts`
- Workspace helper: `lib/workspace.ts`
- next-intl routing: `i18n/routing.ts`
