#!/bin/sh
# cont-init.d script: runs BEFORE s6-overlay services start
# Writes .env from environment variables for the gateway service

set -e

echo "=== Hermes cont-init: writing .env from environment ==="

# The s6-overlay services run as 'hermes' user (UID 10000)
# We need to write to /opt/data/.hermes/.env (HERMES_HOME)
mkdir -p /opt/data/.hermes

cat > /opt/data/.hermes/.env <<EOF
NVIDIA_API_KEY=${NVIDIA_API_KEY}
TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
TELEGRAM_CHAT_ID=${TELEGRAM_CHAT_ID}
TELEGRAM_ADMIN_CHAT_IDS=${TELEGRAM_ADMIN_CHAT_IDS}
GATEWAY_ALLOW_ALL_USERS=${GATEWAY_ALLOW_ALL_USERS}
EOF

chown -R 10000:10000 /opt/data/.hermes
echo "Wrote .env to /opt/data/.hermes/.env"
ls -la /opt/data/.hermes/