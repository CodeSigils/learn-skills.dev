---
name: design
description: Creative web design intelligence. Use when the user wants to build a website, landing page, portfolio, or any web interface that should look designed, not generated. Pre-trained with intelligence from 24 award-quality sites.
---

# design — Creative Web Design Intelligence

Build expressive, non-generic websites. Pre-trained with design intelligence from 24 award-quality sites.

## MANDATORY: Read References Every Time

**Every time this skill is invoked — including re-invocations, "build it now", "try again", or "based on my previous prompt" — you MUST read the reference files and taste folder before writing any code.** Do not rely on memory or prior conversation context for design decisions. The references ARE the skill. Without them you're just guessing.

If you're about to write HTML/CSS and you haven't read at least `design-intelligence.md`, `baselines.json`, `creative-vision.json`, `effects-vocabulary.json`, `fonts.json`, and `anti-patterns.json` in THIS invocation — STOP and read them first.

## Reference Files

Read ALL of these before designing:
- `${CLAUDE_SKILL_DIR}/references/design-intelligence.md` — 9 core principles (content IS the design, effects support never star)
- `${CLAUDE_SKILL_DIR}/references/baselines.json` — data-driven defaults from 24 sites (typography, animation, scroll patterns)
- `${CLAUDE_SKILL_DIR}/references/effects-vocabulary.json` — 30+ effects with implementation code
- `${CLAUDE_SKILL_DIR}/references/creative-vision.json` — 12 metaphor-to-design mappings, 10 archetypes, 10 hero types
- `${CLAUDE_SKILL_DIR}/references/fonts.json` — 40+ curated fonts with avoid list
- `${CLAUDE_SKILL_DIR}/references/anti-patterns.json` — 20+ patterns that make sites look AI-generated

Sub-skill references (read as needed):
- `${CLAUDE_SKILL_DIR}/references/taste.md` — taste analysis process
- `${CLAUDE_SKILL_DIR}/references/layout.md` — hero experiences, page archetypes, composition
- `${CLAUDE_SKILL_DIR}/references/motion.md` — scroll storyboarding, animation timing, reliable patterns
- `${CLAUDE_SKILL_DIR}/references/atmosphere.md` — grain, texture, cursors, preloaders
- `${CLAUDE_SKILL_DIR}/references/effects.md` — image-to-particle, WebGL, canvas techniques
- `${CLAUDE_SKILL_DIR}/references/audit.md` — scoring, inspiration routing, stack scaffolding

## Harness (reference site analysis)

To make the library smarter over time:
```bash
node ${CLAUDE_SKILL_DIR}/templates/learn.js --capture-and-learn "[URL1]" "[URL2]"
```

## Build Process: Gather → Understand → Propose → Build → Deliver

**You MUST follow these steps in order. Never skip to Build.**

### 1. Gather
- Create `taste/inspos/` and `taste/assets/` at the PROJECT ROOT if they don't exist
- **STOP and prompt the user.** Tell them:
  > I've created a `taste/` folder in your project root. Before I start designing, populate it so I can build something that actually reflects your taste:
  >
  > **taste/inspos/** — drop in moodboard images, screenshots of sites you love, visual references. Add an `inspos.txt` with reference URLs (one per line) and I'll analyze them.
  >
  > **taste/assets/** — drop in your real content: project images, logo, team photos, hero imagery. Every asset here will appear in the final design.
  >
  > Let me know when you've added your files, or tell me to proceed without them.
- **WAIT for the user to respond.** Do NOT continue to Step 2 until either:
  - The user confirms they've added files (then read everything in `./taste/inspos/` and `./taste/assets/`)
  - The user explicitly says to proceed without a taste folder (e.g. "skip it", "just go", "I don't have any")
- If `taste/inspos/` and `taste/assets/` already have files from a previous run, read them — but still confirm with the user that they're ready.
- Read all moodboard images from `./taste/inspos/`
- Read all assets from `./taste/assets/`
- Also check: did the user paste URLs or attach images directly in the conversation? Use those too.
- Read the user's brief from conversation
- **MANDATORY: Run the capture harness on EVERY reference URL.** Check these sources for URLs:
  1. `./taste/inspos/inspos.txt` — read this file, one URL per line
  2. Any URLs the user pasted in the conversation
  3. Any URLs passed as arguments to `/design`

  For EACH URL found, run:
  ```bash
  node ${CLAUDE_SKILL_DIR}/templates/capture-scroll.js "THE_URL_HERE" "/tmp/scroll-capture"
  ```
  Then READ the captures (screenshots, `scroll-analysis.json`, frame images). These contain the exact design tokens, typography, animation timing, and layout patterns from the reference site. This data is critical — it's the difference between a generic build and one that actually reflects the reference.

  After reading all captures, clean up: `rm -rf /tmp/scroll-capture`

  **If you skip the harness, you are ignoring the user's most important input.**

### 2. Understand
- **Read ALL 6 core reference files listed above.** This is not optional.
- Read `${CLAUDE_SKILL_DIR}/references/design-intelligence.md` — content IS the design, effects support never star
- Read `${CLAUDE_SKILL_DIR}/references/baselines.json` — nav: 15.7px, body: 16.1px, transitions: 0.8s, easing: cubic-bezier(0.4,0,0.2,1), scroll start: '0% 90%'
- Match to `${CLAUDE_SKILL_DIR}/references/creative-vision.json` — metaphor, archetype, hero type
- Select fonts from `${CLAUDE_SKILL_DIR}/references/fonts.json` — check avoid list
- Auto-select effects from `${CLAUDE_SKILL_DIR}/references/effects-vocabulary.json` based on energy
- Check against `${CLAUDE_SKILL_DIR}/references/anti-patterns.json` — if your plan matches any anti-pattern, change it
- Re-read the moodboard images and taste assets. Cross-reference what you see with what the references suggest.
- **No defaults.** Every decision from the user's inputs. If your plan sounds like your last build, re-read the moodboard.

### 3. Propose
Present your direction BEFORE building:
1. "Here's what I see in your references: [specific]"
2. "Here's what I'd build: [color, type, layout, energy]"
3. "Does this feel right?"
WAIT for approval.

### 4. Build
- Detect tech stack (vanilla HTML, React, Next, Astro, Svelte, Vue)
- Write a scroll storyboard as a comment (frame by frame, not sections)
- Use real assets from `./taste/assets/` — every image appears on the page
- Apply effects from vocabulary. Minimum: blur-in on images, masked reveal on headings, underline sweep on links, hover parallax, smooth scroll.
- Use baselines for values: scroll triggers at `start: '0% 90%'`, transitions at 0.8s, easing `cubic-bezier(0.4,0,0.2,1)`
- Place output where the user's stack expects it

### 5. Deliver
Self-check before presenting to the user:
- Does this reflect the moodboard, not a template?
- Are all assets from `./taste/assets/` used?
- Are all interactions working?
- Is the layout DIFFERENT from the last project?
- Does the code use values from `baselines.json` (not invented defaults)?
- Do the effects come from `effects-vocabulary.json` (not generic CSS)?
- Is the font from `fonts.json` and NOT on the avoid list?
- Would this pass the `anti-patterns.json` check?
