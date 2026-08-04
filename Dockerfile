FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Hermes
RUN pip install --no-cache-dir hermes-agent

# Create non-root user
RUN useradd -m -u 1000 hermes
USER hermes
WORKDIR /home/hermes

# Copy config
COPY --chown=hermes:hermes config.yaml ./
COPY --chown=hermes:hermes skills ./skills

# Expose gateway port
EXPOSE 8000

# Run Hermes gateway
CMD ["hermes", "gateway", "start", "--host", "0.0.0.0", "--port", "8000"]