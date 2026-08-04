# Obsidian Graph View — Configuration Reference
*Last updated: 2026-07-11*

## The One Critical Fact

**Obsidian's graph view is canvas-rendered.** CSS selectors like `.graph-view .node`, `.graph-view .link`, `.graph-view .node:hover` **do not work** — they appear valid in browser dev tools but have zero effect on the rendered canvas. Every failed graph styling attempt on this vault started with trying to style `.node` directly.

The ONLY mechanisms that actually affect the native graph:
1. `.obsidian/graph.json` — color groups, physics, node/edge sizing
2. Obsidian's built-in Graph View settings panel (filters, display toggles)

---

## graph.json Fields That Matter

```json
{
  "colorGroups": [ ... ],       // THE real node coloring mechanism
  "collapse-color-groups": false, // TRUE = all groups collapse to default color
  "nodeSizeMultiplier": 1.8,     // 1.0 = default. Increase for visibility
  "lineSizeMultiplier": 0.7,     // Decrease to reduce edge visual noise
  "repelStrength": 10,           // Higher = more spread, less cramping
  "linkDistance": 180,           // Lower = tighter clusters
  "showTags": true,              // Show #tag nodes
  "showOrphans": true,           // Show unlinked nodes
  "showArrow": true              // Show link direction arrows
}
```

### Color Group Query Format

```json
{
  "query": "tag:#moc OR path:\"05 - MAPS\"",
  "color": { "a": 1, "rgb": 1384146 }
}
```

**RGB conversion**: hex → integer
```python
int('a020f0', 16)  # '#a020f0' → 10438384
```

### Tested High-Contrast Color Palette (24 domains)

| Domain | Hex | RGB Int |
|--------|-----|---------|
| MOCs | #a020f0 | 10438384 |
| Projects | #e2703a | 14821105 |
| Daily Notes | #6b9b3a | 7054550 |
| Indian Politics | #c02020 | 12640890 |
| Philosophy/Religion | #9c5baf | 10218959 |
| Civilizations/IVC | #d4af37 | 13952721 |
| Population Genetics/DNA | #a76bbf | 10971263 |
| Historical Linguistics | #6c8fe5 | 7117264 |
| Epigraphy | #ff7f50 | 16747519 |
| AI & Technology | #0070e0 | 29104 |
| Health/Fitness | #027360 | 2563527 |
| Buddhism | #dc6c0f | 14477049 |
| Dravidian Politics | #fa3ea7 | 16385087 |
| Anti-Caste | #88870e | 8947847 |
| Shramana/Jainism | #ba8cdb | 12257939 |
| RSS/Hindutva | #cb3c25 | 13382421 |
| Wiki Entities (person) | #ffb3c1 | 16741685 |
| Wiki Entities (org/party) | #ffd700 | 16776960 |
| Wiki Concepts | #b05bb1 | 11565729 |
| Places | #5a8a99 | 5880739 |
| Literature/Sources | #8800cc | 8918318 |
| Outputs/Analyses | #00ffff | 65535 |
| System | #babab4 | 12234924 |
| INBOX | #c0c0c0 | 12632256 |

---

## CSS Snippets — What Actually Works

CSS snippets are NOT useless, but they're limited:

### Useful in CSS snippets:
```css
/* Dark background (graph view area) */
.graph-view { background-color: #0f0f14 !important; }
.graph-view canvas { background-color: #0f0f14 !important; }

/* Tooltip and controls */
.graph-view .tooltip {
  background: #1e1e2e !important;
  border: 1px solid #4b5563 !important;
  color: #e2e8f0 !important;
}

/* Controls bar */
.graph-view .controls {
  background: #1e1e2e !important;
}
```

### DOES NOT WORK (canvas-rendered):
```css
/* These look correct in dev tools but do NOTHING on canvas */
.graph-view .node { fill: red; }
.graph-view .link { stroke: blue; }
.graph-view .node:hover { fill: yellow; }
```

---

## When to Build External Plotly Graph Instead

Build `professional_graph.py` → `obsidian_graph.html` when you need:
- Hover tooltips with node metadata (degree, community, links, tags)
- Louvain community detection with distinct colors per community
- Node size = degree (more connected = visually larger)
- Curved edges, opacity control
- Full force-directed layout control (custom k, iterations)

### Script structure:
```python
import networkx as nx
import plotly.graph_objects as go

G = nx.Graph()
# ... parse wikilinks from all .md files ...
# ... add nodes + edges ...

# Layout
pos = nx.spring_layout(G.to_undirected(), k=0.8, iterations=30, seed=42)

# Communities
import community as community_louvain
communities = community_louvain.best_partition(G.to_undirected())

# Color by community, size by degree
# Build go.Scatter traces for edges + nodes
# Save as HTML with CDN Plotly.js
```

### Python environment on this vault:
- `python3` → Python 3.13 (no packages)
- `C:/Users/shrey/AppData/Local/Programs/Python/Python314/python.exe` → has `networkx`, `python-louvain`, `plotly`

Run with full path:
```bash
"C:/Users/shrey/AppData/Local/Programs/Python/Python314/python.exe" professional_graph.py
```

Output: `obsidian_graph.html` — opens in any browser, 861KB, 500 nodes, 60 communities.

---

## Workflow Checklist — Make Graph Look Professional

1. **Open Obsidian Graph View** (`Cmd/Ctrl+G`)
2. **Toggle OFF "Collapse color groups"** in filter panel — this is the switch that enables color groups to show
3. **Check graph.json**: `collapse-color-groups: false`, `nodeSizeMultiplier ≥ 1.5`, `lineSizeMultiplier ≤ 0.7`
4. **CSS snippet active**: `pro-graph-view.css` in `appearance.json` → `enabledCssSnippets[]`
5. **If still ugly**: build external Plotly graph with community detection + node sizing

Step 2 is the most commonly missed — without it, all nodes appear in default grey regardless of color group settings.