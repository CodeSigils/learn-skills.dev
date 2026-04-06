---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, or applications. Generates creative, polished code that avoids generic AI aesthetics. Auto-detects project context (Rails+Inertia, standalone React, or plain HTML) and generates code that fits.
license: Complete terms in LICENSE.txt
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

## Step 0 — Detect Project Context

**Before generating any code**, detect which mode to use by checking the current working directory:

### Mode 1: Rails + Inertia (Auto-detected)

Activate when ALL of these exist:
- `Gemfile` contains `inertia_rails`
- `package.json` contains `@inertiajs/react`
- `app/frontend/pages/` directory exists

→ Jump to **"Rails + Inertia Mode"** section below.

### Mode 2: Standalone React (Vite SPA)

Activate when:
- The user asks for a standalone app, landing page, or marketing site
- No Rails+Inertia project is detected
- The user does NOT request plain HTML

→ Jump to **"Standalone React Mode"** section below.

### Mode 3: Plain HTML

Activate when:
- The user explicitly asks for "plain HTML", "single file", or "no framework"
- The project is a simple static page with no interactivity beyond CSS hover/scroll

→ Generate a single `index.html` with inline CSS/JS. Follow the Design Thinking and Aesthetics sections only.

---

## Rails + Inertia Mode

This mode generates code that integrates directly into a Rails + Vite + Inertia.js + React project. No merge step needed — code goes directly where it belongs.

### Discovery Phase

Before writing any code, read these files to understand the existing project patterns:

1. **Existing pages** — read 1-2 files in `app/frontend/pages/` to match conventions
2. **Layout system** — check `app/frontend/layouts/` to see available layouts
3. **Components** — check `app/frontend/components/ui/` for existing shadcn/ui components
4. **Types** — read `app/frontend/types/index.ts` for `SharedData`, `Auth`, `User` interfaces
5. **Hooks** — check `app/frontend/hooks/` for available hooks (`use-appearance`, `use-i18n`, etc.)
6. **Routes** — check `config/routes.rb` for routing patterns
7. **Tailwind** — check `tailwind.config.*` or `app/frontend/` CSS files for theme/design tokens
8. **Path aliases** — check `tsconfig.app.json` for `@/*` or `~/*` path aliases

### What to Generate

For each feature/page, generate ALL of these:

#### 1. React Page Component(s)
- **Location**: `app/frontend/pages/<feature>/` (e.g., `app/frontend/pages/store/index.tsx`)
- **Pattern**: TypeScript, functional component, props interface for data from Rails
- **Navigation**: Use `Link` and `router` from `@inertiajs/react` — NEVER use `react-router-dom`
- **Head**: Use `Head` from `@inertiajs/react` for page titles and meta tags
- **Shared data**: Access via `usePage<SharedData>()` for auth, flash, etc.
- **Layout assignment**: Set `PageComponent.layout = (page) => <Layout>{page}</Layout>` or use nested layouts

```tsx
// app/frontend/pages/store/index.tsx
import { Head, Link, usePage } from '@inertiajs/react'
import type { SharedData } from '@/types'
import DashboardLayout from '@/layouts/dashboard-layout'

interface StorePageProps {
  products: Product[]
}

export default function StorePage({ products }: StorePageProps) {
  const { auth } = usePage<SharedData>().props

  return (
    <DashboardLayout>
      <Head title="Store" />
      {/* page content */}
    </DashboardLayout>
  )
}
```

#### 2. Reusable Components
- **Location**: `app/frontend/components/<component-name>.tsx`
- **Use existing shadcn/ui** components from `app/frontend/components/ui/` — do NOT recreate buttons, dialogs, cards, etc.
- **Only create new components** for feature-specific UI that doesn't exist yet
- **Import pattern**: `import { Button } from '@/components/ui/button'`

#### 3. Rails Controller
- **Location**: `app/controllers/<feature>_controller.rb`
- **Inherit from**: `InertiaController` (or `ApplicationController` if that's the pattern)
- **Render pattern**: `render inertia: 'feature/index', props: { data: @data }`
- **Share data**: Use `inertia_share` for data needed across actions

```ruby
# app/controllers/store_controller.rb
class StoreController < InertiaController
  def index
    @products = Product.all
    render inertia: 'store/index', props: {
      products: @products.as_json(only: [:id, :name, :price, :image_url])
    }
  end
end
```

#### 4. Routes
- **Location**: Add to `config/routes.rb`
- **Pattern**: Match existing route style (resourceful or custom)

```ruby
# Add to config/routes.rb
resources :store, only: [:index, :show]
```

#### 5. TypeScript Types (if needed)
- **Location**: Add to `app/frontend/types/index.ts` or create a feature-specific type file
- **Pattern**: Export interfaces for props passed from Rails

### Styling in Rails+Inertia Mode

- **Use Tailwind CSS** — this is the project's styling system. Do NOT use CSS Modules or inline `<style>` tags.
- **Use existing design tokens** — check the Tailwind config for colors, spacing, fonts already defined
- **Use shadcn/ui components** for standard UI elements (buttons, inputs, cards, dialogs, dropdowns, etc.)
- **Custom styles**: Only add custom CSS in `app/frontend/` when Tailwind utilities are insufficient (complex animations, pseudo-elements). Use Tailwind's `@apply` sparingly.
- **Dark mode**: Use `dark:` Tailwind variant — the project likely already has theme switching via `use-appearance` hook
- **Icons**: Use `lucide-react` — it's already installed

### Inertia-Specific Patterns

```tsx
// Navigation — use Inertia Link, not <a> tags
import { Link, router } from '@inertiajs/react'
<Link href="/store" className="...">Store</Link>

// Programmatic navigation
router.visit('/store')
router.post('/store', { data })

// Forms — use Inertia useForm
import { useForm } from '@inertiajs/react'
const { data, setData, post, processing, errors } = useForm({ name: '' })

// Page title
import { Head } from '@inertiajs/react'
<Head title="Page Title" />

// Access shared data (auth, flash, etc.)
import { usePage } from '@inertiajs/react'
const { auth, flash } = usePage<SharedData>().props

// i18n (if the project uses it)
import { useI18n } from '@/hooks/use-i18n'
const { t } = useI18n()
```

### Public/Marketing Pages in Rails+Inertia

For landing pages or public-facing pages that don't need the app layout:
- Still create as Inertia pages (for SSR and consistency)
- Use a minimal layout or no layout (`page.default.layout = null`)
- Can be more creative with Tailwind — use arbitrary values, custom gradients, animations
- Import Google Fonts in the page component or add to `index.html`
- Place images in `public/` directory

---

## Standalone React Mode

For projects outside Rails — standalone landing pages, marketing sites, or apps deployable to Vercel/Netlify/Amplify.

### Project Setup

1. **Scaffold with Vite + React**:
   ```bash
   npm create vite@latest <project-name> -- --template react-ts
   cd <project-name>
   npm install
   ```

2. **Install Tailwind CSS**:
   ```bash
   npm install -D tailwindcss @tailwindcss/vite
   ```

   Add the plugin to `vite.config.ts`:
   ```ts
   import tailwindcss from '@tailwindcss/vite'

   export default defineConfig({
     plugins: [react(), tailwindcss()],
   })
   ```

   Replace the contents of `src/index.css` with:
   ```css
   @import "tailwindcss";
   ```

3. **Install shadcn/ui**:
   ```bash
   npx shadcn@latest init
   ```

   Accept defaults or configure to match the project. This creates `src/components/ui/` and a `cn()` utility in `src/lib/utils.ts`.

   Install components as needed:
   ```bash
   npx shadcn@latest add button card dialog input
   ```

4. **Install common dependencies as needed**:
   ```bash
   npm install motion                        # Animation
   npm install react-router-dom              # Routing (if multi-page)
   npm install lucide-react                  # Icons
   npm install react-intersection-observer   # Scroll animations
   ```

5. **Project structure**:
   ```
   src/
   ├── components/       # Reusable UI components
   ├── components/ui/    # shadcn/ui components
   ├── sections/         # Page sections (for landing pages)
   ├── lib/
   │   └── utils.ts      # cn() helper and utilities
   ├── assets/           # Images, fonts, SVGs
   ├── App.tsx
   ├── main.tsx
   └── index.css         # Tailwind imports + custom CSS layers
   ```

### Deployment Ready

- **Build**: `npm run build` → `dist/`
- Include `wrangler.jsonc` in the project root:
  ```jsonc
  {
    "name": "<project-name>",
    "compatibility_date": "2025-04-01",
    "assets": {
      "directory": "./dist"
    }
  }
  ```
- **Deploy to Cloudflare Pages**:
  ```bash
  npm run build && wrangler deploy
  ```
- Use `VITE_` prefixed env vars, document in `.env.example`
- See the **Image Strategy** section below for image handling.

### Component Strategy (Standalone)

- **Use shadcn/ui components** for all standard UI: buttons, inputs, cards, dialogs, dropdowns, tabs, tooltips, etc. Do NOT build custom versions of components that shadcn/ui provides.
- **Import pattern**: `import { Button } from '@/components/ui/button'`
- **Customization**: Modify shadcn/ui component files directly — they are copied into the project, not imported from a package.
- **Only create new components** for feature-specific UI that has no shadcn/ui equivalent.
- **Path alias**: Configure `@/` to point to `src/` in `tsconfig.json` (shadcn init handles this).

### Styling in Standalone Mode

- **Use Tailwind CSS** — all styling through utility classes. Do NOT use CSS Modules or separate `.css` files per component.
- **Custom CSS**: Only for things Tailwind cannot express — complex animations, pseudo-element content, `@font-face` declarations. Add these in `src/index.css` using Tailwind's `@layer` directive.
- **CSS custom properties**: Use sparingly for dynamic theming (e.g., color values set by JS). For static design tokens, prefer Tailwind config or CSS `@theme` directive.
- **Dark mode**: Use `dark:` Tailwind variant. Add `darkMode: 'class'` to config and toggle via a class on `<html>`.
- **Icons**: Use `lucide-react`.

### React Guidelines (Standalone)

- Functional components + hooks only
- `motion` library for animations — `<motion.div>` for enters, layout animations, gestures
- `useInView` from `react-intersection-observer` for scroll-triggered reveals
- Semantic HTML (`<header>`, `<main>`, `<section>`, `<footer>`)
- Tailwind responsive prefixes for layout adaptation (`md:`, `lg:`)
- `loading="lazy"` on below-fold images, explicit `width`/`height` attributes

---

## Design Thinking (All Modes)

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

### Context → Aesthetic Direction

Use the project's domain to anchor the aesthetic. These are starting points — break them when the user's brief demands it:

| Context | Default Direction | Key Characteristics |
|---------|-------------------|---------------------|
| B2B SaaS / Dashboard | Refined, clean, professional | Clarity over flair. Structured grids, muted palette, strong data hierarchy, generous whitespace. Subtle motion only. |
| Creative portfolio / Agency | Maximalist, experimental | Boundary-pushing layouts, oversized type, unexpected interactions, show-don't-tell craftsmanship. |
| E-commerce / Product | Luxurious or playful (match brand) | Product as hero. Lifestyle photography, smooth transitions, persuasive micro-copy, trust signals. |
| Developer tools | Technical, precise | Monospace accents, dark themes, code-block aesthetics, sharp edges, terminal-inspired UI. |
| Health / Wellness | Organic, soft, calming | Warm palettes, rounded shapes, generous whitespace, botanical or nature imagery, gentle motion. |
| Finance / Legal | Authoritative, structured | Conservative elegance, serif typography, navy/charcoal/gold palette, trust and credibility cues. |
| Startup / Landing page | Bold hero, energetic | Strong CTA hierarchy, gradient backgrounds, testimonial-driven, fast-paced scroll reveals. |
| Editorial / Blog | Magazine-like, reading-focused | Strong typographic hierarchy, pull quotes, columnar layouts, minimal distraction from content. |

### Design Brief

Before writing any code, draft a 3-4 line brief. This keeps the implementation focused:

1. **Aesthetic**: The chosen direction in one phrase (e.g., "brutalist editorial with warm accents")
2. **Typography**: The display + body font pairing (e.g., "Playfair Display / Source Sans 3")
3. **Color strategy**: Dominant, secondary, and accent — plus light/dark decision (e.g., "deep navy dominant, warm cream secondary, coral accent — dark theme")
4. **Memorable element**: The single detail a user will remember (e.g., "parallax grain-textured hero with a handwritten annotation overlay")

State the brief explicitly in your response before generating code. This is the contract — every code decision should trace back to it.

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working code that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines (All Modes)

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables or Tailwind config for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- **Motion**: Use animations for effects and micro-interactions. In React, prefer `motion` library. Focus on high-impact moments: one well-orchestrated page load with staggered reveals creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.

NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

Remember: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.

---

## Accessibility (All Modes)

Accessibility is not optional and not a separate pass — build it into every component from the start.

### Color & Contrast
- Meet WCAG AA minimum: 4.5:1 contrast ratio for normal text, 3:1 for large text (18px+) and UI components.
- Never rely on color alone to convey meaning — pair with icons, text, or patterns.
- Test contrast with browser DevTools or the axe extension.

### Focus & Keyboard
- Every interactive element must have a visible focus indicator. Never write `outline: none` without providing an equivalent replacement (e.g., `ring-2 ring-offset-2` in Tailwind).
- All functionality must be reachable via keyboard. Logical tab order following DOM structure.
- Custom components (dropdowns, modals, tabs) must implement full keyboard patterns (arrow keys, Escape to close, focus trap in modals).

### Semantic HTML
- Use proper heading hierarchy: one `<h1>` per page, then `<h2>` → `<h3>` — never skip levels.
- Use landmark regions: `<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>`.
- Use `<button>` for actions and `<a>` for navigation — never `<div onClick>`.
- Use `<ul>`/`<ol>` for lists, `<table>` for tabular data.

### ARIA
- Icon-only buttons must have `aria-label` (e.g., `<button aria-label="Close menu">`).
- Dynamic content updates need `aria-live="polite"` (toasts, status messages) or `aria-live="assertive"` (errors).
- Use `role` attributes only when semantic HTML is insufficient — prefer native elements.
- Modals: `role="dialog"`, `aria-modal="true"`, `aria-labelledby` pointing to the title.

### Screen Readers
- All images must have `alt` text. Decorative images get `alt=""`.
- Use Tailwind's `sr-only` class for labels that are visually hidden but needed by assistive tech.
- Form inputs must have associated `<label>` elements (or `aria-label` for icon inputs).

### Motion
- Wrap all animations in a `prefers-reduced-motion` check:
  ```css
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
      animation-duration: 0.01ms !important;
      transition-duration: 0.01ms !important;
    }
  }
  ```
  Or in React, use the `motion` library's `useReducedMotion()` hook to conditionally disable animations.

### Forms
- Every input needs a visible label — placeholder text is not a label.
- Error messages must be linked to their input via `aria-describedby`.
- Required fields: indicate visually AND with `aria-required="true"` or the `required` attribute.
- Group related fields with `<fieldset>` and `<legend>`.

---

## Responsive Design (All Modes)

### Mobile-First Approach
Write base styles for the smallest viewport (mobile). Layer up with Tailwind breakpoint prefixes: `sm:`, `md:`, `lg:`, `xl:`. Never write desktop-first styles and then override downward.

### Breakpoint Strategy
Follow Tailwind defaults — do not add custom breakpoints unless the design genuinely requires it:
- `sm`: 640px — large phones in landscape, small tablets
- `md`: 768px — tablets
- `lg`: 1024px — small laptops, tablets in landscape
- `xl`: 1280px — desktops

### Layout Adaptation
- **Columns**: Stack vertically on mobile, go side-by-side at `md:` or `lg:`. Use `flex flex-col md:flex-row` or CSS grid with responsive columns.
- **Navigation**: Full nav visible on `lg:`. Below `lg:`, use a hamburger menu opening a sheet/drawer (shadcn/ui `Sheet` component).
- **Spacing**: Reduce padding and margins on mobile. Example: `p-4 md:p-8 lg:p-16`.
- **Grid density**: Fewer columns on small screens. Example: `grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3`.

### Typography Scaling
Use Tailwind responsive prefixes for font sizes: `text-2xl md:text-4xl lg:text-6xl`. For fluid scaling, use `clamp()` in custom CSS:
```css
.hero-title { font-size: clamp(2rem, 5vw, 4.5rem); }
```

### Touch Targets
All interactive elements on mobile must be at least 44x44px. In Tailwind: `min-h-[44px] min-w-[44px]`. Buttons, links, form inputs, and icons that act as buttons all apply.

### Testing Mental Model
Design and visually verify at three viewport widths:
1. **Mobile**: 375px (iPhone SE / standard phone)
2. **Tablet**: 768px (iPad portrait)
3. **Desktop**: 1280px (standard laptop)

If the design works at these three, intermediate sizes will be handled by the fluid utilities.

---

## Image Strategy (All Modes)

### Image Generation

Generate images that match the aesthetic direction using available AI image generation tools.

**Check for `infsh` CLI availability** (from the `ai-image-generation` skill):
```bash
which infsh
```

If available, generate images using FLUX or Grok models (avoid Seedream for potentially sensitive content):
```bash
infsh app run falai/flux-dev-lora --input '{
  "prompt": "[aesthetic-matched prompt based on Design Brief]"
}'
```

**Image set to generate:**

| Image | Purpose | Aspect |
|-------|---------|--------|
| Hero background | Main visual impact, sets the mood | 16:9 or full-width |
| Feature/section visuals (2-3) | Supports content sections | 3:4 or 1:1 |
| CTA background (optional) | Atmospheric, subtle | 16:9 |

**Prompt engineering**: Base each prompt on the Design Brief — use the chosen aesthetic, color palette, and industry context. Never generate generic stock-photo-style images.

**Fallback chain**: If `infsh` is not available, check for the Social Toolkit `HiggsfieldImageTool` as an alternative. If no image generation is available, create the page with CSS-only atmospheric effects (gradients, noise textures, shapes) and note which images the user should add later.

**Save all generated images** to `public/images/` with descriptive filenames (e.g., `hero-abstract-dark.webp`, not `image1.png`). Generate at 2x the display size for retina screens.

### Optimization
- Prefer modern formats: WebP (universal support) or AVIF (smaller, growing support) with `<picture>` fallbacks for critical images.
- Add `loading="lazy"` on all images below the fold. Keep hero/above-fold images eager-loaded.
- Always set explicit `width` and `height` attributes to prevent Cumulative Layout Shift.

### SVG & Icons
- Use `lucide-react` for UI icons — it is the icon set for both modes.
- For custom illustrations or decorative graphics, prefer inline SVG over raster images.
- Optimize SVGs (remove editor metadata, unnecessary groups) before committing.

### Hero Images & Backgrounds
- Default to CSS-only solutions: gradients, `background-blend-mode`, SVG patterns, noise textures via data URIs.
- Only use raster hero images when photographic content is genuinely needed.
- When using a raster hero, apply a CSS overlay (gradient or color with opacity) to ensure text readability.
