---
name: interface-craft
description: Improve product interfaces with tasteful UI craft, micro-interactions, accessibility-preserving polish, and detail-oriented review. Use when building UI, reviewing components, improving perceived quality, making an interface feel better, or auditing forms, buttons, motion, typography, empty states, loading states, and navigation polish.
---

# Interface Craft

Use this skill to make UI feel intentional without turning polish into decoration.

## Resolve the mode

- **Build**: add relevant craft details while implementing UI.
- **Polish**: improve existing UI directly and explain high-impact changes.
- **Review**: do not edit unless asked; produce concise findings with file/line evidence.

If the user's intent is ambiguous, assume **Review** for existing code and **Build** for new UI.

## Workflow

1. Identify the surface: form, button, navigation, loading state, empty state, content display, motion, or platform shell.
2. Read `references/interface-craft-rules.md` and load only the relevant section(s).
3. Apply the restraint gate before proposing any detail.
4. In Build/Polish mode, implement the smallest consistent improvement across sibling surfaces.
5. In Review mode, group findings by file and cite rule IDs.

## Restraint gate

Skip a detail if any answer is no:

- Does it help the user complete or understand the task?
- Does it preserve keyboard, screen reader, touch, and reduced-motion behavior?
- Is it consistent with the product's existing system?
- Is the effect quieter when the interaction is frequent?
- Can the improvement be described in observable terms?

## Review output

```text
path/to/File.tsx:42 — ic-form-1
Label is visually present but not programmatically associated with the input.
Fix: connect label and input with htmlFor/id or wrap the input in the label.
```

Keep review findings high-signal. Prefer 3 material fixes over 20 cosmetic notes.
