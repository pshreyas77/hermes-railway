#!/usr/bin/env python3
"""
vault-only-nodes.py — filter a graph.json to vault-author-note nodes only.

PROBLEM
-------
On the Obsidian vault at E:\\_Knowledge\\ObsidianVault, the graph.json contains
~50k nodes spanning both user-authored vault notes AND AST-extracted symbols
from embedded vendor repos (GitNexus/, tolaria/, ruflo/, InfiniteBrain/,
consciousness-symphony/, genericagent/, copilot/, .smart-env/, _keys/,
node_modules/, ...). When `graphify query "<English topic>"` runs BFS against
this graph, code symbols dominate the result set (every code repo has
identifiers like `extractParty`, `Movement`, `Language`, `Transcendence`) and
the actual vault topical notes never surface.

This script materialises a stripped-down graph containing only the nodes whose
filesystem path is a vault-note path, so subsequent `graphify query --graph`
calls return topical content.

USAGE
-----
    python /home/hermes/graphify/scripts/vault-only-nodes.py \
        --graph /vault/graphify-out/graph.json \
        --out   /vault/graphify-out/graph-vault-only.json

Optional flags:
    --vault-root PATH    override vault root (default: /vault)
    --keep-prefixes P,P  comma-separated extra path prefixes to KEEP
                         (default: wiki, Research, 02 - AREAS, 03 - PROJECTS,
                          04 - DAILY, 05 - MAPS, 06 - OUTPUTS, 07 - SYSTEM,
                          00 - INBOX, 0-raw, BRIEFINGS, Copies, Attachments)
    --drop-prefixes P,P  comma-separated extra path prefixes to DROP
                         (default: tolaria, ruflo, GitNexus, InfiniteBrain,
                          consciousness-symphony, genericagent, copilot,
                          .smart-env, _keys, node_modules, .git)

VAULT TOPOLOGY (verified 2026-07-25)
------------------------------------
Top-level dirs that ARE vault content:
    wiki/                 — concept / entity notes
    Research/             — research notes (Deep/, India/, Genetics/, Articles/, ...)
    02 - AREAS/           — topical MOCs (Ancient Civilizations, Political Analysis, ...)
    03 - PROJECTS/        — project hubs (Dravidian-Lineage-Graph, etc.)
    04 - DAILY/           — daily notes (2026-07-XX.md, CJP-LIVE-UPDATES.md)
    05 - MAPS/            — top-level MOCs (Indian Political History MOC,
                            Historical Linguistics MOC, ...)
    06 - OUTPUTS/         — produced artifacts (HTML graphs, etc.)
    07 - SYSTEM/          — system notes (audit-dashboard, etc.)
    00 - INBOX/           — intake for night-shift pipeline
    0-raw/                — raw captures
    BRIEFINGS/            — morning briefs
    Copies/, Attachments/ — supporting media

Top-level dirs that are EMBEDDED CODE (drop):
    tolaria/, ruflo/, GitNexus/, InfiniteBrain/, consciousness-symphony/,
    genericagent/, copilot/, .smart-env/, _keys/, node_modules/,
    .git/, .obsidian/, .venv/, dist/, build/, out/

OUTPUT FORMAT
-------------
Writes a JSON file with the same schema as graph.json, but with:
    nodes[] — filtered to vault-only entries
    edges[] — every edge where BOTH endpoints survive the filter
    metadata — original counts + filtered counts + drop reasons

If filtering cuts the node count by >90%, the script prints a loud warning —
that usually means a prefix typo or a new project was embedded in the vault
without being added to the deny-list.

REPRODUCIBILITY NOTE
--------------------
The 2026-07-25 cron-generated daily briefing hit the code-symbol-noise bug
3 times (each `graphify query` for CJP / Dravidian / JK elections returned
vendor-repo AST symbols). Falling back to `find . -mtime -7` + raw
`read_file` on Research/India/, wiki/concepts/, 04 - DAILY/, 05 - MAPS/
produced the actual briefing. This script is the durable fix so the next
cron run doesn't repeat the same 3 wasted calls.

Run this script as part of the vault-maintenance cron (or before any
`graphify query` against the vault graph for a topic question), then point
the query at the filtered output:
    --graph graph-vault-only.json
"""

import argparse
import json
import os
import sys
from pathlib import Path


# --- Default prefix lists (verified against the live vault on 2026-07-25) ---
DEFAULT_VAULT_PREFIXES = [
    "wiki",
    "Research",
    "02 - AREAS",
    "03 - PROJECTS",
    "04 - DAILY",
    "05 - MAPS",
    "06 - OUTPUTS",
    "07 - SYSTEM",
    "00 - INBOX",
    "0-raw",
    "BRIEFINGS",
    "Copies",
    "Attachments",
    "Clippings",
    "Sources",
    "_Knowledge",
    "1-desk",
    "2-atoms",
    "3-threads",
    "sources",
    "atoms",
    "_COMMUNITY_",
    "AGENTS.md",
    "README.md",
    "graphify-out",
]

DEFAULT_DROP_PREFIXES = [
    "tolaria",
    "ruflo",
    "GitNexus",
    "InfiniteBrain",
    "consciousness-symphony",
    "genericagent",
    "copilot",
    ".smart-env",
    "_keys",
    "node_modules",
    ".git",
    ".obsidian",
    ".venv",
    "venv",
    "dist",
    "build",
    "out",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
]

# File-extension drops (vendor build artifacts that sometimes slip in)
DROP_EXTENSIONS = {
    ".pyc", ".so", ".dll", ".exe", ".o", ".a", ".class",
    ".map", ".tsbuildinfo",
}


def parse_prefix_list(raw: str | None, default: list[str]) -> list[str]:
    if not raw:
        return list(default)
    return [p.strip() for p in raw.split(",") if p.strip()]


def classify_path(rel_path: str, vault_prefixes: list[str], drop_prefixes: list[str]) -> tuple[bool, str]:
    """Return (keep, reason). keep=True => node stays in filtered graph."""
    p = rel_path.replace("\\", "/").lstrip("/")
    first = p.split("/", 1)[0] if "/" in p else p

    for drop in drop_prefixes:
        if first == drop or p.startswith(drop + "/") or first.startswith(drop):
            return False, f"drop-prefix:{drop}"

    for ext in DROP_EXTENSIONS:
        if p.endswith(ext):
            return False, f"drop-ext:{ext}"

    for keep in vault_prefixes:
        if first == keep or p.startswith(keep + "/") or p.startswith(keep):
            return True, f"keep-prefix:{keep}"

    # Default: keep anything whose top-level matches a known vault dir,
    # else conservative-default to drop but log it.
    return False, f"unknown-prefix:{first!r}"


def filter_graph(graph_path: Path, out_path: Path, vault_root: Path, vault_prefixes: list[str], drop_prefixes: list[str]):
    with graph_path.open("r", encoding="utf-8") as f:
        graph = json.load(f)

    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])

    node_index = {n.get("id"): n for n in nodes}

    keep_nodes = []
    drop_reasons: dict[str, int] = {}
    for n in nodes:
        src = n.get("source_file") or n.get("src") or n.get("path") or ""
        # Some graphs store src as "repo/path/file.py:L123" — strip line locators
        if ":" in src and src.split(":")[0].endswith((".py", ".js", ".ts", ".md", ".txt")):
            src = src.split(":")[0]
        # Make path relative to vault root if absolute
        try:
            rel = str(Path(src).resolve().relative_to(vault_root.resolve()))
        except (ValueError, OSError):
            rel = src

        keep, reason = classify_path(rel, vault_prefixes, drop_prefixes)
        if keep:
            keep_nodes.append(n)
        else:
            drop_reasons[reason] = drop_reasons.get(reason, 0) + 1

    keep_ids = {n["id"] for n in keep_nodes if "id" in n}
    keep_edges = [e for e in edges if e.get("source") in keep_ids and e.get("target") in keep_ids]

    out_graph = {
        "nodes": keep_nodes,
        "edges": keep_edges,
        "metadata": {
            "filtered_from": str(graph_path),
            "vault_root": str(vault_root),
            "original_nodes": len(nodes),
            "original_edges": len(edges),
            "kept_nodes": len(keep_nodes),
            "kept_edges": len(keep_edges),
            "drop_reasons": drop_reasons,
            "vault_prefixes": vault_prefixes,
            "drop_prefixes": drop_prefixes,
        },
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(out_graph, f, indent=2, ensure_ascii=False)

    return out_graph["metadata"]


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Filter a graph.json to vault-author-note nodes only.")
    parser.add_argument("--graph", required=True, help="path to graph.json (input)")
    parser.add_argument("--out", required=True, help="path to write filtered graph.json")
    parser.add_argument("--vault-root", default="/vault",
                        help="vault root for path-relativization (default: /vault)")
    parser.add_argument("--keep-prefixes", default=None, help="comma-separated overrides for keep-list")
    parser.add_argument("--drop-prefixes", default=None, help="comma-separated overrides for drop-list")
    args = parser.parse_args(argv)

    graph_path = Path(args.graph)
    out_path = Path(args.out)
    vault_root = Path(args.vault_root)

    if not graph_path.exists():
        print(f"ERROR: graph not found: {graph_path}", file=sys.stderr)
        return 2
    if not vault_root.exists():
        print(f"ERROR: vault root not found: {vault_root}", file=sys.stderr)
        return 2

    keep_prefixes = parse_prefix_list(args.keep_prefixes, DEFAULT_VAULT_PREFIXES)
    drop_prefixes = parse_prefix_list(args.drop_prefixes, DEFAULT_DROP_PREFIXES)

    meta = filter_graph(graph_path, out_path, vault_root, keep_prefixes, drop_prefixes)

    print(f"Wrote {meta['kept_nodes']} nodes ({meta['original_nodes']} original) "
          f"+ {meta['kept_edges']} edges ({meta['original_edges']} original) → {out_path}")

    kept_pct = (meta['kept_nodes'] / meta['original_nodes'] * 100) if meta['original_nodes'] else 0
    print(f"  Kept: {kept_pct:.1f}% of original nodes")

    if kept_pct < 10:
        print()
        print("WARNING: filtered graph retained <10% of nodes.")
        print("Likely causes:")
        print("  1. A new vendor repo was embedded in the vault without being added to DROP.")
        print("  2. A typo in --keep-prefixes or --drop-prefixes.")
        print("  3. Vault root mismatch between this script and graph.json's source paths.")
        return 1

    print()
    print("Drop reasons:")
    for reason, count in sorted(meta["drop_reasons"].items(), key=lambda kv: -kv[1]):
        print(f"  {count:>6}  {reason}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
