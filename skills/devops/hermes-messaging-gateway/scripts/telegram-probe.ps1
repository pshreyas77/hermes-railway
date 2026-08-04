# Hermes Telegram Deep Probe (Windows)
# Companion to health-check.ps1 — drills into the Telegram adapter to identify
# the SPECIFIC failure mode (placeholder token vs revoked token vs server error vs
# chat_id mismatch). Use when the broad health-check reports "Telegram errors".
#
# Usage:
#   powershell -NoProfile -ExecutionPolicy Bypass -File telegram-probe.ps1
#
# Exits 0 if Telegram is healthy, 1 otherwise. Prints a one-line root-cause verdict.
#
# Probes (in order, stops at first failure):
#   1. gateway_state.json platforms.telegram.state — running/polling vs retrying/error
#   2. Token shape regex on TELEGRAM_BOT_TOKEN in .env — catches the placeholder
#      pitfall (`NNN:***` literally pasted in) without making a network call
#   3. /getMe against api.telegram.org using the secret from .env — source of truth
#      (404 = placeholder, 401 = revoked, ok=true = healthy)
#
# Avoids the MSYS-bash → PowerShell `$_` corruption class of bug by being a .ps1 file.

$ErrorActionPreference = 'Continue'

# --- Locate .env and gateway_state.json under $env:LOCALAPPDATA/hermes ---
$hermesDir = Join-Path $env:LOCALAPPDATA 'hermes'
$envFile   = Join-Path $hermesDir '.env'
$stateFile = Join-Path $hermesDir 'gateway_state.json'

# --- 1. gateway_state.json: telegram adapter state ---
$tgState = 'unknown'
$tgErr   = ''
if (Test-Path $stateFile) {
    try {
        $state = Get-Content $stateFile -Raw -Encoding UTF8 | ConvertFrom-Json
        if ($state.platforms -and $state.platforms.telegram) {
            $tgState = $state.platforms.telegram.state
            $tgErr   = $state.platforms.telegram.error_message
        }
    } catch {
        Write-Host "[1] gateway_state.json unreadable: $_" -ForegroundColor Yellow
    }
} else {
    Write-Host "[1] gateway_state.json MISSING at $stateFile — gateway not running?" -ForegroundColor Yellow
}

Write-Host "[1] telegram state: $tgState"
if ($tgState -ne 'running' -and $tgState -ne 'polling') {
    Write-Host "    VERDICT: Telegram adapter not in a healthy state. error: $tgErr" -ForegroundColor Red
    # Fall through to step 2/3 to identify root cause before exiting.
}

# --- 2. Token shape self-check (no network) ---
$token = $null
if (Test-Path $envFile) {
    $content = Get-Content $envFile -Raw -Encoding UTF8
    # Extract TELEGRAM_BOT_TOKEN="..." or TELEGRAM_BOT_TOKEN=...
    $m = [regex]::Match($content, '(?m)^TELEGRAM_BOT_TOKEN\s*=\s*"?([^"\r\n]+)"?')
    if ($m.Success) { $token = $m.Groups[1].Value }
}

if (-not $token) {
    Write-Host "[2] TELEGRAM_BOT_TOKEN not set in .env" -ForegroundColor Red
    Write-Host "    VERDICT: missing secret. Run: hermes secrets set TELEGRAM_BOT_TOKEN '<real-token>'" -ForegroundColor Red
    exit 1
}

# Valid token shape: 8-12 digits, colon, 30+ chars of [A-Za-z0-9_-]
if ($token -notmatch '^\d{8,12}:[A-Za-z0-9_-]{30,}$') {
    if ($token -like '*:\*\*\*' -or $token -like '*:***') {
        Write-Host "[2] .env token ends in :*** — placeholder, not a real secret" -ForegroundColor Red
        Write-Host "    VERDICT: .env holds placeholder. Reissue via @BotFather -> /token and save the REAL token." -ForegroundColor Red
    } else {
        Write-Host "[2] .env token has wrong shape: '$token' (length=$($token.Length))" -ForegroundColor Red
        Write-Host "    VERDICT: malformed secret. Expected pattern: <digits>:<30+ alphanumeric chars>" -ForegroundColor Red
    }
    exit 1
}

Write-Host "[2] token shape OK ($($token.Length) chars)"

# --- 3. /getMe — source of truth ---
try {
    $resp = Invoke-RestMethod -Uri "https://api.telegram.org/bot$token/getMe" -Method Get -TimeoutSec 10
    if ($resp.ok -eq $true) {
        Write-Host "[3] /getMe OK — bot: @$($resp.result.username) (id $($resp.result.id))" -ForegroundColor Green
        Write-Host "    VERDICT: Telegram healthy." -ForegroundColor Green
        exit 0
    } else {
        Write-Host "[3] /getMe returned ok=$($resp.ok), error_code=$($resp.error_code), description=$($resp.description)" -ForegroundColor Red
        switch ($resp.error_code) {
            404 { Write-Host "    VERDICT: token rejected (404). .env still has a placeholder despite passing the shape check." -ForegroundColor Red }
            401 { Write-Host "    VERDICT: token revoked. Reissue via @BotFather -> /token." -ForegroundColor Red }
            default { Write-Host "    VERDICT: Telegram API error $(([string]$resp.error_code))." -ForegroundColor Red }
        }
        exit 1
    }
} catch {
    Write-Host "[3] /getMe network failure: $_" -ForegroundColor Red
    Write-Host "    VERDICT: cannot reach api.telegram.org. Check network/firewall." -ForegroundColor Red
    exit 1
}
