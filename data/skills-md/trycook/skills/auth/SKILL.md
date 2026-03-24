---
name: auth
description: Authenticate with the TryCook platform via browser login
allowed_tools: Bash, Read, Write
user_invocable: true
---

# /auth — TryCook Authentication

Authenticate your Claude Code instance with the TryCook platform.

## Flow

1. Start a temporary local HTTP server on a random port to receive the callback.
2. Open the user's browser to `https://trycook.ai/cli/auth?port=<PORT>`.
3. User signs in with Clerk (if not already signed in). Only `client` and `admin` roles are allowed.
4. The browser page issues a CLI token and POSTs it back to the local callback server.
5. Store the token in `~/.config/trycook/credentials.json`.

## Instructions

Run the following to authenticate:

```bash
# Start auth flow — opens browser, receives token via local callback
bun ${CLAUDE_PLUGIN_ROOT}/scripts/auth.ts
```

If the browser flow fails, the user can manually copy the token from the browser and paste it. Store it at `~/.config/trycook/credentials.json` as:

```json
{
  "token": "<TOKEN>",
  "created_at": "<ISO_DATE>"
}
```

After auth, verify it works by calling the `ping` MCP tool.
