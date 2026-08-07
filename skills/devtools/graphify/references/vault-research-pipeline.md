# Obsidian Vault Research Pipeline

Reading PDFs from the vault's `BOOKS/pdfs/` or Downloads folder and converting them into structured, linked research notes.

## When to use

User drops a research paper (PDF) and asks to "store and link" it in the vault — or asks to read/summarize a PDF. Applies to: academic papers, genetic studies, historical documents, primary sources.

## Required tool: pymupdf on Python 3.14

**pymupdf is NOT on the default python3.** It is on the Python 3.14 install:

```
Python 3.14 path:  C:/Users/shrey/AppData/Local/Programs/Python/Python314/python.exe
Graphify CLI:       C:/Users/shrey/AppData/Local/Programs/Python/Python314/Scripts/graphify
```

**Use terminal with explicit path — do NOT use execute_code (it blocks pymupdf):**
```bash
"/c/Users/shrey/AppData/Local/Programs/Python/Python314/python.exe" -c "
import pymupdf
doc = pymupdf.open('path/to/file.pdf')
..."
```

## Core pattern: PDF → Structured Research Note

```python
import pymupdf, os

fname = "path/to/paper.pdf"
doc = pymupdf.open(fname)
print(f"Pages: {doc.page_count}")

# Read first 3-4 pages for context
for i in range(min(3, doc.page_count)):
    page = doc[i]
    text = page.get_text()
    print(f"--- Page {i+1} ---")
    print(text[:600])
doc.close()
```

## Research Note Template (copy and modify)

```markdown
---
title: "[Paper Title]"
authors:
  - [Author 1]
  - [Author 2]
date: [YYYY-MM-DD]
status: active
type: research-paper
tags: [topic, subtopic, evidence-type]
subject: [1-line description]
doi: "https://doi.org/..."
journal: [Journal Name]
institution:
  - "[Affiliation 1]"
  - "[Affiliation 2]"
pdf: BOOKS/pdfs/[filename.pdf]
related_vault_notes:
  - "[[Project Note]]"
  - "[[BOOKS/notes/Related Book]]"
confidence: [high|moderate|low]
grading: [strong-evidence|preliminary|corrected]
---

# [Paper Title]

> **Authors:** [list]
> **Published:** [Journal], [Year]
> **DOI:** https://doi.org/...

## Core Finding

[2-3 sentence summary of the main result]

## Key Data Table

| Item | Value |
|------|-------|
| [Row 1] | [Val 1] |
| [Row 2] | [Val 2] |

## Why This Matters for [User's Project]

1. **[Specific relevance]:** [explanation]
2. **[Specific relevance]:** [explanation]

## Evidence Grade

> **Evidence Grade:** [Strong/Preliminary/Corrected]
> **Confidence:** [Settled/Moderate/Weak]
> **Caveat:** [Any methodological limitations]

## Key Quotes

> *"Direct quote from paper."* — p.X

## Relevant for

- [[Project/MOC Note]] — brief relevance statement

## References

- [Full citation]
```

## Linking Pattern (Critical — multi-note wiring)

When storing a research paper, link it into:
1. **The specific project MOC** it belongs to (e.g., Dravidian Folk Deities & Sanskritization)
2. **The relevant synthesis/hub note** (e.g., Aryan Migration synthesis)
3. **The book's note** if it covers the same topic

Link format: add to frontmatter `related_vault_notes: []` AND patch the target note with a brief mention.

## Correction Files — Handling Ellipsis in Filenames

Some papers (e.g., "Correction to: Paper Title...") have `…` (U+2026) or `...` (three dots) in filenames. Direct path construction FAILS. Use:

```python
import os

d = r'C:\Users\shrey\Downloads'
for f in os.listdir(d):
    if 'orrection' in f and 'Neolithic' in f:
        full = os.path.join(d, f)
        doc = pymupdf.open(full)
        # ... process
```

Never construct the path as a string literal — use directory listing with string matching.

## Evidence Grading Scale

Use this in frontmatter for research papers:

| Grade | Meaning |
|-------|---------|
| `strong-evidence` | Peer-reviewed, full methodology, replicable |
| `preliminary` | Preprint, limited sample, or single study |
| `corrected` | Original had errors; correction applied |

## Factual Verification Pitfall (2026-07-21)

When presenting factual claims — especially names, dates, institutional affiliations, and legal opinions — **verify every specific name against sources before stating it as fact.** This applies whether doing legal analysis, research synthesis, or biographical summaries.

**Concrete failure:** CJI name was hallucinated as "Bhanuja Das" in a constitutional analysis of CJP protests. Actual CJI: **Surya Kant**. The broader pattern: AI models fabricate plausible-sounding names/dates/quotes with high confidence when synthesizing across multiple news sources — the output *feels* well-researched but contains made-up details.

**Fix workflow:**
1. Before presenting any named entity as fact → cross-check against at least one live source (Wikipedia, Reuters, etc.)
2. If a source is inaccessible (CAPTCHA, 403), **state that explicitly** rather than relying on training-data memory
3. Distinguish between "established legal principles" (which are stable and don't need per-incident verification) and "specific factual claims about current events" (which MUST be verified live)
4. When uncertain about a name/date/quote → say "one source reports…" with the source name, not "the CJI said…" as settled fact

This is a cross-cutting preference — the user has a low tolerance for fabricated authority and will flag errors.

## PDF Copy to Vault

```bash
cp "source/Downloads/path.pdf" "/vault/BOOKS/pdfs/short-name.pdf"
```

Always copy the PDF into the vault's `BOOKS/pdfs/` so the note's `pdf:` frontmatter link stays valid.