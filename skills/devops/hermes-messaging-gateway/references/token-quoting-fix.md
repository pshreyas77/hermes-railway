# Telegram Bot Token Quoting Fix (Windows)

## Problem
Hermes Gateway fails to connect to Telegram with error:
```
The token `8863778824:***` was rejected by the server.
```

Even after updating `.env` with a real token, the gateway still uses the masked placeholder.

## Root Cause
Two configuration sources conflict:
1. `.env` — updated correctly with real token
2. `config.yaml` — still has placeholder `bot_token: 8863778824:***`

The gateway reads from `config.yaml` first. Additionally, **YAML requires quoted strings for tokens containing colons**. Unquoted `bot_token: 8863778824:AAF...` is parsed as a key-value pair (`8863778824` = key, `AAF...` = value).

## Solution

### 1. Fix config.yaml directly (not via `hermes config set`)
```bash
# Open config.yaml in editor
notepad "%USERPROFILE%\.hermes\config.yaml"

# Find the telegram section and change:
# bot_token: 8863778824:***
# To:
bot_token: "8863778824:AAFo-dFCpYX2_lUv_Ru-WBzOdD0e77z4tps"
#                                                    ↑                    ↑
#                                            REQUIRED quotes for tokens with colons
```

### 2. Also update .env (for other tools)
```bash
TELEGRAM_BOT_TOKEN="8863778824:AAFo-dFCpYX2_lUv_Ru-WBzOdD0e77z4tps"
```

### 3. Restart Gateway from FRESH terminal
```powershell
# In a NEW PowerShell/cmd window (not one running gateway):
hermes gateway stop
hermes gateway run
```

**Critical**: Cannot restart from inside a running gateway process — SIGTERM propagates to child shell.

## Verification
```bash
# Check gateway state
cat "$HOME/AppData/Local/hermes/gateway_state.json" | grep -A 5 telegram
# Should show: "state": "connected"

# Test bot directly
curl -s "https://api.telegram.org/bot<TOKEN>/getMe"
# Should return {"ok":true,"result":{"username":"your_bot",...}}
```

## Common Pitfalls
| Pitfall | Symptom | Fix |
|---------|---------|-----|
| `hermes config set platforms.telegram.extra.bot_token "TOKEN"` | Writes unquoted or masked | Edit YAML directly |
| Token in config.yaml without quotes | YAML parses colon as separator | Always quote: `bot_token: "123:ABC"` |
| Duplicate `bot_token` entries | First one wins (masked) | Ensure only ONE entry |
| Restart from same terminal | Gateway kills restart command | Use fresh terminal |
| Only updated `.env` | Gateway reads config.yaml | Update both |

## Debugging Checklist
- [ ] `.env` has real token (not `***`)
- [ ] `config.yaml` has real token **quoted token
- [ ] Only ONE `bot_token` line in config.yaml
- [ ] Gateway restarted from fresh terminal
- [ ] `gateway_state.json` shows `"state": "connected"`
- [ ] `/start` works in Telegram
- [ ] `/platforms` shows `telegram: connected`