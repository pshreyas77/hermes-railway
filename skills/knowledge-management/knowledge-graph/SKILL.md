---
name: knowledge-graph
description: "Generate interactive D3.js knowledge graphs from Obsidian vaults — dark theme, domain coloring, hub glow, animated nebula. Produces obsidian_graph.html."
triggers:
  - "generate a graph of my vault"
  - "visualize my knowledge graph"
  - "make my graph better and colorful"
  - "rebuild the knowledge graph"
  - "regenerate the graph"
  - "open the graph in browser"
  - "professional_graph.py"
  - "obsidian_graph.html"
  - "extract links from canvas"
  - "make a playlist from canvas"
  - "open canvas file"
when_to_use:
  - Vault has 500+ notes and wikilinks
  - User wants visual polish (colors, glow, nebula, not default)
  - Graph needs to be interactive (hover tooltips, zoom, search, filter by domain)
  - Large vault needs pruning to stay within physics budget
---

# Knowledge Graph Generation

## What this skill does

Generates an interactive D3.js force-directed knowledge graph from an Obsidian vault, with dark theme, domain-specific colors, hub glow effects, animated nebula background, and rich interactivity.

## Trigger phrases

Say "graph", "visualize my vault", "knowledge graph", "make it colorful", "regenerate graph" — or edit `professional_graph.py` directly.

## Steps

1. Read existing `professional_graph.py` if it exists
2. Run it first to check for timeouts (60s budget for generation)
3. If it times out, apply the fixes in `references/performance.md`
4. If community detection is slow, use `greedy_modularity_communities` with a degree-based fallback
5. Generate the HTML
6. Verify output using `references/verification.md`

## Output

- `obsidian_graph.html` in the vault root — open in Obsidian or any browser
- Self-contained (no server needed)
- ~400 nodes, ~6000 edges by default (pruned from full vault)

## Visual features

- **Animated nebula background** — canvas-based stars + colored radial blobs
- **3-tier node glow** — nodes with degree >20 get glow-lg, >12 glow-md, >6 glow-sm
- **Domain color palette** — 16+ distinct saturated colors per subject area
- **Community ring overlays** — dashed circles around cluster groups, toggleable
- **Colored edges** — inherits source node color at 30% opacity
- **Tag nodes** — white radial gradient dots, lower opacity, togglable
- **Hub nodes** — larger, stronger glow, colored stroke
- **Labels** — white stroke outline for legibility on any background

## Interactive features

- Hover tooltip showing domain badge, degree, community ID, linked notes, tags
- Search — dims non-matching nodes, highlights matches
- Legend click — toggle entire domain visibility
- Tags On/Off button
- Communities button — show/hide cluster rings
- Reset View button
- Zoom/pan via D3 zoom

## Performance budget

| Phase | Budget |
|-------|--------|
| File scan + graph build | <30s |
| Community detection | <10s (use fallback if needed) |
| HTML generation | <5s |
| Browser render | <2s |

If community detection times out, the script must fall back to degree-based clustering immediately rather than hanging.

## Key design decisions

- **Canvas nebula** (not SVG) — 200 stars + 5 colored radial blobs, animated via requestAnimationFrame
- **3-tier glow** — nodes with degree >20 get glow-lg, >12 glow-md, >6 glow-sm
- **Domain palette** — 16+ saturated colors keyed to vault subject areas
- **Community rings** — dashed circles around cluster groups, toggleable
- **Edge color** — inherits source node color at 30% opacity
- **Tag nodes** — white radial gradient dots, lower opacity, togglable
- **GRAPH_DATA is an object** (not array) — `const GRAPH_DATA = {"nodes": [...], "links": [...]}`
- **Parse with `json.JSONDecoder().raw_decode()`** at the object start position to avoid truncation

## Canvas File Extraction

Canvas files (`.canvas`) are JSON with `nodes[]` and `edges[]`. To extract links:

```python
import json, re
from pathlib import Path

canvas = json.loads(Path("path/to.file.canvas").read_text())
for node in canvas["nodes"]:
    if node.get("type") == "text":
        for m in re.finditer(r'\[([^\]]+)\]\((https?://[^\)]+)\)', node["text"]):
            print(m.group(2), "|", m.group(1))
```

Canvas node `x` coordinate can group links by philosopher/section (horizontal layout).
Canvas files do NOT open via `cmd //c start obsidian "path.canvas"` — open the vault in Obsidian first, then navigate to the file manually, or use File Explorer → Open With → Obsidian.

## Pitfalls

- **Browser file:// URLs do NOT render markdown** — open the graph HTML in Obsidian directly, not via `file:///` in a web browser
- **Canvas files won't open via `cmd //c start obsidian path.canvas`** — Obsidian must already have the vault open; use File Explorer right-click → Open With → Obsidian, or navigate manually in the Obsidian file browser