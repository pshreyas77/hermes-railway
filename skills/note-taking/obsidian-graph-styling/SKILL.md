---
name: obsidian-graph-styling
description: Style Obsidian's native graph view — graph.json color groups (correct format), CSS snippet rules (they DO work), backup/restore workflow, physics tuning, and when to use D3.js instead.
platforms: [linux, macos, windows]
trigger: "When user asks to change/fix/style/improve the Obsidian graph view, or mentions graph colors/nodes/layout."
created_by: hermes-agent
---

# Obsidian Graph View Styling

> **Two different things share the name "graph":** Obsidian's **native canvas graph** (tuned via `graph.json` + CSS snippets) and a **full HTML/D3.js knowledge graph** (custom build). This skill covers both.

## Which to use?

| Goal | Use |
|------|-----|
| Quick within-Obsidian, colorful clusters by folder/tag | `graph.json` + CSS snippet (native) |
| Glow effects, rich tooltips, legend, animated background | D3.js HTML build (`professional_graph.py`) |

---

## Track A: Native Graph

### File Location
```
{vault}/.obsidian/graph.json
```

### ⚠️ Obsidian Overwrites This File — Continuously

Obsidian **resets `colorGroups` to `[]` on every startup and every graph panel open**, setting `collapse-color-groups: true`. This happens **before** the graph renders, even with file permissions set. A static restore script does NOT work — Obsidian locks the file while running.

**The only reliable automation is a live watchdog** that restores colors faster than Obsidian can clear them:

**Script**: `C:/Users/shrey/AppData/Local/Programs/Obsidian/graph-color-watchdog.py`

The watchdog (verified working 2026-07-15):
- Polls `graph.json` every 5 seconds
- If `colorGroups` is empty/cleared, immediately restores all 23 groups with physics settings
- Obsidian reads the file fresh on each graph panel interaction — the restore lands between reads
- Survives Obsidian restarts; restore happens before the graph view is even opened
- If the graph still shows gray nodes after restart: close graph (`Esc`), re-open (`Ctrl+G`), colors appear within 5s

**Startup sequence** (order matters):
1. Kill Obsidian fully: `taskkill //F //IM Obsidian.exe`
2. Start watchdog: `python3 "…/graph-color-watchdog.py"` (background)
3. Start Obsidian: `"C:/Users/shrey/AppData/Local/Programs/Obsidian/Obsidian.exe"`
4. Watchdog restores colors within seconds; Obsidian reads them on graph open

The watchdog approach was verified working: Obsidian opens with 23 color groups active, watchdog survives, graph shows colored clusters.

**Quick restart command (watchdog):**
```bash
taskkill //F //IM Obsidian.exe
python3 "C:/Users/shrey/AppData/Local/Programs/Obsidian/graph-color-watchdog.py" &
sleep 2
"C:/Users/shrey/AppData/Local/Programs/Obsidian/Obsidian.exe"
```

### Alternative: Vault-Local Restore Script (no watchdog needed)

For vaults on external drives or where you prefer manual control, use the vault-local restore script instead of the system watchdog:

**Script**: `{vault}/.obsidian/restore-graph-colors.sh`

```bash
#!/usr/bin/env bash
# Run this AFTER Obsidian starts, or add to your Obsidian launch wrapper
VAULT="E:/_Knowledge/ObsidianVault"
cp "$VAULT/.obsidian/graph.json.backup.permanent" "$VAULT/.obsidian/graph.json"
echo "✅ Restored color groups from permanent backup"
```

**Workflow**:
1. After configuring `graph.json` with all color groups, create permanent backup:
   ```bash
   cp "E:/_Knowledge/ObsidianVault/.obsidian/graph.json" \
      "E:/_Knowledge/ObsidianVault/.obsidian/graph.json.backup.permanent"
   ```
2. When Obsidian clears colors (on startup or graph open), run the restore script
3. Open/refresh graph (`Ctrl+G` twice) — colors appear

This works because Obsidian reads `graph.json` fresh each time the graph panel opens. The restore just needs to land before you open the graph view.

The watchdog approach was verified working: Obsidian opens with 23 color groups active, watchdog survives, graph shows colored clusters.

### Correct Color Group Format

The format uses **separate r/g/b integer keys**, NOT hex strings or integer RGB:

```json
"colorGroups": [
  {
    "query": "path:02 - AREAS/03 Ancient Civilizations",
    "color": {"r": 249, "g": 115, "b": 22},
    "name": "Ancient Civilizations"
  }
]
```

- **`query`**: Obsidian search syntax — `path:folder-name` (relative, NO leading slash), `tag:#tagname`, combinations with `OR`
- **Pitfall**: `path:/folder` with a leading slash silently matches NOTHING. Always write `path:folder` (relative to vault root). Example: use `path:02 - AREAS/03 Ancient Civilizations`, never `path:/02 - AREAS/03 Ancient Civilizations`.
- **`color`**: Object with `r`, `g`, `b` keys (0–255 integers), NOT `{"rgb": 12345678}` or `#RRGGBB`
- **`name`**: Optional label shown in the Color Groups panel

### CSS Snippets DO Work for Node Coloring

The graph container gets a class like `.color-fill-r249-g115-b22` (one per color group). CSS selectors targeting these classes **DO color canvas-rendered nodes**:

```css
/* Ancient Civilizations — r249,g115,b22 → #F97316 */
.graph-view.color-fill-r249-g115-b22 .node {
    fill: #7c2d12 !important;
    stroke: #f97316 !important;
}
.graph-view.color-fill-r249-g115-b22 .node:hover {
    fill: #ea580c !important;
    stroke: #fb923c !important;
}
```

**Rule**: For every color group in `graph.json`, add a matching CSS rule using `color-fill-r{R}-g{G}-b{B}` (no `#`, all three values). This works because Obsidian adds these classes to the graph container DOM element — the canvas renderer reads the CSS classes.

### Real-World 23-Group Configuration (Verified Working)

This exact configuration was applied to a 50k-node vault (E:/_Knowledge/ObsidianVault) on 2026-07-30:

```json
"colorGroups": [
  {"query": "path:02 - AREAS/03 Ancient Civilizations", "color": {"r": 249, "g": 115, "b": 22}},
  {"query": "path:02 - AREAS/01 Philosophy & Religion", "color": {"r": 168, "g": 85, "b": 247}},
  {"query": "path:02 - AREAS/02 AI & Technology", "color": {"r": 16, "g": 185, "b": 129}},
  {"query": "path:02 - AREAS/04 Political Analysis", "color": {"r": 239, "g": 68, "b": 68}},
  {"query": "path:02 - AREAS/05 Knowledge Management", "color": {"r": 59, "g": 130, "b": 246}},
  {"query": "path:02 - AREAS/06 Personal Development", "color": {"r": 236, "g": 72, "b": 153}},
  {"query": "path:02 - AREAS/07 Society & Culture", "color": {"r": 234, "g": 179, "b": 8}},
  {"query": "path:01 - LITERATURE/", "color": {"r": 6, "g": 182, "b": 212}},
  {"query": "path:03 - PROJECTS/Active", "color": {"r": 245, "g": 158, "b": 11}},
  {"query": "path:03 - PROJECTS/Completed", "color": {"r": 132, "g": 204, "b": 22}},
  {"query": "path:03 - PROJECTS/concepts", "color": {"r": 132, "g": 204, "b": 22}},
  {"query": "path:03 - PROJECTS/people", "color": {"r": 99, "g": 102, "b": 241}},
  {"query": "path:03 - PROJECTS/questions", "color": {"r": 20, "g": 184, "b": 166}},
  {"query": "path:04 - DAILY", "color": {"r": 100, "g": 116, "b": 139}},
  {"query": "path:05 - MEMORY", "color": {"r": 14, "g": 165, "b": 233}},
  {"query": "path:05 - INTELLIGENCE", "color": {"r": 139, "g": 92, "b": 246}},
  {"query": "path:05 - OUTPUTS", "color": {"r": 244, "g": 114, "b": 182}},
  {"query": "path:06 - OUTPUTS", "color": {"r": 244, "g": 114, "b": 182}},
  {"query": "tag:#moc", "color": {"r": 255, "g": 255, "b": 255}},
  {"query": "tag:#index", "color": {"r": 209, "g": 213, "b": 219}},
  {"query": "tag:#dravidian", "color": {"r": 249, "g": 115, "b": 22}},
  {"query": "tag:#ancient-civilization", "color": {"r": 251, "g": 146, "b": 60}},
  {"query": "tag:#ai", "color": {"r": 16, "g": 185, "b": 129}}
],
"collapse-color-groups": false,
"showArrow": true,
"textFadeMultiplier": 0.3,
"nodeSizeMultiplier": 1.3,
"lineSizeMultiplier": 0.7,
"repelStrength": 15,
"linkDistance": 180,
"centerStrength": 0.6,
"linkStrength": 0.8
```

### Critical Path Query Format

**USE RELATIVE PATHS WITHOUT LEADING SLASH:**
```json
{"query": "path:02 - AREAS/03 Ancient Civilizations", "color": {...}}
```

**NEVER USE LEADING SLASH** — `path:/folder` silently matches NOTHING:
```json
{"query": "path:/02 - AREAS/03 Ancient Civilizations", "color": {...}}  // WRONG - matches nothing
```

### Complete CSS Snippet (pro-graph-view.css)

```css
.graph-view, .graph-view canvas { background-color: #0f0d1a !important; }
.graph-view .node { fill: #2a2a3e !important; stroke: #4b5563 !important; stroke-width: 1.5px !important; }
.graph-view .node:hover { fill: #4f46e5 !important; stroke: #818cf8 !important; stroke-width: 2.5px !important; }
.graph-view .node:focus, .graph-view .node.active { fill: #6366f1 !important; stroke: #a5b4fc !important; stroke-width: 3px !important; }
.graph-view .node .node-label { fill: #e2e8f0 !important; font-family: 'Inter', 'Segoe UI', -apple-system, sans-serif !important; font-size: 9px !important; font-weight: 500 !important; text-shadow: 0 1px 3px rgba(0,0,0,0.9), 0 0 8px rgba(0,0,0,0.7) !important; opacity: 0.85 !important; }
.graph-view .node:hover .node-label { fill: #ffffff !important; font-weight: 600 !important; font-size: 10px !important; opacity: 1 !important; }
.graph-view .link { stroke: #3a3055 !important; stroke-width: 1px !important; opacity: 0.5 !important; }
.graph-view .link:hover, .graph-view .link.hovered { stroke: #818cf8 !important; stroke-width: 2px !important; opacity: 0.9 !important; }
.graph-view .node.search-result { fill: #fbbf24 !important; stroke: #f59e0b !important; stroke-width: 2.5px !important; }
.graph-view .node.hovered { stroke: #a5b4fc !important; stroke-width: 2.5px !important; }

/* Color group classes — one per group in graph.json */
.graph-view.color-fill-r249-g115-b22 .node { fill: #7c2d12 !important; stroke: #f97316 !important; }
.graph-view.color-fill-r249-g115-b22 .node:hover { fill: #ea580c !important; stroke: #fb923c !important; }
.graph-view.color-fill-r168-g85-b247 .node { fill: #3b1f6e !important; stroke: #a855f7 !important; }
.graph-view.color-fill-r168-g85-b247 .node:hover { fill: #7c3aed !important; stroke: #c084fc !important; }
.graph-view.color-fill-r16-g185-b129 .node { fill: #064e3b !important; stroke: #10b981 !important; }
.graph-view.color-fill-r16-g185-b129 .node:hover { fill: #047857 !important; stroke: #34d399 !important; }
.graph-view.color-fill-r239-g68-b68 .node { fill: #450a0a !important; stroke: #ef4444 !important; }
.graph-view.color-fill-r239-g68-b68 .node:hover { fill: #b91c1c !important; stroke: #f87171 !important; }
.graph-view.color-fill-r59-g130-b246 .node { fill: #1e3a5f !important; stroke: #3b82f6 !important; }
.graph-view.color-fill-r59-g130-b246 .node:hover { fill: #1d4ed8 !important; stroke: #60a5fa !important; }
.graph-view.color-fill-r236-g72-b153 .node { fill: #4c0519 !important; stroke: #ec4899 !important; }
.graph-view.color-fill-r236-g72-b153 .node:hover { fill: #9d174d !important; stroke: #f472b6 !important; }
.graph-view.color-fill-r234-g179-b8 .node { fill: #451a03 !important; stroke: #eab308 !important; }
.graph-view.color-fill-r234-g179-b8 .node:hover { fill: #854d0e !important; stroke: #facc15 !important; }
.graph-view.color-fill-r6-g182-b212 .node { fill: #083344 !important; stroke: #06b6d4 !important; }
.graph-view.color-fill-r6-g182-b212 .node:hover { fill: #0e7490 !important; stroke: #22d3ee !important; }
.graph-view.color-fill-r245-g158-b11 .node { fill: #451a03 !important; stroke: #f59e0b !important; }
.graph-view.color-fill-r245-g158-b11 .node:hover { fill: #b45309 !important; stroke: #fbbf24 !important; }
.graph-view.color-fill-r132-g204-b22 .node { fill: #1a2e05 !important; stroke: #84cc16 !important; }
.graph-view.color-fill-r132-g204-b22 .node:hover { fill: #3f6212 !important; stroke: #a3e635 !important; }
.graph-view.color-fill-r99-g102-b241 .node { fill: #1e1b4b !important; stroke: #6366f1 !important; }
.graph-view.color-fill-r99-g102-b241 .node:hover { fill: #3730a3 !important; stroke: #818cf8 !important; }
.graph-view.color-fill-r20-g184-b166 .node { fill: #042f2e !important; stroke: #14b8a6 !important; }
.graph-view.color-fill-r20-g184-b166 .node:hover { fill: #115e59 !important; stroke: #2dd4bf !important; }
.graph-view.color-fill-r100-g116-b139 .node { fill: #1e293b !important; stroke: #64748b !important; }
.graph-view.color-fill-r100-g116-b139 .node:hover { fill: #334155 !important; stroke: #94a3b8 !important; }
.graph-view.color-fill-r14-g165-b233 .node { fill: #0c4a6e !important; stroke: #0ea5e9 !important; }
.graph-view.color-fill-r14-g165-b233 .node:hover { fill: #0369a1 !important; stroke: #38bdf8 !important; }
.graph-view.color-fill-r139-g92-b246 .node { fill: #2e1065 !important; stroke: #8b5cf6 !important; }
.graph-view.color-fill-r139-g92-b246 .node:hover { fill: #5b21b6 !important; stroke: #a78bfa !important; }
.graph-view.color-fill-r244-g114-b182 .node { fill: #500724 !important; stroke: #f472b6 !important; }
.graph-view.color-fill-r244-g114-b182 .node:hover { fill: #9d174d !important; stroke: #f9a8d4 !important; }
.graph-view.color-fill-r255-g255-b255 .node { fill: #1e293b !important; stroke: #ffffff !important; stroke-width: 2px !important; }
.graph-view.color-fill-r255-g255-b255 .node:hover { fill: #334155 !important; stroke: #f8fafc !important; }
.graph-view.color-fill-r209-g213-b219 .node { fill: #1f2937 !important; stroke: #d1d5db !important; }
.graph-view.color-fill-r209-g213-b219 .node:hover { fill: #374151 !important; stroke: #f3f4f6 !important; }
.graph-view.color-fill-r251-g146-b60 .node { fill: #431407 !important; stroke: #fb923c !important; }
.graph-view.color-fill-r251-g146-b60 .node:hover { fill: #7c2d12 !important; stroke: #fdba74 !important; }
.graph-view.color-fill-r16-g185-b129 .node { fill: #064e3b !important; stroke: #10b981 !important; }
.graph-view.color-fill-r16-g185-b129 .node:hover { fill: #047857 !important; stroke: #34d399 !important; }

/* Orphans/attachments */
.graph-view .node.color-orphan, .graph-view .node.color-attachment { fill: #2a2a3e !important; stroke: #6b7280 !important; }
.graph-view .node.color-orphan:hover, .graph-view .node.color-attachment:hover { fill: #374151 !important; stroke: #9ca3af !important; }

/* Controls/tooltips */
.graph-view .controls { background: #1a1528ee !important; border: 1px solid #3a3055 !important; backdrop-filter: blur(8px); border-radius: 8px; }
.graph-view .tooltip { background: #1a1528ee !important; border: 1px solid #3a3055 !important; color: #e2e8f0 !important; backdrop-filter: blur(8px); border-radius: 6px; font-family: 'Inter', 'Segoe UI', sans-serif !important; font-size: 12px !important; padding: 6px 10px !important; box-shadow: 0 4px 12px rgba(0,0,0,0.5) !important; }
```

### Recommended Color Palette (distinct, saturated)

| Folder / Topic | R | G | B | Hex |
|---|---|---|---|---|
| Ancient Civilizations | 249 | 115 | 22 | #F97316 |
| Philosophy & Religion | 168 | 85 | 247 | #A855F7 |
| AI & Technology | 16 | 185 | 129 | #10B981 |
| Political Analysis | 239 | 68 | 68 | #EF4444 |
| Knowledge Management | 59 | 130 | 246 | #3B82F6 |
| Personal Development | 236 | 72 | 153 | #EC4899 |
| Society & Culture | 234 | 179 | 8 | #EAB308 |
| Literature / Papers | 6 | 182 | 212 | #06B6D4 |
| Active Projects | 245 | 158 | 11 | #F59E0B |
| Completed Projects | 132 | 204 | 22 | #84CC16 |
| People | 99 | 102 | 241 | #6366F1 |
| Questions | 20 | 184 | 166 | #14B8A6 |
| Daily Notes | 100 | 116 | 139 | #64748B |
| Memory | 14 | 165 | 233 | #0EA5E9 |
| Intelligence | 139 | 92 | 246 | #8B5CF6 |
| Outputs | 244 | 114 | 182 | #F472B6 |
| MOC Hub Files | 255 | 255 | 255 | #FFFFFF |
| Dravidian tag | 249 | 115 | 22 | #F97316 |
| ancient-civilization tag | 251 | 146 | 60 | #FB923C |

### Supporting References

- `references/obsidian-graph-colors.md` — Full graph.json colorGroups + CSS snippet rules + backup/restore workflow
- `references/graph-presets.md` — 6 graph presets for 50k-node vault (Knowledge Atlas, Active Intelligence, Dravidian Deep-Dive, AI & Tech Radar, Writing Pipeline, Orphan Hunter)
- `references/minimal-flexoki-theme.md` — Minimal Theme + Flexoki Dark config for second brains (Style Settings data.json, graph settings, migration guide)
- `scripts/graph-color-watchdog.py` — Background watchdog that restores colors every 5s

### Physics Settings

```json
"nodeSizeMultiplier": 1.3,
"lineSizeMultiplier": 1,
"repelStrength": 15,
"linkDistance": 180,
"centerStrength": 0.6,
"linkStrength": 0.8,
"textFadeMultiplier": 0.3,
"showArrow": true,
"showOrphans": true,
"showTags": true,
"collapse-color-groups": false
```

### How to Enable

1. Open Obsidian → `Ctrl+G` (Global Graph)
2. Click **Display** panel → Toggle **Color Groups** ON
3. Settings → Appearance → CSS Snippets → enable your CSS file
4. Reload Obsidian if colors don't appear

### ⚠️ Always Verify Vault Structure First

Don't assume folder names. **Before generating `path:` queries, list the actual top-level folders** in the vault — they vary wildly:

```bash
ls -d "VAULT_PATH/"*/ 
```

Common traps:
- `03 - PROJECTS/` may contain `Agentic-OS/`, `History-Watchdog/` instead of `Active/`, `Completed/`
- Lowercase inbox folders (`0-Inbox/`, `0-raw/`, `1-desk/`, `2-atoms/`, `3-threads/`) sit alongside numbered PARA folders
- `02 - AREAS/` may have `06 Society & Culture` and `06 Personal Development` (duplicate prefixes!) — match exactly

**Also verify which tags actually exist** before adding tag-based color groups:

```bash
grep -roh "#tagname[a-zA-Z_]*" "VAULT_PATH" --include="*.md" | sort | uniq -c | sort -rn
```

If you generate color groups for non-existent folders or tags, Obsidian silently ignores them and the graph stays monochrome. The user sees no error — just a flat-color graph. The fix is always: re-list the vault, regenerate the queries, reload.

### What CSS Can Style

CSS snippets can style: outer panel background, tooltip background/color/border, and node fill/stroke via the `.color-fill-r{R}-g{G}-b{B}` class mechanism. Generic `.graph-view .node` rules only affect the default (ungrouped) node appearance.

---

### Recommended Theme for Second Brains: Minimal + Flexoki Dark

For large vaults (10k–100k nodes) used as second brains, **Minimal Theme** (v8+) with the **Flexoki Dark** color scheme is the best default. It provides:

- **Typography**: Inter (UI/Text) + JetBrains Mono (code) — scales without visual noise
- **200+ tweaks via Style Settings**: line width, heading style, metadata, focus mode, graph integration
- **12 built-in color schemes**: Catppuccin, Nord, Dracula, Everforest, Flexoki, Gruvbox, Rose Pine, Solarized, macOS, Things, Notion, Default
- **Graph harmony**: Dark palette matches `pro-graph-view.css` perfectly
- **Performance**: No heavy animations, clean DOM — handles 50k nodes smoothly

**Settings to configure** (Settings → Appearance → Minimal Theme Settings):

| Setting | Value | Rationale |
|---------|-------|-----------|
| Color Scheme | Flexoki Dark | Warm, low-eye-strain, good graph contrast |
| Accent Color | `#6366f1` (Indigo) | Calm, professional |
| Editor Font | JetBrains Mono | Code-heavy notes |
| Text Font | Inter | Readable at 15px base |
| Line Width | 88 chars | Readable column |
| Line Height | 1.6 | Breathing room |
| Focus Mode | Typewriter | Deep work |
| Graph Background | Dark | Matches CSS snippet |
| Graph Node Color | Color Group | Uses your 23 groups |
| Graph Accent Links | ON | Links get accent color |
| Colorful Active Tab | ON | Visual tab identity |

**Style Settings data file** (auto-created at `{vault}/.obsidian/plugins/obsidian-style-settings/data.json`):

```json
{
  "minimal-style:colorScheme": "minimal-flexoki-dark",
  "minimal-style:customBaseHue": 0,
  "minimal-style:customBaseSaturation": 3,
  "minimal-style:customAccentHue": 175,
  "minimal-style:customAccentSaturation": 49,
  "minimal-style:fontEditor": "JetBrains Mono",
  "minimal-style:fontEditorSize": 15,
  "minimal-style:fontInterface": "Inter",
  "minimal-style:fontInterfaceSize": 14,
  "minimal-style:fontText": "Inter",
  "minimal-style:fontTextSize": 15,
  "minimal-style:lineWidth": 88,
  "minimal-style:lineHeight": 1.6,
  "minimal-style:focusMode": "typewriter",
  "minimal-style:focusModeDim": true,
  "minimal-style:graphBackground": "dark",
  "minimal-style:graphNodeColor": "colorGroup",
  "minimal-style:graphLinkColor": "muted",
  "minimal-style:graphTextFade": 0.3,
  "minimal-style:graphNodeSize": 1.3,
  "minimal-style:graphLineWidth": 0.7,
  "minimal-style:graphRepelForce": 15,
  "minimal-style:graphCenterForce": 0.6,
  "minimal-style:graphLinkDistance": 180,
  "minimal-style:graphLinkStrength": 0.8,
  "minimal-style:accentColorLinks": true,
  "minimal-style:accentColorTags": true,
  "minimal-style:accentColorSearch": true,
  "minimal-style:accentColorGraph": true,
  "minimal-style:colorfulActiveTab": true,
  "minimal-style:animations": "reduced"
}
```

This replaces the manual `appearance.json` edits with a single plugin config that survives Obsidian updates and is portable across machines.

---

## Track B: D3.js Knowledge Graph

Use when the user wants glow, animated background, rich tooltips, legend, or professional polish that the native graph cannot provide.

### Script
```
{vault}/professional_graph.py
```

### Run
```bash
"C:/Users/shrey/AppData/Local/Programs/Python/Python314/python.exe" professional_graph.py
```

### Key features
- Animated nebula canvas background
- 3-tier hub glow (degree >20/12/6)
- Domain color palette (16+ colors)
- Community ring overlays (toggleable)
- Hover tooltips: domain, degree, community, linked notes, tags
- Search filter, tags toggle, community toggle, reset view
- Output: `{vault}/obsidian_graph.html`

### Domain palette (update for your vault)
```python
DOMAIN_PALETTE = {
    "Ancient Civilizations": "#f97316",
    "Philosophy & Religion": "#a855f7",
    "AI & Technology": "#10b981",
    "Political Analysis": "#ef4444",
    "Knowledge Management": "#3b82f6",
    "Personal Development": "#ec4899",
    "Society & Culture": "#eab308",
    "tag": "#ffffff",
    "default": "#636e72",
}
```

### Graph Presets Reference
See `references/graph-presets.md` for 6 ready-to-create presets tailored to a 50k-node vault (Knowledge Atlas, Active Intelligence, Dravidian Deep-Dive, AI & Tech Radar, Writing Pipeline, Orphan Hunter).

### Performance targets
- Cap nodes at 400–600 for smooth physics
- Use greedy modularity with degree-fallback if community detection times out
- Parse wikilinks `\\[\\[(.*?)\\]\\]` and tags `#([\\w/-]+)` from all `.md` files
- Exclude: `.obsidian`, `.git`, `node_modules`, `_trash`, `.trash`

### Verification
- HTML file > 50 KB
- `__GRAPH_DATA__` replaced with actual JSON
- `d3.min.js` present via CDN
- `forceSimulation` present

### Common errors

| Error | Fix |
|-------|-----|
| `ModuleNotFoundError: No module named 'networkx'` | Use Python 3.14 directly |
| `__GRAPH_DATA__` still in output | `json.dumps` replacement failed — check substitution |
| Graph looks clumped | Lower `forceCharge`, increase `collide` separation |