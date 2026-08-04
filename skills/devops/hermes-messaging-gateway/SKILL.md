---
name: hermes-messaging-gateway
description: "Set up and troubleshoot Hermes Agent messaging gateways (Telegram, Discord, Slack, etc.) for remote access to your agent and tools."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, gateway, telegram, discord, messaging, remote-access, setup]
    homepage: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/
    related_skills: [hermes-agent]
---

# Hermes Messaging Gateway Setup

Class-level skill for configuring Hermes Agent's multi-platform messaging gateway. Covers Telegram, Discord, Slack, and other adapters — from bot creation through config, allowlists, and common pitfalls.

## Scope

- Bot/account creation on each platform
- Hermes `config.yaml` and `.env` configuration
- Gateway startup, restart, and verification
- Allowlist / admin configuration
- Troubleshooting: token masking, duplicate config sections, restart loops

## Telegram Quickstart (Reference)

### 1. Create Bot
- Message `@BotFather` → `/newbot` → name + username (must end in `bot`)
- **Save the token** (format: `123456789:ABC-DEF...`)

### 2. Get Your Chat ID
- Message your new bot anything (e.g., `/start`)
- Message `@userinfobot` or `@getmyid_bot` → copy your numeric **User ID** (e.g., `8336840601`)

### 3. Configure Hermes

**Option A: `.env` (simplest, recommended)**
```bash
echo 'TELEGRAM_BOT_TOKEN="123456789:ABC-DEF..."' >> ~/.hermes/.env
echo 'TELEGRAM_CHAT_ID="8336840601"' >> ~/.hermes/.env
echo 'TELEGRAM_ALLOWED_USERS="8336840601"' >> ~/.hermes/.env
```

**Option B: `config.yaml` (explicit)**
```yaml
platforms:
  telegram:
    enabled: true
    extra:
      bot_token: "123456789:ABC-DEF..."   # QUOTED, not masked
      chat_id: "8336840601"
      admin_chat_ids: '["8336840601"]'
      dm_policy: open
```

### 4. Start Gateway
```bash
hermes gateway run          # foreground (logs visible)
# or
hermes gateway install      # systemd service (Linux/WSL)
hermes gateway start
```

### 5. Verify
In Telegram, message your bot:
```
/platforms
```
Should show `telegram: connected`.

---

## Common Pitfalls & Fixes

| Symptom | Cause | Fix |
|---------|-------|-----|
| `No bot token configured` | Token is `***` (masked) in config.yaml | Edit config.yaml directly (Python/yaml), not `hermes config set` |
| `hermes config set` fails for `platforms.telegram.extra.bot_token` | Dotted key treated as env var name (invalid) | Use `.env` or edit YAML directly |
| Gateway won't restart from inside gateway | SIGTERM propagates to child shell | Stop with `Ctrl+C` in gateway terminal, then rerun |
| Two `platforms:` sections in config.yaml | Legacy + new config merged | Fix **both** occurrences (search for `bot_token:`) |
| "Unknown sender" / commands ignored | No allowlist configured | Set `TELEGRAM_ALLOWED_USERS=your_id` in `.env` or `admin_chat_ids` in config |
| Webhook port not reachable | Behind NAT/firewall | Use polling mode (default) or `cloudflared tunnel --url http://localhost:8644` |
| `.env` not read on Windows | PowerShell `echo`/`>>` writes UTF-16 (BOM), Hermes expects UTF-8 | Write with Python: `python -c "open('.env','w',encoding='utf-8').write(...)"` or use bash |
| Token shows as `123456:***` in config.yaml | `hermes config set` masks values containing `:` in YAML output | Never use `hermes config set` for bot tokens; edit YAML directly |
| Connection retries but fails silently | `dm_policy: restrictive` (default) + no allowlist | Set `dm_policy: open` OR `TELEGRAM_ALLOWED_USERS="your_id"` in .env |
| `hermes gateway restart` blocked | Running inside gateway process | Use **separate terminal window** for gateway commands |
| `.env` shows `TOKEN="NNN:***"`, gateway logs `token NNN:*** was rejected` | Real token revoked/wrong bot — `***` in `.env` is display masking, not actual value | Reissue via `@BotFather → /token` and update Hermes secret store (`hermes secrets set TELEGRAM_BOT_TOKEN "..."`) |
| `.env` literally contains `TOKEN="8863778824:***"` (placeholder, not display mask). `hermes status` still reports `Telegram ✓ configured` | Bob-of-Yesterday pasted a tutorial snippet into `.env` instead of the real secret. `hermes status` only checks that the *key exists*, not that the *value is a token* | Probe the secret against `https://api.telegram.org/bot<tok>/getMe`. `{"ok":true,"result":{...}}` → real, `{"ok":false,"error_code":404}` → placeholder. Then `hermes secrets set TELEGRAM_BOT_TOKEN "@BotFather → /token"` and restart the gateway |
| Cron job reports Telegram healthy but no messages arrive | Gateway alive but adapter in retry loop | Check `hermes logs gateway \| grep -i telegram` for `next retry in Xs` cadence — X growing = transient, X constant = real error |
| PowerShell `Where-Object {$_.Foo}` from MSYS bash fails with "term '...' not recognized" | MSYS expands `$_` as a path before passing to PowerShell | Use `powershell -File script.ps1` or back-tick escape `$` in `powershell -Command "…"` |

## Telegram Health Probe Sequence (for cron health checks)

When a cron job asks "is Telegram healthy?", `hermes status` alone is **not sufficient** — it only reports that the key exists, not that the token is valid. Use this 4-channel probe in order, stopping at the first failure:

1. **`hermes status | grep Telegram`** → check `✓ configured`. If `✗ not configured`, stop and run `hermes setup`.
2. **`cat $HOME/AppData/Local/hermes/gateway_state.json`** → check the `platforms.telegram.state` field. `running` / `polling` = alive; `retrying` / `error` = broken — read `error_message` for the rejection detail.
3. **`curl -s https://api.telegram.org/bot<TOKEN>/getMe`** → the source of truth.
   - `{"ok":true,"result":{"username":"...","id":...}}` → bot is real, secret is valid. Telegram is healthy.
   - `{"ok":false,"error_code":404}` → secret is invalid. Almost always means the `.env` holds a placeholder like `8863778824:***` rather than a real token. **Fix the secret, not the gateway.**
   - `{"ok":false,"error_code":401}` → token revoked. Reissue via `@BotFather → /token`.
4. **Token shape self-check (optional pre-flight):** a valid Telegram token matches `^\d{8,12}:[A-Za-z0-9_-]{30,}$`. If the value in `.env` ends in `:***` or doesn't match this regex, skip the network call and report "`.env` token is a placeholder".

`scripts/health-check.ps1` implements the broad cron triage (gateway process, log errors, drive space, Ollama). `scripts/telegram-probe.ps1` is the focused Telegram deep-probe: gateway_state.json → token-shape regex → /getMe, printing a one-line root-cause verdict and exiting non-zero on failure. **Run both for full coverage**: `health-check.ps1` tells you *that* Telegram is broken; `telegram-probe.ps1` tells you *why* (placeholder secret, revoked token, API error, or network failure).

#### Cron-mode network restriction pitfall

When the probe runs from a cron job, `curl` against `api.telegram.org` may be on the agent's unconditional blocklist (the parser flags it as a credential-bearing endpoint). If step 3 fails with `BLOCKED (hardline)` even though `telegram-probe.ps1` works from a manual terminal, the blocklist is the cause. Workaround: from a cron shell, do NOT call /getMe directly — read `gateway_state.json` (step 2) and the token shape (step 4) only, and emit a `Telegram adapter is in retrying state, see gateway_state.json` verdict. The user can then run `telegram-probe.ps1` from a foreground terminal for the full /getMe verdict.

---

## Config Editing Patterns

### Safe YAML Edit (Python)
```python
import yaml
with open('~/.hermes/config.yaml') as f:
    cfg = yaml.safe_load(f)
cfg['platforms']['telegram']['extra']['bot_token'] = 'REAL_TOKEN_HERE'
with open('~/.hermes/config.yaml', 'w') as f:
    yaml.dump(cfg, f)
```

### Fix Masked Token in Place
```bash
python3 -c "
import re
with open('~/.hermes/config.yaml') as f: c = f.read()
c = re.sub(r'bot_token: \d+:\*\*\*', 'bot_token: \"YOUR_REAL_TOKEN\"', c)
with open('~/.hermes/config.yaml', 'w') as f: f.write(c)
"
```

---

## Discord / Slack / Others

Same pattern: create app/bot → get credentials → add to `.env` or `config.yaml` under `platforms.<name>` → `hermes gateway run`.

See [Hermes Messaging Docs](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/) for platform-specific fields.

---

## Outbound Delivery vs. Inbound Setup

The pitfalls table above covers the **inbound** path (bot refuses messages from the user). The **outbound** path — cron jobs / scripts pushing messages *to* the user — has a different failure mode that looks identical from the user's side: nothing arrives. See:

- `references/outbound-delivery-failures.md` — `chat not found` (bot never received `/start`), missing `channel_directory.json`, `hermes send --list` returning `(none)`, and the `terminal`-tool token-scrubbing quirk that turns a clean bot token into a 404.

---

## Verification Checklist

- [ ] Bot responds to `/platforms` with `telegram: connected`
- [ ] `/tools` shows enabled toolsets
- [ ] Vault query works: `/search "term" in wiki`
- [ ] Subagent delegation works: `delegate researcher to "topic"`
- [ ] Cron job delivery works: `hermes cron create "0 9 * * *" --prompt "Daily summary" --deliver telegram`

---

## References

- `references/telegram-setup-guide.md` — Full walkthrough with screenshots
- `references/troubleshooting.md` — Error messages and fixes. Includes Session-3 patterns: `.env` vs gateway-secret masking distinction, `hermes logs gateway` triage table for retry-loop diagnosis, MSYS-bash → PowerShell `$_` corruption workaround.
- `references/outbound-delivery-failures.md` — `chat not found` (bot never received `/start`), missing `channel_directory.json`, `hermes send --list` empty
- `references/windows-quirks.md` — UTF-16 `.env` from PowerShell, gateway-in-TUI blocking, duplicate `platforms:` sections, token-masking in `hermes config set`
- `references/cloud-deployment-options.md` — **24/7 cloud hosting comparison**: Azure Students (free, no card), Hetzner (₹360/mo), Oracle (free but capacity lottery), architecture for PC+Cloud hybrid
- `references/digitalocean-student-pack.md` — **DigitalOcean Student Pack ($200 credit)**: activation from GitHub Education, Mumbai droplet setup, cost analysis, SSH access, Hermes deployment, credit monitoring, migration path
- `scripts/health-check.ps1` — One-shot cron triage for Hermes gateway state (service, processes, recent log errors). Windows-only; written to avoid the MSYS `$_` corruption class of bug.
- `scripts/telegram-probe.ps1` — Focused Telegram deep-probe. Reads `gateway_state.json`, runs token-shape regex on `TELEGRAM_BOT_TOKEN` from `.env`, then `/getMe` via `Invoke-RestMethod`. Prints a one-line root-cause verdict. Pairs with `health-check.ps1`.