---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications (examples include websites, landing pages, dashboards, React components, HTML/CSS layouts, or when styling/beautifying any web UI). Generates creative, polished code and UI design that avoids generic AI aesthetics.
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise. For complex timelines, orchestrated sequences, or scroll-driven scenes, consult the **animation-specialist**, **gsap**, or **gsap-scrolltrigger** skills.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.

NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

Remember: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.

---

## Related Skills

Frontend-design is the creative director — it sets the aesthetic vision and produces the full interface. The skills below are specialists to call in once the design direction is established or when a particular domain needs deeper expertise.

### css-design
The deep implementation layer for everything styling-related. Reach for this when the task is primarily about CSS architecture — complex layout with subgrid or container queries, intricate pseudo-element work, CSS custom properties / design tokens, advanced selector logic, fluid typography with `clamp()`, or WCAG-compliant colour contrast calculations. If frontend-design is the art director, css-design is the master craftsperson who knows every CSS spec edge case.

**Use alongside frontend-design when:** the interface needs production-grade CSS that has to be maintainable, responsive across many breakpoints, or technically precise about browser support.

### animation-specialist
Covers the full spectrum of motion: CSS keyframes, Web Animations API, spring physics, SVG morphing, canvas animation, Three.js motion, and the mathematical theory behind easing and choreography. Use it when motion is a primary concern — not just a flourish — and you want to reason carefully about timing, sequencing, and what makes animation feel alive versus mechanical.

**Use alongside frontend-design when:** the project is heavily motion-driven (animated landing page, interactive data story, character animation) or you need help structuring a complex multi-element choreography.

### gsap
Professional-grade animation using the GreenSock Animation Platform. Covers timelines, staggered reveals, `SplitText`, `MorphSVG`, and other GSAP plugins. The right choice when the project calls for precisely orchestrated, high-performance sequences across many elements.

**Use instead of animation-specialist when:** GSAP is the confirmed library and you need plugin-level guidance or a production-ready timeline implementation.

### gsap-scrolltrigger
Scroll-based animation using GSAP's ScrollTrigger plugin — pinned sections, scrub-linked animations, snap points, and parallax. Use when scroll position drives the narrative or visual state of the page.

**Use alongside frontend-design when:** the layout includes scroll-driven storytelling, sticky hero sections, or progress-linked reveals.

### web-visual-effects
GPU-accelerated visual experiences: WebGL/WebGPU shaders, particle systems, post-processing effects, procedural backgrounds, glassmorphism done properly, and hardware-accelerated canvas work. Use when you need effects that CSS and SVG can't produce — custom fragment shaders, 3,000-particle simulations, real-time noise fields.

**Use alongside frontend-design when:** the aesthetic calls for a striking visual centrepiece (hero background, generative texture, shader-based overlay) that requires GPU rendering.

### web-components
Native Custom Elements, Shadow DOM, HTML Templates, and Slots — reusable encapsulated UI components without any framework. Use when the deliverable is a distributable component that works in any HTML context, or when the project explicitly avoids React/Vue/Angular.

**Use instead of framework-specific component code when:** portability and encapsulation are requirements, or the user asks for "no framework".

### svg-graphics
Scalable, accessible, theme-aware SVG — icons, illustrations, decorative marks, animated paths, and SVG-as-UI. Use when the design calls for custom vector artwork, logo integration, or SVG animation (SMIL, CSS, or JS-driven path morphing).

**Use alongside frontend-design when:** the interface includes custom icons, illustrated sections, decorative borders, or any vector graphic that needs to scale across resolutions.

### accessibility-patterns
WCAG guidelines, semantic HTML, ARIA patterns, keyboard navigation, focus management, colour contrast, and screen-reader compatibility. Use whenever the interface must meet accessibility standards — which is essentially always for production work.

**Use alongside frontend-design when:** the interface will be used in a professional, public, or regulated context, or when the user mentions a11y, WCAG, screen readers, or keyboard navigation.

### brainstorming
Explores user intent, design requirements, and feature scope before committing to implementation. Use before building anything whose purpose, audience, or scope isn't fully defined.

**Use before frontend-design when:** the user hasn't specified what they want to build, or when a novel feature/component needs its requirements clarified before writing a single line of code.
