# BOOKS/ Folder Restructure — 2026-07-09

## Session Context
User asked to professionally arrange BOOKS folder PDFs. Discovered 8 PDFs mixed with 51 notes in root, source tags in filenames, no cross-references.

## Before State
```
BOOKS/
├── 51 *.md notes (scattered)
├── 8 PDFs with messy names:
│   - Collected Works of Periyar E V R (Periyar E V Ramasamy) (z-library.sk, 1lib.sk, z-lib.sk).pdf
│   - WOF  Periyar E.V. Ramasami (E.V. Ramasami, Periyar) (z-library.sk, 1lib.sk, z-lib.sk).pdf
│   - Studies on the CarvakaLokayata (Bhattacharya, Ramkrishna) (z-library.sk, 1lib.sk, z-lib.sk).pdf
│   - The_Architecture_of_the_Bat.pdf
│   - indian constitution.pdf
│   - Ultimate Guide Rebuilding Civilization.pdf
│   - Surrounded by Psychopaths PDF.pdf
│   - Riddles in Hinduism (B.R. Ambedkar, Kancha Ilaiah) (z-library.sk, 1lib.sk, z-lib.sk).pdf
├── Books Library.md (catalog, 38 books, no PDF visibility)
├── Books Dashboard.md (Dataview querying wrong path)
├── covers/ (41 images)
```

## After State
```
BOOKS/
├── Books Library.md          # Master catalog with [PDF ✓] / 📝 Note only / 📝 Note created column
├── Books Dashboard.md        # Dataview FROM "BOOKS/notes"
├── covers/                   # unchanged
├── notes/                    # 55 notes (51 original + 4 new)
│   ├── Collected Works of Periyar E.V. Ramasamy.md       ✨ NEW
│   ├── Word for Word Periyar E.V. Ramasamy.md            ✨ NEW
│   ├── Studies on the Cārvāka Lokāyata.md                ✨ NEW
│   ├── Riddles in Hinduism.md                            ✨ NEW
│   └── ... (51 existing notes)
├── pdfs/                     # 8 clean kebab-case names
│   ├── ambedkar-riddles-in-hinduism.pdf
│   ├── architecture-of-the-bat.pdf
│   ├── bhattacharya-studies-on-carvaka-lokayata.pdf
│   ├── indian-constitution.pdf
│   ├── periyar-collected-works.pdf
│   ├── periyar-word-for-word.pdf
│   ├── surrounded-by-psychopaths.pdf
│   └── ultimate-guide-rebuilding-civilization.pdf
└── metadata/
    ├── pdfs-index.md         # Machine-readable index (8 rows, Has Note column)
    └── source-manifest.md    # Provenance moved here from filenames
```

---

## Renaming Map (Before → After)

| Original Filename | Clean Filename | Title | Author |
|-------------------|----------------|-------|--------|
| `Collected Works of Periyar E V R (Periyar E V Ramasamy) (z-library.sk, 1lib.sk, z-lib.sk).pdf` | `periyar-collected-works.pdf` | Collected Works of Periyar E.V. Ramasamy | Periyar E.V. Ramasamy |
| `WOF  Periyar E.V. Ramasami (E.V. Ramasami, Periyar) (z-library.sk, 1lib.sk, z-lib.sk).pdf` | `periyar-word-for-word.pdf` | Word for Word: Periyar E.V. Ramasamy | Periyar E.V. Ramasamy |
| `Studies on the CarvakaLokayata (Bhattacharya, Ramkrishna) (z-library.sk, 1lib.sk, z-lib.sk).pdf` | `bhattacharya-studies-on-carvaka-lokayata.pdf` | Studies on the Cārvāka/Lokāyata | Ramkrishna Bhattacharya |
| `The_Architecture_of_the_Bat.pdf` | `architecture-of-the-bat.pdf` | The Architecture of the Bat | (unknown) |
| `indian constitution.pdf` | `indian-constitution.pdf` | Constitution of India | (official) |
| `Ultimate Guide Rebuilding Civilization.pdf` | `ultimate-guide-rebuilding-civilization.pdf` | Ultimate Guide to Rebuilding Civilization | (unknown) |
| `Surrounded by Psychopaths PDF.pdf` | `surrounded-by-psychopaths.pdf` | Surrounded by Psychopaths | Thomas Erikson |
| `Riddles in Hinduism (B.R. Ambedkar, Kancha Ilaiah) (z-library.sk, 1lib.sk, z-lib.sk).pdf` | `ambedkar-riddles-in-hinduism.pdf` | Riddles in Hinduism | B.R. Ambedkar (intro Kancha Ilaiah) |

---

## Source Tags Moved to `source-manifest.md`

| Clean Filename | Original Source Tag | Notes |
|----------------|---------------------|-------|
| `periyar-collected-works.pdf` | `(z-library.sk, 1lib.sk, z-lib.sk)` | Primary text — verify against published edition if available |
| `periyar-word-for-word.pdf` | `(z-library.sk, 1lib.sk, z-lib.sk)` | Complementary volume — transcribed speeches/interviews |
| `bhattacharya-studies-on-carvaka-lokayata.pdf` | `(z-library.sk, 1lib.sk, z-lib.sk)` | Academic monograph — peer-reviewed source |
| `ambedkar-riddles-in-hinduism.pdf` | `(z-library.sk, 1lib.sk, z-lib.sk)` | Primary text by Ambedkar |

---

## 4 Priority PDF Notes Created (Aligns With Active Research)

| Note | PDF | Research Alignment |
|------|-----|-------------------|
| `Collected Works of Periyar E.V. Ramasamy.md` | `periyar-collected-works.pdf` | **Ambedkar vs Periyar comparative (Report 3)** — Dravidian primary source |
| `Word for Word Periyar E.V. Ramasamy.md` | `periyar-word-for-word.pdf` | **Ambedkar vs Periyar comparative** — transcribed speeches/interviews |
| `Studies on the Cārvāka Lokāyata.md` | `bhattacharya-studies-on-carvaka-lokayata.pdf` | **Tilak cultural-origin analysis** — Indian materialism primary source |
| `Riddles in Hinduism.md` | `ambedkar-riddles-in-hinduism.pdf` | **Anti-caste lineage** — Ambedkar's posthumous critique; Kancha Ilaiah intro |

**Note frontmatter pattern used:**
```yaml
---
title: "Exact Book Title"
author: ["Author Name"]
status: "To Read"  # To Read | Reading | Read | DNF
rating: 0          # 1-5
genre: "Domain / Category"
tags: [books, domain-tag, ...]
started: ""
finished: ""
pages: 0
isbn: ""
cover: "BOOKS/covers/descriptive.jpg"
pdf: "BOOKS/pdfs/clean-filename.pdf"
notes: "Context paragraph linking to active research"
---
```

---

## Files Modified/Created This Session

### Created
1. `.obsidian/templates/Book Template.md` — templater-ready frontmatter + sections
2. `BOOKS/metadata/pdfs-index.md` — machine-readable index (8 rows, Has Note/Note Filename/SHA256)
3. `BOOKS/metadata/source-manifest.md` — private source tracking (4 entries)
4. `BOOKS/notes/Collected Works of Periyar E.V. Ramasamy.md` — priority 1
5. `BOOKS/notes/Word for Word Periyar E.V. Ramasamy.md` — priority 2
6. `BOOKS/notes/Studies on the Cārvāka Lokāyata.md` — priority 3
7. `BOOKS/notes/Riddles in Hinduism.md` — priority 4

### Modified
1. `BOOKS/Books Library.md` — complete rewrite: master catalog with Format column `[PDF ✓]` / `📝 Note only` / `📝 Note created`, added Catalog Summary table (59 total, 55 notes, 8 PDFs)
2. `BOOKS/Books Dashboard.md` — updated all Dataview queries: `FROM "BOOKS"` → `FROM "BOOKS/notes"`

### Moved (via terminal execute_code)
- 8 PDFs → `BOOKS/pdfs/` with clean names
- 51 MD notes → `BOOKS/notes/`

---

## Naming Convention Codified

| Type | Pattern | Example |
|------|---------|---------|
| PDF | `{author-surname-or-doc-type}-{descriptor}.pdf` | `periyar-collected-works.pdf` |
| Note (MD) | `{Book Title}.md` | `Collected Works of Periyar E.V. Ramasamy.md` |
| Cover | `{ISBN}.jpg` preferred, or `{descriptive}.jpg` | `9780141188486.jpg` or `periyar.jpg` |

**Rules:**
- PDF: lowercase, kebab-case, no spaces, no source tags
- Note: Title Case matching bibliographic title
- Source tags → `metadata/source-manifest.md` only

---

## Template Frontmatter (`.obsidian/templates/Book Template.md`)

```yaml
---
title: "{{title}}"
author: ["{{author}}"]
status: "To Read"  # To Read | Reading | Read | DNF
rating: 0          # 1-5
genre: ""
tags: [books, "{{genre}}"]
started: ""
finished: ""
pages: 0
isbn: ""
cover: ""
pdf: ""  # relative path to PDF in BOOKS/pdfs/ if available
notes: ""
---
```

---

## Research Alignment (Why These 4 PDFs First)

| PDF | Note | Active Research |
|-----|------|-----------------|
| periyar-collected-works.pdf | ✅ | Ambedkar vs Periyar comparative (Report 3) |
| periyar-word-for-word.pdf | ✅ | Ambedkar vs Periyar comparative (Report 3) |
| bhattacharya-studies-on-carvaka-lokayata.pdf | ✅ | Cārvāka primary source for Tilak analysis (Aryan/Vedic, not Dravidian) |
| ambedkar-riddles-in-hinduism.pdf | ✅ | Anti-caste lineage, Aryan/Dravidian synthesis |

---

## Files Modified This Session

- `E:\_Knowledge\ObsidianVault\BOOKS\Books Library.md` (rewritten)
- `E:\_Knowledge\ObsidianVault\BOOKS\Books Dashboard.md` (Dataview path fix)
- `E:\_Knowledge\ObsidianVault\BOOKS\notes\Collected Works of Periyar E.V. Ramasamy.md` (new)
- `E:\_Knowledge\ObsidianVault\BOOKS\notes\Word for Word Periyar E.V. Ramasamy.md` (new)
- `E:\_Knowledge\ObsidianVault\BOOKS\notes\Studies on the Cārvāka Lokāyata.md` (new)
- `E:\_Knowledge\ObsidianVault\BOOKS\notes\Riddles in Hinduism.md` (new)
- `E:\_Knowledge\ObsidianVault\BOOKS\metadata\pdfs-index.md` (new/updated)
- `E:\_Knowledge\ObsidianVault\BOOKS\metadata\source-manifest.md` (new)
- `E:\_Knowledge\ObsidianVault\.obsidian\templates\Book Template.md` (new)

---

## Next Actions (For Future Sessions)

| Action | Trigger |
|--------|---------|
| Add frontmatter to 51 existing notes | When activating Dataview dashboard |
| Compute SHA256 for 8 PDFs | When integrity verification needed |
| Create notes for remaining 4 PDFs | When research aligns (Constitution, Bat, Civilization, Psychopaths) |
| Add cover images for 4 new notes | When reading begins (`BOOKS/covers/periyar.jpg`, `carvaka.jpg`, `ambedkar.jpg`) |

---

*Session: 2026-07-09 | Triggered by user: "Option C" → full restructure + priority note creation*