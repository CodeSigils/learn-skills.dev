---
name: product-launch-video
description: Produce a launch/marketing film - a Remotion timeline cut over real product footage captured by driving the running app headlessly. Use when asked for a product demo video, launch film, hero video, landing-page video, marketing video, product trailer, or a screen recording of the app turned into something polished. Covers the capture pipeline, the editorial rules, and the traps that silently produce broken footage.
---

# Product launch video

Produces a ~40s film where **motion graphics carry the narrative and every "product"
pixel is really rendered by the real app**.

This exists because of a false choice people keep making:

- A pure motion-graphics film looks professional but **proves nothing** - no real product.
- A raw screen recording proves everything but **looks amateur** - no motion design.

The answer is neither: Remotion is the master timeline, and the product shots are real
frames captured by driving the actual app in a headless browser.

Build a small Remotion project beside the product: shared capture toolkit +
primitives, one directory per app's film (brand, shots, capture script, timeline).
See `references/toolkit.md` for the recommended layout.

---

## Non-negotiables

Read these before writing any code. Each one cost real debugging time, and every one
fails **silently** - you get plausible-looking output that's wrong.

### Capture

| Trap | What happens | Fix |
|---|---|---|
| `setViewport({deviceScaleFactor: 2})` | `page.screencast()` measures its ffmpeg filter chain at the *system* DPR, so it builds a 1× chain and throws away the retina detail. No error. | Force it at the browser: `--force-device-scale-factor=2` + `deviceScaleFactor: 0` in the viewport (`0` = "system default"). |
| Headless renders **no cursor** | `page.mouse.move()` dispatches CDP events the page sees, but nothing is ever painted. | Inject a DOM cursor via `evaluateOnNewDocument`. Put it *in the page*, not composited in Remotion - then every Remotion transform (frame inset, zoom punch) scales it exactly like a real recording. A sprite requires inverting every transform, and 6px of drift reads as broken. |
| Headless has **no GPU** | Any WebGL/three.js content records as a blank or black panel. | `--use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader`. Verify with a pixel readback, not just "did a context exist". |
| SwiftShader also **composites the page** | A software GL driver compositing 2560x1440 caps the whole tab at ~8fps, so every animated shot records as a slideshow. It reads as a slow product, not a broken capture, so nobody suspects the flags. | Add `--disable-gpu-compositing`. Skia's CPU rasteriser is much quicker at plain 2D, WebGL still works, and A/B stills are identical. Measured on the same page: 8.2fps → 60.1fps. |
| Judging smoothness **by eye** | Duplicated frames look fine in a contact sheet and fine scrubbing one frame at a time. Only playback gives it away, and by then it's rendered. | Count *distinct* frames: `ffmpeg -i take.mp4 -vf mpdecimate,showinfo -f null - 2>&1 \| grep -c pts_time`. Well under the file's frame count means stutter. |
| `page.mouse.click(x, y, {clickCount: 2})` | Sends **one** press carrying clickCount metadata. Chrome never synthesizes `dblclick`. Two discrete clicks 60ms apart don't either. | If the app needs a real `dblclick`, click for the visible cursor motion then dispatch the event inside the frame at the element's own coords. |
| `page.keyboard.type()` after clicking into an iframe | Keys go to whatever the **parent** page focused. If the parent forwards keys to the app (arrow-key nav, shortcuts), your typing silently drives the UI instead of entering text. | Type into the frame: `frame.type(selector, text)`. |
| `evaluateOnNewDocument` doing DOM work | Runs at document-start where `document.head` **and** `document.documentElement` can both be null. An unguarded `appendChild` throws and silently aborts everything after it in that script. | Guard, and defer to `DOMContentLoaded`. |
| Recording the navigation | Buries the useful seconds deep into the file and bloats the mezzanine. | Split each shot into `setup` (not recorded) and `action` (recorded). |
| Trusting marker timestamps | Screencast is variable-frame-rate; the encoded timeline **compresses** relative to wall clock, so a marker at 22s is not at 22s in the file. | Use markers to find *roughly* where to look, then pick `startAt` by extracting frames and looking. |
| Remote/hotlinked assets | Third-party CDNs intermittently refuse the capture browser; image grids paint as empty transparency checkerboards, which reads as a broken product. | Wait for images and **warn**, then frame the shot to avoid them. Don't ship a take with blank art. |
| `window.scrollTo` in an app shell | Many shells scroll an inner element (`<main class="overflow-y-auto">`), not the window. Scrolling the window is a silent no-op and the shot never moves. | Find the real scroller and set its `scrollTop`. |
| Guessing click coordinates | Apps often only accept interactions on specific nodes - e.g. an inline editor that only accepts *leaf* elements (`childElementCount === 0`) while headings wrap their text in spans. Clicking the visually obvious target does nothing. | Read the app's own source for the rule, then ask the page where its valid targets are (`frame.evaluate`) and map frame coords → page coords via the iframe's measured box. |

### Rendering

| Trap | What happens | Fix |
|---|---|---|
| Skipping the mezzanine transcode | Remotion seeks arbitrarily; with a normal GOP every seek decodes from the previous I-frame. A 3-minute render becomes 40. | Transcode to **all-intra**: `-c:v libx264 -crf 14 -g 1 -keyint_min 1 -sc_threshold 0 -pix_fmt yuv420p`, plus explicit `bt709` tags so Chrome doesn't shift the brand colour. |
| `page.screencast({format:'mp4'})` | Emits VP9 inside a fragmented MP4 - badly supported. | `format: 'webm'`, then transcode. |
| `<TransitionSeries>` with a beat grid | Transitions **overlap**, so total duration = sum of sequences − sum of transitions. Your frame grid silently drifts. | For a frame-exact cut use explicit `<Sequence from/durationInFrames>` and do dissolves locally. Assert the chain sums to the total. |
| A `<Sequence>` longer than its source | Freezes on the last decoded frame - reads as a stall, not an error. | Bound every duration by the real take length. Record source durations in a comment. |
| `premountFor` on overlapping sequences | A premounted sequence renders early *on top of* the current one - you get ghosted double-exposed text. | Don't premount sequences that share screen space; premount only across hard cuts. |
| Overlays positioned in composition space | If the footage component crops and scales the plate internally, a mask or highlight placed in composition coordinates will not line up with anything in the frame - edges cut through the content. | Put overlays inside the same transform as the plate, or do the treatment natively instead of over footage. |
| `Math.random()` / `Date.now()` in a composition | Re-rolls every frame; text flickers. Remotion renders each frame independently. | Make all randomness a pure function of the index (a `sin`-based hash). |
| CSS animations / transitions / Tailwind `animate-*` inside Remotion | Render frozen or garbage - Remotion drives time via `useCurrentFrame()`, not wall clock. | Rebuild motion on `useCurrentFrame()`. This also means you generally **cannot** reuse the marketing site's animated components. |
| Building a loop by offsetting into the film | Two seam bugs: a black flash if the range opens on a dissolve, and a hard jump cut where it wraps. | Give the loop its own composition and cross-fade its tail into a `<Freeze frame={0}>` of its own head. Choose a *continuously moving* shot; anything that dwells is near-static and bad to autoplay. |

---

## Process

### 1. Establish product truth *before* designing the film

**The single most important step.** Read the code for every capability the film intends
to claim. Marketing pages illustrate aspirations; do not assume the product does what its
own landing page animation implies.

It has already happened once: a film's planned centrepiece was taken from an animated
component on the marketing site showing one document morphing through four different
aspect ratios. The product hardcoded a single aspect ratio and a fixed export stage - the
component was an illustration of an idea, not a feature. Building the money shot on it
would have put an unsupported claim on the homepage.

Check, specifically:
- Which content actually renders? Old records may be un-renderable by the current engine.
- Which routes need auth? Which redirect without prior state?
- What does each interactive feature actually require to engage?

### 2. De-risk the pipeline with the smallest possible test

In order, before building anything on top:
1. Prove the capture geometry (corner-marked page → is the file really 2×?).
2. Prove auth (can the browser reach a signed-in route?).
3. Prove WebGL if any 3D is involved.
4. Prove one interaction end to end.

### 3. Scout, don't guess

Screenshot every candidate surface and **show the user a contact sheet** before spending
time on video takes. Content choice dominates production value: mediocre demo content
makes a beautiful film an advert for a mediocre product.

### 4. Pick the demo content deliberately

Prefer **the product's own brand**. Featuring a recognisable third party is more
persuasive but puts someone else's trademark on the homepage, and swapping one third
party for another doesn't change that. Self-referential content also closes the loop: the
artefact selling the tool was made by the tool.

If the content doesn't exist yet, **creating it is a design job, not a capture job** - it
is every frame of the film's back half. Draft it deliberately, produce a few candidates,
and let the user pick.

### 5. Cut to a grid

120 BPM ⇒ 1 bar = 60 frames = 2s at 30fps. Land every cut on a multiple of 30 and every
act boundary on 60. Costs nothing, and cutdowns fall out for free.

### 6. Verify by looking

After every render, extract frames and **actually look at them**. Build a labelled
contact sheet. Every real defect found so far - blank logos, a shot showing the wrong
page, a caption illegible on a light panel, a dark band from a mis-measured crop, a mask
seam through a label - was found by looking at frames, not by any test passing.

Watch it **muted**, since that's how it will autoplay.

---

## Editorial rules

These are what separate a film that works from one that's good.

**Every claim on screen must be supported by the footage next to it.** One cut had "Share
a link" over footage where nothing showed sharing. Either show it or state it plainly on a
card - don't imply.

**Watch for claims that are honest in context but not at video scale.** A figure labelled
*"illustrative"* in small type becomes a hard assertion the moment it's a held hero frame
in a marketing film. Keep those out of held frames.

**Quote the product's motion, don't reinvent it.** Lift the app's own easing curve and
entrance vocabulary. One curve for everything that enters or lands. Nothing bounces -
overshoot reads as hesitation.

**Two grounds, never mid-grey.** A dark ground for statements, a light one for
explanations. Pick them from the product's own tokens.

**One accent, spent sparingly** - the caret, the one word carrying the sentence, a state
changing. Not decoration.

**Nothing in frame that isn't for the audience.** Real email addresses, org names, the
operator's own conversation with an in-app assistant, dev-mode badges. Prefer the app's
own mechanisms (cookies for a collapsed sidebar or a dismissed banner) over CSS hacks -
no flash on camera.

**A "money shot" earns the most time.** Pick the one moment showing something competitors
*structurally cannot do*, then: lock the camera, no cuts, no text over it, and let the
music drop out. Stillness tells the eye the subject is moving, not the camera. Put the
explanatory line *after* it - text before the reaction tells people what to think.

**Legibility beats coverage.** A shot spread across four screens can leave none of them
readable. Dwelling on one is usually better.

**Build the beat rather than filming it when the UI can't perform.** A static screen
cannot introduce three things one at a time. If the beat needs sequencing the product
doesn't do, compose it natively in Remotion using the product's real copy and tokens -
and keep it visually distinct from the footage so it reads as an explainer, not a fake
screenshot.

**If there's no voiceover, the cards carry 100% of the meaning.** Budget reading time.

---

## Discuss with the user, don't decide alone

- **Slogans and on-screen copy.** Offer several options grouped by angle, with a
  recommendation and the reasoning. Note that the film wants a *demo cue* while a website
  headline wants a *durable positioning statement* - they don't have to be the same line.
- **Which content to feature** - show the contact sheet.
- **Music.** You cannot license a track. Design the film to work silent and ship a cue
  sheet (BPM, where any drop lands) so a supplied track drops onto the grid later. When
  one arrives, check its shape before placing it: measure loudness over time rather than
  assuming it has an intro or a drop to align to.
- **Remotion licensing.** Free for individuals, non-profits and companies up to 3
  employees; above that a commercial licence is required. Flag it before it ships.

---

## Commands (shape)

Capture never starts a server and never guesses a port — auth URLs are usually pinned.

```bash
# terminal 1 — product already serving
pnpm --filter <app> dev   # or equivalent

# terminal 2 — film project
pnpm install
pnpm check-webgl          # if any 3D
pnpm capture:<app>        # or one shot: pnpm capture:<app> <shot>
pnpm mezzanine:<app>      # mandatory — see traps
pnpm studio
pnpm render:<app>         # mp4 / webm / loop / poster as needed
```

Auth for signed-in surfaces: prefer borrowing a live session cookie over signing up a
throwaway user (empty accounts force slow content generation before every shoot).

---

## Shipping to a page

Two shapes, and it's the user's call:

- **Short loop, click for the film.** Lightest - a few hundred KB autoplays, the full
  film is only fetched on demand. Best when page weight matters.
- **The full film, autoplaying muted and looping.** Heavier (megabytes for anyone who
  scrolls to it) but it *is* the film, and the sound toggle just unmutes.

Either way:

- **One `<video>` element, not two.** Swapping between two elements in a conditional lets
  React patch the existing DOM node instead of replacing it - and changing `<source>`
  children on a live `<video>` does **not** reload it. Toggle `muted` on a single element,
  or force a remount with distinct `key` props.
- `muted loop playsInline autoPlay` **together**, or iOS Safari refuses.
- `preload="metadata"`, never `auto`, or you wreck LCP. Start it on an
  IntersectionObserver so visitors who never scroll there pay nothing.
- Respect `prefers-reduced-motion` by rendering only the poster.
- Verify in a real browser and assert on `currentSrc`, not just "is it playing".
