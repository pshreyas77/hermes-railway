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

# Startup script:
#   1) Write .env from injected environment variables
#   2) Clone vault from GitHub (with retry, longer timeout)
#   3) Verify vault exists and has markdown files
#   4) Launch gateway (vault MUST be ready first)
RUN printf '#!/bin/sh\necho "[start.sh] $(date) - Starting"\nset +e\nmkdir -p ~/.hermes\ncat > ~/.hermes/.env <<EOF2\nNVIDIA_API_KEY=${NVIDIA_API_KEY}\nTELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}\nTELEGRAM_CHAT_ID=${TELEGRAM_CHAT_ID}\nTELEGRAM_ADMIN_CHAT_IDS=${TELEGRAM_ADMIN_CHAT_IDS}\nGATEWAY_ALLOW_ALL_USERS=${GATEWAY_ALLOW_ALL_USERS}\nOBSIDIAN_VAULT_PATH=/vault\nEOF2\necho "[start.sh] .env written"\n\n# Clone vault with retry logic\necho "[start.sh] Cloning Obsidian vault..."\nVAULT_READY=0\nfor attempt in 1 2 3; do\n  echo "[start.sh] Attempt $attempt of 3"\n  if [ -d /vault/.git ]; then\n    echo "[start.sh] Vault exists, pulling latest..."\n    timeout 60 git -C /vault pull --depth=1 --ff-only 2>&1 | tail -3\n  else\n    echo "[start.sh] Cloning vault from GitHub..."\n    timeout 180 git clone --depth=1 https://github.com/pshreyas77/MYOBSIDIAN-VAULT.git /vault 2>&1 | tail -5\n  fi\n  \n  if [ -d /vault ]; then\n    VAULT_FILES=$(find /vault -name "*.md" -type f 2>/dev/null | wc -l)\n    echo "[start.sh] Vault has $VAULT_FILES markdown files"\n    if [ "$VAULT_FILES" -gt 0 ]; then\n      VAULT_READY=1\n      echo "[start.sh] ✅ Vault ready!"\n      break\n    fi\n  fi\n  echo "[start.sh] Vault not ready, retrying in 5s..."\n  sleep 5\ndone\n\nif [ "$VAULT_READY" -eq 0 ]; then\n  echo "[start.sh] ⚠️ WARNING: Vault clone failed after 3 attempts, launching gateway anyway"\nfi\n\necho "[start.sh] Launching gateway..."\nexec hermes gateway run --no-supervise\n' > /home/hermes/start.sh && chmod +x /home/hermes/start.sh

# Expose gateway port
EXPOSE 8000

# Environment variables to bind gateway to 0.0.0.0:8000
ENV HERMES_GATEWAY_HOST=0.0.0.0
ENV HERMES_GATEWAY_PORT=8000

# Run startup script
CMD ["/home/hermes/start.sh"]
