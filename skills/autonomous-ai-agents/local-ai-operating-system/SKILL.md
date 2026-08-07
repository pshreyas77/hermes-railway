---
name: local-ai-operating-system
description: "Build and operate a local-first AI operating system (Jarvis-style) using Hermes Agent as the brain, with graphify knowledge graphs, MemPalace verbatim memory, Obsidian vault structured memory, MCP tool integration, Telegram remote control, cron automation, and web dashboard. All local-first, zero cloud cost."
version: 1.0.0
author: Hermes Agent + User
license: MIT
platforms: [linux, macos, windows]
tags: [local-ai, jarvis, hermes, graphify, mempalace, obsidian, mcp, telegram, cron, dashboard, autonomous]
---

# Local AI Operating System (Jarvis Stack)

A complete, production-ready pattern for building a **local-first AI operating system** — an autonomous agent that doesn't just answer questions but *executes workflows* across your tools, remembers everything verbatim, builds knowledge graphs from your data, and runs autonomously on schedule. All local, zero cloud cost.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      LOCAL JARVIS                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   Telegram   │    │   Hermes     │    │   Obsidian   │      │
│  │   Gateway    │◄───│   Agent      │───►│   Vault      │      │
│  │  (Remote     │    │   (Brain)    │    │  (Structured │      │
│  │   Control)   │    │              │    │   Memory)    │      │
│  └──────────────┘    └──────┬───────┘    └──────┬───────┘      │
│                             │                   │              │
│                    ┌────────┴────────┐          │              │
│                    ▼                 ▼          ▼              │
│            ┌───────────────┐  ┌───────────────┐ ┌─────────┐    │
│            │  MemPalace    │  │   graphify    │ │ MCP     │    │
│            │  (Verbatim    │  │  (Knowledge   │ │ Servers │    │
│            │   Memory)     │  │   Graph)      │ │ (Hands) │    │
│            └───────────────┘  └───────────────┘ └─────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Core Components

| Layer | Technology | Purpose | Key Files |
|-------|------------|---------|-----------|
| **Brain** | Hermes Agent | LLM reasoning, tool use, session management | `~/.hermes/config.yaml` (profile: `jarvis`) |
| **Verbatim Memory** | MemPalace (Docker) | Exact conversation storage, semantic search | `/home/hermes/mempalace/docker-compose.yml` |
| **Structured Memory** | Obsidian Vault | Notes, MOCs, daily logs, research | `/vault/` |
| **Knowledge Graph** | graphify | 50k+ nodes, entity relationships, queries | `/vault/graphify-out/` |
| **Hands (Tools)** | MCP Servers | Terminal, Obsidian, Graphify, Browser | `/home/hermes/jarvis/mcp/` |
| **Remote Control** | Telegram Bot | `/brief`, `/graph`, `/run`, `/status` | `/home/hermes/jarvis/telegram/bot.py` |
| **Automation** | Hermes Cron | 6 scheduled jobs | `hermes cron list` |
| **Dashboard** | FastAPI + WS | Web UI, WebSocket, real-time | `/home/hermes/jarvis/dashboard/server.py` |

---

## Quick Start

```bash
# 1. Configure Telegram (one-time)
cp /home/hermes/jarvis/.env.template /home/hermes/jarvis/.env
# Edit .env with BOT_TOKEN and USER_ID from @BotFather / @userinfobot

# 2. Start everything
python /home/hermes/jarvis/launch_complete.py
```

**What starts:**
- MemPalace Docker (ChromaDB + API on :8081)
- 3 MCP servers (Terminal, Obsidian, Graphify)
- Web Dashboard at `http://localhost:8080`
- Telegram Bot (if configured)
- Hermes Jarvis CLI (profile: `jarvis`)

---

## Core Workflows

### 1. Content Pipeline (Primary)
```
Research Topic → graphify query → MemPalace search → 
Draft in Obsidian → Review → Publish
```

### 2. Daily Briefing (Automated)
```bash
# Runs at 7:00 AM via Hermes cron
graphify query "What are the most important updates in my vault today?"
→ Telegram summary with sections:
  📰 Research Updates
  🗳️ Political Updates  
  🧠 Knowledge Graph Insights
  📝 New Notes
```

### 3. Vault Maintenance (Automated)
```bash
# 2:00 AM daily
graphify update /vault  # incremental, no API cost
mempalace mine                               # new conversations → entities
```

### 4. GitHub Repo → Second Brain (Verified Recipe)

When the user asks to "wire X repo into my second brain" (or any variant — "mine this repo", "add it to the brain", "do it with my second brain"), this 5-step pipeline is the consolidated pattern. Verified end-to-end on `rahulnyk/knowledge_graph` (2026-07-26, 22 files → 1,968 palace drawers → 20-node graph).

```bash
# 1. Clone to E:
cd /home/hermes && git clone --depth=1 https://github.com/<owner>/<repo>.git
#    (or use the canonical cache: graphify clone <url> → ~/.graphify/repos/<owner>/<repo>/)

# 2. Update entities.json (project + author)
# /vault/entities.json — append to projects[], add author to people[]

# 3. Mine into MemPalace
cd /home/hermes/mempalace && ./mp.sh mine "/home/hermes/<repo>" --wing <short-name>
#    CLI: positional dir + --wing NAME. --folder/--room do NOT exist.

# 4. Graphify the repo itself
cd C:/Users/shrey/.graphify/repos/<owner>/<repo> && graphify update .
#    Bare `graphify <path>` errors with "unknown command '<path>'". Always cd first.

# 5. Write a wikilinked vault note
# /vault/wiki/<short-name>.md — tag `second-brain-source`,
#    link the palace wing + graphify-out path + repo URL
```

Each step is independent and short, so a failure at any stage is recoverable.
Full worked example (with verified outputs) lives in
[`references/github-repo-to-second-brain.md`](references/github-repo-to-second-brain.md).


---

## Key Implementation Patterns

### MCP Server Pattern (Reusable)
Each MCP server is a standalone Python async server exposing tools via stdio:

```python
# Pattern: tools/mcp/<name>/server.py
from mcp.server import Server
from mcp.types import Tool, TextContent

SERVER = Server("jarvis-<name>")

@SERVER.list_tools()
async def list_tools() -> List[Tool]:
    return [Tool(name="tool_name", description="...", inputSchema={...})]

@SERVER.call_tool()
async def call_tool(name: str, arguments: dict) -> List[TextContent]:
    if name == "tool_name":
        result = do_work(arguments)
        return [TextContent(type="text", text=json.dumps(result))]
```

**Created servers:** `terminal`, `obsidian`, `graphify`

### Telegram Bot Pattern
```python
# telegram/bot.py
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

async def graph_command(update, context):
    if not authorized(update): return
    query = " ".join(context.args)
    output = run_cmd(["graphify", "query", query, "--budget", "1500"])
    await update.message.reply_text(f"🔍 **Graph Query**: {query}\n\n{output}")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("graph", graph_command))
app.run_polling()
```

### Cron Job Pattern (Hermes)
```bash
# Daily briefing at 7 AM
hermes cron create "0 7 * * *" \
  --prompt "Generate daily briefing: query graphify for 'What are the most important updates in my vault today?' including recent research, JK elections, Dravidian movement, language families. Format as Telegram markdown with sections: 📰 Research, 🗳️ Politics, 🧠 Graph, 📝 Notes. Send via Telegram." \
  --skills "graphify,obsidian,memory,terminal" \
  --name "daily-briefing" \
  --deliver "telegram"
```

---

## Critical Fixes & Workarounds

### MemPalace NumPy/ChromaDB Fix
**Problem:** `numpy._core._multiarray_umath` import error on Python 3.13/3.14 due to ABI mismatch between system numpy (cp311) and isolated env (cp313/314).

**Solution:** Docker with pinned compatible versions.
```dockerfile
# Dockerfile
FROM python:3.13-slim
RUN apt-get update && apt-get install -y build-essential curl git && rm -rf /var/lib/apt/lists/*
COPY pyproject.toml uv.lock ./
COPY mempalace/ ./mempalace/
RUN uv sync --frozen --no-dev
```
```yaml
# docker-compose.yml
services:
  mempalace:
    build: .
    volumes:
      - ./data:/data
      - ./config:/config
    ports: ["8081:8081"]
  chromadb:
    image: chromadb/chroma:0.4.24
    volumes: ["./chroma_data:/chroma/chroma"]
    ports: ["8000:8000"]
```

**Key pins:** `numpy==1.24.3`, `chromadb==0.4.22` in `pyproject.toml`.

### E: Drive Enforcement
**Rule:** ALL installs, clones, builds, caches → `E:` drive. Never `C:`.
- Vault: `/vault`
- Dev tools: `/home/hermes/` (graphify, mempalace, jarvis)
- AI tools: `/home/hermes/_AI_Tools/`

Enforced in `AGENTS.md` and `obsidian` skill vault-path section.

### Graphify Query First
**Rule:** For any vault research question, use `graphify query` NOT `rg`/`grep`.
- Traverses EXTRACTED + INFERRED edges
- Returns god nodes, community structure, paths
- Example: `graphify query "How did G.O. 3136 influence post-independence reservation?"`

---

## File Structure Reference

```
/home/hermes/jarvis/
├── ARCHITECTURE.md              # Full system spec
├── launch_complete.py           # One-command startup
├── mcp_config.json              # MCP server registry
├── .env.template                # Telegram config template
├── mcp/
│   ├── terminal/server.py       # Shell execution
│   ├── obsidian/server.py       # Vault CRUD + search
│   └── graphify/server.py       # Graph queries
├── telegram/bot.py              # Full command set
├── dashboard/
│   ├── server.py                # FastAPI + WebSocket
│   └── templates/dashboard.html # Tailwind + Chart.js UI
├── cron/jarvis_crons.md         # 6 cron definitions
└── launch.py                    # Simple launcher

/home/hermes/mempalace/
├── docker-compose.yml           # ChromaDB + MemPalace
├── Dockerfile                   # Python 3.13, pinned deps
└── pyproject.toml               # numpy==1.24.3, chromadb==0.4.22

/vault/
├── AGENTS.md                    # Jarvis system prompt
├── wiki/entities/               # People, orgs
├── wiki/concepts/               # Concepts, movements
├── graphify-out/                # 50k nodes, 97k edges
└── 04 - DAILY/                  # Daily logs
```

---

## Telegram Command Reference

| Command | Description |
|---------|-------------|
| `/brief` | Daily briefing from graphify |
| `/graph "question"` | Knowledge graph query |
| `/path "A" "B"` | Shortest path between concepts |
| `/explain "concept"` | Plain-language explanation |
| `/status` | System health |
| `/run "command"` | Execute shell in vault |
| `/mem "query"` | Search MemPalace |
| `/note "Title" "Content"` | Create vault note |
| `/help` | Show all commands |

---

## Maintenance

| Task | Frequency | Command |
|------|-----------|---------|
| Graph update | After major vault changes | `graphify update /vault` |
| MemPalace mine | Daily (auto) | `cd /home/hermes/mempalace && bash mp.sh mine --limit 50 /vault` (positional dir, not `--vault`; mp.sh enforces E:-only caches) |
| Docker restart | After config changes | `cd /home/hermes/mempalace && docker-compose up -d --build` |
| Cron status | Weekly | `hermes cron list` |
| Disk check | Monthly | `df -h E:` |

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `numpy._core._multiarray_umath` import error | ABI mismatch | Use Docker (pinned numpy 1.24.3) |
| Graphify "not found" | Binary not on PATH | Use full path: `C:/Users/shrey/AppData/Local/Programs/Python/Python314/Scripts/graphify` |
| Graphify `error: unknown command '<path>'` | Tried `graphify <path>` from a non-target dir | `cd` into the target dir first, then run `graphify update .`. For GitHub repos, use `graphify clone <url>` then `cd ~/.graphify/repos/<owner>/<repo>`. |
| `graphify cluster-only` fails with `JSONDecodeError: Expecting ',' delimiter` at a high line number in `graph.json` | `graph.json` was truncated mid-write (killed process, disk full, etc.) — ends mid-node with no closing `]}` brackets | File is **physically corrupted**, not stale. `graphify update` cannot read it. **Fix:** delete or move `/vault/graphify-out/graph.json` aside, then run a full `/graphify /e/_Knowledge/ObsidianVault` regen (community-detection pass takes 30-90 min on the 50k-node vault). Until regen completes, the prior `GRAPH_REPORT.md` is still readable but no incremental updates can land. Verified Aug-4 2026 — Aug-1 graph.json ended at line 419742 mid-`aiAgents.ts` node. |
| Cron wrapper fails with `ValueError: open: embedded null character in path` | Hermes lifecycle_guard trips on literal `C:/Users/shrey/...` paths when the shell normalizes them — known false-positive on this Windows host | Use **msys / Git-bash style paths** in cron commands: `cd /e/_Dev_Tools/graphify && python scripts/graphify-with-fix.py cluster-only /e/_Knowledge/ObsidianVault`. PowerShell / cmd invocations with literal `/home/hermes/...` paths still work — only the bash wrapper is affected. Verified Aug-4 2026. |
| `mempalace mine --vault X --incremental --limit 50` errors with `unrecognized arguments` | `mempalace mine` takes `dir` as **positional**, and decides new-vs-existing by file mtime itself — there is no `--vault` or `--incremental` flag | Correct invocation: `bash mp.sh mine --limit 50 /e/_Knowledge/ObsidianVault` (positional dir, mp.sh wrapper enforces E:-only caches). A run that reports `Files processed: 0 / Drawers filed: 0` is healthy steady-state, not an error — hallway/entity-tunnel counts are still refreshed. |
| Telegram bot silent | Token/user ID wrong | Check `.env`, verify with `@userinfobot` |
| Cron not firing | Hermes not running | `hermes cron status`, ensure gateway/CLI running |
| Dashboard 404 | Server not started | `python /home/hermes/jarvis/dashboard/server.py` |

---

## Extending the Stack

| Need | Add |
|------|-----|
| New data source | MCP server in `/home/hermes/jarvis/mcp/<name>/server.py` |
| New Telegram command | Handler in `telegram/bot.py` + register in `main()` |
| New dashboard widget | API route in `dashboard/server.py` + HTML in `templates/dashboard.html` |
| New cron job | `hermes cron create "SCHEDULE" --prompt "..." --skills "..." --name "name" --deliver "telegram"` |
| New vault section | Create folder + MOC in `wiki/` or `Research/` + link from `AGENTS.md` |

---

## Cost Analysis

| Item | Monthly Cost |
|------|--------------|
| VPS/Cloud | $0 (local) |
| Cloud LLMs | $0 (Ollama local + NVIDIA free tier) |
| Telegram | Free |
| Storage | Your E: drive |
| **Total** | **$0/month** |

---

## References

- `references/jarvis-architecture.md` — Full architecture doc
- `references/mempalace-docker-fix.md` — NumPy/ChromaDB fix details
- `references/graphify-usage.md` — Query patterns, god nodes, path finding
- `references/telegram-commands.md` — Full command implementations
- `templates/mcp-server.py` — MCP server boilerplate
- `templates/cron-job.md` — Cron job template
- `scripts/launch-jarvis.py` — One-command launcher
- `scripts/health-check.py` — System verification

---
*Generated from session: Built complete local Jarvis on Hermes + graphify + MemPalace + Obsidian + MCP + Telegram + Cron + Dashboard. All local, $0/month.*