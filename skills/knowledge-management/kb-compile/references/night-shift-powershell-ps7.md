# Night Shift Pipeline — PowerShell 7.5 Compatibility Notes

**Date:** 2026-07-13  
**Context:** All 3 Night Shift cron jobs (Scout/Refinery/Editor) were failing since ~Jul 12 after a PS version change. Root cause: PowerShell 7.5 syntax incompatibilities.

---

## Issue 1: Multi-Value Switch Cases

**Problem:** PowerShell 7.5 no longer accepts comma-separated values in `switch` statement cases.

**Wrong (PowerShell < 7.5 style):**
```powershell
switch ($Ext) {
    ".html", ".htm" { return "article" }
    ".mp4", ".mkv", ".avi" { return "video" }
}
```

**Correct (PowerShell 7.5):**
```powershell
switch ($Ext) {
    {".html"} { return "article" }
    {".htm"} { return "article" }
    {".mp4"} { return "video" }
    {".mkv"} { return "video" }
    {".avi"} { return "video" }
}
```

**Affected files:** `scout-run.ps1` (fixed 2026-07-13).

---

## Issue 2: Date Subtraction Ambiguity

**Problem:** `Get-Date - $StartTime` is ambiguous in PS7 — it parses `-$StartTime` as the `-Date` parameter value (a string `-` followed by the datetime object).

**Wrong:**
```powershell
$StartTime = Get-Date
# Later:
Write-Host "Duration: $([Math]::Round((Get-Date - $StartTime).TotalSeconds, 1)) seconds"
```

**Correct:**
```powershell
$StartTime = Get-Date
# Later:
Write-Host "Duration: $([Math]::Round(((Get-Date) - $StartTime).TotalSeconds, 1)) seconds"
```

**Affected files:** `scout-run.ps1`, `refinery-run.ps1`, `editor-run.ps1` (all fixed).

---

## Issue 3: $StartTime Not Declared

**Problem:** `refinery-run.ps1` and `editor-run.ps1` used `$StartTime` in the duration calculation but never declared it. Only `scout-run.ps1` had it defined.

**Fix:** Add `$StartTime = Get-Date` immediately after `$ErrorActionPreference = "Stop"`.

---

## Issue 4: Missing Directories

**Problem:** `0-raw/sources/archived/` did not exist, causing `refinery-run.ps1` to fail when trying to archive processed files.

**Created:**
- `0-raw/sources/archived/`
- `1-desk/_quarantine/`
- `briefings/`

---

## Verification Commands

```bash
# Test Scout
pwsh -File E:\_Knowledge\ObsidianVault\playbooks\scout-run.ps1 -VaultPath "E:\_Knowledge\ObsidianVault"

# Test Refinery  
pwsh -File E:\_Knowledge\ObsidianVault\playbooks\refinery-run.ps1 -VaultPath "E:\_Knowledge\ObsidianVault"

# Test Editor
pwsh -File E:\_Knowledge\ObsidianVault\playbooks\editor-run.ps1 -VaultPath "E:\_Knowledge\ObsidianVault"

# Check pipeline health
grep -A5 "Last Run" ~/.hermes/cron/*.json 2>/dev/null || cronjob(action='list')
```

---

## Pipeline Architecture Summary

| Cron ID | Stage | Script | Schedule | Status |
|---------|-------|--------|----------|--------|
| `b60bd1a2ba42` | Scout | `scout-run.ps1` | 23:30 IST | ✅ Fixed |
| `e5fa48dbb046` | Refinery | `refinery-run.ps1` | 03:00 IST | ✅ Fixed |
| `8e3ee9ca65d5` | Editor | `editor-run.ps1` | 06:00 IST | ✅ Fixed |
| `5981bc3a96fd` | Audit | `audit-run.ps1` | Sun 22:00 | ⚠️ May also need PS7 fixes (untested) |

The Audit run (`audit-run.ps1`) was not tested — it may have the same PS7.5 issues. Test before next Sunday.

---

## Related Skills

- `kb-compile` — compiles 0-raw/ → 02 - AREAS/ (parallel to Night Shift pipeline)
- `kb-healthcheck` — Hermes-native weekly audit (does NOT use PowerShell, always works)
- `obsidian` — vault structure and Night Shift pipeline overview