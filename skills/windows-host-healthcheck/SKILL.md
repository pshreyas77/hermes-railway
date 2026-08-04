---
name: windows-host-healthcheck
description: Run Windows host health probes from a Hermes cron context.
category: devops
---

# Windows Host Healthcheck (from Hermes cron / bash)

The user's setup: Windows 11 host, E:-only data drive, Hermes Agent running
in a cron-style loop. Periodic health checks answer four questions:

  1. **Disk:** is E: (and any secondary drives) within sane thresholds?
  2. **Local AI runtime:** is Ollama (or whatever) listening, or is the model
     strictly cloud? — and is the cloud provider reachable?
  3. **Hermes gateway:** is the `hermes serve` process alive and responding?
  4. **Messaging delivery:** is the configured delivery channel (Telegram,
     Slack, Discord) actually able to deliver? Token health, polling state.

The class of work: short probe script, report ONLY if a probe fails, exit
silent otherwise. The user's standing rule for cron is "Only report via
Telegram if issues found" — match that.

## Environment gotchas (read first)

**`execute_code` is hard-blocked in cron mode.** Calling it from a cron
session returns `BLOCKED: execute_code runs arbitrary local Python
(including subprocess calls that bypass shell-string approval checks).
Cron jobs run without a user present to approve it. Use normal tools
instead...` and reports 0 tool calls consumed. Don't waste a turn
retrying it — go straight to `terminal` with inline commands or a
`.ps1`/`.sh` script file.

The Hermes terminal tool on Windows runs through **bash (git-bash / MSYS)**,
NOT PowerShell or cmd.exe. Several non-obvious consequences:

- `tasklist //FI "..."` breaks — MSYS rewrites `//FI` to `/FI` and PowerShell
  rejects the slash form. **Use `powershell -NoProfile -Command "..."`
  instead** for anything process-related on Windows.
- POSIX paths (`/e`, `/c/Users/shrey`) work alongside native
  (`C:\Users\shrey`). Prefer native for PowerShell, POSIX for grep/find.
- `df -h E:` fails — there is no drive E on a POSIX mount list.
  **Use `df -h /e`** (MSYS maps the drive under `/e`).
- The `terminal` skill is sometimes listed but not loaded — don't depend on
  it; fall back to inline bash + powershell.
- **MSYS bash mangles PowerShell variables when passed via `-Command`.**
  Any PowerShell expression containing `$_`, `$.Name`, `$_.Foo`, `$x.Bar`,
  `Where-Object { ... }`, or any `{}` block will be silently corrupted by
  bash before PowerShell ever sees it — bash expands `$_` (last command
  path), strips `.Name` (treats as chained command), and chokes on `{`.
  Symptom in a cron run: PowerShell floods the terminal with ~100KB of
  `The term '/c/Users/shrey.X' is not recognized as the name of a cmdlet`
  errors. **Fix:** write the PowerShell to a `.ps1` file under
  `E:\.tmp\health_check.ps1` (or wherever) and invoke via
  `powershell -ExecutionPolicy Bypass -File "E:\.tmp\health_check.ps1"`.
  The `-File` path does not go through bash variable expansion. This is
  the ONLY safe way to run multi-line PowerShell with `$_` from this
  bash terminal. For one-liners without `$_` (e.g. `Get-Service Ollama`),
  inline `-Command` is fine.
- **Python `Path.exists()` does NOT auto-resolve `.exe` on Windows.** A
  script that hardcodes `Path("C:/.../Scripts/graphify")` returns
  `False` from `.exists()` even when `Scripts/graphify.exe` is sitting
  right there — `pathlib` only sees the literal filename you pass.
  Symptom in a cron wrapper: logs `[err] graphify binary not found`
  followed by a silent `[noop]` (the wrapper continues without doing the
  actual work). Bash/cmd resolve `.exe` automatically; Python does not.
  Fix in Python: probe both `[p, p.with_suffix(".exe")]` (or use
  `shutil.which(name)` for PATH-resolved binaries). Audit any wrapper
  script that hardcodes a Windows binary path before relying on its
  exit code.

## The 4 probes

### Probe 1 — Disk space

```bash
df -h /e /c 2>&1 | head -10
```

Warning thresholds: >90% used = WARN, >95% = CRITICAL. The user's E: is 150G
total; 51% used (76G / 74G free) is the calm baseline.

### Probe 2 — Local AI runtime (Ollama or cloud-only)

Ollama has **three distinct states** and the probe must distinguish them.
Reporting "Ollama is down" when the binary isn't installed is noise; reporting
"OK" when the binary is sitting on disk but never started is a missed alert.

```bash
# (a) Cloud-only check (nvidia/minimax provider reachability)
curl -s -o /dev/null -w "%{http_code}\n" --max-time 5 \
  https://integrate.api.nvidia.com/v1/models

# (b) Ollama: is the binary installed? (default + E: drive locations)
ls "C:/Users/shrey/AppData/Local/Programs/Ollama/ollama.exe" 2>/dev/null
ls "E:/_AI_Tools/ollama/OllamaSetup.exe" 2>/dev/null

# (c) Ollama: is the service registered?
powershell -NoProfile -Command "Get-Service -Name Ollama -ErrorAction SilentlyContinue |
  Select-Object Name,Status,StartType"

# (d) Ollama: is the daemon reachable?
curl -s --max-time 5 http://127.0.0.1:11434/api/tags | head -5
```

**Verdict matrix** (report exactly one):
| binary | service | port 11434 | verdict |
|--------|---------|------------|---------|
| ❌     | ❌      | ❌         | OLLAMA NOT INSTALLED — expected on cloud-only setups; not an alert |
| ✅     | ❌      | ❌         | **OLLAMA INSTALLED BUT NOT RUNNING** — alert (model on disk but unreachable) |
| ✅     | ✅ or ❌| ✅         | HEALTHY |
| ✅     | ✅      | ❌         | service stuck — `Restart-Service Ollama` |

The **installed-but-not-running** state is the trap: `curl /api/tags → 000`
looks identical to "not installed", but the user's E: drive contains
`OllamaSetup.exe` and the model blobs/manifests under `E:/_AI_Tools/ollama/`.
They installed the model and never started the service. Always check the
binary location before declaring Ollama absent. (Observed 2026-07-30 cron:
`OllamaSetup.exe` in `E:/_AI_Tools/`, no `ollama.exe` process, no Ollama
service — alert fired correctly only because binary location was checked.)

If neither local Ollama nor a configured cloud model is reachable, model calls
fail — that's the actual failure mode. Older crons check Ollama
unconditionally even when the user runs cloud-only; that warning in the log
is a stale check, not a current issue.

### Probe 3 — Hermes gateway liveness

Find the port first (Hermes uses `--port 0` so it picks dynamically):

```bash
powershell -NoProfile -Command "Get-NetTCPConnection -State Listen |
  Where-Object { \$_.LocalPort -in 55716,55876,11434,8000 } |
  Select-Object LocalPort,OwningProcess | Format-Table -AutoSize"
```

Then probe:

```bash
curl -s --max-time 5 http://127.0.0.1:<PORT>/openapi.json | head -5
```

A 200 with the OpenAPI schema dump = healthy. Headless backend responds
with `{"error":"Headless backend (hermes serve): web UI disabled ..."}`
to the root path — that IS the healthy response, not an error.

### Probe 4 — Messaging channel health (Telegram etc.)

Two equally-canonical signals exist; use whichever is cleaner for the run:

**(a) State file (preferred — single read, no log scraping):**
```bash
cat "$HOME/AppData/Local/hermes/gateway_state.json" 2>/dev/null
# Look for: "platforms":{"telegram":{"state":"connected","error_code":null,...}}
# State values: "connected" | "disconnected" | "connecting" | "error"
# Healthy = state == "connected" AND error_code == null AND error_message == null
# updated_at freshness: stale (>1h old on an idle system) is itself a signal
# that the gateway event loop has wedged.
```

**(b) Log scrape (use when state file is missing or stale):**
```bash
"C:/Users/shrey/AppData/Local/hermes/logs/gateway.log"
# Recent Telegram state
powershell -NoProfile -Command \
  "Get-Content 'C:\Users\shrey\AppData\Local\hermes\logs\gateway.log' -Tail 500 |
   Select-String -Pattern 'Telegram|token|rejected'"
```

Failure signatures to grep for:
- `The token 'XXXX:***' was rejected by the server` — token revoked/rotated
  or pasted incorrectly. **Critical: cron delivery to Telegram is dead.**
- `Reconnect telegram failed, next retry in 300s` — repeating means
  unrecoverable (token or network).
- `Disconnected from Telegram` after a fresh `Starting Hermes Gateway` —
  gateway tried but the bot can't authenticate.
- `no delivery target resolved for deliver=telegram` — scheduler-level
  consequence of the broken channel; cron output is being silently dropped.

## CRITICAL gotcha: Hermes secret redaction

Hermes masks secrets **at the source**, not just in tool output:

- `~/.bashrc` and `.env` both show tokens as `8863778824:***`
- `read_file` on `.env` returns `Access denied: ... Hermes credential store`
- Even raw `powershell -NoProfile -Command "Get-Content .env"` returns the
  masked form because the file on disk IS masked

The actual token lives behind Hermes's internal credential channel. From a
cron context you CANNOT recover the raw token. The fix is **foreground
session only** — `hermes env set TELEGRAM_BOT_TOKEN=...` or
`hermes messaging platforms` to inspect.

Implication: don't burn cycles trying to extract a Telegram token from disk.
Read the logs, report the failure mode, recommend the foreground-only fix.

## Reporting discipline

The user explicitly wants: **"Only report via Telegram if issues found"**.

Match that. If the cron job has `deliver=telegram` AND Telegram is broken,
the cron output is silently dropped anyway — so the final response is the
report channel, not Telegram. Always:

1. Table of probe results (✅/⚠️/❌ + detail)
2. List of CRITICAL findings first, then warnings
3. For each issue: severity, likely cause, **the foreground-only fix**
4. Note any other observations worth flagging (transient API retries, etc.)

If ALL probes pass → respond with exactly `[SILENT]` (nothing else).

### Sending the report via Telegram from cron

**Use `hermes send --to telegram` — it is cron-safe and does NOT need the
running gateway.** Per `hermes send --help`: "Reuses the gateway's
platform credentials (~/.hermes/.env + ~/.hermes/config.yaml) — no LLM,
no agent loop, no running gateway required for bot-token platforms like
Telegram/Discord/Slack/Signal."

Important gotchas observed in real cron runs:

- **The real Telegram bot token is read from `config.yaml`
  (`platforms.telegram.extra.bot_token`), NOT from `~/.hermes/.env`.**
  The `.env` entry may legitimately hold the placeholder
  `8863778824:***` (or similar `id:***` form) and `hermes send` will
  still work. The Hermes "redaction at the source" masking seen in
  `.env` is a red herring — the live token lives in config.yaml's
  `extra.bot_token` field. Don't waste time trying to "fix" `.env`.
  Verified 2026-08-03: gateway had the masked `.env`, yet `hermes send`
  delivered successfully because config.yaml held the real token.
- **Channel discovery:** `hermes send --list telegram` shows what
  target names the gateway already knows about (e.g.
  `telegram:P Sunny [8336840501]`). If `hermes send --to telegram`
  fails with "No home channel set for telegram to determine where to
  send the message", use `--to "telegram:<display-name>"` or
  `--to "telegram:<chat_id>"` (the chat_id form works but the bot
  needs to have seen that chat — a bare chat_id with no prior message
  history returns "Chat not found"). The display-name form is most
  reliable.
- **`--quiet` suppresses stdout on success, prints only on failure.**
  Always pair with `--quiet` in cron output and rely on exit code:
  `0 = delivered`, `1 = backend error` (network/auth/channel),
  `2 = usage error`.
- **Trigger-phrase blocklist catches quoted text inside message bodies.**
  Phrases like `hermes gateway restart` or `hermes update` inside the
  `-m` argument get matched by the command parser and the whole
  command is refused with
  `Blocked: cannot restart or stop the gateway from inside the gateway process.`
  even though they're just quoted prose. Phrase the alert as
  "restart the gateway" or "relaunch the gateway process" to avoid
  the false positive. The blocklist is at `command_allowlist` in
  `config.yaml`.
- **`hermes send` may trigger a stale auto-update recovery.** The first
  invocation after a crashed `hermes update` will print
  `⚠ A previous 'hermes update' was interrupted mid-install —
  finishing dependency installation now...` and may fail with
  `Access is denied. (os error 5)` on files locked by the live
  gateway (e.g. `venv\Lib\site-packages\PIL\_imaging.cp311-win_amd64.pyd`).
  The send itself usually still succeeds ("sent" at the end of
  output, exit 0) — the auto-recovery failure is a separate issue
  to flag in the report.
- **It is safe to send from cron even if the gateway is down or the
  bot token in `.env` looks masked** — `hermes send` reads from
  config.yaml directly.

## Anti-patterns to avoid

- ❌ Do NOT curl `api.telegram.org/bot<token>/...` directly from cron —
  you don't have the raw token (Hermes redacts it at the source) and
  the request will 404 anyway. Use `hermes send --to telegram` instead.
- ❌ Do NOT try to "fix" `~/.hermes/.env` if the token there looks
  masked — that's cosmetic; the real token lives in `config.yaml`.
- ❌ Do NOT retry `localhost:11434` if Ollama isn't installed (and isn't
  expected to be) — wasted calls, noise in logs.
- ❌ Do NOT propose fixes that require raw token access from cron.
- ❌ Do NOT swallow failures silently — the whole point of the cron is to
  surface them. If something is wrong, say so in the report.
- ❌ Do NOT call the headless-backend response an error. That string is the
  healthy response shape.
- ❌ Do NOT embed trigger phrases like `hermes gateway restart` inside a
  `hermes send` message body — the command parser will refuse the whole
  send. Rephrase.

## References

- `references/hermes-logs-layout.md` — what each `logs/*.log` contains, when to read which one, and how to filter for specific subsystems.
- `references/driver-windows-update-healthcheck.md` — **Driver version & Windows Update probes**: NVIDIA/Intel GPU driver age thresholds, Realtek audio pending updates, Windows Update COM API patterns, automated healthcheck integration for cron.
- `references/telegram-token-rejected.md` — the exact reproduction recipe
  for diagnosing token rejection, including the foreground-only fix path.

## Scripts

- `scripts/probe-hermes-port.ps1` — find which port Hermes is actually on
  (it picks dynamically with `--port 0`). Reusable from any cron health
  check.
- `scripts/quick-healthcheck.ps1` — self-contained one-shot probe covering
  disk, Ollama (4-state matrix), Hermes process, and Telegram state.json.
  Designed to be invoked via `-File` from MSYS bash; never inline its
  PowerShell with `$_` through `-Command` (MSYS bash will mangle it — see
  Environment gotchas).
- `scripts/send-telegram-cron.sh` — wrapper around `hermes send` for
  cron-side alerts. Pins the channel target to `telegram:P Sunny`
  (verify with `hermes send --list telegram`), uses `--quiet`, and
  relies on exit code (0 = delivered, 1 = backend, 2 = usage).
  Embedding trigger phrases like `hermes gateway restart` in the
  message body will be caught by the command-parser blocklist and
  refuse the whole send — rephrase in your alerts.
