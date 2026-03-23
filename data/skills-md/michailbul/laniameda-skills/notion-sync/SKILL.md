---
name: notion-sync
description: >
  Sync a task to the laniameda Notion kanban board (upsert by name).
  Use whenever a task is created/updated/completed in pm/todos/.
metadata:
  requires:
    env:
      - NOTION_API_KEY
      - NOTION_TASKS_DB
---

# notion-sync

Sync a task to the laniameda Notion kanban board.
Use this whenever you create or update a task.md file in any pm/todos/ folder.

## When to use

- After creating a new task folder + task.md
- After updating the Status of an existing task
- After completing a task (status → Done)
- When asked to update the board

## Config

```bash
NOTION_KEY=$(cat ~/.config/notion/api_key)
DB_ID="316e9215-3d4b-8145-b6c7-c468224f2391"
```

## Sync a task (create or update by name)

```bash
python3 /root/.openclaw/workspace/skills/notion-sync/sync.py \
  --name "Task name" \
  --status "In Progress" \
  --agent "Lani" \
  --priority "High" \
  --department "Operations" \
  --area "Infrastructure" \
  --notes "Short context note"
```

## Status values
`Idea` | `Research` | `In Progress` | `Review` | `Done`

## Agent values
`Lani` | `Meda` | `Persey` | `Michael` | `All`

## Priority values
`High` | `Medium` | `Low`

## Department values (in priority order)
`Marketing` | `Dev` | `Operations`

## Area values
`Infrastructure` | `laniameda.gallery` | `RunMusic` | `Content & Marketing` | `Agent System` | `Website` | `AI Creator OS`

## Notes
- Script upserts by name — updates existing task if found, creates new one if not
- Always call this after writing to a task.md file
- Department is the most important field — Marketing is always top priority
