#!/bin/sh
# Startup script for Hermes bot
# Creates .env with API keys, then runs the gateway

set -e

# Create .hermes directory and .env file with secrets
mkdir -p ~/.hermes
cat > ~/.hermes/.env <<EOF
NVIDIA_API_KEY=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
TELEGRAM_BOT_TOKEN=8863778824:AAFo-dFCpYX2_lUv_Ru-WBzOdD0e77z4tps
TELEGRAM_CHAT_ID=8336840601
TELEGRAM_ADMIN_CHAT_IDS=8336840601,8336840501
GATEWAY_ALLOW_ALL_USERS=true
EOF

echo "Starting Hermes gateway..."
exec hermes gateway run
