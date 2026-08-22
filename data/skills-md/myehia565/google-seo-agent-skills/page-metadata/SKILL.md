---
name: page-metadata
description: Implements and audits title links, meta descriptions, robots meta, rel attributes, and heading hierarchy. Use when snippets are poor, titles are duplicated, or indexing directives need changing.
---

# Page Metadata

## Overview

Give Google clear on-page metadata and structure for titles, snippets, and indexing.

## When to Use

- Bad SERP titles/snippets, missing titles, heading chaos, robots directive edits

**Not for:** Full content rewrites (pair with `seo-content-authoring`).

## Official sources

- https://developers.google.com/search/docs/crawling-indexing/special-tags
- https://developers.google.com/search/docs/appearance/title-link
- https://developers.google.com/search/docs/appearance/snippet

## Process

1. Ensure a unique, descriptive `<title>` reflecting primary topic (Google may rewrite).
2. Write a specific meta description; avoid boilerplate sitewide reuse.
3. Confirm robots meta / header match intent (`index`/`noindex`, `follow`/`nofollow`).
4. Enforce **one** `<h1>` and logical `h2`/`h3` hierarchy.
5. Review relevant `rel` attributes (canonical handled in `canonicalization`).
6. Optionally run crawl audit script for title/robots extraction.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Meta description does not matter." | It often influences snippets; unique descriptions reduce ugly auto-snippets. |
| "Google rewrites titles anyway." | Strong titles still improve relevance and click clarity. |
| "Multiple H1s help SEO." | Prefer one clear H1; hierarchy beats stuffing. |

## Red Flags

- Inventing ranking factors not documented by Google
- Skipping verification ("looks fine")
- Advising spammy shortcuts (cloaking, doorways, link schemes)

## Verification

- [ ] Title unique and descriptive
- [ ] Exactly one H1 for the main topic
- [ ] Robots directives match indexing intent
