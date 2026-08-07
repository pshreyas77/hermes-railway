"""Search an Obsidian vault for a given tag.

Distinguishes three forms of "tag presence" so cron/agent jobs matching on tags
don't get fooled by stray prose mentions:

  1. YAML frontmatter array:   tags: [foo, bar]   or  tags:\n  - foo\n  - bar
  2. Inline body tag:          #foo   (must be word-bounded; not a URL fragment)
  3. Body prose mention:       "foo pipeline" -- NOT a tag, just text

Usage (matches the execute_code workaround pattern in the graphify SKILL.md):

    cd /home/hermes/graphify && python find-tag.py <vault> <tag>

Example:

    python find-tag.py /vault content-pipeline

Output:
    Section 1: file paths where the tag is real (frontmatter array OR inline #tag)
    Section 2: file paths where the string appears only as prose (NOT tags)
    Final summary line with counts.

Pitfalls we hit that this avoids:
  - `grep -rl <tag> --include="*.md"` over an 8k+ file vault with a `graphify-out/`
    dir can be slow / time out. Python with pathlib + per-file read is fast (sub-30s
    on 8,403 files in practice).
  - `rg` reads respect-ignore by default but ignores binary; UI/binary `.md` blobs
    (some are web-archive transcripts embedded as MD) need a binary-skip guard.
  - Frontmatter array form needs multiline regex; a naive `tags: ... <tag>` match
    misses the `[a, b, c]` form.
"""

from __future__ import annotations
import re
import sys
from pathlib import Path


def is_probably_text(p: Path, chunk: int = 1 << 20) -> bool:
    try:
        with p.open("rb") as fh:
            return b"\x00" not in fh.read(chunk)
    except OSError:
        return False


FRONTMATTER_ARRAY = re.compile(
    r"(?ms)^\s*tags\s*:\s*\[([^\]]*)\]"               # tags: [a, b, c]
)
FRONTMATTER_BLOCK = re.compile(
    r"(?ms)^\s*tags\s*:\s*\n((?:[ \t]*-\s*[^\n]+\n)+)"  # tags:\n  - a\n  - b
)
INLINE_TAG = re.compile(r"(?m)#([A-Za-z0-9_/-]+)\b")    # #content-pipeline
PROSE_HINT = re.compile(r"(?i)\bcontent[\s_-]pipeline\b")


def classify(text: str, needle: str) -> tuple[bool, bool]:
    """Return (frontmatter_match, inline_hash_match). Prose is checked separately."""
    nlow = needle.lower()
    fm = bool(
        any(nlow == t.strip().strip('"').strip("'").lower()
            for t in FRONTMATTER_ARRAY.search(text and "".join(__import__("re").findall(r".{0,2000}", text)) or "").group(1).split(",") if t.strip())
    ) if FRONTMATTER_ARRAY.search(text) else False
    # Cleaner: extract array contents into a list, compare case-insensitively
    fm = False
    m = FRONTMATTER_ARRAY.search(text)
    if m:
        items = [s.strip().strip('"').strip("'").lower() for s in m.group(1).split(",")]
        if any(it == nlow for it in items if it):
            fm = True
    m = FRONTMATTER_BLOCK.search(text)
    if m:
        items = re.findall(r"-\s*([^\n]+)", m.group(1))
        if any(s.strip().strip('"').strip("'").lower() == nlow for s in items):
            fm = True
    inline = any(
        t.lower() == nlow
        for t in INLINE_TAG.findall(text)
    )
    return fm, inline


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: python find-tag.py <vault_path> <tag>", file=sys.stderr)
        return 2
    vault = Path(sys.argv[1])
    tag = sys.argv[2].lstrip("#")

    if not vault.exists():
        print(f"Vault not found: {vault}", file=sys.stderr)
        return 2

    md_files = [p for p in vault.rglob("*.md") if "graphify-out" not in p.parts and is_probably_text(p)]
    print(f"Scanning {len(md_files)} markdown files under {vault}")

    real_tagged: list[tuple[Path, bool, bool]] = []   # path, fm, inline
    prose_only: list[Path] = []

    for p in md_files:
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if tag.lower() not in text.lower() and tag not in text:
            continue
        fm, inline = classify(text, tag)
        prose = bool(PROSE_HINT.search(text))
        if fm or inline:
            real_tagged.append((p, fm, inline))
        elif prose:
            prose_only.append(p)

    print()
    if real_tagged:
        print(f"=== REAL TAGS ({len(real_tagged)}) ===")
        for p, fm, inline in real_tagged:
            kinds = []
            if fm: kinds.append("frontmatter")
            if inline: kinds.append("inline #tag")
            rel = p.relative_to(vault)
            print(f"  {rel}   [{', '.join(kinds)}]")
    else:
        print("=== REAL TAGS: none ===")

    print()
    if prose_only:
        print(f"=== PROSE ONLY (string appears, NOT tagged) ({len(prose_only)}) ===")
        for p in prose_only:
            rel = p.relative_to(vault)
            print(f"  {rel}")
    else:
        print("=== PROSE ONLY: none ===")

    print()
    print(f"Real tag count: {len(real_tagged)} | Prose-only count: {len(prose_only)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
