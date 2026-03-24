---
name: blog-research
description: Keyword research and blog topic suggestion tool. Use when user wants to find what to write about, needs keyword research, wants to identify ranking opportunities, or needs content strategy for a niche or region. Analyzes search volume, competition, and intent to suggest blog topics ranked by ranking potential.
---

# Blog Keyword Research & Topic Suggestion

Research high-ranking keyword opportunities and suggest blog topics with the best chance of ranking.

## Input

User will provide: **$ARGUMENTS**

This can be:
- A niche/industry (e.g., "digital marketing in Bahrain")
- A company context (e.g., "digital marketing agency targeting Dubai clients")
- A broad topic area (e.g., "web development services")

If no input is provided, ask the user for their niche, target audience, and target regions.

## Process

### Step 1: Understand the Business Context
Before researching, clarify:
- **What does the business do?** (services, products)
- **Who is the target audience?** (business owners, developers, marketers)
- **What regions/countries to target?** (important for geo-specific keywords)
- **What's the goal?** (leads, brand awareness, authority)

### Step 2: Keyword Research

Perform web searches to find:

#### A. High-Volume Keywords
Search for trending and high-volume keywords in the niche:
```
Search: "[niche] blog topics 2026"
Search: "most searched [niche] keywords"
Search: "[niche] in [target region] trends"
Search: "what [target audience] search for online"
Search: "[service] + [city/country]" keyword variations
```

#### B. Competitor Analysis
Find what's already ranking and identify gaps:
```
Search: "best [niche] blogs"
Search: "[competitor topic] site:medium.com OR site:hubspot.com"
Search: "[niche] [target region]" — check what ranks on page 1
```

#### C. Long-Tail Opportunities
Find specific, less competitive keywords:
```
Search: "[niche] for small business [region]"
Search: "how to [action] in [region]"
Search: "[service] cost in [region] 2026"
Search: "best [service] for [specific audience]"
```

#### D. People Also Ask / Question Keywords
Find question-based keywords (great for AEO/GEO):
```
Search: "[niche] questions people ask"
Search: "why [topic] is important for [audience]"
Search: "how to choose [service] in [region]"
```

### Step 3: Analyze & Score Keywords

For each keyword found, evaluate:

| Factor | What to Check | Why It Matters |
|--------|--------------|----------------|
| **Search Volume** | Is this searched often? | High volume = more traffic potential |
| **Competition** | How many quality articles exist? | Low competition = easier to rank |
| **Intent** | Informational, commercial, or transactional? | Commercial/transactional = leads |
| **Relevance** | Does it match the business? | Must align with services offered |
| **Regional Fit** | Is it searched in target regions? | Geo-targeting matters |

### Step 4: Generate Blog Topic Suggestions

Present findings as a ranked table:

```markdown
## Blog Topics Ranked by Ranking Potential

| Rank | Blog Title Suggestion | Primary Keyword | Search Intent | Competition | Ranking Chance | Why This Topic |
|------|----------------------|-----------------|---------------|-------------|----------------|----------------|
| 1 | ... | ... | Commercial | Low | High | ... |
| 2 | ... | ... | Informational | Medium | High | ... |
| ... | ... | ... | ... | ... | ... | ... |
```

### Step 5: Provide Actionable Recommendation

For the top 3 recommended topics, provide:

```markdown
### Recommendation #1: [Blog Title]
- **Primary Keyword:** [keyword]
- **Secondary Keywords:** [kw1], [kw2], [kw3]
- **Long-tail Keywords:** [lt1], [lt2]
- **Search Intent:** [Informational/Commercial/Transactional]
- **Target Region:** [Bahrain/Dubai/USA/Global]
- **Competition Level:** [Low/Medium/High]
- **Why this will rank:** [1-2 sentence reasoning]
- **Content angle:** [What unique perspective to take]
- **Suggested slug:** [url-friendly-slug]

Ready to write? Use: `/blog [topic]`
```

## Output Rules
- Always present at least 5 topic suggestions
- Rank by realistic ranking potential (prioritize low competition + high relevance)
- Include a mix of intents (some informational for traffic, some commercial for leads)
- For geo-targeted businesses, include location-specific keyword variations
- Be honest about competition — don't suggest keywords dominated by massive sites
- Prefer long-tail keywords for new/small blogs (easier to rank)
- If the blog/site is new, prioritize low-competition topics to build domain authority first

## Regional Keyword Tips
For geo-targeted content (e.g., Bahrain, Dubai, USA):
- Add city/country modifiers: "digital marketing in Bahrain"
- Use local terms: "GCC", "MENA region", "Gulf states"
- Consider bilingual search: some regions search in English + Arabic
- Check if the topic has regional search demand (not just global)
- "Near me" and "[service] in [city]" are high-intent commercial keywords
