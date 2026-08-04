---
name: kb-report
description: Generate structured markdown reports from wiki/ knowledge base in response to complex queries, with citations and backlinks
version: 1.0.0
category: knowledge-management
tags: [obsidian, knowledge-base, reporting, karpathy-method]
---

# kb-report Skill

Generate structured markdown reports from your wiki knowledge base in response to complex queries. Reports are saved to `reports/` with full citations linking back to wiki concepts and raw sources.

## Usage

```
/kb-report "Your complex question here"
/kb-report --topic "prediction markets" --format report
/kb-report --topic "LLM agents" --format slides --output reports/llm-agents-deck.md
```

## Workflow

1. Parse the query to identify relevant concepts and entities
2. Search `wiki/concepts/`, `wiki/entities/`, and `wiki/index/` for relevant pages
3. Read all relevant markdown files end-to-end
4. Synthesize a comprehensive answer with inline citations
5. Write report to `reports/YYYY-MM-DD-topic-slug.md`
6. Append report reference to relevant concept pages' "Reports" section

## Report Format

```markdown
---
query: "Your original question"
topic: "Topic Name"
date: "2026-07-12"
sources_used:
  - wiki/concepts/Concept-Name.md
  - wiki/entities/Entity-Name.md
  - 0-raw/source-file.md
confidence: 0.85
---

# Report: Your Question

## Executive Summary
2-3 paragraph synthesis answering the question directly.

## Detailed Analysis

### Subtopic 1
Content with inline citations like [[Concept Name]] or [0-raw/source.md].

### Subtopic 2
...

## Key Claims & Evidence
| Claim | Confidence | Sources |
|-------|------------|---------|
| Claim 1 | 0.9 | [[Concept 1]], 0-raw/source1.md |
| Claim 2 | 0.7 | [[Concept 2]] |

## Gaps & Open Questions
- Question 1
- Question 2

## Related Concepts
- [[Related Concept 1]]
- [[Related Concept 2]]

## Source Traceability
All claims trace back to:
- Wiki concepts: [[Concept 1]], [[Concept 2]]
- Raw sources: 0-raw/source1.md, 0-raw/source2.md
```

## Slide Deck Format (Marp)

```markdown
---
marp: true
theme: default
title: "Topic Title"
---

# Topic Title

---

## Executive Summary
...

---

## Key Finding 1
...
```

## Implementation Notes

- Use wiki wikilinks `[[Concept]]` for internal citations
- Use raw source paths `0-raw/file.md` for source citations
- Confidence scoring: 0.9+ = well-supported, 0.7-0.9 = probable, <0.7 = speculative
- Always include "Gaps & Open Questions" section
- Link report from relevant wiki concept pages (append to "Reports" section)
- Support both report and slide (Marp) output formats