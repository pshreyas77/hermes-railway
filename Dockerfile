FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
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

# Create startup script that writes .env from environment variables
RUN mkdir -p /home/hermes && printf '#!/bin/sh\nmkdir -p ~/.hermes\ncat > ~/.hermes/.env <<EOF\nNVIDIA_API_KEY=${NVIDIA_API_KEY}\nTELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}\nTELEGRAM_CHAT_ID=${TELEGRAM_CHAT_ID}\nTELEGRAM_ADMIN_CHAT_IDS=${TELEGRAM_ADMIN_CHAT_IDS}\nGATEWAY_ALLOW_ALL_USERS=${GATEWAY_ALLOW_ALL_USERS}\nEOF\necho "Wrote .env"\nexec hermes gateway run\n' > /home/hermes/start.sh && chmod +x /home/hermes/start.sh

# Expose gateway port
EXPOSE 8000

# Run startup script
CMD ["/home/hermes/start.sh"]