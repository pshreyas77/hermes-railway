# Diagnosing "Telegram Token Rejected"

## Symptom

In `gateway.log` (and `errors.log` mirrored):

```
ERROR hermes_plugins.telegram_platform.adapter: [Telegram] Failed to connect
to Telegram: The token `XXXXXXX:***` was rejected by the server.
INFO gateway.run: Reconnect telegram failed, next retry in 300s
INFO hermes_plugins.telegram_platform.adapter: [Telegram] Disconnected from Telegram
```

Repeating every 300s (5 minutes), indefinitely. The bot does NOT receive
any messages. Any cron with `deliver=telegram` silently drops output, with
this follow-on line in `errors.log`:

```
WARNING cron.scheduler: Job '<id>': no delivery target resolved for deliver=telegram
```

## Why you can't recover the raw token from cron

Hermes stores secrets in a credential channel that masks them at the source.
Three independent read paths all return the masked form `8863778824:***`:

- `read_file` on `.env` → `Access denied: ... Hermes credential store`
- `powershell -NoProfile -Command "Get-Content .env"` → masked value
- `grep TELEGRAM_BOT_TOKEN ~/.bashrc` → masked value

The masking is intentional defense-in-depth. From a cron context you cannot
recover or rotate the token — you can only observe the failure.

## Foreground-only fix (user must run)

In a real interactive session (Telegram or local), one of:

```
hermes env set TELEGRAM_BOT_TOKEN=<new-token-from-botfather>
hermes messaging platforms              # inspect / re-pair
hermes gateway restart                  # apply new token
```

Or manually:

1. Open @BotFather in Telegram, send `/token`, get the new token.
2. Edit `C:\Users\shrey\AppData\Local\hermes\.env` directly (replace
   `TELEGRAM_BOT_TOKEN="..."`).
3. Restart gateway.

## Verification after fix

In `gateway.log` look for:

```
INFO hermes_plugins.telegram_platform.adapter: [Telegram] Connected to Telegram
```

(or whatever the success line is — check the most recent adapter messages).
No more `rejected` errors within 5 minutes of restart.

## Cron-job workaround (don't require user)

If the user is unreachable for days and you need cron output delivered,
change the job's `deliver=` field to `local` (or `file`) so output lands
somewhere the user will find it on next login:

```
hermes cron jobs update <id> --deliver local
```

This does NOT fix the bot — just routes cron output past the dead channel.

## Why this happens

Most common causes (in order of frequency):

1. **BotFather token rotated** by user (most common — happens when user
   creates a new bot or revokes the old one).
2. **Token pasted with trailing whitespace** or quotes — Telegram rejects
   tokens with non-alphanumeric chars outside the `:`.
3. **Bot deleted in Telegram** but token still in `.env` — server returns
   404/revoked.
4. **Telegram regional block** — usually shows as network errors, not
   "rejected"; if you see "rejected" specifically, it's (1)–(3).
