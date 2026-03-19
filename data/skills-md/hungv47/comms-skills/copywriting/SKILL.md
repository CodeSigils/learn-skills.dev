---
name: copywriting
description: "This skill should be invoked when the user needs persuasive copy — headlines, hooks, CTAs, taglines, subject lines, or full-page section-by-section copy with annotations and alternatives. Triggers include 'write headlines', 'evaluate this copy', 'is this headline good', 'write landing page copy', 'section-by-section copy', 'annotate the copy', 'variation workflow', 'headline formulas', 'copy evaluation', 'three-question test', 'swap test', or when another skill needs key lines written with craft rigor. Not for choosing content formats or platforms (use content-create), editing existing text for AI patterns (use humanize), or diagnosing landing page conversion issues (use lp-optimization)."
argument-hint: "[copy task or text to evaluate]"
license: MIT
metadata:
  author: hungv47
  version: "1.0.0"
---

# Copywriting

*Horizontal skill — produces craft-quality copy with annotations, alternatives, and quantitative evaluation.*

**Core Question:** "Is every key line visual, falsifiable, and uniquely ours?"

## Philosophy

The copy frameworks (PAS, 3-Question Test, CTA formula) are proven tools — not mandatory templates. A skilled writer may combine frameworks, or write a hook that breaks the 8-word guideline because the extra words earn their place. The test is: does this stop the scroll and move the reader? Frameworks get you there faster. They don't define the only path.

## Inputs Required
- Brief: what to write (headline, hook, CTA, tagline, subject line, or full-page copy)
- Context: audience, product, awareness stage (from `.agents/mkt/icp-research.md`, `.agents/product-context.md`, or user-provided)

## Output
- Inline annotations + alternatives on key lines (when called by another skill)
- `.agents/mkt/content/[slug].copy.md` (for standalone full-page copy tasks)

## Quality Gate
Before delivering, verify:
- [ ] Every key line passes the Three-Question Test: visual? falsifiable? uniquely ours?
- [ ] Rubric score averages ≥3.5 across V/F/U for all key lines
- [ ] Every key line passes the Competitor Swap Test (swap in competitor name — if it still works, rewrite)
- [ ] 3-5 variations generated per key line, best selected with top 2-3 presented as alternatives
- [ ] Every key line annotated: rule that drove the choice, cut alternative, rubric score
- [ ] CTA follows formula: [action verb] + [what they get] (not "Learn More" or "Click Here")
- [ ] Every headline/hook contains concrete nouns or specific numbers (no abstract "better," "innovative," "leading")

## Chain Position
Horizontal — called by `content-create`, `lp-optimization`, `imc-plan`. Can run standalone.
**Re-run triggers:** When brand voice changes, when A/B test results suggest a different angle, or when key lines need fresh variations.

### Skill Deference
- **Need a full content asset (carousel, thread, email, video)?** → Use `content-create` — this skill writes key lines and page copy, not format-specific assets.
- **Content reads as AI-generated?** → Run `humanize` after — it strips AI patterns and compresses.
- **Diagnosing a live page's conversion problem?** → Use `lp-optimization` — this skill writes copy, not diagnoses.
- **Optimizing for search/AI citations?** → Coordinate with `seo` for keyword targeting and content structure.

---

## Before Starting

### Step 0: Product Context
Check for `.agents/product-context.md`. If available, read for product details, voice adjectives, and accuracy.
If `.agents/product-context.md` or `.agents/mkt/icp-research.md` `date` fields are older than 30 days, recommend re-running upstream skills before proceeding — stale data produces misaligned copy.

### Required Artifacts
None — can write copy standalone with a user-provided brief.

### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `icp-research.md` | icp-research | VoC language for copy |
| `product-context.md` | icp-research | Product details, voice adjectives |
| `imc-plan.md` | imc-plan | Angle, awareness stage, channel context |

---

## Step 1: Pre-Writing Framework

Before writing any key line, answer:
1. **Who am I talking to?** What do they currently believe? What language do they use?
2. **What should they believe after reading this?** What's the one shift?
3. **What can I say that nobody else can?** What's our unique proof?
4. **Where is the traffic coming from?** (Ad, search, email, social, direct) — this determines what they already know and expect.

If `.agents/mkt/icp-research.md` exists, pull VoC quotes and pain language. Write how the buyer talks, not how the brand talks.

---

## Step 2: Three-Question Test

Run every key sentence through this filter:

1. **Visual?** Close eyes — can the reader see it? ("Couch to 5K" = yes. "Regain fitness" = no.)
2. **Falsifiable?** Is it true or false? ("6'2, reads on the tube" = yes. "Funny, smart, good values" = no.)
3. **Uniquely yours?** Could a competitor sign this? ("The dating app designed to be deleted" = only Hinge. "The best platform" = anyone.)

Three yeses = keep. Any no = rewrite.

---

## Step 3: Variation Workflow

Never deliver the first version of a key line. For every hook, headline, CTA, tagline, and subject line:

1. Write 3-5 variations using different approaches
2. Run each through the Three-Question Test
3. Apply the Speed Test (show for 2 seconds — understood?)
4. Run the Competitor Swap Test (replace brand with competitor — still works? → cut it)
5. Score survivors using the Evaluation Rubric (Step 4)
6. Keep the highest-scoring version. Present top 2-3 as alternatives with annotations.

**When 2+ variations tie on the 3Q test**, apply secondary criteria:

| Tiebreaker | Question | Higher Score Wins |
|-----------|---------|-------------------|
| **Surprise** | Which was least obvious / most unexpected? | Surprising hooks stop the scroll |
| **ICP anchor** | Which maps to a specific metric or pain from ICP research? | Grounded hooks convert better |
| **Objection-free** | Which triggers zero obvious objections? | Clean hooks have less falloff |

Document which tiebreaker you used — this trains judgment for future content.

Key lines = hooks, headlines, CTAs, taglines, subject lines. Body copy doesn't need 5 variations — but key lines always do.

---

## Step 4: Evaluation Rubric

Upgrade the binary Three-Question Test to quantitative scoring for final polish. Use on key lines after the Variation Workflow.

| Dimension | 1 (Weak) | 3 (Adequate) | 5 (Strong) |
|---|---|---|---|
| **Visual Clarity** | Pure abstraction, no image | Reader gets a vague picture | Reader pictures it instantly |
| **Falsifiability** | Subjective claim anyone makes | Mix of vague and concrete | Concrete, verifiable statement |
| **Competitive Uniqueness** | Any competitor could sign it | Somewhat specific to us | Only we could say this |

**Threshold:** Key lines must average ≥3.5 across all three. Below 3 on ANY dimension → rewrite targeting that specific dimension.

**Relationship to Three-Question Test:** The 3Q test is a quick pass/fail gate during drafting. The rubric is a precision tool for final polish — same dimensions, finer resolution.

---

## Step 5: Seven Sweeps

Apply the structured 7-pass editing method to all copy. Each pass focuses on exactly one dimension. The sequence matters — edit in this order. See [references/seven-sweeps.md](references/seven-sweeps.md) for the full checklist.

1. **Clarity** — Can every sentence be understood on first read?
2. **Voice & Tone** — Does it sound like the brand, consistently?
3. **So What?** — Every claim must answer "why should I care?"
4. **Prove It** — Every assertion needs evidence.
5. **Specificity** — Replace every abstraction with a concrete detail.
6. **Heightened Emotion** — Make the reader feel something.
7. **Zero Risk** — Remove every barrier to the desired action.

Key lines (hooks, headlines, CTAs, taglines, subject lines) always get the full seven sweeps. Body copy gets the quick-pass rules (see reference).

---

## Step 6: Annotation & Delivery

When delivering copy, annotate each key line with:
- **Which rule drove the choice** (Visual? Falsifiable? Conflict? Fact-over-adjective?)
- **What alternative was considered** and why it was cut
- **Rubric score** if the line went through evaluation

Format:
```
**Headline:** "12 hours/week back from status updates nobody reads."
  Rule: Visual + Falsifiable. Score: V:5 F:5 U:4.
  Cut alternative: "Stop wasting time on updates" — failed uniqueness (any tool could say this).
```

### Full-Page Copy Organization

When writing full-page copy, organize output section-by-section with 2-3 alternatives per key section:

1. **Hero** — headline + subheadline + CTA (3 variations)
2. **Social Proof** — logo bar, stat, or testimonial snippet
3. **Problem** — articulate their pain (2 variations)
4. **Solution** — bridge to your product
5. **How It Works** — 3-4 numbered steps
6. **Testimonials** — selected per criteria in [references/page-sections.md](references/page-sections.md)
7. **Final CTA** — recap + CTA (2 variations)

For each section with alternatives, annotate which rule each version leans on and its rubric score.

### Page-Specific Guidance

| Page | Key Principle |
|------|--------------|
| **Homepage** | What you do in one sentence. Primary use case, not every feature. |
| **Landing Page** | One goal, one CTA. Match headline to traffic source. Remove nav. |
| **Pricing** | Lead with value, not price. Anchor with most popular plan. |
| **Feature** | Lead with outcome ("Track time in one click"), not feature name. |
| **About** | Founding story. What you believe. Team photos + real context. |

---

## Artifact Template

```markdown
---
skill: copywriting
version: 1
date: [today's date]
status: draft
---

# Copy: [Title / Brief Description]

**Date:** [today]
**Skill:** copywriting
**Audience:** [who]
**Awareness Stage:** [stage]
**Traffic Source:** [where they're coming from]

## Pre-Writing

1. **Talking to:** [audience + current belief]
2. **Shift to:** [desired belief after reading]
3. **Only we can say:** [unique proof/angle]
4. **Traffic context:** [what they already know]

## Key Lines

### [Line Type: Headline / Hook / CTA / Tagline / Subject Line]

**Selected:** "[winning line]"
  Rule: [which principle]. Score: V:[n] F:[n] U:[n].
  Cut alternative: "[runner-up]" — [why cut].

**Alternative A:** "[second option]"
  Rule: [principle]. Score: V:[n] F:[n] U:[n].

**Alternative B:** "[third option]"
  Rule: [principle]. Score: V:[n] F:[n] U:[n].

## [Additional sections for full-page copy — Hero, Problem, Solution, etc.]

> On re-run: rename existing artifact to `[slug].copy.v[N].md` and create new with incremented version.
```

---

## Worked Example

```markdown
# Copy: Status Update Waste — Headlines & Hook

**Date:** 2026-03-19
**Skill:** copywriting
**Audience:** Engineering managers at 50-200 person companies
**Awareness Stage:** Problem Aware
**Traffic Source:** LinkedIn organic (cold audience)

## Pre-Writing

1. **Talking to:** Engineering managers who feel buried in status overhead but think it's just part of managing.
2. **Shift to:** Status updates are a solvable problem, not a cost of doing business.
3. **Only we can say:** We have internal data showing 12 hrs/week lost to status theater — no competitor has this stat.
4. **Traffic context:** LinkedIn feed scroll. They haven't searched for anything. Hook must interrupt.

## Key Lines

### Hook

**Selected:** "Your team loses 12 hours a week to status updates nobody reads."
  Rule: Visual (status updates, 12 hours) + Falsifiable (12 is specific, checkable). Score: V:5 F:5 U:4.
  Cut alternative: "Stop doing standups" — failed falsifiability (opinion, not fact).

**Alternative A:** "I cut meetings 80%. Output doubled."
  Rule: Falsifiable (80%, doubled) + Story hook. Score: V:4 F:5 U:3.

**Alternative B:** "31 hours/month in unproductive meetings — here's the breakdown."
  Rule: Falsifiable (31 hours) + Data hook. Score: V:4 F:5 U:3.

### CTA

**Selected:** "See how teams ship without status theater →"
  Rule: Outcome-focused (ship), specific (status theater). Score: V:4 F:4 U:4.
  Cut alternative: "Learn more about our product" — generic, fails all three tests.

**Alternative A:** "Watch the 2-minute demo →"
  Rule: Specificity (2-minute), low commitment. Score: V:3 F:4 U:2.
```

---

## Copy Principles — Extended Reference

### Make It Visual (Zoom-In Technique)

Abstract words evaporate. Concrete words stick.

**The technique:** Start abstract → ask "what do I actually mean?" → keep zooming until you reach something physical, picturable, droppable-on-your-foot.

| Start (abstract) | Zoom 1 | Zoom 2 (concrete) |
|---|---|---|
| "Regain fitness" | "Run again" | "Couch to 5K" |
| "Improve productivity" | "Save time on updates" | "12 hours/week back from status updates nobody reads" |
| "Better collaboration" | "Fewer meetings" | "Ship without a single standup" |

**Test:** If someone can close their eyes and picture it, it's concrete enough.

### Make It Falsifiable (The Pointing Technique)

"Don't talk, only point." — Direct the reader's eye to evidence.

| Unfalsifiable (opinion) | Falsifiable (checkable) |
|---|---|
| "The best analytics tool" | "See every metric on one screen, updated every 5 minutes" |
| "Fast customer support" | "Average response time: 4 minutes" |
| "Innovative solution" | "First CRM that auto-updates from email signatures" |

### Make It Yours Alone (The Swap Test)

"Never write an ad a competitor can sign." — Jim Durfee

1. Write your headline/claim
2. Replace your brand name with your top competitor's
3. Does it still work? → Rewrite. It must ONLY work for you.

### Facts Over Adjectives

Every adjective is a missed opportunity for a fact.

| Adjective | Fact |
|---|---|
| "trusted" | "Used by 3,000 teams including Stripe and Notion" |
| "fast" | "Loads in 200ms" |
| "popular" | "12,000 signups in the first week" |
| "reliable" | "99.99% uptime since 2023" |

### The Conflict Framework

Create memorability through tension. State what you're AGAINST, then what you stand FOR.

**Pattern:** "We don't [conventional approach]. We [our approach]."

| Against | For | Brand |
|---|---|---|
| "Don't buy this jacket" | Quality over consumption | Patagonia |
| "Think different" | Non-conformity over status quo | Apple |
| "A dating app designed to be deleted" | Relationships over engagement | Hinge |

**When to use:** Contrarian hooks, differentiation headlines, brand manifestos, about pages. Not every piece needs conflict — reserve for high-impact placements.

### CTA Formula

`[Action Verb] + [What They Get] + [Qualifier]`

Bad: Submit, Learn More, Click Here
Good: "Start your free trial", "Download the 2026 playbook", "See pricing for your team"

### Speed Test

Show someone the copy for two seconds. If they don't get it, rewrite.

---

## Psychology of Persuasion

### Pratfall Effect
Small, authentic imperfections increase trust. A brand that admits a weakness ("Our UI isn't the prettiest — but our data is the most accurate") is more believable than one that claims perfection. Include one honest limitation in long-form copy, then pivot to your strength.

### Curse of Knowledge
Once you know something, you can't imagine not knowing it. Product teams write copy that assumes the reader understands their jargon. Test every key line with someone outside the company. If they can't explain it back, use the Zoom-In Technique to replace abstraction with concreteness.

---

## Anti-Patterns

**Adjective-heavy copy** — "Innovative, cutting-edge, best-in-class solution" says nothing specific. Replace every adjective with a fact: "Used by 3,000 teams" beats "trusted by many."

**Features without benefits** — "Real-time sync" is a feature. "Never ask 'did you see my update?' again" is a benefit. Lead with the outcome the reader cares about, then mention the feature that enables it.

**Writing for the brand, not the buyer** — Copy that sounds impressive to the marketing team but doesn't use the buyer's language. Pull phrasing from VoC quotes and ICP research — write how they talk, not how the brand talks.

**AI copy slop** — Recognizable AI-generated patterns that signal generic output: "Unlock the power of...", "In today's fast-paced world...", "Revolutionize your workflow", "Seamlessly integrate", "Whether you're a [X] or a [Y]". The Competitor Swap Test catches most of these — if it reads like any SaaS website's hero, it fails.

**First-draft delivery** — Delivering the first version of a headline without variation or evaluation. Key lines always need 3-5 versions.

**Untested uniqueness** — Assuming copy is ownable without running the swap test. Most copy fails the swap test on first draft.

---

## References

- [references/copywriting-craft.md](references/copywriting-craft.md) — Variation workflow, extended techniques, evaluation rubric, annotation guide
- [references/seven-sweeps.md](references/seven-sweeps.md) — Structured 7-pass editing method (Clarity → Voice → So What → Prove It → Specificity → Emotion → Zero Risk)
- [references/headline-formulas.md](references/headline-formulas.md) — Outcome, problem, audience, differentiation, and proof-focused headline formulas
- [references/page-sections.md](references/page-sections.md) — Landing page section types, page structure templates, testimonial selection
