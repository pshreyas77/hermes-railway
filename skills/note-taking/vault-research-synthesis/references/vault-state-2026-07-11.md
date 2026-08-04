# Vault State — 2026-07-11 (Night Shift Rebuild Session)

## Vault Location
`E:\_Knowledge\ObsidianVault`

## Night Shift Pipeline — Hermes Cron Architecture

| Job | Cron ID | Schedule (IST) | Playbook |
|-----|---------|----------------|----------|
| Scout Run | b60bd1a2ba42 | `30 23 * * *` (23:30 daily) | `playbooks/01-scout-run.md` |
| Refinery Run | e5fa48dbb046 | `0 3 * * *` (03:00 daily) | `playbooks/02-refinery-run.md` |
| Editor Run | 8e3ee9ca65d5 | `0 6 * * *` (06:00 daily) | `playbooks/03-editor-run.md` |
| Audit Run | 5981bc3a96fd | `0 22 * * 0` (Sun 22:00) | `playbooks/04-audit-run.md` |

## History Watchdog — Hermes Cron Architecture

| Job | Cron ID | Schedule (IST) | First Run |
|-----|---------|----------------|-----------|
| Weekly Scout | 8aa3b1f9906b | `0 2 * * 1` (Mon 02:00) | 2026-07-13 |

**Directory**: `03 - PROJECTS/History-Watchdog/`
**Key artifact**: `queries.yaml` (26 queries across 4 domains, 2026-07-11)

## Auto-Commit

| Cron ID | Schedule | Script |
|---------|----------|--------|
| 9e0ae3e8c9b3 | `0 22 * * *` (22:00 IST) | `vault-auto-commit.py` (no_agent) |

## Pre-Existing Infrastructure (Operational)

- **`07 - SYSTEM/log.md`** — vault operation log (append-only)
- **`night-shift-log.md`** — Night Shift agent run log (root level)
- **`house-rules.md`** — Night Shift constitution (root level)
- **`playbooks/`** — Scout/Refinery/Editor/Audit runbooks
- **`BRIEFINGS/`** — morning briefs (last: 2026-06-25)
- **Smart Connections**: `.smart-env/` semantic embeddings running in background
- **`graphify-repo/`** — graph visualization toolkit (not `graphify-out/`)
- **`genericagent/`** — autonomous agent SOP framework
- **`vault_analyzer.py`** — Python vault analysis (4-pipeline: god nodes, orphans, bridges, edge confidence)

## Active Cross-Domain Projects (from 2026-07-08 synthesis)

| Project | Status | First Deliverable |
|---------|--------|-------------------|
| History Watchdog | 🟢 Active | queries.yaml ✅ (2026-07-11) |
| Health Autopilot | ⬜ Not started | Week 4 checkpoint 2026-07-13 |
| Dravidian Lineage Graph | ⬜ Not started | Interactive prototype 2026-07-28 |

## Vault Stats (approximate, as of 2026-07-11)

- **~200 markdown files** across 8 layers (00 INBOX → 07 SYSTEM)
- **Last Night Shift run**: 2026-07-06 (actually died ~Jun 25 based on log gap)
- **Last morning brief**: 2026-06-25
- **Known issues** (from July 8 audit):
  - 20+ broken wikilinks (Batman Philosophy Archive, Philosophy Links Tracker, Knowledge Hub, Agentic OS, etc. — targets don't exist)
  - 15+ orphan notes from Jul 8 analysis
  - Health Dashboard stale since April 23

## Vault Architecture

```
00 INBOX/        ← intake (currently empty after India Urban Flooding quarantined)
0-raw/           ← pre-processed sources
00 INBOX/        ← Karpathy layer (8-folder)
01 - LITERATURE/ ← articles, papers, web sources
02 - PERMANENT/  ← concepts, entities (atoms, wiki)
03 - PROJECTS/   ← active projects + project hubs
04 - DAILY/      ← daily notes (YYYY-MM-DD format)
05 - MAPS/       ← MOCs (6: Philosophy, Indian Pol History, AI&Tech, Health, Digital Garden, Agentic)
06 - OUTPUTS/   ← finished work (essays, analyses, cross-domain syntheses)
07 - SYSTEM/    ← system infrastructure, CRITICAL_FACTS, ai-first-rules, templates
BRIEFINGS/       ← morning briefs
playbooks/       ← Night Shift runbooks (4)
sources/         ← archived raw sources
```

## Important File Paths

```
E:\_Knowledge\ObsidianVault\_CLAUDE.md                     ← Vault operating manual (280 lines)
E:\_Knowledge\ObsidianVault\07 - SYSTEM\log.md             ← Operation log
E:\_Knowledge\ObsidianVault\night-shift-log.md             ← Night Shift agent log
E:\_Knowledge\ObsidianVault\house-rules.md                  ← Night Shift constitution
E:\_Knowledge\ObsidianVault\playbooks\NIGHT-SHIFT-RUNBOOK.md ← Pipeline overview
E:\_Knowledge\ObsidianVault\BRIEFINGS\2026-07-11 — Morning Brief.md ← Today's brief
E:\_Knowledge\ObsidianVault\02 - PERMANENT\concepts\Karpathy Method — Gap Analysis Against Our Vault.md ← Gap analysis
E:\_Knowledge\ObsidianVault\03 - PROJECTS\History-Watchdog.md ← Project hub (active)
E:\_Knowledge\ObsidianVault\03 - PROJECTS\History-Watchdog\queries.yaml ← 26 queries
```

## Key Lessons from This Session

1. **PowerShell Task Scheduler jobs die silently** — they vanish when the session ends. Always rebuild as Hermes cron jobs.
2. **INBOX quarantine pattern** — items without source attribution get quarantined to `1-desk/article/` with "Quarantined — No Sources" suffix per Prime Directive
3. **Vault already had Karpathy's method** — the gap was pipeline death, not missing architecture. Gap analysis + restart was the right response.
4. **History Watchdog is the highest-leverage project** — directly feeds core research interests (Aryan migration, Dravidian politics, RSS funding, anti-caste movements). queries.yaml IS the deliverable.