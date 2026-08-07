FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    ca-certificates \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Install Hermes with messaging extra (for Telegram)
RUN pip install --no-cache-dir "hermes-agent[messaging]"

# Create non-root user with bash shell
RUN useradd -m -u 1000 -s /bin/bash hermes

# Create /vault directory and set ownership to hermes
RUN mkdir -p /vault && chown hermes:hermes /vault

USER hermes
WORKDIR /home/hermes

# Create .hermes directory and copy config
RUN mkdir -p ~/.hermes
COPY --chown=hermes:hermes config.yaml /home/hermes/.hermes/config.yaml
COPY --chown=hermes:hermes skills /home/hermes/.hermes/skills

# Create vault sync script
RUN cat > /home/hermes/sync_vault.sh << 'SHEOF'
#!/bin/sh
# Sync vault from GitHub - runs every hour in background
while true; do
    if [ -d /vault/.git ]; then
        cd /vault
        git pull --depth=1 --ff-only 2>&1 | tail -2
        if [ $? -ne 0 ]; then
            echo "[sync] Pull failed, attempting fresh clone..."
            cd /
            rm -rf /vault
            mkdir -p /vault && chown hermes:hermes /vault
            git clone --depth=1 https://github.com/pshreyas77/MYOBSIDIAN-VAULT.git /vault 2>&1 | tail -2
        fi
    else
        echo "[sync] Cloning vault..."
        rm -rf /vault
        mkdir -p /vault && chown hermes:hermes /vault
        git clone --depth=1 https://github.com/pshreyas77/MYOBSIDIAN-VAULT.git /vault 2>&1 | tail -2
    fi
    if [ -d /vault ]; then
        VAULT_COUNT=$(find /vault -name "*.md" -type f 2>/dev/null | wc -l)
        echo "[sync] $(date) - Vault: $VAULT_COUNT markdown files"
    fi
    sleep 3600  # Wait 1 hour
done
SHEOF
RUN chmod +x /home/hermes/sync_vault.sh

# Create startup script
# Verify skills directory exists and list skills
RUN ls -la /home/hermes/.hermes/skills/ && ls -la /home/hermes/.hermes/skills/second_brain/

RUN cat > /home/hermes/start.sh << 'STARTEOF' 
#!/bin/sh
echo "[start.sh] $(date) - HERMES BOT STARTING"
set +e
mkdir -p ~/.hermes
cat > ~/.hermes/.env <<EOF2
NVIDIA_API_KEY=${NVIDIA_API_KEY}
TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
TELEGRAM_CHAT_ID=${TELEGRAM_CHAT_ID}
TELEGRAM_ADMIN_CHAT_IDS=${TELEGRAM_ADMIN_CHAT_IDS}
GATEWAY_ALLOW_ALL_USERS=${GATEWAY_ALLOW_ALL_USERS}
OBSIDIAN_VAULT_PATH=/vault
EOF2
echo "[start.sh] .env written"

# Start vault sync in background (runs every hour)
echo "[start.sh] Starting vault sync daemon..."
/home/hermes/sync_vault.sh > /tmp/sync.log 2>&1 &
SYNC_PID=$!
echo "[start.sh] Vault sync PID: $SYNC_PID"

# Clone vault (BLOCKING - must complete before gateway)
echo "[start.sh] Cloning Obsidian vault..."
VAULT_OK=0
for attempt in 1 2 3; do
  echo "[start.sh] Attempt $attempt/3"
  if [ -d /vault/.git ]; then
    echo "[start.sh] Vault exists, pulling latest..."
    timeout 60 git -C /vault pull --depth=1 --ff-only 2>&1 | tail -3
  else
    echo "[start.sh] Cloning vault from GitHub..."
    timeout 180 git clone --depth=1 https://github.com/pshreyas77/MYOBSIDIAN-VAULT.git /vault 2>&1 | tail -5
  fi
  
  if [ -d /vault ]; then
    VAULT_COUNT=$(find /vault -name "*.md" -type f 2>/dev/null | wc -l)
    echo "[start.sh] Vault has $VAULT_COUNT markdown files"
    if [ "$VAULT_COUNT" -gt 0 ]; then
      VAULT_OK=1
      echo "[start.sh] VAULT READY"
      break
    fi
  fi
  echo "[start.sh] Vault not ready, retrying..."
  sleep 5
done

if [ "$VAULT_OK" -eq 0 ]; then
  echo "[start.sh] WARNING: Vault clone failed, but launching gateway anyway"
fi

echo "[start.sh] Launching gateway on port 8000..."
# Launch gateway in background so we can set webhook after it's ready
hermes gateway run --no-supervise > /tmp/gateway.log 2>&1 &
GATEWAY_PID=$!
echo "[start.sh] Gateway PID: $GATEWAY_PID"

# Wait for gateway to be ready (poll the local webhook endpoint on 8000)
echo "[start.sh] Waiting for gateway to be ready..."
for i in {1..30}; do
  # Try to reach the gateway on 8000 - use the webhook path or root
  if curl -sf http://localhost:8000/webhooks/telegram > /dev/null 2>&1; then
    echo "[start.sh] Gateway is ready (webhook endpoint responding)!"
    break
  fi
  sleep 2
done

# Set webhook via Telegram API (using token from .env)
echo "[start.sh] Setting webhook..."
WEBHOOK_URL="https://hermes-bot.victoriousdesert-40e70367.koreacentral.azurecontainerapps.io/webhooks/telegram"
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook" \
  -d "url=${WEBHOOK_URL}" \
  -d "secret_token=hermes-webhook-secret-2026-08-06" \
  -d "drop_pending_updates=true" \
  -d "allowed_updates=["message","edited_message"]" \
  | tee /tmp/webhook_set.log
echo "[start.sh] Webhook set result: $(cat /tmp/webhook_set.log)"

# Wait for gateway (this keeps the container alive)
wait $GATEWAY_PID
STARTEOF
RUN chmod +x /home/hermes/start.sh

# Expose only port 8000
EXPOSE 8000

# Environment variables
ENV HERMES_GATEWAY_HOST=0.0.0.0
ENV HERMES_GATEWAY_PORT=8000

# Run startup script
CMD ["/home/hermes/start.sh"]
