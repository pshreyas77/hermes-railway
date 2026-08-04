#!/usr/bin/env bash
# Send a Telegram alert from cron via `hermes send`.
# Usage: send-telegram-cron.sh "your message text"
#        send-telegram-cron.sh --subject "Header" "Body"
#
# Uses the display-name form of the channel (`hermes send --list telegram`)
# because the bare `telegram` target fails with "No home channel set for
# telegram to determine where to send the message" and the bare chat_id
# form fails with "Chat not found" if the bot hasn't seen the chat.
#
# Avoid trigger-phrase blocklist (e.g. "hermes gateway restart") in the
# message body — the command parser matches those and refuses the send.

set -euo pipefail

CHANNEL="telegram:P Sunny"   # adjust if `hermes send --list telegram` shows a different name

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 [--subject HEADER] MESSAGE" >&2
  exit 2
fi

SUBJECT=""
if [[ "${1:-}" == "--subject" ]]; then
  SUBJECT="--subject $2"
  shift 2
fi

MSG="$*"

# --quiet keeps cron logs clean on success; rely on exit code.
hermes send --to "$CHANNEL" --quiet $SUBJECT "$MSG"
RC=$?

if [[ $RC -ne 0 ]]; then
  echo "[send-telegram-cron] FAILED exit=$RC channel=$CHANNEL" >&2
  echo "[send-telegram-cron] MSG was: $MSG" >&2
fi

exit $RC
