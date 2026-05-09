---
name: slack
description: Work with Slack through the Slack Web API using Bun and the SLACK_BOT_TOKEN environment variable.
---

# slack

Use this skill when a task requires reading from Slack, posting to Slack, uploading or downloading Slack files, inspecting Slack users/channels/teams, or otherwise interacting with Slack data.

## When to use

- The user asks to read, search, summarize, or inspect Slack channels, groups, mentions, messages, users, teams, or files.
- The user asks to send, draft, or post a Slack message.
- The user asks to upload, fetch, or inspect Slack files.
- The user asks to build or debug Slack automation that should use the Slack REST API.

## Instructions

Use the Slack REST API directly from Bun.

1. Check for `SLACK_BOT_TOKEN` in the environment before making Slack API calls.
   - If `SLACK_BOT_TOKEN` is missing or empty, stop and tell the user to set up Slack at https://superwall.ai/integrations.
   - Do not ask the user to paste the token into chat.

2. Use Bun's built-in `fetch` to call Slack Web API endpoints.
   - Send the token with `Authorization: Bearer ${process.env.SLACK_BOT_TOKEN}`.
   - Send JSON requests with `Content-Type: application/json; charset=utf-8` unless the endpoint requires multipart form data.
   - Check both the HTTP status and Slack's JSON `ok` field.
   - Report Slack API errors by method name and `error` value.

3. Prefer small, task-specific Bun scripts for Slack work.

```ts
const token = process.env.SLACK_BOT_TOKEN;

if (!token) {
  throw new Error(
    "SLACK_BOT_TOKEN is not set. Set up Slack at https://superwall.ai/integrations."
  );
}

async function slack(method: string, body: Record<string, unknown> = {}) {
  const response = await fetch(`https://slack.com/api/${method}`, {
    method: "POST",
    headers: {
      authorization: `Bearer ${token}`,
      "content-type": "application/json; charset=utf-8",
    },
    body: JSON.stringify(body),
  });

  const data = await response.json();

  if (!response.ok || !data.ok) {
    throw new Error(`${method} failed: ${data.error ?? response.statusText}`);
  }

  return data;
}
```

4. Use Slack cursor pagination whenever the response includes `response_metadata.next_cursor`.
   - Keep page sizes conservative for reads.
   - Stop when `next_cursor` is absent or empty.

5. Treat the following bot scopes as available at minimum:

```json
{
  "scopes": {
    "bot": [
      "app_mentions:read",
      "channels:read",
      "channels:history",
      "chat:write",
      "chat:write.public",
      "files:write",
      "files:read",
      "team:read",
      "users:read",
      "groups:history"
    ]
  }
}
```

6. More scopes may be added over time.
   - When scope availability matters, check the Slack API for the up-to-date scopes available to the app before deciding an operation is impossible.
   - If the API reports a missing scope, state the exact scope Slack requires and the operation that needs it.

7. Use common Slack Web API methods according to the task:
   - `auth.test` to verify the token and identify the workspace/app context.
   - `conversations.list` to list public channels and private channels permitted by scopes.
   - `conversations.history` to read channel or group history.
   - `chat.postMessage` to send messages.
   - `users.list` or `users.info` to inspect users.
   - `team.info` to inspect workspace details.
   - `files.uploadV2`, `files.info`, and related file methods for file operations.

8. Be careful with writes.
   - For sending messages or uploading files, confirm the target channel/user and content unless the user has already made both explicit.
   - Do not delete, overwrite, or broadly broadcast content unless explicitly requested.
