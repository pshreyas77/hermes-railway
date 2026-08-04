---
name: hermes-azure-deploy
description: Deploy Hermes Telegram gateway 24/7 on Azure student credit.
version: 1.0.0
tags: [hermes, azure, deployment, telegram, docker, container-instances, app-service, student-credit]
platforms: [windows, linux, macos]
---

# Deploy Hermes to Azure for 24/7 Gateway Operation

Run Hermes with messaging gateways (Telegram, Discord, Slack, etc.) 24/7 on Azure using the **Azure for Students $100 credit**. Cheapest path: **Azure Container Instances (ACI)** ~$15-25/mo. App Service B1 ~$13/mo with better logs/scaling.

## Prerequisites

- Azure CLI installed (`winget install Microsoft.AzureCLI`)
- Azure for Students activated ($100 credit, expires 365 days)
- Hermes config.yaml with gateway platforms configured
- Docker Desktop or `docker` CLI for building image

## Quick Start

```bash
# 1. Login to Azure (device code works in WSL/Git Bash)
az login --use-device-code

# 2. Create resource group in India region (Mumbai = centralindia)
az group create --name hermes-rg --location centralindia

# 3. Build & push Docker image
# See templates/Dockerfile.hermes for the Dockerfile
docker build -f Dockerfile.hermes -t hermes-gateway .
docker tag hermes-gateway <your-acr>.azurecr.io/hermes-gateway:latest
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/hermes-gateway:latest

# 4. Deploy to Azure Container Instances (simplest, cheapest)
az container create \
  --resource-group hermes-rg \
  --name hermes-telegram \
  --image <your-acr>.azurecr.io/hermes-gateway:latest \
  --cpu 1 --memory 2 \
  --registry-login-server <your-acr>.azurecr.io \
  --registry-username <acr-username> \
  --registry-password <acr-password> \
  --environment-variables \
    HERMES_HOME=/app/hermes \
    MODEL_PROVIDER=nvidia \
    MODEL_BASE_URL=https://integrate.api.nvidia.com/v1 \
    TELEGRAM_BOT_TOKEN=<from-azure-keyvault> \
  --restart-policy Always \
  --dns-name-label hermes-telegram-<unique>

# 5. Or deploy to App Service (better logs, scaling, custom domain)
az webapp up \
  --resource-group hermes-rg \
  --name hermes-telegram \
  --plan hermes-plan \
  --sku B1 \
  --location centralindia \
  --docker-custom-image-name <your-acr>.azurecr.io/hermes-gateway:latest
```

## Required Environment Variables

| Variable | Source | Notes |
|----------|--------|-------|
| `TELEGRAM_BOT_TOKEN` | Azure Key Vault / App Settings | **Never in Dockerfile** |
| `HERMES_HOME` | `/app/hermes` | Persistent volume mount recommended |
| `MODEL_PROVIDER` | `nvidia` / `openrouter` / `anthropic` | |
| `MODEL_BASE_URL` | `https://integrate.api.nvidia.com/v1` | For NVIDIA |
| `DISPLAY_INTERFACE` | `tui` or empty | Headless gateway doesn't need TUI |
| `GATEWAY_TIMEOUT` | `0` | No timeout for 24/7 |
| `PLATFORMS_TELEGRAM_ENABLED` | `true` | Or set in config.yaml |

## Dockerfile Template

See `templates/Dockerfile.hermes` — optimized for headless gateway:
- Python 3.11 slim base
- Installs `hermes-agent` via pip
- Creates non-root user
- Runs `hermes gateway start` (not interactive chat)
- Health check endpoint on port 8080

## Cost Optimization for Student Credit

| Service | Config | Est. Monthly | Credit Duration |
|---------|--------|--------------|-----------------|
| ACI | 1 vCPU, 2GB, Always | ~$18 | 5.5 months |
| App Service B1 | 1 vCPU, 1.75GB, Always On | ~$13 | 7.5 months |
| App Service F1 (Free) | 1 vCPU, 1GB, 60 min/day | $0 | Forever (but sleeps) |

**Recommendation:** App Service B1 — better logging, custom domain, auto-scale, always-on. $100 covers ~7 months.

## Persistent Storage (HERMES_HOME)

Hermes needs persistent storage for:
- `state.db` (sessions, FTS5)
- `config.yaml` (or mount from ConfigMap)
- `.env` (secrets)
- `logs/`

**Options:**
1. **Azure File Share** mounted to `/app/hermes` (ACI & App Service)
2. **App Service built-in persistent storage** (`/home` persists)
3. **External SQLite** (Azure SQL / Cosmos DB) — advanced

## Secrets Management

**Never bake secrets into Docker image.** Use:
- **Azure Key Vault** + Key Vault references in App Settings
- **App Service Application Settings** (encrypted at rest)
- **ACI Environment Variables** with `--secure-environment-variables`

```bash
# Store secret in Key Vault
az keyvault secret set --vault-name hermes-kv --name telegram-token --value "8863778824:..."

# Reference in App Service
az webapp config appsettings set \
  --resource-group hermes-rg \
  --name hermes-telegram \
  --settings TELEGRAM_BOT_TOKEN="@Microsoft.KeyVault(SecretUri=https://hermes-kv.vault.azure.net/secrets/telegram-token/)"
```

## Monitoring & Logs

- **App Service:** `az webapp log tail --name hermes-telegram --resource-group hermes-rg`
- **ACI:** `az container logs --name hermes-telegram --resource-group hermes-rg`
- **Health check:** `curl https://hermes-telegram.azurewebsites.net/health` (add `/health` endpoint in Hermes)

## Common Pitfalls

| Issue | Fix |
|-------|-----|
| Container exits immediately | Use `hermes gateway start` not `hermes chat`; add `tail -f /dev/null` as fallback |
| Telegram webhook not receiving | Set webhook URL: `az webapp config appsettings set --settings TELEGRAM_WEBHOOK_URL=https://your-app.azurewebsites.net/telegram/webhook` |
| Gateway times out | Set `GATEWAY_TIMEOUT=0` in env vars |
| Config not found | Mount config.yaml via Azure File Share or bake minimal config in image |
| Out of memory | Increase to 2GB+ (ACI) or B2 tier (App Service) |
| **Azure for Students regional restrictions** | **Student subscriptions block ACR/App Service/ACI in many regions (incl. India Central). Workaround: use allowed regions (East US, West US 2, Southeast Asia, North Europe, etc.) OR fall back to DigitalOcean (Mumbai BLR1 works great, ~$6/mo from $200 student credit = 33 months free).** |
| ACR creation fails with `RequestDisallowedByAzure` | Policy restricts regions for student subs. Try `eastus`, `westus2`, `southeastasia`, `northeurope`. If all fail, use DigitalOcean. |

## Clean Up (When Credit Runs Low)

```bash
# Stop (keeps resources, saves money)
az container stop --name hermes-telegram --resource-group hermes-rg
# or
az webapp stop --name hermes-telegram --resource-group hermes-rg

# Delete everything
az group delete --name hermes-rg --yes --no-wait
```

## References

- Azure Container Instances docs: https://learn.microsoft.com/azure/container-instances
- App Service Linux docs: https://learn.microsoft.com/azure/app-service/containers
- Azure for Students: https://azure.microsoft.com/free/students
- Hermes gateway config: https://hermes-agent.nousresearch.com/docs/gateway
- **DigitalOcean fallback for student regional restrictions:** `references/digitalocean-fallback.md`