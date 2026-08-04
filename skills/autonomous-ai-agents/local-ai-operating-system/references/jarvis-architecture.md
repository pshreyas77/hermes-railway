# Jarvis Architecture - Detailed Reference

## System Overview

A local-first AI operating system built on Hermes Agent with these pillars:

1. **Brain**: Hermes Agent (local Ollama + NVIDIA cloud fallback)
2. **Verbatim Memory**: MemPalace (Docker, ChromaDB backend)
3. **Structured Memory**: Obsidian Vault (markdown, wikilinks, MOCs)
3. **Knowledge Graph**: graphify (50k nodes, 97k edges, 3910 communities)
4. **Hands**: MCP servers (terminal, obsidian, graphify, browser)
5. **Remote Control**: Telegram bot
6. **Automation**: Hermes cron jobs
7. **Dashboard**: FastAPI + WebSocket web UI

## Data Flow

```
User Input (Telegram/CLI/Dashboard)
    │
    ▼
Hermes Agent (Brain)
    │
    ├─► Graphify (Knowledge Graph Queries)
    ├─► MemPalace (Verbatim Memory Search)
    ├─► Obsidian MCP (Vault CRUD)
    ├─► Terminal MCP (Shell Execution)
    └─► Browser MCP (Web Research)
    │
    ▼
Response / Action Execution
    │
    ▼
Persistence: Obsidian Vault + MemPalace + Graphify Update
```

## Component Specifications

### Hermes Agent (Brain)
- **Config**: `~/.hermes/config.yaml` (profile: `jarvis`)
- **Models**: Local Ollama (llama3.1, codellama) + NVIDIA Nemotron/DeepSeek fallback
- **Tools**: All MCP servers + built-in (web, file, terminal, etc.)
- **Session**: SQLite + FTS5 at `~/.hermes/state.db`

### MemPalace (Verbatim Memory) - Docker Fix for NumPy/ChromaDB
- **Architecture**: Docker (ChromaDB 0.4.24 + MemPalace API)
- **Storage**: ChromaDB vector store + SQLite metadata
- **API**: FastAPI on port 8001
- **Key Fix**: Python 3.11 + NumPy 1.24.4 + ChromaDB 0.4.22 pinned for ABI compatibility
- **Commands**:
  ```bash
  mempalace init <path>       # Initialize palace
  mempalace mine <path>       # Mine conversations
  mempalace search "query"    # Semantic search
  mempalace wake-up           # L0+L1 context for current session
  mempalace status            # Show filed stats
  ```

**Docker Fix Details**: 
- Problem: ChromaDB 0.4.x wheels built against NumPy 1.24.x ABI; Python 3.13+ ships NumPy 2.x → ABI mismatch
- Solution: Docker with Python 3.11, NumPy 1.24.4, ChromaDB 0.4.22
- Files: `E:/_Dev_Tools/mempalace/Dockerfile`, `E:/_Dev_Tools/mempalace/docker-compose.yml`

### Graphify (Knowledge Graph)
- **Binary**: `C:/Users/shrey/AppData/Local/Programs/Python/Python314/Scripts/graphify`
- **Graph**: 50,137 nodes, 97,449 edges, 3,910 communities
- **Outputs**: `graph.json`, `GRAPH_REPORT.md`, `GRAPH_TREE.html`
- **Key Commands**:
  ```bash
  graphify query "question"           # BFS traversal
  graphify query "q" --mode dfs       # Deep path
  graphify path "A" "B"               # Shortest path
  graphify explain "concept"          # Plain explanation
  graphify update <path>              # Incremental (AST only)
  graphify god-nodes                  # Top connected
  ```

### Obsidian Vault (Structured Memory)
- **Path**: `E:/_Knowledge/ObsidianVault`
- **Structure**:
  ```
  01 - LITERATURE/      # Book notes, articles
  02 - AREAS/           # Active projects
  03 - RESOURCES/       # Reference material
  04 - DAILY/           # Daily logs (YYYY-MM-DD.md)
  05 - MAPS/            # MOCs (Maps of Content)
  wiki/
    entities/           # People, orgs, places
    concepts/           # Ideas, movements
    analyses/           # Deep research
  Research/             # Deep research notes
  BOOKS/                # Book notes + PDFs
  graphify-out/         # Knowledge graph outputs
  ```
- **Naming**: `YYYY-MM-DD — Title.md` for dailies, `Title.md` for entities/concepts
- **Linking**: `[[Wikilink]]` mandatory for all cross-references

### MCP Servers (Hands)

| Server | Tools | Purpose |
|--------|-------|---------|
| `terminal` | `run_command`, `run_background`, `list_processes`, `kill_process` | Shell execution |
| `obsidian` | `read_note`, `write_note`, `append_note`, `search_notes`, `list_notes`, `add_wikilink`, `get_backlinks` | Vault management |
| `graphify` | `query`, `path`, `explain`, `update`, `god_nodes` | Graph traversal |

### Telegram Bot
- **File**: `E:/_Dev_Tools/jarvis/telegram/bot.py`
- **Commands**: `/brief`, `/graph`, `/path`, `/explain`, `/status`, `/run`, `/mem`, `/note`, `/help`
- **Auth**: Single user ID from `JARVIS_TELEGRAM_USER_ID`

### Cron Jobs (Hermes)
| Job | Schedule | Action |
|-----|----------|--------|
| `daily-briefing` | 0 7 * * * | Graphify query → Telegram summary |
| `vault-maintenance` | 0 2 * * * | `graphify update` + `mempalace mine` |
| `health-check` | 0 * * * * | Disk, Ollama, Hermes, Telegram |
| `content-pipeline` | 0 */4 * * * | Tagged notes → drafts → Telegram |
| `weekly-deep-research` | 0 9 * * 0 | Dravidian gaps → research note |
| `mempalace-mining` | 0 3 * * * | Mine conversations → entities |

### Dashboard
- **URL**: `http://localhost:8080`
- **Tech**: FastAPI + WebSocket + Tailwind + Chart.js
- **Features**: Graph query, path finding, explain, terminal, notes, god nodes, cron status

---

## Key Files Created

```
E:/_Dev_Tools/jarvis/
├── ARCHITECTURE.md              # Full system spec
├── launch_complete.py           # One-command startup
├── mcp_config.json              # MCP server registry
├── .env.template                # Telegram config template
├── mcp/
│   ├── terminal/server.py       # Shell execution
│   ├── obsidian/server.py       # Vault operations
│   └── graphify/server.py       # Graph queries
├── telegram/bot.py              # Telegram bot
├── dashboard/
│   ├── server.py                # FastAPI + WebSocket
│   └── templates/dashboard.html # Tailwind + Chart.js UI
├── cron/jarvis_crons.md         # 6 cron definitions
└── launch.py                    # Simple launcher

E:/_Dev_Tools/mempalace/
├── docker-compose.yml           # ChromaDB + MemPalace
├── Dockerfile                   # Python 3.11, pinned deps
└── pyproject.toml               # numpy==1.24.4, chromadb==0.4.22

E:/_Knowledge/ObsidianVault/
├── AGENTS.md                    # Jarvis system prompt
├── wiki/entities/               # Entities (Annadurai, Periyar, etc.)
├── wiki/concepts/               # Concepts (Justice Party, DK, etc.)
├── graphify-out/                # 50k node graph
└── 04 - DAILY/                  # Daily logs
```

---

## Quick Start

```bash
# 1. Configure Telegram (one-time)
cp E:/_Dev_Tools/jarvis/.env.template E:/_Dev_Tools/jarvis/.env
# Edit .env with BOT_TOKEN and USER_ID from @BotFather / @userinfobot

# 2. Start everything
python E:/_Dev_Tools/jarvis/launch_complete.py
```

**What starts:**
- MemPalace Docker (ChromaDB + API on :8001)
- 3 MCP servers (Terminal, Obsidian, Graphify)
- Web Dashboard at `http://localhost:8080`
- Telegram Bot (if configured)
- Hermes Jarvis CLI (profile: `jarvis`)

---

## Telegram Commands Quick Reference

| Command | Description |
|---------|-------------|
| `/brief` | Daily briefing from graphify |
| `/graph "question"` | Query 50k-node knowledge graph |
| `/path "A" "B"` | Shortest path between concepts |
| `/explain "concept"` | Plain-language explanation |
| `/status` | System health |
| `/run "command"` | Execute shell in vault |
| `/mem "query"` | Search MemPalace |
| `/note "Title" "Content"` | Create vault note |

---

## Current Research Context (July 2026)

### Justice Party & Dravidian Movement (Verified)
- **Justice Party** (1916–1944): First non-Congress party in South India
- **Communal G.O. 3136 (1921)**: First caste-based reservation in India
- **Periyar takeover (1938–1944)**: Transformed elite party → mass movement
- **1944 Salem Conference**: Justice Party → Dravidar Kazhagam (DK)
- **1949 Split**: Annadurai forms DMK (electoral) vs Periyar's DK (social reform)

### Reservation Jurisprudence (Verified)
- **G.O. 3136 (1921/1922/1928)**: Proportional representation for non-Brahmins
- **Champakam Dorairajan (1951)**: SC struck down G.O. → **1st Amendment** (Art 15(4))
- **Mandal (1990)**: OBC reservation upheld
- **EWS (2019)**: Economic criteria added

### Language Families (Verified)
| Family | NE India Coverage |
|--------|------------------|
| Indo-European | Bengali, Assamese, Nepali |
| Sino-Tibetan | Meitei, Bodo, Mizo, Naga langs |
| Austroasiatic | Khasi, Jaintia, Mundari, Santali |
| Tai-Kadai | Ahom, Khamti, Phake |

---

## Key Files Map

| Purpose | Path |
|---------|------|
| Architecture spec | `E:/_Dev_Tools/jarvis/ARCHITECTURE.md` |
| Launch script | `E:/_Dev_Tools/jarvis/launch_complete.py` |
| MCP config | `E:/_Dev_Tools/jarvis/mcp_config.json` |
| Telegram bot | `E:/_Dev_Tools/jarvis/telegram/bot.py` |
| Dashboard | `E:/_Dev_Tools/jarvis/dashboard/server.py` |
| Dashboard UI | `E:/_Dev_Tools/jarvis/dashboard/templates/dashboard.html` |
| Cron jobs | `E:/_Dev_Tools/jarvis/cron/jarvis_crons.md` |
| Launch script | `E:/_Dev_Tools/jarvis/launch.py` |
| MCP Terminal | `E:/_Dev_Tools/jarvis/mcp/terminal/server.py` |
| MCP Obsidian | `E:/_Dev_Tools/jarvis/mcp/obsidian/server.py` |
| MCP Graphify | `E:/_Dev_Tools/jarvis/mcp/graphify/server.py` |
| MemPalace Docker | `E:/_Dev_Tools/mempalace/docker-compose.yml` |
| MemPalace Dockerfile | `E:/_Dev_Tools/mempalace/Dockerfile` |
| Vault AGENTS.md | `E:/_Knowledge/ObsidianVault/AGENTS.md` |
| Graph output | `E:/_Knowledge/ObsidianVault/graphify-out/` |

---

## Critical Rules

1. **E: drive only** — Never C: for installs/clones/builds
2. **Graphify first** — Research questions → `graphify query`, not `rg`
3. **Update graph** — After major vault changes: `graphify update`
4. **Wikilinks mandatory** — `[[Note Name]]` for all cross-references
5. **Telegram auth** — Single user via `JARVIS_TELEGRAM_USER_ID`
6. **MemPalace Docker** — Fixes numpy/chromadb ABI issues
7. **Hermes profile** — Use `jarvis` profile with AGENTS.md prompt