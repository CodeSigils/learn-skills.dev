---
name: tailwindcss-mobile-first
description: Comprehensive mobile-first responsive design patterns with 2025/2026 best practices for Tailwind CSS v4
---

# Mobile-First Responsive Design (2025/2026)

## Core Philosophy

Mobile-first design is the **industry standard for 2025/2026**. With mobile traffic consistently exceeding 60% of global web traffic and Google's mobile-first indexing, starting with mobile ensures optimal user experience and SEO performance.

### The Mobile-First Mindset

```html
<!-- CORRECT: Mobile-first (progressive enhancement) -->
<div class="text-sm md:text-base lg:text-lg">Start small, enhance upward</div>

<!-- INCORRECT: Desktop-first (graceful degradation) -->
<div class="text-sm md:text-base lg:text-lg">
  Starts large, reduces down (more code, more bugs)
</div>
```

**Key Principle**: Unprefixed utilities apply to ALL screen sizes. Breakpoint prefixes apply at that size AND ABOVE.

## 2025/2026 Breakpoint Strategy

### Tailwind's Default Breakpoints

| Prefix | Min-width      | Target Devices               |
| ------ | -------------- | ---------------------------- |
| (none) | 0px            | All mobile phones (base)     |
| `sm:`  | 640px (40rem)  | Large phones, small tablets  |
| `md:`  | 768px (48rem)  | Tablets (portrait)           |
| `lg:`  | 1024px (64rem) | Tablets (landscape), laptops |
| `xl:`  | 1280px (80rem) | Desktops                     |
| `2xl:` | 1536px (96rem) | Large desktops               |

### Content-Driven Breakpoints

**Best Practice 2025/2026**: Let content determine breakpoints, not device dimensions.

```css
@theme {
  /* Override defaults based on YOUR content needs */
  --breakpoint-sm: 36rem; /* 576px - when your content needs more space */
  --breakpoint-md: 48rem; /* 768px */
  --breakpoint-lg: 62rem; /* 992px - common content width */
  --breakpoint-xl: 75rem; /* 1200px */
  --breakpoint-2xl: 90rem; /* 1440px */

  /* Add custom breakpoints for specific content needs */
  --breakpoint-xs: 20rem; /* 320px - very small devices */
  --breakpoint-3xl: 120rem; /* 1920px - ultra-wide */
}
```

### Screen Coverage Strategy

```html
<!-- Cover the most common device ranges (2025/2026 data) -->

<!-- 375px-430px: ~50% of mobile devices (iPhone, modern Android) -->
<div class="px-4">Mobile base</div>

<!-- 768px+: Tablets and small laptops -->
<div class="px-4 md:px-6">Tablet enhancement</div>

<!-- 1024px+: Desktop experience -->
<div class="px-4 md:px-6 lg:px-8">Desktop enhancement</div>

<!-- 1440px+: Wide desktop experience -->
<div class="px-4 md:px-6 lg:px-8 xl:px-12">Wide desktop</div>
```

## Fluid Typography System

### CSS Clamp for Smooth Scaling

Fluid typography eliminates jarring size jumps between breakpoints:

```css
@theme {
  /* Fluid typography scale */
  --text-fluid-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);
  --text-fluid-sm: clamp(0.875rem, 0.8rem + 0.375vw, 1rem);
  --text-fluid-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
  --text-fluid-lg: clamp(1.125rem, 1rem + 0.625vw, 1.25rem);
  --text-fluid-xl: clamp(1.25rem, 1rem + 1.25vw, 1.5rem);
  --text-fluid-2xl: clamp(1.5rem, 1.1rem + 2vw, 2rem);
  --text-fluid-3xl: clamp(1.875rem, 1.2rem + 3.375vw, 2.5rem);
  --text-fluid-4xl: clamp(2.25rem, 1rem + 6.25vw, 3.5rem);
  --text-fluid-5xl: clamp(3rem, 1rem + 10vw, 5rem);
}
```

**Important for Accessibility**: Always combine `vw` with `rem` to respect user zoom preferences (WCAG compliance).

### Using Fluid Typography

```html
<!-- Fluid heading that scales smoothly -->
<h1 class="text-fluid-4xl leading-tight font-bold">Responsive Heading</h1>

<!-- Fluid body text -->
<p class="text-fluid-base max-w-prose leading-relaxed">
  Body text that scales proportionally with the viewport while respecting user's
  font size preferences.
</p>

<!-- Fluid with breakpoint overrides for fine control -->
<h2 class="text-fluid-2xl lg:text-fluid-3xl font-semibold">Section Title</h2>
```

## Fluid Spacing System

### Clamp-Based Spacing

```css
@theme {
  /* Fluid spacing scale */
  --spacing-fluid-xs: clamp(0.25rem, 0.2rem + 0.25vw, 0.5rem);
  --spacing-fluid-sm: clamp(0.5rem, 0.4rem + 0.5vw, 1rem);
  --spacing-fluid-md: clamp(1rem, 0.75rem + 1.25vw, 2rem);
  --spacing-fluid-lg: clamp(1.5rem, 1rem + 2.5vw, 3rem);
  --spacing-fluid-xl: clamp(2rem, 1.25rem + 3.75vw, 4rem);
  --spacing-fluid-2xl: clamp(3rem, 1.5rem + 7.5vw, 6rem);
  --spacing-fluid-section: clamp(4rem, 2rem + 10vw, 8rem);
}
```

### Using Fluid Spacing

```html
<!-- Fluid section padding -->
<section class="py-fluid-section px-fluid-md">
  <div class="mx-auto max-w-7xl">
    <h2 class="mb-fluid-lg">Section Title</h2>
    <div class="gap-fluid-md grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
      <!-- Cards -->
    </div>
  </div>
</section>

<!-- Hero section with fluid spacing -->
<header class="py-fluid-2xl px-fluid-md flex min-h-screen items-center">
  <div class="max-w-4xl">
    <h1 class="text-fluid-5xl mb-fluid-md">Hero Title</h1>
    <p class="text-fluid-lg mb-fluid-lg">Hero description</p>
    <button class="px-fluid-md py-fluid-sm">Get Started</button>
  </div>
</header>
```

## Touch-Friendly Interactive Elements

### WCAG 2.2 Touch Target Requirements

**Minimum sizes (2025 standards)**:

- **WCAG 2.2 Level AA**: 24x24 CSS pixels minimum
- **Recommended**: 44x44 CSS pixels (Apple, Google, Microsoft guidelines)
- **Optimal**: 48x48 CSS pixels for critical actions

```html
<!-- WCAG 2.2 compliant touch targets -->

<!-- Minimum AA compliant (24px) -->
<button class="min-h-6 min-w-6 p-1">
  <svg class="h-4 w-4">...</svg>
</button>

<!-- Recommended size (44px) -->
<button class="min-h-11 min-w-11 p-2.5">
  <svg class="h-6 w-6">...</svg>
  <span class="sr-only">Action</span>
</button>

<!-- Optimal for primary actions (48px) -->
<button class="min-h-12 min-w-12 px-6 py-3 text-base">Primary Action</button>
```

### Extended Touch Targets

```html
<!-- Extend touch target beyond visible element -->
<a href="/link" class="relative inline-block text-sm">
  Small visible link
  <!-- Invisible extended touch area -->
  <span class="absolute -inset-3" aria-hidden="true"></span>
</a>

<!-- Icon button with extended target -->
<button class="relative -m-2 rounded-lg p-2 hover:bg-gray-100">
  <svg class="h-5 w-5" aria-hidden="true">...</svg>
  <span class="sr-only">Close</span>
</button>
```

### Touch Target Spacing

```html
<!-- Adequate spacing between touch targets (minimum 8px gap) -->
<nav class="flex gap-3">
  <a href="#" class="min-h-11 px-4 py-2.5">Home</a>
  <a href="#" class="min-h-11 px-4 py-2.5">About</a>
  <a href="#" class="min-h-11 px-4 py-2.5">Contact</a>
</nav>

<!-- Stacked navigation with adequate spacing -->
<nav class="flex flex-col">
  <a href="#" class="min-h-11 border-b border-gray-100 px-4 py-3">Link 1</a>
  <a href="#" class="min-h-11 border-b border-gray-100 px-4 py-3">Link 2</a>
  <a href="#" class="min-h-11 px-4 py-3">Link 3</a>
</nav>

<!-- Button group with safe spacing -->
<div class="flex flex-wrap gap-3">
  <button class="min-h-11 px-4 py-2">Cancel</button>
  <button class="min-h-11 bg-blue-600 px-4 py-2 text-white">Confirm</button>
</div>
```

## Container Queries (2025 Game-Changer)

Container queries enable **component-level responsiveness**, independent of viewport size.

### Setup

```css
@import 'tailwindcss';
@plugin "@tailwindcss/container-queries";
```

### Container Query Breakpoints

| Class  | Min-width      |
| ------ | -------------- |
| `@xs`  | 20rem (320px)  |
| `@sm`  | 24rem (384px)  |
| `@md`  | 28rem (448px)  |
| `@lg`  | 32rem (512px)  |
| `@xl`  | 36rem (576px)  |
| `@2xl` | 42rem (672px)  |
| `@3xl` | 48rem (768px)  |
| `@4xl` | 56rem (896px)  |
| `@5xl` | 64rem (1024px) |

### Practical Container Query Patterns

```html
<!-- Card that responds to its container, not viewport -->
<article class="@container">
  <div
    class="flex flex-col gap-4 rounded-xl bg-white p-4 shadow-sm @sm:flex-row"
  >
    <img
      src="..."
      class="aspect-video w-full rounded-lg object-cover @sm:aspect-square @sm:w-32 @lg:w-48"
    />
    <div class="min-w-0 flex-1">
      <h3 class="truncate text-base font-semibold @md:text-lg @lg:text-xl">
        Card Title
      </h3>
      <p
        class="mt-2 line-clamp-2 text-sm text-gray-600 @md:text-base @lg:line-clamp-3"
      >
        Description that adapts to available space...
      </p>
      <div class="mt-4 flex flex-wrap gap-2 @md:gap-3">
        <span class="rounded bg-gray-100 px-2 py-1 text-xs @md:text-sm"
          >Tag</span
        >
      </div>
    </div>
  </div>
</article>
```

### Named Containers

```html
<div class="@container/sidebar w-64">
  <nav
    class="flex flex-col gap-2 @lg/sidebar:flex-row @lg/sidebar:items-center @lg/sidebar:gap-4"
  >
    <a href="#">Link 1</a>
    <a href="#">Link 2</a>
  </nav>
</div>

<main class="@container/main flex-1">
  <div class="grid grid-cols-1 gap-6 @md/main:grid-cols-2 @xl/main:grid-cols-3">
    <!-- Grid items respond to main container -->
  </div>
</main>
```

### When to Use Container vs Viewport Queries

| Use Container Queries | Use Viewport Queries |
| --------------------- | -------------------- |
| Reusable components   | Page-level layouts   |
| Sidebar widgets       | Navigation bars      |
| Card grids            | Hero sections        |
| Embedded content      | Full-width sections  |
| CMS/dynamic content   | Fixed app shells     |

## Responsive Layout Patterns

### Mobile-First Grid System

```html
<!-- Auto-responsive grid with minimum card width -->
<div
  class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4"
>
  <!-- Cards automatically flow -->
</div>

<!-- CSS Grid auto-fit (no breakpoints needed) -->
<div class="grid grid-cols-[repeat(auto-fit,minmax(280px,1fr))] gap-6">
  <!-- Cards auto-fit with 280px minimum -->
</div>

<!-- CSS Grid auto-fill for fixed-size items -->
<div class="grid grid-cols-[repeat(auto-fill,minmax(200px,1fr))] gap-4">
  <!-- Fixed minimum size, grows to fill -->
</div>
```

### Responsive Flexbox Patterns

```html
<!-- Stack to row -->
<div class="flex flex-col gap-4 md:flex-row">
  <div class="flex-1">Content 1</div>
  <div class="flex-1">Content 2</div>
</div>

<!-- Wrap with centered items -->
<div class="flex flex-wrap justify-center gap-4">
  <div class="w-full sm:w-auto">Item 1</div>
  <div class="w-full sm:w-auto">Item 2</div>
  <div class="w-full sm:w-auto">Item 3</div>
</div>

<!-- Mobile stack, desktop inline with push -->
<div class="flex flex-col gap-4 sm:flex-row sm:items-center">
  <div class="flex-1">
    <h3>Title</h3>
    <p class="text-sm text-gray-600">Description</p>
  </div>
  <button class="min-h-11 px-4 py-2 sm:ml-auto">Action</button>
</div>
```

### Responsive Sidebar Layouts

```html
<!-- Collapsible sidebar -->
<div class="flex min-h-screen">
  <!-- Sidebar: hidden on mobile, visible on desktop -->
  <aside class="hidden w-64 border-r bg-gray-50 lg:flex lg:flex-col">
    <nav class="flex-1 p-4">...</nav>
  </aside>

  <!-- Main content -->
  <main class="flex-1 p-4 lg:p-8">Content</main>
</div>

<!-- Mobile drawer + desktop sidebar -->
<div class="relative flex min-h-screen">
  <!-- Mobile drawer overlay -->
  <div
    class="fixed inset-0 z-40 bg-black/50 data-[open=false]:hidden lg:hidden"
    data-open="false"
  >
    <aside class="h-full w-64 bg-white">Mobile navigation</aside>
  </div>

  <!-- Desktop sidebar -->
  <aside class="hidden w-64 border-r lg:block">Desktop navigation</aside>

  <main class="flex-1">Content</main>
</div>
```

### Holy Grail Layout (2025)

```html
<div class="grid min-h-screen grid-rows-[auto_1fr_auto]">
  <!-- Header -->
  <header class="sticky top-0 z-50 h-16 border-b bg-white shadow-sm">
    <nav
      class="mx-auto flex h-full max-w-7xl items-center justify-between px-4"
    >
      <Logo />
      <ul class="hidden gap-6 md:flex">
        ...
      </ul>
      <button class="min-h-11 min-w-11 md:hidden">Menu</button>
    </nav>
  </header>

  <!-- Main content area with optional sidebars -->
  <div
    class="grid grid-cols-1 gap-0 md:grid-cols-[240px_1fr] lg:grid-cols-[240px_1fr_280px]"
  >
    <nav class="hidden border-r p-4 md:block">Left Nav</nav>
    <main class="p-4 md:p-6 lg:p-8">Main Content</main>
    <aside class="hidden border-l p-4 lg:block">Right Sidebar</aside>
  </div>

  <!-- Footer -->
  <footer class="bg-gray-900 py-8 text-white md:py-12">Footer content</footer>
</div>
```

## Responsive Images

### Aspect Ratio Containers

```html
<!-- Maintain aspect ratio across all sizes -->
<div class="aspect-video overflow-hidden rounded-lg">
  <img src="..." class="h-full w-full object-cover" loading="lazy" />
</div>

<!-- Responsive aspect ratio -->
<div class="aspect-square overflow-hidden sm:aspect-video lg:aspect-[4/3]">
  <img src="..." class="h-full w-full object-cover" />
</div>
```

### Responsive Image Sizes

```html
<!-- Art direction with picture element -->
<picture>
  <source media="(min-width: 1024px)" srcset="large.jpg" />
  <source media="(min-width: 640px)" srcset="medium.jpg" />
  <img
    src="small.jpg"
    alt="Description"
    class="h-auto w-full rounded-lg"
    loading="lazy"
  />
</picture>

<!-- Responsive srcset -->
<img
  src="image-800.jpg"
  srcset="
    image-400.jpg   400w,
    image-800.jpg   800w,
    image-1200.jpg 1200w,
    image-1600.jpg 1600w
  "
  sizes="
    (min-width: 1280px) 1200px,
    (min-width: 768px) 80vw,
    100vw
  "
  alt="Responsive image"
  class="h-auto w-full"
  loading="lazy"
/>
```

## Responsive Typography Patterns

### Heading Hierarchy

```html
<!-- Mobile-first heading scale -->
<h1
  class="text-2xl leading-tight font-bold tracking-tight sm:text-3xl md:text-4xl lg:text-5xl xl:text-6xl"
>
  Main Heading
</h1>

<h2
  class="text-xl leading-snug font-semibold sm:text-2xl md:text-3xl lg:text-4xl"
>
  Section Heading
</h2>

<h3 class="text-lg font-medium sm:text-xl md:text-2xl">Subsection Heading</h3>
```

### Readable Body Text

```html
<!-- Optimal line length and spacing -->
<article class="mx-auto max-w-prose">
  <p
    class="text-base leading-relaxed text-gray-700 md:text-lg md:leading-loose dark:text-gray-300"
  >
    Body text optimized for readability with 45-75 characters per line.
  </p>
</article>

<!-- Text that balances across lines -->
<h2 class="max-w-2xl text-2xl font-bold text-balance md:text-3xl">
  This heading will balance text across lines to avoid orphans
</h2>
```

## Mobile Navigation Patterns

### Hamburger to Full Nav

```html
<nav class="relative">
  <!-- Desktop navigation -->
  <ul class="hidden items-center gap-6 md:flex">
    <li><a href="#" class="py-2 hover:text-blue-600">Home</a></li>
    <li><a href="#" class="py-2 hover:text-blue-600">Products</a></li>
    <li><a href="#" class="py-2 hover:text-blue-600">About</a></li>
    <li><a href="#" class="py-2 hover:text-blue-600">Contact</a></li>
  </ul>

  <!-- Mobile menu button -->
  <button
    class="min-h-11 min-w-11 p-2 md:hidden"
    aria-expanded="false"
    aria-controls="mobile-menu"
    aria-label="Toggle navigation menu"
  >
    <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M4 6h16M4 12h16M4 18h16"
      />
    </svg>
  </button>

  <!-- Mobile menu (controlled via JS) -->
  <div
    id="mobile-menu"
    class="absolute top-full right-0 left-0 hidden border-t bg-white shadow-lg md:hidden"
  >
    <ul class="py-2">
      <li>
        <a href="#" class="block min-h-11 px-4 py-3 hover:bg-gray-50">Home</a>
      </li>
      <li>
        <a href="#" class="block min-h-11 px-4 py-3 hover:bg-gray-50"
          >Products</a
        >
      </li>
      <li>
        <a href="#" class="block min-h-11 px-4 py-3 hover:bg-gray-50">About</a>
      </li>
      <li>
        <a href="#" class="block min-h-11 px-4 py-3 hover:bg-gray-50"
          >Contact</a
        >
      </li>
    </ul>
  </div>
</nav>
```

### Bottom Navigation (Mobile App Style)

```html
<!-- Fixed bottom navigation for mobile -->
<nav
  class="safe-area-pb fixed inset-x-0 bottom-0 z-50 border-t bg-white shadow-lg md:hidden"
>
  <ul class="flex justify-around">
    <li>
      <a
        href="#"
        class="flex min-h-14 min-w-14 flex-col items-center px-3 py-2 text-xs text-gray-600 hover:text-blue-600 aria-current:text-blue-600"
      >
        <svg class="mb-1 h-6 w-6">...</svg>
        Home
      </a>
    </li>
    <li>
      <a
        href="#"
        class="flex min-h-14 min-w-14 flex-col items-center px-3 py-2 text-xs"
      >
        <svg class="mb-1 h-6 w-6">...</svg>
        Search
      </a>
    </li>
    <li>
      <a
        href="#"
        class="flex min-h-14 min-w-14 flex-col items-center px-3 py-2 text-xs"
      >
        <svg class="mb-1 h-6 w-6">...</svg>
        Profile
      </a>
    </li>
  </ul>
</nav>

<!-- Add padding to main content to prevent overlap -->
<main class="pb-20 md:pb-0">Content</main>
```

## Safe Area Handling (Notched Devices)

```css
@utility safe-area-pt {
  padding-top: env(safe-area-inset-top);
}

@utility safe-area-pb {
  padding-bottom: env(safe-area-inset-bottom);
}

@utility safe-area-pl {
  padding-left: env(safe-area-inset-left);
}

@utility safe-area-pr {
  padding-right: env(safe-area-inset-right);
}

@utility safe-area-p {
  padding-top: env(safe-area-inset-top);
  padding-right: env(safe-area-inset-right);
  padding-bottom: env(safe-area-inset-bottom);
  padding-left: env(safe-area-inset-left);
}
```

```html
<!-- Header that respects notch -->
<header class="safe-area-pt sticky top-0 bg-white">
  <div class="flex h-16 items-center px-4">Navigation</div>
</header>

<!-- Bottom navigation with safe area -->
<nav class="safe-area-pb fixed inset-x-0 bottom-0 border-t bg-white">
  Bottom nav
</nav>
```

## Performance Optimization for Mobile

### Lazy Loading

```html
<!-- Native lazy loading for images -->
<img src="image.jpg" alt="..." loading="lazy" class="h-auto w-full" />

<!-- Lazy load below-fold content -->
<div class="contents" data-lazy-load>Heavy component loaded on demand</div>
```

### Content Visibility

```css
@utility content-auto {
  content-visibility: auto;
  contain-intrinsic-size: auto 500px;
}
```

```html
<!-- Skip rendering off-screen content -->
<section class="content-auto">Large section that may be off-screen</section>
```

### Reduced Data Usage

```html
<!-- Show simpler version on slow connections -->
<picture>
  <source srcset="video-poster.jpg" media="(prefers-reduced-data: reduce)" />
  <img src="animated.gif" alt="..." />
</picture>
```

## Responsive Testing Checklist

### Essential Tests

1. **320px** - Smallest supported width (older iPhones)
2. **375px** - Modern iPhone base
3. **414px** - Large phones (iPhone Plus/Max)
4. **768px** - iPad portrait
5. **1024px** - iPad landscape / small laptop
6. **1280px** - Standard laptop
7. **1440px** - Large desktop
8. **1920px** - Full HD desktop

### Quality Checks

- [ ] Text remains readable at all sizes
- [ ] Touch targets are minimum 44px on mobile
- [ ] No horizontal scroll on any viewport
- [ ] Images don't overflow containers
- [ ] Navigation is accessible on all sizes
- [ ] Forms are usable on mobile
- [ ] Modals fit mobile screens
- [ ] Tables have mobile alternatives
- [ ] Performance under 3s LCP on 3G

## Responsive Video Containers

### Aspect Ratio Utilities for Video

Use Tailwind's `aspect-*` utilities to maintain correct video proportions across all screen sizes, preventing Cumulative Layout Shift (CLS):

```html
<!-- Standard 16:9 video container -->
<div class="aspect-video overflow-hidden rounded-lg bg-black">
  <video class="h-full w-full object-cover" playsinline preload="metadata">
    <source src="video.mp4" type="video/mp4" />
  </video>
</div>

<!-- Vertical video (9:16) for mobile-first social content -->
<div class="mx-auto aspect-[9/16] max-w-sm overflow-hidden rounded-lg bg-black">
  <video class="h-full w-full object-cover" playsinline muted loop>
    <source src="reel.mp4" type="video/mp4" />
  </video>
</div>

<!-- Square video (1:1) common for social feeds -->
<div class="aspect-square overflow-hidden rounded-lg bg-black">
  <video class="h-full w-full object-cover" playsinline preload="metadata">
    <source src="square.mp4" type="video/mp4" />
  </video>
</div>

<!-- Responsive aspect ratio - vertical on mobile, widescreen on desktop -->
<div class="aspect-[9/16] overflow-hidden rounded-lg bg-black sm:aspect-video">
  <video class="h-full w-full object-contain" playsinline preload="metadata">
    <source src="video.mp4" type="video/mp4" />
  </video>
</div>
```

### Preventing CLS with Video Placeholders

Videos without defined dimensions cause layout shift when they load. Use aspect ratio containers to reserve space:

```html
<!-- CLS-safe video with poster and skeleton loader -->
<div class="relative aspect-video overflow-hidden rounded-lg bg-gray-900">
  <!-- Skeleton placeholder while video loads -->
  <div
    class="absolute inset-0 animate-pulse bg-gray-800"
    aria-hidden="true"
  ></div>

  <video
    class="absolute inset-0 h-full w-full object-cover"
    poster="/thumbnails/video-poster.jpg"
    playsinline
    preload="metadata"
  >
    <source src="video.mp4" type="video/mp4" />
  </video>
</div>

<!-- Responsive grid of video thumbnails with zero CLS -->
<div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
  <div class="aspect-video overflow-hidden rounded-lg bg-gray-900">
    <video
      class="h-full w-full object-cover"
      poster="/thumb1.jpg"
      preload="none"
      playsinline
    ></video>
  </div>
  <div class="aspect-video overflow-hidden rounded-lg bg-gray-900">
    <video
      class="h-full w-full object-cover"
      poster="/thumb2.jpg"
      preload="none"
      playsinline
    ></video>
  </div>
  <div class="aspect-video overflow-hidden rounded-lg bg-gray-900">
    <video
      class="h-full w-full object-cover"
      poster="/thumb3.jpg"
      preload="none"
      playsinline
    ></video>
  </div>
</div>
```

### Full-Bleed Video on Mobile, Constrained on Desktop

```html
<!-- Full-width on mobile, centered with max-width on desktop -->
<div class="w-full lg:mx-auto lg:max-w-4xl">
  <div class="aspect-video overflow-hidden bg-black lg:rounded-xl">
    <video class="h-full w-full object-cover" playsinline preload="metadata">
      <source src="hero.mp4" type="video/mp4" />
    </video>
  </div>
</div>

<!-- Full-bleed hero video background -->
<section class="relative h-screen w-full overflow-hidden">
  <video
    class="absolute inset-0 h-full w-full object-cover"
    autoplay
    muted
    loop
    playsinline
    preload="auto"
  >
    <source src="hero-bg.mp4" type="video/mp4" />
  </video>

  <!-- Content overlay with safe padding -->
  <div
    class="relative z-10 flex h-full items-center justify-center px-4 sm:px-8"
  >
    <div class="max-w-2xl text-center text-white">
      <h1 class="text-3xl font-bold sm:text-4xl lg:text-6xl">Hero Title</h1>
      <p class="mt-4 text-lg sm:text-xl">Subtitle text</p>
    </div>
  </div>

  <!-- Dark overlay for text readability -->
  <div class="absolute inset-0 bg-black/40" aria-hidden="true"></div>
</section>
```

### Safe Zone Overlays for Video UI

Video player controls and UI elements need touch-friendly sizing and proper placement:

```html
<!-- Custom video player with touch-safe controls -->
<div
  class="group @container relative aspect-video overflow-hidden rounded-lg bg-black"
>
  <video class="h-full w-full object-cover" playsinline preload="metadata">
    <source src="video.mp4" type="video/mp4" />
  </video>

  <!-- Play/Pause overlay - centered, touch-friendly -->
  <button
    class="absolute inset-0 flex items-center justify-center bg-black/0 transition-colors group-hover:bg-black/20"
  >
    <span
      class="flex h-16 w-16 items-center justify-center rounded-full bg-white/90 shadow-lg sm:h-20 sm:w-20"
    >
      <svg
        class="ml-1 h-8 w-8 text-gray-900 sm:h-10 sm:w-10"
        viewBox="0 0 24 24"
        fill="currentColor"
      >
        <path d="M8 5v14l11-7z" />
      </svg>
    </span>
  </button>

  <!-- Bottom controls bar - respects touch targets -->
  <div
    class="absolute inset-x-0 bottom-0 flex items-center gap-3 bg-gradient-to-t from-black/80 to-transparent p-3 opacity-0 transition-opacity group-hover:opacity-100 sm:p-4"
  >
    <!-- Progress bar - tall enough for touch -->
    <div class="h-1 flex-1 cursor-pointer rounded-full bg-white/30">
      <div class="relative h-full w-1/3 rounded-full bg-white">
        <span
          class="absolute top-1/2 right-0 -mr-2 h-4 w-4 -translate-y-1/2 rounded-full bg-white"
        ></span>
      </div>
    </div>

    <!-- Time display -->
    <span class="shrink-0 text-xs text-white tabular-nums sm:text-sm"
      >1:23 / 4:56</span
    >

    <!-- Fullscreen button - touch-friendly minimum size -->
    <button
      class="flex min-h-11 min-w-11 items-center justify-center text-white"
    >
      <svg
        class="h-5 w-5"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
      >
        <path
          d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"
        />
      </svg>
    </button>
  </div>
</div>
```

### Container Queries for Adaptive Video Players

Video player components that adapt their layout based on container size --- useful when the same player appears in a sidebar, main content area, or modal:

```html
<!-- Video player that adapts to its container -->
<div class="@container">
  <div
    class="flex flex-col gap-4 overflow-hidden rounded-xl bg-gray-950 @lg:flex-row @lg:gap-6"
  >
    <!-- Video area -->
    <div class="aspect-video w-full overflow-hidden @lg:flex-1">
      <video class="h-full w-full object-cover" playsinline preload="metadata">
        <source src="video.mp4" type="video/mp4" />
      </video>
    </div>

    <!-- Info panel - below video on narrow, beside on wide -->
    <div class="p-4 text-white @lg:w-80 @lg:overflow-y-auto @lg:p-6">
      <h3 class="text-base font-semibold @lg:text-lg">Video Title</h3>
      <p class="mt-2 line-clamp-2 text-sm text-gray-400 @lg:line-clamp-none">
        Video description that shows more text when the container is wider...
      </p>

      <!-- Related videos - hidden in narrow containers -->
      <div class="mt-6 hidden space-y-3 @xl:block">
        <h4 class="text-sm font-medium text-gray-300">Related</h4>
        <div class="space-y-2">
          <div class="flex gap-3">
            <div class="aspect-video w-28 shrink-0 rounded bg-gray-800"></div>
            <div class="text-xs text-gray-400">Related Video 1</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
```

## Best Practices Summary

| Practice               | Implementation                               |
| ---------------------- | -------------------------------------------- |
| Mobile-first utilities | Unprefixed first, then `sm:`, `md:`, `lg:`   |
| Touch targets          | `min-h-11 min-w-11` (44px minimum)           |
| Fluid typography       | `clamp(min, preferred, max)` with `rem + vw` |
| Fluid spacing          | `clamp()` for padding and margins            |
| Container queries      | `@container` for component responsiveness    |
| Safe areas             | `env(safe-area-inset-*)` for notched devices |
| Readable text          | `max-w-prose` (65ch) and `leading-relaxed`   |
| Lazy loading           | `loading="lazy"` on below-fold images        |
| Touch spacing          | `gap-3` (12px) minimum between targets       |
| Viewport meta          | `width=device-width, initial-scale=1`        |
