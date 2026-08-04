---
name: pptx-from-code
description: "Generate PowerPoint .pptx files programmatically with python-pptx — when you need precise layout control, dark themes, or bulk generation from data. Use when the user wants slides generated from scratch (not from a template)."
tags: [powerpoint, pptx, python-pptx, slides, presentations]
platforms: [windows, linux, macos]
trigger: "create slides|pptx|presentation pptx|make me slides|generate slides"
---

# pptx-from-code

Generate `.pptx` files programmatically using `python-pptx`. Use when you need exact visual control — dark themes, precise layouts, data-driven slides, or bulk generation.

> **Companion:** The `powerpoint` skill covers design principles and templates. This skill covers the code-based generation path.

---

## Setup

### The hermes-agent venv PIL conflict (Windows)

**Problem:** When importing `pptx` via the default Windows Python (3.13 at `WindowsApps`), it fails with:
```
ImportError: cannot import name '_imaging' from 'PIL'
```
The hermes-agent virtualenv has a broken PIL that shadows the path.

**Fix — isolated venv with `PYTHONPATH=""`:**

```bash
# Create clean venv
uv venv C:/Users/shrey/AppData/Local/Temp/pptx_venv --python python3.14 -q

# Install python-pptx into it
uv pip install --python C:/Users/shrey/AppData/Local/Temp/pptx_venv/Scripts/python.exe python-pptx -q

# Run with PYTHONPATH="" to block broken hermes PIL
PYTHONPATH="" C:/Users/shrey/AppData/Local/Temp/pptx_venv/Scripts/python.exe your_script.py
```

> The `PYTHONPATH=""` trick is essential on Windows when hermes-agent's venv is in the process environment. It clears the contaminated sys.path before Python starts.

On Linux/macOS: `uv run --with python-pptx python your_script.py` works without isolation.

---

## Core API Pattern

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

prs = Presentation()
prs.slide_width  = Inches(13.33)  # 16:9 widescreen
prs.slide_height = Inches(7.5)

blank = prs.slide_layouts[6]       # truly blank layout
slide = prs.slides.add_slide(blank)

# Background rectangle
bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.33), Inches(7.5))
bg.fill.solid(); bg.fill.fore_color.rgb = RGBColor(0x0f, 0x0d, 0x1a)
bg.line.fill.background()

# Text box
txb = slide.shapes.add_textbox(Inches(0.5), Inches(1.0), Inches(8), Inches(1))
txb.text_frame.word_wrap = True
p = txb.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
r = p.add_run(); r.text = "Your title"
r.font.size = Pt(28); r.font.bold = True
r.font.color.rgb = RGBColor(0xF0, 0xEC, 0xE3); r.font.name = "Calibri"

# Table
t = slide.shapes.add_table(n_rows, n_cols, Inches(x), Inches(y), Inches(w), Inches(h)).table
t.columns[0].width = Inches(1.5)
cell = t.cell(0, 0); cell.text = "Header"
cell.text_frame.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0x00, 0x00)

prs.save("output.pptx")
```

---

## Color Palette (dark theme)

```python
BG    = RGBColor(0x0f, 0x0d, 0x1a)  # dark background
BG2   = RGBColor(0x1a, 0x15, 0x28)  # slightly lighter panel
ACC   = RGBColor(0xc8, 0x50, 0x30)  # red-orange accent
ACC2  = RGBColor(0x7b, 0x5e, 0xa7)  # purple accent
ACC3  = RGBColor(0x2a, 0x7a, 0x6a)  # teal accent
TEXT  = RGBColor(0xf0, 0xec, 0xe3)   # near-white text
MUTED = RGBColor(0xa0, 0x98, 0x80)   # muted/secondary text
BORDER= RGBColor(0x3a, 0x30, 0x55)   # subtle border
```

---

## Helper functions pattern

Always define reusable helpers to keep slide code DRY:

```python
def rect(slide, x, y, w, h, fill=None, line=None):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    s.line.fill.background()
    if fill: s.fill.solid(); s.fill.fore_color.rgb = fill
    else: s.fill.background()
    if line: s.line.color.rgb = line; s.line.width = Pt(0.5)
    return s

def txt(slide, text, x, y, w, h, fs=11, bold=False, color=TEXT,
        align=PP_ALIGN.LEFT, italic=False):
    txb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    txb.text_frame.word_wrap = True
    p = txb.text_frame.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = text
    r.font.size = Pt(fs); r.font.bold = bold; r.font.italic = italic
    r.font.color.rgb = color; r.font.name = "Calibri"
    return txb
```

---

## Design rules

Follow the `powerpoint` skill design section — dark theme, strong color contrast, left-aligned body text, no accent lines under titles:

- **Dark background** on every slide (`RGBColor(0x0f,0x0d,0x1a)`)
- **Color band at top** (red-orange `ACC` header strip, 0.07" tall)
- **Slide label** in accent color top-left, **slide number** top-right muted
- **Titles** 18-22pt bold near-white
- **Body tables** with alternating row shading
- **Color-coded state/region badges** using consistent per-region color constants

---

## QA

After generation, always verify content:
```bash
python -m markitdown output.pptx
```

Check for: missing text, wrong order, placeholder artifacts (`xxxx`, `lorem`), table overflow.

## PDF Export (when LibreOffice unavailable)

On Windows, LibreOffice is often not installed. If you need a PDF from the slides, build an HTML slideshow instead and print-to-PDF via Edge:

```bash
HTML="E:/path/to/Presentation.html"
PDF="E:/path/to/Presentation.pdf"
EDGE="C:/Program Files (x86)/Microsoft/Edge/Application/149.0.4022.98/msedge.exe"

"$EDGE" --headless --disable-gpu --no-pdf-header-footer --print-to-pdf="$PDF" "$HTML"
```

This works reliably. The HTML slideshow (dark-themed, keyboard-navigable) can be the primary artifact, with PPTX and PDF as derived outputs.

## See also

## See also

- `powerpoint` skill — design principles, color palettes, template workflow
- `knowledge-graph` skill — dark-themed HTML visualization (similar aesthetic)