---
name: rn-replica-qc
description: >
  Analyze, recreate, align, and verify reference-video motion. Use when the
  user asks to recreate, copy, match, align, pixel-align, or compare a video
  against a reference; when a HyperFrames or Remotion remake is judged "not
  aligned"; when reference motion should be turned into reusable components; or
  when a video needs frame-by-frame breakdown, side-by-side contact sheets,
  dense failing-window sampling, repair logs, PSNR/SSIM, hash checks, or a
  clear pixel-level vs visual-level vs style-level fidelity decision.
---

# Reference Video Replica QC

## Role

Make reference-video work evidence-driven and reusable. First classify the
requested fidelity, then extract frames, describe the source timeline, compare
the candidate, repair the implementation in small verified passes, and capture
successful motion patterns as HyperFrames / Remotion components.

This skill is not only a final QC gate. It is also a replication loop for
turning real video motion into a component library so future AI-generated videos
can reuse proven animated patterns instead of defaulting to static slide-like
layouts.

## Canonical Showcase

- Human display name: Presenton 复刻 Bitexact 成片
- Example finished piece: Presenton replica pixel-aligned bitexact output
- File: `assets/showcases/presenton-replica-pixel-aligned-bitexact.mp4`
- Use this as the repository's reference-video replication showcase. It is the
  correct public example for this skill, replacing older short preview clips.

## Fidelity Levels

Read `references/replica-levels.md` before promising any fidelity level.

- Pixel-level: exact decoded pixels, or exact source stream reuse. Requires hard
  evidence such as matching SHA-256/`cmp`, PSNR infinity, or SSIM 1.0.
- Visual-level: hand-authored recreation that matches scene timing, layout,
  motion, typography, and color closely enough for human review.
- Style-level: uses the reference as a design language, not as a frame target.

Never describe a HyperFrames/Remotion rebuild as pixel-level unless it passes
the hard metrics.

## Operating Modes

- Analysis-only: inspect the reference and/or candidate, write reports, and do
  not edit implementation code.
- Replica-loop: keep a persistent objective, compare reference and candidate at
  the same timestamps, edit the HyperFrames/Remotion/CSS/SVG/timeline code, and
  re-run evidence until the requested level is met or the remaining mismatch is
  explicitly documented.
- Component-capture: after a motion pattern is visually aligned, describe it as
  a reusable component with purpose, inputs, timing, implementation stack,
  evidence, and limits.

## Workflow

### 1. Establish Inputs

Collect:

- reference video path or URL
- candidate video path, if one exists
- requested fidelity level
- sampling interval, default `0.5s`
- failing-window interval, default `0.1s` when motion is fast or misaligned
- target implementation stack: HyperFrames, Remotion, or another renderer
- component-library output path, if reusable motions should be saved
- output directory for analysis artifacts

If the URL is private or expired, use the download skill or browser/source page
to retrieve a fresh source before analysis.

### 2. Set The Persistent Objective

When the environment has Goal mode, create or reuse a goal that states:

- the exact reference segment
- the fidelity level
- the target renderer
- the visible components to align
- the acceptance evidence

If Goal mode is unavailable, use `alignment-report.md` and `patch-log.md` as
the persistent objective. Do not rely on chat memory alone.

### 3. Analyze The Reference

Use `scripts/extract_halfsec_frames.py` or equivalent ffmpeg commands to extract
frames at fixed timestamps. Start with `0.5s`, then add `0.1s` or explicit
timestamps around transitions, fast typography, cursor movement, model lists,
rail/line motion, or any failing window. Create contact sheets. Then write a
timeline report:

- timestamp
- visible text
- primary subject and position
- transition state
- camera/scale movement
- UI/cursor/button behavior
- notes about typography, color, glow, grain, or background

Do not build from memory. The extracted frames are the source of truth.

### 4. Compare Candidate To Reference

If a candidate exists, use `scripts/compare_videos.py` for hard metrics, then
create side-by-side contact sheets at the same timestamps.

Classify every mismatch:

- timing offset
- scene boundary mismatch
- subject size or position mismatch
- missing/extra transition
- wrong typography or text state
- wrong background or color system
- asset mismatch
- compression/encoding-only difference

For hand-authored HyperFrames/Remotion work, also run component-level checks
instead of relying only on whole-frame metrics:

- object center, size, and rotation
- text line breaks, font weight, and opacity
- rail/line path, length, color, and mask timing
- card/logo/color anchor positions
- crop-level overlays for the active component
- adjacent timestamps before and after each fix

### 5. Repair In Small Verified Passes

In replica-loop mode, pick the earliest or largest visible mismatch and make a
targeted code change. Then regenerate frames for the same timestamps and update
the evidence before touching the next mismatch.

Rules:

- Prefer one visible fix per pass: timing, layout, motion path, scale, color, or
  asset state.
- Recheck neighboring timestamps so a local fix does not break the sequence.
- Treat whole-frame PSNR/SSIM as supporting evidence, not the only truth, when
  fonts, browser rasterization, and generated assets differ.
- For HyperFrames, run `lint`, `validate`, and `inspect` before final render.
- For Remotion, run the equivalent render/screenshot validation used by the
  project.
- Do not say "aligned" until the report points to the passing evidence.

### 6. Capture Reusable Components

When a motion pattern is aligned well enough to reuse, write a component entry.
Each component entry should include:

- component name and short description
- source reference and timestamp range
- when to use it in an AI-generated video
- input props or parameters
- timing contract and important easing/state changes
- implementation stack: HyperFrames, Remotion, React, CSS, SVG, GSAP, assets
- visual acceptance evidence: contact sheet, crop, overlay, or metrics
- known limits and what should not be promised

The goal is a growing library of proven video-language building blocks: title
openers, model switch lists, vertical rails, floating cards, product panels,
code reveals, CTA transitions, captions, and diagram motions.

### 7. Decide

Approve only if the candidate meets the requested level:

- Pixel-level: hard metrics pass.
- Visual-level: side-by-side frames align at the declared interval, with only
  accepted differences.
- Style-level: the style principles are present; exact timing is optional.

If it fails, produce a repair list ordered by timestamp. Say "not aligned" and
name the first failing timestamp.

## Script Usage

```bash
python3 scripts/extract_halfsec_frames.py reference.mp4 --out analysis/reference
python3 scripts/extract_halfsec_frames.py reference.mp4 --out analysis/reference-dense --interval 0.1 --start 18 --end 21 --contact
python3 scripts/compare_videos.py reference.mp4 candidate.mp4 --out analysis/compare
```

Use the workspace Python from `load_workspace_dependencies` when Pillow is
needed for labeled contact sheets.

## Outputs

Keep these artifacts near the video project:

- `alignment-report.md`
- `patch-log.md`
- reusable component entries or `component-catalog.md`
- source contact sheets
- side-by-side contact sheets
- crop/overlay evidence for active components
- `comparison-report.md`
- PSNR/SSIM logs when comparing videos
- final pass/fail summary

For content-creation projects, copy the final QC artifacts into the desktop
archive `质检/` folder.
