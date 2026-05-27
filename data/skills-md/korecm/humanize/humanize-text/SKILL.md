---
name: humanize-text
description: Rewrite AI-generated text so it reads as if written by a human. Removes AI tells (uniform sentence length, hedge clichés, translationese, em-dash overuse, abstract noun stacks, perfect topic sentences) and injects human signals (burstiness, casual register, sentence fragments, personal voice, register variation). Multi-language with per-language rule packs in references/<lang>.md. Use when the user asks to humanize text, make AI writing sound natural, remove ChatGPT/Claude tells, or rewrite formal text in a casual human voice.
---

# Humanize Text

Rewrite text so it reads as human-written. Language-agnostic procedure + per-language rule packs.

## Procedure

1. **Detect language** of the input.
   - Use `scripts/detect-lang.js <file>` if available, or judge from script + vocabulary.
   - Supported: `ko`, `en`. Fallback to closest match for other languages, but warn the user.

2. **Load the rule pack** for that language: `references/<lang>.md`.
   - Always also load `references/_common.md` for language-agnostic principles.

3. **Diagnose AI tells** in the input against the rule pack's `## AI tells` section.
   - List the specific tells you found (line/phrase level). Do not skip this.

4. **Rewrite** applying the rule pack's `## Rewrite rules`. Then apply `## Human signals` to inject naturalness.
   - Preserve meaning, facts, numbers, names, structure of argument.
   - Do not invent new claims, opinions, or anecdotes the original does not imply.

5. **Validate** against `_common.md` metrics:
   - Burstiness — sentence-length variance (mix short and long).
   - Register variation — not every sentence in the same form.
   - Concrete > abstract — abstract nouns reduced.
   - No meta scaffolding ("In conclusion / 결론적으로 / 따라서") unless the original explicitly needs it.

6. **Optional deterministic post-pass**: if the working tree has `scripts/rules/<lang>.json`, you may run the regex substitutions in it as a final pass. These are safe one-to-one swaps (translationese phrases, AI vocab blocklist).

## Output format

Default: return only the rewritten text. No preamble, no explanation.

If the user asks "what did you change" or "diff", produce a brief diagnosis list (the AI tells found, the rules applied) followed by the rewritten text.

## When NOT to humanize

- Legal, regulatory, academic-formal contexts where the formal register is required — confirm with the user first.
- Code, command output, structured data (JSON, YAML).
- Direct quotations.

## Adding a new language

1. Create `references/<lang>.md` with the same section structure as `ko.md`:
   `## AI tells` → `## Human signals` → `## Rewrite rules` → `## Examples`
2. Create `scripts/rules/<lang>.json` with `{ "translationese": [[pattern, replacement], ...], "blocklist": [...] }`.
3. Add the language to `scripts/detect-lang.js`'s supported list.

The procedure above is language-agnostic. Rules live entirely in the language pack.
