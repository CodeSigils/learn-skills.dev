---
name: hackmd
description: >
  Interact with HackMD notes via the HackMD API. Use this skill whenever the user
  mentions HackMD, wants to create a note or document in HackMD, read or retrieve
  content from HackMD, search through their HackMD notes, update or edit a HackMD
  note, list notes, publish to HackMD, or work with HackMD team workspaces. Trigger
  on phrases like "HackMD", "create a doc in HackMD", "find my HackMD note about X",
  "update my HackMD note", "list my notes", "publish this to HackMD", "what does my
  HackMD note on X say", "save this to HackMD", "share on HackMD", or "HackMD team".
  Even casual mentions like "put this in HackMD" or "check my notes" in a HackMD
  context should trigger this skill.
---

# HackMD Skill

This skill enables Claude to interact with HackMD — a collaborative Markdown editor — using the HackMD REST API. You can create, read, update, list, delete, and search notes, both in the user's personal workspace and in team workspaces.

## Authentication Setup

HackMD requires an API Bearer Token. The token is stored in `~/.hackmd_config.json` for reuse across sessions.

**On first use (or if token is missing):**
1. Tell the user: "To connect to HackMD, I need your API token. You can get one at: Settings → API → Create API Token → Copy token."
2. Ask them to paste the token in the chat.
3. Save it by running:
   ```bash
   python3 /sessions/serene-practical-knuth/mnt/hackmd-skill/hackmd/scripts/hackmd_client.py --action save_token --token "<pasted-token>"
   ```
4. Confirm: "Your token has been saved. You won't need to paste it again."

**To check if token exists:**
```bash
python3 /sessions/serene-practical-knuth/mnt/hackmd-skill/hackmd/scripts/hackmd_client.py --action get_me
```
If this returns user info, you're authenticated. If it returns a token error, request a new token from the user.

## Using the Client Script

All API operations go through `hackmd_client.py`. It outputs JSON — parse it to extract what you need.

**General pattern:**
```bash
python3 /sessions/serene-practical-knuth/mnt/hackmd-skill/hackmd/scripts/hackmd_client.py --action <action> [options]
```

Read `references/api-reference.md` for the full list of actions and their parameters.

## Common Operations

### 1. List & Search Notes

List all personal notes:
```bash
python3 .../hackmd_client.py --action list_notes
```

To **search/filter** (HackMD API doesn't have search — filter client-side):
```bash
python3 .../hackmd_client.py --action list_notes | python3 -c "
import json, sys, re
query = 'architecture'   # ← change this
notes = json.load(sys.stdin)
matches = [n for n in notes if query.lower() in (n.get('title','') + n.get('tags','') + '').lower()]
print(json.dumps(matches, indent=2))
"
```

After listing, present results in a readable table:
```
| # | Title | Last Modified | Tags |
|---|-------|---------------|------|
| 1 | ...   | ...           | ...  |
```
Always show the note URL in the format `https://hackmd.io/<noteId>` so the user can open it.

### 2. Read a Note

```bash
python3 .../hackmd_client.py --action get_note --note-id <noteId>
```

The response includes `content` (Markdown), `title`, `tags`, `readPermission`, `writePermission`, `publishLink`.

Render the content in a readable way — don't just dump raw JSON.

### 3. Create a Note

```bash
python3 .../hackmd_client.py --action create_note \
  --title "My Note Title" \
  --content "# Heading\n\nContent here..." \
  --read-perm owner \
  --write-perm owner
```

Permission values: `owner`, `signed_in`, `guest` (read); `owner`, `signed_in` (write).

Default: `read=owner, write=owner` (private) unless the user specifies otherwise.

After creating, always share the URL: `https://hackmd.io/<noteId>`

### 4. Update a Note

```bash
python3 .../hackmd_client.py --action update_note \
  --note-id <noteId> \
  --content "# Updated content\n\n..." \
  --title "New title"   # optional
```

You can update content, title, and permissions independently. Only pass flags for what's changing.

### 5. Delete a Note

Ask the user to confirm before deleting — this is irreversible:
> "Are you sure you want to delete '`<note title>`'? This cannot be undone."

```bash
python3 .../hackmd_client.py --action delete_note --note-id <noteId>
```

### 6. Team Notes

First, list teams to get the teamPath:
```bash
python3 .../hackmd_client.py --action list_teams
```

Then use team operations:
```bash
# List team notes
python3 .../hackmd_client.py --action list_team_notes --team <teamPath>

# Create team note
python3 .../hackmd_client.py --action create_team_note \
  --team <teamPath> --title "..." --content "..."

# Get team note
python3 .../hackmd_client.py --action get_team_note \
  --team <teamPath> --note-id <noteId>

# Update team note
python3 .../hackmd_client.py --action update_team_note \
  --team <teamPath> --note-id <noteId> --content "..."

# Delete team note
python3 .../hackmd_client.py --action delete_team_note \
  --team <teamPath> --note-id <noteId>
```

## Output Guidelines

- **Always render content, not raw JSON.** Format results for reading.
- **Always include note URLs** so the user can open them in the browser.
- **For lists:** use a markdown table with title, last modified, and direct link.
- **For note content:** render the Markdown as-is (it will display correctly in Claude).
- **For errors:** explain what went wrong and what the user can do to fix it (e.g., "Note not found — check the note ID or make sure you have access").

## Error Handling

| Error | Cause | Action |
|-------|-------|--------|
| 401 Unauthorized | Token missing or expired | Ask user to paste a new token |
| 403 Forbidden | No permission on note | Inform user; suggest checking note permissions |
| 404 Not Found | Note/team doesn't exist | Confirm the ID with the user |
| 429 Too Many Requests | Rate limited | Wait a moment and retry |
| Connection error | Network issue | Retry; if persistent, check HackMD status |

## Tips

- Note IDs appear in HackMD URLs: `https://hackmd.io/<noteId>` or `https://hackmd.io/s/<noteId>`
- Tags are useful for organizing notes — include them when creating if the user mentions categories
- If the user pastes a HackMD URL, extract the note ID from it automatically
- When content is long, summarize and offer to show the full content if needed
