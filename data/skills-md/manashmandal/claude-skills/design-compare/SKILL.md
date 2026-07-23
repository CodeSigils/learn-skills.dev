---
name: design-compare
description: Use when comparing a frontend implementation against a reference design (Figma, mockup, screenshot). Performs pixel-level and structural analysis to identify discrepancies.
---

# Design Compare

## Overview

Compare your frontend implementation against a reference design to identify visual discrepancies, spacing inconsistencies, and structural mismatches.

**Core principle:** Every pixel matters. Systematic comparison reveals what eyeballing misses.

## When to Use

Use this skill when:
- Implementing a design from Figma/Sketch/mockup
- Checking if implementation matches design spec
- Debugging visual differences between design and code
- QA review before handoff
- User says "compare this to the design" or "check against mockup"

## Required Inputs

1. **Reference design** - Screenshot, Figma export, or mockup image
2. **Implementation** - Screenshot of current frontend OR URL to capture

**Announce:** "I'll compare your implementation against the reference design using design-compare."

## Comparison Process

### Phase 1: Capture and Prepare

1. **Obtain reference design**
   - User provides screenshot/image path
   - Read the image using Read tool
   - Note dimensions, viewport size

2. **Capture implementation**
   - User provides screenshot OR
   - Request user to capture current state
   - Match viewport/dimensions to reference

### Phase 2: Structural Analysis

Compare these elements systematically:

| Element | Check For |
|---------|-----------|
| **Layout** | Grid alignment, container widths, flex/grid structure |
| **Spacing** | Margins, padding, gaps between elements |
| **Typography** | Font family, size, weight, line-height, letter-spacing |
| **Colors** | Background, text, borders, shadows |
| **Components** | Button styles, inputs, cards, icons |
| **Hierarchy** | Visual weight, heading levels, emphasis |
| **Responsive** | Breakpoint behavior if applicable |

### Phase 3: Generate Comparison Report

**Output format:**

```markdown
## Design Comparison Report

### Match Score: [X/10]

### Critical Discrepancies (Must Fix)
- [ ] Issue description | Location | Reference vs Implementation

### Minor Discrepancies (Should Fix)
- [ ] Issue description | Location | Reference vs Implementation

### Acceptable Variations
- Variation description | Reason acceptable

### Pixel-Perfect Elements
- Element that matches exactly
```

## Evaluation Criteria

### Spacing (Weight: High)
- Measure in pixels or design tokens
- Flag differences > 4px
- Check consistency across similar elements

### Typography (Weight: High)
- Font family must match exactly
- Size tolerance: ±1px
- Weight must match (400 vs 500 matters)
- Line-height tolerance: ±2px

### Colors (Weight: Medium)
- Hex values within #02 tolerance per channel
- Check in multiple states (hover, active, focus)
- Gradient direction and stops

### Layout (Weight: Critical)
- Container widths must match
- Alignment (left/center/right)
- Element ordering
- White space distribution

### Visual Polish (Weight: Medium)
- Border radius consistency
- Shadow values
- Icon sizing and alignment
- Image aspect ratios

## Common Discrepancies

| Issue | Impact | Typical Cause |
|-------|--------|---------------|
| Inconsistent spacing | High | Missing design tokens |
| Wrong font weight | Medium | Default browser styles |
| Color off by shade | Low | Color space conversion |
| Different line-height | High | Framework defaults |
| Misaligned icons | Medium | Baseline alignment issues |
| Border radius mismatch | Low | Hardcoded values |

## Output Actions

After comparison, offer:
1. **Generate CSS fixes** - Output corrected values
2. **Create issue list** - Checklist format for tickets
3. **Deep dive** - Analyze specific element in detail

## Red Flags

Stop and clarify if:
- Reference image is low resolution
- Implementation uses different viewport size
- Design has responsive variants not provided
- Component states differ (hover vs default)

## Integration

**Related skills:**
- `design-audit` - For identifying issues without reference
- `design-report` - For comprehensive expert analysis
