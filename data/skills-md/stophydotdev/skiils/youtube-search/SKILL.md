---
name: youtube-search
description: Search YouTube by keyword with Stophy CLI. Trigger when the user asks to find videos, Shorts, channels, or playlists; asks for top/recent content on a topic; needs YouTube search results before fetching transcripts, comments, channels, or playlist data.
metadata:
  author: stophy
  version: "1.0.0"
allowed-tools:
  - Bash(stophy *)
  - Bash(npx @stophy/cli *)
---

# youtube-search

Search YouTube by keyword and filter results by type, date, duration, and sort order.

## Choose this skill when

- The user asks to “search YouTube”, “find videos about X”, “top videos on X”, or “recent videos about X”.
- The user needs candidate videos before fetching transcripts, comments, or metadata.
- The user is researching a topic, creator space, market, tutorial niche, product category, or trend.

Use a more specific skill if the user already provided a direct video, channel, or playlist URL.

## Commands

```bash
# Basic search
stophy search --q "how to build a SaaS"

# Videos sorted by popularity
stophy search --q "Claude Code" --type video --sortBy popularity

# Recent results
stophy search --q "AI news" --uploadDate week

# Long-form videos
stophy search --q "Python for beginners" --duration long

# Paginate
stophy search --q "typescript" --continuation-token <token>
```

## Options

| Option | Values | Use when |
|--------|--------|----------|
| `--q <query>` | any query | Always required |
| `--type <type>` | video, short, channel, playlist, movie | Limit result type |
| `--sortBy <sort>` | relevance, popularity, date, rating | Prefer relevance, popularity, recency, or rating |
| `--uploadDate <date>` | today, week, month, year | Focus on recent content |
| `--duration <duration>` | short, medium, long | Match short-form, mid-length, or long-form content |
| `--continuation-token <token>` | string | Fetch the next page |
| `--json` | — | Pipe or parse raw JSON |

## Decision rules

- Use `--sortBy popularity` for “top”, “popular”, or “biggest” videos.
- Use `--sortBy date` or `--uploadDate week/month` for news and fast-moving topics.
- Use `--duration long` for podcasts, lectures, tutorials, and deep dives.
- Use `--type channel` when the user asks for creators or channels, not individual videos.
- Keep the query human-readable; do not over-optimize with awkward Boolean syntax unless the user asks.

## Output guidance

- Return a short ranked list with title, channel, URL, publish date, and views when available.
- Include the `continuationToken` if the user may want more results.
- If the user plans follow-up analysis, suggest the next exact command for transcript, comments, or metadata.

## Follow-up paths

- [youtube-video](../youtube-video/SKILL.md) — get metadata for one selected result
- [youtube-transcript](../youtube-transcript/SKILL.md) — get transcript text after selecting a video
- [youtube-comments](../youtube-comments/SKILL.md) — read comments after selecting a video
- [youtube-channel](../youtube-channel/SKILL.md) — inspect a channel from search results
- [youtube-playlist](../youtube-playlist/SKILL.md) — fetch playlist videos from a playlist result
