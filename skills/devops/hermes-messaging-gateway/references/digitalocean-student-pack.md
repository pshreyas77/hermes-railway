---
title: DigitalOcean Student Pack Setup (via GitHub Education)
description: Complete guide to activating and using the DigitalOcean $200 credit from GitHub Student Developer Pack for Mumbai droplets
category: cloud-deployment
version: 1.0.0
---

# DigitalOcean Student Pack Setup Guide

## Overview
- **Credit**: $200 (equivalent to ~33 months on $6/mo Basic droplet)
- **Region**: Mumbai (BLR1) available ✅
- **Eligibility**: Verified GitHub Student Developer Pack (approved July 31, 2026)
- **Payment**: Auto-deducts from credit — **no card needed** if credit covers it
- **Validity**: 12 months from activation, then expires

---

## Prerequisites
- GitHub Student Developer Pack **verified** (status: "Verified (benefits available)")
- GitHub account linked to personal email (pshreyas.work@gmail.com)
- College email for verification: `22r21a05q2@mlrit.ac.in` (MLR Institute of Technology)

---

## Activation Steps

### 1. Get the Offer from GitHub Education
1. Open: https://education.github.com/pack
2. Sign in with **GitHub** (personal email)
2. Scroll to **DigitalOcean** section
3. Click **"Get Student Developer Pack offer"**
4. Redirects to DigitalOcean signup page

### 2. Create DigitalOcean Account
- Click **"Sign up with GitHub"** (auto-verifies student status)
3. Authorize DigitalOcean to access GitHub profile
4. Complete email verification
5. **$200 credit** appears automatically in Billing → Credits

### 3. Create Mumbai Droplet
1. Dashboard → **Create** → **Droplets**
4. **Region**: **BLR1 (Mumbai)** ← critical for Hyderabad latency
5. **Image**: **Ubuntu 24.04 LTS** (or 22.04 LTS)
6. **Size**: **Basic** → **Regular** → **$6/mo**
   - 1 vCPU, 1 GB RAM, 25 GB SSD, 1 TB transfer
   - **Alternative**: $12/mo for 2 GB RAM if running heavier workloads
7. **Authentication**: Password (simpler) or SSH Key (more secure)
   - **Password**: Set strong root password
   - **SSH Key**: Add `~/.ssh/id_ed25519.pub` for key-only access
8. **Hostname**: `hermes-bot-mumbai` (or your choice)
9. Click **Create Droplet** (~60 seconds)

### 4. Post-Creation
- Note **Public IP** (e.g., `164.90.xxx.xxx`)
- Note **Root password** (if password auth)
- Droplet ready in ~1 minute

---

## Cost Analysis

| Droplet Size | Monthly | Credit Duration | RAM | vCPU | Best For |
|--------------|---------|-----------------|-----|------|----------|
| **Basic $6** | $6/mo | **33 months** | 1 GB | 1 | Hermes bot + light workloads |
| **Basic $12** | $12/mo | 16 months | 2 GB | 1 | Hermes + local embeddings |
| **Basic $24** | $24/mo | 8 months | 4 GB | 2 | Heavy local processing |

---

## SSH Access

### Password Auth
```bash
ssh root@<PUBLIC_IP>
# Enter password from creation
```

### SSH Key Auth (Recommended)
```bash
# Local: generate key if needed
ssh-keygen -t ed25519 -C "hermes-bot-mumbai"

# Add to DigitalOcean: Settings → Security → SSH Keys → Add Key
# Paste contents of ~/.ssh/id_ed25519.pub

# Then SSH:
ssh root@<PUBLIC_IP>
```

---

## Hermes Bot Setup (Post-Droplet)

### One-Command Setup Script
```bash
# Run as root on droplet
curl -fsSL https://raw.githubusercontent.com/user/hermes-cloud-setup/main/setup.sh | bash
```

Or manual steps:
```bash
# 1. Install Docker
curl -fsSL https://get.docker.com | sh

# 2. Create Hermes config
mkdir -p /opt/hermes
cat > /opt/hermes/.env <<EOF
TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN"
TELEGRAM_ALLOWED_USERS="8336840601,8336840501"
HERMES_CONFIG=/opt/hermes/config.yaml
EOF

# 3. Pull and run Hermes
docker run -d \
  --name hermes \
  --restart unless-stopped \
  --env-file /opt/hermes/.env \
  -v /opt/hermes:/root/.hermes \
  ghcr.io/nousresearch/hermes-agent:latest

# 4. Verify
docker logs -f hermes
```

---

## Credit Monitoring
- **Dashboard**: Billing → Credits
- **CLI**: `doctl billing credits list` (if doctl configured)
- **Alert**: Set billing alert at $50 remaining

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **Offer not showing** | Ensure GitHub Student Pack shows "Verified (benefits available)" |
| **Credit not applied** | Wait 10 min, refresh; contact DO support if persists |
| **Mumbai region missing** | Select "Bangalore" (BLR1) — same datacenter |
| **SSH timeout** | Check firewall: Networking → Firewalls → Allow port 22 |
| **Droplet stuck** | Power cycle: Power Off → Power On in DO dashboard |

---

## Migration Path (When Credit Expires)
1. **Renew Student Pack** (next year) → fresh $200 credit
2. **Migrate to Hetzner CX22** (€3.99/mo, Germany, UPI accepted)
3. **Azure Students** (if verified by then) — free B1s in Mumbai

---

## Related Resources
- [GitHub Student Pack](https://education.github.com/pack)
- [DigitalOcean Student Offer](https://www.digitalocean.com/github-students)
- [doctl CLI](https://docs.digitalocean.com/reference/doctl/)
- [Hermes Agent Docker](https://github.com/nousresearch/hermes-agent)
- [Mumbai Region Guide](https://docs.digitalocean.com/products/platform/availability-matrix/)