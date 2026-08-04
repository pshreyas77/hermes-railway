# Hermes Log Layout

Canonical log locations for a Hermes Agent installation on Windows:

```
C:\Users\<user>\AppData\Local\hermes\logs\
├── gateway.log              # Main gateway process log — Telegram connection, REST, lifecycle
├── gateway.log.1            # Rotated previous run (file size capped)
├── errors.log               # Cross-cutting errors + cron job warnings
├── errors.log.1             # Rotated previous errors
├── gateway-exit-diag.log    # Stack traces on abnormal exit
├── gateway-stdio.log        # stdin/stdout chatter for the gateway subprocess
├── gateway-restart.log      # Restart trigger events
├── gui.log                  # Desktop GUI app
├── tui_gateway_crash.log    # TUI-specific crashes
├── hermes-update.log        # Self-updater
└── update.log               # Package-level update events
```

## What to grep where

| Want to know about...                  | File                      | Pattern                                  |
|----------------------------------------|---------------------------|------------------------------------------|
| Telegram connection state              | `gateway.log`             | `Telegram|rejected|Reconnecting`         |
| Cron job run history                   | `errors.log`              | `cron.scheduler|cron_<jobid>`            |
| Provider API failures (502/504/etc.)   | `errors.log`              | `API call failed|provider=`              |
| Tool executor errors                   | `errors.log`              | `agent.tool_executor: Tool .* returned`  |
| Tool-availability warnings             | `errors.log`              | `tools.registry: check_fn .* returned`   |
| Gateway lifecycle (starts/crashes)     | `gateway.log`             | `Starting Hermes Gateway|gateway.run`    |
| Skill loader warnings                  | `errors.log`              | `skill not found, skipping`              |

## Reading tips

- Use `Get-Content ... -Tail N` from PowerShell, NOT bash `tail`, because
  `-Tail` works on locked files; bash tail on a locked file returns empty.
- If `gateway.log` is huge, narrow with `Select-String -Pattern ...` rather
  than dumping the whole file.
- Lines are formatted `<timestamp>,<ms> <LEVEL> <logger>: <message>` — easy
  to grep by timestamp if you need a window.
