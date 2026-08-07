#!/bin/sh
# Sync Obsidian vault from GitHub
# Runs every hour via cron to keep vault up-to-date

echo "[vault-sync] $(date) - Starting sync"

if [ -d /vault/.git ]; then
  cd /vault
  git pull --depth=1 --ff-only 2>&1 | tail -3
  if [ $? -eq 0 ]; then
    VAULT_FILES=$(find /vault -name "*.md" -type f 2>/dev/null | wc -l)
    echo "[vault-sync] ✅ Synced: $VAULT_FILES markdown files"
  else
    echo "[vault-sync] ⚠️ Pull failed, trying fresh clone..."
    cd /
    rm -rf /vault
    timeout 180 git clone --depth=1 https://github.com/pshreyas77/MYOBSIDIAN-VAULT.git /vault 2>&1 | tail -3
  fi
else
  echo "[vault-sync] Vault not found, cloning..."
  timeout 180 git clone --depth=1 https://github.com/pshreyas77/MYOBSIDIAN-VAULT.git /vault 2>&1 | tail -3
fi

if [ -d /vault ]; then
  VAULT_FILES=$(find /vault -name "*.md" -type f 2>/dev/null | wc -l)
  echo "[vault-sync] Final state: $VAULT_FILES markdown files"
fi
