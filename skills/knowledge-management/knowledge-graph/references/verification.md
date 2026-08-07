# Knowledge Graph — Verification Reference

## Quick Functional Verification

Run this after generating `obsidian_graph.html`:

```bash
python3 - << 'PY'
import json, re
from pathlib import Path

f = Path("/vault/obsidian_graph.html")
html = f.read_text(encoding="utf-8")
size = f.stat().st_size

checks = {
    "D3 force sim": 'd3.forceSimulation' in html,
    "Data injected (no placeholder)": '__GRAPH_DATA__' not in html,
    "Nebula background": 'nebula' in html,
    "Glow filters (3 tiers)": 'glow-lg' in html,
    "Community rings": 'commColor' in html,
    "Tooltip badges": 'domain-badge' in html,
    "Purple accent (#a855f7)": '#a855f7' in html,
    "Dark background (#070810)": '#070810' in html,
    "Tag gradient": 'tag-grad' in html,
    "3+ domains in legend": html.count('legend-item') > 5,
}
for k, v in checks.items():
    print(f"{'PASS' if v else 'FAIL'}: {k}")
failed = [k for k, v in checks.items() if not v]
if failed:
    print("FAILED:", failed)
    exit(1)

# Parse JSON — GRAPH_DATA is an object, not array
m = re.search(r'GRAPH_DATA = \{\s*"nodes":', html)
assert m, "GRAPH_DATA object not found"
pos = m.start() + len('GRAPH_DATA = ')
data, _ = json.JSONDecoder().raw_decode(html[pos:])
nodes = data['nodes']
links = data['links']
print(f"\nNodes: {len(nodes)}, Links: {len(links)}, Size: {size//1024}KB")
assert 350 <= len(nodes) <= 450, f"node count {len(nodes)} out of range"
assert len(links) > 1000, f"only {len(links)} links"
ids = [n['id'] for n in nodes]
assert len(set(ids)) == len(ids), "duplicate node IDs"
colors = set(n['color'] for n in nodes)
print(f"Unique domain colors: {len(colors)}")
print("ALL CHECKS PASSED")
PY
```

## What to Look For Visually

1. **Nebula background** — animated stars + colored blobs visible behind nodes
2. **Hub glow** — high-degree nodes have visible colored halos
3. **Domain colors** — at least 5 distinct node colors visible
4. **Legend** — all domains listed with colored dots
5. **Tags toggle** — clicking "Tags: On/Off" hides/shows tag nodes
6. **Search** — typing dims non-matching nodes
7. **Hover tooltip** — shows node name, domain badge, degree, links

## Browser Display

Open in **Obsidian** (not a raw web browser) for best results:
```
cmd //c start obsidian "E:\_Knowledge\ObsidianVault\obsidian_graph.html"
```

Or open the file directly in any browser via:
```
file:////vault/obsidian_graph.html
```

## Common Issues

| Issue | Fix |
|-------|-----|
| Graph doesn't load | File is >1MB — normal, large vault |
| Nodes all gray | DOMAIN_PALETTE not applied — check classify_node() |
| No labels showing | Labels only on degree >6 nodes — add more connections |
| Community rings missing | Click "Communities" button |
| Physics is sluggish | Reduce MAX_NODES to 300 |
| Graph times out on regenerate | Apply performance.md fallback for community detection |