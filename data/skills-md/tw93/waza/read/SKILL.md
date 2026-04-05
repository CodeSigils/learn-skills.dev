---
name: read
description: Fetches any URL, web page, or PDF as clean Markdown with title, source, and summary. Use when reading external content. Not for local files already in the repo.
version: 1.2.0
allowed-tools:
  - Bash
  - Read
  - Write
---

# Read: Fetch Any URL or PDF as Markdown

Convert any URL or local PDF to clean Markdown and save it.

## Routing

| Input | Method |
|-------|--------|
| `mp.weixin.qq.com` | WeChat script |
| `.pdf` URL or local PDF path | PDF extraction |
| Everything else | Proxy cascade |

## Proxy Cascade

Try in order. Success = non-empty output with readable content. If a proxy returns empty, an error page, or fewer than 5 lines, treat it as failed and try the next:

### 1. r.jina.ai

```bash
curl -sL "https://r.jina.ai/{url}"
```

Wide coverage, preserves image links. Try this first.

### 2. defuddle.md

```bash
curl -sL "https://defuddle.md/{url}"
```

Cleaner output with YAML frontmatter. Use if r.jina.ai returns empty or errors.

### 3. Local tools

```bash
npx agent-fetch "{url}" --json
# or
defuddle parse "{url}" -m -j
```

Last resort if both proxies fail.

## PDF to Markdown

### Remote PDF URL

r.jina.ai handles PDF URLs directly:

```bash
curl -sL "https://r.jina.ai/{pdf_url}"
```

If that fails, download and extract locally:

```bash
curl -sL "{pdf_url}" -o /tmp/input.pdf
pdftotext -layout /tmp/input.pdf -
```

### Local PDF file

```bash
# Best quality (requires: pip install marker-pdf)
marker_single /path/to/file.pdf --output_dir ~/Downloads/

# Fast, text-heavy PDFs (requires: brew install poppler)
pdftotext -layout /path/to/file.pdf - | sed 's/\f/\n---\n/g'

# No-dependency fallback
python3 -c "
import pypdf, sys
r = pypdf.PdfReader(sys.argv[1])
print('\n\n'.join(p.extract_text() for p in r.pages))
" /path/to/file.pdf
```

Use `marker` when layout matters (papers, tables). Use `pdftotext` for speed.

## WeChat Public Account

Requires a local `fetch_weixin.py` with `playwright`, `beautifulsoup4`, `lxml`.

```bash
python3 /path/to/fetch_weixin.py "{url}"
```

Output: YAML frontmatter (title, author, date, url) + Markdown body.
Fallback: use proxy cascade if no local script is available.

## Output Format

```
Title:  {title}
Author: {author} (if available)
Source: {platform}
URL:    {original url}

Summary
{3-5 sentence summary}

Content
{full Markdown, truncated at 200 lines if long}
```

## Saving

Save to `~/Downloads/{title}.md` with YAML frontmatter by default.
Skip only if user says "just preview" or "don't save". Tell the user the saved path.

## Notes

- r.jina.ai and defuddle.md require no API key
- Network failures: prepend local proxy env vars if available
- Long content: `| head -n 200` to preview first
- GitHub URLs: prefer `gh` CLI over fetching directly
