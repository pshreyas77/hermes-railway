FROM nousresearch/hermes-agent:latest

# Switch to root to add our cont-init.d script
USER root

# Copy custom config and skills into the Hermes config directory
COPY --chown=10000:10000 config.yaml /opt/data/.hermes/config.yaml
COPY --chown=10000:10000 skills /opt/data/.hermes/skills

# Copy cont-init.d script to write .env from environment variables
COPY --chmod=0755 cont-init.d/01-write-env.sh /etc/cont-init.d/01-write-env.sh

# Switch back to hermes user
USER 10000

# The official image's ENTRYPOINT + s6-overlay will run our cont-init.d script,
# then start the gateway service automatically