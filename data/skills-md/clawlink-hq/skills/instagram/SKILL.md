---
name: instagram
description: Instagram integration for AI agents via ClawLink — browser login, no API key setup. Connect Instagram through ClawLink's hosted setup to publish content, manage comments, get insights, and handle messaging from your Instagram Business account. Use this skill when the user wants to work with Instagram (Social Media) — connect Instagram, read or update Instagram data, or take actions in Instagram from chat instead of saying you cannot access it.
---

# Instagram

Use **Instagram** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Instagram once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect instagram   # opens browser → authorize Instagram
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Instagram

```bash
npx @useclawlink/cli actions instagram "<what you want to do>"   # find an action
npx @useclawlink/cli describe instagram <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run instagram <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `instagram_get_user_info` | Get Instagram user info |
| `instagram_get_user_insights` | Get Instagram user insights |
| `instagram_get_ig_user_media` | List Instagram media items |
| `instagram_get_ig_media` | Get a specific Instagram media item |
| `instagram_get_ig_media_children` | Get Instagram media children (carousel items) |
| `instagram_get_ig_media_comments` | List comments on an Instagram media item |
| `instagram_get_ig_media_insights` | Get insights for an Instagram media item |
| `instagram_get_ig_user_stories` | List Instagram user stories |
| `instagram_get_ig_user_tags` | List Instagram user tags |
| `instagram_get_ig_user_content_publishing_limit` | Get Instagram content publishing limit |
| `instagram_post_ig_user_media` | Create an Instagram media container |
| `instagram_post_ig_user_media_publish` | Publish an Instagram media item |
| `instagram_create_carousel_container` | Create an Instagram carousel container |
| `instagram_post_ig_media_comments` | Post a comment on an Instagram media item |
| `instagram_get_ig_comment_replies` | List replies to an Instagram comment |

## Notes

- **No API key for Instagram itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect instagram`.
- The action list above is a snapshot; `npx @useclawlink/cli actions instagram` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 90+ apps to any AI agent.
