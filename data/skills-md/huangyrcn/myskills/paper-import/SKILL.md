---
name: paper-import
description: >
  Import a paper into the local literature library: metadata, PDF, LaTeX source, Markdown, and code repo.
  Use this skill whenever the user wants to get, download, fetch, find, import, or save a paper —
  even if they only mention the title, arXiv ID, or DOI.
  Also use when the user wants to find or clone the code/implementation for a paper.
  Triggers: "下载论文", "获取论文", "找这篇论文", "下载这篇", "导入论文", "import paper",
  "get paper", "fetch paper", "download paper", "找代码", "下载代码", "find the code",
  "get the implementation", "clone the repo", "有没有开源代码",
  or any mention of acquiring a paper or its code.
  Can be called silently by other skills (lit-review, idea-discovery) with an arXiv ID or DOI.
  Output: literature/{identifier}/ with metadata.yaml, paper/, and optional repo/.
---

# Paper Import

Downloads a complete paper package into a standardized local directory.

## Output Structure

```
literature/{identifier}/          e.g.  papers/vaswani2017attention/
├── metadata.yaml            paper metadata + asset paths
├── paper/
│   ├── paper.pdf            PDF full text
│   ├── paper.md             Markdown version (via /pdf-to-md)
│   ├── main.tex             LaTeX source (arXiv only, flattened)
│   └── refs.bib             bibliography (if present)
└── repo/                    code repository (optional)
```

`{identifier}` = `{author}{year}{keyword}`, e.g. `vaswani2017attention`.
See `references/identifier-generation.md` for rules.
See `references/metadata-schema.md` for the full metadata.yaml field reference.

---

## Step 1: Resolve Metadata

Extract from user message: title, arXiv ID (`1706.03762` or full URL), or DOI.

```bash
# SKILL_DIR is the directory containing this SKILL.md
# (shown as "Base directory" when the skill loads)
python3 "${SKILL_DIR}/scripts/query_apis.py" "{query}"
```

This queries S2, arXiv, OpenAlex, OpenReview, Crossref, and others in parallel,
deduplicates by DOI, and writes `literature/{identifier}/metadata.yaml`.
Candidates are saved to `/tmp/candidates.json`.

**When to interact vs. stay silent:**

- arXiv ID or DOI provided → single candidate → **silent, proceed**
- Title search, top candidate similarity ≥ 0.9 and gap > 0.05 from next → **silent, proceed**
- Title search, top two candidates within 0.05 similarity → show top 3, ask user to pick

When called by another skill with an arXiv ID or DOI, always stay silent.

---

## Step 2: Download Paper

```bash
PAPER_DIR="literature/{identifier}/paper"
mkdir -p "${PAPER_DIR}"
```

**Download PDF** — OA-first Fallback 链:

```bash
# 使用 OA-first Fallback 链下载
# 自动尝试: 原生链接 → OA 仓库 → Unpaywall → Sci-Hub
python3 "${SKILL_DIR}/scripts/download_pdf.py" \
    --metadata "literature/{identifier}/metadata.yaml" \
    --output "${PAPER_DIR}"
```

如果下载失败，脚本会自动尝试多个来源:
1. **原生下载**: pdf_urls 中的链接（按可靠性排序）
2. **OA Repository**: OpenAIRE → CORE → EuropePMC → PMC
3. **Unpaywall**: 通过 DOI 解析开放获取版本
4. **Sci-Hub**: 最后手段（可通过 `--no-scihub` 禁用）

**手动下载** (备用方案):

如果自动下载失败，可以手动尝试:

```bash
curl -L \
  -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  -o "${PAPER_DIR}/paper.pdf" "{url}"

# Verify it's actually a PDF:
file "${PAPER_DIR}/paper.pdf" | grep -q "PDF" && echo "OK" || echo "FAILED - try next source"
```

**Download LaTeX** — only when `latex_source.available: true`:

```bash
curl -L -o /tmp/latex_src.tar.gz "{latex_source.url}"

if file /tmp/latex_src.tar.gz | grep -qE "gzip|tar"; then
    tar -xzf /tmp/latex_src.tar.gz -C "${PAPER_DIR}/" 2>/dev/null || \
    tar -xf  /tmp/latex_src.tar.gz -C "${PAPER_DIR}/"

    # Flatten: move .tex and .bib up to paper/ root (no nested subdirs)
    find "${PAPER_DIR}" -mindepth 2 \( -name "*.tex" -o -name "*.bib" \) \
        -exec mv {} "${PAPER_DIR}/" \; 2>/dev/null
    find "${PAPER_DIR}" -mindepth 1 -type d -empty -delete 2>/dev/null
fi
```

**Convert PDF → Markdown** (always, via `/pdf-to-md` skill):

```
/pdf-to-md "${PAPER_DIR}/paper.pdf"
```

This produces `paper.md` + `paper_images/` in the same directory.
If `/pdf-to-md` is unavailable, fallback to PyMuPDF4LLM locally:

```bash
python3 -c "
import pymupdf4llm
md_text = pymupdf4llm.to_markdown('${PAPER_DIR}/paper.pdf', table_strategy='text', show_progress=False)
with open('${PAPER_DIR}/paper.md', 'w', encoding='utf-8') as f:
    f.write(md_text)
print('✓ Converted to Markdown')
"
```

---

## Step 3: Find Code

**Skip this step entirely** if the user only asked to download the paper without mentioning code,
implementation, or repository.

Search in priority order — stop at the first confirmed result.

### ① LaTeX source (most reliable — author embedded it)

```bash
grep -rhoE 'https?://(github|gitlab|gitee)\.com/[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+' \
    "${PAPER_DIR}"/*.tex 2>/dev/null | sort -u
```

### ② PDF hyperlinks (clickable embedded links)

```bash
# pdftotext: extracts text with URLs
pdftotext -layout "${PAPER_DIR}/paper.pdf" - 2>/dev/null | \
    grep -oE 'https?://(github|gitlab|gitee)\.com/[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+'

# mutool: extracts annotation links (often more complete)
mutool show "${PAPER_DIR}/paper.pdf" links 2>/dev/null | \
    grep -iE '(github|gitlab|gitee)\.com'
```

### ③ Markdown context window (semantic judgment)

When LaTeX and hyperlinks find nothing, search `paper.md` for code-hosting URLs:

```bash
grep -n -oE 'https?://(github|gitlab|gitee)\.com/[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+' \
    "${PAPER_DIR}/paper.md"
```

For each URL found at line N, extract surrounding context:

```bash
sed -n "$((N-3)),$((N+3))p" "${PAPER_DIR}/paper.md"
```

Read the context and judge intent:
- "our code is available at...", "code released at...", "we release..." → **this paper's code ✓**
- "compared with [X] (code: ...)", "based on [Y]'s github..." → someone else's code ✗
- Ambiguous → mark as low-confidence candidate, keep searching

### ④ Web search (final fallback)

Use **searxng-search skill** (preferred) or **WebSearch tool** if searxng is unavailable:

```
# searxng-search skill:
query: '"{paper title}" github implementation'   category: it

# WebSearch tool fallback:
"{paper title}" site:github.com OR site:gitee.com implementation
```

### Validate and select repo

For each candidate URL, validate using `references/github-api.md`:

- Fetch repo metadata (stars, description) and README (first 5000 chars)
- Score: title match in README (3pt) + "official implementation" text (3pt) +
  arXiv/DOI in README (2pt) + author name (2pt) + train/main script exists (1pt)
- Score ≥ 5 → **clone automatically**
- Score 2–4 → show candidate with score, ask user to confirm
- Score < 2 → skip

```bash
# Clone (with optional GitHub token auth)
REPO_DIR="literature/{identifier}/repo"
if [ -n "$GITHUB_TOKEN" ]; then
    git clone "https://${GITHUB_TOKEN}@github.com/{owner}/{repo}.git" "${REPO_DIR}"
else
    git clone "{repo_url}" "${REPO_DIR}"
fi

[ -d "${REPO_DIR}/.git" ] && echo "✓ Cloned" || echo "✗ Clone failed"
```

---

## Step 4: Update metadata.yaml

Append the `assets` section after Steps 2–3:

```bash
cat >> "literature/{identifier}/metadata.yaml" << 'YAML'

# local assets (appended by get-paper)
assets:
  pdf: paper/paper.pdf
  markdown: paper/paper.md
YAML

# Append latex_dir only if LaTeX was downloaded
[ -f "literature/{identifier}/paper/main.tex" ] && \
    echo "  latex_dir: paper/" >> "literature/{identifier}/metadata.yaml"

# Append repo only if code was cloned
[ -d "literature/{identifier}/repo/.git" ] && \
    echo "  repo: repo/" >> "literature/{identifier}/metadata.yaml"
```

---

## Step 5: Report

```
✓ papers/vaswani2017attention/

  paper/paper.pdf     1.4 MB  [arxiv]
  paper/paper.md              [/pdf-to-md]
  paper/main.tex              [LaTeX, 3 .tex files]
  repo/                       [github.com/jadore801120/attention-is-all-you-need ⭐8.2k]
```

If code was not fetched (user didn't ask), omit the `repo/` line.
If LaTeX was not available (non-arXiv paper), omit the `main.tex` line.

---

## Quick Reference

```bash
# Check what was fetched
ls literature/{identifier}/paper/
cat literature/{identifier}/metadata.yaml

# Read the paper
cat literature/{identifier}/paper/paper.md

# Explore code
ls literature/{identifier}/repo/
```
