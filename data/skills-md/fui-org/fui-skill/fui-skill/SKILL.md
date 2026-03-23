---
name: fui-skill
description: Use this skill when developing, structuring, reviewing, or modifying FUI web modules. It provides strict guidelines for the metadata-driven architecture (module.json), mandatory grid layout system, action protocols, and environment-aware workflow rules. Apply the canonical module structure in both editor and chat contexts. In editor or extension contexts with workspace access, work with the real module files. In chat or agent-chat contexts without workspace access, work from pasted artifacts while virtualizing the same module structure in the response.
---

# FUI Skill

Develop web modules using FUI's metadata-driven approach where UI and logic are defined in JSON.

## Execution Context

Apply this skill differently depending on the environment:

- **Editor / extension / workspace context**: Read, create, and modify local module folders and files when the environment actually exposes them. Apply the canonical local module structure directly.
- **Chat app / agent chat context**: Do not assume local file access, an existing workspace, or that the module folder already exists. Work from pasted JSON, snippets, screenshots, or explicit file attachments. Still apply the canonical module structure to virtualize the expected files, organize the response, and reason about what is missing.
- **Unclear context**: Infer from the available tools and artifacts. If no workspace or local files are explicitly available, default to chat-safe behavior and avoid pretending to read or update files that were never provided.

## Module Structure

Use this structure as the canonical folder layout for a complete FUI module in both environments. In editor or extension contexts, create or update these files directly. In chat contexts, use the same structure to virtualize the module, explain which files are involved, and provide the relevant file contents inline.

```text
<module-name>/
|-- _info.json                    (Required: module metadata)
|-- module.json                   (Required: core data/watch/controls/set)
|-- script.js                     (Recommended: helper logic)
|-- dependencies.json             (Recommended: external js/css)
|-- header.html                   (Recommended: all module/component CSS lives here)
|-- body.html                     (Optional)
|-- components/                   (Optional custom components)
|   |-- _components.json          (Required when using components/)
|   `-- uc-*.vue                  (Custom components, use `uc-` prefix)
```

For full structure rules and checklist, see [module-structure.md](references/module-structure.md). Apply that reference in both workspace-aware and chat environments.

## module.json Anatomy

The core file has four sections:

- **`data`**: Reactive state and named Actions
- **`watch`**: Observers triggering actions on change
- **`controls`**: UI layout (containers > rows > cols > elements)
- **`set`**: Module settings (title, menu)

## Action Protocol

Define logic in `data` as named action objects. Execute with `CALL`.

| Key            | Description                                   |
| :------------- | :-------------------------------------------- |
| `API`          | Endpoint to call                              |
| `IN`           | Input params (use `vueData.` or `item.` refs) |
| `OUT`          | Store response (e.g., `"myList"`)             |
| `CALLBACK`     | Action after success                          |
| `CONFIRM`      | Show confirmation first                       |
| `MESS`         | Toast message                                 |
| `CALL`         | Execute another named action                  |
| `IF/THEN/ELSE` | Conditional logic                             |
| `EXE`          | Raw JS (use sparingly)                        |

**Example:**

```json
"fetchUsers": {
  "API": "/api/users",
  "IN": { "GroupID": "vueData.selectedGroup" },
  "OUT": "userList",
  "CALLBACK": { "MESS": "Loaded!" }
}
```

### Literal String Rule (CRITICAL)

This rule applies when passing values inside Action Protocol `IN` blocks.
In `IN`, FUI core may evaluate string values as expressions/variables when the value has no spaces.

To force a literal string value, use one of these patterns:

- Prefix with backtick: ``"id": "`winUser"`` or ``"id": "`winUser`"``
- Wrap with single quotes inside JSON string: `"id": "'winUser'"`

Recommended for fields like `id`, `url`, or any key inside `IN` that must stay as plain text:

```json
{
  "FUN": "openWindow",
  "IN": {
    "id": "`winUser",
    "url": "'/fp/module?mid=123'"
  }
}
```

For Vue component props (`f-*`, `t-*`, `v-*`) without `:` in `attr`, values are plain strings by default.
Example: `"url": "/fp/module?mid=123"` is already a literal string prop.

## Layout System (Grid & Controls)

**CRITICAL RULE**: The `controls` array MUST follow the **Mandatory Grid System** structure at the top level.

### 1. Mandatory Grid Wrapper

All controls must be wrapped in a container > rows > cols structure:

```json
"controls": [
  {
    "prop": "fluid grid-list-md",
    "rows": [
      {
        "prop": "row",
        "cols": [
          // Control Objects go here
        ]
      }
    ]
  }
]
```

### 2. Control Object Structure

Inside the `cols` array (or nested `innerHTML`), every item is a **Control Object**:

| Key             | Type          | Description                                                                    |
| :-------------- | :------------ | :----------------------------------------------------------------------------- |
| **`el`**        | String        | HTML tag (`div`, `span`), Vue component, or FUI component.                     |
| **`attr`**      | Object        | Attributes/directives (`class`, `style`, `v-model`, `v-on:click`). **NO `@`**. |
| **`w`**         | Number/String | Column width. `1-12` (grid) or `pixel value`. REQUIRED for items in `cols`.    |
| **`col`**       | Object        | Wrapper config. Attributes for the grid column (`class`, `style`).             |
| **`innerHTML`** | String/Array  | Content. Can be recursive array of Control Objects.                            |

**Example:**

```json
{
  "el": "v-btn",
  "w": 6,
  "col": { "class": "text-center" },
  "attr": {
    ":disabled": "true",
    "color": "primary",
    "v-on:click": "CALL(vueData.submit)"
  },
  "innerHTML": "Submit"
}
```

### `innerHTML` Supports `{{ }}`

`innerHTML` string can use Vue template interpolation for reactive text binding.

```json
{
  "el": "div",
  "w": 12,
  "innerHTML": "Xin chao {{formData.fullName}}"
}
```

## Layout Rules

- **Wrapper**: ALWAYS start with the Grid Wrapper.
- **No `children`**: Use `innerHTML` (array) for nesting.
- **Attributes**: Use `attr` for element attributes. Use `col` for grid column attributes.
- **Events**: Use `v-on:click` (valid JSON), not `@click`.

## Vuetify 2 Styling Rule

- **Prefer Vuetify 2 classes first**: Always try Vuetify 2 utility classes, helper classes, and standard component props before writing inline `style`.
- **Use inline style only as fallback**: Only add `style` when Vuetify 2 classes/props cannot express the requirement cleanly.
- **Common preference order**:
  1. Vuetify component props (`color`, `outlined`, `dense`, `elevation`, `rounded`, `tile`, `justify`, `align`)
    2. Vuetify/helper classes (`pa-*`, `ma-*`, `d-flex`, `flex-*`, `justify-*`, `align-*`, `text-*`, `primary--text`, `rounded-*`)
    3. Custom class names
    4. Inline `style` as the last option
- **No component-local style blocks**: Do not write `<style>` or `<style scoped>` inside `.vue` components.
- **Header-owned styles**: Put all custom CSS in `header.html`. Treat `header.html` as the canonical place for module and component styles.
- **No template strings in `<template>`**: Never use backtick template strings inside Vue `<template></template>`. Use string concatenation or computed values instead.

## Reusable Component Rule

When creating `components/uc-*.vue`, prefer reusable building blocks over one-off screen-specific components.

- Design the component around clear props, emits, and slots before adding business-specific logic.
- Keep data fetching, routing, permissions, and page orchestration in `module.json` or parent actions unless the component is explicitly meant to own them.
- Use neutral names such as `items`, `value`, `label`, `loading`, `readonly`, `disabled`, `options`, or `config` instead of tightly coupling the component to one screen's entity names when a generic contract will work.
- Emit events upward (`input`, `change`, `select`, `submit`, `remove`, `action`) instead of mutating parent state indirectly.
- Support configurable empty/loading/error states with props or slots when the component is intended for repeated use.
- Only build a highly specific component when the UI is genuinely unique to one workflow and abstraction would make it harder to maintain.

## UI Templates

Copy templates from `examples/` as starting points. See [ui-templates.md](references/ui-templates.md) for usage guide.

| Template                                      | Type | Use Case                 |
| :-------------------------------------------- | :--- | :----------------------- |
| [form-basic.json](examples/form-basic.json)   | JSON | Simple input forms       |
| [table-crud.json](examples/table-crud.json)   | JSON | Data tables with CRUD    |
| [dialog-form.json](examples/dialog-form.json) | JSON | Modal dialogs            |
| [component.vue](examples/component.vue)       | Vue  | Custom component starter |

## Instructions

1.  **Match the environment before acting**:
    - In editor or extension contexts with workspace access, create or update the real module root directory first (for example, `my-module/`) and keep all module files inside it.
    - In chat or agent-chat contexts, do not claim to have created folders or edited files unless the environment actually supports it. Instead, use the same module structure virtually, present the folder tree when helpful, and provide the file contents the user should use.
    - When reviewing an existing module in chat, ask for the specific files or snippets that are needed instead of assuming they are readable from disk.

2.  **Creating New Modules**:
    - `module.json` (Required): Define UI and logic.
    - `_info.json` (Required): Metadata (ID, Name, Framework).
    - `dependencies.json` (Optional): External libs.
    - `header.html` (Optional but preferred for styling): Place all custom CSS here when the module needs styles.
    - `components/` (Optional): Custom Vue components.
    - If the environment is chat-only, return these as separate file payloads or clearly labeled code blocks.
    - When creating a custom Vue component, default to a reusable prop/event/slot API unless the user clearly needs a one-off component tied to a single screen.
    - Never add `<style>` or `<style scoped>` inside component files. Move those styles to `header.html`.
    - Never use backtick template strings inside Vue `<template>` markup.

3.  **Reference Docs**: See `references/` for component and function details:
    - [fastproject.md](references/fastproject.md) - Core action engine
    - [default-function.md](references/default-function.md) - Utility functions
    - [module-structure.md](references/module-structure.md) - Canonical module layout and file responsibilities
    - [components.md](references/components.md) - FUI `f-*` component catalog with examples
    - [component-table.md](references/component-table.md) - `f-table` and `f-table-view` reference
    - [script-map.md](references/script-map.md) - Quick lookup map for scripts/functions
    - [coding-standards.md](references/coding-standards.md) - Class naming & Menu config
    - [controls-patterns.md](references/controls-patterns.md) - Action patterns & Logic
    - [watcher-patterns.md](references/watcher-patterns.md) - Cascading and filter watcher best practices
    - [ui-templates.md](references/ui-templates.md) - Template usage guide
    - [advanced-techniques.md](references/advanced-techniques.md) - Advanced Logic & PDF patterns
    - [quality-assurance.md](references/quality-assurance.md) - Code Review & Edge Case Analysis

4.  **Module Assessment**: When asked to review or assess a module, follow the [Quality Assurance Protocol](references/quality-assurance.md) to identify issues, propose clean solutions, and analyze edge cases.
    - In workspace-aware environments, inspect the actual module files.
    - In chat contexts, review only the artifacts the user provided and say clearly when the assessment is limited by missing files.

5.  **Editing module.json**: Use valid JSON. Reference state with `vueData.` prefix.
    - In workspace-aware environments, edit the real `module.json`.
    - In chat contexts, return the updated JSON content or a focused patch snippet without implying filesystem access.

6.  **UI Templates**: Reuse the templates from `examples/`, then modify APIs and fields.
    - In workspace-aware environments, copy or adapt the template files directly.
    - In chat contexts, inline the adapted template content in the response.

## Continuous Improvement

This skill is a living document. The Agent MUST actively maintain and improve it based on user feedback and project evolution.

### Workflow

1.  **Post-Task Review**: After completing a complex task, ask the user: _"Are there any lessons, patterns, or corrections from this task that should be added to the FUI skill?"_
2.  **Correction & Refinement**: If the user points out a mistake or a better way to do something:
    - **Update**: Modify existing guidelines/references immediately.
    - **Delete**: Remove obsolete or incorrect information.
    - **Add**: Create new reference files for novel techniques.
3.  **Knowledge Consolidation**: Periodically review `references/` to merge scattered tips into cohesive guides.

**Goal**: Ensure `fui-skill` always reflects the most up-to-date, best-practice way to build FUI modules.

## Common Components

### f-table (Data Table with CRUD)

The `f-table` component supports built-in CRUD operations using `update-api` and `update-form`.

**Configuration:**

- **`ctrl-update`**: Add a header with `value: "ctrl-update"` to show Action buttons.
- **`update-form`**: Array of controls for the Add/Edit dialog.
- **`update-api`**: Object defining logic for `new`, `edit`, `delete` keys. Logic passed as string expressions.

**Example:**

```json
{
  "el": "f-table",
  "attr": {
    ":items": "vueData.list",
    ":headers": [
      { "text": "Name", "value": "name" },
      { "text": "Actions", "value": "ctrl-update" }
    ],
    ":update-form": [
      { "el": "v-text-field", "attr": { "v-model": "name", "label": "Name" } }
    ],
    ":update-api": {
      "new": { "list": "[...list, item]" },
      "edit": { "list": "list.map(i => i.id === item.id ? item : i)" },
      "delete": { "list": "list.filter(i => i.id !== item.id)" }
    }
  }
}
```
