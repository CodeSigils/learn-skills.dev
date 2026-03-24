---
name: blog
description: Generate fully SEO/AEO/GEO optimized technical blog posts. Use when user asks to write a blog, create content, or generate articles. Covers on-page SEO, answer engine optimization, generative engine optimization, programmatic SEO, and off-page SEO in every blog.
---

# SEO-Optimized Technical Blog Generator

Generate a production-ready, fully SEO/AEO/GEO optimized technical blog post.

## Input

User will provide: **$ARGUMENTS**

This can be:
- A blog topic (e.g., "web application security best practices")
- A keyword from research (e.g., "digital marketing services in Bahrain")
- A full brief with keywords (e.g., "topic: X, primary keyword: Y, target: Z")

If no topic is provided, ask the user for a blog topic. If the topic seems broad, suggest running `/blog-research` first.

## Process

### Step 1: Keyword Research (GEO + SEO)

**If user provides keywords from `/blog-research`:** Use those directly, skip to Step 2.

**If user provides only a topic:** Do quick keyword research:
- Web search: "[topic] 2026 keywords", "[topic] people also ask"
- Web search: "[topic] trending subtopics"
- Identify: 1 primary keyword, 3-5 secondary keywords, 2-3 long-tail keywords
- Check what's currently ranking and what AI engines (ChatGPT, Perplexity, Google AI Overview) cite for this topic
- If a target region is mentioned, add geo-modifiers to keywords

**Present keyword plan to user before writing:**
```
Primary Keyword: [keyword]
Secondary Keywords: [kw1], [kw2], [kw3]
Long-tail: [lt1], [lt2]
Search Intent: [Informational/Commercial/Transactional]
Target Region: [if applicable]
Proceed with writing? (Y/n)
```

### Step 2: Content Directory Detection

Check the project for where blogs are stored:
- Look for `content/blogs/`, `src/content/`, `blog/`, `posts/` directories
- Match the existing frontmatter format of other blog files
- If no blog directory exists, ask the user where to save

### Step 3: Write the Blog Post

Create a markdown file with this exact structure:

#### Frontmatter (Programmatic SEO)
```yaml
---
title: "[Primary Keyword near start] — [Compelling hook under 60 chars]"
description: "[Under 160 chars, includes primary keyword, creates curiosity]"
date: "[YYYY-MM-DD]"
image: "/blogs/[slug].jpg"
tags: ["Tag1", "Tag2", "Tag3", "Tag4", "Tag5", "Tag6"]
---
```
Note: Match frontmatter fields to existing blogs in the project. Some projects use `category`, `author`, `draft`, `slug` etc.

#### Content Structure

**1. TL;DR (AEO)**
- 2-3 sentence direct answer to the topic
- Include 1 key statistic with source
- This is what AI engines will extract — make it citation-worthy

**2. Introduction / What is [Topic]?**
- Clear definition in first sentence (featured snippet bait)
- Why it matters — real statistic with citation ("According to [Source], ...")
- Image reference: `![Alt text with keyword](/blogs/[slug].jpg)`

**3. Core Sections (3-5 sections with H2 headings)**
Each section must include:
- H2 heading with a secondary keyword
- Opening sentence that directly answers "what is this" (AEO)
- A table OR code block OR comparison (linkable asset for off-page SEO)
- At least 1 statistic with source attribution (GEO — AI engines cite sourced claims)
- Practical example or code snippet where relevant
- Use H3 subsections to break down complex topics

**4. Practical Section**
- Real-world workflow, implementation guide, or "how to get started" steps
- Code examples with comments (TypeScript/JavaScript preferred for tech blogs)
- Before/after comparisons where applicable
- For non-tech/marketing blogs: step-by-step guides, checklists, templates

**5. Trade-offs / When to Use What**
- Honest comparison (builds E-E-A-T trust signals)
- Table format preferred (featured snippet + linkable asset)

**6. FAQ Section (SEO Rich Snippets + AEO)**
- 4-5 questions in `### Question?` format
- Each answer: 2-4 sentences, direct, starts with the answer (not "Well..." or "It depends...")
- Include questions people actually search for (use "People Also Ask" patterns)
- For geo-targeted blogs, include region-specific questions

**7. Resources Section (GEO + Off-page SEO)**
- 5-6 real, authoritative links (official docs, research papers, reputable blogs)
- Use format: `[Descriptive Anchor Text](URL)`
- Prefer: official documentation, GitHub repos, research from known companies

### Step 4: SEO Checklist (verify before saving)
- [ ] Primary keyword in: title, description, H1, first paragraph, 1-2 H2s
- [ ] Secondary keywords distributed across H2/H3 headings
- [ ] At least 3 tables (comparison, checklist, feature matrix)
- [ ] At least 2 code blocks OR detailed examples
- [ ] At least 5 statistics with source citations
- [ ] FAQ section with 4+ questions
- [ ] Resources section with 5+ authoritative links
- [ ] TL;DR at the top (AI engine extraction)
- [ ] "According to [Source]" pattern used 3+ times (GEO)
- [ ] All images have descriptive alt text with keywords
- [ ] Frontmatter complete and matches project format
- [ ] File saved with kebab-case slug
- [ ] Title under 60 characters, description under 160 characters
- [ ] If geo-targeted: location keywords in title/headings/content

### Step 5: Internal Linking (if existing blogs found)
- Check other blog files in the project
- Add 1-2 internal links to related existing posts where natural
- Suggest which existing posts should link back to this new post

## Writing Rules
- Language: English (unless user specifies otherwise)
- Tone: Professional but easy to understand (a beginner should get it)
- No fluff, no filler — every sentence adds value
- Use "you" to address the reader directly
- Bold key terms on first use
- Keep paragraphs short (3-4 sentences max)
- Total length: 1500-2500 words (optimal for SEO)

## Geo-Targeted Blog Rules (for regional businesses)
When writing for a specific region (e.g., Bahrain, Dubai, USA):
- Include city/country in title and at least 2 headings
- Reference local market conditions, regulations, or trends
- Use local business examples where possible
- Include region-specific statistics
- Add "in [Region]" to FAQ questions
- Consider local search intent (may differ from global)

## SEO Optimization Summary

| Type | What It Covers | How This Blog Does It |
|------|---------------|----------------------|
| **SEO** | Google ranking | Keywords in title/headings, meta description, heading hierarchy, internal links |
| **AEO** | Answer engines, featured snippets | TL;DR, FAQ section, direct definitions, concise answers |
| **GEO** | AI search (ChatGPT, Perplexity, Gemini) | Cited statistics, "According to" patterns, authoritative sources |
| **Programmatic SEO** | Scalable content structure | Consistent frontmatter, tags, structured format, slug pattern |
| **Off-page SEO** | Linkability and shareability | Tables, comparisons, quotable stats, resource links to authority sites |
