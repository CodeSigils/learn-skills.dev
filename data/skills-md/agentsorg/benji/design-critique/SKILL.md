---
name: design-critique
description: "Use when judging a rendered screen or screenshot rather than code: what to look at in what order, naming what feels wrong, and turning it into a written rule."
---


# Judging a Rendered Screen

Default posture: **look in a fixed order, and refuse to say anything you cannot write down as a rule.** "It feels off" is a reaction, not a finding — it cannot be handed to anyone, cannot be checked tomorrow, and cannot be argued with. The work of a critique is converting a reaction into a falsifiable sentence of the form *this element should be this exact value because this mechanism*. Benji Taylor's account of pairing with a model on morphing icons names the failure precisely: the model got it technically correct but optimised for working rather than feeling right, so a human had to watch the transitions and describe what was wrong. That description is the deliverable here. Emil Kowalski's framing is the reason it is learnable at all — taste is a trained instinct rather than a preference, so almost every reaction has a reason underneath it if you look long enough to find it.

The sibling boundary is the artifact under review: `ui-review` reads a diff and returns a verdict on code, this skill reads pixels and returns rules. `ai-tells` matches a fixed list of literal tokens and answers one question; this teaches a looking order and will find things no list contains.

**Before naming anything wrong, find out what the screen is already supposed to obey.** Open the project's token file, `DESIGN.md`, Tailwind theme, or component library and read the scale, the ramp, and the elevation ladder. A critique that proposes values from outside that system produces a fork, not a fix — so the rule you write should name the project's own step ("this gap should be the `space-4` step, not an off-scale 13px"), and only invent a value when the project demonstrably has no system yet.

## Quick reference

| Topic | File | Open it when |
|---|---|---|
| Building the judgment itself — paired comparison, the write-down-why protocol, the reference library | `references/training-judgment.md` | Open it when the request is to get better at this rather than to fix this screen, or when you looked and genuinely could not name what was wrong. |

## The looking order

Work top to bottom. Do not deliver a finding from a later stop while an earlier stop is unresolved — a shadow note delivered under an inverted hierarchy is noise.

| Stop | The question | What it catches |
|---|---|---|
| 1. Structure | What is this screen for, and where does the eye land first? | Two competing primaries, inverted hierarchy, no focal point |
| 2. Rhythm | Do the gaps come from one scale, and do things that belong together sit together? | Off-scale values, proximity grouping failures, broken alignment |
| 3. Contrast | Is hierarchy carried by weight and grey value, or only by size? | Everything emphasized, a second accent, unreadable secondary text |
| 4. States | What does this look like when it is empty, loading, wrong, or full? | The missing four-fifths of the design |
| 5. Motion | Should this move at all — and if it does, what does it look like slowed down? | Desync, wrong origin, motion that should be deleted |

## Core principles

1. **Finish each stop before starting the next.** Structure errors change every downstream judgment, so a rhythm finding written under an unresolved hierarchy is usually wrong. Deliver `0` findings from stop 3 while stop 1 is open. *Exception:* a crop that shows only one stop — a lone shadow, a single button — starts at whatever stop the crop belongs to.

2. **Convert every reaction into a falsifiable rule before speaking it.** The form is `<element> should be <exact value or behavior> because <mechanism>`. A rule in that shape can be disagreed with, tested, and pasted into a design document; "make it cleaner" cannot. *Exception:* when you looked hard and still cannot name it, say exactly that and escalate to a slow-motion or next-day pass — a guessed mechanism is worse than an admitted gap.

3. **Point, then say why.** Benji Taylor's rule for feedback headed to an agent: pointing beats describing, because a selector, `file:line`, or coordinate costs the reader nothing to resolve while "the blue button in the sidebar" costs a search. Give both — the pointer says *where*, the prose says *why*. *Exception:* a bare pointer with no reason is worse than prose; if you have no mechanism yet, you have no finding yet.

4. **Critique the instance, never restate the guideline.** Benji Taylor's distinction: guidelines describe principles, feedback addresses instances. "Follow the spacing scale" is a guideline someone already wrote; "this card's `13px` gap is off the scale — use the neighbouring `12px` step" is feedback. *Exception:* when the screen violates a principle the project has never written down, write the principle once — then still attach it to the instance.

5. **Never judge motion at full speed.** Every Benji Taylor demo ships with a 1× / 0.5× toggle for exactly this reason; Emil Kowalski's version is to raise duration `2–5×` or step frame-by-frame in the DevTools Animations panel, watching for opacity, transform, and color falling out of sync. At full speed you can only register that something was wrong, not what. *Exception:* on a 100+/day interaction the slow-motion pass is moot — the live question is whether it should animate at all, which `motion` owns.

6. **Distrust a still frame for anything stateful.** One screenshot shows one state out of hover, focus-visible, active, disabled, empty, loading, error, overflow, and longest-string — so a critique from a single frame is at best one-ninth of a critique. Ask for the missing frames or scope the critique out loud. *Exception:* a deliberately static surface, such as a marketing hero, where the composition genuinely is the artifact.

7. **Look again the next day.** Emil Kowalski's habit: fresh eyes find the imperfection that familiarity hid during the build. Cheap, and it changes the finding list more often than any tool does. *Exception:* when the deadline is today, substitute cold eyes — hand it to someone who has never seen the product and take their first reaction literally.

8. **Reject the one-shot.** Benji Taylor: sometimes it is one pass, usually a few, and the point is that each pass counts. A critique that fires once and declares itself finished is optimising for looking decisive. *Exception:* a screen already inside a mature system may genuinely resolve in one pass — say so rather than inventing a second.

## Smells

| Smell | Fix |
|---|---|
| "It feels off" / "make it pop" | Name the phenomenon; `naming` owns the term |
| A finding with no pointer | Add the selector, `file:line`, or coordinate |
| A pointer with no mechanism | Add the *because*, or drop the finding |
| Critique that quotes the guideline | Requote it as the instance and its exact value |
| Motion judged from a description | Watch it at `0.5×` or step it frame-by-frame first |
| Verdict from one screenshot | Ask for hover, focus, empty, loading, error, overflow |
| Ten notes with no ranking | Order by the looking-order stop; structure first |
| "This is great" with nothing preserved | Name what must survive the fix, so it does |

## Output format

Findings grouped under the looking-order stop they came from, earliest stop first. Each finding is three parts on one line: **where** (selector, `file:line`, or a coordinate on the screenshot), **what** (the phenomenon, named), **rule** (`<element> should be <value> because <mechanism>`).

Close with a **Rules** block: every rule from the findings restated free of this screen, in the form the project could paste into its design document. That block is the durable output — the screen gets fixed once, the rules keep applying. If a state could not be inspected, name it in one line rather than implying it passed.

## Checklist

- [ ] Project tokens and design doc read before naming anything wrong
- [ ] Stops worked in order; nothing delivered from a later stop over an open earlier one
- [ ] Every finding carries a pointer and a mechanism
- [ ] Every finding restated as `<element> should be <value> because <mechanism>`
- [ ] Motion inspected at reduced speed or frame-by-frame, never at full speed
- [ ] Missing states requested or explicitly scoped out
- [ ] Instances critiqued, guidelines not restated
- [ ] Rules block written and free of this specific screen
- [ ] Nothing named that you could not defend tomorrow with fresh eyes
