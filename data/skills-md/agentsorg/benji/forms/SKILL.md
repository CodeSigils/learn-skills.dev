---
name: forms
description: "Use when building inputs and validation: field layout, labels, validation timing, error recovery, autofill, keyboard flow, and multi-step submission."
---


# Building Fields, Validation, and Submission

The default posture: **one column, a persistent label above every field, a real `<form>` element, validation on blur and then on change, and the error rendered directly beneath the field that caused it.** Forms are where users do real work and they notice every rough edge — the label that doesn't focus its input, the page that zooms on iOS, the submit that fires twice, the Enter key that does nothing. None of these are hard; they are only easy to forget. Start from the semantics the platform gives you and add as little as the design requires. This skill owns *construction* — layout, timing, autofill tokens, submit handling. `a11y` owns the *contract* the finished form must honour: tab order, focus management, `:focus-visible`, ARIA, and live-region announcements. When a rule concerns what the assistive stack hears rather than how the field is built, it belongs there, not here.

**Work inside the form stack the project already has.** Look for React Hook Form, Formik, TanStack Form, native `FormData` with a server action, or a hand-rolled `useState` per field; look for a schema layer (Zod, Valibot, Yup) and an existing `<Field>` / `<FormItem>` wrapper. Wire your validation into the resolver that is already there. A second validation library — or client rules that silently disagree with the server schema — produces fields that pass locally and fail on submit, which is the worst error state a form can have.

## Quick Reference

| Topic | Reference | Open it when |
|---|---|---|
| Per-field-type recipes: input `type`, `inputmode`, `autocomplete` token, validation timing, and error string for email, password, OTP, phone, number, date, search, select, file, textarea, address | `references/field-recipes.md` | Open it whenever you are building a specific field type and need its exact attribute set, rather than deciding a general rule. |

## Core Principles

1. **The label is persistent, sits above the field, and focuses it.** A placeholder is not a label: it disappears the instant typing starts, exactly when the reminder is needed, and it leaves autofill nothing stable to bind to. Wire it with `<label for="email">` + `id="email"`, or wrap the input. Exception: a lone search box with a visible icon may carry a visually hidden label — hidden, never absent.

2. **Validate on blur, then on change once an error is showing.** Flagging a field while the user is mid-way through their first attempt shouts "invalid email" after one character. Once the error exists, switch that field to validating on every change so it clears the moment it is fixed: reward early, punish late. Exception: purely additive live feedback — a password strength meter, a character counter — may update on change from the start because it never accuses.

3. **Anchor every error to its field.** Render the message directly beneath the control with `aria-invalid` set, never in a summary at the top of the form, which makes the user hunt for the field the summary is describing. Exception: an error that belongs to no single field ("Card declined", "This invite has expired") goes immediately above the submit button, where the action that triggered it lives.

4. **Give every field its type, its `inputmode`, and its `autocomplete` token.** These are three separate switches: `type="email"` picks browser validation, `inputmode="email"` picks the mobile keyboard, `autocomplete="email"` picks the autofill entry. Exception: fields that aren't identity or address data — slugs, codes, invite names — take `autocomplete="off"`, `spellcheck="false"`, and `data-1p-ignore` / `data-lpignore="true"` so password managers stop overlaying them.

5. **Inputs, textareas, and selects render at `16px` or larger.** Below that, iOS Safari zooms the whole page on focus and the user has to pinch back out. Set it globally and scale the visual weight some other way if the design wants smaller text. Exception: none on touch — `touch-input` holds the wider iOS Safari catalog, but this one value is a field property and belongs on every field you build.

6. **Never disable the submit button to express invalidity.** A greyed-out button with no explanation is a dead end: the user cannot discover which field is wrong. Let submit run, validate everything, and move focus to the first invalid field. Disable it *only* while a submission is in flight, swap the label to say what is happening (`Saving…`), and reserve the width so the button does not resize. Exception: a genuinely unavailable action — an expired session, an exhausted quota — may be disabled, and then it needs adjacent text saying why.

7. **Wrap the fields in a `<form>` so Enter submits.** A lone input outside a form makes Enter do nothing, which reads as broken. In a textarea, where Enter must insert a newline, bind `Cmd+Enter` / `Ctrl+Enter` to submit instead. Autofocus the first field when a modal opens, and suppress it on touch (`'ontouchstart' in window`) so the keyboard does not ambush the user. Exception: a form whose primary action is destructive should not submit on Enter from a single-line field — require the button.

8. **Overlay decorations on the input; leave no dead zones on controls.** Prefix icons, suffix units, and clear buttons are absolutely positioned over the input with matching padding, not rendered as siblings — otherwise the border lies about the hit area and clicking the icon does nothing. Static decorations take `pointer-events: none`; clickable ones refocus the input. For checkboxes and radios, one `<label>` wraps control and text so the control, the text, **and the gap between them** are all clickable. Exception: a decoration that opens a distinct surface (a currency picker, a country selector) is a real adjacent control and should look like one.

9. **Chunk multi-step forms by decision, not by field count.** Each step should ask one question the user can answer without leaving the page for information. Persist entered values before navigating so Back never destroys work, keep the URL in step with the step so a refresh does not restart the flow, and show `Step 2 of 4` only when the total is genuinely fixed. Exception: a branching flow where the remaining count is unknown shows the current step name without a total — a fake denominator is worse than none.

10. **Prefill everything you already know.** The logged-in user's name, email, and locale should already be in the fields, and a link into a form should carry its context — a "Change username" link lands on a form already scoped to that request. Exception: security-sensitive re-entry (current password, payment CSC, a confirmation email address) is never prefilled.

## Smell / Fix

| Smell | Fix |
|---|---|
| Placeholder used as the label | Persistent `<label>` above; placeholder shows format only, or nothing |
| Error summary stacked at the top of the form | Message under its field, `aria-invalid` on the control |
| "Invalid email" after one keystroke | Validate on blur; switch to on-change only after the error exists |
| Submit disabled until the form is valid | Always submittable; validate on submit and focus the first invalid field |
| Submit stays live and fires twice | Disable in flight, swap label, reserve width |
| `14px` input text | `16px` minimum on input, textarea, select |
| Icon rendered as a sibling of the input | Absolutely positioned over it, padding makes room, `pointer-events: none` |
| Checkbox where only the 16px box is clickable | One `<label>` wrapping control, text, and gap |
| `<div onClick>` as a button | A real `<button type="button">` |
| Back button on step 3 wipes steps 1 and 2 | Persist on navigate; the URL carries the step |

## Output Format

Every field ships as the same four-part block, in this order, and nothing is skipped:

```
label  →  hint (optional, persistent)  →  control  →  error (conditional)
```

The hint sits above the control, because a format requirement read after typing is read too late. The error slot is reserved in the layout — an error appearing must not push the rest of the form down.

## Checklist

- [ ] Persistent label above every field, wired so clicking it focuses the control
- [ ] Correct `type`, `inputmode`, and `autocomplete` token on every field
- [ ] `16px` minimum font-size on input, textarea, select
- [ ] Validation on blur first, on change only after an error is showing
- [ ] Error rendered under its own field with `aria-invalid`; form-level errors above submit
- [ ] Submit never disabled for invalidity; disabled + relabelled during flight only
- [ ] Fields inside a `<form>`; Enter submits; `Cmd/Ctrl+Enter` submits from a textarea
- [ ] Autofocus in modals, suppressed on touch
- [ ] Decorations overlaid on the input; no dead zones in checkbox and radio rows
- [ ] Multi-step: one decision per step, values persisted, URL tracks the step
- [ ] Everything knowable is prefilled; nothing security-sensitive is
- [ ] Keyboard order, focus return, and announcements verified against `a11y`
