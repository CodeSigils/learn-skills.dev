---
name: ui-ux-pro
description: 'Design and build modern, clean UI/UX with elegant animations and transitions using shadcn/ui, Tailwind, GSAP, and accessibility best practices. Use for component creation, page design, design system implementation, and interactive experiences. Covers responsive layouts, micro-animations, dynamic effects, and performance optimization.'
argument-hint: 'Describe the UI component or page layout you want to build (e.g., "Product card with hover animation", "Dashboard layout for rural users")'
---

# UI/UX Professional Design Skill

Build beautiful, modern interfaces with clean design, smooth animations, and excellent user experience using industry-standard frameworks and creative techniques.

## When to Use

- Creating elegant UI components with smooth transitions
- Designing full-page layouts with responsive behavior
- Enhancing user experience with micro-animations and GSAP effects
- Building design systems and component libraries
- Optimizing visual hierarchy and accessibility
- Creating interactive, dynamic interfaces without visual overload
- Designing for specific user contexts (rural users, accessibility needs)

## Design Principles

Review [Design & Accessibility Principles](./references/design-principles.md) for foundational approach.

## Step-by-Step Procedure

### 1. **Define Requirements & User Context**

Before designing, clarify:
- Target audience (e.g., rural users, accessibility needs)
- Purpose of the component/page (action, information, engagement)
- Device context (mobile-first vs. desktop-first)
- Performance constraints (animation complexity, bundle size)
- Emotional tone (professional, playful, minimal, energetic)

### 2. **Choose the Right Framework Stack**

**Primary Stack (Recommended for TrustServe):**
- **UI Framework**: shadcn/ui + Tailwind CSS
- **Animation**: GSAP (complex), Framer Motion (React-native), CSS transitions (simple)
- **Accessibility**: Radix UI primitives (built into shadcn)
- **Icons**: Lucide React, Heroicons
- **State Management**: React Context (existing) or Zustand

**Alternative Stacks:**
- Headless UI + Tailwind (more minimalist)
- Chakra UI (more opinionated, accessibility-first)
- Bootstrap-based (if not using Tailwind)

### 3. **Create Component Structure**

Start with [Component Template](./assets/component-template.jsx):
- Semantic HTML structure
- Tailwind utility classes
- Responsive breakpoints (mobile, tablet, desktop)
- Built-in accessibility attributes (ARIA labels, roles)
- CSS variables for theming

```jsx
// Key structure:
// 1. Component props interface
// 2. Responsive layout logic
// 3. Accessibility attributes
// 4. Export for tree-shaking
```

### 4. **Design the Visual Hierarchy**

Apply these principles in order:
- **Scale & Size**: Primary elements larger, supporting elements smaller
- **Color & Contrast**: WCAG AA or AAA compliance (min 4.5:1 for text)
- **Spacing**: Consistent use of space (8px grid, Tailwind scale)
- **Typography**: Font hierarchy (h1, h2, p, small; max 2-3 fonts)
- **Whitespace**: Breathing room between sections (rural users appreciate clarity)

### 5. **Layer in Animations & Transitions**

Reference [Animation & Motion Guide](./references/animation-guide.md) for detailed approach.

**Animation Hierarchy (from subtle to complex):**

| Level | Tools | Use Cases | Performance |
|-------|-------|-----------|-------------|
| **Light** | CSS `transition` | Hover states, color changes, opacity | Excellent |
| **Medium** | CSS `@keyframes`, Framer Motion | Button effects, page transitions, entrance animations | Very Good |
| **Heavy** | GSAP, Lottie | Complex parallax, scroll effects, interactive sequences | Good (optimize) |

**Golden Rules:**
- Keep animations **< 300ms** for UI feedback
- Use **easing functions** (ease-out for entrances, ease-in for exits)
- Disable animations on `prefers-reduced-motion` for accessibility
- Test animation performance on low-end devices

### 6. **Implement Responsive Design**

Use Tailwind breakpoints:
```jsx
// Mobile-first
<div className="w-full md:w-1/2 lg:w-1/3 xl:w-1/4">
  {/* Responsive content */}
</div>
```

**Breakpoints:**
- `sm`: 640px (tablet portrait)
- `md`: 768px (tablet landscape)
- `lg`: 1024px (desktop)
- `xl`: 1280px (wide desktop)
- `2xl`: 1536px (ultra-wide)

### 7. **Ensure Accessibility**

Non-negotiable checklist:
- [ ] Semantic HTML (`<button>`, `<nav>`, `<main>`, not `<div>` everywhere)
- [ ] ARIA labels for icons/hidden content
- [ ] Keyboard navigation (Tab, Enter, Escape, arrows)
- [ ] Focus indicators visible
- [ ] Color not the only indicator
- [ ] Text alternatives for images
- [ ] Sufficient contrast (WCAG standards)
- [ ] Form labels properly associated
- [ ] `alt` text for decorative vs. informational images

### 8. **Test & Optimize**

**Visual Testing:**
- Responsive preview (Chrome DevTools)
- Different browsers (Chrome, Firefox, Safari, Edge)
- Light/dark modes (if applicable)
- High contrast mode

**Performance Testing:**
- Lighthouse audit (target: 90+ performance)
- Animation FPS (target: 60fps)
- Bundle size impact of new components

**Accessibility Testing:**
- Keyboard-only navigation
- Screen reader (NVDA, JAWS)
- Axe DevTools, Lighthouse
- Manual accessibility review

### 9. **Document & Version**

Create inline documentation:
```jsx
/**
 * @component ProductCard
 * Beautiful product card with hover animation and action buttons.
 * 
 * @param {string} title - Product title
 * @param {string} image - Image URL
 * @param {function} onAction - Callback when action button clicked
 * @returns {JSX.Element}
 * 
 * @example
 * <ProductCard title="Service" image="/img.jpg" onAction={() => {}} />
 */
```

## Quick Start Checklist

- [ ] Framework chosen (shadcn recommended)
- [ ] Component structure defined
- [ ] Visual hierarchy applied (scale, color, spacing)
- [ ] Base styles added (Tailwind utilities)
- [ ] Animations specified (level: light/medium/heavy)
- [ ] Responsive breakpoints tested
- [ ] Accessibility checklist passed
- [ ] Performance benchmarked
- [ ] Component documented

## Common Patterns

### Button with Loading State
- Use spinner icon from Lucide
- Disabled state during loading
- Smooth 200ms transition

### Card Component
- Subtle shadow on hover
- Border on light theme, shadow on dark
- Consistent padding (Tailwind scale)

### Modal/Dialog
- Backdrop blur effect (Tailwind `backdrop-blur`)
- Smooth scale + fade animation (200ms)
- Focus trap + escape key support (Radix UI handles this)

### Dropdown Menu
- Slide + fade entrance (150ms)
- Position relative to trigger
- Keyboard navigation support

### Loading States
- Skeleton components for predictable layouts
- Animated spinners (subtle rotation)
- Progress indicators for long operations

## Tools & Resources

### Frameworks & Libraries
- **shadcn/ui**: Pre-built accessible components
- **Tailwind CSS**: Utility-first styling
- **Framer Motion**: React animations (easier learning curve)
- **GSAP**: Professional animations (steeper curve, powerful)
- **Radix UI**: Headless components, accessibility primitives

### Design Tools  
- Figma (design → code workflow)
- Adobe XD, Sketch (design references)
- Storybook (component documentation)

### Testing & QA
- Lighthouse (performance)
- Axe DevTools (accessibility)
- Responsively App (device preview)
- BrowserStack (real device testing)

## References

- [Design & Accessibility Principles](./references/design-principles.md) — Color theory, spacing, typography, WCAG standards
- [Animation & Motion Guide](./references/animation-guide.md) — GSAP, Framer Motion, CSS animations, performance optimization
- [Component Template](./assets/component-template.jsx) — Boilerplate for new components
- [Layout Template](./assets/layout-template.jsx) — Responsive page layout starter

## TrustServe Specific Guidelines

For the TrustServe marketplace platform:
- **Urban Company aesthetic**: Clean, organized, professional
- **Rural accessibility**: Clear typography, sufficient color contrast, less animation distraction
- **Trust first**: Steady, confident design without excessive visual effects
- **Mobile-first**: Majority of rural users on mobile devices
- **Performance**: Keep animations light (< 200ms), images optimized, bundle lean

---

**Need help?** Describe the component or page you want to build, and the agent will walk through each step with code examples and accessibility checks.
