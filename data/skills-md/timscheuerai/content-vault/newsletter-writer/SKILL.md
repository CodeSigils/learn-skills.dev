---
name: newsletter-writer
description: Draft newsletters, lifecycle/onboarding emails, and broadcasts in YOUR voice. Uses the linkedin-copywriter corpus as the voice anchor and a hardened anti-slop pass to keep the output from reading like a SaaS template. Renders to your master email template and (optionally) ships to Resend. Use when asked to "write a newsletter", "write the welcome / day-X / check-in email", "draft a broadcast", or "/newsletter-writer".
---

# newsletter-writer

Draft emails (newsletters, onboarding sequences, broadcasts) that read
like you, not like ChatGPT. Renders into your brand email template and
(optionally) pushes to Resend.

This skill **fails its job if the output reads like generic SaaS copy.**
That is the test. Smoothness is the failure mode.

---

## SETUP (run this once before drafting)

The voice comes from the same corpus the writer skills share:

1. Populate `skills/linkedin-copywriter/corpus.md` (copy from
   `corpus.md.example` and fill with your top posts). The newsletter
   voice is anchored to those posts.
2. Fill the placeholder tokens this skill uses verbatim in CTAs and
   sender lines: `<YOUR_NAME>`, `<YOUR_BRAND>`, `<YOUR_DOMAIN>`,
   `<YOUR_EMAIL>`, `<YOUR_CAL_LINK>`.
3. If you ship through Resend, set the env + IDs in step 8:
   `RESEND_API_KEY`, `<YOUR_RESEND_AUDIENCE_ID>`, `<YOUR_RESEND_FROM>`.
   Skip this whole block if you only want the drafted copy.
4. (Optional) Point `<YOUR_EMAIL_TEMPLATE>` at your master HTML email
   chrome. No template? The skill drafts the copy and you paste it
   wherever you send from.

---

## When to invoke

Triggers: "write a newsletter", "draft the welcome email", "day-X
check-in email", "broadcast about X", "/newsletter-writer".

In scope:
- Lifecycle / onboarding sequence emails (welcome, activation nudges,
  founder check-ins, win-back)
- One-off newsletters / broadcasts
- Transactional emails with marketing copy (receipts, account events
  that double as touchpoints)

Out of scope (use the other skill):
- LinkedIn posts → `/linkedin-copywriter`
- Long-form blog / docs → `/long-form`
- YouTube scripts → `/youtube-script`

---

## Workflow

### 1. Brief

```
Quick brief.

1. Email type: welcome, activation nudge, founder check-in, broadcast/newsletter, win-back.
2. The single specific anchor: a number, a tool name, a person, a moment, or a real observation. Concrete beats generic. ("5 days in" / "you ran the install yesterday" beats "thanks for joining").
3. Primary CTA: install, book a call, browse resources, reply, share, upgrade.
4. Audience: all subscribers, free trial, paying, segment.
5. Send timing: trigger event + delay, or scheduled date.
```

Parse what the user gave; only ask for missing fields.

### 2. Voice anchors

Read `../linkedin-copywriter/corpus.md` if you haven't this session.
The top 5 posts there are your viral anchors. Internalise:

- Punchy opens. Often one short sentence or fragment.
- Numerals everywhere ("$480/year", "80k emails", "5 days in").
- Specific tool names (the real ones in your stack).
- Specific people by name + context.
- Opinionated takes that signal stake ("They are wrong.").
- Self-aware moments ("still a bit mindblown", "at least that's the plan").
- Uneven pacing. Fragments mixed with longer thoughts. One-word sentences.
- → arrows for choice-lists.
- Direct asks, not generic CTAs.

### 3. Adapt for email

- **Subject**: lowercase, < 50 chars, concrete. "5 days in." / "anything stuck?" / "welcome to <YOUR_BRAND>" beats "Welcome to the <YOUR_BRAND> Family!".
- **Preheader**: < 90 chars, specific hook. The inbox preview line.
- **Body**: 3-6 short blocks. One idea per paragraph. Three sentences is a long paragraph.
- **CTA**: one primary, button-styled. Optional inline secondary link. The button label is a specific verb, not "Get started" or "Learn more".

### 4. Slop blacklist — hard rejects

The model has trained on a million SaaS emails. These patterns are its
defaults and they all signal AI. Reject every one. Re-read the draft
hunting for them before approving.

**Structural patterns to reject:**

| Pattern | Why it's slop | Replace with |
|---|---|---|
| "The [adj] way to [verb] X" · "The fastest way to feel what <YOUR_BRAND> does" | LLM stem cell | Drop the framing entirely. Just state the action. |
| "X, Y, and Z" three-item parallels | AI rhythm | Pick one. Or use two with no conjunction. Or be specific about each. |
| "No X, no Y, no Z" enumerated negatives | Borrowed from Apple keynote, now everywhere | Pick one negative and make it concrete. ("Nothing to wire up.") |
| "Whether you're X or Y" generic positioning | Hedging | Pick an audience and address them. |
| "Designed to" / "Built to" | Passive feature copy | Active. ("It scores leads 0-100." not "Designed to score leads.") |
| "We believe" / "We think" | Soft claims | State or shut up. |
| Promise-then-soften · "It does X. Of course, X has limits..." | Cover-your-ass instinct | Make the claim clean. Address limits elsewhere or not at all. |
| Smooth corporate transitions · "Here's the thing." / "Here's why." | Connective filler | Cut. Start the next sentence. |
| Three-clause smoothing · "fast, efficient, and reliable" | LLM default rhythm | Pick one. Make it specific. |
| "Imagine if" / "What if I told you" / "Picture this" | Hype opener | Open with a number, a name, or a fragment. |
| Generic CTA labels · "Get started", "Learn more", "Try it now" | Don't earn the click | Specific verb. "Install the CLI" / "Browse the resources" / "Book 45 minutes" |

**Voice patterns to reject:**

| Pattern | Why | Fix |
|---|---|---|
| Em dashes (—, –) | Brand rule | Period, comma, colon, parens, or `·` middot |
| Banned words: leverage, synergy, robust, world-class, seamless, intuitive, powerful, innovative, game-changer, revolutionize, unlock, delve, in today's fast-paced world | Universally AI-marked | Use plain English or a concrete verb |
| "Hey [Name]" when [Name] isn't available | Empty greeting | Skip greeting entirely. Start with the substance. |
| Sign-offs invoking the sender's name when From line already has it | Redundant | Often skip the signature block entirely · the From carries identity |
| Uniform sentence lengths | AI-rhythm tell | Vary deliberately. Mix one-word sentences, fragments, and longer thoughts. |

### 5. Texture requirements — every draft must have

These are what make copy feel hand-typed, not generated:

- **At least one specific number or proper noun in the first 30 words.**
- **At least one piece of texture**: a specific tool name, a real
  observation, a self-aware aside, a time anchor, or a named person.
- **At least one direct opinion or stake**, especially in newsletters.
  ("They are wrong." / "Don't bother with X." / "This was a mistake.")
- **Sentence-length variation**. Drop in at least one fragment or
  one-word sentence somewhere.

If a draft has zero of these, the draft is slop. Rewrite.

### 6. Self-audit before approving

After drafting, do a re-read with this checklist:

```
[ ] Opens with a number, fragment, name, or claim (not setup phrasing)
[ ] No "The [adj] way to..." anywhere
[ ] No "X, Y, and Z" parallels
[ ] No "No X, no Y, no Z" enumerated negatives
[ ] No banned words
[ ] No em dashes
[ ] At least 1 specific number / proper noun in first 30 words
[ ] At least 1 texture moment (tool name / observation / aside)
[ ] CTA label is a specific verb, not generic
[ ] Sentence lengths vary
[ ] If sender name isn't dynamic, no "Hey [name]" greeting
[ ] If From carries identity, signature block is optional, often skipped
```

Any unchecked item = rewrite that section before showing the user.

### 7. Before / after examples

**SLOP** (what the LLM defaults to):

```
Hey,

The fastest way to feel what <YOUR_BRAND> does is to clone someone else's setup.

Templates are pre-built workflows · tables, integrations, and
dashboards that drop into your workspace in 30 seconds. No yaml, no
glue code, no chasing the right combination of providers.

The full library lives on the resources page · featured by us, plus
what the community is sharing.

[Browse the resources →]

Build something worth sharing? Hit reply with the slug and
I'll feature it.
```

What's wrong: "Hey," empty greeting · "The fastest way to feel" stem
cell opener · "tables, integrations, and dashboards" three-parallel ·
"No yaml, no glue code, no chasing" enumerated negatives · "lives on
the resources page · featured by us, plus what the community" smooth
corporate transition · no specific numbers · no texture.

**TIGHTER** (your voice):

```
You can read about <YOUR_BRAND> all day. Easier to just clone someone's
setup and run it.

That's what the templates are. Pre-built workflows you drop into your
workspace. 30 seconds, no yaml.

The library is on the resources page · what we've shipped, plus what
people are sharing.

[Browse the resources →]

Built something useful? Reply with the slug. If it's good I'll feature
it on the page.
```

What changed: opens with a specific stake ("You can read about
<YOUR_BRAND> all day"). One negative not three. Specific number ("30
seconds"). "If it's good" is an opinion. Same length but more weight.

### 8. Render + push to Resend (optional)

After the user approves the draft. Skip this block entirely if you
just want the copy.

```bash
# Compose the HTML using your master template chrome (<YOUR_EMAIL_TEMPLATE>).

# Render preview
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-sandbox \
  --window-size=700,1200 --hide-scrollbars --virtual-time-budget=2000 \
  --screenshot=lifecycle/<flow>/<NN-slug>-preview.png \
  "file://$(pwd)/lifecycle/<flow>/<NN-slug>.html"

# Push to Resend (newsletters = broadcasts, lifecycle emails = templates)
set -a; source .env; set +a

# For broadcasts:
python3 -c "
import pathlib, json
html = pathlib.Path('lifecycle/newsletters/YYYY-MM-DD-<slug>.html').read_text()
pathlib.Path('/tmp/bc.json').write_text(json.dumps({
    'audience_id': '<YOUR_RESEND_AUDIENCE_ID>',
    'from': '<YOUR_RESEND_FROM>',     # e.g. '<YOUR_NAME> <hello@updates.<YOUR_DOMAIN>>'
    'reply_to': '<YOUR_EMAIL>',
    'subject': '<SUBJECT_LINE>',
    'preview_text': '<PREHEADER>',
    'html': html,
}))
"
curl -s -X POST -H "Authorization: Bearer $RESEND_API_KEY" \
  -H "Content-Type: application/json" \
  --data-binary @/tmp/bc.json https://api.resend.com/broadcasts

# For lifecycle templates (then attach to an automation step):
# POST /templates with {name, subject, html, from, reply_to}
# POST /templates/{id}/publish
```

Persist resource IDs to a local state file (e.g. `lifecycle/resend.json`).

---

## Quality bar

Before declaring done:

- Self-audit checklist all passed.
- Reads aloud like you on a call. If you imagine saying it to a
  customer over Zoom, ship it.
- One specific number or name in first 30 words.
- Single primary CTA, specific verb label.
- Renders correctly in the local Chrome screenshot (if you templated it).

---

## Content graph (close the loop)

When an issue is saved as a `content/posts/` file, it feeds the content
knowledge graph (`content/CONTENT-WIKI.md`). Before drafting, pull the
relevant note from `content/concepts/` and build on its canonical lines
instead of starting blank. After the issue ships, deposit its 1-3 core
ideas back: add the post to each concept's `## Appears in` (create a note
if the idea is genuinely new), update any `content/entities/` or
`content/mocs/` it touches, and append to `content/log.md`. Edges live in
the concept notes (Obsidian backlinks are automatic), so don't edit the
post body to add them.

## Related

- Voice corpus (shared with /linkedin-copywriter):
  [`../linkedin-copywriter/corpus.md`](../linkedin-copywriter/corpus.md)
- Reference creators: [`../linkedin-copywriter/reference-creators.md`](../linkedin-copywriter/reference-creators.md)
- Brand voice rules: `<YOUR_BRAND_DOC>`
- Booking link for CTAs: `<YOUR_CAL_LINK>`
