---
name: tinyfish
description: Searches the web and extracts page content. Use when needing real-time web search results, fetching and extracting clean content from URLs, or scraping JavaScript-heavy pages. Best for web search, content extraction, and combining search results with full page content in a single workflow.
---

# TinyFish Web Search & Scraping

Search the web and extract clean page content via the TinyFish API. Combines search and fetch in a single lightweight skill — no MCP server needed.

## When to Use

**Use TinyFish** when you need to:
- Search the web and get ranked results with titles, snippets, and URLs
- Fetch and extract clean content from one or more URLs (JavaScript rendering included)
- Combine search + fetch in a pipeline: find URLs, then extract full page content
- Scrape JavaScript-heavy or dynamic web pages that simple curl can't handle
- Get geo-targeted search results by country and language

## Protocol

### Step 1: Web Search

```bash
scripts/tinyfish.sh search "<query>" [location] [language] [page]
```

**Parameters:**
- `query` (required) — Search query string. Supports `site:` and `-site:` operators
- `location` (optional) — Country code for geo-targeted results (US, GB, FR, DE, etc.)
- `language` (optional) — Language code (en, fr, de, etc.). Auto-resolves with location
- `page` (optional) — Page number for pagination (0-indexed, max 10)

**Examples:**
```bash
scripts/tinyfish.sh search "web automation tools" US en
scripts/tinyfish.sh search "best restaurants" FR fr
scripts/tinyfish.sh search "python tutorial site:docs.python.org"
scripts/tinyfish.sh search "recipe ideas -site:facebook.com"
```

### Step 2: Fetch Page Content

```bash
scripts/tinyfish.sh fetch "<url1>" ["<url2>"] [--format markdown|html|json] [--links] [--image-links]
```

**Parameters:**
- `urls` (required) — One or more URLs to fetch (max 10)
- `--format` (optional) — Output format: `markdown` (default), `html`, `json`
- `--links` (optional) — Include all `<a href>` URLs in output
- `--image-links` (optional) — Include all `<img src>` URLs in output

**Examples:**
```bash
scripts/tinyfish.sh fetch "https://example.com"
scripts/tinyfish.sh fetch "https://example.com" --format html --links
scripts/tinyfish.sh fetch "https://docs.tinyfish.ai/llms.txt" "https://tinyfish.ai"
```

### Step 3: Validate API Keys

```bash
scripts/tinyfish.sh validate
```

Tests all configured API keys against the search endpoint and reports pass/fail for each. Run once after setup or when key rotation seems off.

**Example:**
```bash
scripts/tinyfish.sh validate
```

### Step 4: Search then Fetch Pipeline

Combine both commands to find URLs and extract their content:

```bash
# Step 1: Find relevant pages
scripts/tinyfish.sh search "TinyFish web agent" US en

# Step 2: Extract full content from top results
scripts/tinyfish.sh fetch "https://result1.com" "https://result2.com"
```

## Critical Rules

1. **Specific queries win** - "web automation tools site:github.com" beats "tools"
2. **Search first, fetch second** - Use `search` to find URLs, then `fetch` to get content
3. **Fetch handles JS** - Use `fetch` for JavaScript-rendered pages that simple curl can't handle
4. **Max 10 URLs per fetch** - Batch up to 10 URLs in a single fetch request
5. **Current year is 2026** - Use this when recency matters; omit for timeless topics or use older years when historically relevant
6. **No guessing** - If search returns nothing, ask user before proceeding
7. **Fetch timeout is 150s** - Set appropriate client timeouts for fetch operations (110s per-URL backend timeout)
8. **TINYFISH_API_KEY must be exported** - The env var must be set before pi launches (in `.zshrc`/`.bashrc` or the parent shell). Launching pi from a non-login shell that doesn't source your profile will not have the key.

## Resources

See `reference/troubleshooting.md` for error handling, configuration, and common issues.
