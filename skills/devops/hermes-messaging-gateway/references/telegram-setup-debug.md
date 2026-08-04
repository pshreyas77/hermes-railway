# Telegram Bot Setup & Debugging (Windows)

## Complete Setup Flow

### 1. Create Bot via BotFather
```
1. Open Telegram → search @BotFather
2. /newbot → name: "HERMES_BOT" → username: "shrey_hermes_01_bot"
3. Save the token: 8863778824:AAFo-dFCpYX2_lUv_Ru-WBzOdD0e77z4tps
4. Get your user ID: message @userinfobot → copy ID (e.g., 8336840601)
```

### 2. Configure Hermes (`.env` first, then `config.yaml`)

**`.env` (simplest, recommended):**
```bash
TELEGRAM_BOT_TOKEN="8863778824:AAFo-dFCpYX2_lUv_Ru-WBzOdD0e77z4tps"
TELEGRAM_CHAT_ID="8336840601"
TELEGRAM_ALLOWED_USERS="8336840601"
```

**`config.yaml` (if `.env` doesn't work):**
```yaml
platforms:
  telegram:
    enabled: true
    extra:
      bot_token: "8863778824:AAFo-dFCpYX2_lUv_Ru-WBzOdD0e77z4tps"
      chat_id: "8336840601"
      admin_chat_ids: ['8336840601']
      dm_policy: open
```

### 3. Start Gateway (FRESH terminal!)
```powershell
hermes gateway run
```

### 4. Verify
```bash
# Check state
cat "$HOME/AppData/Local/hermes/gateway_state.json" | grep -A 5 telegram

# Should show: "state": "connected"
```

### 5. Test in Telegram
- Search `@shrey_hermes_01_bot`
- Send `/start` → should respond
- Send `/platforms` → should show `telegram: connected`

---

## Debugging Checklist (When "Not Working")

### Symptom: `The token '8863778824:***' was rejected`
**Cause**: Config has placeholder `***` instead of real token.

**Check both files:**
```bash
# .env
grep TELEGRAM_BOT_TOKEN "$HOME/AppData/Local/hermes/.env"

# config.yaml  
grep bot_token "$HOME/AppData/Local/hermes/config.yaml"
```

**Fix**: Both must have real token. In YAML, **token MUST be quoted**:
```yaml
bot_token: "8863778824:AAFo-dFCpYX2_lUv_Ru-WBzOdD0e77z4tps"
```

### Symptom: Gateway shows "retrying" but token is correct
**Cause**: Gateway process started before config update.

**Fix**: Kill and restart from **fresh terminal**:
```powershell
taskkill /F /IM python.exe
hermes gateway run
```

### Symptom: `hermes config set` doesn't work
**Cause**: Dotted key treated as env var, value gets masked.

**Fix**: Edit YAML directly (see above).

### Symptom: `/platforms` works but cron messages don't arrive
**Cause**: Cron job uses `deliver: telegram` but bot never received `/start`.

**Fix**: Message bot `/start` first, then cron deliveries work.

### Symptom: "chat not found" on send
**Cause**: `TELEGRAM_CHAT_ID` wrong or bot never messaged by user.

**Fix**: 
1. Message @userinfobot to get YOUR numeric ID
2. Add to `.env`: `TELEGRAM_CHAT_ID="YOUR_ID"`
3. Message bot `/start`
3. Test: `curl -s "https://api.telegram.org/bot<TOKEN>/sendMessage" -d "chat_id=YOUR_ID" -d "text=test"`

---

## Common Windows Gotchas

| Issue | Cause | Fix |
|-------|-------|-----|
| `.env` has `TOKEN="8863778824:***"` | PowerShell `>>` writes UTF-16 | Write via Python or bash |
| Gateway restart blocked | Running inside gateway process | Use separate terminal window |
| YAML token unquoted | Colon parsed as separator | Always quote: `bot_token: "123:ABC"` |
| Duplicate `bot_token` lines | First one wins (masked) | Keep only one |
| `hermes status` shows ✓ but not working | Only checks key EXISTS, not valid | Check `gateway_state.json` |

---

## Health Probe Script (for cron)
```powershell
# telegram-probe.ps1
$envPath = "$env:USERPROFILE\.hermes\.env"
$statePath = "$env:USERPROFILE\AppData\Local\hermes\gateway_state.json"

# 1. Check .env token shape
$token = (Get-Content $envPath) -match 'TELEGRAM_BOT_TOKEN' | ForEach-Object { $_ -replace '.*="(.*)"', '$1' }
if ($token -notmatch '^\d{8,12}:[A-Za-z0-9_-]{30,}$') {
    Write-Error ".env token is placeholder or malformed"
    exit 1
}

# 2. Check gateway state
$state = Get-Content $statePath -Raw | ConvertFrom-Json
if ($state.platforms.telegram.state -ne 'connected') {
    Write-Error "Gateway Telegram state: $($state.platforms.telegram.state)"
    exit 1
}

# 3. Verify with Telegram API
$resp = Invoke-RestMethod "https://api.telegram.org/bot$token/getMe"
if (-not $resp.ok) { Write-Error "API rejected token"; exit 1 }

Write-Host "Telegram: HEALTHY"
```

---

## File Locations
| File | Path |
|------|------|
| `.env` | `%USERPROFILE%\.hermes\.env` |
| `config.yaml` | `%USERPROFILE%\AppData\Local\hermes\config.yaml` |
| `gateway_state.json` | `%USERPROFILE%\AppData\Local\hermes\gateway_state.json` |
| Gateway logs | `%USERPROFILE%\AppData\Local\hermes\gateway-starts.log` |