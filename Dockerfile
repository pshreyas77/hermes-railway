FROM python:3.11-slim

# Install system dependencies (git is already there; we add ca-certificates for HTTPS)
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

# Create startup script:
#   1) Write .env from injected environment variables
#   2) Clone the latest Obsidian vault from GitHub (shallow clone = fast)
#   3) Set OBSIDIAN_VAULT_PATH so Hermes tools know where to read notes
#   4) Launch the gateway
RUN printf '#!/bin/sh\nset -e\nmkdir -p ~/.hermes\ncat > ~/.hermes/.env <<EOF2\nNVIDIA_API_KEY=${NVIDIA_API_KEY}\nTELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}\nTELEGRAM_CHAT_ID=${TELEGRAM_CHAT_ID}\nTELEGRAM_ADMIN_CHAT_IDS=${TELEGRAM_ADMIN_CHAT_IDS}\nGATEWAY_ALLOW_ALL_USERS=${GATEWAY_ALLOW_ALL_USERS}\nOBSIDIAN_VAULT_PATH=/vault\nEOF2\necho "Wrote .env"\n\n# Clone (or update) the Obsidian vault from GitHub\necho "Cloning Obsidian vault from GitHub..."\nif [ -d /vault/.git ]; then\n  cd /vault && git pull --depth=1 --ff-only 2>&1 | tail -3\nelse\n  git clone --depth=1 https://github.com/pshreyas77/MYOBSIDIAN-VAULT.git /vault 2>&1 | tail -3\nfi\necho "Vault ready at /vault ($(ls /vault | wc -l) top-level entries)"\n\nexec hermes gateway run --no-supervise\n' > /home/hermes/start.sh && chmod +x /home/hermes/start.sh

# Expose gateway port
EXPOSE 8000

# Environment variables to bind gateway to 0.0.0.0:8000
ENV HERMES_GATEWAY_HOST=0.0.0.0
ENV HERMES_GATEWAY_PORT=8000

# Run startup script
CMD ["/home/hermes/start.sh"]
