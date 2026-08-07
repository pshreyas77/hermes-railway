---
name: kb-compile
description: Compile raw source material from 0-raw/ into structured wiki/ concept and entity pages — Step 2 of the Karpathy method
version: 1.1.0
category: knowledge-management
tags: [obsidian, knowledge-base, compilation, karpathy-method, hermes-agent]
vault_path: "/vault"
raw_dir: "0-raw"
concepts_dir: "02 - AREAS"
entities_dir: "02 - PERMANENT"
output_dir: "05 - OUTPUTS"
---

# kb-compile Skill

Compiles raw source material from `0-raw/` into structured wiki pages in `wiki/concepts/` and `wiki/entities/`. This is Step 2 of the Karpathy method: "Let the LLM Write Your Wiki For You."

## Prerequisites

- Vault at `/vault`
- Raw source files in `0-raw/` (captured via Obsidian Web Clipper or manual markdown)
- Existing directories: `wiki/concepts/`, `wiki/entities/`, `wiki/index.md`, `wiki/log.md`

## Usage

```
/kb-compile              # Incremental: process raw files newer than last compile
/kb-compile --full       # Full recompilation of every raw file
/kb-compile --concepts-only   # Only concept pages
/kb-compile --entities-only   # Only entity pages
/kb-compile --since 2026-07-01  # Only raw files modified after date
/kb-compile --limit 10   # Cap at N files this run
```

## Workflow

1. Scan `0-raw/` for new/updated source files
2. Extract key concepts, entities, claims, and relationships
3. Create/update concept pages in `wiki/concepts/`
4. Create/update entity pages in `wiki/entities/`
5. Create/update index pages (e.g., `wiki/concepts/RAG.md`, `wiki/concepts/prediction-markets.md`)
6. Update `wiki/index.md` and `wiki/log.md`

## Concept Page Template

```markdown
---
concept: "Concept Name"
aliases: ["alias1", "alias2"]
sources: ["0-raw/source-file.md", "..."]
related: ["Related Concept 1", "Related Concept 2"]
tags: ["tag1", "tag2"]
confidence: 0.8
last_updated: "2026-07-12"
---

# Concept Name

**Definition:** Brief 2-3 sentence definition.

**Key Insights:**
- Insight 1
- Insight 2

**Key Claims:**
- Claim 1 (source: 0-raw/xyz.md)
- Claim 2 (source: 0-raw/abc.md)

**Related Concepts:** [[Related Concept 1]], [[Related Concept 2]]

**Open Questions:**
- Question 1
- Question 2
```

## Entity Page Template

```markdown
---
entity: "Entity Name"
type: "person|organization|concept|tool|paper"
aliases: ["alias1"]
sources: ["0-raw/source-file.md"]
tags: ["tag1"]
confidence: 0.9
last_updated: "2026-07-12"
---

# Entity Name

**Type:** person|organization|concept|tool|paper

**Description:** Brief description.

**Key Attributes:**
- Attribute 1: Value
- Attribute 2: Value

**Mentions in Sources:**
- 0-raw/source1.md (context: ...)
- 0-raw/source2.md (context: ...)

**Related Entities:** [[Entity 1]], [[Entity 2]]
```

## Index Page Template

```markdown
---
index: "Topic Name"
concepts: ["Concept 1", "Concept 2", "..."]
entities: ["Entity 1", "Entity 2", "..."]
last_compiled: "2026-07-12"
source_count: 42
---

# Topic Name Index

## Core Concepts
- [[Concept 1]]
- [[Concept 2]]

## Key Entities
- [[Entity 1]]
- [[Entity 2]]

## Source Materials
- 0-raw/source1.md
- 0-raw/source2.md
```

## State Tracking

Maintains `.kb-compile-state.json` in vault root:
```json
{
  "last_full_compile": "2026-07-10T14:30:00Z",
  "last_incremental": "2026-07-13T09:15:00Z",
  "processed_files": {
    "0-raw/article.md": "2026-07-10T14:30:00Z"
  },
  "concepts_created": 10,
  "entities_created": 28
}
```

## Vault Configuration (CORRECTED — 2026-07-13)

```
/vault/
├── 0-raw/                      ← capture sources (Night Shift Scout watches here)
│   └── sources/archived/        ← archived after refinery
├── 1-desk/                     ← Night Shift processing queue
│   └── article/, book/, paper/, video/, podcast/, idea/, _quarantine/, _needs-work/
├── 2-atoms/                    ← Night Shift extracted atoms
│   └── concepts/, people/, events/
├── 02 - AREAS/                 ← 1,194 wiki pages by domain (kb-compile OUTPUT — NOT wiki/)
│   ├── 01 Philosophy & Religion/
│   ├── 02 AI & Technology/
│   ├── 03 Ancient Civilizations/
│   ├── 04 Political Analysis/
│   ├── 05 Knowledge Management/
│   └── 06 Personal Development/ ... (etc.)
├── 02 - PERMANENT/             ← canonical definitions
│   └── concepts/, people/        (NOT wiki/entities — entities go here)
├── 05 - OUTPUTS/               ← kb-report output, healthcheck reports
├── 05 - MEMORY/                ← 5-tier memory engine
├── 05 - SYSTEM/                ← skill definitions in vault (kb-compile.md, etc.)
├── 03 - PROJECTS/              ← active projects (History Watchdog, Night Shift)
├── 04 - DAILY/                 ← daily notes
├── playbooks/                  ← Night Shift PS scripts (scout/refinery/editor/audit)
└── .kb-compile-state.json      ← state tracking
```

**Critical path note:** Do NOT use `wiki/concepts/` or `wiki/entities/` — those directories don't exist in this vault. All concept pages go directly into the appropriate `02 - AREAS/<domain>/` subfolder. Entity pages go to `02 - PERMANENT/concepts/` or `02 - PERMANENT/people/`.

## Night Shift Integration

The vault has a fully automated nightly pipeline (Scout 23:30 / Refinery 03:00 / Editor 06:00 / Audit Sun 22:00). kb-compile complements it:

| Stage | What it does | kb-compile's role |
|-------|-------------|-------------------|
| Scout | Captures → 1-desk/ | — |
| Refinery | 1-desk/ → 2-atoms/ | — |
| **kb-compile** | **0-raw/ → 02 - AREAS/** | ← This skill's job |
| Editor | Links 2-atoms/, detects orphans | — |
| Audit | Weekly audit | `kb-healthcheck` |

kb-compile processes **raw captures that bypass the 1-desk queue** (e.g., web clips going directly to 0-raw/) and compiles them into the main wiki (02 - AREAS/). The two pipelines are parallel: Night Shift manages the literature→atom flow; kb-compile manages raw→wiki.

If raw captures exist in 0-raw/ that haven't appeared in 1-desk/ (means Scout missed them), run kb-compile manually.

## Agentic OS Integration

kb-compile also ships as a vault-native skill at `agentic-os/loop/skills/kb-compile-skill/SKILL.md`
— registered with the Agentic OS loop, runs via `bash loop.sh` in autonomous mode.

**Two usage modes:**

| Mode | How to invoke | Runs via |
|------|--------------|----------|
| **On-demand** | `/kb-compile` in Hermes chat | Hermes skill system |
| **Autonomous** | `bash loop.sh` heartbeat | Agentic OS loop.sh |

The on-demand path and the autonomous path use the same source/destination folders.
Compiled pages land in `wiki/concepts/` and `wiki/entities/` either way.

**Agentic OS skill path** (for loop integration):
`/vault/agentic-os/loop/skills/kb-compile-skill/SKILL.md`

## Pitfalls

- Raw files must be **markdown** (`.md`) — `.canvas` files are skipped
- Obsidian wikilinks `[[Page Name]]` work across the vault — use them for ALL backlinks
- Confidence scores: 0.9+ = well-established, 0.7-0.9 = probable, <0.7 = speculative
- Incremental mode relies on file modification times in Windows/git-bash
- This skill runs under **Hermes Agent**, not Claude Code
- Do NOT write files to `~/.hermes/skills/` — that directory is not the skill store; skills live in `%LOCALAPPDATA%/hermes/skills/`

## Support Files

- `references/night-shift-powershell-ps7.md` — PS7.5 compatibility fixes for the Night Shift pipeline scripts (multi-value switch cases, date subtraction, $StartTime). **Read this before debugging Scout/Refinery/Editor script failures.**
- `references/hermes-obsidian-mcp-setup.md` — Zero-cost guide to connect Hermes directly to Obsidian via MCP. Enables real-time AI read/write of the vault, not just scheduled processing.