---
name: obsidian-sync-doctor
description: Diagnose the Hermes Agent to Obsidian Sync loop on a VPS, including obsidian-headless, systemd service status, vault path mismatches, login or subscription issues, and two-way sync tests. Use when notes are not appearing on Mac, Telegram captures fail, or the video setup needs proof before recording.
---

# Obsidian Sync Doctor

## Overview

Diagnose the full loop: Hermes writes to the VPS vault folder, obsidian-headless syncs it, and Obsidian on the Mac receives it. Prefer concrete filesystem and service checks over vague advice.

## Diagnostic Order

1. Confirm the expected vault path.
2. Confirm `OBSIDIAN_VAULT_PATH` points to that exact path.
3. Confirm `ob` is installed and authenticated.
4. Confirm the vault folder is the folder configured by `ob sync-setup`.
5. Confirm `obsidian-sync.service` is active and enabled.
6. Inspect recent logs.
7. Run a one-off sync.
8. Optionally create a test note and sync it.
9. Ask the user to confirm the note appears on the Mac.
10. Ask the user to create a Mac note and confirm it appears on the VPS.

## Quick Command

Read-only check:

```bash
bash scripts/verify_hermes_obsidian_loop.sh --vault /root/HermesVault
```

Write a test note and run sync:

```bash
bash scripts/verify_hermes_obsidian_loop.sh --vault /root/HermesVault --write-test
```

## Common Diagnoses

- Notes created but not synced: service down, bad auth, wrong vault path, or wrong remote vault.
- Service active but no Mac note: Mac is on a different account or remote vault.
- `ob` missing: npm global bin is not on `PATH`, or obsidian-headless was not installed.
- Login failures: often inactive Obsidian Sync or wrong account.
- Vault at `/root`: setup was run from the wrong directory.

## Resources

- Read `references/diagnostic-playbook.md` for the full decision tree.
- Run `scripts/verify_hermes_obsidian_loop.sh` on the VPS.

## Completion Criteria

Finish only when the cause is identified or the user has a concrete next check, and the two-way sync test has either passed or failed with a specific reason.
