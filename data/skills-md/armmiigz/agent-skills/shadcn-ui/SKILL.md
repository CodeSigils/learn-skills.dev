---
name: shadcn-ui
description: Use this skill to install, configure, and manage shadcn/ui components with Tailwind CSS v4. Trigger this WHENEVER the user needs to initialize a UI library, add specific components like "Button" or "Dialog", or apply custom branding to their interface.
license: MIT
compatibility: Designed for any Agent Skills-compliant client (e.g. Claude Code)
metadata:
  version: "1.2"
  triggers:
    - "install shadcn"
    - "add shadcn component"
    - "setup shadcn/ui"
    - "shadcn best practices"
    - "ui library setup"
---

# shadcn/ui Skill

This skill provides comprehensive guidance on managing shadcn/ui components within a modern web project. It focuses on the "Ownership over Dependency" model, ensuring components are properly integrated, customized, and maintained.

## Prerequisites
Before implementation, it is recommended to:
1.  **Define Brand Identity**: Use the `ui-foundations` skill to generate your color palette (OKLCH/HSL) and typographic system.
2.  **Generate Tokens**: Finalize your `@theme` and `:root` variables to ensure a consistent implementation phase.

## Core Principles
1. **Source Ownership**: You own the code in `components/ui`. Modify it directly when needed.
2. **Composition over Logic**: Keep business logic out of `components/ui`. Use wrapper components for feature-specific logic.
3. **Consistency**: Use CSS variables for theming and the `cn()` utility for class merging.

## Quick Workflow
Progress:
- [ ] **Infrastructure**: Use `npx shadcn@latest init` to set up the project.
- [ ] **Discovery**: Browse the [Component Catalog](./references/components.md) for the right tool.
- [ ] **Expansion**: Use `npx shadcn@latest add <component-name>` to pull source code.
- [ ] **Branding**: Customize `tailwind.config.ts` (or CSS `@theme`) and `components.json`.

## Gotchas
- **Tailwind v4 vs v3**: If using Tailwind v4, ensure you are using the latest `shadcn` CLI that supports CSS-only configuration.
- **Hydration Errors**: When using components with many client-side states (like `Sheet` or `Dialog`), ensure they are used within `Client Components` in Next.js.
- **Icon Defaults**: `shadcn` defaults to `lucide-react`. If using a different icon set, you must manually update the imported icons in the component source.
- **Z-Index Stacking**: Multiple overlays (Dialog over a Popover) can sometimes cause stacking issues. Use the `Portal` pattern provided by the underlying Radix primitives.

## Quick Setup (Automated)
If you prefer a fully automated setup, run the built-in setup script:

```bash
bash ./skills/shadcn-ui/scripts/setup.sh
```

## Reference Documentation
For detailed instructions, refer to the following local documentation:
- [Installation & Branding Configuration](./references/installation.md)
- [Coding Standards & Best Practices](./references/best-practices.md)
- [Component Catalog & Dependencies](./references/components.md)

## Usage Suitability
Ensure you are using the right component for the job:
- **Dialog vs Popover**: Use Dialog for intrusive actions; Popover for non-intrusive metadata.
- **Select vs Command**: Use Select for small lists; Command/Combobox for long, searchable lists.
- **Tooltip vs HoverCard**: Use Tooltip for brief labels; HoverCard for rich content previews.

