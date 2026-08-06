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

# Copy config, skills and startup script
COPY --chown=hermes:hermes config.yaml /home/hermes/.hermes/config.yaml
COPY --chown=hermes:hermes skills /home/hermes/.hermes/skills
COPY --chown=hermes:hermes start.sh /home/hermes/start.sh
COPY --chown=hermes:hermes health_server.py /home/hermes/health_server.py

RUN chmod +x /home/hermes/start.sh

# Expose gateway port
EXPOSE 8000

# Run startup script which writes .env and starts the gateway
CMD ["/home/hermes/start.sh"]
