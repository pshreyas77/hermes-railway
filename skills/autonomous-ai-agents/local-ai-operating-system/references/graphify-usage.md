# Graphify Usage Patterns

## Binary Location
```
C:/Users/shrey/AppData/Local/Programs/Python/Python314/Scripts/graphify
```

## Graph Stats (Current)
- **Nodes**: 50,137
- **Edges**: 97,449
- **Communities**: 3,910
- **Generated**: 2026-07-18

## Core Commands

### Query (BFS - Broad Context)
```bash
graphify query "Justice Party 1937 election results"
graphify query "Dravidian movement open questions" --mode bfs --budget 2000
graphify query "Periyar USSR 1932 influence" --budget 1500
```

### Query (DFS - Deep Path)
```bash
graphify query "How did G.O. 3136 influence post-independence reservation?" --mode dfs
graphify query "Trace Periyar's ideological evolution" --mode dfs --budget 2000
```

### Path Finding
```bash
graphify path "Justice Party" "DMK"
graphify path "Periyar" "Ambedkar"
graphify path "Communal G.O. 3136" "First Amendment"
graphify path "C. Natesa Mudaliar" "Self-Respect Movement"
```

### Explain Concept
```bash
graphify explain "Communal G.O. 3136"
graphify explain "Self-Respect Marriage"
graphify explain "Dravida Nadu"
graphify explain "Suyamariyathai"
```

### Update Graph (Incremental - AST Only, No API Cost)
```bash
graphify update E:/_Knowledge/ObsidianVault
```

### Full Rebuild (With Semantic Extraction - Needs MOONSHOT_API_KEY)
```bash
graphify extract E:/_Knowledge/ObsidianVault --mode deep
```

### God Nodes (Top Connected)
```bash
graphify query "god nodes" --budget 500
# Or read from GRAPH_REPORT.md
```

## Query Patterns for Research

### Political History
```bash
# Justice Party specifics
graphify query "Justice Party 1937 election defeat causes"
graphify query "Periyar 1938 Justice Party presidency"
graphify query "1944 Salem Conference Dravidar Kazhagam formation"
graphify query "1949 DMK split Annadurai Periyar"

# Reservation jurisprudence
graphify query "Communal G.O. 3136 implementation 1921-1937"
graphify query "Champakam Dorairajan 1951 Supreme Court"
graphify query "First Amendment Article 15(4) reservation"
graphify query "Mandal Commission 1990 implementation"

# Dravidian movement
graphify query "Self-Respect Movement 1925 founding"
graphify query "Anti-Hindi agitations 1937 1965"
graphify query "Dravida Nadu demand evolution"
```

### Language Families
```bash
graphify query "Dravidian language family branches South I South II Central North"
graphify query "Indo-Aryan migration timeline 3500 years ago"
graphify query "Sino-Tibetan NE India languages Bodo Garo Mizo"
graphify query "Austroasiatic Khasi Mundari Santali India"
```

### Comparative Analysis
```bash
# Cross-concept connections
graphify path "Communal G.O. 3136" "First Amendment"
graphify path "Self-Respect Movement" "Navayana Buddhism"
graphify path "Periyar" "Ambedkar"
graphify path "Justice Party" "AIADMK"

# God nodes for hub concepts
graphify query "god nodes" --budget 300
```

## Output Interpretation

### BFS Query Result Structure
```
Traversal: BFS depth=2 | Start: [extractParty()] | 35 nodes found

NODE: Justice Party (entity)
NODE: Periyar E. V. Ramasamy (entity)
EDGE: Justice Party --transformed_by [INFERRED 0.85]--> Dravidar Kazhagam
EDGE: Periyar E. V. Ramasamy --led [EXTRACTED 1.0]--> Self-Respect Movement
```

### Path Result Structure
```
Shortest path: Justice Party → Dravidar Kazhagam → DMK
Length: 3 edges
Communities crossed: 2
```

### Explain Output
```
Communal G.O. 3136 (1921): First statutory caste-based reservation in India.
Issued by Justice Party government in Madras Presidency.
Reserved seats for non-Brahmins in local bodies and education.
Precursor to Article 15(4) and post-independence reservation policy.
```

## Best Practices

1. **Always use BFS first** for broad context, then DFS for deep dives
2. **Budget 1500-2000 tokens** for complex historical queries
3. **Use path finding** for causal/ideological chains
3. **Update after major vault changes** - `graphify update` is fast (AST only)
4. **Read GRAPH_REPORT.md** for god nodes and community structure
4. **Use `--budget`** to control token costs

## Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| "Graph not built" | No graph.json | Run `graphify update <vault>` |
| Timeout | Budget too high | Lower `--budget` to 500-1000 |
| Empty results | Concept not in graph | Check spelling, try synonyms |
| Path not found | Concepts in different components | Try broader concepts |

## Integration with Hermes

In Hermes session:
```
/graph "Justice Party 1937 election"
/path "Justice Party" "DMK"
/explain "Communal G.O. 3136"
```

Or via MCP (when connected):
```python
await mcp.call_tool("graphify", "query", {"question": "Justice Party 1937", "budget": 1000})
```