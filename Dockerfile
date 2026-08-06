FROM nousresearch/hermes-agent:latest

# Switch to root to install our config
USER root

# Copy custom config and skills into the Hermes config directory
COPY --chown=hermes:hermes config.yaml /home/hermes/.hermes/config.yaml
COPY --chown=hermes:hermes skills /home/hermes/.hermes/skills
COPY --chown=hermes:hermes start.sh /home/hermes/start.sh

RUN chmod +x /home/hermes/start.sh

USER hermes

# Expose gateway port (Hermes gateway listens on 8000 by default in container)
EXPOSE 8000

# Run the Hermes gateway via startup script
CMD ["/home/hermes/start.sh"]