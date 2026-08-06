FROM nousresearch/hermes-agent:latest

# Switch to root to add our config
USER root

# Copy custom config and skills
COPY --chown=hermes:hermes config.yaml /home/hermes/.hermes/config.yaml
COPY --chown=hermes:hermes skills /home/hermes/.hermes/skills

# Create startup script that writes .env from environment variables
RUN printf '#!/bin/sh\nmkdir -p ~/.hermes\ncat > ~/.hermes/.env <<EOF\nNVIDIA_API_KEY=${NVIDIA_API_KEY}\nTELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}\nTELEGRAM_CHAT_ID=${TELEGRAM_CHAT_ID}\nTELEGRAM_ADMIN_CHAT_IDS=${TELEGRAM_ADMIN_CHAT_IDS}\nGATEWAY_ALLOW_ALL_USERS=${GATEWAY_ALLOW_ALL_USERS}\nEOF\necho "Wrote .env"\n' > /home/hermes/setup.sh && chmod +x /home/hermes/setup.sh

USER hermes

# The official image's ENTRYPOINT will run our setup.sh then start the gateway
CMD ["/home/hermes/setup.sh"]