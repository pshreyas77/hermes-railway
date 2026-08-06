#!/bin/sh
# Startup script for official hermes-agent image with s6-overlay
# Creates .env from environment variables, then starts gateway

# Create .hermes directory
mkdir -p ~/.hermes

# Write .env with secrets from environment variables
cat > ~/.hermes/.env <<EOF
NVIDIA_API_KEY=${NVIDIA_API_KEY}
TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
TELEGRAM_CHAT_ID=${TELEGRAM_CHAT_ID}
TELEGRAM_ADMIN_CHAT_IDS=${TELEGRAM_ADMIN_CHAT_IDS}
GATEWAY_ALLOW_ALL_USERS=${GATEWAY_ALLOW_ALL_USERS}
EOF

echo "Wrote .env file from environment variables"
ls -la ~/.hermes/

echo "Starting Hermes gateway..."
exec hermes gateway run --no-supervise --force