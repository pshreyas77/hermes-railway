# Windows-Specific Hermes Gateway Quirks

## PowerShell UTF-16 .env Encoding

**Problem**: PowerShell `echo "KEY=value" >> .env` writes **UTF-16 LE with BOM**, not UTF-8. Hermes reads `.env` as UTF-8 → tokens appear as garbage or empty.

**Symptoms**:
- `TELEGRAM_BOT_TOKEN` shows as `��T\u0000E\u0000L...` in cat output
- Gateway logs: "No bot token configured" despite token in .env

**Fix**: Write `.env` with Python (forces UTF-8):

```powershell
python -c "
with open(r'C:\Users\shrey\AppData\Local\hermes\.env', 'w', encoding='utf-8') as f:
    f.write('TELEGRAM_BOT_TOKEN=\"8863778824:AAFo-dFCpYX2_lUv_Ru-WBzOdD0e77z4tps\"\n')
    f.write('TELEGRAM_CHAT_ID=\"8336840601\"\n')
    f.write('OBSIDIAN_VAULT_PATH=\"E:/_Knowledge/ObsidianVault\"\n')
    f.write('TELEGRAM_ALLOWED_USERS=\"8336840601\"\n')
"
```

**Verify**:
```powershell
python -c "
with open(r'C:\Users\shrey\AppData\Local\hermes\.env', 'r', encoding='utf-8') as f:
    print(repr(f.read()[:100]))
"
```

---

## Gateway Process Isolation

**Problem**: You're inside the Hermes TUI (this chat) → the gateway runs as a child process → `hermes gateway stop/restart` sends SIGTERM to **your current shell**, killing the chat.

**Symptoms**:
- `hermes gateway restart` → "Refusing to restart from inside gateway process"
- `hermes gateway stop` → "Blocked: cannot stop from inside gateway"
- `taskkill /F /IM hermes.exe` works but kills TUI too

**Fix**: Use **separate terminal window** for gateway:
1. `Win + X` → "Windows Terminal" / "PowerShell"
2. Run `hermes gateway run` there
3. Keep it open; this chat stays alive

**Alternative**: Background with `start` (but logs hidden):
```powershell
start cmd /c "hermes gateway run"
```

---

## Duplicate `platforms:` Sections in config.yaml

**Problem**: Running `hermes config set platforms.telegram.enabled true` multiple times (or old + new config) creates **two `platforms:` sections**. Hermes reads the first; your token edit may be in the second (ignored).

**Symptoms**:
- Token fixed in one section but gateway still says "No bot token configured"
- `grep -n "platforms:" config.yaml` shows 2+ line numbers

**Fix**: Search and consolidate:

```python
import yaml
with open('config.yaml') as f:
    cfg = yaml.safe_load(f)
# Merge platforms sections manually, then dump
```

Or manually edit: keep only one `platforms:` block with all platforms.

---

## Token Masking in `hermes config set`

**Problem**: `hermes config set platforms.telegram.extra.bot_token "123:ABC"` treats the key as an env var name (`PLATFORMS.TELEGRAM.EXTRA.BOT_TOKEN` invalid) AND masks the value as `***` in YAML because it contains `:`.

**Never use for bot tokens**. Use:
1. `.env` with `TELEGRAM_BOT_TOKEN="..."` (recommended)
2. Direct YAML edit via Python

---

## Allowlist / dm_policy Confusion

**Default**: Restrictive — only users in `TELEGRAM_ALLOWED_USERS` (env) or `admin_chat_ids` (config) can use bot.

**Symptoms**: Bot receives message but doesn't reply; logs show "Unknown sender" or silent drop.

**Fixes** (pick one):
```bash
# .env
TELEGRAM_ALLOWED_USERS="8336840601"

# OR config.yaml
platforms:
  telegram:
    extra:
      dm_policy: open
      admin_chat_ids: '["8336840601"]'
```

**Both needed for full admin**: `dm_policy: open` allows anyone to DM; `admin_chat_ids` controls who can approve commands (`/approve`).

---

## Verify Token Without Gateway

```bash
curl "https://api.telegram.org/bot8863778824:AAFo-dFCpYX2_lUv_Ru-WBzOdD0e77z4tps/getMe"
```
Response should contain `"ok":true,"result":{"id":...,"username":"your_bot",...}}`

---

## Firewall / Network

- Polling mode (default): Outbound HTTPS to `api.telegram.org:443` only
- No inbound ports needed
- Corporate firewall may block → use webhook + Cloudflare Tunnel if needed

---

## Quick Diagnostic Script

```powershell
python -c "
import os, yaml
from pathlib import Path

# Check .env
env_path = Path(os.environ['USERPROFILE']) / 'AppData' / 'Local' / 'hermes' / '.env'
if env_path.exists():
    content = env_path.read_text(encoding='utf-8')
    print('.env exists:', 'TELEGRAM_BOT_TOKEN' in content)
    print('  encoding OK:', not content.startswith('\ufeff'))
else:
    print('.env: NOT FOUND')

# Check config.yaml
cfg_path = Path(os.environ['USERPROFILE']) / 'AppData' / 'Local' / 'hermes' / 'config.yaml'
if cfg_path.exists():
    cfg = yaml.safe_load(cfg_path.read_text(encoding='utf-8'))
    token = cfg.get('platforms',{}).get('telegram',{}).get('extra',{}).get('bot_token','')
    print('config.yaml token:', 'FULL' if 'AAFo' in token else 'MASKED' if '***' in token else 'MISSING')
    print('  dm_policy:', cfg.get('platforms',{}).get('telegram',{}).get('extra',{}).get('dm_policy'))
    print('  admin_chat_ids:', cfg.get('platforms',{}).get('telegram',{}).get('extra',{}).get('admin_chat_ids'))
else:
    print('config.yaml: NOT FOUND')
"
```