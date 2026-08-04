# Hermes Telegram Gateway Setup for Vault Automation

## Overview

This documents the complete setup for Hermes Agent's Telegram gateway to enable remote access to your second brain from your phone. The gateway allows you to:

- Send prompts to Hermes from Telegram
- Receive cron job notifications (daily briefs, vault health checks, etc.)
- Query the vault remotely via `/search`, `/platforms`, `/tools` commands
- Delegate tasks to subagents from your phone

## The Problem We Solved

**Symptom**: Bot shows "connected" in `hermes status` but doesn't respond to messages. Gateway logs show: `The token '8863778824:***' was rejected by the server.`

**Root Cause**: The `.env` file and `config.yaml` contained a **placeholder token** (`8863778824:***`) instead of a real token from @BotFather. Hermes reports "✓ configured" because the *key exists*, but the *value is invalid*.

## Complete Setup Procedure

### 1. Create Bot via @BotFather

1. Open Telegram → search `@BotFather`
2. Send `/newbot`
3. Name: `HERMES_BOT` (or your choice)
4. Username: `shrey_hermes_01_bot` (must end in `bot`)
5. **Copy the token** — format: `8863778824:AAFo-dFCpYX2_lUv_Ru-WBzOdD0e77z4tps`

### 2. Get Your Chat ID

1. Message your new bot anything (e.g., `/start`)
2. Search `@userinfobot` → send `/start`
3. **Copy your User ID** (e.g., `8336840601`)

### 3. Configure Hermes (Both Files Required)

**File 1: `~/.hermes/.env`**
```bash
TELEGRAM_BOT_TOKEN="8863778824:AAFo-dFCpYX2_lUv_Ru-WBzOdD0e77z4tps"
TELEGRAM_CHAT_ID="8336840601"
TELEGRAM_ALLOWED_USERS="8336840601,8336840501,YOUR_ID_HERE"
```

**File 2: `~/.hermes/config.yaml`** (under `platforms.telegram.extra`)
```yaml
platforms:
  telegram:
    enabled: true
    extra:
      admin_chat_ids:
        - '8336840601'
        - '8336840501'
        - 'YOUR_ID_HERE'
      bot_token: "8863778824:AAFo-dFCpYX2_lUv_Ru-WBzOdD0e77z4tps"
      chat_id: '8336840601'
      dm_policy: open
```

**Critical**: Token must be **quoted** in YAML (`"token"`) because it contains colons.

### 4. Start Gateway (Fresh Terminal Required)

```powershell
# Stop any running gateway
hermes gateway stop

# Start fresh (in NEW terminal window)
hermes gateway run
```

### 5. Test in Telegram

1. Open Telegram → search `@shrey_hermes_01_bot`
2. Send `/start` → should respond
3. Send `/platforms` → should show `telegram: connected`
4. Send `/tools` → lists available tools
5. **Set home channel**: Send `/sethome` in the chat

### 6. Make Permanent (Windows Service)

```powershell
# Run as Administrator
hermes gateway install
hermes gateway start
hermes gateway status
```

This creates a Windows startup item that auto-starts the gateway on boot.

## Common Issues & Fixes

| Symptom | Cause | Fix |
|---------|-------|-----|
| `The token '...:***' was rejected` | Placeholder in `.env` or `config.yaml` | Update both files with real token |
| `404 Not Found` on `/getMe` | Invalid token | Re-create bot via @BotFather → `/token` |
| `403 Forbidden: bot can't send messages to bot` | Sending to bot's own ID | Use your User ID from `@userinfobot` |
| `400 Bad Request: chat not found` | User hasn't messaged bot | Send `/start` to bot first |
| Gateway connected but no response | User ID not in allowlist | Add your ID to `TELEGRAM_ALLOWED_USERS` and `admin_chat_ids` |
| `Conflict: terminated by other getUpdates` | Multiple polling instances | Only one gateway process should run |

## Cron Job Integration

The gateway enables cron job delivery to Telegram. Example cron jobs that deliver to Telegram:

```bash
# Daily briefing at 7 AM
cronjob action=create schedule="0 7 * * *" \
  prompt="Generate daily briefing from vault updates" \
  skills=["vault-research-synthesis"] \
  deliver="telegram"

# Vault health check hourly
cronjob action=create schedule="0 * * * *" \
  script="health-check" \
  deliver="telegram"
```

## Security Notes

- **Never paste real tokens in chat** — they persist in history
- Use the script method: `python -c "..."` to write tokens directly to `.env`
- Bot tokens are like passwords — anyone with the token controls the bot
- Regenerate via @BotFather → `/token` if compromised

## Verification Commands

```bash
# Check token validity
curl -s "https://api.telegram.org/bot<YOUR_TOKEN>/getMe"

# Check gateway state
cat ~/.hermes/gateway_state.json | jq .platforms.telegram

# Check allowlist
grep TELEGRAM_ALLOWED_USERS ~/.hermes/.env

# Check config
grep -A 10 "platforms.telegram" ~/.hermes/config.yaml
```

## Integration with Vault Workflow

Once set up, the Telegram bot becomes your remote interface to the second brain:

| Command | Purpose |
|---------|---------|
| `/start` | Initialize chat |
| `/sethome` | Set this chat for cron deliveries |
| `/platforms` | Verify connection |
| `/tools` | List available tools |
| `/search "topic" in wiki` | Search vault |
| `/understand-knowledge .` | Analyze vault as wiki |
| Custom prompts | Delegate research/tasks |

## Maintenance

- **Token rotation**: @BotFather → `/token` → update both files → `hermes gateway restart`
- **Add users**: Add User IDs to `TELEGRAM_ALLOWED_USERS` and `admin_chat_ids`
- **Monitor**: Check `hermes gateway status` and `gateway_state.json` periodically
- **Logs**: `hermes logs gateway` for debugging