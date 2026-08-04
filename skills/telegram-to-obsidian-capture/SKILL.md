---
name: telegram-to-obsidian-capture
description: Convert messy Telegram messages, voice transcriptions, URLs, PDFs, screenshots, and pasted conversations into Obsidian-ready notes with titles, summaries, source trails, tasks, wikilinks, and tags. Use when the Hermes and Telegram workflow receives raw captures for the vault.
---

# Telegram To Obsidian Capture

## Overview

Turn quick phone captures into useful Obsidian notes. Preserve the raw input, extract what matters, file it into the right vault location, and respond with a short confirmation the user can read on Telegram.

## Capture Contract

For every capture, produce one of these outcomes:

- Create a new source note.
- Create or update an existing project note.
- Create one or more atomic notes linked to a source.
- Place the capture in inbox with a clear question when classification is impossible.

## Workflow

1. Read the incoming Telegram material.
2. Identify the capture type:
   - Quick idea
   - Link
   - PDF/document
   - Voice transcription
   - Pasted conversation
   - Instruction or task
3. Preserve provenance:
   - Source should say `telegram`.
   - Include the URL, file name, sender context, or pasted-conversation label when available.
4. Create the note:
   - Use clear filenames.
   - Use Obsidian-compatible Markdown.
   - Add frontmatter.
   - Add wikilinks to existing concepts when obvious.
5. Update related notes:
   - Add to a project note if the capture changes active work.
   - Add to a map if the topic is recurring.
6. Reply briefly on Telegram:
   - What note was created or updated.
   - Where it was filed.
   - Any follow-up question.

## Output Standard

New capture notes should include:

```yaml
---
type: source
status: inbox
created: YYYY-MM-DD
source: telegram
tags:
  - source/telegram
---
```

Then:

- Summary
- Key points
- Raw capture
- Extracted notes or links
- Follow-ups

## Guardrails

- Do not pretend to read a PDF, webpage, screenshot, or audio file if its contents were not actually available.
- Do not over-organize tiny captures. A one-line idea can stay as a short note.
- Do not create fake backlinks.
- Do not expose sensitive Telegram content in public-facing outputs.
- Ask one concise follow-up question if the capture cannot be filed responsibly.

## Resources

- Read `references/capture-contract.md` for detailed examples and response formats.
- Use `assets/prompt-cards.md` when the user wants ready-to-send Telegram prompts.

## Completion Criteria

Finish when the capture is saved as useful Markdown, linked where appropriate, and the user receives a short confirmation that makes the vault location obvious.
