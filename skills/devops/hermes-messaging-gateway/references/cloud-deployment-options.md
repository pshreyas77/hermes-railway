# Cloud Deployment Options for 24/7 Hermes Agent

## Executive Summary (Aug 2026)

For a student in Hyderabad (India) wanting true 24/7 Telegram bot + general Hermes access without laptop dependency:

| Option | Cost | Timeline | Card Needed? | Specs | Verdict |
|--------|------|----------|--------------|-------|---------|
| **Azure for Students** | **₹0 (12 mo)** | ~2 days after GitHub Student Pack approval | **NO** | 1 vCPU, 4GB RAM, Mumbai region | ✅ **BEST FREE** |
| **Hetzner CX22** | ₹360/mo | Today | Yes (UPI works) | 2 vCPU, 4GB RAM, 40GB SSD, Germany | ✅ Best paid, instant |
| **Oracle Cloud Free Tier** | ₹0 forever | Weeks (ARM lottery) | Yes (credit card) | 4 ARM cores, 24GB RAM, 200GB, Mumbai | ⚠️ Capacity lottery |
| **AWS/GCP/Azure Free Tiers** | 12 mo then paid | Today | Yes | 1GB RAM, weak | ❌ Too weak for Hermes |

---

## Recommended Path: Azure for Students

### Prerequisites
1. GitHub account
2. College email (`@college.edu.in`) or student ID card
3. Apply at https://education.github.com/pack
4. Wait 72 hours after approval → Azure for Students activates

### Benefits
- $100 Azure credit (12 months)
- **No credit card required**
- Mumbai region = low latency from Hyderabad
- B1s VM (1 vCPU, 4GB RAM) fits in free tier
- Can run Docker + Hermes Agent 24/7

### VM Setup (What the Agent Does)
```bash
# On fresh Ubuntu 22.04/24.04 VM in Mumbai:
# 1. Install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# 2. Create Hermes Docker Compose
cat > docker-compose.yml << 'EOF'
version: '3.8'
services:
  hermes:
    image: ghcr.io/nousresearch/hermes-agent:latest
    container_name: hermes
    restart: unless-stopped
    environment:
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - TELEGRAM_ALLOWED_USERS=8336840601,8336840501
      - HERMES_VAULT_PATH=/vault
    volumes:
      - ~/.hermes:/root/.hermes
      - ./vault:/vault
    ports:
      - "8644:8644"
    deploy:
      resources:
        limits:
          memory: 2G
EOF

# 3. Add vault sync (git pull cron)
# 4. Start: docker compose up -d
# 5. Systemd service for auto-start
```

---

## Fallback: Hetzner CX22 (₹360/mo)

If Azure Students fails or you need it TODAY:
- Sign up at hetzner.com (accepts UPI/netbanking)
- Create CX22 in Nuremberg or Helsinki (closest to India)
- Same Docker setup above
- Cancel anytime

---

## Oracle Cloud Free Tier — The Trap

**Specs look amazing:** 4 OCPU ARM, 24GB RAM, 200GB SSD, Mumbai region, FREE FOREVER

**Reality:**
- ARM instances **almost always "Out of capacity"**
- Requires credit card for verification (not charged)
- Oracle **reclaims idle instances** (7 days <10% CPU = deleted)
- Need cron job to prevent reclaim:
  ```bash
  # Add to crontab on Oracle VM
  */6 * * * * /usr/bin/timeout 30s stress-ng --cpu 1 --cpu-load 15 >/dev/null 2>&1
  ```
- Many wait **weeks** for capacity

**Verdict:** Try if you have time, but don't count on it.

---

## Architecture: PC + Cloud Hybrid

```
PC (Native Hermes)          Cloud VM (Docker Hermes)
─────────────────           ────────────────────────
Interactive coding          24/7 Telegram bot
Local LLM (GPU)             Cron jobs / scheduled tasks
Obsidian vault (E:)         Webhook endpoints
Computer-use control        Remote access from phone
Git push                    Git pull (vault mirror)
```

**No "switch" needed.** Run native on PC for you. Run Docker on cloud for bot. Both free (Azure Students).

---

## Student Card Issues

| Card Type | Works on Oracle/Hetzner/Azure? |
|-----------|--------------------------------|
| SBI RuPay | ❌ No (domestic only) |
| SBI Visa/MC Debit | ✅ If international enabled |
| HDFC/ICICI Visa Debit | ✅ Usually |
| Wise Virtual Card | ✅ (15 min KYC, free) |
| **Azure Students** | **No card at all** |

---

## Quick Commands Reference

```bash
# Check Azure Students status
# Visit: https://education.github.com/pack → "Azure for Students"

# Provision Azure VM (after approval)
az login
az group create --name hermes-rg --location centralindia
az vm create --resource-group hermes-rg --name hermes-vm \
  --image Ubuntu2204 --size Standard_B1s --admin-username hermes \
  --generate-ssh-keys

# SSH in and run Docker setup
ssh hermes@<public-ip>

# Verify Telegram bot from cloud
curl -s https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMe | jq .ok
```

---

## Related Skills
- `hermes-messaging-gateway` — Telegram bot setup, allowlists, troubleshooting
- `hermes-agent` — Core Hermes CLI, config, updates
- `devops/hermes-messaging-gateway` — This skill's parent umbrella