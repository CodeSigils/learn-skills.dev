---
name: feature-planner
description: Interactive feature planning assistant that pulls a spec template from Notion, walks the user through filling it out step-by-step, and creates a completed feature spec as a new Notion page ready to paste into Claude Code. Use this skill whenever the user wants to plan a new feature, start a new page or screen, spec out a UI, create a feature brief, or says things like "let's plan a feature", "new feature spec", "I want to build something new", "help me spec this out", "create a feature plan", "plan the frontend for...", "start a new project", "scaffold a new app", or "I have an idea for...". Also trigger when the user references the Feature Spec Template or mentions wanting to fill out a spec for Claude Code. This skill is critical for the user's workflow of going from idea → Notion spec → Claude Code implementation, whether it's a brand-new project or a feature for an existing app.
---

# Feature Planner

An interactive skill that replaces Lovable in the user's workflow. It pulls the Feature Spec Template from Notion, guides the user through every section with smart defaults and clarifying questions, then creates a completed Notion page ready to be pasted into Claude Code.

## Template Location

The Feature Spec Template lives in Notion at page ID: `328ff269-2fbb-81af-841f-c500c24ca122`

## Workflow

### Step 0: Determine Scope

Before anything else, figure out whether the user is:

**A) Starting a brand-new project from scratch**
Signs: "new app", "new project", "I have an idea", "build something from scratch", "scaffold", no existing repo mentioned.

**B) Adding a feature to an existing app**
Signs: mentions an existing project name (Social Toolkit, Nameless Café, Agente Shei, Catador Pro, NightOwl, etc.), references existing pages or models, says "add", "extend", "new page for..."

**C) Redesigning or overhauling an existing UI**
Signs: "redesign", "redo the frontend", "make it look better", "overhaul the dashboard"

Use `ask_user_input_v0` to confirm:
- "New project from scratch"
- "New feature for an existing app"
- "Redesign / UI overhaul of existing app"

This choice affects the template flow:
- **New project**: Include project-level sections (project name, description, target audience, branding/identity, ALL initial pages, deployment target)
- **New feature**: Skip project-level context, focus on the feature pages, data, and interactions. Pull existing project context from Notion (see Step 1.5).
- **Redesign**: Fetch existing app context from Notion, focus on aesthetic direction and component redesign while preserving backend.

### Step 0.5: Pull Existing Project Context (Features & Redesigns only)

When the user is adding to an existing project:

1. **Ask which project** — or infer from conversation context
2. **Search Notion** for the project:
   ```
   Notion MCP: notion-search
   query: "[project name]"
   query_type: "internal"
   page_size: 5
   ```
3. **Fetch the project page** to understand what already exists:
   ```
   Notion MCP: notion-fetch
   id: [page_id from search results]
   ```
4. **Extract existing context:**
   - Tech stack (Rails, React, Inertia, etc.)
   - Existing pages/routes and their purpose
   - Data models and relationships
   - Design system / aesthetic direction already in use
   - Layouts and component patterns
   - Any existing feature specs linked from the project page

5. **Present a summary** to the user: "Here's what I found about [Project]. Based on this, the new feature will need to integrate with [existing models/pages]. Does this look right?"

This context informs everything downstream — the data shape section will reference existing models, the pages will fit into existing route patterns, and components will follow established conventions.

### Step 1: Fetch the Template

Use the Notion MCP `notion-fetch` tool to read the template page. This gives you the exact structure and sections to fill.

```
Notion MCP: notion-fetch
id: 328ff269-2fbb-81af-841f-c500c24ca122
```

### Step 2: Gather Context

Start by understanding what the user wants to build. If they've already described the feature/project in the current conversation, extract as much as you can from that context before asking questions. Don't re-ask things the user already told you.

Present a brief summary of what you understood so far, then begin filling gaps section by section.

### Step 3: Walk Through Each Section Interactively

Go through the template sections in this order, using the `ask_user_input_v0` tool for structured choices and prose questions for open-ended fields. Batch related questions together — don't ask one question per message.

**Round 1 — Core Definition (combine these):**
- Feature/Project Name (ask in prose if not already clear)
- What It Does (ask in prose, or propose a summary based on the conversation)
- Who Uses It (use `ask_user_input_v0` with the persona options)
- **[New projects only]** One-line tagline or value prop

**Round 2 — Design Direction (combine these):**
- Aesthetic Direction (use `ask_user_input_v0` with the 6 options from the template)
- Color direction (ask in prose, suggest based on the project context — e.g., Nameless Café brand colors, Agente Shei palette, Social Toolkit theme)
- Typography direction (suggest a pairing based on the aesthetic choice, let user confirm or override)
- Reference/inspiration (ask if they have any, skip if not)
- **[New projects only]** Brand identity: Does the project need a logo, favicon, and banner? (default: yes for new projects)

**Round 3 — Architecture (most technical, take your time):**
- Pages & Routes: Propose a set of pages based on the feature description, present as a table, ask user to confirm/modify
  - **[New projects]** Include auth pages (Login, Register, Forgot Password), a landing/home page, and a dashboard as defaults
- Data Shape: For each page, propose the props structure based on what the feature needs. Be specific about types.
- Interactions & Forms: List every action you can identify, ask if anything is missing

**Round 4 — Implementation Details:**
- Responsive Behavior: Propose sensible defaults based on the feature type (dashboard = sidebar layout, form = centered, listing = cards on mobile). Use `ask_user_input_v0` for key layout decisions.
- Components to Build: Propose a component list based on the pages and interactions
- Backend Dependencies: List models, migrations, services needed

**Round 5 — Acceptance Criteria:**
- Propose 5-8 acceptance criteria based on everything discussed
- Ask user to confirm, add, or remove items

### Step 4: Generate Brand Assets

After the spec is finalized but before creating the Notion page, handle image/asset generation for the project.

**For new projects or when the user requests branding:**

<!-- TODO: Integrate image generation into this step.
     Current options to evaluate:
     - Social Toolkit MCP: HiggsfieldImageTool for AI image generation
     - ComfyUI workflows via API (Floyo/RunPod)
     - Midjourney via API if available

     The generation step should produce these standard assets:
     1. Logo: app/frontend/assets/images/brand/logo.png (also generate logo.svg if possible)
     2. Logo dark variant: app/frontend/assets/images/brand/logo-dark.png
     3. Favicon: app/frontend/assets/images/brand/favicon.ico (also favicon.png at 32x32)
     4. Apple touch icon: app/frontend/assets/images/brand/apple-touch-icon.png (180x180)
     5. Banner/hero image: app/frontend/assets/images/brand/banner.png (1200x630, good for OG meta too)
     6. OG image: app/frontend/assets/images/brand/og-image.png (1200x630, can be same as banner)

     Additional images as needed by the frontend:
     7. Empty state illustration: app/frontend/assets/images/ui/empty-state.png
     8. Auth background: app/frontend/assets/images/ui/auth-bg.png
     9. 404 illustration: app/frontend/assets/images/ui/not-found.png

     When generating, pass the aesthetic direction, color palette, and project description
     as context to the image generation prompt.

     After generation, the images should be downloaded and placed in the standard paths above.
     The CLAUDE.md in the repo tells Claude Code to use these exact paths.

     FUTURE: Once integrated, remove this TODO block and replace with actual generation logic
     that uses the available image generation tools. The flow should be:
     1. Generate prompts based on aesthetic direction + brand identity
     2. Call image gen tool(s)
     3. Download results to standard paths
     4. Include the asset manifest in the Notion spec so Claude Code knows what was generated
-->

For now, include an "Assets to Generate" section in the Notion spec that lists the required images with their standard filenames and a description of what each should look like based on the aesthetic direction. The user can generate these manually or this step will be automated once image generation is integrated.

**Standard asset filenames (always use these):**

| Asset | Path | Size | Purpose |
|-------|------|------|---------|
| Logo | `brand/logo.png` | 512x512 | Primary logo |
| Logo (dark) | `brand/logo-dark.png` | 512x512 | Logo for dark backgrounds |
| Favicon ICO | `brand/favicon.ico` | 32x32 | Browser tab icon |
| Favicon PNG | `brand/favicon.png` | 32x32 | Modern browsers |
| Apple Touch Icon | `brand/apple-touch-icon.png` | 180x180 | iOS home screen |
| Banner / OG Image | `brand/og-image.png` | 1200x630 | Social sharing + hero |
| Empty State | `ui/empty-state.png` | 400x300 | Empty data states |
| Auth Background | `ui/auth-bg.png` | 1920x1080 | Login/register backdrop |

All paths are relative to `app/frontend/assets/images/`.

### Step 5: Create the Notion Page

Once all sections are filled, create a new Notion page using `notion-create-pages` with the completed spec. Use the same structure and formatting as the template, but with all placeholder text replaced by the actual content.

**For new projects**, the page title should be: `Project Spec: [Project Name]`
**For new features**, the page title should be: `Feature Spec: [Feature Name]`
**For redesigns**, the page title should be: `Redesign Spec: [App Name] — [Scope]`

The page icon should be: 🎯

Format the content in clean Notion markdown with proper headings, tables, checkboxes, and code blocks matching the template structure.

**Include the Assets section** with the standard filenames table and generation prompts for each image based on the aesthetic direction.

### Step 6: Present the Result

After creating the page, share the Notion URL with the user and provide:
1. A brief summary of the spec
2. The exact Claude Code prompt they should use, pre-filled based on the scope:

**For new projects:**
```
I'm starting a new project: [Project Name].
I've scaffolded from rails-ai-kit. Here's the full spec:

[paste Notion page content]

Start by:
1. Setting up the database (models + migrations)
2. Configuring the brand assets (images are in app/frontend/assets/images/brand/)
3. Building the layout shell (sidebar, header, footer)
4. Then build pages one at a time, starting with [most important page].
Follow the CLAUDE.md conventions for all frontend work.
```

**For new features:**
```
I want to build [Feature Name] in [Project]. Here's the full spec:

[paste Notion page content]

Start by creating the Rails backend (models, migrations, controllers, routes),
then build the frontend pages and components following the CLAUDE.md conventions.
Build one page at a time, starting with [most important page].
```

**For redesigns:**
```
I want to redesign [scope] in [Project]. Here's the spec:

[paste Notion page content]

Don't change any backend logic. Focus on the frontend components,
following the new aesthetic direction in the spec and the CLAUDE.md conventions.
Brand assets are in app/frontend/assets/images/brand/.
```

## Important Behavior Notes

- Be opinionated. Don't present empty options — always propose a default based on context and let the user confirm or change it. The user is a senior engineer; they'll push back if they disagrees.
- Use the user's project context when suggesting defaults. If the feature is for Nameless Café, suggest warm/grounded aesthetics and earthy colors. If for Social Toolkit, suggest technical/utilitarian. If for Agente Shei, suggest bold editorial or playful.
- Keep the conversation moving. Batch questions aggressively — 2-3 rounds of questions max before you have enough to create the spec. Don't ask 10 rounds of single questions.
- The data shape section is the most important for Claude Code to work well. Be specific about TypeScript types, not vague descriptions.
- For the components list, follow the CLAUDE.md convention: one component per file, 50 lines max, kebab-case filenames.
- If the user says "just go with your best guess" or similar, fill in sensible defaults and create the page. Don't block on every detail.
