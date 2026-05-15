---
name: durable-objects
description: >
  Build Cloudflare Durable Objects for stateful coordination, one-per-entity actors, strong consistency, private SQLite-backed storage, RPC methods, WebSockets, alarms, sessions, rooms, rate limits, and collaborative state. Use when Workers code needs serialized state or race-free coordination.
compatibility: "Cloudflare Workers TypeScript projects using Wrangler; verify current Cloudflare APIs, limits, and pricing before production use."
metadata:
  source: "Architecting on Cloudflare plus official Cloudflare Developer Platform docs"
  generated: "2026-04-28"
---
# Durable Objects

Use this skill when code needs stateful coordination. A Durable Object should represent the smallest logical unit that needs serialization: a room, document, cart, user, game, tenant workspace, rate-limit bucket, or workflow coordinator.

## Design rules

- Create one Durable Object per coordination atom.
- Do not create one global object for all users or all writes.
- Keep object state small and local to its entity.
- Persist durable state; in-memory fields are performance caches only and can disappear.
- Expose clear RPC methods for application operations.
- Use WebSockets in Durable Objects for data realtime: chat, collaboration, live dashboards, multiplayer.
- Make alarms and retries idempotent.

## Current TypeScript skeleton

```ts
import { DurableObject } from "cloudflare:workers";

export interface Env {
  ROOM: DurableObjectNamespace<Room>;
}

export class Room extends DurableObject<Env> {
  constructor(ctx: DurableObjectState, env: Env) {
    super(ctx, env);
  }

  async addMessage(input: { userId: string; body: string }) {
    const id = crypto.randomUUID();
    const now = new Date().toISOString();

    this.ctx.storage.sql.exec(
      `CREATE TABLE IF NOT EXISTS messages (
         id TEXT PRIMARY KEY,
         user_id TEXT NOT NULL,
         body TEXT NOT NULL,
         created_at TEXT NOT NULL
       )`
    );

    this.ctx.storage.sql.exec(
      "INSERT INTO messages (id, user_id, body, created_at) VALUES (?, ?, ?, ?)",
      id,
      input.userId,
      input.body,
      now
    );

    return { id, createdAt: now };
  }

  async listMessages(limit = 50) {
    return [...this.ctx.storage.sql.exec(
      "SELECT id, user_id, body, created_at FROM messages ORDER BY created_at DESC LIMIT ?",
      limit
    )];
  }
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const roomName = url.searchParams.get("room") ?? "default";
    const room = env.ROOM.getByName(roomName);

    if (request.method === "POST") {
      const input = await request.json<{ userId: string; body: string }>();
      return Response.json(await room.addMessage(input));
    }

    return Response.json(await room.listMessages());
  }
} satisfies ExportedHandler<Env>;
```

## Wrangler binding and migration

```jsonc
{
  "durable_objects": {
    "bindings": [
      { "name": "ROOM", "class_name": "Room" }
    ]
  },
  "migrations": [
    {
      "tag": "v1",
      "new_sqlite_classes": ["Room"]
    }
  ]
}
```

## Identity key guidance

- Stable key: `tenant:${tenantId}`, `room:${roomId}`, `doc:${docId}`, `user:${userId}`.
- Do not key by request ID unless each request should have isolated state.
- Avoid unbounded hot keys like `global`, `all`, or `singleton`.
- Hash or normalize externally supplied names if they might be long, sensitive, or inconsistent.

## Durable Object vs alternatives

- Use plain Workers for stateless request handling.
- Use D1 for relational data that does not need per-entity serialized code execution.
- Use Queues for deferred background work where ordering is not central.
- Use Workflows for durable ordered multi-step processes.
- Use KV for cached values, not locks or counters.

## Anti-patterns

- Treating a Durable Object as a global database server.
- Doing long CPU-heavy processing inside a hot object.
- Fanning every request through one coordinator.
- Keeping critical state only in memory.
- Changing/deleting old migration tags instead of appending migrations.
