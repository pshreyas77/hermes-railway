# Canvas File Extraction — References

## Obsidian Canvas Format

`.canvas` files are JSON with a top-level object:
```json
{
  "nodes": [...],   // text, image, file, link, group, text
  "edges": [...],   // connections between nodes
  "metadata": { "version": "1.0-1.0", "frontmatter": {} }
}
```

## Node Types

| `type` | Has `text` | Has `file` | Has `x`,`y` |
|--------|-----------|------------|--------------|
| `"text"` | ✅ | ❌ | ✅ |
| `"file"` | ❌ | ✅ (path) | ✅ |
| `"link"` | ❌ | ❌ (has `url`) | ✅ |

## Extracting All Links from a Canvas

```python
import json, re
from pathlib import Path

canvas = json.loads(Path("path/to/file.canvas").read_text())

links = []
for node in canvas["nodes"]:
    if node.get("type") == "text":
        text = node["text"]
        # Markdown links: [display](url)
        for m in re.finditer(r'\[([^\]]+)\]\((https?://[^\)]+)\)', text):
            links.append({
                "display": m.group(1).strip(),
                "url": m.group(2).strip(),
                "x": node.get("x", 0),
                "y": node.get("y", 0),
            })
```

## Grouping by Visual Position (Philosopher Sections)

Canvas nodes use x/y coordinates for layout. In horizontal layouts:
- Philosopher sections have distinct x ranges
- Header nodes have `text` starting with `# Name`
- Resource nodes follow below each header

```python
def classify_by_x(x):
    if x < -500:   return "Philosopher A"
    elif x < -100: return "Philosopher B"
    elif x < 300:  return "Philosopher C"
    elif x < 750:  return "Philosopher D"
    else:          return "Philosopher E"
```

Adjust x thresholds based on your specific canvas layout.

## Classifying Link Type

```python
def classify_link(url):
    if "youtube" in url.lower():
        return "video"
    elif any(domain in url.lower() for domain in ["goodreads", "archive.org", "store", "shop", "holybooks", "scribd", "mlbd", "worldmets"]):
        return "book"
    elif any(domain in url.lower() for domain in ["kfoundation.org/video", "jkrishnamurti"]):
        return "video"  # some foundation pages are video indexes
    else:
        return "resource"
```

## Quick One-Liner (Terminal)

```bash
python3 -c "
import json,re
from pathlib import Path
c=json.loads(Path('path/to.canvas').read_text())
for n in c['nodes']:
 if n.get('type')=='text' and n.get('text'):
  for m in re.finditer(r'\[([^\]]+)\]\((https?://[^\)]+)\)',n['text']):
   print(m.group(2))
"
```

## Canvas File Locations in This Vault

- `03 - RESOURCES/Philosophy_Links_Tracker.canvas` — Indian philosophers playlist (source)
- `all canvas/Philosophy_Links_Tracker.canvas` — duplicate, avoid
- `02 - AREAS/01 Philosophy & Religion/Missing Philosophers Encyclopedia.canvas`
- `02 - AREAS/01 Philosophy & Religion/World Philosophers Encyclopedia.canvas`
- Many more in `all canvas/` and `02 - AREAS/` subdirectories