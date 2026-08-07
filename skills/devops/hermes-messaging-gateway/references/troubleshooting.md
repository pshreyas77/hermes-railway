# Hermes Gateway Troubleshooting — Real Session Notes

These are actual errors encountered and fixes applied during a live Telegram gateway setup (July 2026, Windows).

---

## Error: `ValueError: Invalid environment variable name: 'PLATFORMS.TELEGRAM.EXTRA.BOT_TOKEN'`

**Cause:** `hermes config set platforms.telegram.extra.bot_token "..."` treats the dotted key as an env var name (invalid).

**Fix:** Use `.env` for secrets, or edit `config.yaml` directly with Python/yaml.

---

## Error: `No bot token configured` — but token is in `.env`

**Cause 1:** `.env` saved as UTF-16 (PowerShell `>>` default). Hermes reads UTF-8 only.

**Fix:** Rewrite `.env` as UTF-8:
```bash
cat > ~/.hermes/.env << 'EOF'
TELEGRAM_BOT_TOKEN="8863778824:REAL_TOKEN"
TELEGRAM_CHAT_ID="8336840601"
TELEGRAM_ALLOWED_USERS="8336840601"
OBSIDIAN_VAULT_PATH="/vault"
EOF
```

**Cause 2:** `config.yaml` has **two** `platforms:` sections (legacy + new). The first one wins and has masked token `bot_token: 8863778824:***`.

**Fix:** Search for all `bot_token:` occurrences and fix **both**:
```bash
grep -n "bot_token" ~/.hermes/config.yaml
# Fix each occurrence
python3 -c "
import re
with open('~/.hermes/config.yaml') as f: c = f.read()
c = re.sub(r'bot_token: \d+:\*\*\*', 'bot_token: \"YOUR_REAL_TOKEN\"', c)
with open('~/.hermes/config.yaml', 'w') as f: f.write(c)
"
```

---

## Error: `Another gateway instance is already running (PID XXXX)`

**Cause:** Gateway started in background or previous terminal.

**Fix:**
```bash
# Windows
taskkill /F /PID XXXX
# Or use --replace flag
hermes gateway run --replace
```

---

## Error: `Refusing to restart the gateway from inside the gateway process`

**Cause:** Running `hermes gateway restart` or `stop` from a shell spawned BY the gateway (SIGTERM propagates).

**Fix:** Stop with `Ctrl+C` in the gateway's own terminal, then rerun from a fresh shell.

---

## Windows `.env` Encoding Fix

PowerShell `echo '...' >> file` writes **UTF-16 LE with BOM**. Hermes's dotenv parser reads UTF-8.

**Always use:**
```bash
# Bash (Git Bash / WSL)
cat > ~/.hermes/.env << 'EOF'
TELEGRAM_BOT_TOKEN="..."
EOF

# Or Python
python3 -c "
with open('~/.hermes/.env', 'w') as f:
    f.write('TELEGRAM_BOT_TOKEN=\"...\"\n')
"
```

---

## Allowlist Not Working

**Symptom:** Bot ignores commands, logs "deny unknown sender"

**Fix:** Set **both** (belt + suspenders):
- `.env`: `TELEGRAM_ALLOWED_USERS="8336840601"`
- `config.yaml`: `admin_chat_ids: '["8336840601"]'` and `dm_policy: open`

---

## Additional Fixes (Session 2)

### Masked Token in config.yaml (Literal `***`)

**Cause:** After failed `hermes config set`, the config shows `bot_token: 8863778824:***` literally. The `***` is not a redaction — it's the stored value.

**Fix:** Direct YAML edit (Python):
```python
import yaml
with open('~/.hermes/config.yaml') as f:
    cfg = yaml.safe_load(f)
cfg['platforms']['telegram']['extra']['bot_token'] = 'REAL_TOKEN'
with open('~/.hermes/config.yaml', 'w') as f:
    yaml.dump(cfg, f)
```

---

### Duplicate `platforms:` Sections

**Symptom:** `grep "bot_token"` shows multiple lines, fixing one doesn't work.

**Fix:** Remove the legacy `platforms:` block (around line 345) or ensure both have correct token.

---

### PowerShell `.env` Encoding (UTF-16)

**Symptom:** `.env` looks correct but `cat` shows `��T\u0000E\u0000L...`

**Fix:** Rewrite with Python or bash heredoc (see above).

---

## Diagnostic Patterns (Session 3 — cron health check)

### `.env` `***` masking ≠ gateway secret is broken

**Misconception:** Many assume `TELEGRAM_BOT_TOKEN="8863778824:***"` in `~/.hermes/.env` means the secret is missing or corrupted. **It doesn't** — Hermes writes `***` to `.env` for *display* purposes, while the actual token lives in the gateway's internal secret store.

**How to see the gateway's view of the secret:**
```bash
hermes logs gateway 2>&1 | tail -30
```
The gateway also redacts the token in logs — but it shows the **bot id prefix** (real, from Telegram's response). So if logs say:
```
ERROR ... The token `8863778824:***` was rejected by the server.
```
…then:
- The `8863778824:` part is the *actual* bot id Telegram saw.
- The gateway IS using a real stored secret.
- Telegram rejected that secret → token revoked, wrong bot, or wrong account.

This rules out `.env` misconfiguration as the cause. **Don't waste time editing `.env`** — fix the secret store instead:
```bash
hermes secrets set TELEGRAM_BOT_TOKEN "NEW_BOT_TOKEN_FROM_BOTFATHER"
hermes gateway restart
```
(subcommand may be `hermes config` or similar depending on Hermes version; check `hermes --help`.)

### `hermes logs gateway | grep -i telegram` triage

| Pattern | Meaning | Action |
|---|---|---|
| `Connecting (attempt 1/8)… Connected` — single line | Transient blip | None |
| `Failed to connect … attempt 1/8` once, then `Connected` | Network flicker | None |
| `Failed … next retry in 300s`, attempts incrementing every 5 min | Persistent secret/config error | Fix token (above) or allowlist |
| `next retry in Xs` where X grows (exponential backoff) | Telegram server-side outage | Wait; loop is self-healing |
| `Disconnected from Telegram` after success | Bot token revoked | Reissue via `@BotFather → /token` |

### `hermes status` is the right 1-shot triage on cron

For cron jobs asking "is everything up?", `hermes status` covers all four dimensions in one command:
- `◆ Gateway Service` → `Status: ✓ running`, `Manager:`, `PID(s):` — non-zero PID = alive even if you can't reach `:8644`.
- `◆ Sessions` → `Active: 0` is normal; non-zero = a chat is open right now.
- `◆ Scheduled Jobs` → `Jobs: N active, N total`. Drop in `total` between runs → a cron file disappeared.
- `◆ Messaging Platforms` → each platform's `✓ configured` / `✗ not configured`.

### PowerShell `$_` corruption from MSYS bash

**Symptom:** Inline PowerShell from Git Bash fails with:
```
Where-Object : The term '/e/_Knowledge/ObsidianVault.LocalPort' is not recognized
```
**Cause:** MSYS bash interprets `$_.LocalPort` as a path starting with `/e/.../ObsidianVault.LocalPort` and passes it as a literal to PowerShell, where `Where-Object` tries to evaluate it.

**Fix (preferred):** Write a `.ps1` file and invoke with `-File`:
```bash
cat > /tmp/check.ps1 << 'EOF'
Get-NetTCPConnection | Where-Object { $_.LocalPort -eq 11434 } | Format-Table -AutoSize
EOF
powershell -NoProfile -ExecutionPolicy Bypass -File /tmp/check.ps1
```
**Fix (inline escape):** Back-tick escape the `$` in `powershell -Command "…"` so MSYS doesn't expand it.

This affects any `Where-Object` / `ForEach-Object` / `$_.Property` syntax crossing from MSYS bash to PowerShell — not just the script we hit during the cron health check.

---

## Verification Commands

```bash
# Check gateway health
curl http://localhost:8644/health

# Check logs
tail -f ~/.hermes/logs/gateway.log | grep -i telegram

# Test from Telegram
/platforms
/tools
/search "test" in wiki
```

---

## Additional Fixes (Session 4 — Duplicate .env Lines & Config Priority)

### Duplicate Lines in .env After Python String Replace

**Symptom:** `.env` file ends up with duplicate `TELEGRAM_BOT_TOKEN` and `TELEGRAM_ALLOWED_USERS` lines after running a Python replace script.

**Cause:** The Python script used `content.replace(old, new)` where `old` didn't match exactly (newline/spacing differences), so it appended instead of replacing. The original content had:
```
TELEGRAM_BOT_TOKEN="8863778824:***"
TELEGRAM_CHAT_ID="8336840601"
OBSIDIAN_VAULT_PATH="/vault"
TELEGRAM_ALLOWED_USERS="8336840601"
TELEGRAM_BOT_TOKEN="8863778824:***"
TELEGRAM_ALLOWED_USERS="8336840601"
```

**Fix:** Write the entire clean `.env` file instead of trying to replace lines:
```python
import os
env_path = os.path.expanduser(r'~/.hermes/.env')
content = '''TELEGRAM_BOT_TOKEN="8863778824:REAL_TOKEN"
TELEGRAM_CHAT_ID="8336840601"
OBSIDIAN_VAULT_PATH="/vault"
TELEGRAM_ALLOWED_USERS="8336840601,8336840501"
NVIDIA_API_KEY=...
NVIDIA_BASE_URL=...
'''
with open(env_path, 'w', encoding='utf-8') as f:
    f.write(content)
```

**Lesson:** For `.env` files, **write the whole file fresh** — don't try surgical line replacement.

---

### Config Priority: .env Overrides config.yaml

**Key behavior:** Hermes gateway reads `.env` **first**, then falls back to `config.yaml`. The `.env` token takes precedence.

**Implication:** If `.env` has a placeholder (`8863778824:***`) and `config.yaml` has the real token, the gateway will still use the placeholder from `.env`.

**Fix:** Ensure `.env` has the real token, or remove the token from `.env` entirely and only keep it in `config.yaml`.

---

### `getUpdates` Returns Empty Array — Not an Error

**Symptom:** `curl https://api.telegram.org/bot<token>/getUpdates` returns `{"ok":true,"result":[]}`

**Meaning:** The bot **has not received any messages yet**. This is normal — it's not an error.

**Test:** Send a message to the bot from Telegram, then call `getUpdates` again — the message will appear in `result`.

---

### Duplicate `bot_token` Entries in config.yaml

**Symptom:** `grep "bot_token" config.yaml` shows multiple lines; fixing one doesn't work.

**Cause:** Legacy `platforms:` section + new `platforms.telegram:` section both exist.

**Fix:** Use Python/YAML to load the full config, set the token once, and dump the entire config back (this removes duplicates automatically):
```python
import yaml
with open('~/.hermes/config.yaml') as f:
    cfg = yaml.safe_load(f)
cfg['platforms']['telegram']['extra']['bot_token'] = 'REAL_TOKEN'
with open('~/.hermes/config.yaml', 'w') as f:
    yaml.dump(cfg, f, default_flow_style=False, sort_keys=False)
```

This writes a clean config with single `bot_token` entry.

---

### Complete Clean Setup Checklist

After any token/allowlist change:
1. `.env` — clean, single token line, UTF-8, real token
2. `config.yaml` — single `bot_token` entry, real token, `dm_policy: open`, correct `admin_chat_ids`
3. `hermes gateway restart` (from fresh terminal)
4. Verify: `hermes status` → `Telegram ✓ configured`
4. Verify: `cat ~/.hermes/gateway_state.json` → `telegram.state: "connected"`
5. Test: Send `/start` to bot from Telegram
6. Verify: `getUpdates` shows the message