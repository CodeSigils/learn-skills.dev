---
name: youtube-transcript
description: Get YouTube transcripts and captions with Stophy CLI. Trigger when the user provides a video URL and asks for the transcript, captions, spoken text, summary input, quotes, timestamps, notes, or wants to send video text into an app, workflow, or AI agent.
metadata:
  author: stophy
  version: "1.0.0"
allowed-tools:
  - Bash(stophy *)
  - Bash(npx @stophy/cli *)
---

# youtube-transcript

Get transcript text with timestamps for a YouTube video.

## Choose this skill when

- The user asks for a transcript, captions, spoken content, quotes, or a summary source.
- The user wants to process a video with an app, workflow, or AI agent.
- The user needs timestamps for citations, clips, notes, or references.

Use `youtube-video` first only if you need metadata. Use `youtube-comments` if the user asks what viewers said.

## Commands

```bash
# Transcript with timestamps
stophy video transcript --url "https://www.youtube.com/watch?v=h6ukrWyqOm4"

# Raw JSON
stophy video transcript --url "https://www.youtube.com/watch?v=h6ukrWyqOm4" --json

# Plain transcript text
stophy video transcript --url "https://www.youtube.com/watch?v=h6ukrWyqOm4" --json   | jq '.data.segments[].text' -r
```

## Options

| Option | Values | Use when |
|--------|--------|----------|
| `--url <url>` | YouTube video URL | Always required |
| `--json` | — | Pipe or parse raw JSON |

## Response shape

`transcript` returns:

- `language`
- `segments[]`
  - `text`
  - `start`
  - `duration`

## Output guidance

- If the user asks for the transcript, provide readable text and preserve timestamps when useful.
- If the user asks for summarization or extraction, first fetch the transcript, then perform the requested work.
- If captions are unavailable, report that directly. Do not fabricate a transcript.
- For long transcripts, summarize or save the structured output when appropriate instead of flooding the response.

## Related skills

- [youtube-video](../youtube-video/SKILL.md) — get video metadata
- [youtube-comments](../youtube-comments/SKILL.md) — read audience discussion
- [youtube-search](../youtube-search/SKILL.md) — find candidate videos first
- [youtube-playlist](../youtube-playlist/SKILL.md) — collect videos from a playlist before fetching transcripts
