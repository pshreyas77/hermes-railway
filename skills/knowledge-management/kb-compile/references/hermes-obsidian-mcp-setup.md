# Hermes ↔ Obsidian MCP Connection (Zero-Cost)

**Date:** 2026-07-13  
**Purpose:** Connect Hermes Agent directly to your Obsidian vault via MCP — enables AI to read/write vault files in real-time, not just during scheduled cron runs.

---

## Why This Matters

Without MCP: Hermes processes your vault only during Night Shift (23:30/03:00/06:00).  
With MCP: Hermes reads and writes your vault on-demand, any time, as part of every conversation.

This is what makes the vault "cognitive" — not just storage.

---

## Step 1: Install Obsidian Plugin (Manual — Must Do in App)

1. Open Obsidian → Settings → Community Plugins → Browse
2. Search: `obsidian-local-rest-api`
3. Install `obsidian-local-rest-api` by @coddingtonbear
4. Enable: Settings → Local REST API
5. **Enable "Allow HTTP"** (required for localhost)
6. **Copy the API key** (Settings → Local REST API → API key)

Plugin URL: `community.obsidian.md/plugins/obsidian-local-rest-api`

---

## Step 2: Connect Hermes via MCP

```bash
hermes mcp add obsidian \
  --transport http \
  --url https://127.0.0.1:27124/mcp/ \
  --header "Authorization: Bearer YOUR_API_KEY_HERE"
```

**Important:** 
- Obsidian must be running with the Local REST API plugin enabled
- The plugin runs at `https://127.0.0.1:27124/mcp/` by default
- API key is from Step 1

Test:
```bash
hermes mcp test obsidian
```

---

## What This Enables

| Action | Without MCP | With MCP |
|--------|-------------|----------|
| Read vault files | Only via read_file tool | ✅ Direct MCP + any time |
| Write vault files | Only via scheduled cron | ✅ Instant, in conversation |
| Search vault | grep through files | ✅ Full-text via MCP |
| Daily notes | Pre-scheduled | ✅ Created on-demand |
| Vault queries | Manual | ✅ AI asks your vault questions |
| Synthesis | Scheduled (06:00) | ✅ Any time |

---

## Troubleshooting

### "Connection refused"
- Obsidian not running → Open Obsidian app
- Plugin not enabled → Settings → Local REST API → Enable
- Wrong port → Default is 27124, check plugin settings

### "401 Unauthorized"
- Wrong API key → Re-copy from Obsidian → Settings → Local REST API → API key
- Or generate new one in plugin settings

### "SSL certificate error"
- The plugin uses a self-signed cert. Hermes MCP with `--transport http` (not https) bypasses this:
  ```
  hermes mcp add obsidian --transport http --url http://127.0.0.1:27124/mcp/ --header "Authorization: Bearer KEY"
  ```

---

## Alternative: HTTP Without Header (Simplest)

If you just want HTTP (no SSL), the plugin supports plain HTTP at port 27123:
```bash
hermes mcp add obsidian \
  --transport http \
  --url http://127.0.0.1:27123/mcp/
```

Note: Port 27123 = no HTTPS/no cert. Port 27124 = HTTPS with self-signed cert.

---

## Key Files Created During Setup

```
05 - SYSTEM/ZERO-COST-SECOND-BRAIN-SETUP.md  — Full setup guide
05 - SYSTEM/DEMO-CAPTURE-PROMPTS.md           — Test prompts for Telegram
05 - SYSTEM/telegram-to-obsidian-capture.md   — In-vault capture skill
05 - SYSTEM/obsidian-sync-doctor.md           — Diagnostic skill
playbooks/verify_hermes_obsidian_loop.sh      — Verification script
```

---

## Related Skills

- `kb-compile` — compiles 0-raw/ → 02 - AREAS/ (use with MCP for instant processing)
- `kb-healthcheck` — weekly audit (cron model drift pitfall documented)
- `night-shift-powershell-ps7.md` — PowerShell 7.5 fixes for pipeline scripts