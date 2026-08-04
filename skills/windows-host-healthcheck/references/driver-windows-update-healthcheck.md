# Driver & Windows Update Healthcheck Reference

## Overview
This reference documents the driver version checking and Windows Update probing patterns used during the Aug 3, 2026 session. These checks are useful for `windows-host-healthcheck` cron jobs to detect stale drivers or pending updates that may affect system stability or Hermes performance.

---

## NVIDIA GPU Driver Check

### Current Status (Aug 3, 2026)
- **GPU:** NVIDIA GeForce GTX 1650 with Max-Q Design
- **Driver Version:** 32.0.16.1088
- **Driver Date:** 2026-07-22 (12 days old)
- **Status:** ✅ **Current** — Game Ready / Studio driver, late July 2026

### Check Command
```powershell
# Via nvidia-smi (fastest)
nvidia-smi --query-gpu=driver_version,name --format=csv,noheader

# Via WMI (more detailed)
Get-WmiObject Win32_PnPSignedDriver | Where-Object {$_.DeviceClass -eq 'Display'} | Select-Object DeviceName, DriverVersion, DriverDate
```

### Thresholds
- **Current:** < 30 days old
- **Warning:** 30-90 days
- **Critical:** > 90 days or known security vulnerability

---

## Intel UHD Graphics (iGPU) Check

### Current Status (Aug 3, 2026)
- **GPU:** Intel(R) UHD Graphics (10th gen Comet Lake)
- **Driver Version:** 31.0.101.2140
- **Driver Date:** 2025-11-05 (~9 months old)
- **Status:** ⚠️ **Outdated** — Latest for 10th gen is 31.0.101.5xxx or 32.x (mid-2026)

### Check Command
```powershell
Get-WmiObject Win32_PnPSignedDriver | Where-Object {$_.DeviceClass -eq 'Display'} | Select-Object DeviceName, DriverVersion, DriverDate
# Look for "Intel" in DeviceName
```

### Thresholds
- **Current:** < 60 days
- **Warning:** 60-180 days
- **Critical:** > 180 days (affects video decode, multi-monitor, iGPU compute)

### Update Source
- Intel DCH Drivers: https://www.intel.com/content/www/us/en/download/780504/intel-graphics-windows-dch-drivers.html
- Or via Windows Update (optional driver)

---

## Realtek Audio Driver Check

### Current Status (Aug 3, 2026)
- **Pending Updates via Windows Update:**
  - Realtek AudioProcessingObject Driver Update (13.5809.2469.844)
  - Realtek SoftwareComponent Driver Update (1.0.986.0)
- **Status:** 🔄 **Updates Available**

### Check Command
```powershell
# Via Windows Update COM API (see check_updates.ps1)
# Or manually: Settings → Windows Update → View optional updates
```

### Thresholds
- Audio driver updates rarely critical but fix glitches, microphone issues, codec support
- Install when convenient (next reboot)

---

## Windows Update Probe

### Current Status (Aug 3, 2026)
- **Last Search:** 8/3/2026 9:40:17 AM
- **Last Install:** 8/2/2026 6:46:29 AM
- **Pending Updates:** 3 (Defender definitions + 2 Realtek audio)

### Check Command
```powershell
# Last search/install dates
(New-Object -ComObject Microsoft.Update.AutoUpdate).Results

# Pending updates (requires .ps1 file due to MSYS bash mangling)
# See E:/_Dev_Tools/check_updates.ps1
```

### Thresholds
- **Critical:** Security updates pending > 7 days
- **Warning:** Driver updates pending > 30 days
- **Info:** Feature updates pending (Windows 11 24H2, etc.)

---

## Automated Healthcheck Integration

Add to `windows-host-healthcheck` cron probes:

```powershell
# Probe: Driver Freshness
$drivers = Get-WmiObject Win32_PnPSignedDriver | Where-Object {$_.DeviceClass -eq 'Display'}
foreach ($d in $drivers) {
    $ageDays = (Get-Date) - [DateTime]::ParseExact($d.DriverDate.Substring(0,8), 'yyyyMMdd', $null)
    $status = if ($ageDays -lt 30) { '✅' } elseif ($ageDays -lt 90) { '⚠️' } else { '❌' }
    Write-Host "$status $($d.DeviceName): v$($d.DriverVersion) ($($ageDays.Days) days)"
}

# Probe: Windows Update Pending
$session = New-Object -ComObject Microsoft.Update.Session
$searcher = $session.CreateUpdateSearcher()
$results = $searcher.Search('IsInstalled=0')
$pending = $results.Updates.Count
if ($pending -gt 0) {
    Write-Host "⚠️ $pending Windows updates pending"
    $results.Updates | ForEach-Object { Write-Host "  - $($_.Title)" }
} else {
    Write-Host "✅ Windows up to date"
}
```

---

## Related Files
- `E:/_Dev_Tools/check_drivers.ps1` — Display driver version/date checker
- `E:/_Dev_Tools/check_updates.ps1` — Windows Update pending checker
- `scripts/quick-healthcheck.ps1` — Main healthcheck script (add driver probes here)