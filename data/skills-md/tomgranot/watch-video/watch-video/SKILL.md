---
name: watch-video
description: Watch and analyze local or directly downloadable public videos using platform captions and timestamped frames. Use for summaries, chapters, visual evidence, comparisons, and finding moments.
---

# Watch Video

Build a timestamped account of what the video shows, says, and supports. Keep observations, spoken claims, and inferences separate.

## Requirements

Local files require `ffmpeg`, `ffprobe`, Python 3.10+, and Pillow. Public URLs also require `yt-dlp`. Resolve `SKILL_DIR` to the directory containing this file. Run commands through `$SKILL_DIR/scripts/run.py` so they use the private `.venv` when present. If the runtime is missing and local dependency installation is allowed, run `python3 "$SKILL_DIR/scripts/setup_runtime.py"`. Never sign in, load browser cookies, bypass DRM or paywalls, or work around access controls.

## Workflow

1. Create a dedicated analysis directory. Never modify the source video.
2. Acquire the source and platform captions:

   ```bash
   python3 "$SKILL_DIR/scripts/run.py" acquire <video-path-or-url> \
     --output-dir <analysis-dir> [--language en]
   ```

   Local files are primary. Only accept a public URL when `yt-dlp` can inspect and download it directly without sign-in, cookies, paywalls, DRM, or browser automation. If direct retrieval fails, ask for an authorized local copy. For URLs, prefer manual platform captions, then automatic captions. If neither exists, record `transcript unavailable` and continue visually; do not generate a transcript. For local files, detect same-name `.vtt`, `.srt`, `.json`, or `.json3` sidecars.

3. Read `<analysis-dir>/source.json` and `<analysis-dir>/transcript.md` when present. Treat captions as speech evidence, not visual evidence.
4. Build a coarse visual index:

   ```bash
   python3 "$SKILL_DIR/scripts/run.py" sample-frames <video-path-from-source.json> \
     --output-dir <analysis-dir>/visual-overview --mode overview --scene-threshold 0.32
   ```

5. Open every contact sheet listed in `visual-overview/index.md`. Record visible events, demonstrations, slide changes, on-screen text, and notable mismatches with the transcript.
6. Run targeted dense passes around important or ambiguous timestamps:

   ```bash
   python3 "$SKILL_DIR/scripts/run.py" sample-frames <video> \
     --output-dir <analysis-dir>/window-<start> \
     --mode dense --start <seconds> --end <seconds> --fps 4
   ```

   Use `--mode every-frame` only for short forensic windows. It samples with FFmpeg at the reported source frame rate, so variable-frame-rate material may contain duplicated or dropped samples. The script caps output by default. Increase the cap only when the user needs the densest available inspection.
7. Synthesize findings with timestamps. For each substantive claim, label its basis as:
   - `observed`: visible in sampled frames
   - `spoken`: present in captions or supplied transcript
   - `inferred`: a reasoned conclusion from observed or spoken evidence
8. Mark support as `supported`, `conflicted`, or `not_found`. State what evidence is missing when confidence is low.
9. For detailed work, save `report.json` using the schema in [references/analysis-protocol.md](references/analysis-protocol.md), then validate it:

   ```bash
   python3 "$SKILL_DIR/scripts/run.py" validate-report <analysis-dir>/report.json \
     --manifest <analysis-dir>/visual-overview/manifest.json
   ```

   Repeat `--manifest <path>` for each dense window cited in the report.

## Analysis rules

- Start coarse, then inspect important windows at higher temporal density.
- Never describe a transcript claim as something the video visibly proves.
- Quote captions sparingly; paraphrase by default.
- Attach timestamps to chapters, findings, discrepancies, and requested moments.
- Inspect frames at higher resolution when slides, code, diagrams, or small interface text matter.
- Say when captions are automatic, absent, incomplete, or out of sync.
- If the question spans many scattered facts, answer it in focused passes instead of one broad scan.
- Do not infer identity, intent, causation, or off-screen events without evidence.

Read [references/analysis-protocol.md](references/analysis-protocol.md) for sampling modes, the evidence schema, long-video handling, and failure cases.
