---
name: kb-healthcheck
description: Weekly knowledge base health check - finds conflicts, missing pages, duplicates, unsourced claims, and suggests new articles
version: 1.0.0
category: knowledge-management
tags: [obsidian, knowledge-base, maintenance, karpathy-method, cron]
---

# kb-healthcheck Skill

Periodic knowledge base integrity check. Scans wiki/ for inconsistencies, gaps, duplicates, and quality issues. Produces a health report and optional auto-fix suggestions.

## Usage

```
/kb-healthcheck
/kb-healthcheck --auto-fix
/kb-healthcheck --report-only
```

## Health Checks Performed

### 1. Conflicting Statements
- Scan all concept pages for contradictory claims about the same concept
- Flag numerically inconsistent claims (e.g., "GPT-4 has 1.7T params" vs "GPT-4 has 1.8T params")
- Report confidence-weighted conflicts

### 2. Orphaned Entities (Missing Pages)
- Find entities/concepts mentioned ≥3 times across wiki but lacking dedicated page
- Suggest new concept/entity pages to create

### 3. Near-Duplicate Pages
- Detect concept pages with >80% content similarity (cosine similarity on embeddings or n-gram overlap)
- Suggest merges with diff preview

### 4. Unsourced/Low-Confidence Claims
- Flag claims with confidence <0.6 or missing source references
- Flag pages with no sources listed in frontmatter

### 5. Stale Content
- Pages not updated in >90 days with high-traffic topics
- Sources in 0-raw/ newer than wiki page last_updated

### 6. Graph Connectivity Issues
- Isolated nodes (no backlinks, no forward links)
- Concepts with no related concepts
- Circular reference chains >3 hops

### 7. New Article Candidates
- Emerging connection patterns (concepts frequently co-mentioned but not linked)
- Trending entities in raw/ sources not yet in wiki/

## Output Report

```markdown
---
healthcheck_date: "2026-07-12"
wiki_size:
  concepts: 142
  entities: 87
  index_pages: 12
  raw_sources: 340
issues_found:
  conflicts: 3
  missing_pages: 12
  duplicates: 2
  unsourced_claims: 8
  stale_pages: 5
  isolated_nodes: 7
  new_candidates: 4
---

# Knowledge Base Health Check - 2026-07-12

## Summary
Overall health: 78/100 (Good)

## Critical Issues (Fix First)
### Conflicting Claims
1. **GPT-4 Parameters**: [[GPT-4]] claims 1.7T params (0-raw/gpt4-tech-report.md) but [[LLM-Architectures]] claims 1.8T (0-raw/llama3-paper.md)
   - Recommendation: Verify primary source, update lower-confidence page

### Unsourced High-Stakes Claims
1. [[Prediction-Market-Arbitrage]] claims "80% win rate" with confidence 0.4, no source cited

## Missing Pages (Mentioned ≥3x, No Page)
1. **RLHF** - mentioned in [[RL]], [[LLM-Training]], [[Alignment]]
2. **Constitutional AI** - mentioned in [[Alignment]], [[Claude]], [[Anthropic]]

## Near-Duplicates
1. [[RAG-Architecture]] (85% similar to [[Retrieval-Augmented-Generation]])
   - Suggestion: Merge into [[RAG]] index page, archive one

## Stale Pages (>90 days, high-traffic topics)
1. [[LLM-Benchmarks]] - last updated 2026-03-15, new benchmarks in 0-raw/

## Isolated Nodes
1. [[Obscure-Paper-2023]] - no backlinks, no forward links
2. [[Random-Concept]] - only linked from 0-raw/temp.md

## New Article Candidates
1. **Inference-Time Compute Scaling** - emerging in 5+ recent raw sources, connects [[LLM-Inference]], [[Test-Time-Compute]], [[Reasoning-Models]]
2. **Agent Evaluation Frameworks** - mentioned across [[Agents]], [[Benchmarks]], [[Tool-Use]]

## Auto-Fix Suggestions (--auto-fix)
- Merge [[RAG-Architecture]] → [[Retrieval-Augmented-Generation]]
- Create stub pages for RLHF, Constitutional AI
- Add missing source references to [[Prediction-Market-Arbitrage]]
```

## Implementation Notes

- Use embeddings (sentence-transformers) or n-gram Jaccard for duplicate detection
- Confidence scoring: pages with >5 sources and >3 backlinks = high trust
- Run weekly via cron job
Outputs to: `05 - OUTPUTS/reports/healthcheck-YYYY-MM-DD.md`

## Vault Configuration (CORRECTED — 2026-07-13)

```
E:/_Knowledge/ObsidianVault/
├── 0-raw/                      ← capture sources
├── 02 - AREAS/                 ← 1,194 wiki pages by domain (primary healthcheck target)
├── 02 - PERMANENT/             ← canonical definitions (concepts/, people/)
├── 03 - PROJECTS/              ← active projects
├── 05 - OUTPUTS/               ← generated reports (healthcheck output goes HERE — NOT wiki/)
│   └── healthcheck-YYYY-MM-DD.md
├── 05 - MEMORY/                ← 5-tier memory engine
├── 04 - DAILY/                 ← daily notes
└── playbooks/                  ← Night Shift PS scripts
```

**Output target:** Reports go to `05 - OUTPUTS/healthcheck-YYYY-MM-DD.md` (NOT `wiki/healthcheck-YYYY-MM-DD.md`).

**Critical path note:** Do NOT write to `wiki/` directories — `wiki/concepts/` and `wiki/entities/` don't exist in this vault. All concept pages live under `02 - AREAS/<domain>/`.

## Pitfalls (Added 2026-07-13)

### Large Vault: Never Use Shell Tools for Scanning
**Problem:** This vault has 55,000+ files. `find`, `du`, `ls -la`, and `tree` at the vault root all hang or timeout.

**Fix:** Use Python's `os.walk` instead:
```python
import os
base = r'E:\_Knowledge\ObsidianVault'

# Quick top-level item count (instant)
for d in sorted(os.listdir(base)):
    full = os.path.join(base, d)
    if os.path.isdir(full):
        print(f'{d}: {len(os.listdir(full))} items')

# Folder sizes, capped per folder to avoid long waits
for d in sorted(os.listdir(base)):
    full = os.path.join(base, d)
    if not os.path.isdir(full): continue
    total = 0; count = 0
    try:
        for root, dirs, files in os.walk(full):
            for f in files:
                try: total += os.path.getsize(os.path.join(root, f)); count += 1
                except: pass
            if count > 5000: break  # cap per folder
    except: pass
    print(f'{total//1024} KB  {count} files  {d}')
```

### Vault Junk Identification (2026-07-13)
The vault root had 60+ folders — tangled mix of PARA duplicates, AI tool artifacts, and empty folders.

| Type | Examples | Action |
|------|----------|--------|
| Empty PARA duplicates | `00 INBOX/`, `inbox/`, `QUEUE/`, `Topics/`, `Untitled/`, `Weekly Notes/`, `fleeting/` | Delete if empty |
| AI tool artifacts | `InfiniteBrain/`, `graphify/`, `.smart-env/`, `pegasus/`, `genericagent/`, `agentic-os/` | DELETE (not notes) |
| Cache | `__pycache__/`, `logs/`, `.trash/` | DELETE |
| Canvas duplicates | `all canvas/` | Merge or delete |
| Real PARA | `00 - SYSTEM/`, `02 - AREAS/`, `0-raw/`, `1-desk/`, `2-atoms/`, `playbooks/`, `BRIEFINGS/` | KEEP |

**Safe to delete without asking** (confirmed empty/junk 2026-07-13): `.trash/`, `__pycache__/`, `.swarm/`, `logs/`, `autoresearch/`, `chats/`, `temp_autoresearch/`, `graphify/`, `graphify-repo/`, `.understand-anything/`, `skills/`, and empty PARA duplicates (`-p/`, `00 - INBOX/`, `00 INBOX/`, `fleeting/`, `inbox/`, `QUEUE/`, `QwenVault/`, `raw-sources/`, `references/`, `Topics/`, `Untitled/`, `Weekly Notes/`).

**Investigate before deleting:** `ruflo/` (has AGENTS.md project files — keep project, delete `node_modules/` only), `BOOKS/` (174 MB — check for large attachments), `tolaria/` (50 MB — likely real notes).

### Cron Model Drift
**Problem:** When the active model changes, ALL unpinned cron jobs silently fail with:
```
RuntimeError: Skipped to prevent unintended spend: global inference config drifted since this job was created
```
All Night Shift crons (Scout/Refinery/Editor/Audit) fail until re-pinned.

**Fix:** Re-pin all crons via the cronjob tool:
```python
cronjob(action='update', job_id='<job-id>', model={'model': 'minimaxai/minimax-m2.7', 'provider': 'nvidia'})
```

**Prevention:** When model/provider changes mid-session, immediately re-pin ALL Night Shift cron jobs to the new model.

### PowerShell 7 Compatibility (Night Shift Scripts)
The Night Shift PowerShell scripts had two PS7.5-specific issues:
1. **Multi-value switch cases** — `"a", "b" { ... }` syntax removed in PS7. Split into separate `{".a"} { ... }`, `{".b"} { ... }` cases.
2. **Date subtraction** — `Get-Date - $StartTime` parsed as `-Date` parameter. Fix: `((Get-Date) - $StartTime)`.
3. **$StartTime undefined** — missing `\$StartTime = Get-Date` at top of scripts.

All three fixed in `playbooks/scout-run.ps1`, `refinery-run.ps1`, `editor-run.ps1` on 2026-07-13. If scripts error again, check for these patterns.
**Problem:** When the active model changes (e.g., provider switches model mid-session), ALL unpinned cron jobs fail with:
```
RuntimeError: Skipped to prevent unintended spend: global inference config drifted since this job was created
```
This causes ALL Night Shift crons (Scout/Refinery/Editor/Audit) to silently fail.

**Fix:** Pin every cron to a specific model+provider:
```bash
# List all crons to find job IDs
hermes cron list

# Pin each one to current model
cronjob(action='update', job_id='<scout-id>', model={'model': 'minimaxai/minimax-m2.7', 'provider': 'nvidia'})
cronjob(action='update', job_id='<refinery-id>', model={'model': 'minimaxai/minimax-m2.7', 'provider': 'nvidia'})
cronjob(action='update', job_id='<editor-id>', model={'model': 'minimaxai/minimax-m2.7', 'provider': 'nvidia'})
cronjob(action='update', job_id='<audit-id>', model={'model': 'minimaxai/minimax-m2.7', 'provider': 'nvidia'})
```

**Prevention:** When model changes mid-session, immediately re-pin all Night Shift crons to the new model.