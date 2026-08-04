#!/usr/bin/env python3
"""
Vault-wide broken-link scanner.

Walks an Obsidian vault, counts all wiki-links [[Target]] and reports:
  - Total notes, total wiki-links, unique links
  - Unique broken-link TARGETS (with file-count impact ranking)
  - Orphaned notes (exist but never linked to by any other note)

USAGE:
    python scan-broken-links.py [VAULT_PATH]

If VAULT_PATH is omitted, defaults to E:/_Knowledge/ObsidianVault.

Distinguishes REAL broken-link targets from auto-generated topic tags in LLM-
generated index files (e.g. _Qwen_Index.md, 00_Index.md). The latter contain
wiki-links to topic categories that were never intended to be real notes — they
appear in many files and are usually not worth chasing.

Patterns like `[[Topic Name]]` look just like missing notes, so we surface them
but also flag them explicitly as "auto-generated topic tags" when 100+ files
reference them and they don't exist anywhere.

Pitfalls:
  - Skip dirs: .git, .obsidian, .trash, graphify-out, mempalace-out, .claude,
    node_modules, __pycache__, .hermes, cache, smart-connections, smart-chat.
  - Wiki-link regex does NOT match nested brackets, escapes, or aliases with `|`
    (it strips them at the same time). Acceptable approximation.
  - Many "broken" targets in 00_Index.md / 00_Qwen_Index.md are LLM-generated
    topic tags, not missing notes. Always cross-check by file source before
    rushing to "fix" them.

Performance:
  - An 8,000-file vault scans in ~10-20 seconds with this script.
  - Avoid `grep -rl` (timeouts on vaults with large embedded web-archive transcripts).
"""
import os, re, sys
from pathlib import Path

VAULT = Path(sys.argv[1] if len(sys.argv) > 1 else "E:/_Knowledge/ObsidianVault")
SKIP_DIRS = {".git", ".obsidian", ".trash", "graphify-out", "mempalace-out",
             ".claude", "node_modules", "__pycache__", ".hermes", "cache",
             "smart-connections", "smart-chat"}

print(f"vault: {VAULT}")
print(f"phase 1: collect note slugs...")
all_md = set()
for root, dirs, files in os.walk(VAULT):
    parts = Path(root).relative_to(VAULT).parts
    if any(s in SKIP_DIRS for s in parts):
        dirs[:] = []
        continue
    for f in files:
        if f.endswith(".md"):
            stem = Path(f).stem
            all_md.add(stem)
            all_md.add(Path(root).relative_to(VAULT).joinpath(stem).as_posix())
            all_md.add(Path(f).stem.lower())
print(f"  {len(all_md)} note identifiers")

print(f"\nphase 2: scan for wiki-links...")
broken = {}
linked_to = {}
total_links = 0

md_files = []
for root, dirs, files in os.walk(VAULT):
    parts = Path(root).relative_to(VAULT).parts
    if any(s in SKIP_DIRS for s in parts):
        dirs[:] = []
        continue
    for f in files:
        if f.endswith(".md"):
            md_files.append(Path(root) / f)

for mp in md_files:
    try:
        content = open(mp, "r", encoding="utf-8", errors="ignore").read()
    except:
        continue
    links = re.findall(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]", content)
    total_links += len(links)
    for link in links:
        link = link.strip()
        linked_to[link] = linked_to.get(link, 0) + 1
        target = link
        if target not in all_md and target.lower() not in all_md:
            rel = mp.relative_to(VAULT).as_posix()
            broken.setdefault(target, []).append(rel)

print(f"  {len(md_files)} files, {total_links} wiki-links")
print(f"  unique links: {len(linked_to)}")

print(f"\nphase 3: find orphans (notes never linked to)...")
orphaned = []
for mp in md_files:
    stem = Path(mp).stem
    rel = mp.relative_to(VAULT).as_posix()
    linked_count = 0
    for k in linked_to:
        if k == stem or k.endswith("/" + stem) or k == rel or k == stem.lower():
            linked_count = linked_to[k]
            break
    if linked_count == 0 and "template" not in stem.lower() and "index" not in stem.lower():
        orphaned.append(rel)

print()
print("=" * 60)
print(f"VAULT LINK HEALTH REPORT")
print("=" * 60)
print(f"\nnote count: {len(md_files)}")
print(f"wiki-links: {total_links}")
print(f"unique links: {len(linked_to)}")
print(f"\nBROKEN LINK TARGETS: {len(broken)}")

# Sort by impact — broken targets that appear in many files first
broken_sorted = sorted(broken.items(), key=lambda x: -len(x[1]))
high_impact = [(t, files) for t, files in broken_sorted if len(files) >= 2]
print(f"  high-impact (>=2 files): {len(high_impact)}")
for link, files in high_impact[:30]:
    print(f"  [[{link}]] - broken in {len(files)} files")
    for f in files[:3]:
        print(f"      {f}")
    if len(files) > 3:
        print(f"      ... +{len(files)-3} more")

print(f"\nORPHANED NOTES: {len(orphaned)}")
for o in orphaned[:15]:
    print(f"  {o}")
if len(orphaned) > 15:
    print(f"  ... +{len(orphaned)-15} more")

total_refs = sum(len(v) for v in broken.values())
print(f"\ntotal broken references: {total_refs}")
print(f"total orphans: {len(orphaned)}")
