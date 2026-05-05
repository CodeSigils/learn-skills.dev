---
name: computer-use
description: Accurate desktop interaction for Windows with UI Automation, screen capture, image matching, keyboard and mouse control, verification, and recovery. Use when Codex or OpenClaw needs to operate desktop applications like a human, including launching apps, focusing windows, clicking controls, typing into fields, validating results, inspecting the UI tree, or recovering from ambiguous visual states. Prefer this skill when raw coordinates alone would be fragile, and use its Clawbot image-analysis fallback when the UI is visually complex or poorly exposed to accessibility APIs.
---

# Computer Use

Use this skill to operate Windows desktop apps through a strict loop:

1. Inspect the environment.
2. Identify the target window.
3. Build the strongest selector available.
4. Act.
5. Verify the result.
6. Recover or stop if verification fails.

This skill is for reliable desktop work, not blind macro playback. Prefer semantic targeting and verification over speed.

## Preflight

Install dependencies into your preferred Python environment first:

```powershell
pip install -r requirements.txt
```

Run these checks before the first action in a new environment or app:

```powershell
python scripts/doctor.py
```

Use the result to confirm:

- screen capture works
- the active window is readable
- the vision analyzer is available for Clawbot fallback
- monitor geometry looks sane

If the app is unfamiliar, inspect its UI tree before guessing selectors:

```powershell
python scripts/inspect_ui.py --active
```

Read [references/windows-uia.md](references/windows-uia.md) when you are unsure whether the app should be driven through `uia`, `win32`, or vision fallback.

## Main Loop

Use this loop for every non-trivial action:

1. Activate or identify the correct window.
2. Resolve the target with the selector ladder below.
3. Capture the pre-action evidence if the action matters.
4. Click, type, paste, or send the hotkey.
5. Verify the effect.
6. Retry with recovery only if the verification failed for a clear reason.

Do not chain many actions without verification in between unless the workflow is already proven stable.

## Selector Ladder

Build selectors in this order. Stop at the first level that is stable enough.

1. `window_handle` or `window_title` plus `automation_id`
2. `window_handle` or `window_title` plus `name` and `control_type`
3. Add `class_name` if the UI tree exposes multiple similar controls
4. `image_path` template matching in a bounded region
5. `relative_xy` inside a known window
6. `exact_coords` only as a last resort

Rules:

- Always anchor the selector to a specific window when possible.
- Prefer `automation_id` over visible text.
- Prefer visible text plus `control_type` over `class_name` alone.
- Narrow `region` before using template matching.
- Avoid `exact_coords` unless the window is fixed and short-lived.

## Target Discovery

Use the UI tree first. It is cheaper and more stable than image analysis.

Look for:

- the top-level window title
- the actual editable or clickable control type
- stable control names
- automation IDs
- class names only when the stronger fields are missing

Example: modern Notepad on this machine exposes the editor as `Document` with class `RichEditD2DPT`, not `Edit`. Do not assume legacy control types.

If the UI tree is incomplete:

1. Use a bounded image template.
2. If that is still ambiguous, ask Clawbot to analyze a screenshot.

## Using the Controller

Import the controller and selector models from the package:

```python
from computer_use import ComputerUseController, SelectorSpec, VerificationPlan
```

Construct one controller per task:

```python
controller = ComputerUseController()
```

Resolve a target explicitly when you want to inspect what the skill found:

```python
target = controller.resolve(
    SelectorSpec(
        window_title="Notepad",
        control_type="Document",
        class_name="RichEditD2DPT",
    )
)
print(target.source, target.point)
```

Use `click()` when the action is primarily spatial:

```python
result = controller.click(
    SelectorSpec(window_title="Calculator", name="7", control_type="Button"),
    verification=VerificationPlan(require_state_change=True),
)
```

Use `type_into()` when the action requires focus plus text entry:

```python
result = controller.type_into(
    SelectorSpec(window_title="Notepad", control_type="Document", class_name="RichEditD2DPT"),
    "computer-use benchmark",
    paste=True,
)
```

Use `hotkey()` when the app already has focus and the shortcut is the strongest interface:

```python
result = controller.hotkey(
    "ctrl",
    "c",
    verification=VerificationPlan(expected_clipboard="computer-use benchmark"),
)
```

## Typing Rules

Do not type blindly.

Before typing:

- ensure the correct window is active
- ensure the correct field has focus if focus is inspectable
- decide whether raw keystrokes or paste mode is safer

Prefer `paste=True` when:

- the string is long
- the string is sensitive
- an IME is active
- the app rewrites or localizes keystrokes
- deterministic entry matters more than human-like behavior

Prefer raw typing when:

- the app blocks paste
- the field reacts to per-key events
- the task explicitly needs human-like typing cadence

For deterministic validation after text entry, use clipboard verification or a follow-up select-all and copy pass instead of relying only on screenshot diffs.

## Verification

Pick the cheapest verification that proves success.

Available checks in `VerificationPlan`:

- `expected_window_title`
- `expected_focus_name`
- `expected_clipboard`
- `require_state_change`

Guidance:

- Use `expected_focus_name` before important typing.
- Use `expected_clipboard` after copy or select-all/copy validation.
- Use `require_state_change` after opening menus, dialogs, toggles, and navigation.
- Do not rely on `require_state_change` alone for text editors with subtle rendering changes.

Read [references/verification.md](references/verification.md) when you need stricter evidence or retry behavior.

## Recovery

When verification fails:

1. Re-focus the target window.
2. Re-resolve the selector.
3. Retry with a small click nudge around the resolved point.
4. Re-inspect the UI tree if the app may have changed structure.
5. Use Clawbot screenshot analysis if the screen state is unclear.
6. Stop after bounded retries instead of compounding bad state.

Do not let the skill drift into repeated blind clicking.

## Clawbot Fallback

Use Clawbot only when local targeting is not enough.

Good cases:

- the app is highly visual
- the UI tree is incomplete
- you need grounded reading of visible labels
- you need help narrowing the target region

Bad cases:

- replacing a strong UIA selector
- driving the entire workflow through screenshots alone
- repeated click retries without verification

Use the built-in helper:

```python
analysis = controller.describe_with_clawbot(
    prompt="Identify the primary action button. Quote its label exactly. If possible, return approximate JSON bbox coordinates."
)
print(analysis)
```

Treat Clawbot coordinates as hints, not proof. Verify the post-action state after using them.

The skill compresses screenshots before sending them to Clawbot:

- it downsizes oversized screenshots
- it keeps text-oriented screenshots on a higher-quality profile
- it prefers PNG for small sharp crops when that stays efficient
- it prefers 4:4:4 JPEG for larger screenshots when that cuts size materially

You still reduce token usage most by sending a bounded `region` instead of a full-screen image.

Read [references/complex-vision.md](references/complex-vision.md) for prompt guidance.

## Practical Recipes

### Recipe: Type into Notepad reliably

1. Inspect the UI tree once.
2. Target the editor as `Document` plus `RichEditD2DPT`.
3. Use `paste=True`.
4. Validate with `Ctrl+A`, `Ctrl+C`, and `expected_clipboard`.

### Recipe: Click a visible button by name

1. Start with `window_title`, `name`, and `control_type="Button"`.
2. Add `automation_id` if available.
3. Verify with `require_state_change` or the expected next window title.

### Recipe: Click a visual target in a weakly accessible app

1. Bind the action to a specific window.
2. Use `image_path` with a narrow `region`.
3. If the image is ambiguous, ask Clawbot to describe the screenshot and narrow the target.
4. Verify the result immediately.

## Scripts

- `scripts/doctor.py`
  Check imports, monitor layout, active window access, screenshot capture, and Clawbot fallback availability.
- `scripts/inspect_ui.py`
  Dump the current window tree so selectors are built from evidence instead of guesses.
- `scripts/bench.py`
  Run local benchmark scenarios. Use this to validate the skill against real apps before trusting a workflow.

## References

- [references/windows-uia.md](references/windows-uia.md)
- [references/verification.md](references/verification.md)
- [references/complex-vision.md](references/complex-vision.md)

## Non-Negotiable Rules

- Prefer selectors over coordinates.
- Prefer verification over optimism.
- Prefer paste mode over raw typing when IME state may interfere.
- Keep failure screenshots in `.artifacts/`.
- If the state is ambiguous, stop and inspect before acting again.
