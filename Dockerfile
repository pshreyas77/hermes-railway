FROM nousresearch/hermes-agent:latest

# Switch to root to install our config
USER root

# Copy custom config and skills into the Hermes config directory
COPY --chown=hermes:hermes config.yaml /home/hermes/.hermes/config.yaml
COPY --chown=hermes:hermes skills /home/hermes/.hermes/skills

USER hermes

# Expose gateway port (Hermes gateway listens on 8000 by default in container)
EXPOSE 8000

# Run the Hermes gateway in the foreground (s6-overlay will manage it)
CMD ["hermes", "gateway", "run", "--no-supervise", "--force"]
