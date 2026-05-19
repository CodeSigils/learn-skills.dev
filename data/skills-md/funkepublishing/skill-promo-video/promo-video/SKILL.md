---
name: promo-video
description: Use this skill when the user wants to assemble a short promo video from a folder of raw clips — vertical/square/horizontal, with optional intro, outro, music (AI-generated via Suno or provided), and overlay effects. Triggers on phrases like "promo video", "hackathon video", "social media clip", "cut these clips together", "make a reel", or when the user points at a folder of .mov/.mp4 files that should become one deliverable. Use it whenever the user describes a short-form branded video workflow regardless of whether they explicitly name this skill.
license: see LICENSE.txt
---

# promo-video

Assemble short promo videos from raw clips. Portrait, square, or landscape.
Optional Blender-rendered intro/outro, optional AI-generated music.

The skill is agnostic of the host agent: it MUST work identically across
every runtime that implements the Agent Skills standard
(https://agentskills.io) — Claude, Claude Code, OpenAI Codex, Gemini CLI,
Cursor, GitHub Copilot, Cline, OpenCode, OpenHands, Goose, Kiro, Junie,
and others. Never rely on host-specific tools (no `AskUserQuestion`, no
slash commands, no MCP unless explicitly available). Conduct all user
interaction as normal chat messages.

## When to use

- "Cut these clips together into a 30-second reel."
- "Build me a hackathon promo video in portrait."
- "I have a folder of phone videos — make a 1080x1920 social clip with music."
- "Generate a promo with logo intro + heart outro + background track."
- The user references a directory of `.mov`/`.mp4` files and wants one
  deliverable.

## Prerequisites

- `ffmpeg` on PATH, built with `libx264`, `aac`, and `prores_ks` (the last one
  is only needed for alpha-channel intro/outro MOVs).
- Python 3.9+.
- Install Python deps once: `pip install -r requirements.txt` from inside the
  skill directory.
- Optional: a `.env` at the project root containing `SUNO_API_KEY` to enable
  music generation. The skill auto-detects whether the key is set and only
  offers music generation if it is.
- Optional: Blender MCP available in the host agent to produce intro/outro
  renders. See `references/blender_mcp.md`.

## Default flow (dialog-based)

### Step 0 — Detect whether clips have changed since last run

Before asking any questions, check if the user is resuming from a previous
session. If `gallery/.clips_snapshot.json` exists (or if the user points
you at a clips folder that was used before), run:

```bash
python scripts/clip_diff.py <clips_dir>
```

- Exit code **0** — clips folder matches the last snapshot. Continue.
- Exit code **1** — drift. The report lists new / removed / modified
  clips. Show it to the user, then offer to re-run `scripts/gallery.py`
  so the gallery picks up the new clips. Existing selections for clips
  that are still there survive untouched.
- Exit code **2** — no snapshot yet. Normal first-run, continue.

Do NOT skip this step when resuming an existing project — silently
working against a stale gallery / selection.json is the classic
"where did my new clips go?" bug.

### Questions

At the start, ask the user the questions below, in order. Accept natural
answers; do not present a multiple-choice UI unless the host supports it.
For every question, also accept "you decide" and apply the sensible default.

1. **Target format.** 1080x1920 portrait (default), 1920x1080 landscape, or
   1080x1080 square. Custom sizes allowed.
2. **Clips source.** Absolute or relative path to a directory containing the
   raw clips. `.mov`, `.mp4`, `.m4v` are supported.
3. **Target length in seconds.** (Typical: 20–45 s.)
4. **Music.** One of: (a) existing audio file, (b) generate via Suno (only
   offer if `SUNO_API_KEY` is set), (c) no music.
5. **Intro.** One of: none, static image (path), Blender MCP generated.
6. **Outro.** Same choices as intro.
7. **Director mode.** Yes or no. If yes, follow
   `references/director_mode.md` instead of continuing linearly here.

Then handle clip selection. Offer two paths:

**A) Visual gallery (recommended for >10 clips or when the user wants to
see frames before picking cues).** Run
`scripts/gallery.py <clips_dir> --resolution WxH --fps 30 --target-length N`
— it generates `gallery/gallery.html` with thumbnails, IN/OUT sliders,
speed slider, and range preview. Tell the user to open it in a browser,
pick clips, set cues, then click "Export selection.json". The downloaded
file is ready for `build.py`.

**B) Inline dialog (fine for small batches or when no browser is
available).** Walk through each clip yourself:
- `cue_in` and `cue_out` in seconds (trim range)
- `speed` multiplier (1.0 = original)
- `fixed: true` if timing/speed is hand-curated, `false` for free fillers
  (default: 0.6 s from the middle, speed 1.0)

Offer "Just give me defaults" — pick every clip alphabetically, free
defaults, up to the target length.

Either way, the result is a `selection.json` matching
`templates/selection.schema.json`. Validate before proceeding.

## Build

Once `selection.json` is valid, run:

```bash
python <skill>/scripts/build.py <selection.json> --out output/<name>.mp4
```

`build.py` writes intermediate artefacts under `build/` (relative to the
current working directory): `build/normalized/`, `build/trimmed/`,
`build/montage.mp4`, `build/composed.mp4`. Delete `build/` to force a full
re-render.

Every submodule under `scripts/` is also runnable standalone — useful for
iterating on one step without rebuilding the whole pipeline. Each takes an
`--help` argument.

## Director mode (optional)

Opt-in. See `references/director_mode.md` for the role prompts. The skill
spawns four sequential roles — Narrator → Cutter → Composer → Supervisor —
that share `selection.json` as state. Each role reads the current JSON and
writes its updates back. Use this when the user asks for "a more guided
process" or "walk me through it like a producer".

## Music generation (optional)

If the user chose "generate via Suno", delegate the music step to the
**Song-Builder sub-agent** defined in `references/song_builder_agent.md`.
That sub-agent:

1. Asks the user for genre, mood, BPM range, section structure, instrumental
   on/off, and takes video length as duration.
2. Formulates a Suno prompt + style tags.
3. Calls `scripts/music.generate_song(spec)` — supply `takes > 1` if the user
   wants options to compare.
4. Trims and fades the chosen take to the video length.
5. Writes the final mp3 path into `selection.json` as `audio`.

If the host provides a sub-agent mechanism (e.g. Claude Code's Agent tool),
use it. Otherwise, play the role inline in the same thread.

## Blender MCP integration (optional)

Only assistance — this skill does not bundle a Blender scene.

If the user wants a Blender-rendered intro or outro, delegate to the
**Blender-Builder sub-agent** defined in
`references/blender_builder_agent.md`. It owns the full flow: preflight
(check that Blender + MCP are actually reachable in this host), design
interview (visual direction, colors, duration), scene build, iterative
preview, render to ProRes 4444 alpha MOV, and hand-off of the MOV path
into `selection.json`.

If the host provides a sub-agent mechanism (e.g. Claude Code's Agent
tool), spawn it. Otherwise play the role inline. The main dialog flow
should invoke the Blender-Builder whenever the user chose "Blender MCP
generated" for intro or outro in step 5 of the questionnaire.

Setup documentation (install Blender, install the MCP server, register
it with the host) lives in `references/blender_mcp.md`. The
Blender-Builder sub-agent pulls from that doc when the user needs to
configure the stack for the first time.

## Error recovery

- If a clip fails normalization (codec / resolution edge case), `build.py`
  exits with a non-zero code and a clear stderr message pointing at the
  offending file. Ask the user whether to skip the clip or investigate.
- If Suno returns a 4xx or times out, offer the user to retry, switch to
  "existing file", or proceed without music.
- Never silently drop clips. Never overwrite an existing output file without
  confirmation unless `--force` is passed.

## Style notes for this skill

- **Never assume host-specific tools.** All dialog is plain chat.
- **Show your work.** When trimming, tell the user which cue points you
  settled on before building.
- **Fail loud.** If `ffmpeg` is missing, say so and show the install command
  for the user's platform.
