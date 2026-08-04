# quick-healthcheck.ps1
# Self-contained Windows host health probe for Hermes cron runs.
# Run from MSYS bash via:
#   powershell -ExecutionPolicy Bypass -File "E:\.tmp\quick-healthcheck.ps1"
# Avoid passing complex PowerShell inline (with $_ / Where-Object blocks) via
# -Command — MSYS bash will mangle it. Always use -File with a script.
#
# Output: plain-text table covering disk, Ollama (matrix verdict), Hermes
# gateway process, and Telegram bot state.json. Exit 0 always (cron reporter
# decides silent vs alert from the content).
#
# Requires: powershell 5+; nothing else.

# --- 1. Disk ---
$disk = Get-PSDrive -PSProvider FileSystem -ErrorAction SilentlyContinue |
    Where-Object { $_.Used -gt 0 } |
    ForEach-Object {
        $pct = if ($_.Used + $_.Free -gt 0) {
            [math]::Round(($_.Used / ($_.Used + $_.Free)) * 100, 1)
        } else { 0 }
        [PSCustomObject]@{
            Drive    = $_.Name
            Used_GB  = [math]::Round($_.Used / 1GB, 1)
            Free_GB  = [math]::Round($_.Free / 1GB, 1)
            Total_GB = [math]::Round(($_.Used + $_.Free) / 1GB, 1)
            Pct      = $pct
        }
    }
Write-Host "== DISK =="
if ($disk) { $disk | Format-Table -AutoSize | Out-String } else { Write-Host "(none)" }

# --- 2. Ollama (4-state matrix) ---
$ollamaBin = @(
    "C:\Users\shrey\AppData\Local\Programs\Ollama\ollama.exe"
    "E:\_AI_Tools\ollama\OllamaSetup.exe"
) | Where-Object { Test-Path $_ }
$ollamaProc = Get-Process -Name ollama -ErrorAction SilentlyContinue
$ollamaSrv  = Get-Service -Name Ollama -ErrorAction SilentlyContinue
$ollamaPort = Get-NetTCPConnection -LocalPort 11434 -State Listen -ErrorAction SilentlyContinue
Write-Host "== OLLAMA =="
Write-Host "binary:    $($ollamaBin -join ', ')"
Write-Host "process:   $($ollamaProc.Id -join ',')"
Write-Host "service:   $($ollamaSrv.Status)"
Write-Host "port:      $(if ($ollamaPort) { 'LISTENING' } else { 'CLOSED' })"

# --- 3. Hermes gateway process ---
$hermesProc = Get-Process -Name python,pythonw -ErrorAction SilentlyContinue |
    Where-Object { $_.CommandLine -like "*hermes_cli*" -or $_.Path -like "*hermes*" }
Write-Host "== HERMES GATEWAY =="
if ($hermesProc) {
    $hermesProc | Select-Object Id, ProcessName, StartTime | Format-Table -AutoSize | Out-String
} else {
    Write-Host "(no python/hermes process)"
}

# --- 4. Telegram state.json ---
$stateFile = "C:\Users\shrey\AppData\Local\hermes\gateway_state.json"
Write-Host "== TELEGRAM =="
if (Test-Path $stateFile) {
    $state = Get-Content $stateFile -Raw | ConvertFrom-Json -ErrorAction SilentlyContinue
    if ($state.platforms.telegram) {
        $tg = $state.platforms.telegram
        Write-Host "state:       $($tg.state)"
        Write-Host "error_code:  $($tg.error_code)"
        Write-Host "error_msg:   $($tg.error_message)"
        Write-Host "updated_at:  $($tg.updated_at)"
    } else {
        Write-Host "(no telegram entry in state.json)"
    }
} else {
    Write-Host "(gateway_state.json missing)"
}
