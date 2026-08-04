# DigitalOcean Fallback for Azure Student Regional Restrictions

**Problem:** Azure for Students subscriptions have strict regional policies that block ACR, App Service, and ACI in many regions (including India Central, Southeast Asia, East US, West US 2). Error: `RequestDisallowedByAzure`.

**Solution:** Use **DigitalOcean Mumbai (BLR1)** — already provisioned in user's account with $200 student credit (33 months free on $6/mo Basic droplet).

## Quick Deploy to DigitalOcean

### Prerequisites
```bash
# Install doctl
winget install DigitalOcean.doctl

# Authenticate (get token from https://cloud.digitalocean.com/account/api/tokens)
doctl auth init -t YOUR_TOKEN
```

### Create Droplet in Mumbai (BLR1)
```bash
# Create 1GB Basic droplet (AMD) in BLR1 (Mumbai)
doctl compute droplet create hermes-telegram \
  --region blr1 \
  --image ubuntu-22-04-x64 \
  --size s-1vcpu-1gb \
  --ssh-keys $(doctl compute ssh-key list --format ID --no-header) \
  --wait
```

### Deploy Hermes via Docker on Droplet
```bash
# SSH to droplet
ssh root@$(doctl compute droplet get hermes-telegram --format PublicIPv4 --no-header)

# Install Docker
curl -fsSL https://get.docker.com | sh

# Create Hermes directory
mkdir -p /opt/hermes && cd /opt/hermes

# Create docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'
services:
  hermes:
    image: ghcr.io/nousresearch/hermes-agent:latest
    container_name: hermes-gateway
    restart: always
    environment:
      - HERMES_HOME=/app/hermes
      - MODEL_PROVIDER=nvidia
      - MODEL_BASE_URL=https://integrate.api.nvidia.com/v1
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - GATEWAY_TIMEOUT=0
      - DISPLAY_INTERFACE=tui
    volumes:
      - ./data:/app/hermes
    ports:
      - "8080:8080"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
EOF

# Create .env with secrets
cat > .env << 'EOF'
TELEGRAM_BOT_TOKEN=8863778824:YOUR_ACTUAL_TOKEN_HERE
EOF

# Start
docker compose up -d

# Verify
docker compose logs -f hermes
```

### Cost Comparison
| Platform | Region | Spec | Monthly | Student Credit Duration |
|----------|--------|------|---------|------------------------|
| Azure ACI | East US (if allowed) | 1 vCPU, 2GB | ~$18 | 5.5 months |
| Azure App Service B1 | East US (if allowed) | 1 vCPU, 1.75GB | ~$13 | 7.5 months |
| **DigitalOcean Droplet** | **BLR1 (Mumbai)** | **1 vCPU, 1GB** | **~$6** | **33 months** |
| DigitalOcean Droplet | BLR1 (Mumbai) | 2 vCPU, 2GB | ~$12 | 16 months |

**Recommendation for this user:** DigitalOcean BLR1 1GB Basic — lowest latency from Hyderabad, longest credit duration, no regional restrictions.

### Persistent Storage
- Docker volume `./data:/app/hermes` persists `state.db`, `config.yaml`, logs
- Survives container restarts, droplet reboots
- For backups: `doctl compute droplet-action snapshot hermes-telegram --snapshot-name hermes-backup-$(date +%Y%m%d)`

### Monitoring
```bash
# View logs
docker compose logs -f hermes

# Health check
curl http://<droplet-ip>:8080/health

# System status
htop  # on droplet
```

### Auto-restart on Crash/Reboot
Docker `restart: always` handles this. For extra safety, add systemd service:
```bash
cat > /etc/systemd/system/hermes.service << 'EOF'
[Unit]
Description=Hermes Telegram Gateway
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/hermes
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

systemctl enable hermes
systemctl start hermes
```

### User's Specific Config (from session)
- Bot token: `8863778824:***` (in config.yaml)
- Admin chats: `8336840601`, `8336840501`
- Model: NVIDIA `minimaxai/minimax-m3` via `https://integrate.api.nvidia.com/v1`
- Platform: Telegram enabled