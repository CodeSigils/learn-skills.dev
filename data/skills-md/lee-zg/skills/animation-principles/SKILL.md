---
name: animation-principles
description: Apply Disney's 12 Principles of Animation to any UI, web, game, or motion design context. Provides comprehensive guidance on squash & stretch, anticipation, staging, timing, easing, arcs, and all 12 principles with code examples for CSS, GSAP, Framer Motion, React Spring, Lottie, and more. Use when building animations, micro-interactions, transitions, loading states, or any motion design work.
---

# Disney's 12 Animation Principles

Give your AI agent the superpower of a Disney animator. A comprehensive collection of 144 animation skills covering every context, tool, and scenario.

## The 12 Principles at a Glance

| # | Principle | Core Concept | Web Application |
|---|-----------|--------------|-----------------|
| 1 | **Squash & Stretch** | Volume deformation shows weight | `transform: scale()` on interaction states |
| 2 | **Anticipation** | Preparation signals action | Slight reverse movement before action |
| 3 | **Staging** | Direct attention to what matters | Motion hierarchy and focus dimming |
| 4 | **Straight Ahead / Pose to Pose** | Sequential vs keyframe approach | JS frame-by-frame vs CSS `@keyframes` |
| 5 | **Follow Through / Overlapping** | Parts move at different rates | Staggered child animations, elastic easing |
| 6 | **Slow In / Slow Out** | Natural acceleration/deceleration | `ease-in-out`, cubic-bezier curves |
| 7 | **Arc** | Organic curved motion paths | `offset-path` or bezier transforms |
| 8 | **Secondary Action** | Supporting movements reinforce | Shadows, glows responding to primary |
| 9 | **Timing** | Speed conveys weight and emotion | Micro 100-200ms, standard 200-400ms |
| 10 | **Exaggeration** | Push beyond reality for clarity | Scale beyond 1.0, overshoot animations |
| 11 | **Solid Drawing** | Maintain volume and consistency | Consistent `transform-origin`, perspective |
| 12 | **Appeal** | Charisma and watchability | Smooth 60fps, purposeful motion |

## Quick Start

When applying animation principles:

1. **Identify the context** — What are you building? Check [skills/](skills/) by category
2. **Choose the right skill** — Find guidance specific to your domain, tool, or goal
3. **Apply the principles** — Use the principle-specific guidance for your scenario
4. **Validate timing** — Check the timing reference below
5. **Test performance** — Ensure 60fps with `transform` and `opacity` only

## Essential CSS Easing

```css
:root {
  /* Standard material easing */
  --ease-standard: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-decelerate: cubic-bezier(0, 0, 0.2, 1);
  --ease-accelerate: cubic-bezier(0.4, 0, 1, 1);

  /* Playful / bouncy */
  --ease-overshoot: cubic-bezier(0.34, 1.56, 0.64, 1);
  --ease-elastic: cubic-bezier(0.68, -0.55, 0.265, 1.55);
  --ease-pop: cubic-bezier(0.175, 0.885, 0.32, 1.275);

  /* Timing durations */
  --duration-instant: 50ms;
  --duration-micro: 100ms;
  --duration-small: 200ms;
  --duration-medium: 300ms;
  --duration-large: 500ms;
  --duration-slow: 800ms;
  --duration-dramatic: 1200ms;
}
```

## Timing Reference

| Element | Duration | Easing | Principle |
|---------|----------|--------|-----------|
| Button press | 100-150ms | `ease-out` | Squash & Stretch |
| Hover state | 150-200ms | `ease-in-out` | Secondary Action |
| Dropdown expand | 200-300ms | `ease-overshoot` | Anticipation |
| Modal enter | 250-350ms | `ease-decelerate` | Staging |
| Modal exit | 150-250ms | `ease-accelerate` | Exit |
| Page transition | 300-500ms | `ease-standard` | Follow Through |
| Toast notification | 200-400ms | `ease-overshoot` | Appeal |
| Loading spinner | Infinite | `linear` | Continuous |
| Success celebration | 400-600ms | `ease-elastic` | Exaggeration |

## Core CSS Patterns

```css
/* Squash & Stretch - elastic button */
.button:active {
  transform: scale(0.95, 1.05);
  transition: transform 100ms var(--ease-standard);
}

/* Anticipation - pre-expand shrink */
@keyframes dropdown-enter {
  0% { transform: scaleY(0.97); opacity: 0; }
  100% { transform: scaleY(1); opacity: 1; }
}

/* Slow In / Slow Out - never use linear for UI */
.element {
  transition: all 300ms cubic-bezier(0.4, 0, 0.2, 1);
}

/* Arc - curved motion path */
@keyframes arc-motion {
  0% { transform: translate(0, 0); }
  50% { transform: translate(50px, -40px); }
  100% { transform: translate(100px, 0); }
}

/* Follow Through - staggered children */
.parent > .child { animation: slide-in 300ms var(--ease-decelerate); }
.parent > .child:nth-child(1) { animation-delay: 0ms; }
.parent > .child:nth-child(2) { animation-delay: 50ms; }
.parent > .child:nth-child(3) { animation-delay: 100ms; }
```

## Performance Rules

- **ALWAYS** animate `transform` and `opacity` for GPU acceleration
- **NEVER** animate `width`, `height`, `top`, `left` (triggers layout)
- Use `will-change` sparingly and remove after animation completes
- Prefer CSS over JavaScript when animation is predictable
- Target 60fps — test on low-powered devices
- Respect `prefers-reduced-motion` for accessibility

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Critical Rules

- NEVER use `linear` easing for UI motion (feels robotic)
- ALWAYS provide `prefers-reduced-motion` fallback
- ALWAYS use `cubic-bezier` or named easing functions
- Keep micro-interactions under 200ms
- Keep standard transitions between 200-400ms
- Use overshoot easing for playful, energetic interfaces
- Use decelerate easing for entering elements
- Use accelerate easing for exiting elements
- Maintain consistent `transform-origin` across related elements

## Skill Categories (144 Skills)

This skill includes 144 specialized sub-skills organized across 12 categories. Reference the appropriate sub-skill for detailed guidance:

### By Domain (`skills/01-by-domain/`)
Web, mobile, game, data visualization, 3D, video, accessibility, and more.

### By Thinking Style (`skills/02-by-thinking-style/`)
Physics intuition, emotional narrative, rhythm pacing, spatial thinking, and more.

### By Role (`skills/03-by-role-persona/`)
Frontend developer, motion designer, creative director, game designer, and more.

### By Skill Level (`skills/04-by-skill-level/`)
From absolute beginner to master, including teaching and troubleshooting.

### By Animation Type (`skills/05-by-animation-type/`)
Entrances, exits, loops, hover, scroll, loading states, and transitions.

### By Emotional Outcome (`skills/06-by-emotional-outcome/`)
Joy, trust, elegance, urgency, calm, excitement, and more.

### By UI Element (`skills/07-by-ui-element/`)
Buttons, modals, cards, navigation, forms, notifications, and more.

### By Industry (`skills/08-by-industry/`)
Fintech, e-commerce, healthcare, education, SaaS, gaming, and more.

### By Tool/Framework (`skills/09-by-tool-framework/`)
CSS, GSAP, Framer Motion, React Spring, Lottie, Anime.js, Rive, and more.

### By Time Scale (`skills/10-by-time-scale/`)
From instant (0-100ms) to dramatic (2000ms+), including continuous loops.

### By Principle Focus (`skills/11-by-principle-focus/`)
Deep mastery of each individual principle.

### By Problem Type (`skills/12-by-problem-type/`)
Debugging, performance, accessibility, timing calibration, and more.

## How to Navigate Sub-Skills

When you need specific guidance, load the relevant sub-skill:

1. **By what you're building** → `skills/01-by-domain/` or `skills/07-by-ui-element/`
2. **By your role** → `skills/03-by-role-persona/`
3. **By your tool** → `skills/09-by-tool-framework/`
4. **By desired emotion** → `skills/06-by-emotional-outcome/`
5. **By problem to solve** → `skills/12-by-problem-type/`
6. **Deep dive a principle** → `skills/11-by-principle-focus/`

## Additional Resources

- For the complete skill index, see [index.md](index.md)
- Based on Disney's "The Illusion of Life" (Ollie Johnston & Frank Thomas, 1981)
- Original source: [dylantarre/animation-principles](https://github.com/dylantarre/animation-principles)
