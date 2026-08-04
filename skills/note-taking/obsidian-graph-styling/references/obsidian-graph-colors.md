# Obsidian graph.json — 23-Color Configuration Reference

Built: 2026-07-15 for `E:\_Knowledge\ObsidianVault\`

## graph.json colorGroups (correct format)

```json
{
  "colorGroups": [
    {"query": "path:/02 - AREAS/03 Ancient Civilizations", "color": {"r": 249, "g": 115, "b": 22}, "name": "Ancient Civilizations"},
    {"query": "path:/02 - AREAS/01 Philosophy & Religion", "color": {"r": 168, "g": 85, "b": 247}, "name": "Philosophy & Religion"},
    {"query": "path:/02 - AREAS/02 AI & Technology", "color": {"r": 16, "g": 185, "b": 129}, "name": "AI & Technology"},
    {"query": "path:/02 - AREAS/04 Political Analysis", "color": {"r": 239, "g": 68, "b": 68}, "name": "Political Analysis"},
    {"query": "path:/02 - AREAS/05 Knowledge Management", "color": {"r": 59, "g": 130, "b": 246}, "name": "Knowledge Management"},
    {"query": "path:/02 - AREAS/06 Personal Development", "color": {"r": 236, "g": 72, "b": 153}, "name": "Personal Development"},
    {"query": "path:/02 - AREAS/06 Society & Culture", "color": {"r": 234, "g": 179, "b": 8}, "name": "Society & Culture"},
    {"query": "path:/01 - LITERATURE", "color": {"r": 6, "g": 182, "b": 212}, "name": "Literature / Papers"},
    {"query": "path:/03 - PROJECTS/Active", "color": {"r": 245, "g": 158, "b": 11}, "name": "Active Projects"},
    {"query": "path:/03 - PROJECTS/Completed", "color": {"r": 132, "g": 204, "b": 22}, "name": "Completed Projects"},
    {"query": "path:/03 - PROJECTS/concepts", "color": {"r": 132, "g": 204, "b": 22}, "name": "Concepts"},
    {"query": "path:/03 - PROJECTS/people", "color": {"r": 99, "g": 102, "b": 241}, "name": "People"},
    {"query": "path:/03 - PROJECTS/questions", "color": {"r": 20, "g": 184, "b": 166}, "name": "Questions"},
    {"query": "path:/04 - DAILY", "color": {"r": 100, "g": 116, "b": 139}, "name": "Daily Notes"},
    {"query": "path:/05 - MEMORY", "color": {"r": 14, "g": 165, "b": 233}, "name": "Memory"},
    {"query": "path:/05 - INTELLIGENCE", "color": {"r": 139, "g": 92, "b": 246}, "name": "Intelligence"},
    {"query": "path:/05 - OUTPUTS", "color": {"r": 244, "g": 114, "b": 182}, "name": "Outputs"},
    {"query": "path:/06 - OUTPUTS", "color": {"r": 244, "g": 114, "b": 182}, "name": "Outputs II"},
    {"query": "tag:#moc", "color": {"r": 255, "g": 255, "b": 255}, "name": "MOC Hub Files"},
    {"query": "tag:#index", "color": {"r": 209, "g": 213, "b": 219}, "name": "Index Files"},
    {"query": "tag:#dravidian", "color": {"r": 249, "g": 115, "b": 22}, "name": "Dravidian Atlas"},
    {"query": "tag:#ancient-civilization", "color": {"r": 251, "g": 146, "b": 60}, "name": "Ancient Civilization"},
    {"query": "tag:#ai", "color": {"r": 16, "g": 185, "b": 129}, "name": "AI Files"}
  ]
}
```

## CSS snippet (pro-graph-view.css) — working rules

Location: `E:\_Knowledge\ObsidianVault\.obsidian\snippets\pro-graph-view.css`

The key insight: Obsidian adds `.color-fill-r{R}-g{G}-b{B}` classes to the graph container element.
CSS then targets these to color canvas-rendered nodes. Example rule:

```css
/* Ancient Civilizations — r249,g115,b22 → #F97316 */
.graph-view.color-fill-r249-g115-b22 .node {
    fill: #7c2d12 !important;  /* dark orange fill */
    stroke: #f97316 !important; /* bright orange outline */
}
.graph-view.color-fill-r249-g115-b22 .node:hover {
    fill: #ea580c !important;
    stroke: #fb923c !important;
}
```

Fill color should be dark (near-black with tint of the hue), stroke should be the bright saturated color.

## Full CSS rules (all 23 groups)

```css
/* Ancient Civilizations — #F97316 */
.graph-view.color-fill-r249-g115-b22 .node { fill: #7c2d12; stroke: #f97316; }
.graph-view.color-fill-r249-g115-b22 .node:hover { fill: #ea580c; stroke: #fb923c; }

/* Philosophy & Religion — #A855F7 */
.graph-view.color-fill-r168-g85-b247 .node { fill: #3b1f6e; stroke: #a855f7; }
.graph-view.color-fill-r168-g85-b247 .node:hover { fill: #7c3aed; stroke: #c084fc; }

/* AI & Technology — #10B981 */
.graph-view.color-fill-r16-g185-b129 .node { fill: #064e3b; stroke: #10b981; }
.graph-view.color-fill-r16-g185-b129 .node:hover { fill: #047857; stroke: #34d399; }

/* Political Analysis — #EF4444 */
.graph-view.color-fill-r239-g68-b68 .node { fill: #450a0a; stroke: #ef4444; }
.graph-view.color-fill-r239-g68-b68 .node:hover { fill: #b91c1c; stroke: #f87171; }

/* Knowledge Management — #3B82F6 */
.graph-view.color-fill-r59-g130-b246 .node { fill: #1e3a5f; stroke: #3b82f6; }
.graph-view.color-fill-r59-g130-b246 .node:hover { fill: #1d4ed8; stroke: #60a5fa; }

/* Personal Development — #EC4899 */
.graph-view.color-fill-r236-g72-b153 .node { fill: #4c0519; stroke: #ec4899; }
.graph-view.color-fill-r236-g72-b153 .node:hover { fill: #9d174d; stroke: #f472b6; }

/* Society & Culture — #EAB308 */
.graph-view.color-fill-r234-g179-b8 .node { fill: #451a03; stroke: #eab308; }
.graph-view.color-fill-r234-g179-b8 .node:hover { fill: #854d0e; stroke: #facc15; }

/* Literature / Papers — #06B6D4 */
.graph-view.color-fill-r6-g182-b212 .node { fill: #083344; stroke: #06b6d4; }
.graph-view.color-fill-r6-g182-b212 .node:hover { fill: #0e7490; stroke: #22d3ee; }

/* Active Projects — #F59E0B */
.graph-view.color-fill-r245-g158-b11 .node { fill: #451a03; stroke: #f59e0b; }
.graph-view.color-fill-r245-g158-b11 .node:hover { fill: #b45309; stroke: #fbbf24; }

/* Completed Projects / Concepts — #84CC16 */
.graph-view.color-fill-r132-g204-b22 .node { fill: #1a2e05; stroke: #84cc16; }
.graph-view.color-fill-r132-g204-b22 .node:hover { fill: #3f6212; stroke: #a3e635; }

/* People — #6366F1 */
.graph-view.color-fill-r99-g102-b241 .node { fill: #1e1b4b; stroke: #6366f1; }
.graph-view.color-fill-r99-g102-b241 .node:hover { fill: #3730a3; stroke: #818cf8; }

/* Questions — #14B8A6 */
.graph-view.color-fill-r20-g184-b166 .node { fill: #042f2e; stroke: #14b8a6; }
.graph-view.color-fill-r20-g184-b166 .node:hover { fill: #115e59; stroke: #2dd4bf; }

/* Daily Notes — #64748B */
.graph-view.color-fill-r100-g116-b139 .node { fill: #1e293b; stroke: #64748b; }
.graph-view.color-fill-r100-g116-b139 .node:hover { fill: #334155; stroke: #94a3b8; }

/* Memory — #0EA5E9 */
.graph-view.color-fill-r14-g165-b233 .node { fill: #0c4a6e; stroke: #0ea5e9; }
.graph-view.color-fill-r14-g165-b233 .node:hover { fill: #0369a1; stroke: #38bdf8; }

/* Intelligence — #8B5CF6 */
.graph-view.color-fill-r139-g92-b246 .node { fill: #2e1065; stroke: #8b5cf6; }
.graph-view.color-fill-r139-g92-b246 .node:hover { fill: #5b21b6; stroke: #a78bfa; }

/* Outputs — #F472B6 */
.graph-view.color-fill-r244-g114-b182 .node { fill: #500724; stroke: #f472b6; }
.graph-view.color-fill-r244-g114-b182 .node:hover { fill: #9d174d; stroke: #f9a8d4; }

/* MOC Hub Files — #FFFFFF */
.graph-view.color-fill-r255-g255-b255 .node { fill: #1e293b; stroke: #ffffff; stroke-width: 2px; }
.graph-view.color-fill-r255-g255-b255 .node:hover { fill: #334155; stroke: #f8fafc; }

/* Index Files — #D1D5DB */
.graph-view.color-fill-r209-g213-b219 .node { fill: #1f2937; stroke: #d1d5db; }
.graph-view.color-fill-r209-g213-b219 .node:hover { fill: #374151; stroke: #f3f4f6; }

/* ancient-civilization tag — #FB923C */
.graph-view.color-fill-r251-g146-b60 .node { fill: #431407; stroke: #fb923c; }
.graph-view.color-fill-r251-g146-b60 .node:hover { fill: #7c2d12; stroke: #fdba74; }
```

## Backup / Restore workflow

```bash
# 1. After writing graph.json, always save permanent backup
cp "E:/_Knowledge/ObsidianVault/.obsidian/graph.json" \
   "E:/_Knowledge/ObsidianVault/.obsidian/graph.json.backup.permanent"

# 2. When Obsidian overwrites it (restore)
cp "E:/_Knowledge/ObsidianVault/.obsidian/graph.json.backup.permanent" \
   "E:/_Knowledge/ObsidianVault/.obsidian/graph.json"

# Script: E:/_Knowledge/ObsidianVault/.obsidian/restore-graph-colors.sh
#!/usr/bin/env bash
VAULT="E:/_Knowledge/ObsidianVault"
cp "$VAULT/.obsidian/graph.json" "$VAULT/.obsidian/graph.json.backup.before_restore"
cp "$VAULT/.obsidian/graph.json.backup.permanent" "$VAULT/.obsidian/graph.json"
echo "✅ Restored from permanent backup"
```

### Vault-Local Restore Script (updated 2026-07-29)

Location: `{vault}/.obsidian/restore-graph-colors.sh`

```bash
#!/usr/bin/env bash
# Graph Color Configuration Loader — Updated for current vault structure
# Run this after opening Obsidian to apply color groups

GRAPH_FILE="E:/_Knowledge/ObsidianVault/.obsidian/graph.json"

# Check if Obsidian has overwritten the file (colorGroups empty or missing)
if ! grep -q '"colorGroups"' "$GRAPH_FILE" 2>/dev/null || [ "$(grep -c '"colorGroups": \[\]' "$GRAPH_FILE")" -eq 1 ]; then
    echo "Restoring color groups to graph.json..."

    cat > "$GRAPH_FILE" << 'GRAPHEOF'
{
  "collapse-filter": false,
  "search": "",
  "showTags": true,
  "showAttachments": false,
  "hideUnresolved": true,
  "showOrphans": false,
  "collapse-color-groups": false,
  "colorGroups": [
    {"query": "path:/02 - AREAS/03 Ancient Civilizations", "color": {"r": 249, "g": 115, "b": 22}},
    {"query": "path:/02 - AREAS/01 Philosophy & Religion", "color": {"r": 168, "g": 85, "b": 247}},
    {"query": "path:/02 - AREAS/02 AI & Technology", "color": {"r": 16, "g": 185, "b": 129}},
    {"query": "path:/02 - AREAS/04 Political Analysis", "color": {"r": 239, "g": 68, "b": 68}},
    {"query": "path:/02 - AREAS/05 Knowledge Management", "color": {"r": 59, "g": 130, "b": 246}},
    {"query": "path:/02 - AREAS/06 Personal Development", "color": {"r": 236, "g": 72, "b": 153}},
    {"query": "path:/02 - AREAS/07 Society & Culture", "color": {"r": 234, "g": 179, "b": 8}},
    {"query": "path:/01 - LITERATURE/", "color": {"r": 6, "g": 182, "b": 212}},
    {"query": "path:/03 - PROJECTS/Active", "color": {"r": 245, "g": 158, "b": 11}},
    {"query": "path:/03 - PROJECTS/Completed", "color": {"r": 132, "g": 204, "b": 22}},
    {"query": "path:/03 - PROJECTS/concepts", "color": {"r": 132, "g": 204, "b": 22}},
    {"query": "path:/03 - PROJECTS/people", "color": {"r": 99, "g": 102, "b": 241}},
    {"query": "path:/03 - PROJECTS/questions", "color": {"r": 20, "g": 184, "b": 166}},
    {"query": "path:/04 - DAILY", "color": {"r": 100, "g": 116, "b": 139}},
    {"query": "path:/05 - MEMORY", "color": {"r": 14, "g": 165, "b": 233}},
    {"query": "path:/05 - INTELLIGENCE", "color": {"r": 139, "g": 92, "b": 246}},
    {"query": "path:/05 - OUTPUTS", "color": {"r": 244, "g": 114, "b": 182}},
    {"query": "path:/06 - OUTPUTS", "color": {"r": 244, "g": 114, "b": 182}},
    {"query": "tag:#moc", "color": {"r": 255, "g": 255, "b": 255}},
    {"query": "tag:#index", "color": {"r": 209, "g": 213, "b": 219}},
    {"query": "tag:#dravidian", "color": {"r": 249, "g": 115, "b": 22}},
    {"query": "tag:#ancient-civilization", "color": {"r": 251, "g": 146, "b": 60}},
    {"query": "tag:#ai", "color": {"r": 16, "g": 185, "b": 129}}
  ],
  "collapse-display": true,
  "showArrow": true,
  "textFadeMultiplier": 0.3,
  "nodeSizeMultiplier": 1.3,
  "lineSizeMultiplier": 0.7,
  "collapse-forces": true,
  "centerStrength": 0.6,
  "repelStrength": 15,
  "linkStrength": 0.8,
  "linkDistance": 180,
  "scale": 0.3,
  "close": false
}
GRAPHEOF

    echo "✓ Color groups restored!"
else
    echo "✓ Color groups already configured"
fi
```

**Usage**: `bash "{vault}/.obsidian/restore-graph-colors.sh"` then refresh graph (`Ctrl+G` twice).