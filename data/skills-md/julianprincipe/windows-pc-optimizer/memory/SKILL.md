---
name: memory
description: >
  Reduce Windows RAM usage at idle by auditing and cleaning up startup programs and
  unnecessary background services. Use when the user has high memory usage with nothing
  open, slow performance due to RAM pressure, or wants to know what's eating their RAM.
  Trigger for: "too much RAM used", "15GB used at idle", "RAM always full", "what's
  using my memory", "reduce background processes", "too many things running".
---

# /optimize:memory — RAM + Background Process Cleanup

Identifies what's consuming RAM at idle and reduces it by cleaning up startup items
and setting unnecessary services to manual start.

---

## Step 1 — Measure before

Run `scripts/02_benchmark.ps1 -Label "pre"` as Administrator.

---

## Step 2 — Capture current state

Run `scripts/01_diagnose.ps1` as Administrator.

Focus on:
- `ram_info.json` — total, free, used %
- `processes.json` — top processes by RAM
- `services.json` — running services with RAM
- `startup_items.json` — everything loading at boot

---

## Step 3 — Ask about use case

Before making any changes, ask:

**What software do you actively use on this machine?**
Focus on: audio interfaces, DAWs, game launchers, dev tools, remote access, backup
tools, cloud sync, communication apps.

**What do you need available immediately when the PC starts?**
vs. what can open when you actually use it?

This determines what stays in startup vs. what becomes manual.

---

## Step 4 — Analyze and propose

Group what you find into three buckets and present it to the user:

**KEEP in startup** — essential to the user's stated workflow
(e.g. Plex if running as a server, Parsec if used for remote access, audio interface
notifiers, Defender/SecurityHealth)

**REMOVE from startup** — loads at boot but user launches manually anyway
(e.g. Spotify, Discord, Epic Games Launcher, EA Desktop, Notion, Slack,
backup tools that can sync periodically)

**SET SERVICE TO MANUAL** — service starts when needed, not always
Present each with: what it does, RAM it's using, why it's safe to set to manual.

Services safe to disable outright (not just manual):
- `DiagTrack` — Windows telemetry, no user benefit
- `SysMain` (Superfetch) — irrelevant with SSD + 16GB+ RAM
- Xbox services (if not using Xbox features): XblAuthManager, XblGameSave,
  XboxGipSvc, XboxNetApiSvc, BcastDVRUserService
- `RemoteRegistry` — security risk, no use case for most users
- `TabletInputService` — only needed with touchscreen
- `Fax` — unless there's a fax machine

Wait for explicit approval on the list before making any changes.

---

## Step 5 — Execute

**Back up startup registry first:**
```powershell
reg export "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" backup_hkcu_run.reg /y
reg export "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" backup_hklm_run.reg /y
```

**Remove approved startup items:**
```powershell
Remove-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" -Name "AppName"
```

**Set approved services to Manual:**
```powershell
sc.exe config ServiceName start= demand
sc.exe stop  ServiceName
```

**Set approved services to Disabled:**
```powershell
sc.exe config ServiceName start= disabled
sc.exe stop  ServiceName
```

**Kill processes from removed startup items** (so the change takes effect now
without needing a reboot):
```powershell
Stop-Process -Name "ProcessName" -Force -ErrorAction SilentlyContinue
```

---

## Step 6 — Measure after

Run `scripts/02_benchmark.ps1 -Label "post"` — prints the delta automatically.

Note: the full RAM benefit shows after a clean reboot, since some processes that were
already running stay in memory until then.

---

## References
- `scripts/01_diagnose.ps1`
- `scripts/02_benchmark.ps1`
- `scripts/00_safety.ps1` (run first if making many changes)
