---
name: reddit
description: Read-only Reddit toolkit. Search posts, browse subreddits (hot/new/top), read posts with comments, look up user profiles, and get subreddit info — all without authentication. Use when the user asks about Reddit content, wants to search Reddit, browse a subreddit, read a post, check a user's profile, or find discussions on any topic. No API key required. Write features (post, vote, inbox) are not yet available (require Reddit API auth setup).
---

# Reddit Skill

Read-only Reddit access via the public JSON API. No auth, no API key — just works.

## Script

All operations go through `scripts/reddit.py`. Run with:
```bash
python3 /home/ajitesh/.openclaw/skills/reddit/scripts/reddit.py <command> [args]
```

## Commands

| Command | Args | Description |
|---------|------|-------------|
| `search` | `<query> [limit] [sort]` | Search Reddit. sort: relevance/hot/new/top |
| `hot` | `<subreddit> [limit]` | Hot posts from a subreddit |
| `new` | `<subreddit> [limit]` | New posts from a subreddit |
| `top` | `<subreddit> [limit] [timeframe]` | Top posts. timeframe: hour/day/week/month/year/all |
| `post` | `<post_id>` | Get post + top 15 comments |
| `user` | `<username>` | User profile + recent posts |
| `subreddit` | `<name>` | Subreddit info (subscribers, description, etc.) |

Post IDs are the alphanumeric part of a Reddit URL: `reddit.com/r/sub/comments/<post_id>/title`

## Notes

- Default limit: 10 posts
- Post content truncated at 500 chars; comments at 500 chars
- Output is JSON — parse and summarize for the user in a readable format
- Rate limit: be reasonable, don't hammer in loops
- Write features (post, comment, vote, inbox) require Reddit API auth — tell the user to set up API credentials when they ask for these
