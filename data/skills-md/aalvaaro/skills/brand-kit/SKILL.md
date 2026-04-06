---
name: brand-kit
description: "Brand identity generator that creates logos, color palettes, typography, brand images, and checks domain and social media username availability. Suggests and verifies available handles across platforms. Outputs a complete brand kit to Notion, Google Drive, or downloadable PDF. Use this skill when the user says things like: 'create a brand for...', 'build a brand identity', 'I need a logo for...', 'brand kit for my business', 'check if this domain is available', 'find me a username for...', 'branding for my startup', 'design a brand', 'logo and brand for...', 'help me name my brand', or wants to create brand assets, check domain availability, or find social media handles."
---

# Brand Kit Generator

A research-driven skill that creates complete brand identities — logo, color palette, typography, imagery, domain names, and social media handles — with real-time availability checking. Goes beyond generic branding by researching the industry, competitors, and audience before generating any assets.

This is NOT a logo generator. It's a full brand identity system: research the space, define the strategy, generate visual assets, verify digital availability, and deliver a polished brand kit.

## Workflow Overview

```
Input (business idea, existing materials)
  -> Research (industry, competitors, audience)
    -> Brand Strategy (positioning, voice, personality)
      -> Visual Identity (colors, typography, mood)
        -> Logo Generation (AI-generated options)
          -> Brand Imagery (hero, social, patterns)
            -> Domain Check (suggest + verify availability)
              -> Username Check (suggest + verify across platforms)
                -> Brand Kit Delivery (Notion / Drive / PDF)
```

---

## Step 0: Gather Inputs

**Check for existing materials first:**

> "Do you have any existing materials I should start from? This could be a brief, mood board, existing logo, website, social profiles, or any document describing the brand. Share the file path, paste the content, or provide URLs — otherwise I'll walk you through it step by step."

**If materials are provided:**
- Read files using the Read tool
- Scrape URLs using `FirecrawlScrapeTool`
- Fetch social profiles using `FetchInstagramProfileTool`, `FetchTiktokProfileTool`, `FacebookBusinessPageInfoTool`
- Extract: brand name, industry, existing colors, tone, audience, visual style
- Present a summary table and confirm before proceeding. Skip to Step 2.

**If no materials — ask these in a single message:**

| Question | Purpose |
|----------|---------|
| Business or project name (or ideas for a name) | Brand naming |
| What does it do? Who is it for? | Positioning and audience |
| Industry or niche | Competitor research context |
| Brand personality in 3 words (e.g., bold, minimal, warm) | Visual direction |
| Any color preferences or colors to avoid? | Palette constraints |
| Where will this brand live? (web app, physical store, social-only, SaaS) | Asset requirements |
| Preferred language for brand copy | Localization |

---

## Step 1: Research Phase

Run all applicable research in parallel.

### 1A: Industry & Competitor Research

```
Social Toolkit MCP:
- PerplexitySonarSearchTool -> "[industry] branding trends 2025" (current visual trends)
- PerplexitySonarSearchTool -> "best [industry] brands [region]" (competitor landscape)
- GoogleNewsSearchTool -> "[industry] brand design" (recent trends, rebrands)
```

### 1B: Competitor Visual Analysis

For 2-3 top competitors identified in 1A:

```
Social Toolkit MCP:
- FirecrawlScrapeTool -> competitor websites (extract color schemes, typography, tone)
- FetchInstagramProfileTool -> competitor handles (visual style, content patterns)
```

**Extract from each competitor:**
- Color palette (dominant, accent, neutral)
- Typography style (serif, sans-serif, display)
- Visual tone (photography vs illustration, dark vs light, busy vs minimal)
- Logo style (wordmark, symbol, combination, emblem)
- Brand voice (formal, playful, technical, warm)

### 1C: Audience Research

```
Social Toolkit MCP:
- GoogleForumsSearchTool -> "[target audience] preferences [industry]" (what resonates)
- PerplexitySonarSearchTool -> "[target audience] demographics design preferences"
```

**Compile a research summary:**
> "Here's what I found about the [industry] landscape: [key findings]. The main competitors use [patterns]. The target audience responds to [preferences]. I'll use this to differentiate the brand. Ready to proceed?"

---

## Step 2: Brand Strategy

Based on research, define the brand strategy. Present as a structured summary:

### Brand Positioning

| Element | Definition |
|---------|-----------|
| Brand promise | One sentence: what the brand delivers |
| Differentiator | What sets it apart from competitors found in research |
| Target audience | Primary and secondary personas |
| Brand personality | 3-5 traits (e.g., bold, approachable, innovative) |
| Brand voice | How it speaks (tone, vocabulary, formality level) |
| Emotional territory | How it should make people feel |

### Visual Direction

Based on personality and audience, propose a visual direction:

| Direction | Description |
|-----------|-------------|
| Style A | [e.g., "Minimal & Premium — clean lines, generous whitespace, muted palette, geometric logo"] |
| Style B | [e.g., "Warm & Organic — earth tones, rounded shapes, hand-drawn feel, botanical accents"] |
| Style C | [e.g., "Bold & Energetic — high contrast, vibrant colors, dynamic shapes, strong typography"] |

Present all three options with a brief mood description. Ask the user to pick one or combine elements.

> "Which direction feels right? Pick one, or tell me what to combine from each."

---

## Step 3: Visual Identity

### 3A: Color Palette

Generate a complete palette based on the chosen direction:

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| Primary | [name] | `#XXXXXX` | Main brand color, CTAs, headers |
| Secondary | [name] | `#XXXXXX` | Supporting elements, accents |
| Accent | [name] | `#XXXXXX` | Highlights, notifications, links |
| Neutral Dark | [name] | `#XXXXXX` | Body text, headings |
| Neutral Light | [name] | `#XXXXXX` | Backgrounds, cards |
| Background | [name] | `#XXXXXX` | Page background |

Include contrast ratios for accessibility (WCAG AA minimum).

### 3B: Typography

Recommend a font pairing (Google Fonts for accessibility):

| Role | Font | Weight | Usage |
|------|------|--------|-------|
| Headlines | [font name] | Bold (700) | H1-H3, hero text |
| Body | [font name] | Regular (400) | Paragraphs, UI text |
| Accent (optional) | [font name] | Medium (500) | Buttons, labels, captions |

### 3C: Visual Style Guide

Define the overall aesthetic rules:

- Photography style (if applicable): [e.g., natural light, high contrast, desaturated]
- Illustration style (if applicable): [e.g., flat, isometric, hand-drawn, geometric]
- Icon style: [e.g., outlined, filled, duotone]
- Corner radius: [e.g., sharp, slightly rounded (4px), fully rounded (12px+)]
- Spacing philosophy: [e.g., generous whitespace, compact and dense]
- Pattern/texture: [e.g., subtle grain, geometric patterns, clean flat]

---

## Step 4: Logo Generation

Generate logo options using available image generation tools.

**Check for `infsh` CLI availability first:**
```bash
which infsh
```

**If available**, generate logos using the model best suited for graphic design:
```bash
infsh app run falai/flux-dev-lora --input '{
  "prompt": "[logo prompt based on brand strategy]"
}'
```

**If `infsh` is not available**, use the Social Toolkit `HiggsfieldImageTool` with the `nano_banana_pro` model (optimized for logos and simple graphics):

```
HiggsfieldImageTool:
  model: "nano_banana_pro"
  prompt: "[logo prompt]"
  aspect_ratio: "1:1"
  resolution: "1080p"
```

**Generate 3-4 logo variants:**

| Variant | Style | Prompt Focus |
|---------|-------|-------------|
| Option A | Symbol/Icon | Abstract or representational mark, no text |
| Option B | Wordmark | Stylized brand name as the logo |
| Option C | Combination | Symbol + brand name together |
| Option D | Monogram | Initials or abbreviation, compact form |

**Prompt engineering for logos:**
- Include the brand personality traits in every prompt
- Specify "logo design, vector style, clean lines, [brand colors], transparent background"
- Reference the visual direction chosen in Step 2
- Avoid photorealism — logos need to work as flat graphics
- Specify "no text" for symbol variants to avoid garbled AI text

**Download all generated logos** to the output directory.

---

## Step 5: Brand Imagery

Generate supporting brand images for use across web and social.

**Image set to generate:**

| Image | Purpose | Aspect | Model |
|-------|---------|--------|-------|
| Hero/Banner | Website header, social cover | 16:9 | `nano_banana_2` or `infsh` |
| Social profile picture | Instagram, TikTok, X avatar | 1:1 | `nano_banana_pro` |
| OG/Share image | Link preview image | 16:9 | `nano_banana_2` or `infsh` |
| Pattern/Texture | Background element, brand texture | 1:1 | `nano_banana_2` or `infsh` |
| Lifestyle/Mood (2-3) | Social media content, about sections | 4:3 | `soul_2` or `infsh` |

**Prompt engineering for brand images:**
- Use the brand's color palette explicitly in prompts
- Match the visual style guide from Step 3C
- Reference the industry and audience context from research
- Never generate generic stock-photo-style images

**Fallback chain:**
1. `infsh` CLI (preferred — FLUX or Grok models)
2. `HiggsfieldImageTool` (Social Toolkit MCP)
3. CSS-only effects + detailed prompts saved for manual generation later

**Download all generated images** to the output directory alongside the logos.

---

## Step 6: Domain Name Suggestions

Suggest 8-12 domain name options based on the brand name, positioning, and industry.

**Naming strategies to cover:**

| Strategy | Example |
|----------|---------|
| Exact match | `brandname.com` |
| With prefix | `get[brand].com`, `try[brand].com`, `hello[brand].com` |
| With suffix | `[brand]app.com`, `[brand]hq.com`, `[brand]studio.com` |
| Alternative TLD | `brandname.io`, `brandname.co`, `brandname.dev`, `brandname.shop` |
| Creative variation | Abbreviation, portmanteau, related word |

**Check availability for each domain by fetching the URL and checking for non-200 responses:**

```
WebFetch -> https://[domain]
```

A connection error, 404, or "domain not found" page indicates the domain is likely available. A 200 with real content indicates it's taken. A parked/for-sale page means it's registered but potentially purchasable.

**Present results as a table:**

| Domain | Status | Notes |
|--------|--------|-------|
| `brandname.com` | Taken | Active website |
| `brandname.io` | Available | Recommended |
| `getbrandname.com` | Available | Good alternative |
| `brandname.co` | Parked | For sale — may be purchasable |

Highlight the top 2-3 recommendations with reasoning.

---

## Step 7: Social Media Username Check

Suggest 5-8 username options and check availability across platforms.

**Platforms to check:**

| Platform | URL Pattern |
|----------|-------------|
| Instagram | `https://www.instagram.com/[username]/` |
| TikTok | `https://www.tiktok.com/@[username]` |
| X (Twitter) | `https://x.com/[username]` |
| YouTube | `https://www.youtube.com/@[username]` |
| Facebook | `https://www.facebook.com/[username]` |
| GitHub | `https://github.com/[username]` |
| LinkedIn | `https://www.linkedin.com/company/[username]` |

**Check availability by fetching each URL:**

```
WebFetch -> [platform URL with username]
```

A 404 response or "page not found" content indicates the username is likely available. A 200 with a real profile means it's taken.

**Run all platform checks for each username in parallel** to minimize wait time.

**Present results as a matrix:**

| Username | IG | TikTok | X | YouTube | FB | GitHub |
|----------|----|--------|---|---------|----|--------|
| `brandname` | Taken | Available | Available | Available | Taken | Available |
| `brandname_official` | Available | Available | Taken | Available | Available | Available |
| `getbrandname` | Available | Available | Available | Available | Available | Available |

Highlight usernames that are available across ALL platforms. Recommend the most consistent handle.

> "My top recommendation is `@[username]` — it's available on all [N] platforms and matches the domain `[domain]`. Want me to finalize the brand kit with these?"

---

## Step 8: Brand Kit Delivery

Compile all brand assets into a deliverable. Ask the user which output format to use:

> "How would you like the brand kit delivered?"
> 1. **Notion** — creates a structured Notion page with all assets, colors, fonts, and availability results
> 2. **Google Drive** — generates an HTML brand guide + asset folder ready to upload
> 3. **Download (PDF-ready)** — generates a self-contained HTML brand guide, opens in browser for PDF export via print

### Option 1: Notion

Use `notion-create-pages` to create a brand kit page with sections:
- Brand Strategy (positioning, personality, voice)
- Color Palette (with hex swatches)
- Typography (font names, weights, pairings)
- Logo Options (embedded images)
- Brand Imagery (embedded images)
- Domain Recommendations (availability table)
- Social Media Handles (availability matrix)
- Visual Style Guide (rules and guidelines)

### Option 2: Google Drive

Generate a folder structure:
```
brand-kit-[brandname]/
+-- brand-guide.html          # Visual brand guide (self-contained)
+-- logos/
|   +-- logo-symbol.png
|   +-- logo-wordmark.png
|   +-- logo-combination.png
|   +-- logo-monogram.png
+-- images/
|   +-- hero-banner.png
|   +-- social-avatar.png
|   +-- og-share.png
|   +-- pattern-texture.png
|   +-- lifestyle-1.png
|   +-- lifestyle-2.png
+-- availability-report.md    # Domain + username availability results
```

Save to `/tmp/brand-kit-[brandname]/` and open the brand guide in the browser.

### Option 3: Download (PDF-ready)

Generate a single self-contained HTML file with:
- All images embedded as base64 or referenced from downloaded files
- Print-optimized CSS (`@media print` with page breaks)
- Clean layout: cover page, strategy, palette swatches, typography samples, logo showcase, imagery grid, availability tables
- Open in the default browser with instructions: "Print to PDF (Cmd+P / Ctrl+P) to save"

Save to `/tmp/brand-kit-[brandname]/brand-guide.html` and open in the browser.

---

## Conventions

- **Research before creating** — never generate logos or suggest names without understanding the industry and audience first.
- **Parallel operations** — run all social media checks, image generations, and domain lookups in parallel where possible.
- **Confirm at gates** — confirm brand strategy (Step 2) and visual direction before generating assets.
- **Real availability data** — always check domains and usernames live. Never guess availability.
- **Download all assets** — every generated image must be downloaded to the output directory, not just linked.
- **Language detection** — default to auto-detecting language from the user's input. Support explicit override.
