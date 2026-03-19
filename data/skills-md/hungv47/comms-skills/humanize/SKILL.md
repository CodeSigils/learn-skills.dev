---
name: humanize
description: "This skill should be invoked when the user has existing text that sounds robotic, generic, or AI-generated and wants it to read like a human wrote it. Triggers include 'this sounds like AI', 'this reads like a template', 'make this more human', 'too robotic', 'tighten this up', 'make this shorter', 'edit this', 'fix my copy', 'polish this', 'too formal', 'too corporate', 'this doesn't sound like us', 'more conversational', or 'rewrite in our brand voice' -- even if they just paste text without comment and the issue is clearly AI tone, or say 'this won't pass AI detection.' Not for writing new content from scratch (use content-create) or rewriting full landing pages (use lp-optimization)."
argument-hint: "[content file or text]"
license: MIT
metadata:
  author: hungv47
  version: "1.0.1"
---

# Humanize & Compress

*Horizontal skill — strips AI patterns and compresses content so it reads like a human wrote it and an editor approved it.*

**Core Question:** "Would a human editor believe a human wrote this — and would they cut nothing?"

## Inputs Required
- Any content artifact (from `content-create`, `lp-optimization`, or any other skill) or raw text

## Output
- `.agents/mkt/content/[slug].humanized.md`

## Quality Gate
Before delivering, verify:
- [ ] Zero Hard Tell patterns from the 33-pattern checklist
- [ ] ≤2 Soft Tell patterns in the entire piece
- [ ] No clusters of 3+ high-frequency AI vocabulary words in any paragraph
- [ ] ≥15% word reduction from original
- [ ] No unique ideas, data, examples, or nuance removed (check against original)
- [ ] Read aloud — no stumbles, no robotic rhythm
- [ ] Every paragraph contains at least one concrete fact, number, or named example

## Chain Position
Horizontal — works on output from any skill. If content passed `copywriting`'s Seven-Sweeps, humanize focuses on compression + residual patterns. For external or AI-generated content, full 5-step process applies.
**Re-run triggers:** When brand voice adjectives change, when content-create output consistently triggers AI detection, or when voice injection guidance is updated.

### Skill Deference
- **Need new content written from scratch?** → Use `content-create` — this skill cleans existing content, not creates new.
- **Conversion optimization needed?** → Use `lp-optimization` — this skill focuses on voice and AI pattern removal, not conversion mechanics.
- **Content already passed copywriting's Seven-Sweeps?** → Focus on compression + residual AI patterns only — skip full audit if seven-sweeps already ran.

---

## Before Starting

### Step 0: Product Context
Check for `.agents/product-context.md`. If available, read for voice adjectives and brand personality. Voice injection (Step 3) requires these adjectives — without them, output will be clean but generic.
If `.agents/product-context.md`'s `date` field is older than 30 days, recommend re-running `icp-research` to refresh voice adjectives — brand voice evolves.

### Required Artifacts
None — can humanize any text standalone.

### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `product-context.md` | icp-research | Voice adjectives for personality injection |
| `icp-research.md` | icp-research | Audience register calibration |
| `content/[slug].md` | content-create | Original content with copywriting's seven-sweeps applied |

---

## Step 1: Audit

Scan the content for two categories of problems:

**AI Patterns** — Run through all 33 patterns in [references/ai-patterns.md](references/ai-patterns.md). Start with the high-frequency AI vocabulary scan, then work through each category. For each pattern found, log:
- Pattern number and name
- Exact text that triggered it
- Severity (Hard Tell / Soft Tell)

**Bloat** — Scan for:
- Redundant sentences (two sentences making the same point)
- Hedge stacking and unnecessary qualifiers
- Throat-clearing intros and setup paragraphs
- Paired synonyms and filler adverbs
- Bridge sentences that exist only to connect ideas
- Sections that don't pass the earn-your-place test

Produce an internal diagnosis — do not modify the content yet. The diagnosis informs Steps 2-4.

---

## Step 2: Strip

Surgical removal of AI tells and filler. **Only subtract — do not rewrite for style yet.**

For each flagged pattern from Step 1:
- Apply the specific fix from [references/ai-patterns.md](references/ai-patterns.md)
- Replace paired synonyms → pick the stronger word
- Fix copula avoidance → "serves as" becomes "is"
- Delete throat-clearing intros → start where the content actually begins
- Remove template transitions → let sections flow naturally or use a line break
- Cut hedge stacking → commit or cut the claim
- Delete -ing phrase tacking → remove "highlighting," "underscoring," "showcasing" appendages
- Replace vague attributions → name the source and date, or cut the claim
- Delete formulaic conclusions and generic positive endings → end with the strongest final thought
- Remove permission-seeking closers → end with a recommendation, not an offer
- Replace high-frequency AI vocabulary → plain-language equivalents (see vocabulary list)

**Rule:** Every edit in this step must be a subtraction or a substitution. No new sentences, no new ideas, no style changes.

---

## Step 3: Inject Soul

The content is now clean but potentially sterile. Apply voice using [references/voice-injection.md](references/voice-injection.md).

1. **Read voice adjectives** from `product-context.md` and apply the adjective framework constraints
2. **Vary sentence rhythm** — break the AI metronome. Mix short (4-6 words), medium (10-15), and long (18-25) sentences. Use the 1-3-1 pattern as a starting point
3. **Upgrade abstractions to specifics** — every "many companies" becomes a named company, every "significant improvement" becomes a number
4. **Break structural monotony** — not every paragraph should be 3 sentences, not every section needs a subheading, not every list needs to be bulleted
5. **Add experience markers** where brand voice allows — "we found," "our data shows," "teams tell us"

**Constraint:** Net word count from Step 2 must not increase. Every word added means a word removed elsewhere.

---

## Step 4: Compress

Systematic compression using [references/conciseness-rules.md](references/conciseness-rules.md). Work at three levels:

### Sentence Level
- Replace filler phrases using the compression table (14 substitutions)
- Eliminate filler adverbs ("really," "very," "significantly")
- Convert passive → active where it shortens the sentence

### Paragraph Level
- Apply the merge test: consecutive paragraphs making the same point → merge, keep the stronger example
- Apply the redundancy test: if the last sentence of a paragraph says the same thing as the first sentence of the next, delete one
- Eliminate setup paragraphs: if a paragraph exists only to introduce the next, cut it and let the next paragraph stand alone
- Inline evidence: merge "studies show X" + "for example, Y" into just "Y"

### Section Level
- Earn-your-place test: if deleting a section entirely loses nothing the reader needs, delete it
- Hierarchy compression: sections with one paragraph → merge into adjacent section
- List compression: lists with ≤3 items → convert to sentence

**Target:** 15-30% reduction from the original word count. Check content-type targets in [references/conciseness-rules.md](references/conciseness-rules.md) for specific guidance.

---

## Step 5: Final Audit

Re-scan the entire piece using a three-pass self-audit:

### Pass 1: Systematic check
1. **Pattern check** — Run all 33 patterns again. Steps 3-4 can reintroduce patterns (especially during voice injection when new sentences are written). Fix any that appear.
2. **Vocabulary check** — Scan for clusters of 3+ high-frequency AI words in any paragraph. Replace or restructure.
3. **Density check** — Every paragraph must contain at least one concrete fact, number, or named example. Paragraphs that are pure abstraction get cut or upgraded.
4. **Meaning preservation** — Compare against the original. Every unique idea, data point, example, and nuance from the original must still be present. If compression removed substance, restore it.
5. **Compression verification** — Calculate final word count vs. original. Must be ≥15% reduction. If not, return to Step 4.

### Pass 2: Introspection loop
After Pass 1, explicitly ask: **"What still makes this obviously AI-generated?"** Answer honestly — identify any remaining tells, even subtle ones not in the 33-pattern checklist. Then fix those tells and re-read. This catches emergent patterns that no checklist covers: the overall "feel" of AI writing that comes from multiple small signals combining.

6. **Cut quotables** — If any sentence sounds like it was designed to be pulled as a quote or shared on social media, rewrite it. AI generates sentences that sound profound in isolation but say nothing specific. "The best time to start was yesterday" is a quotable. "We lost 40% of signups in the first 48 hours" is a fact. Keep facts, kill quotables.

7. **Read-aloud test** — Read the final piece aloud. Mark any sentence where you stumble or where the rhythm feels mechanical. Fix those sentences. If nothing catches, move to Pass 3.

### Pass 3: Scoring rubric
Score the final piece on five dimensions, 1-10 each:

| Dimension | Question | 1 (worst) | 10 (best) |
|-----------|----------|-----------|-----------|
| Directness | Does the text state things or announce it will state things? | Every paragraph has a setup sentence | Every sentence carries information |
| Rhythm | Do three consecutive sentences match length? | Metronomic — all 12-15 words | Varied — short punches, long development, fragments |
| Trust | Does the text explain things the reader already knows? | Patronizing — defines basic terms | Respects the reader's existing knowledge |
| Authenticity | Would I know who wrote this without a byline? | Could be any brand, any author | Distinctive voice, specific perspective |
| Density | Can I delete any sentence without losing information? | 30%+ is filler | Every sentence earns its place |

**Threshold: 35/50.** Below 35 → return to Step 3 (voice injection) and re-apply with more specificity and personality. Above 35 → the piece is done.

---

## Artifact Template

```markdown
---
skill: humanize
version: 1
date: [today's date]
status: draft
compression: [X]%
---

# Humanized: [Original Title]

## Humanization Summary

| Metric | Value |
|--------|-------|
| Words (original) | [count] |
| Words (humanized) | [count] |
| Compression | [X]% |
| AI patterns found | [count] |
| AI patterns fixed | [count] |
| Hard Tells remaining | 0 |
| Soft Tells remaining | [0-2] |
| Quality score | [X]/50 (Di:[n] R:[n] T:[n] A:[n] De:[n]) |

## Change Log

| Location | Original | Change | Rule |
|----------|----------|--------|------|
| [para/section] | "[original text]" | "[new text]" or [deleted] | Pattern #[N] / Compression / Voice |

---

[Humanized content here]
```

> On re-run: rename existing artifact to `[slug].humanized.v[N].md` and create new with incremented version.

---

## Worked Example

### Original (AI-generated, 178 words)

> In today's rapidly evolving SaaS landscape, customer onboarding has become a critical and essential component of the user experience. Companies that invest in comprehensive onboarding programs see significantly better retention rates. For example, a well-designed onboarding flow can help users understand the full value of your platform more quickly and efficiently.
>
> It's important to note that onboarding isn't just about product tours. Effective onboarding encompasses email sequences, in-app guidance, and personalized support. By implementing these strategies, you can create a seamless and intuitive experience that drives long-term engagement.
>
> In conclusion, investing in onboarding is one of the best decisions a SaaS company can make. The data clearly shows that companies with strong onboarding see up to 50% higher retention. Start building your onboarding program today and see the difference it can make for your business!

### Humanized + Compressed (91 words)

> SaaS companies with structured onboarding retain 50% more users — yet most treat it as a product tour and stop there.
>
> Onboarding that works combines three things: triggered emails based on usage gaps, in-app guidance tied to the user's actual workflow (not a generic checklist), and human support when activation stalls. Intercom's onboarding rebuild in 2024 cut their time-to-value from 14 days to 3 by replacing their 12-step tour with two targeted nudges.
>
> The pattern: less coverage, more precision. Guide users to one aha-moment fast, then expand.

### Change Annotation

| Location | Original | Change | Rule |
|----------|----------|--------|------|
| Para 1, S1 | "In today's rapidly evolving SaaS landscape" | Deleted | Pattern #21 (throat-clearing intro) |
| Para 1, S1 | "critical and essential" | "critical" → restructured | Pattern #6 (paired synonyms) |
| Para 1, S1 | "has become a critical component of..." | Lead with the data point instead | Compression: setup elimination |
| Para 1, S3 | "more quickly and efficiently" | Deleted (paired synonyms + filler) | Pattern #6, Compression |
| Para 2, S1 | "It's important to note that" | Deleted | Pattern #8 (hedge) + Compression |
| Para 2, S2 | "a seamless and intuitive experience" | Restructured with specifics | Pattern #6 + AI vocabulary ("seamless") + Voice: specificity |
| Para 3, S1 | "In conclusion" | Deleted | Pattern #5 (formulaic structure) + #25 (generic positive conclusion) |
| Para 3, S3 | "Start building... see the difference!" | Replaced with actionable takeaway | Pattern #20 (permission-seeking) + Pattern #11 (exclamation) |
| Throughout | Generic claims | Added Intercom example | Voice: specificity as personality |
| — | 178 words → 91 words | **49% compression** | — |

---

## Anti-Patterns

**Mechanical pattern-matching without judgment** — Not every instance of a Soft Tell pattern needs fixing. A single em dash in a 1,000-word piece is fine. A single hedge before a genuinely uncertain claim is honest. Use the checklist as a detection tool, not a find-and-replace script.

**Sterile output** — Content that's been stripped of AI patterns but has no personality. If the output reads like a legal document, Step 3 (voice injection) was skipped or under-applied. Clean ≠ good.

**Surface compression** — Cutting depth instead of filler. Removing a data point to save 8 words is the opposite of what compression should do. Check every deletion against the depth preservation rules.

**Voice cosplay** — Injecting a personality that doesn't match the brand. A fintech compliance tool shouldn't sound like a DTC sneaker brand. Read the voice adjectives from product-context.md — they're constraints.

**Compression without reading the full piece first** — Starting to compress paragraph 1 before reading paragraph 12. The piece might make a point once clearly and once redundantly — you need to see both before deciding which to keep.

**One-pass editing** — Running all five steps simultaneously. Each step has a different focus: audit, strip, voice, compress, verify. Combining them produces worse results because you're optimizing for conflicting goals simultaneously.

**Destroying structure in the name of conciseness** — Removing all subheadings, merging all sections, eliminating all lists because "shorter is better." Structure aids scanning. Compress within structure before eliminating structure.

**Over-compressing introductions** — The opening carries disproportionate weight. A 50% compressed intro that loses its hook is worse than a 20% compressed intro that keeps it. Compress introductions last and most carefully.

**Ignoring audience register** — Compressing a developer blog post into marketing-speak, or making a white paper sound like a tweet thread. Compression preserves register — it removes filler within the existing tone, not across tones.

**Skipping the final audit** — Steps 3 and 4 frequently reintroduce AI patterns (especially during voice injection when new sentences are written). The final audit catches these. Skip it and you'll ship content with the same patterns you started with.

---

## Content Type Calibration

This skill's examples are marketing-focused, but it works on any content type. Adjust the intensity of each step by content type:

| Content Type | Strip Intensity | Voice Injection | Compression Target |
|-------------|----------------|-----------------|-------------------|
| Marketing copy | Full — all 33 patterns | Full — brand voice adjectives | 20-30% |
| Blog posts / thought leadership | Full | Moderate — author voice, not brand voice | 15-25% |
| Documentation / technical writing | Light — focus on clarity patterns only | Minimal — accuracy over personality | 10-15% |
| Internal communications | Moderate | Light — conversational, not branded | 15-20% |
| Academic / research | Light — remove only Hard Tells | None — maintain formal register | 5-10% |

**Key principle:** The further from marketing, the lighter the touch. Documentation that sounds like a blog post is worse than documentation with a few AI tells.

---

## References

| Reference | Use For |
|-----------|---------|
| [ai-patterns.md](references/ai-patterns.md) | 33 AI writing patterns + high-frequency vocabulary & phrase lists — detection, examples, fixes, severity |
| [conciseness-rules.md](references/conciseness-rules.md) | Compression techniques at sentence, paragraph, and section level |
| [voice-injection.md](references/voice-injection.md) | Voice adjective framework, rhythm, specificity, personality injection |
