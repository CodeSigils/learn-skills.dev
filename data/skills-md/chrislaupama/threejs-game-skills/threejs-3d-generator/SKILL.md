---
name: threejs-3d-generator
description: "Generate, texture, rig, animate, remesh, convert, and download 3D assets for Three.js games using the Meshy API. Use for text-to-3D, image-to-3D, 2D concept to 3D conversion, game-ready GLB/FBX assets, characters, creatures, buildings, props, weapons, terrain pieces, humanoid auto-rigging, animation-library clips, model retexturing, low-poly/quad remeshing, and browser asset pipelines. Pair with threejs-image-generator for concepts, texture references, sky/background/terrain textures, logos, icons, and GUI art before image-to-3D generation."
---

# Three.js 3D Generator

## Purpose

Create production-oriented 3D assets, then prepare them for Three.js games. This is the Three.js game system's 3D-generation layer; it uses Meshy as the provider for text-to-3D, image-to-3D, retexturing, humanoid rigging, animation-library clips, remeshing/conversion, and downloadable GLB/FBX outputs.

## API Key

Never store API keys in skill files or client-side game code. The script checks:

1. `--api-key`
2. `MESHY_API_KEY`

Step 0 before declaring the key unavailable:

```bash
bash ~/.claude/skills/threejs-game-director/scripts/probe_asset_credentials.sh
```

For Codex installs:

```bash
bash ~/.codex/skills/threejs-game-director/scripts/probe_asset_credentials.sh
```

Paste the literal `MESHY_API_KEY=SET|MISSING` output in the report. Do not conclude the key is unavailable from a plain non-interactive shell until this probe has sourced the user's shell profiles.

When the probe says SET but `threejs_3d_asset.py` reports a missing key, the key is exported in an interactive-only profile (e.g. `~/.zshrc`). Wrap script invocations the same way the probe does:

```bash
zsh -c 'source "$HOME/.zprofile" 2>/dev/null; source "$HOME/.zshrc" 2>/dev/null; python3 .../threejs_3d_asset.py ...'
```

Use the API only from local/server-side tooling. Generated model download URLs expire, so download outputs immediately after successful tasks.

## Tool Script

Reference gate:

- Load `references/api-notes.md` before provider API work, endpoint/task decisions, model choices, polling, retexture, remesh, rigging, animation, or download handling.
- Load `references/threejs-integration.md` before importing Meshy outputs into a browser game or advising GLB/FBX integration.
- Load `references/image-generator-workflows.md` before pairing `threejs-image-generator` with this skill for 2D concepts, texture references, UI art, logos, decals, or image-to-3D inputs.

Track required references in a reference ledger with yes/no, path, and failure reason. Do not mark an asset pipeline complete while a required reference is skipped.

Run from the user's current project directory:

```bash
python3 ~/.claude/skills/threejs-3d-generator/scripts/threejs_3d_asset.py --help
```

If installed in Codex instead of Claude, use:

```bash
python3 ~/.codex/skills/threejs-3d-generator/scripts/threejs_3d_asset.py --help
```

## Common Commands

Downloads default to the GLB model plus textures and thumbnail. Pass `--formats fbx,glb` for more formats or `--formats all` for everything Meshy produces (FBX/OBJ/STL/USDZ can be 4-5x the bytes).

Recommended premium game hero model (runs Meshy's preview stage, then the textured refine stage):

```bash
python3 ~/.claude/skills/threejs-3d-generator/scripts/threejs_3d_asset.py text \
  --prompt "game-ready [hero asset], strong readable silhouette, layered hard-surface detail, PBR materials, clean topology for browser game, centered pivot, 3/4 view, no text" \
  --ai-model latest \
  --wait --download --out-dir assets/models/hero
```

Text to 3D:

```bash
python3 ~/.claude/skills/threejs-3d-generator/scripts/threejs_3d_asset.py text \
  --prompt "game-ready sci-fi hover bike, sleek armored panels, readable silhouette, PBR, front facing" \
  --ai-model latest \
  --wait --download --out-dir assets/models/hover-bike
```

Image to 3D from a local `threejs-image-generator` concept:

```bash
python3 ~/.claude/skills/threejs-3d-generator/scripts/threejs_3d_asset.py image \
  --image assets/concepts/hover-bike-front.png \
  --ai-model latest \
  --wait --download --out-dir assets/models/hover-bike
```

Status and download (pass the task type that created the task):

```bash
python3 ~/.claude/skills/threejs-3d-generator/scripts/threejs_3d_asset.py status TASK_ID --task-type text-to-3d
python3 ~/.claude/skills/threejs-3d-generator/scripts/threejs_3d_asset.py download TASK_ID --task-type image-to-3d --out-dir assets/models
```

Retexture, remesh, rig, or animate:

```bash
python3 ~/.claude/skills/threejs-3d-generator/scripts/threejs_3d_asset.py retexture \
  --input-task-id TASK_ID \
  --texture-prompt "brushed gunmetal, orange hazard decals, worn edges" \
  --wait --download --out-dir assets/models/retextured

python3 ~/.claude/skills/threejs-3d-generator/scripts/threejs_3d_asset.py remesh \
  --input-task-id TASK_ID --target-polycount 20000 --formats glb \
  --wait --download --out-dir assets/models/lowpoly

# Rigging accepts TEXTURED HUMANOID models only (rig the refine task, not the preview).
python3 ~/.claude/skills/threejs-3d-generator/scripts/threejs_3d_asset.py rig \
  --input-task-id REFINE_TASK_ID --height-meters 1.8 --wait --download --out-dir assets/models/rig

# animate takes the RIG task ID plus an integer action ID from the Meshy
# animation library (https://docs.meshy.ai/en/api/animation-library).
# One action per task; the rig download already includes walk/run clips.
python3 ~/.claude/skills/threejs-3d-generator/scripts/threejs_3d_asset.py animate \
  --rig-task-id RIG_TASK_ID --action-id 0 \
  --wait --download --out-dir assets/models/animated
```

Animated character pipeline (preview -> textured refine -> rig -> animation clips -> downloads). Rigging is humanoid-only, so this pipeline is for bipedal characters; the rig step also ships free walking/running clips:

```bash
python3 ~/.claude/skills/threejs-3d-generator/scripts/threejs_3d_asset.py character-pipeline \
  --prompt "stylized cyber runner character, T-pose, full body, game-ready outfit, readable silhouette" \
  --action-ids 0,4 \
  --out-dir assets/models/cyber-runner
```

## Three.js Image Generator Pairing

Use `threejs-image-generator` before 3D generation when the asset benefits from a strong 2D reference:

- Character concept, full-body T-pose/A-pose, front/side/back variants.
- Building, prop, vehicle, weapon, pickup, enemy, obstacle, or terrain tile reference.
- Style sheet for a whole asset family.
- Texture references: terrain, rock, metal, fabric, decals, skyboxes, backgrounds, UI materials.
- Logos, faction marks, pickup icons, hazard signs, cockpit decals, HUD symbols, and GUI panels.

Load `references/image-generator-workflows.md` for prompt patterns before generating or editing 2D inputs.

## Three.js Integration

Load `references/threejs-integration.md` before importing Meshy outputs into a browser game. In short:

- Prefer GLB/PBR outputs for Three.js.
- Use `GLTFLoader` for loading.
- Use `AnimationMixer` for rigged/animated GLBs.
- Keep generated model files out of client-side API flows; generation is a tooling step.
- Inspect triangle count, texture count, material count, file size, scale, pivot, bounds, and animation clips.
- Use generated 3D assets as hero/high-fidelity content, then build surrounding prop kits procedurally or with additional `threejs-3d-generator` / `threejs-image-generator` passes.

## Rigging and Animation Reliability

Load `references/api-notes.md` for the full parameter tables. The rules that prevent most failures:

- Rigging accepts HUMANOID (bipedal) models only, with clearly defined limbs. There are no creature rig types: plan quadrupeds, fliers, and other body plans as procedural motion in Three.js or external animation pipelines.
- Rigging requires a TEXTURED model. In the text-to-3D chain, rig the refine task ID — a preview task is untextured and will be rejected.
- Rigging caps at 300,000 faces for `input_task_id`; run `remesh` first if the model is heavier.
- Generate characters in a clean full-body T-pose or A-pose (`--pose-mode t-pose`), arms away from body, symmetric, no props fused to the silhouette. Verify the downloaded thumbnail actually shows a complete, clearly-limbed humanoid before rigging; regenerate if not.
- Set `--height-meters` to the character's intended real-world height; it scales the skeleton.
- A pose-estimation failure returns HTTP 422 and refunds the credits — the fix is regenerating with a clearer humanoid silhouette, not retrying the same model.
- The rig result already includes free walking and running clips (GLB + FBX + armature-only). Only spend animation credits on clips the library adds (idle, attack, dance, etc.).
- Animation tasks take the RIG task ID plus one integer `action_id` from the animation library (595+ actions: https://docs.meshy.ai/en/api/animation-library). One clip per task.
- Each animation download is a self-contained skinned GLB/FBX. To drive one character with many clips, load each animation GLB and reuse its `animations[0]` on the shared skeleton — see `threejs-integration.md`.
- A SUCCEEDED rig can still have warped skinning. The `character-pipeline` runs keyframe QA on the free walk/run clips before buying action clips (override with `--force`); run it standalone on any clip with `threejs_3d_asset.py validate-animation clip.glb` (flags scale tracks, limb-stretch translations, extreme rotations).
- After download, inspect `gltf.animations` clip names and counts before wiring the `AnimationMixer`, and verify motion visually in the engine.

## Quality Rules

- Improve the user's prompt with material, silhouette, camera/readability, scale, and game-use constraints.
- For riggable characters, include full-body T-pose or A-pose in the prompt (or `--pose-mode`) or create a T-pose reference image first.
- For Three.js games, request GLB/PBR and a `--target-polycount` matched to the performance budget.
- For mobile/browser games, favor `--lowpoly`, a lower `--target-polycount`, or a later `remesh` pass when the asset is too expensive.
- Always download output URLs immediately after success; they expire.
- Report the credential probe output, reference ledger, task IDs, output paths, ai_model, texture/polycount settings, animation action IDs, remesh settings, Three.js import notes, and any missing/failed steps.
