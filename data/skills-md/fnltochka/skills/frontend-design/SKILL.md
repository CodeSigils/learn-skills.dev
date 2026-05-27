---
name: frontend-design
description: "Build or restyle frontend UI with this repo's visual taste. Use for web pages, landing pages, dashboards, components, HTML/CSS layouts, React/Vue/Svelte UI, and requests to make an interface look better. Add only project-specific design direction: avoid generic AI SaaS defaults, choose a clear aesthetic, and keep the implementation responsive and usable."
---

# Frontend design

Use this for UI work. It records taste, not a generic design process.

## Taste

- Pick one visual direction that fits the product: editorial, industrial, playful, utilitarian, luxury, brutalist, calm, dense, or sparse.
- Avoid the default AI SaaS look: purple gradients, Inter/Roboto/Arial stacks, centered hero plus three cards, generic glassmorphism, vague marketing copy.
- Use typography on purpose. Pair a distinctive display face with a readable body face when the project allows custom fonts.
- Make backgrounds feel designed: texture, pattern, depth, image treatment, asymmetric blocks, or strong whitespace. Do not leave a flat page unless flatness is the concept.
- Use color with intent. A narrow palette with one sharp accent usually beats many evenly weighted colors.
- Add motion only where it explains hierarchy or state: page entrance, section reveal, hover affordance, navigation transition.

## Implementation

- Preserve the app's existing framework, routing, component library, and design system unless the user asks for a new direction.
- Ship working responsive UI, not a static mockup.
- Check mobile layout explicitly: touch targets, wrapping, viewport height, overflow, and readable type.
- Prefer CSS variables or design tokens for repeated color, spacing, radius, shadow, and motion values.
- Keep accessibility visible: semantic elements, labels, focus states, contrast, reduced-motion fallback when animation is substantial.
- Match code complexity to the design. Quiet layouts need precision; expressive layouts can justify heavier visuals.

## Output

When editing files, make the change and summarize the visual direction plus the main implementation points. When only proposing a design, give one clear direction instead of a menu of generic options.
