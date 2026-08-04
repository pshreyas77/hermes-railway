# Obsidian Cross-Device Sync: Vault Anywhere for Free

This doc covers free, self-hosted paths to access your Obsidian vault from iOS and anywhere else — no cloud subscription, no data leaving your own infrastructure.

---

## The Problem

Obsidian's official Sync costs $8/mo. This doc covers alternatives that are $0.

---

## Option 1 — Obsidian Git + GitJournal (Recommended)

**Best for:** Desktop + iOS, GitHub already in use, zero ongoing cost.

### Desktop Side

1. **Install Obsidian Git plugin** (in-app only — no CLI):
   - Open Obsidian → Settings → Community Plugins → Browse → search `obsidian-git` → Install → Enable
   - Configure:
     - `Auto backup interval`: `5` minutes
     - `Auto commit message`: `vault backup {date}`
     - `Auto pull after checkout`: ✅ on

2. **Push vault to GitHub** (if not already):
   ```bash
   cd E:/_Knowledge/ObsidianVault
   git init
   git remote add origin https://github.com/YOUR_USERNAME/obsidian-vault.git
   git add .
   git commit -m "initial vault"
   git branch -M main
   git push -u origin main
   ```

3. **Enable 2FA on GitHub** before pushing sensitive notes (your vault contains personal research).

### iOS Side

1. Download **GitJournal** (free on App Store)
2. On first open → **Clone Git Repo** → paste your GitHub repo URL
3. Authenticate with GitHub (personal access token or OAuth)
4. Vault syncs. Edit any note → GitJournal auto-commits and pushes.

### How edits flow

```
PC: edit note → Obsidian Git pushes → GitHub
iPhone: GitJournal pulls → edit → GitJournal pushes → PC pulls on next cycle
```

**Pros:** Free, version-controlled, no third-party server
**Cons:** Not real-time (5-min lag on PC side); needs manual pull on iOS

---

## Option 2 — Syncthing on a VPS (~$3–5/mo)

**Best for:** Real-time two-way sync, multiple devices, slightly more reliable.

### Server Side (cheap VPS: Hetzner, Contabo)

```bash
# On VPS (Ubuntu)
curl -sSL https://github.com/syncthing/syncthing/releases/latest/download/linux-amd64.tar.gz | tar xz
cd syncthing-linux-amd64-*  # rename for convenience
./syncthing &
```

Configure: `https://YOUR_VPS:8384` → Actions → Show ID

### Desktop Side

Install Syncthing on your PC → add VPS device ID → share vault folder.

### iOS Side

Install **Syncthing** (free) → add VPS device ID → receive vault folder.

### How edits flow

```
PC ←→ VPS (Syncthing, real-time) ←→ iPhone
```

**Pros:** Real-time, no Git knowledge needed
**Cons:** VPS costs money; slightly more complex setup

---

## Option 3 — iCloud (Free but PC ≠ Mac)

If you ran Obsidian on a **Mac**, vault in iCloud = instant free sync to iOS.

**Doesn't apply** if your primary desktop is Windows/Linux.

---

## Vault Preparation Before Syncing

### .gitignore (exclude sensitive/binary files)

Create `E:/_Knowledge/ObsidianVault/.gitignore`:

```
# Obsidian system files
.trash/
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/graph.json

# Attachments (optional — large binary files)
!**/*.png
!**/*.jpg
!**/*.pdf
*.zip
*.mp4

# OS
.DS_Store
Thumbs.db

# Temporary
*.tmp
*.bak
```

### Security Checklist Before Going Mobile

- [ ] Enable 2FA on GitHub
- [ ] Add `.gitignore` and commit it BEFORE pushing sensitive notes
- [ ] Never commit `.env` files, API keys, or credentials
- [ ] Consider a separate `public-vault/` subset for truly public work
- [ ] Obsidian Git plugin settings → `Do not back up mobile apps` → ✅ on

---

## Quick Decision Guide

| Need | Best Option |
|------|-------------|
| PC + iPhone, free, version-controlled | Obsidian Git + GitJournal |
| Multiple PCs + iPhone, real-time, ~$4/mo | Syncthing on VPS |
| Mac + iPhone, free | iCloud |
| Research vault with 50k+ nodes, already on GitHub | Obsidian Git + GitJournal |

---

## Vault Status (Shrey's Current Setup)

- Vault: `E:/_Knowledge/ObsidianVault`
- Already on GitHub: likely yes (based on existing git workflow)
- iOS access: not yet configured
- **Recommended next step:** Install Obsidian Git plugin in-app, push to GitHub, clone in GitJournal