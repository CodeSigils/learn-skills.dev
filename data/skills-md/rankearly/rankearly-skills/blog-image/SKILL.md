---
name: blog-image
description: Generate a Nanobanana Pro prompt for blog images - either a scroll-stopping cover or an explanatory in-post illustration. Use when the user asks for a "blog cover", "blog image", "post thumbnail", "illustration for my blog", "header image", or wants to create a visual for a blog post or article section.
metadata:
  displayName: Blog Image
  status: live
  phases:
    - name: Determine mode
    - name: Generate prompt
    - name: Review prompt
---

Generate **one optimized Nanobanana Pro prompt** for a blog image.

## Step 1: Pick the mode

| Mode | Use when the user wants... | Goal |
|------|---------------------------|------|
| **Cover** | A header, hero, thumbnail, or scroll-stopper | Visual impact — abstract and attention-grabbing |
| **Illustration** | An in-post diagram, workflow, comparison, or concept explainer | Clarity — literal and educational |

If the user supplies a blog title for a cover, treat it as a **titled cover** (title becomes the focal point).

## Step 2: Apply the mode spec (subagent)

Read the corresponding reference file for the chosen mode:

- **Cover** → `references/cover.md`
- **Illustration** → `references/illustration.md`

Apply all style rules, palette constraints, and formatting guidelines from that file.

## Step 3: Write the prompt

Use this structure:

**Mode:** [Cover / Illustration]

**Focus:** [One-line description of the visual's purpose]

````
[ASPECT] [TYPE], [STYLE DESCRIPTORS]. [BACKGROUND].

[LAYOUT — structure, placement, spacing]

[ELEMENTS — each with color, position, label, visual cue]

[RELATIONSHIPS — what connects, groups, or contrasts]

[STYLE NOTES from the mode spec above]
````

Keep the prose tight. Every sentence should either describe something the generator needs to draw or a style rule it needs to follow.

## Step 4: Review and tighten

Before returning the prompt, check it once:

- Remove repeated facts or labels.
- Labels should name entities of the diagram, not effects.
- Return only the cleaned-up prompt.
