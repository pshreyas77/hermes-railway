---
date: YYYY-MM-DD
type: research
subtype: deep-dive|policy|technical-guide|evidence-update
tags: [domain, topic, ...]
priority: critical|high|medium|practical|personal
status: completed
source: "Live web search, academic databases, government notifications, primary texts"
ai-first: true
---

# Title — Subtitle

**For future Claude:** One-paragraph context: what gap this fills, vault location, priority.

---

## 1. Executive Summary

## 2. Evidence Tables (Tiered: Hard Evidence → Strong Hypothesis → Corrected Errors)

| Category | Detail |
|----------|--------|
| Key Finding | Evidence |
| ... | ... |

## 3. Methodology / Source Grading

| Source Type | Examples | Reliability |
|-------------|----------|-------------|
| Primary/Official | Government data, direct inscriptions, original texts | S |
| Academic/Peer-reviewed | Journal articles, monographs by established scholars | A |
| News Analysis/Secondary | Reputable outlets, think tank reports | NA |
| Community/Contested | Movement documents, organizational publications | C |

## 4. Vault Updates Required (checklist)

- [ ] Create entity/concept notes
- [ ] Update MOC tables
- [ ] Update project hubs
- [ ] Cross-link related notes

## 5. Entity/Concept Scaffolds (YAML frontmatter for new notes)

```yaml
# wiki/entities/NewEntity.md
---
date: YYYY-MM-DD
type: entity
tags: [entity, domain, ...]
priority: critical|high|medium
status: active|historical
source: "Report N: Title"
ai-first: true
---
```

## 6. Cross-Links

- [[MOC Name]]
- [[Research Report]]
- [[Entity Note]]

## 7. Sources Table

| Citation ID | Source | Date | Authority |
|-------------|--------|------|-----------|
| web_search:N#M | Source Name | YYYY-MM | S/A/NA/C |