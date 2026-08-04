# Hermes Gateway Health Check (Windows)
# One-shot triage script for cron-driven health checks.
# Avoids the MSYS-bash → PowerShell `$_` corruption class of bug by running as a .ps1 file.
#
# Usage:
#   powershell -NoProfile -ExecutionPolicy Bypass -File health-check.ps1
#
# Outputs a structured report and exits 0 if healthy, 1 if any check failed.

$ErrorActionPreference = 'Continue'
$Report = New-Object System.Collections.ArrayList
$Failed = $false

function Check($Name, $Script, $Severity = 'info') {
    $Report.Add([pscustomobject]@{
        Name = $Name
        Status = if (& $Script) { 'OK' } else { 'FAIL' }
        Severity = $Severity
    }) | Out-Null
}

# --- 1. Gateway process ---
$Report.Add([pscustomobject]@{
    Name = 'Gateway process (PID)'
    Status = if (Get-Process hermes -ErrorAction SilentlyContinue) { 'OK' } else { 'FAIL' }
    Severity = 'critical'
}) | Out-Null

# --- 2. Logged-in Telegram session (gateway recent log) ---
$logDir = Join-Path $env:USERPROFILE 'AppData\Local\hermes\logs'
$logFile = Join-Path $logDir 'gateway.log'
if (Test-Path $logFile) {
    $recentErrorCount = (Select-String -Path $logFile -Pattern 'ERROR' -ErrorAction SilentlyContinue |
        Select-Object -Last 200).Count
    $Report.Add([pscustomobject]@{
        Name = "Gateway log ERRORs (last 200 lines)"
        Status = if ($recentErrorCount -eq 0) { 'OK' } else { "FAIL ($recentErrorCount errors)" }
        Severity = 'warning'
    }) | Out-Null
} else {
    $Report.Add([pscustomobject]@{
        Name = 'Gateway log file'
        Status = 'MISSING'
        Severity = 'warning'
    }) | Out-Null
}

# --- 3. Telegram adapter state (proxy: .env says configured; gateway logs say whether it can talk to Telegram) ---
$envFile = Join-Path $env:USERPROFILE 'AppData\Local\hermes\.env'
$telegramConfigured = $false
if (Test-Path $envFile) {
    $content = Get-Content $envFile -Raw -Encoding UTF8
    if ($content -match 'TELEGRAM_BOT_TOKEN=') {
        $telegramConfigured = $true
    }
}
$Report.Add([pscustomobject]@{
    Name = 'Telegram configured in .env'
    Status = if ($telegramConfigured) { 'OK' } else { 'FAIL' }
    Severity = 'info'
}) | Out-Null

# Recent gateway error mentioning Telegram = adapter actually failing
$telegramErrors = 0
if (Test-Path $logFile) {
    $telegramErrors = (Select-String -Path $logFile -Pattern 'Failed to connect to Telegram' -ErrorAction SilentlyContinue |
        Select-Object -Last 50).Count
}
$Report.Add([pscustomobject]@{
    Name = 'Telegram adapter errors (last 50 log matches)'
    Status = if ($telegramErrors -eq 0) { 'OK' } else { "FAIL ($telegramErrors errors)" }
    Severity = 'critical'
}) | Out-Null

# --- 4. Ollama (optional local LLM) ---
$ollama = Get-Process ollama -ErrorAction SilentlyContinue
$Report.Add([pscustomobject]@{
    Name = 'Ollama process'
    Status = if ($ollama) { 'OK' } else { 'FAIL' }
    Severity = 'info'
}) | Out-Null

# Port 11434 reachable?
$port11434 = Get-NetTCPConnection -LocalPort 11434 -State Listen -ErrorAction SilentlyContinue
$Report.Add([pscustomobject]@{
    Name = 'Ollama port 11434 listening'
    Status = if ($port11434) { 'OK' } else { 'FAIL' }
    Severity = 'info'
}) | Out-Null

# --- 5. Disk space on user-visible drives (warn if any drive >90% full) ---
$drives = Get-PSDrive -PSProvider FileSystem | Where-Object { $_.Used -gt 0 }
foreach ($drv in $drives) {
    $usedPct = [math]::Round(($drv.Used / ($drv.Used + $drv.Free)) * 100, 1)
    $Report.Add([pscustomobject]@{
        Name = "Drive $($drv.Root): usage"
        Status = if ($usedPct -gt 90) { "FAIL ($usedPct%)" } else { "OK ($usedPct%)" }
        Severity = 'warning'
    }) | Out-Null
}

# --- Render ---
$Report | Format-Table -AutoSize
$Failed = $Report | Where-Object { $_.Status -like 'FAIL*' -or $_.Status -eq 'MISSING' } | Where-Object { $_.Severity -ne 'info' }

if ($Failed.Count -gt 0) {
    Write-Host "`nCRITICAL failures: $($Failed.Count)" -ForegroundColor Red
    $Failed | Format-Table -AutoSize
    exit 1
} else {
    Write-Host "`nAll critical checks passed." -ForegroundColor Green
    exit 0
}
