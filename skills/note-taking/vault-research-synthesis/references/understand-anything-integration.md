# Understand Anything Integration for Vault Research

## Overview

**Understand Anything** (Egonex-AI/Understand-Anything) is a knowledge graph plugin that works with Karpathy-pattern LLM wikis like this vault. It provides:

- Deterministic parse of wiki structure (wikilinks, index.md categories)
- LLM-powered entity/claim extraction from articles
- Implicit relationship discovery between articles
- Force-directed graph dashboard with community clustering
- Interactive exploration, search, and guided tours

## Installation for Hermes

```bash
cd E:/_Dev_Tools/Understand-Anything
bash install.sh hermes
```

This adds 10 skills under `understand-anything/` in `~/.hermes/skills/`:

| Skill | Purpose |
|-------|---------|
| `understand-knowledge` | Analyze Karpathy wiki → graph with entities, claims, implicit links |
| `understand` | Analyze codebase → architecture graph |
| `understand-dashboard` | Open interactive graph dashboard |
| `understand-chat` | Ask questions about the graph |
| `understand-onboard` | Generate onboarding guide from graph |
| `understand-diff` | Analyze impact of changes |
| `understand-explain` | Deep-dive into specific file |
| `understand-domain` | Extract business domain knowledge |
| `understand-figma` | Figma design analysis |
| `understand-knowledge` (alias) | Same as understand-knowledge |

## Running on This Vault (E:/_Knowledge/ObsidianVault)

### Quick Start (CLI)

```bash
cd "E:/_Knowledge/ObsidianVault"

# 1. Parse wiki structure (deterministic)
python "C:/Users/shrey/.hermes/skills/understand-anything/understand-knowledge/parse-knowledge-base.py" .

# 2. Run LLM analysis (extracts entities, claims, implicit links)
python "C:/Users/shrey/.hermes/skills/understand-anything/understand-knowledge/analyze-articles.py" .

# 3. Merge all graphs
python "C:/Users/shrey/.hermes/skills/understand-anything/understand-knowledge/merge-knowledge-graph.py" .

# 4. Copy to final location
cp .ua/intermediate/assembled-graph.json .ua/knowledge-graph.json

# 5. Open dashboard
npx https://github.com/Egonex-AI/Understand-Anything/releases/latest/download/understand-anything-viewer.tgz .
```

### Expected Output (from 2026-07-30 run)

- **Articles detected**: 54
- **Topics from index.md**: 5 (Entities, Concepts, Analyses, MOCs, Gaps)
- **Wikilinks**: 755 (557 unresolved)
- **Final graph**: 59 nodes, 184 edges, 6 layers, 5 tour steps
- **Dashboard**: `http://127.0.0.1:5174/?token=...`

## Dashboard Features

- Force-directed layout with community clustering
- Entity/claim extraction from articles
- Implicit cross-references discovered by LLM agents
- Interactive search, filtering, node exploration
- Tour steps generated from index.md section ordering
- No LLM needed for dashboard viewing (static HTML/JS)

## Integration with Vault Workflow

### 1. Scheduled Analysis (Monthly)
Add cron job to re-analyze after major vault additions:
```bash
cronjob action=create schedule="0 3 1 * *" \
  script="vault-understand-knowledge.sh" \
  skills=["vault-research-synthesis"]
```

### 2. Commit Graph to Git
```bash
git add .ua/knowledge-graph.json
git commit -m "chore: update knowledge graph $(date +%Y-%m-%d)"
```

### 3. Team Sharing
Commit `.ua/knowledge-graph.json` — teammates can open dashboard without LLM:
```bash
npx understand-anything-viewer /path/to/vault
```

### 4. Query via Chat
```bash
# From Hermes
hermes chat --skills understand-anything "/understand-chat How does Dravidian research connect to AI notes?"
```

### 5. Generate Onboarding
```bash
hermes chat --skills understand-anything "/understand-onboard"
```

## Vault-Specific Results (2026-07-30)

### Detected Structure
- **54 articles** in wiki pattern
- **5 topics** from index.md: Entities, Concepts, Analyses, MOCs, Gaps
- **755 wikilinks** (557 unresolved — many point to non-existent notes)
- **59 nodes** in final graph
- **184 edges** (wikilinks + implicit + categorized)
- **6 layers** from index.md categories
- **5 tour steps** from index.md ordering

### Key Insights
1. **High unresolved wikilink ratio** (557/755) → many referenced notes don't exist yet
2. **Implicit connections discovered** between Dravidian research and AI/Tech notes
3. **Gaps topic** in index.md has actionable research items
4. **Entities/Concepts split** matches vault's wiki/entities and wiki/concepts structure

## Automation Script

Create `E:/_Dev_Tools/scripts/vault-understand-knowledge.sh`:

```bash
#!/usr/bin/env bash
# Monthly vault knowledge graph update
set -e

VAULT="E:/_Knowledge/ObsidianVault"
SKILLS_ROOT="C:/Users/shrey/.hermes/skills/understand-anything"

cd "$VAULT"
echo "[$(date)] Starting vault knowledge graph update..."

# 1. Parse wiki structure
python "$SKILLS_ROOT/understand-knowledge/parse-knowledge-base.py" .

# 2. Run article analysis (uses local LLM or API)
python "$SKILLS_ROOT/understand-knowledge/analyze-articles.py" .

# 3. Merge graphs
python "$SKILLS_ROOT/understand-knowledge/merge-knowledge-graph.py" .

# 4. Copy to final location
cp .ua/intermediate/assembled-graph.json .ua/knowledge-graph.json

# 5. Git commit if changed
if git diff --quiet .ua/knowledge-graph.json; then
    echo "No changes to knowledge graph"
else
    git add .ua/knowledge-graph.json
    git commit -m "chore: update knowledge graph $(date +%Y-%m-%d)"
    git push
    echo "Knowledge graph updated and pushed"
fi

echo "[$(date)] Update complete"
```

Make executable: `chmod +x vault-understand-knowledge.sh`

Add to cron:
```bash
cronjob action=create schedule="0 3 1 * *" \
  script="vault-understand-knowledge.sh" \
  skills=["vault-research-synthesis"] \
  deliver="local"
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError: networkx` | Use Python 3.14: `C:/Users/shrey/AppData/Local/Programs/Python/Python314/python.exe` |
| Parse script fails | Check index.md exists and has proper `# Topic` headings |
| Analysis hangs | Use `--max-articles` limit or run in batches |
| Dashboard shows no data | Verify `.ua/knowledge-graph.json` exists and has valid JSON |
| Token expired | Restart viewer — new token generated each run |

## References

- Repository: https://github.com/Egonex-AI/Understand-Anything
- Live Demo: https://understand-anything.com/demo/
- Installation: https://github.com/Egonex-AI/Understand-Anything#installation
- Karpathy Wiki Pattern: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f