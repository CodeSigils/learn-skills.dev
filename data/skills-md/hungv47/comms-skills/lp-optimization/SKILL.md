---
name: lp-optimization
description: "This skill should be invoked when the user mentions a landing page, homepage, signup page, pricing page, checkout page, or any single page that needs to convert visitors. Triggers include 'my page isn't converting', 'nobody is signing up', 'people visit but don't buy', 'high bounce rate', 'review my landing page', 'review my homepage', 'optimize for conversion', 'is my conversion rate good', 'CTA isn't working', or 'people click our ads but then leave' -- even if they just share a URL and ask 'what's wrong with this' or say 'our ads are sending traffic but we're not converting.' Not for A/B testing page variants (use experiment), writing net-new marketing content (use content-create), full site SEO audits (use seo), or multi-step in-app flows (use user-flow)."
argument-hint: "[url or description]"
license: MIT
metadata:
  author: hungv47
  version: "2.2.1"
---

# Landing Page Conversion Optimization

*Horizontal skill — optimizes the conversion layer where communication meets action.*

**Core Question:** "What's stopping visitors from converting?"

## Philosophy

The frameworks here (PAS, 4-U, social proof hierarchy) are evidence-backed defaults. They work in most situations. But landing pages serve different audiences, traffic sources, and goals. When your data or testing reveals a different optimal approach, follow the data. The principles matter more than the specific numbers.

## Inputs Required
- Landing page URL or description of the page
- ICP research from `.agents/mkt/icp-research.md` (recommended — VoC language strengthens copy)
- Traffic source context (where visitors come from)

## Output
- Optimization recommendations with specific copy/structure changes
- For new pages: complete page structure with copy

## Quality Gate
Before delivering, verify:
- [ ] Headline scores ≥3 out of 4 on the U's (Useful, Unique, Urgent, Ultra-specific)
- [ ] Message matches the traffic source (headline echoes the ad/link that brought them)
- [ ] One primary CTA per page (secondary CTAs don't compete)
- [ ] Trust signals appear within scroll-distance of every CTA
- [ ] Form has ≤5 fields (or justified why more are needed)
- [ ] Social proof is from the last 12 months (older proof replaced or removed)
- [ ] Every audit finding includes: what was observed, which principle it violates, and a specific recommended fix

## Chain Position
Horizontal — works with `icp-research` (audience data), `content-create` (content assets), `copywriting` (copy craft), `experiment` (test design)
**Re-run triggers:** After major page redesigns, when conversion drops >10%, when traffic source mix changes significantly, or quarterly.

### Skill Deference
- **Need to write copy from scratch (not optimize existing)?** → Use `content-create` — this skill optimizes existing pages, not blank-page writing.
- **Need craft-quality headline rewrites or CTA copy?** → Run `copywriting` for variation workflow and evaluation rubric.
- **AI pattern cleanup needed?** → Use `humanize` — this skill focuses on conversion mechanics, not voice/pattern editing.

---

## Before Starting

### Step 0: Product Context
Check for `.agents/product-context.md`. If available, read for product details and accuracy. If missing, strongly recommend running `icp-research` first — this skill works without it but produces significantly better output with it.
If `.agents/product-context.md` or `.agents/mkt/icp-research.md` `date` fields are older than 30 days, recommend re-running `icp-research` — stale VoC data weakens copy recommendations.

### Required Artifacts
None — can audit any page standalone.

### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `icp-research.md` | icp-research | VoC data for persuasion |
| `product-context.md` | icp-research | Product details for accuracy |
| `experiment-*.md` | experiment | Test design context |

---

## Core Frameworks

### 4-U Headline Formula

| U | Question | Scoring |
|---|---------|---------|
| **Useful** | Does it communicate clear value? | Y/N |
| **Unique** | Could a competitor use this headline? | Y/N (N = good) |
| **Urgent** | Is there a reason to act now? | Y/N |
| **Ultra-specific** | Does it include a number or concrete outcome? | Y/N |

80% of visitors won't read past the headline. Generate 10+ variations, score each.

### PAS Copy Framework

1. **Problem**: Lead with pain in the audience's own language. If `.agents/mkt/icp-research.md` exists, use VoC quotes directly.
2. **Agitate**: What happens if they don't solve this? Make consequences vivid.
3. **Solve**: Your product as the relief. Benefits, not features.

### Message Match

Check: does the landing page headline echo the exact promise from the ad/email/link? Broken promise = instant bounce.

**Message match verification method:**
1. **Analytics first:** Check GA4 → Acquisition → Traffic Source → filter by landing page. Identify top 3 traffic sources.
2. **Paid sources:** Log into the ads platform (Google Ads, Meta, LinkedIn) → find active ads pointing to this page → check if ad headline matches landing page headline.
3. **Organic sources:** Search the page's target keywords → check if the meta title/description that appears in search results matches the page headline.
4. **Email/referral:** Check the email or referring link copy that drives traffic → verify the promise matches.
5. **Document mismatches:** For each source, note: [source headline/promise] vs. [landing page headline] → match or mismatch.

Don't rely on `site:` searches alone — paid ads aren't indexed by Google, and many traffic sources are invisible to search.

### First-Person CTA

"Get MY guide" > "Get YOUR guide" (90% more clicks). Formula: `[Action Verb] + [What They Get]`

---

## Quick Reference

### Social Proof Hierarchy (most → least powerful)
1. Testimonials with specific results ("Increased revenue 40% in 3 months")
2. Case studies with before/after numbers
3. Customer count ("Join 10,000+ teams")
4. Media mentions / press logos
5. Expert endorsements
6. Customer logos

**Recency multiplier** — within each tier, recent proof outperforms old proof:

| Age | Multiplier | Action |
|-----|-----------|--------|
| <3 months | 100% | Use prominently |
| 3-6 months | 80% | Use — still credible |
| 6-12 months | 60% | Use if nothing fresher available |
| >12 months | 40% | Replace — signals stagnation to visitors |

A 6-month-old testimonial with results beats a 2-year-old case study, even though case studies rank higher in the hierarchy. Prioritize freshness when you have multiple options per tier.

Context-dependent. Fast-moving industries (AI, crypto): 6-month-old proof already feels dated. Stable industries (manufacturing, legal): 18-month case studies still carry weight. Principle: proof should reflect a reality your visitors recognize.

### Cognitive Bias Stack

| Bias | How to Apply |
|------|-------------|
| Loss aversion | "Don't miss..." / limited genuine availability |
| Social proof | Testimonials near CTAs, user counts |
| Anchoring | Show higher price first, then actual price |
| Reciprocity | Give free value before asking (lead magnet, calculator) |
| Authority | Expert quotes, certification badges, press logos |

### Form Rules
- Limit to 5 fields — every additional field costs ~10% conversions (evidence-backed default from Unbounce/HubSpot research). Exceptions: high-intent enterprise traffic may tolerate 7-8 fields. If your completion rate is >60% with more fields, the default doesn't apply. Principle: only ask for what you need right now.
- Start with just email. Use progressive profiling for the rest
- Each field justifies its existence — if it can be asked later, ask later

### Trust Signals
Cluster near CTAs and forms: security badges, money-back guarantee, privacy link, contact info.

---

## Testing Priority

Test in this order (highest impact first):
1. Headlines (biggest swing)
2. Offers (what you're promising)
3. CTAs (text, color, placement)
4. Page layout
5. Form fields

Use `experiment` for proper test design with success/kill thresholds and sample size validation.

---

## Workflows

### New Landing Page
1. Read ICP research (if available) for VoC language and pain points
2. Define primary conversion goal (one per page)
3. Generate 10+ headline variations using 4-U formula
4. Structure body with PAS framework
5. Add social proof (strongest above fold)
6. Design form (minimal fields)
7. Place trust signals near every CTA
8. Verify message match with traffic source
9. Run through quality gate checklist

### Optimization Audit
1. Check message match between traffic sources and headline
2. Score headline against 4-U formula
3. Audit social proof: placement, specificity, relevance
4. Count form fields — can any be removed?
5. Check mobile experience (thumb zone CTAs, load time)
6. Identify highest-impact fix
7. Design A/B test via `experiment`

Audit findings without evidence are opinions — they don't give the team enough to act on. Every finding must include:
1. **What was observed** — specific text, element, or metric on the page
2. **Which principle it violates** — name the framework (4-U, message match, social proof hierarchy, etc.)
3. **Recommended fix** — exact replacement text, not "improve the headline"

---

## Artifact Template

When saving optimization artifacts, use this frontmatter:

```yaml
---
skill: lp-optimization
version: 1
date: [today's date]
status: draft
---
```

> On re-run: rename existing artifact to `[name].v[N].md` and create new with incremented version.

---

## Worked Example

```markdown
---
skill: lp-optimization
version: 1
date: 2026-03-17
status: draft
---

# LP Audit — Acme Analytics Free Trial Page

## Headline Assessment

Current: "The Best Analytics Platform for Modern Teams"
4-U Score: 1/4 (Useful only — not Unique, not Urgent, not Ultra-specific)

Recommended: "See every metric your team tracks — one screen, updated every 5 minutes."
4-U Score: 4/4

## Message Match
Traffic source: Google Ads — "real-time analytics dashboard"
Current headline mentions neither "real-time" nor "dashboard" → broken match.
Fix: Echo "real-time dashboard" in headline.

## Social Proof Audit
- No testimonials above fold → add strongest result quote near hero CTA
- Customer logos present but below fold → move 3 logos above fold

## Form Audit
Current: 7 fields (name, email, company, role, size, phone, referral source)
Recommended: 3 fields (name, email, company) — collect rest via progressive profiling after signup
Expected impact: ~40% form completion improvement

## Priority Action Items
| # | Fix | Expected Impact | Effort |
|---|-----|----------------|--------|
| 1 | Rewrite headline for message match | High | Low |
| 2 | Cut form to 3 fields | High | Low |
| 3 | Move testimonial above fold | Medium | Low |
| 4 | A/B test headline variants via `experiment` | High | Medium |
```

---

## Anti-Patterns

**Redesign without diagnosis** — jumping to "make it look better" without identifying what's actually blocking conversion. Diagnose before prescribing.

**Testing design before copy** — A/B testing button colors or layouts when the headline doesn't pass the 4-U test. Copy is responsible for 80%+ of conversion impact — fix the words before the visuals.

**Ignoring mobile experience** — Optimizing for desktop when 60%+ of traffic is mobile. Check thumb zone placement for CTAs, ensure forms are completable one-handed, and verify load time on mobile networks.

**Social proof without specificity** — "Trusted by thousands of companies" is weaker than "Used by 3,247 teams including Stripe and Notion." Generic social proof triggers skepticism, not trust.

**Multiple competing CTAs** — Primary CTA, secondary CTA, sidebar CTA, and exit-intent popup all fighting for attention. One primary CTA per page — secondary CTAs must not visually compete.

---

## References

| Reference | Use For |
|-----------|---------|
| [core-principles.md](references/core-principles.md) | Headlines, value props, CTAs, forms, message match, PAS |
| [social-proof-trust.md](references/social-proof-trust.md) | Social proof hierarchy, biases, trust signals |
| [ux-design.md](references/ux-design.md) | Visual hierarchy, mobile optimization |
| [advanced-psychology.md](references/advanced-psychology.md) | Headline formulas, close sequences, pricing, urgency |
| [testing-optimization.md](references/testing-optimization.md) | A/B testing, tracking |
| [implementation-checklist.md](references/implementation-checklist.md) | Pre-launch checklists |

**Sources:** [CopyHackers](https://copyhackers.com), [CXL](https://cxl.com), [Unbounce](https://unbounce.com/landing-page-articles/)
