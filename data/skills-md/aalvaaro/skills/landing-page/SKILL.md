---
name: landing-page
description: "Research-driven landing page generator. Pulls data from social media, websites, Google Maps, YouTube, forums, and optionally a CV to build a complete profile of a company or person. Analyzes the data as a marketer to extract competitive advantages, value props, audience insights, and brand voice. Then generates a compelling landing page with AI-generated images tailored to the audience. Use this skill when the user says things like: 'create a landing page for...', 'build a website for this business', 'make a landing page from their social media', 'generate a page for this company', 'research and build a site for...', 'landing page for my client', 'portfolio page for...', 'personal brand page', or provides social media handles, a website URL, or a CV and wants a page built from it."
---

# Landing Page Generator

A research-driven skill that builds compelling landing pages by first deeply understanding who the subject is — through social media, web presence, reviews, and optionally a CV — then crafting copy, visuals, and design that resonates with their specific audience.

This is NOT a generic page builder. It's a research-first approach: understand the subject deeply, then design for their audience.

## Workflow Overview

```
Input (handles, URLs, CV)
  → Research (Social Toolkit + SearchAPI MCPs)
    → Analysis (marketer/SEO lens)
      → Design Direction (audience-driven)
        → Copy Generation (voice-matched)
          → Image Generation (aesthetic-matched)
            → Landing Page (deploy-ready)
```

---

## Step 0: Gather Inputs

Ask the user for as many of these as available. At minimum, one social media handle or a website URL is required.

**Structured inputs to request:**

| Input | Example | Required? |
|-------|---------|-----------|
| Instagram handle | `@kerikuamorelia` | At least one social profile |
| TikTok handle | `@username` | Optional |
| Facebook page | `Page Name` | Optional |
| YouTube channel | `@channel` or URL | Optional |
| LinkedIn | URL or company name | Optional |
| Website URL | `https://example.com` | Optional |
| Google Maps / Business name | `K'ERI KUA Morelia` | Optional |
| CV / Resume | File path or pasted text | Optional |
| Target audience hint | "young professionals in Mexico" | Optional |
| Language | es, en, pt, etc. | Default: auto-detect from content |

Also ask:
- **Who is this for?** (themselves, a client, a friend, a business they found)
- **What's the goal?** (get clients, build community, sell products, personal brand, portfolio)

---

## Step 1: Research Phase

Pull data from ALL available sources in parallel. Use **Social Toolkit MCP** as primary and **SearchAPI MCP** as backup/complement.

### 1A: Social Media Profiles

Fetch all provided profiles in parallel:

```
Social Toolkit MCP:
- FetchInstagramProfileTool → username (gets bio, followers, posts, captions, engagement)
- FetchTiktokProfileTool → username (gets bio, followers, videos, engagement)
- FacebookBusinessPageInfoTool → page name (gets about, likes, posts)
- FetchYoutubeChannelTool → channel (gets description, subscribers, videos)
- FetchYoutubeChannelVideosTool → channel (gets recent video titles, views)
```

**From each profile, extract:**
- Bio / description text
- Follower counts and engagement rates
- Last 10-12 posts/videos with captions
- Hashtags used frequently
- Posting frequency and content themes
- Visual style (from post descriptions — dark/light, colorful/muted, professional/casual)
- Language and tone of voice
- Links to website or other profiles
- Location information

### 1B: Website Scraping

If a website URL is provided (or found in social bios):

```
Social Toolkit MCP:
- FirecrawlMapTool → URL (discover all pages on the site)
- FirecrawlScrapeTool → URL (scrape main page content)
- FirecrawlScrapeTool → key subpages (about, services, contact)
```

**Extract:**
- Tagline / hero text
- Services or products listed
- About section / company story
- Testimonials if present
- Contact information
- Existing color scheme and fonts
- SEO meta tags (title, description)
- Call-to-action patterns

### 1C: Google Maps & Reviews

If a business name or location is provided:

```
SearchAPI MCP:
- google_maps_search → business name + location
- google_maps_place → place_id from search (gets reviews, rating, hours, photos)
```

**Extract:**
- Rating and review count
- Business category/type
- Address, hours, phone
- **GPS coordinates** (`latitude`, `longitude`) — save these for the map embed
- Review themes (what customers praise, what they complain about)
- Popular times
- Payment methods, amenities
- Photos description
- `people_also_search_for` — save these as potential competitors for Step 1G

### 1D: Web Research

Search for additional context:

```
Social Toolkit MCP:
- GoogleNewsSearchTool → business/person name (recent press, mentions)
- GoogleForumsSearchTool → business/person name (community discussions, Reddit mentions)
- PerplexitySonarSearchTool → "who is [name] and what do they do" (synthesized overview)
```

```
SearchAPI MCP (backup):
- google_news_light → business/person name
```

### 1E: YouTube Deep Dive

If a YouTube channel exists:

```
Social Toolkit MCP:
- FetchYoutubeChannelVideosTool → channel (get video list)
- FetchYoutubeTranscriptTool → top 2-3 videos by views (understand what they talk about)
- FetchYoutubeCommentsTool → top video (understand audience reaction)
```

### 1F: CV / Resume Analysis

If a CV is provided (file path or pasted text):
- Read the file using the Read tool
- Extract: skills, experience, education, certifications, achievements, career narrative
- Identify expertise areas and years of experience
- Note any awards, publications, speaking engagements

### 1G: Competitor / Similar Business Research (Fallback)

**Trigger this step when:**
- The subject has very little web presence (few posts, no website, few reviews)
- The social profiles are sparse or recently created
- Not enough data was gathered in Steps 1A-1F to build a compelling page

**Goal:** Find 2-3 similar businesses that rank well, study their websites, and use their patterns as inspiration — while keeping the output professional and tailored to the subject's actual context.

**How to find competitors:**

1. Use `people_also_search_for` from the Google Maps results (Step 1C) — these are the closest competitors
2. Search Google for the business category + location:
   ```
   Social Toolkit MCP:
   - PerplexitySonarSearchTool → "best [business type] in [city]" or "[business category] near [location]"
   - GoogleForumsSearchTool → "[business type] [city] recommendations"
   ```
3. For each competitor found, scrape their website:
   ```
   Social Toolkit MCP:
   - FirecrawlScrapeTool → competitor website URL (get their homepage)
   ```

**Extract from competitors:**
- Page structure and section order (what sections do they include?)
- Services/offerings listed (use as inspiration for the subject's page)
- Tone of voice and copy patterns
- Color schemes and visual style
- CTAs and conversion patterns
- Trust signals they use (certifications, awards, "since 2005", etc.)

**How to use competitor data:**
- **DO**: Use the page structure, section patterns, and professional tone as a template
- **DO**: Adapt the mood and visual style to match what works in the industry
- **DO**: Include similar sections (e.g., if all competitors have a "Why Choose Us" section, include one)
- **DON'T**: Copy specific text or claims — everything must be about the actual subject
- **DON'T**: Use competitor branding, colors, or logos
- **DON'T**: Fabricate testimonials, awards, or stats the subject doesn't have
- **DO**: Be transparent with the user: "I didn't find much about [subject] online, so I studied similar businesses in the area to inform the design. Here's what I used as reference: [list competitors]"

**When writing copy with limited data:**
- Keep claims general but professional: "Quality service" instead of "Award-winning service"
- Focus on the basics that ARE known: location, hours, category, contact
- Use the aesthetic and tone of successful competitors as a guide
- Add placeholder sections the user can fill in: "[Your tagline here]", "Tell your story..."
- Make the page look established and professional even with minimal content — this IS the value

---

## Step 2: Analysis Phase — Think Like a Marketer

After gathering all data, perform a structured analysis. Write this analysis out explicitly before designing — it informs every design decision.

### 2A: Subject Profile

Synthesize a clear picture:
- **Who they are**: One paragraph summary
- **What they do**: Core offering/service/product
- **Where they operate**: Geography, market, niche
- **How long**: Maturity/experience level
- **Brand voice**: Formal/casual, playful/serious, bold/understated, technical/accessible
- **Content themes**: Top 3-5 recurring topics across all platforms
- **Visual identity**: Colors, imagery style, and aesthetic patterns from existing content

### 2B: Audience Analysis

Based on followers, engagement, review language, and content type:
- **Primary audience**: Demographics, interests, pain points
- **What they value**: What makes them follow/engage/buy
- **Language they use**: Slang, formality level, emotional triggers
- **Where they hang out**: Which platforms are strongest

### 2C: Competitive Advantages

Identify from the data:
- **Unique value prop**: What do they offer that others don't?
- **Social proof**: Ratings, testimonials, follower count, engagement
- **Authority signals**: Years in business, certifications, press mentions, expertise
- **Emotional hooks**: Community, exclusivity, safety, luxury, accessibility, rebellion
- **Content edge**: What type of content performs best for them

### 2D: SEO & Conversion Insights

- **Keywords**: Terms from their content, hashtags, and audience language
- **Search intent**: What would someone Google to find them?
- **Conversion goal**: What action should the landing page drive?
- **Trust barriers**: What objections might a visitor have? How does the data address them?

---

## Step 3: Design Direction

Based on the analysis, commit to a design direction. Don't ask the user to pick — **propose one based on the data** and let them override.

### Aesthetic Selection

Choose based on brand voice + audience:

| If the data suggests... | Choose... |
|---|---|
| Luxury, exclusivity, high-end | Dark theme, serif fonts, gold accents, editorial layout |
| Friendly, accessible, community | Light/warm theme, rounded fonts, soft colors, open layout |
| Technical, professional, B2B | Clean minimal, monospace accents, structured grid, muted palette |
| Bold, rebellious, youth | High contrast, oversized type, asymmetric layout, neon accents |
| Natural, organic, wellness | Earth tones, organic shapes, textured backgrounds, botanical imagery |
| Playful, creative, artistic | Vibrant colors, custom illustrations, dynamic layout, personality |

### Color Palette

Derive from:
1. Their existing brand colors (from website/social)
2. Their industry conventions
3. Their audience preferences
4. The emotional tone of their content

### Typography

Select 2 fonts — a display font and a body font — that match the aesthetic. Never use Inter, Roboto, Arial, or system fonts. Use Google Fonts.

### Content Structure

Based on conversion goal, structure the page:

**For service businesses:**
Hero → Problem/Solution → Services → Social Proof → About → CTA

**For personal brands / portfolios:**
Hero → About → Work/Projects → Testimonials → Contact

**For communities / clubs:**
Hero → Experience → Pillars/Values → Events → Location → CTA

**For products / e-commerce:**
Hero → Product Showcase → Features → Reviews → Pricing → CTA

**For professionals (CV-based):**
Hero → Expertise → Experience Timeline → Skills → Publications/Talks → Contact

---

## Step 4: Copy Generation

Write all copy in the subject's voice and the audience's language:

- **Hero headline**: Bold, specific, emotionally resonant. Not generic.
- **Hero subheadline**: Clarify what they do and for whom.
- **Section headlines**: Each tells a mini-story, not just labels.
- **Body copy**: Short paragraphs, conversational, benefit-driven.
- **CTAs**: Action-specific ("Solicitar Membresía", not "Click Here")
- **Social proof snippets**: Pull real quotes from reviews, format naturally.
- **Meta tags**: SEO-optimized title and description.

**Language**: Write in the same language the subject uses on their profiles. If mixed, default to the language most of their audience engages in.

---

## Step 5: Image Generation

Generate 3-5 images that match the aesthetic direction using available image generation tools.

**Check for `infsh` CLI availability** (from the `ai-image-generation` skill):
```bash
which infsh
```

If available, generate images using FLUX or Grok models (avoid Seedream for potentially sensitive content):

```bash
infsh app run falai/flux-dev-lora --input '{
  "prompt": "[aesthetic-matched prompt based on brand analysis]"
}'
```

**Image set to generate:**

| Image | Purpose | Aspect |
|-------|---------|--------|
| Hero background | Main visual impact, sets the mood | 16:9 or full-width |
| About/Feature visual | Supports the story section | 3:4 or 1:1 |
| Service/Pillar images (2-3) | One per key offering | 1:1 or 16:9 |
| CTA background (optional) | Atmospheric, subtle | 16:9 |

**Prompt engineering**: Base each prompt on the analysis — use the brand's visual style, color palette, and industry context. Never generate generic stock-photo-style images.

**If `infsh` is not available**, check for the Social Toolkit `HiggsfieldImageTool` as an alternative. If no image generation is available, create the page with CSS-only atmospheric effects (gradients, noise textures, shapes) and note which images the user should add later.

**Download all generated images** to the project directory alongside the HTML/React files.

---

## Step 6: Build the Landing Page

### Output Format Selection

Present the user with options based on their situation:

**Option A: Single HTML File** (recommended for beginners)
- Zero dependencies, open in any browser
- Best for: clients who need it NOW, non-technical users, quick prototypes
- Inline CSS + JS, Google Fonts via CDN
- Images referenced as local files in same directory
- Deploy with Wrangler — include `wrangler.jsonc` in the project folder:
  ```jsonc
  {
    "name": "<project-name>",
    "compatibility_date": "2025-04-01",
    "assets": {
      "directory": "./"
    }
  }
  ```
  Then: `cd <project-folder> && wrangler deploy`

**Option B: Vite + React SPA** (recommended for developers)
- `npm run build` → deploy with `wrangler deploy`
- Component-based, easy to modify
- Best for: developers, projects that will grow, custom domains
- Follow the standalone React guidelines from the `frontend-design` skill (includes `wrangler.jsonc` setup)

**Option C: Rails + Inertia Page** (recommended for SaaS integration)
- Generates directly into a Rails project structure
- Inertia page component + controller + route
- Best for: when the landing page is part of a larger Rails app
- Only available when inside a Rails+Inertia project (auto-detected)
- Follow the Rails+Inertia guidelines from the `frontend-design` skill

**Option D: Deployable HTML + Asset Bundle** (recommended for client handoff)
- Organized folder: `index.html` + `css/` + `images/` + `js/`
- README with deployment instructions
- Best for: freelancers, agency work, client deliverables
- Include `wrangler.jsonc` in the folder root:
  ```jsonc
  {
    "name": "<project-name>",
    "compatibility_date": "2025-04-01",
    "assets": {
      "directory": "./"
    }
  }
  ```
  Deploy: `cd <project-folder> && wrangler deploy`

**Auto-selection logic** (propose this, let user override):
- Inside a Rails+Inertia project → Option C
- User mentioned "client" or "freelance" → Option D
- User is technical / mentioned Vercel/Netlify/Cloudflare → Option B
- Default / beginner / "just make it work" → Option A

### Design Execution

Regardless of format, apply ALL guidelines from the `frontend-design` skill:
- Distinctive typography (never generic)
- Bold color palette derived from the research
- Atmospheric backgrounds and textures
- Scroll animations and micro-interactions
- Mobile-responsive
- Fast loading (optimize images, minimal JS)

### Map & Directions Integration

If Google Maps coordinates were obtained in Step 1C, include an interactive map section. Ask the user which option they prefer:

**Option 1: Google Maps Embed (recommended — free, no API key)**
```html
<iframe
  src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3000!2d{longitude}!3d{latitude}!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s{place_id}!2s{business_name}!5e0!3m2!1sen!4v1"
  width="100%" height="400" style="border:0;" allowfullscreen="" loading="lazy">
</iframe>
```

**Option 2: OpenStreetMap Embed (no Google dependency)**
```html
<iframe
  src="https://www.openstreetmap.org/export/embed.html?bbox={lng-0.005},{lat-0.005},{lng+0.005},{lat+0.005}&layer=mapnik&marker={latitude},{longitude}"
  width="100%" height="400" style="border:0;">
</iframe>
```

**Option 3: Static Map Image (fastest load, no iframe)**
- Generate a map screenshot or use a static map API
- Best for performance-critical pages

**Option 4: No map** (for online-only businesses, personal brands without a physical location)

**"How to Get There" section** — include alongside the map:
- Full formatted address
- A "Get Directions" button linking to Google Maps navigation:
  ```html
  <a href="https://www.google.com/maps/dir/?api=1&destination={latitude},{longitude}&destination_place_id={place_id}" target="_blank">
    Get Directions
  </a>
  ```
- Nearby landmarks or neighborhoods (if mentioned in reviews)
- Parking information (if found in Google Maps extensions)
- Public transit tips (if available from the data)

**Auto-selection logic:**
- Physical business with foot traffic (restaurant, store, club) → Option 1 + full "How to Get There"
- Professional office (agency, clinic, studio) → Option 1, minimal directions
- Online-only business → Option 4
- User requests minimal dependencies → Option 2

### Page Must Include

Every generated landing page must have:
- [ ] SEO meta tags (title, description, OG image, canonical)
- [ ] Mobile viewport meta tag
- [ ] Semantic HTML structure
- [ ] At least one clear CTA above the fold
- [ ] Social proof section (ratings, followers, testimonials)
- [ ] Contact/location information (if available)
- [ ] Map embed with directions (if physical location — see Map & Directions section)
- [ ] Footer with legal/disclaimer text (if applicable)
- [ ] Google Fonts loaded
- [ ] All images with alt text
- [ ] Favicon link (if generated)

---

## Step 7: Present the Result

After generating, provide:

1. **Research Summary**: Key findings about the subject (2-3 bullet points)
2. **Design Rationale**: Why you chose this aesthetic direction (1-2 sentences)
3. **The page**: Open it in browser (`open index.html`) or provide dev server instructions
4. **What's included**: List of files generated (HTML, images, CSS)
5. **Deployment instructions**: Based on the format chosen
6. **Suggested improvements**: Things that could be added with more data or budget (video, testimonials page, blog, etc.)

---

## Behavior Notes

- **Research thoroughly, don't rush to design.** The quality of the landing page depends entirely on understanding the subject. Spend time in Steps 1-2.
- **Be opinionated about design.** Don't ask the user to pick colors or fonts — derive them from the research and propose confidently. The user will push back if they disagree.
- **Write copy in context.** Every headline and paragraph should feel like it was written BY someone who deeply understands the business, not by a generic AI.
- **Use real data.** Pull actual numbers (4.9 stars, 3,235 followers), real quotes from reviews, actual business hours. Never invent testimonials.
- **Match the audience, not just the brand.** A luxury brand targeting Gen Z needs a different page than one targeting executives, even with the same brand colors.
- **Generate images that fit.** Every AI-generated image should feel like it belongs to this specific business. No generic stock vibes.
- **Handle multiple languages naturally.** If the business operates in Spanish, write in Spanish. Don't translate — write natively.
- **Respect disclaimers.** If the business includes legal disclaimers in their content (e.g., cannabis clubs, financial services), include appropriate disclaimers in the landing page footer.
- **Always show the research.** Before presenting the design, share a brief summary of what you found. This builds trust and lets the user correct any misunderstandings before you build.
