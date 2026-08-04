# Vault Conventions — Shreyas's Second Brain (E:/_Knowledge/ObsidianVault)

*Discovered during 2026-07-08 gap analysis session. Update per vault.*

---

## VAULT LOCATION (CRITICAL)

**All write_file / read_file / patch / search_files operations MUST use:**
```
E:/_Knowledge/ObsidianVault
```

**Do NOT write to**:
- `C:` drive defaults (`~/Documents/Obsidian Vault`, etc.)
- `$OBSIDIAN_VAULT_PATH` literal (file tools don't expand shell variables)
- C: drive temp paths when vault work is requested

**User confirmation**: "always store everything in my E:\_Knowledge\ObsidianVault — not C drive" (2026-07-08)

---

## Folder Structure (PARA + Wiki Hybrid)

```
E:/_Knowledge/ObsidianVault/
├── 00 - INBOX/                    # Raw captures
├── 01 - LITERATURE/               # External source notes (articles, papers)
├── 02 - AREAS/                    # Active areas (Philosophy, AI, etc.)
│   ├── 01 Philosophy & Religion/
│   └── 02 AI & Technology/
├── 03 - PROJECTS/                 # Active project hubs
│   ├── Cross-Domain Idea Synthesis.md
│   ├── History-Watchdog.md
│   ├── Health-Autopilot.md
│   ├── Dravidian-Lineage-Graph.md
│   └── [project folders with data/, scripts/, logs/]
├── 04 - DAILY/                    # Daily notes (YYYY-MM-DD.md)
├── 05 - MAPS/                     # MOCs (Maps of Content)
│   ├── AI & Technology MOC.md
│   ├── Philosophy & Religion MOC.md
│   ├── Indian Political History MOC.md
│   ├── Health & Fitness MOC.md
│   ├── Population Genetics Methods MOC.md
│   ├── Historical Linguistics MOC.md
│   ├── Epigraphy Methods MOC.md
│   ├── Agentic Systems MOC.md
│   └── Digital Garden MOC.md
├── 06 - OUTPUTS/                  # Finished essays, reports
│   ├── Deep-Research-Reports-Index-2026-07-08.md
│   └── Vault-Analysis-to-Cross-Domain-Ideas-2026-07-08.md
├── 07 - SYSTEM/                   # Infrastructure
├── wiki/                          # Wiki hub (entities/concepts/analyses)
├── Research/                      # Deep research by domain
│   ├── Politics/  Philosophy/  AI Tools/  Health/
│   ├── Deep/      Articles/     PKM/
├── scripts/                       # Vault-maintenance scripts (graph colors, etc.)
├── index.md                       # Root catalog (auto-generated)
├── _CLAUDE.md                     # Vault operating manual
├── house-rules.md                 # Night Shift agent rules
├── log.md                         # Append-only operation log
└── obsidian-nightly.ps1           # Scheduled maintenance
```

---

## Frontmatter Fields (Standard)

```yaml
date: 2026-07-08
type: project|research|map|entity|concept|daily|output|workflow
subtype: deep-dive|reference|technical-guide|evidence-update|policy|synthesis
tags: [domain, topic, ...]          # lowercase, hyphenated
priority: critical|high|medium|practical|personal
status: active|completed|historical|dormant
source: "Description of sources"
ai-first: true                      # Used for agent routing — REQUIRED on all new notes
confidence: stated|high|medium|low  # For permanent/concept notes
evidence_tier: hard + strong hypothesis  # For research synthesis
```

**Note on `## For future Claude` preamble**: Always present immediately after the title block. This is the first paragraph future-Claude reads when navigating the vault. It's a context paragraph (what gap this fills, vault location, priority), NOT an abstract.

---

## MOC Conventions

### Standard Sections (in order)
1. **Frontmatter** with `type: map`, `ai-first: true`
2. **For future Claude** — one-paragraph orientation
3. **Core content** — tables with wikilinks
4. **Cross-Links** — related MOCs, entities, research
5. **Gaps to Fill** — explicit checkboxes
6. **Last updated** — date in frontmatter + note

### Table Patterns

**Entity Table** (in domain MOCs):
| Entity | Era/Date | Key Contribution | Related Notes |

**Project Table** (in AI & Technology MOC):
| Project | Stack | Status | Key Files |

**Research Table** (in MOCs):
| Document | Purpose | Word Count |

---

## Entity Note Convention

```yaml
---
date: 2026-07-08
type: entity
tags: [entity, domain, ...]
priority: critical|high|medium
status: active|historical
source: "Report N: Title"
ai-first: true
---
# Entity Name
## Overview (table)
## Critical Corrections (if any)
## Cross-Links (wikilinks to MOCs, reports, entities)
```

---

## Research Report Convention

```yaml
---
date: 2026-07-08
type: research
subtype: deep-dive|policy|technical-guide|evidence-update
tags: [domain, topic, ...]
priority: critical|high|medium|practical|personal
status: completed
source: "Live web search, academic databases, government notifications, primary texts"
ai-first: true
---
# Title — Subtitle
**For future Claude:** Context paragraph
## Sections with evidence tables
## Vault Updates Required (checklist)
## Entity/Concept Scaffolds (YAML)
## Sources Table (Citation ID, Source, Date, Authority S/A/NA/C)
```

---

## Authority Codes for Sources

| Code | Meaning | Examples |
|------|---------|----------|
| **S** | Official/Primary | Election Commission, PIB, Cabinet notifications, direct inscriptions |
| **A** | Academic/Peer-reviewed | Journal articles, monographs by established scholars |
| **NA** | News Analysis/Secondary | Reputable outlets (The Hindu, Indian Express), think tanks |
| **C** | Community/Contested | Movement documents, organizational publications, crowd-AI-written (Grokipedia) |

---

## Cross-Link Patterns

- **Entity → MOC**: Add row to MOC table with `[[Entity Name]]`
- **Research → MOC**: Add to "Deep Research" or "Related Notes" section
- **Project → MOC**: Add to "Active Projects" table
- **Concept → MOC**: Add to concepts table or "Core Concepts" section
- **Project Hub → Research**: Link from "Spec Highlights" or "Vault Integration"

---

## Project Hub Convention

Located in `03 - PROJECTS/Project-Name.md` with:
- Frontmatter: `type: project`, `priority: 1|2|3`
- Spec highlights table
- Agent/tool stack table
- First deliverable checklist
- Vault integration table
- Success metrics table

---

## Automation Infrastructure (Existing)

| Component | Location | Purpose |
|-----------|----------|---------|
| **genericagent SOP** | `genericagent/memory/autonomous_operation_sop.md` | Agent framework |
| **Night Shift** | `house-rules.md`, `obsidian-nightly.ps1` | Scheduled autonomous runs |
| **Graph pipeline** | `graphify-repo/`, `professional_vault_graph.py`, `obsidian_graph.html` | Knowledge graph viz |
| **Graph colors** | `scripts/generate_graph_colors.py` → `.obsidian/graph.json` | 20 category color groups |
| **Research tools** | Documented in `Research/AI Tools/2026-06-19...` | Elicit, Undermind, Scite, DeepSeek, Kimi, etc. |
| **MCP + Ollama** | `Research/AI Tools/MCP-Ollama-Local-LLM-Production-Guide.md` | Local LLM production guide |

---

## Health Protocol Stack (Existing)

| Component | Detail |
|-----------|--------|
| **Tier A Supplements** | Whey, Creatine, Caffeine, Omega-3, D3, Berberine |
| **Training** | 3-day PPL with 4kg dumbbells |
| **Checkpoints** | Week 4 (2026-07-19), Week 8, Week 12 |
| **Budget** | ₹15,000–26,000 / 12 weeks |

---

## Key Corrections Established Across Sessions

| # | Topic | Was | Corrected To | Date |
|---|-------|-----|--------------|------|
| 1 | TVK status | Upcoming variable | Won 108/234 seats, minority govt (May 2026) | 2026-07-08 |
| 2 | Charvaka epistemology | Rejected inference entirely | Caricature; accepted inference for verifiable causation | 2026-07-08 |
| 3 | Periyar role | Party founder | Never founded party; DK non-electoral; opposed DMK | 2026-07-08 |
| 4 | IVC seals | Tier A writing | Undeciphered = Tier C at best | 2026-07-08 |
| 5 | BJP TN strategy | Viable path | Failed completely 2026; money ≠ social base | 2026-07-08 |
| 6 | **Tilak cultural origin** | **"Vedic-Aryan import, late-Vedic/Grhya Sutra period"** | **"Neither IVC/Dravidian nor Aryan-migration-import is proven; sectarian tilak system = late Puranic/Gupta era (~300–600 CE+); grew on subcontinent through syncretic codification. Tilak joins the 'absence-of-evidence-rebranded-as-proof' pattern."** | **2026-07-08** |
| 7 | **IVC terracotta red-pigment forehead mark = "tilak predates 2000 BCE"** | Asserted as fact online | **Source = Grokipedia only (crowd-AI, no peer-review). Unverified. Folk etymology dressed as archaeology.** | **2026-07-08** |

### The "Absence-of-Evidence-Rebranded-as-Proof" Pattern (Tilak-style)
Repeated across the vault. When a claim circulates confidently without strong sources:

1. **State the gap explicitly** — don't nudge to either side
2. **Flag source quality** — Grokipedia, Wikipedia, blog posts = low reliability
3. **Note date-of-composition vs period-described** — Vasudeva Upanishad is Puranic-era, NOT early Vedic, even if it describes Vedic deities
4. **Cross-check with established correction log** — this is the live pattern log

This pattern recurs across: IVC lingas, 40% Rigveda non-IA vocabulary, Nuzi horse-bones conflation, EA 25 vs EA 19 tablet confusion, Bruce Lincove 40% figure, **IVC tilak claim**.

---

## Next Session Quick-Start

1. Read `06 - OUTPUTS/Deep-Research-Reports-Index-2026-07-08.md` for report status
2. Check `03 - PROJECTS/` for project hubs created
3. Review `05 - MAPS/` for updated MOCs
4. Run `scripts/generate_graph_colors.py` if updating color groups
5. Apply Tilak-pattern corrections to any new origin claims before writing
6. Prepare Week 4 health checkpoint (2026-07-19)
