# Graph Presets for 50K-Node Second Brain

Create these in Obsidian → Settings → Graph Presets (after installing community plugin "Graph Presets" by bmgjet).

---

## Preset 1: "🏛️ Knowledge Atlas" — Full Vault Overview
- **Filters**: `path:/02 - AREAS` OR `path:/01 - LITERATURE` OR `path:/03 - PROJECTS` OR `path:/05 - MEMORY` OR `path:/05 - INTELLIGENCE` OR `path:/06 - OUTPUTS`
- **Groups**: ON (all 23 color groups)
- **Physics**: Center 0.6, Repel 15, Link 0.8, Distance 180
- **Display**: Arrows ON, Tags ON, Orphans OFF, Unresolved HIDDEN
- **Node Size**: 1.3x, Text Fade 0.3, Line 0.7x
- **Use case**: Daily big-picture navigation, finding cross-area connections

---

## Preset 2: "🧠 Active Intelligence" — Current Work
- **Filters**: `path:/03 - PROJECTS/Active` OR `path:/05 - MEMORY` OR `path:/05 - INTELLIGENCE` OR `tag:#active`
- **Groups**: ON (Active=Amber, Memory=Sky, Intelligence=Violet, AI=Green)
- **Physics**: Center 0.8, Repel 20, Link 1.0, Distance 150
- **Display**: Arrows ON, Tags ON
- **Node Size**: 1.5x
- **Use case**: Morning planning, active project context

---

## Preset 3: "🏛️ Dravidian Deep-Dive" — Research Cluster
- **Filters**: `path:/02 - AREAS/03 Ancient Civilizations` OR `tag:#dravidian` OR `tag:#ancient-civilization`
- **Groups**: ON (Ancient=Orange, Ancient-Civ=Light Orange, Literature=Cyan)
- **Physics**: Center 0.7, Repel 18, Link 0.9, Distance 200
- **Display**: Arrows ON, Tags ON, Orphans ON (spot disconnected research)
- **Node Size**: 1.4x
- **Use case**: Deep research sessions on Dravidian/ancient topics

---

## Preset 4: "🤖 AI & Tech Radar" — Technology Cluster
- **Filters**: `path:/02 - AREAS/02 AI & Technology` OR `tag:#ai`
- **Groups**: ON (AI=Emerald, Tech=Emerald)
- **Physics**: Center 0.5, Repel 12, Link 0.6, Distance 220
- **Display**: Arrows ON
- **Node Size**: 1.2x
- **Use case**: Tracking AI papers, tooling, experiments

---

## Preset 5: "📝 Writing & Output Pipeline" — Production View
- **Filters**: `path:/03 - PROJECTS/Active` OR `path:/05 - OUTPUTS` OR `path:/06 - OUTPUTS` OR `tag:#moc` OR `tag:#index`
- **Groups**: ON (Active=Amber, Outputs=Rose, MOC=White, Index=Light Gray)
- **Physics**: Center 0.4, Repel 10, Link 0.5, Distance 250
- **Display**: Arrows ON, Tags ON, Attachments OFF
- **Node Size**: 1.1x
- **Use case**: Weekly review, seeing what's ready to publish

---

## Preset 6: "🔍 Orphan Hunter" — Cleanup Mode
- **Filters**: `-tag:#moc` AND `-tag:#index` AND `-path:/04 - DAILY` AND `-path:/03 - PROJECTS`
- **Groups**: OFF (uniform color)
- **Physics**: Center 0.3, Repel 8, Link 0.4, Distance 300
- **Display**: Orphans ON, Unresolved ON, Tags OFF, Arrows OFF
- **Node Size**: 0.9x
- **Use case**: Monthly cleanup — find notes with no connections

---

## Quick-Switch Hotkeys (bind in Settings → Hotkeys)

| Hotkey | Preset |
|--------|--------|
| `Ctrl+Shift+1` | Knowledge Atlas |
| `Ctrl+Shift+2` | Active Intelligence |
| `Ctrl+Shift+3` | Dravidian Deep-Dive |
| `Ctrl+Shift+4` | AI & Tech Radar |
| `Ctrl+Shift+5` | Writing Pipeline |
| `Ctrl+Shift+6` | Orphan Hunter |

---

## Pro Tips for 50K Nodes

1. **Collapse Groups** (Graph sidebar → collapse-color-groups): ON for Atlas, OFF for deep-dives
2. **Search Filter** while in graph: Type `#dravidian` to isolate, then clear
3. **Local Graph** (note toolbar): Better for single-note context than global
4. **Canvas + Graph**: Drop a graph view on a Canvas for persistent reference
5. **Graph Presets Plugin**: Adds preset dropdown to graph toolbar — one-click switching