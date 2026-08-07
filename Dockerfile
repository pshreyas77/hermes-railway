FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Hermes with messaging extra (for Telegram)
RUN pip install --no-cache-dir "hermes-agent[messaging]"

# Create non-root user with bash shell
RUN useradd -m -u 1000 -s /bin/bash hermes
USER hermes
WORKDIR /home/hermes

# Create .hermes directory and copy config
RUN mkdir -p ~/.hermes
COPY --chown=hermes:hermes config.yaml ~/.hermes/config.yaml
COPY --chown=hermes:hermes skills ~/.hermes/skills

# MINIMAL startup: just write .env and launch gateway
# Vault cloning moved to a separate background process to avoid blocking
RUN printf '#!/bin/sh\necho "[start.sh] $(date) - Writing .env"\nmkdir -p ~/.hermes\ncat > ~/.hermes/.env <<EOF2\nNVIDIA_API_KEY=${NVIDIA_API_KEY}\nTELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}\nTELEGRAM_CHAT_ID=${TELEGRAM_CHAT_ID}\nTELEGRAM_ADMIN_CHAT_IDS=${TELEGRAM_ADMIN_CHAT_IDS}\nGATEWAY_ALLOW_ALL_USERS=${GATEWAY_ALLOW_ALL_USERS}\nOBSIDIAN_VAULT_PATH=/vault\nEOF2\necho "[start.sh] .env written"\n\n# Clone vault in background (non-blocking, with timeout)\n(\n  echo "[vault-bg] Starting vault clone..."\n  timeout 120 git clone --depth=1 https://github.com/pshreyas77/MYOBSIDIAN-VAULT.git /vault 2>&1 | tail -5 || echo "[vault-bg] Clone failed or timed out"\n  if [ -d /vault ]; then\n    VAULT_FILES=$(find /vault -name "*.md" -type f 2>/dev/null | wc -l)\n    echo "[vault-bg] Vault ready: $VAULT_FILES markdown files"\n  fi\n) > /tmp/vault.log 2>&1 &\necho "[start.sh] Vault clone started in background (PID $!)"\n\n# Launch gateway IMMEDIATELY (don\xe2\x80\x99t wait for vault)\necho "[start.sh] Launching gateway..."\nexec hermes gateway run --no-supervise\n' > /home/hermes/start.sh && chmod +x /home/hermes/start.sh

# Expose gateway port
EXPOSE 8000

# Environment variables to bind gateway to 0.0.0.0:8000
ENV HERMES_GATEWAY_HOST=0.0.0.0
ENV HERMES_GATEWAY_PORT=8000

# Run startup script
CMD ["/home/hermes/start.sh"]
