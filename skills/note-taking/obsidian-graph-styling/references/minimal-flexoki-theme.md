# Minimal Theme + Flexoki Dark — Second Brain Configuration

## Why This Combo for 10K–100K Node Vaults

| Factor | Minimal + Flexoki |
|--------|-------------------|
| **Typography** | Inter + JetBrains Mono — scales to 50k notes without visual noise |
| **Customization** | 200+ Style Settings toggles — no CSS needed |
| **Color Schemes** | 12 built-in (Catppuccin, Nord, Dracula, Everforest, Flexoki, Gruvbox, Rose Pine, Solarized, macOS, Things, Notion, Default) |
| **Graph Integration** | Native settings for graph background, node color strategy, link color, physics |
| **Performance** | Zero heavy animations, clean DOM |
| **Portability** | Single `data.json` in plugin folder — copy to new vault, done |

---

## Flexoki Dark Palette (warm, low-eye-strain)

```css
/* Base (auto-applied by theme) */
--base-h: 0;      /* neutral */
--base-s: 3%;     /* near-gray */
--base-l: 6%;     /* very dark */

--accent-h: 175;  /* teal */
--accent-s: 49%;
--accent-l: 45%;
```

| Role | Color | Use |
|------|-------|-----|
| Background | `#100F0F` | Deep warm black |
| Surface | `#1C1B1A` | Panels, cards |
| Border | `#282726` | Dividers |
| Text Primary | `#CECDC3` | Main content |
| Text Muted | `#878580` | Secondary |
| Accent | `#3AA99F` | Links, highlights |
| Accent Hover | `#24837B` | Interactive |

---

## Style Settings Config (copy to `{vault}/.obsidian/plugins/obsidian-style-settings/data.json`)

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
  "minimal-style:headingStyle": "none",
  "minimal-style:headingWeight": 600,
  "minimal-style:focusMode": "typewriter",
  "minimal-style:focusModeDim": true,
  "minimal-style:showActiveLine": true,
  "minimal-style:editorWidth": "readable",
  "minimal-style:tabStyle": "modern",
  "minimal-style:tabsCompact": true,
  "minimal-style:showTabCloseButton": true,
  "minimal-style:navFontSize": 13,
  "minimal-style:navShowIcons": true,
  "minimal-style:navIconStyle": "filled",
  "minimal-style:statusbarStyle": "minimal",
  "minimal-style:colorfulActiveTab": true,
  "minimal-style:accentColorLinks": true,
  "minimal-style:accentColorTags": true,
  "minimal-style:accentColorSearch": true,
  "minimal-style:accentColorGraph": true,
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
  "minimal-style:translucency": false,
  "minimal-style:animations": "reduced",
  "minimal-style:roundedCorners": "medium"
}
```

---

## Graph-Specific Settings (in Style Settings → Graph section)

| Setting | Value | Why |
|---------|-------|-----|
| Graph Background | Dark | Matches `pro-graph-view.css` |
| Graph Node Color | Color Group | Uses your 23 groups |
| Graph Link Color | Muted | Subtle connections |
| Graph Text Fade | 0.3 | Labels fade at distance |
| Graph Node Size | 1.3 | Readable at scale |
| Graph Line Width | 0.7 | Clean edges |
| Graph Repel Force | 15 | Separates clusters |
| Graph Center Force | 0.6 | Stable center |
| Graph Link Distance | 180 | Breathing room |
| Graph Link Strength | 0.8 | Tight communities |
| Accent Color Links | ON | Interactive links pop |
| Accent Color Tags | ON | Tag pills use accent |
| Accent Color Graph | ON | Search highlights use accent |

---

## Quick Switch: Alternative Schemes

If Flexoki feels too warm, swap in Style Settings → Color Scheme:

| Scheme | Vibe | Best For |
|--------|------|----------|
| **Catppuccin Mocha** | Soft pastel | Long reading sessions |
| **Nord** | Cool blue-gray | Code-heavy vaults |
| **Everforest Dark** | Green-nature | Research/biology |
| **Gruvbox Dark** | Warm retro | Terminal lovers |
| **Rose Pine Moon** | Muted purple | Creative writing |
| **Dracula** | High contrast | Presentations |
| **Solarized Dark** | Classic | Compatibility |
| **Things Dark** | Apple-like | macOS users |
| **Notion Dark** | Familiar | Notion migrants |

All preserve your graph color groups and physics — only UI chrome changes.

---

## Migration from Manual appearance.json

Old workflow (manual):
```json
// .obsidian/appearance.json — brittle, overwritten on update
{ "cssTheme": "GitHub Theme", "accentColor": "#d10000", ... }
```

New workflow (Style Settings):
1. Install Minimal Theme + Style Settings plugin
2. Settings → Appearance → CSS Theme → **Minimal**
3. Settings → Minimal Theme Settings → Color Scheme → **Flexoki Dark**
4. Configure 200+ options via UI — saved to `data.json`
5. Copy `data.json` to new vault → instant identical setup

No CSS snippets needed for theme-level tweaks. Keep `pro-graph-view.css` only for graph node coloring.