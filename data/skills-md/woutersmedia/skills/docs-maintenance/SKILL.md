---
name: docs-maintenance
description: >
  Automates maintenance of the documentation app (apps/docs).
  Use when asked to update docs, add a new API endpoint to the docs, sync SDK
  types with the documentation, regenerate navigation metadata, or add a new doc page.
  Triggers on tasks mentioning "update docs", "add endpoint to docs", "sync
  docs with SDK", "new doc page", or "regenerate navigation".
---

# Docs Maintenance

## Overview

The documentation lives in **`apps/docs`** — a standalone Next.js documentation app served at `/docs` on the main domain via a reverse-proxy rewrite in `apps/web/next.config.ts`.

**Recommended framework: [Nextra](https://nextra.site/) 4.x** — a Next.js-based docs framework with MDX support, sidebar navigation, and built-in search. Other documentation tools (Docusaurus, Mintlify, plain Next.js with MDX) are acceptable if the project has already adopted them. Check `apps/docs/package.json` to see what is in use.

The documentation is kept in sync with the SDK surface through:

1. **Navigation metadata** (`_meta.json` in Nextra, or equivalent) — maps file names to sidebar labels.
2. **This skill** — provides step-by-step instructions for keeping content in sync with SDK and API changes.

---

## File Locations (Nextra default layout)

| Purpose                            | Path                                                     |
| ---------------------------------- | -------------------------------------------------------- |
| All documentation MDX pages        | `apps/docs/content/*.mdx`                                |
| Sidebar navigation metadata        | `apps/docs/content/_meta.json`                           |
| Nextra config (Next.js wrapper)    | `apps/docs/next.config.ts`                               |
| Root layout                        | `apps/docs/app/layout.tsx`                               |
| MDX catch-all page renderer        | `apps/docs/app/[[...mdxPath]]/page.tsx`                  |
| Global CSS + color theme           | `apps/docs/app/globals.css`                              |

> If the project uses a different docs framework, adapt these paths accordingly.

---

## Running the Docs App Locally

```bash
# Preferred: pnpm (used in Wouters Media projects)
pnpm --filter docs dev        # docs only, port 3001
pnpm dev                      # everything together

# npm also works
npm run dev --workspace=apps/docs
```

---

## Adding a New Documentation Page

### 1. Create the MDX file

```bash
# Create apps/docs/content/<page-key>.mdx
```

Use an existing content file as a reference template.

### 2. Register the page in the navigation metadata

For Nextra, edit `apps/docs/content/_meta.json`:

```json
{
  "index": "Introduction",
  "my-new-page": "My New Page"
}
```

If the project uses a `generateDocsMeta` utility, use that instead:

```ts
import { generateDocsMeta, DOCS_DEFAULT_PAGES } from '@your-org/docs';

const meta = generateDocsMeta([
  ...DOCS_DEFAULT_PAGES,
  { key: 'my-new-page', label: 'My New Page' },
]);
```

### 3. Update the canonical page list

If the project maintains a `DOCS_DEFAULT_PAGES` constant, add the new entry:

```ts
export const DOCS_DEFAULT_PAGES: DocsMetaEntry[] = [
  // ... existing entries
  { key: 'my-new-page', label: 'My New Page' },
];
```

---

## Syncing Docs When the SDK Changes

When new types, endpoints, or methods are added to `packages/sdk/src/`:

1. **Identify the affected doc page** — each SDK method typically maps to one content file.
2. **Update the MDX page** with new endpoint docs, request/response examples, and any changed query parameters.
3. **If a new top-level resource is added**, create a new MDX page and register it in the navigation metadata.

---

## Styling Guidelines (Nextra)

```css
/* In apps/docs/app/globals.css */
:root {
  --nextra-primary-hue: 26;
  --nextra-primary-saturation: 90%;
  --nextra-primary-lightness: 48%;
}
```

To change the accent color, update those three `--nextra-primary-*` variables only. Do **not** add inline styles or override Nextra's utility classes directly.

For other documentation frameworks, follow the equivalent theming approach documented by that framework.

---

## Deployment

The docs app is a separate Next.js deployment. Set the `DOCS_URL` environment variable in the main web app to point to the deployed docs URL:

```
DOCS_URL=https://docs.example.co.nl
```

The `apps/web/next.config.ts` rewrite rule forwards all `/docs` traffic to `DOCS_URL`.

