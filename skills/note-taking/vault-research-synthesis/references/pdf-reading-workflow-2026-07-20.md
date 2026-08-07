# PDF Reading from Vault — Research Paper Workflow

**Date:** 2026-07-20
**Context:** Sylvester et al. mtDNA paper + Ambedkar Riddles in Hinduism + Cārvāka/Lokāyata PDFs

---

## Setup: pymupdf on Windows

```bash
# Install to Python 3.14 (not Python 3.13 — mismatch)
uv pip install pymupdf --system

# Correct Python path (Python 3.13 default on PATH, but has no packages)
PYTHON="/c/Users/shrey/AppData/Local/Programs/Python/Python314/python.exe"
```

```python
import pymupdf

doc = pymupdf.open('/absolute/path/to/file.pdf')
print(f'Pages: {doc.page_count}')
for i in range(min(n, doc.page_count)):
    page = doc[i]
    text = page.get_text()
    print(f'--- Page {i+1} ---')
    print(text[:800])  # first 800 chars per page
doc.close()
```

---

## Vault PDF Locations

```
/vault/BOOKS/pdfs/
├── ambedkar-riddles-in-hinduism.pdf        (148 pages)
├── bhattacharya-studies-on-carvaka-lokayata.pdf  (253 pages)
├── periyar-collected-works.pdf             (527 pages)
├── periyar-word-for-word.pdf               (54 pages)
├── indian-constitution.pdf
├── sylvester-2018-neolithic-mtdna-melakudiya.pdf  (NEW — copied from Downloads)
└── sylvester-2018-correction.pdf           (NEW — copied from Downloads)
```

---

## Paper Ingestion Pipeline (Full)

### Step 1: Read the paper
- Extract abstract, intro, key findings, discussion, conclusions
- Note: authors, year, journal, DOI, GenBank accession numbers
- Check for correction notes

### Step 2: Create research note
```markdown
---
title: "Paper Short Title"
authors: [First Author, Second Author]
date: YYYY-MM-DD
status: active
type: research-paper
tags: [domain, topic, ...]
subject: One-line description
doi: "https://doi.org/..."
journal: Journal Name
institution: [Affiliation 1, Affiliation 2]
pdf: BOOKS/pdfs/short-filename.pdf
related_vault_notes:
  - "Path/to/related-note-1"
  - "Path/to/related-note-2"
confidence: primary-source
grading: strong-evidence
---

# Paper Full Title

> **Authors:** ...
> **Published:** Journal, Year
> **DOI:** https://...

## Core Finding
(2-3 sentence summary)

## Key Data Points
(table or list of most important numbers/claims)

## Why This Matters for Your Research
(specific connection to existing vault projects)

## Critical Context for Your Project
(caveats, confidence levels, what it does NOT prove)

## Key Quotes
(blockquotes of most quotable lines)

## Relevant for
- [[Related Vault Note]]
```

### Step 3: Copy PDF to vault
```bash
cp "C:/Users/shrey/Downloads/Original filename (with source tags).pdf" \
   "/vault/BOOKS/pdfs/short-clean-name.pdf"
```
Strip source tags like `(z-library.sk, 1lib.sk, z-lib.sk)` from filenames.

### Step 4: Link into existing research
1. Find the most relevant existing project note (e.g., `Dravidian Folk Deities & Sanskritization`)
2. Add to frontmatter `genetics_evidence:` or `sources:` field with wikilink + summary
3. If Tier 1 evidence: add row to appropriate evidence table in the synthesis note
4. Add back-reference in the paper's note to the project it supports

### Step 5: Check correction papers
- Search for "Correction to [paper title]" in the same folder
- If exists: create `paper-name-correction.md` noting what was corrected
- Copy correction PDF to vault alongside main paper
- In main paper note: add `Correction noted: ...` footer

---

## Windows Path Formats (Python)

```python
# Always use raw strings or forward slashes — backslashes escape
# These work:
pymupdf.open('/vault/BOOKS/pdfs/file.pdf')
pymupdf.open(r'E:\_Knowledge\ObsidianVault\BOOKS\pdfs\file.pdf')

# This FAILS:
pymupdf.open('E:\_Knowledge\ObsidianVault\...\file.pdf')  # \t \f etc.

# Finding files with special chars (brackets, spaces) in Downloads:
import glob
files = glob.glob(r'C:\Users\shrey\Downloads\*Neolithic*.pdf')
```

---

## Key Finding: mtDNA Phylogenetics Paper

**Sylvester et al. 2018** — Melakudiya tribe, Kodagu, Karnataka:
- 113 individuals, Dravidian-speaking tribal population
- 46/113 carried West Eurasian haplogroups HV14 + U7
- Two novel subclades: HV14a1b, HV14a1b1
- Coalescence ages: HV14 ~16.1 kya, U7a3a1a2* ~13.4 kya
- Supports proto-Dravidian origin in Elam (SW Iran) and Neolithic genetic continuity
- **Correction applied:** molecular dating section had rate calculation error

Linked to: `Dravidian Folk Deities & Sanskritization` (genetics evidence) + `Aryan Migration & Pre-Aryan Substrate` (Tier 1 evidence table)