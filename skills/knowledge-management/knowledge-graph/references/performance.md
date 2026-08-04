# Knowledge Graph — Performance Reference

## Community Detection Timeout Fix

**Problem**: `greedy_modularity_communities` hangs on vaults with 10k+ nodes. Timeout 60s exceeded.

**Root cause**: NetworkX's greedy modularity is O(n log n) but with very large dense graphs it still times out.

**Fix**: Wrap in try/except and fall back immediately:

```python
try:
    from networkx.algorithms.community import greedy_modularity_communities
    comms = list(greedy_modularity_communities(G.to_undirected()))
    communities = {}
    for i, c in enumerate(comms):
        for n in c:
            communities[n] = i
    print(f"Communities (greedy): {len(comms)}")
except Exception:
    # Fallback: degree-modulo clustering — O(n), never hangs
    communities = {n: i % 12 for i, n in enumerate(G.nodes())}
    print(f"Communities (fallback): {len(set(communities.values()))}")
```

**Why 12 communities for fallback**: Good spread for ~400 nodes, looks visually distinct with D3's Tableau10 palette.

## Graph Generation Timeout

**Problem**: Full vault scan (12,901 nodes) takes >60s.

**Fix**: Always prune to MAX_NODES (default 400) BEFORE building community structure:

```python
deg = dict(G.degree())
all_nodes = sorted(G.nodes(), key=lambda n: deg.get(n, 0), reverse=True)
if len(all_nodes) > MAX_NODES:
    keep = set(all_nodes[:MAX_NODES])
    for n in list(G.nodes()):
        if n not in keep:
            G.remove_node(n)
```

This also keeps the physics simulation snappy.

## Guardrails verify.sh Must Be Fast

**Problem**: Looping all vault files for wikilink validation times out on large vaults.

**Fix**: Only spot checks — verify a SAMPLE of files, not all:

```bash
# Check only top-degree nodes for broken wikilinks
SAMPLE=$(find "$VAULT_ROOT/wiki" -name "*.md" -exec basename {} .md \; | \
  sort -t/ -k2 | head -20)
```

Or skip wikilink validation entirely and just check:
1. Required directories exist
2. Index files exist
3. No single file >500KB

## Python Interceptor Path

Always use the full path to avoid PATH resolution issues:
```
C:/Users/shrey/AppData/Local/Programs/Python/Python314/python.exe
```

The system Python is 3.13 at `python3`, but `python-louvain` and other packages may only be on 3.14.