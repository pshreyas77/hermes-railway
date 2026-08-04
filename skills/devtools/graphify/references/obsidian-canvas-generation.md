# Obsidian Canvas Generation — Reference

Programmatic `.canvas` file generation for Obsidian vaults.

## When to use

Building flashcard galleries, book shelves, dashboards, or any card-grid canvas from structured vault data.

## Canvas JSON structure

```json
{
  "nodes": [
    { "id": "unique_id", "type": "text", "text": "<html content>",
      "x": 30, "y": 112, "width": 265, "height": 355 }
  ],
  "edges": [],
  "metadata": { "version": "1.0-1.0", "frontmatter": {} }
}
```

## Text node HTML

- Text nodes render HTML inline — use inline `style=` attributes
- Images: `file:///E:/path/to/image.jpg` (local) or `https://...` (remote)
- Cards render dark — use `background:#1e1e30`, `color:#f0f0f0`, `border-radius`
- Card dims: `width=265, height=355`; category headers: `height=60`
- Grid: `pad_x=28, pad_y=22` between cards

## execute_code workaround

If `execute_code` blocks a script:
```
1. write_file  → E:/_Dev_Tools/graphify/<script>.py
2. terminal    → cd E:/_Dev_Tools/graphify && python <script>.py
```

## Case-insensitive string matching

Always `.lower()` before `in` checks on genre/tag fields.
Genre field is often `Psychology` not `psychology` — a common bug.

```python
g = (fm.get("genre","") or "").lower()
t = " ".join(tags).lower()
all_text = g + " " + t + " " + title_lower
if any(k in all_text for k in ["fiction","novel","literary","beat"]):
    return "Fiction & Philosophy"
```

## Cover image slug matching

```python
book_slug = fn[:-3].lower().replace("-", " ").replace("'", "")
for lc in os.listdir(covers_dir):
    lc_slug = lc.lower().replace(".jpg","").replace("_","")
    if book_slug in lc_slug or lc_slug in book_slug or \
       any(p in lc_slug for p in book_slug.split() if len(p) > 4):
        local_path = os.path.join(covers_dir, lc)
        break
```

## Workflow

1. Load all source notes (frontmatter + body `## Key Takeaways` etc.)
2. Classify into groups, compute card positions
3. Build one JSON node per item
4. `write_file` to `vault/BOOKS/books-flashcards.canvas`
5. Verify: `json.load()` → count nodes, spot-check img src