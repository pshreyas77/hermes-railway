# Telegram Gateway Setup — Complete Walkthrough

## Prerequisites

- Hermes Agent installed (`hermes --version` works)
- Telegram app (mobile/desktop/web)
- Terminal access to machine running Hermes

---

## Step 1: Create Bot with @BotFather

1. Open Telegram → search `@BotFather`
2. Send `/newbot`
3. **Name**: Any display name (e.g., `Hermes Bot`)
4. **Username**: Must end in `bot` (e.g., `my_hermes_bot`, `shrey_hermes_01_bot`)
5. **Copy the token** — format: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`
   - Save it securely; anyone with this token controls your bot
6. Optional: `/setprivacy` → `Disable` (allows bot to read all group messages, not just @mentions)

---

## Step 2: Get Your User ID (Chat ID)

1. Message your new bot anything (e.g., `/start`)
2. Open `@userinfobot` or `@getmyid_bot`
3. Send any message → it replies with your **User ID** (numeric, e.g., `8336840601`)
4. **Copy this number** — this is your `TELEGRAM_CHAT_ID`

> For groups/channels: add bot to group, send message, use `@userinfobot` in group or check `getUpdates` API. Group chat IDs are negative (e.g., `-1001234567890`).

---

## Step 3: Configure Hermes

### Option A: .env file (Recommended — avoids YAML token masking)

**On Linux/macOS/WSL/Git Bash:**
```bash
cat >> ~/.hermes/.env << 'EOF'
TELEGRAM_BOT_TOKEN="123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
TELEGRAM_CHAT_ID="8336840601"
TELEGRAM_ALLOWED_USERS="8336840601"
OBSIDIAN_VAULT_PATH="/path/to/your/vault"
EOF
```

**On Windows (PowerShell writes UTF-16 — use Python instead):**
```powershell
python -c "
with open(r'C:\Users\shrey\AppData\Local\hermes\.env', 'w', encoding='utf-8') as f:
    f.write('TELEGRAM_BOT_TOKEN=\"123456789:ABCdefGHIjklMNOpqrsTUVwxyz\"\n')
    f.write('TELEGRAM_CHAT_ID=\"8336840601\"\n')
    f.write('TELEGRAM_ALLOWED_USERS=\"8336840601\"\n')
    f.write('OBSIDIAN_VAULT_PATH=\"E:/_Knowledge/ObsidianVault\"\n')
"
```

### Option B: config.yaml (Explicit)

```bash
hermes config edit
```

Add/update:
```yaml
platforms:
  telegram:
    enabled: true
    extra:
      bot_token: "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"  # QUOTED, full token
      chat_id: "8336840601"
      admin_chat_ids: '["8336840601"]'
      dm_policy: open          # allows your user without explicit allowlist
      # allowed_chats: ""      # optional: restrict to specific chat IDs
```

> ⚠️ **Never use `hermes config set platforms.telegram.extra.bot_token "..."`** — it masks the token as `***` in YAML because of the colon.

---

## Step 4: Start Gateway

```bash
# Foreground (see logs, good for first run)
hermes gateway run

# Background service (Linux/macOS/WSL2 with systemd)
hermes gateway install
hermes gateway start

# Windows: keep terminal open, or use NSSM/Task Scheduler
```

**Wait for this log line:**
```
[INFO] [Telegram] Connected as @your_bot_username (polling mode)
```

---

## Step 5: Test from Telegram

Open chat with your bot (`t.me/your_bot_username`) and send:

```
/platforms
```

Expected response: shows `telegram: connected` and other platform statuses.

Then try vault access:
```
/search "Aryan migration" in wiki
read wiki/entities/B. R. Ambedkar
```

---

## Step 6: Enable Toolsets for Gateway (if needed)

Default gateway toolsets may be limited. Check and enable:

```bash
# List available
hermes tools list

# Enable for telegram platform
hermes tools enable file --platform telegram
hermes tools enable terminal --platform telegram
hermes tools enable web --platform telegram
hermes tools enable obsidian --platform telegram
hermes tools enable cronjob --platform telegram
hermes tools enable delegation --platform telegram
```

Or via config:
```yaml
platform_toolsets:
  telegram:
    - file
    - terminal
    - web
    - obsidian
    - cronjob
    - delegation
    - skills
    - memory
    - session_search
    - todo
    - image_gen
    - vision
    - code_execution
```

---

## Troubleshooting

### "No bot token configured" but token is in config
- Check config.yaml for `bot_token: 123456:***` (masked) → fix with Python edit
- Check `.env` has `TELEGRAM_BOT_TOKEN` (no quotes issues, UTF-8)

### Bot doesn't reply to `/start` or `/platforms`
- **Allowlist missing**: Add `TELEGRAM_ALLOWED_USERS="your_id"` to `.env` OR set `dm_policy: open` in config.yaml
- **Privacy mode**: `/setprivacy @BotFather` → Disable (for groups)

### Gateway shows "telegram: failed to connect" retrying
- Token invalid → verify with `curl "https://api.telegram.org/bot<TOKEN>/getMe"`
- Network block → ensure machine can reach `api.telegram.org:443`

### Two `platforms:` sections in config.yaml
```bash
grep -n "platforms:" ~/.hermes/config.yaml
```
Fix **both** occurrences (legacy + new).

### Windows: .env not read
- PowerShell `echo`/`>>` writes UTF-16 with BOM
- **Fix**: Use Python to write `.env` as UTF-8 (see Step 3 Option A)

### Cannot restart gateway from inside Hermes TUI
- Gateway process = current process → `SIGTERM` kills your shell
- **Fix**: Open **separate terminal window** for gateway commands

---

## Advanced: Webhook Mode (Public HTTPS)

If you need webhook instead of polling (lower latency, but needs public URL):

```yaml
platforms:
  telegram:
    enabled: true
    extra:
      bot_token: "..."
      chat_id: "..."
      webhook: true
      webhook_url: "https://your-domain.com/webhooks/telegram"
      webhook_port: 8644
```

Expose locally with Cloudflare Tunnel:
```bash
cloudflared tunnel --url http://localhost:8644
# Copy the https://xxx.trycloudflare.com URL → use as webhook_url
```

---

## Maintenance Commands

```bash
# View gateway logs
tail -f ~/.hermes/logs/gateway.log

# Check platform status
hermes gateway status

# Update bot token
# Edit .env or config.yaml → hermes gateway restart (from external shell)

# Deliver cron job to Telegram
hermes cron create "0 9 * * *" --prompt "Daily vault health report" --deliver telegram --deliver-chat-id "8336840601"
```