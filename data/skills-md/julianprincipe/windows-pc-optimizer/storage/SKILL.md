---
name: storage
description: >
  Targeted disk space cleanup for Windows. Use when the user only wants to free up
  space on their drives without touching startup, services, or system settings.
  Trigger for: "free up disk space", "my C: is full", "clean up my SSD",
  "delete temp files", "what's eating my disk", "recover space on Windows".
---

# /optimize:storage — Disk Space Cleanup

Analyzes what's using space on your drives and recovers it safely, without touching
services, startup items, or system configuration.

---

## Step 1 — Measure before

Run `scripts/02_benchmark.ps1 -Label "pre"` as Administrator.

---

## Step 2 — Scan

Run `scripts/01_diagnose.ps1` as Administrator.

Focus on these fields from the output:
- `C_Free_GB` — current free space
- `CleanupPotential_MB` — recoverable from known safe locations
- `TopCleanupItems` — what's biggest
- `DevCaches_MB` — dev caches if present
- `top_folders_c.json` — largest folders on C: for context

---

## Step 3 — Show the user what was found

Present a table like:

```
CLEANUP CANDIDATES
  %TEMP%                     X.X GB   — safe to delete
  C:\Windows\Temp            X.X GB   — safe to delete
  WinSxS (DISM cleanup)      ~X GB    — safe (keeps rollback for current patch)
  Windows Update cache       X.X GB   — safe to delete
  C:\AMD / C:\NVIDIA         X.X GB   — driver installer leftovers
  Chrome cache               X.X GB   — safe to delete
  npm cache                  X.X GB   — safe (recreates automatically)
  pip cache                  X.X GB   — safe (recreates automatically)
  ...
TOTAL POTENTIAL: ~X GB
```

Ask if there's anything they want to skip.

---

## Step 4 — Execute cleanup

Stop services that lock files before cleaning:
```powershell
Stop-Service wuauserv, BITS, WSearch, DiagTrack -Force
```

Clean in this order:

**Safe, always clean:**
1. `%TEMP%` (user temp)
2. `C:\Windows\Temp`
3. `C:\tmp` (if exists)
4. `C:\Windows\SoftwareDistribution\Download`
5. `C:\AMD`, `C:\NVIDIA`, `C:\Intel` (driver leftovers, if they exist)
6. Windows Error Reporting: `%LOCALAPPDATA%\Microsoft\Windows\WER\ReportArchive` + ReportQueue
7. Browser caches (kill browsers first: `taskkill /f /im chrome.exe` etc.)
8. Spotify cache (`%LOCALAPPDATA%\Spotify\Storage`)
9. Steam download/temp cache
10. Thumbnail and icon cache (Explorer)
11. Font cache DAT files (stop FontCache service first)

**Dev caches (only if dev tools are present on this machine):**
- npm: `npm cache clean --force` or delete `%APPDATA%\npm-cache`
- pnpm: `pnpm store prune`
- pip: `pip cache purge` or delete `%LOCALAPPDATA%\pip\Cache`
- cargo: delete `%USERPROFILE%\.cargo\registry\cache` (src/ stays)
- gradle: delete `%USERPROFILE%\.gradle\caches`
Ask before cleaning dev caches — confirm the user has dev tools installed.

**DISM WinSxS cleanup (takes 10-30 min, significant space):**
```powershell
DISM /Online /Cleanup-Image /StartComponentCleanup
DISM /Online /Cleanup-Image /StartComponentCleanup /ResetBase
```
`/ResetBase` removes rollback for already-installed updates. Safe unless you
plan to uninstall recent Windows updates. Ask before running.

**Disk Cleanup (cleanmgr):**
Set StateFlags0099 = 2 for all categories, then run `cleanmgr /sagerun:99`.
⚠️ Monitor it — if CPU usage freezes at an exact value for 10+ minutes,
kill the cleanmgr process. The space it found is already counted.

**Delivery Optimization cache:**
```powershell
Delete-DeliveryOptimizationCache -Force
```

Restart services after:
```powershell
Start-Service wuauserv, BITS, WSearch
Start-Process explorer.exe
```

---

## Step 5 — Large software audit (optional)

If after cleanup space is still tight, look at `installed_software.json` from the
diagnosis and `top_folders_c.json` for large items to discuss with the user:

- Large games → move to secondary drive or uninstall
- Multiple versions of the same software → keep only the latest
- Audio sample libraries → can usually be moved to a secondary drive
- Old Docker images / WSL distros → `docker system prune`, `wsl --unregister`

Never uninstall anything without explicit user confirmation.

---

## Step 6 — Measure after

Run `scripts/02_benchmark.ps1 -Label "post"` — prints the delta automatically.

---

## References
- `scripts/01_diagnose.ps1`
- `scripts/02_benchmark.ps1`
