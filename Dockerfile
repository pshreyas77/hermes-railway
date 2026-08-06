FROM nousresearch/hermes-agent:latest

# Switch to root to add our config
USER root

# Copy custom config and skills
COPY --chown=10000:10000 config.yaml /opt/data/.hermes/config.yaml
COPY --chown=10000:10000 skills /opt/data/.hermes/skills

USER 10000

# The official image's ENTRYPOINT handles everything
# We just need to run the gateway in the foreground
CMD ["hermes", "gateway", "run", "--no-supervise", "--force"]