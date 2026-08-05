FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Hermes with messaging extra
RUN pip install --no-cache-dir "hermes-agent[messaging]"

# Create non-root user
RUN useradd -m -u 1000 hermes
USER hermes
WORKDIR /home/hermes

# Copy config
COPY --chown=hermes:hermes config.yaml ./
COPY --chown=hermes:hermes skills ./skills

# Add health check server (runs on port 8000 for Azure health checks)
COPY --chown=hermes:hermes health_server.py ./

# Expose gateway port
EXPOSE 8000

# Hermes gateway listens on port 8000 and handles /health, /webhook, etc.
# Use exec form so the shell doesn't fork - the gateway is the main process.
CMD ["hermes", "gateway", "run", "--host", "0.0.0.0", "--port", "8000"]