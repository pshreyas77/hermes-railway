FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    ca-certificates \
    procps \
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

# Create health check server
RUN cat > /home/hermes/health_server.py << 'PYEOF'
from http.server import BaseHTTPRequestHandler, HTTPServer
import os, json, time, threading

START_TIME = time.time()

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            vault_info = self.check_vault()
            response = {
                'status': 'ok',
                'uptime_seconds': int(time.time() - START_TIME),
                'vault': vault_info,
                'gateway_port': 8000
            }
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response, indent=2).encode())
        elif self.path == '/vault-status':
            vault_info = self.check_vault()
            self.send_response(200 if vault_info['exists'] else 503)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(vault_info, indent=2).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def check_vault(self):
        if not os.path.exists('/vault'):
            return {'exists': False, 'markdown_files': 0, 'error': '/vault directory does not exist'}
        md_files = []
        for root, dirs, files in os.walk('/vault'):
            for f in files:
                if f.endswith('.md'):
                    md_files.append(os.path.join(root, f))
        return {
            'exists': True,
            'markdown_files': len(md_files),
            'sample_files': md_files[:5]
        }
    
    def log_message(self, format, *args):
        pass  # Suppress default logs

def run_server():
    server = HTTPServer(('0.0.0.0', 8080), HealthHandler)
    print('[health-server] Listening on port 8080')
    server.serve_forever()

if __name__ == '__main__':
    run_server()
PYEOF

# Create vault sync script
RUN cat > /home/hermes/sync_vault.sh << 'SHEOF'
#!/bin/sh
# Sync vault from GitHub - runs every hour via cron
while true; do
    if [ -d /vault/.git ]; then
        cd /vault
        git pull --depth=1 --ff-only 2>&1 | tail -2
        if [ $? -ne 0 ]; then
            echo "[sync] Pull failed, attempting fresh clone..."
            cd /
            rm -rf /vault
            git clone --depth=1 https://github.com/pshreyas77/MYOBSIDIAN-VAULT.git /vault 2>&1 | tail -2
        fi
    else
        echo "[sync] Cloning vault..."
        rm -rf /vault
        git clone --depth=1 https://github.com/pshreyas77/MYOBSIDIAN-VAULT.git /vault 2>&1 | tail -2
    fi
    if [ -d /vault ]; then
        VAULT_COUNT=$(find /vault -name "*.md" -type f 2>/dev/null | wc -l)
        echo "[sync] $(date) - Vault: $VAULT_COUNT markdown files"
    fi
    sleep 3600  # Wait 1 hour
done
SHEOF
RUN chmod +x /home/hermes/sync_vault.sh

# Create startup script:
# 1. Write .env
# 2. Start health server (background)
# 3. Start vault sync (background)
# 4. Clone vault (BLOCKING - must complete before gateway)
# 5. Verify vault has files
# 6. Launch gateway
RUN printf '#!/bin/sh\necho "[start.sh] $(date) - HERMES BOT STARTING"\nset +e\nmkdir -p ~/.hermes\ncat > ~/.hermes/.env <<EOF2\nNVIDIA_API_KEY=${NVIDIA_API_KEY}\nTELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}\nTELEGRAM_CHAT_ID=${TELEGRAM_CHAT_ID}\nTELEGRAM_ADMIN_CHAT_IDS=${TELEGRAM_ADMIN_CHAT_IDS}\nGATEWAY_ALLOW_ALL_USERS=${GATEWAY_ALLOW_ALL_USERS}\nOBSIDIAN_VAULT_PATH=/vault\nEOF2\necho "[start.sh] .env written"\n\n# Start health server in background\necho "[start.sh] Starting health server on port 8080..."\npython3 /home/hermes/health_server.py > /tmp/health.log 2>&1 &\nHEALTH_PID=$!\necho "[start.sh] Health server PID: $HEALTH_PID"\n\n# Start vault sync in background (runs every hour)\necho "[start.sh] Starting vault sync daemon..."\n/home/hermes/sync_vault.sh > /tmp/sync.log 2>&1 &\nSYNC_PID=$!\necho "[start.sh] Vault sync PID: $SYNC_PID"\n\n# Clone vault (BLOCKING - must complete before gateway)\necho "[start.sh] Cloning Obsidian vault..."\nVAULT_OK=0\nfor attempt in 1 2 3; do\n  echo "[start.sh] Attempt $attempt/3"\n  if [ -d /vault/.git ]; then\n    echo "[start.sh] Vault exists, pulling latest..."\n    timeout 60 git -C /vault pull --depth=1 --ff-only 2>&1 | tail -3\n  else\n    echo "[start.sh] Cloning vault from GitHub..."\n    timeout 180 git clone --depth=1 https://github.com/pshreyas77/MYOBSIDIAN-VAULT.git /vault 2>&1 | tail -5\n  fi\n  \n  if [ -d /vault ]; then\n    VAULT_COUNT=$(find /vault -name "*.md" -type f 2>/dev/null | wc -l)\n    echo "[start.sh] Vault has $VAULT_COUNT markdown files"\n    if [ "$VAULT_COUNT" -gt 0 ]; then\n      VAULT_OK=1\n      echo "[start.sh] VAULT READY"\n      break\n    fi\n  fi\n  echo "[start.sh] Vault not ready, retrying..."\n  sleep 5\ndone\n\nif [ "$VAULT_OK" -eq 0 ]; then\n  echo "[start.sh] WARNING: Vault clone failed, but launching gateway anyway"\nfi\n\necho "[start.sh] Launching gateway on port 8000..."\nexec hermes gateway run --no-supervise\n' > /home/hermes/start.sh && chmod +x /home/hermes/start.sh

# Expose ports
EXPOSE 8000
EXPOSE 8080

# Environment variables
ENV HERMES_GATEWAY_HOST=0.0.0.0
ENV HERMES_GATEWAY_PORT=8000

# Run startup script
CMD ["/home/hermes/start.sh"]
