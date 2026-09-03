---
name: seedance
description: "Seedance 2.0/2.5 video generation skill — craft prompts, direct camera/light/motion, manage @references, multi-shot sequences, troubleshoot, API usage. For any Seedance surface: Dreamina, Jimeng, CapCut, Doubao, Fal AI, Volcengine/Ark, Runway, Replicate, or third-party routers. Covers text-to-video, image-to-video, reference-to-video, first/last-frame, video edit/extend, lip-sync, audio sync."
license: MIT
user-invocable: true
tags: [seedance, video-generation, ai-video, bytedance]
---

# Seedance Video Generation Skill

Comprehensive skill for ByteDance's Seedance 2.0/2.5 AI video generation model. Covers prompt engineering, camera direction, lighting, multi-shot storytelling, API integration, and troubleshooting across all platforms.

## Soul

Three principles govern every interaction:

1. **Hear the intent behind the words.** Users describe outcomes ("make it feel like home"), not parameters. Translate feeling into craft; never hand the translation work back to the user.
2. **Keep the story alive.** Hold state across the conversation: subject, mode, look, references, decided constraints, and what failed before. A user should never repeat a decision; a new request inherits the world already built.
3. **Evolve with the user.** Speak plainly to a beginner and in director language to a professional — and notice when the same user grows across a project. Register adapts; standards never do.

---

## Quick Start

When a user asks to create a Seedance video:

1. Ask what they want — type, mood, duration
2. Ask what materials they have — images, videos, audio files
3. Draft the prompt using the structure below
4. Explain your choices briefly
5. Offer variations — simpler or more ambitious
6. Remind about constraints — face restrictions and file limits

For simple single-clip requests, go straight to drafting. Don't run full analysis for one-off clips.

---

## Platform Access

| Platform | Access | Best For |
|----------|--------|----------|
| **Dreamina (Jimeng/即梦)** | Official Chinese platform, free daily credits | Casual creators, visual UI |
| **Doubao** | VPN to HK, ~10 credits/day | Free testing |
| **CapCut Pro** | Partial integration | Video editors |
| **Fal AI** | API key from fal.ai | Developers, programmatic access |
| **Volcengine/Ark** | ByteDance cloud API | Production, enterprise |
| **Runway (Seedance route)** | Runway API key | Runway ecosystem users |
| **Replicate** | Cog model | Developers |
| **MuAPI** | Unified API gateway | Multi-provider access |

### API Endpoints

```
# Fal AI
Image-to-Video:  fal-ai/seedance-2.0/pro/image-to-video
Reference-to-Video: fal-ai/seedance-2.0/pro/reference-to-video
Text-to-Video: fal-ai/seedance-2.0/pro/text-to-video

# MuAPI
T2V: POST https://api.muapi.ai/api/v1/seedance-2.5-t2v
I2V: POST https://api.muapi.ai/api/v1/seedance-2.5-i2v
Extend: POST https://api.muapi.ai/api/v1/seedance-2.5-extend
```

---

## Input Constraints

| Input Type | Limit | Format | Max Size |
|------------|-------|--------|----------|
| Images | ≤ 9 (2.0), ≤ 30 (2.5) | jpeg, png, webp, bmp, tiff, gif | 30 MB each |
| Videos | ≤ 3 (2.0), ≤ 10 (2.5), total ≤ 15s (2.0) / 30s (2.5) | mp4, mov | 50 MB each |
| Audio | ≤ 3 (2.0), ≤ 10 (2.5), total ≤ 15s (2.0) / 30s (2.5) | mp3, wav | 15 MB each |
| **Total files** | ≤ 12 (2.0), ≤ 50 (2.5) | — | — |

### Output

- Duration: 4–15s (2.0), 4–30s (2.5)
- Resolutions: 480p, 720p (1080p, 4K planned)
- Aspect ratios: `21:9` `16:9` `4:3` `1:1` `3:4` `9:16`
- Formats: MP4 (default), MOV (2.5, high color-fidelity)
- Native audio-visual sync with auto-generated sound effects/BGM

### Key Restrictions

- **No realistic human faces** in uploaded images (platform compliance on official surfaces)
- Face detection blocks realistic face uploads on Jimeng/Dreamina
- Reference videos incur slightly higher generation cost
- Prioritize uploading materials that most influence visuals or rhythm

---

## Modes

| Mode | Description | When To Use |
|------|-------------|-------------|
| **T2V** (Text-to-Video) | Generate from text only | No reference assets available |
| **I2V** (Image-to-Video) | Animate a still image | You have a reference image, want controlled output |
| **V2V** (Video-to-Video) | Restyle/reinterpret a video | Transfer motion, camera, or timing from a clip |
| **R2V** (Reference-to-Video) | Multi-modal: combine images + video + audio | Maximum control, best quality |
| **FLF2V** (First/Last Frame) | Interpolate between two keyframes | Precise start and end control |
| **Edit** | Modify one layer while preserving source | Character swap, outfit change, background edit |
| **Extend** | Continue from accepted footage | Make a clip longer, seamless continuation |

### Mode-Specific Prompting

**T2V:** Build the whole shot in compact layers. Core structure: Subject + Action + Scene + Camera + Lighting/Style + Audio. Keep one visible beat and one endpoint per clip.

**I2V:** Preserve visible identity; add motion. Say `preserve @Image1 exactly`; describe only motion, camera, timing, transformation, audio, and preservation constraints — don't re-describe the image.

**V2V:** Transfer motion, camera, or timing. Use owned/licensed/authorized references. State transfer role explicitly.

**R2V:** Assign one primary role per asset. Don't ask one reference to control identity, pose, scene, AND style. Split roles: `@Image1 for character identity, @Video1 for motion reference, @Image2 for scene style`.

**FLF2V:** State `@Image2 is the final visual target`. Frame-by-frame interpolation between first and last frame.

**Edit:** Say `@Video1 is the source clip; change only [specific element]`. Don't rewrite the whole scene.

**Extend:** Route continuation requests properly. Observe the actual end state of the accepted clip. Duration setting = NEW portion only.

---

## The @ Reference System

The most critical syntax for Seedance. Use `@` to assign each uploaded asset a role in your prompt.

### Syntax

```
@Image1 @Image2 @Image3 ...
@Video1 @Video2 @Video3
@Audio1 @Audio2 @Audio3
```

### Role Assignment

Always explicitly state what each reference does:

```
@Image1 is the main character (identity anchor).
@Image2 is the scene background.
@Video1 provides the camera motion reference.
@Audio1 is the background music.
```

### File Allocation by Use Case

| Use Case | Images | Videos | Audio | Total |
|----------|--------|--------|-------|-------|
| Product commercial | 4 (product angles) | 1 (camera ref) | 1 (music) | 6 |
| Character animation | 3 (character + scene) | 2 (motion ref) | 1 (music) | 6 |
| Music video | 2 (style + character) | 2 (dance ref) | 3 (tracks) | 7 |
| Multi-shot narrative | 6 (scene keyframes) | 1 (style ref) | 1 (music) | 8 |
| Quick test | 1 | 0 | 0 | 1 |

> Golden rule: 1 reference image per 2 seconds of video. Fewer, higher-quality references usually outperform many low-quality ones.

### Common @ Reference Mistakes

1. Forgetting @ references after uploading — model ignores your assets
2. Tagging wrong media types — `@Video1` when you uploaded an image
3. Not specifying roles — model guesses which asset does what
4. One reference asked to do too many things — split roles

---

## Core Prompt Formula

```
[Subject] + [Action] + [Scene] + [Camera] + [Lighting/Style] + [Audio/Constraints]
```

Put the subject and primary action first — early clauses set the shot hierarchy. Target 40–110 words for single clips; 60–100 for production.

### Example

```
A young chef (subject) carefully plates a dish with tweezers (action)
in a Michelin-star restaurant kitchen at midnight (scene),
close-up rack focus from hands to face (camera),
warm tungsten lighting, cinematic 35mm film grain (style),
no jump cuts, maintain consistent kitchen background (constraints).
```

### The 6D Framework (for stable production)

1. **Subject** — Who or what (singular preferred)
2. **Action** — What they're doing (plain language, specific speed)
3. **Scene Boundaries** — Where, when, spatial context
4. **Camera** — Shot type + movement + lens feel
5. **Lighting** — One strong lighting keyword beats ten adjectives
6. **Timing** — Duration, pacing, beat structure

---

## Camera Movement Vocabulary

Use exact terms for precise control:

| Movement | Keyword | Effect |
|----------|---------|--------|
| Move toward subject | `slow push in` / `dolly in` | Close-up emphasis, emotional focus |
| Move away from subject | `pull back` / `dolly out` | Environmental reveal |
| Horizontal slide | `tracking shot left/right` | Subject following |
| Vertical rise | `crane up` / `boom up` | Grandeur, scale |
| Follow subject | `steadicam follow shot` | Action, walking |
| Rotate around subject | `orbit shot` / `360 arc` | Product, hero shots |
| Quick pan | `whip pan left/right` | Energy, transition |
| Lock still | `static shot` / `locked off camera` | Dialogue, observation |
| Overhead | `bird's eye view` / `top-down` | Establishing, food |
| Low angle | `worm's eye view` / `low angle` | Power, intimidation |
| Shaky, urgent | `handheld camera` | Documentary, realism |
| Smooth glide | `gimbal shot` | Commercial, polished |
| Background blur | `rack focus to subject` | Emotional focus |
| First-person drone | `FPV continuous long take` | Immersion, action |

### Compound Camera Moves

Structure compound moves as sequential beats — Seedance respects sequence better than simultaneous:

```
Start: slow dolly-in establishing the scene.
Then: gentle pan right for the final 2 seconds.
```

**Wrong:** "dolly-in while panning right" — jams both into one clause.

### Camera + Shot Size Pairings

| Shot Size | Best Pairing | Avoid |
|-----------|-------------|-------|
| Wide | Slow dolly or locked-off | Fast pans |
| Medium | Handheld (personal) or gimbal (polished) | — |
| Close-up | Tiny push-ins | Pans (jarring) |

---

## Lighting Keywords

Lighting has the **single biggest impact** on output quality. One keyword beats ten adjectives.

| Look | Keyword |
|------|---------|
| Golden hour warmth | `golden hour cinematography` |
| Night interior | `tungsten practical lighting` |
| Drama / mystery | `chiaroscuro lighting` |
| Studio clean | `soft box three-point lighting` |
| Neon / cyberpunk | `neon-drenched night scene` |
| Documentary | `natural available light` |
| Horror | `harsh under-lighting` |
| Beauty / fashion | `butterfly lighting` |
| Overcast outdoor | `diffused cloudy daylight` |
| Underwater | `volumetric light beams through water` |
| Sci-fi epic | `high dynamic range, realistic sci-fi texture` |

---

## Visual Style Anchors

Seedance responds strongly to specific industry references. Replace generic adjectives with concrete anchors:

| Instead of | Try |
|------------|-----|
| `cinematic` | `locked close-up, warm practical key, cool rim light` |
| `epic` | `wide low-angle shot, tiny figure against storm wall` |
| `beautiful` | `pearl highlights on wet ceramic, soft window bounce` |
| `dynamic` | `fast lateral track ending on the hero label` |
| `professional` | `clean commercial tabletop, controlled reflection, no clutter` |

Stack 2–3 film/anchor references per prompt:
```
35mm handheld film camera, natural grain + DaVinci industrial-grade color grading + cold documentary style, natural light
```

---

## Scene Templates

### 1. Product Commercial

```
@Image1 (product hero shot), @Image2 (lifestyle angle), @Image3 (detail close-up).
Slow orbit around @Image1 on a minimalist pedestal against pure black background.
Soft box three-point lighting with rim light accent on product edges.
Clean commercial tabletop, controlled reflections, no clutter.
4K sharp details, gimbal-smooth motion. No jump cuts.
```

### 2. Character Narrative

```
@Image1 is the main character (identity anchor — preserve exactly).
@Image2 is the scene setting.
[Character] walks tiredly down the hallway, slowing steps, finally stopping at the door.
Close-up push-in on face — deep breath, shifts expression from weariness to calm.
Warm tungsten practical lighting from hallway sconces.
Natural ambient sound: footsteps, breathing, door creak.
```

### 3. Motion Transfer

```
@Image1 (character identity) performs the choreography from @Video1 (motion reference).
Setting: abandoned warehouse with dust particles in light beams.
Camera: wide establishing shot, then medium tracking as movement intensifies.
Natural light through broken windows, volumetric rays.
```

### 4. Multi-Shot Story (Shot Script Format)

```
[0:00–0:05] WIDE — Aerial view of volcanic island at sunrise, slow push in.
[0:05–0:12] MEDIUM — Researcher emerges from tent, looks toward volcano, rack focus to face.
[0:12–0:20] CLOSE-UP — Eyes reflecting distant glow, golden hour light, handheld slight tremor.
[0:20–0:27] ACTION — Dramatic eruption, ash cloud rolling, motion blur, camera shake.
[0:27–0:30] FREEZE/PULL-OUT — Final hero frame, title card reveal.

Style: BBC Planet Earth documentary, natural light, no jump cuts.
```

### 5. One-Shot / Long Take

```
Single continuous take, no cuts.
Camera begins wide on the alley entrance, slowly pushes forward past graffiti walls,
tracks right following a stray cat, rises to reveal the skyline at dusk.
Gimbal-smooth throughout. Natural fading light with neon signs flickering on.
Duration: 12 seconds.
```

### 6. Music Beat-Matching

```
@Image1 @Image2 @Image3 @Image4 @Image5 @Image6 @Image7 —
match the keyframe positions and overall rhythm of @Video1 for beat-synced cuts.
Characters with more dynamic movement.
Overall visual style more dreamlike with strong visual tension.
Adjust shot sizes and add lighting changes based on music and visual needs.
```

### 7. Dialogue / Lip-Sync

```
@Image1 is the speaker. @Audio1 is the dialogue track.
Close-up on @Image1 facing camera. Natural expressions.
Phoneme-level lip-sync to @Audio1: "[Dialogue text here]".
Tungsten key light, soft fill. Static shot, locked off camera.
Background: tech-styled study, shallow depth of field.
```

---

## Multi-Shot Sequence Workflow

For projects spanning multiple clips:

1. **Define the story objective** — final outcome, beats, scene groupings
2. **Set clip budget** — which beat goes in which clip
3. **Anchor consistency** — same character reference (`@Image1`) in every clip
4. **Track canonical state** — accepted footage defines reality; rejected footage is excluded
5. **Continuation rule** — review the actual end frame before writing the next clip
6. **Scene boundaries** — reset from canonical references at each scene change

### Sequence Invariants
- Same `@Image1` for character across ALL clips
- Describe only what changed from the previous clip
- Extension depth counter resets at scene boundaries
- Never leak future beats into current prompt
- Update continuity state after each accepted take

---

## Anti-Slop Checklist

Before delivering a prompt, verify:

- [ ] One visible beat (what we actually see happen)
- [ ] One motivated camera move (why it moves)
- [ ] One motivated light source (where light comes from)
- [ ] Sound intent (what we hear)
- [ ] Directing coherence (one intention; camera, light, performance serve it)
- [ ] No filler words: replace `cinematic`, `epic`, `beautiful`, `dynamic`, `professional` with concrete production language
- [ ] Every major phrase passes the visibility test (visible to camera, measurable by light meter, audible in mix, or observable as motion)
- [ ] Reference tags preserved exactly — never modify `@Image1` syntax
- [ ] Prompt within 40–110 words (single clip) or 60–100 words (production)

---

## Troubleshooting

| Problem | Root Cause | Fix |
|---------|-----------|-----|
| Character identity drifts | Scene variety too high | One environment per generation, same @Image1 in every prompt |
| Output feels chaotic | "fast-paced" keyword | Replace with `smooth pacing`, animate one element at a time |
| Motion unclear | Vague speed | Specify: `walked at 0.5x speed` not `walked slowly` |
| Lip-sync off | Ambiguous dialogue | Use brackets: `[Dialogue: "exact text here"]` |
| Camera too shaky | Unspecified stabilization | Add `gimbal-smooth` or `stabilized` |
| Quality drops in final seconds | Duration near limit | Keep clips under 10s even though cap is higher |
| Jitter / flicker | "fast" keyword | Avoid "fast"; keep one element moving at normal speed |
| Reference ignored | Uploaded but not @tagged | Check every asset has `@Image1`, `@Video1`, etc. in prompt |
| Face detection block | Realistic face in upload | Use stylized/illustrated references; route through third-party API |
| Twinning (duplicate people) | Complex multi-subject | One subject per scene |

### Retake Protocol

When a take comes back unsatisfactory:

1. **Keep** — it's good enough
2. **Fix in post** — minor issues fixable in editing
3. **Edit** — use Seedance Edit mode for targeted changes
4. **Re-roll** — same prompt, different seed
5. **Rewrite** — change ONE variable (one camera word, one light source, one constraint)
   - Never rewrite the whole prompt; iterate one change at a time
   - Generate 3–5 times before concluding a prompt doesn't work (output is stochastic)

---

## Seedance 2.0 vs 2.5

| Feature | 2.0 | 2.5 |
|---------|-----|-----|
| Max duration | 15s | 30s native single clip |
| Multi-shot coherence | Basic | Director-grade, single-pass |
| Character consistency | Good | Excellent (cross-shot) |
| Reference images | ≤ 9 | ≤ 30 |
| Reference videos | ≤ 3 (15s total) | ≤ 10 (30s total) |
| Reference audio | ≤ 3 | ≤ 10 |
| Video editing | Not supported | Background swap, object removal, style transfer |
| Output container | MP4 only | MP4 or MOV (high color-fidelity) |
| Audio sync | Present | Enhanced, tighter lip-sync |
| Physics | Standard | Improved cloth & fluid sim |

---

## Pro Tips

1. **Keep clips under 10 seconds** — quality drops noticeably in the final seconds even at higher caps
2. **Reference images are everything for consistency** — same face reference every time for character lock
3. **Use the multi-input system properly** — reference image + audio + text together, not just text
4. **Use Dreamina for testing** — free daily credits, don't pay for experiments
5. **Iterate small** — change one word or swap one reference, don't rewrite everything
6. **"Cut scene to..."** for multi-scene videos in a single clip
7. **Avoid the word "fast"** — it causes jitter. Keep one element fast if needed for pace
8. **Describe camera and subject movement separately** — avoids shaky output
9. **Use high-resolution references** — 2K or 4K images as input. Blurry in, blurry out
10. **Native audio is a feature** — let Seedance generate synced audio rather than adding it in post
11. **One subject per scene** — multiple subjects = inconsistent results
12. **For extension: duration = NEW portion** — not total length

---

## Quick Reference

### Prompt Compress (for character-limited surfaces)

```
Subj+Act+Scene+Cam+Light+Audio
@I1 identity @V1 motion @A1 music
One beat. One camera move. One light source.
Preserve @I1 exactly.
```

### Essential Camera Shortcuts
`push-in` `pull-out` `track-left` `track-right` `crane-up` `orbit` `handheld` `gimbal` `static` `rack-focus`

### Essential Light Shortcuts
`golden-hour` `tungsten` `chiaroscuro` `three-point` `neon` `natural-light` `butterfly` `under-lighting` `volumetric`
