# GitHub Repo → Second Brain (Verified Recipe)

> **Status:** Verified end-to-end on `rahulnyk/knowledge_graph` (2026-07-26,
> 22 files → 1,968 MemPalace drawers → 20-node graphify graph + wikilinked
> vault note). Total wall time ≈ 25 minutes, dominated by mining and LLM
> extraction steps.

When the user asks any variant of "wire X repository into my second brain"
(`/obsidian /mempalace … do it with my second brain`, "mine this repo",
"add it to the brain", etc.), this 5-step pipeline is the consolidated pattern.

---

## Step 1 — Clone to E:

All installs/clones/source code/data → `E:` drive. Never `C:`.

```bash
cd "/home/hermes" && git clone --depth=1 https://github.com/<owner>/<repo>.git
```

**Alternative (canonical graphify cache):** `graphify clone <url>` lands the
repo at `C:/Users/shrey/.graphify/repos/<owner>/<repo>/` — same location the
graphify tool uses internally. Pick this if you want the graphify step
auto-discoverable.

```bash
graphify clone https://github.com/<owner>/<repo>.git
# → Ready at: C:/Users/shrey/.graphify/repos/<owner>/<repo>
```

**Pitfall — `--depth=1`:** clones are shallow by default. The repo will not
have full git history. Acceptable for "wire into second brain" use cases
where you only need the working tree. Re-clone without `--depth=1` if you
need the full history.

---

## Step 2 — Entity registration

Append to `/vault/entities.json`:

```json
{
  "people": [..., "Rahul Nayak"],
  "projects": [..., "knowledge_graph"]
}
```

Pick a stable `projects[]` slug (kebab-case, ≤32 chars). Same slug will
become the MemPalace wing name in step 3 and the wikilink slug in step 5.

**Why:** MemPalace reads `entities.json` to disambiguate people/projects
during hallway graph construction. Without an entity entry, hallways
won't link the project's drawers to its author/vault references.

---

## Step 3 — Mine into MemPalace

```bash
cd "/home/hermes/mempalace" && \
    ./mp.sh mine "/home/hermes/<repo>" --wing <short-name>
```

**CLI shape (verified Jul-2026):**
- Positional `dir` (path to corpus)
- `--wing NAME` — defaults to the dir's basename
- These flags DO NOT exist: `--folder`, `--room`, `--path`
- `--dry-run` to preview drawer counts before filing

**Dry run first if uncertain:**

```bash
./mp.sh mine "/home/hermes/<repo>" --wing <short-name> --dry-run
# Look for "Files processed" + "Drawers filed" + acceptable skip count
```

**Heads-up — large mines (>500 files) likely background-time out:**
Foreground `terminal` maxes out at ~600 s. Large/mini mines (notebooks +
CSV outputs > 1k files) need `background=true` + `notify_on_complete=true`.

```bash
# Example — the 22-file knowledge_graph mine took ~20 min, foreground-OK at 600s.
# A 1000+ file mine would need the background pattern.
```

**Heads-up — HNSW BM25-only notice:** a successful mine can surface
`NOTICE: vector search disabled — HNSW index has diverged from SQLite.`
The mine still worked (data is in `chroma.sqlite3`); only the vector index
needs rebuilding. See [`repair-and-healthcheck.md`](repair-and-healthcheck.md).
Don't redo the mine.

---

## Step 4 — Graphify the repo itself

```bash
# A — if you cloned to the canonical cache dir in step 1:
cd "C:/Users/shrey/.graphify/repos/<owner>/<repo>" && graphify update .

# B — if you cloned to /home/hermes/<repo> in step 1:
cd "/home/hermes/<repo>" && graphify update .
```

**Critical — bare `graphify <path>` FAILS:**

```
$ graphify "/home/hermes/knowledge_graph"
error: unknown command '/home/hermes/knowledge_graph'
```

The CLI does NOT accept a path arg at the top level. Always `cd` into the
target dir first, then run `graphify update .`

**Output:** `graph.json`, `graph.html` (interactive viz), `GRAPH_REPORT.md`
in `graphify-out/`. Small repos (~22 files like repository_graph) yield
~20 nodes / 19 edges / 3 communities.

**Verify by reading the report:**

```bash
head -60 <repo>/graphify-out/GRAPH_REPORT.md
# Look for: Summary (node/edge/community counts), God Nodes,
# Surprising Connections
```

---

## Step 5 — Wikilinked vault note

Write to `/vault/wiki/<short-name>.md` with:

```markdown
---
tags:
  - <domain>
  - second-brain-source
source: <repo URL>
author: <author>
license: <SPDX id>
stars: <count>
forks: <count>
cloned: <YYYY-MM-DD>
cloned-path: /home/hermes/<repo>
---

# <short-name>

> *"<repo tagline from README.md>"*

[Brief paragraph on what the repo does and why it overlaps with the user's
existing stack.]

## Why it matters here (shrey's second brain)

[Table mapping repo pieces → user's existing tools]

## The pipeline (verbatim from README)

[Numbered steps from README, 1..6]

## Key files to read

| File | Why |
|---|---|
| ... | ... |

## Stack (from pyproject.toml)

[toml excerpt]

## How to mine/graphify/observe

[Bash code block with verified commands from this recipe]

## Sources

- Repo: <URL> — verified live on <DATE>
- Local clone: `/home/hermes/<repo>/`
```

**Tags to consider:** `second-brain-source`, the topic domain
(`knowledge-graph`, `graphrag`, `ollama`, etc.), and any `graphify-relative`
markers if the repo overlaps with the user's in-house tooling.

**Wikilinks to the user's stack:** when the repo overlaps with in-house
tools, link them with `[[wikilink]]` syntax — `[[graphify]]`,
`[[mempalace]]`, `[[local-ai-operating-system]]`, etc.

---

## Verification checklist (run before reporting success)

| # | Check | Pass criterion |
|---|---|---|
| 1 | MemPalace drawer count grew | `./mp.sh status` shows new wing OR +~drawer-count delta on existing wing |
| 2 | Graphify output exists | `ls <repo>/graphify-out/{graph.json,graph.html,GRAPH_REPORT.md}` → all three |
| 3 | Vault note reachable | `search_files pattern=<short-name>.md path=/vault/wiki` returns ≥1 |
| 4 | Search actually returns | `./mp.sh search "<known phrase from corpus>"` returns ≥1 result (BM25 is fine) |
| 5 | Entity registered | `cat entities.json | jq '.projects' | grep <short-name>` matches |

If 1, 2, and 4 fail simultaneously, suspect the HNSW divergence pitfall —
the mine & graphify probably completed but the vector index needs
rebuilding. See the warning in Step 3.

---

## Variations

**Larger corpus:** if `git clone` produces > 100 files, the mine step will
likely time out in foreground. Switch to `terminal(background=true,
notify_on_complete=true)` for step 3.

**PDF-heavy repo:** this pipeline already handles PDFs because MemPalace
auto-extracts them (per the Jul-2026 `mempalace mine --mode extract`).
Graphify on PDFs requires explicit `--update` from inside the AI assistant
(pitfall: the cron-only `update` is code-AST only).

**Private repo:** requires auth. Set `GITHUB_TOKEN` per the
`github-auth` skill; `git clone https://x-access-token:$GITHUB_TOKEN@github.com/<owner>/<repo>.git`.
All other steps are auth-agnostic.

**Multiple repos in one batch:** run steps 1-4 sequentially per repo.
Output for all of them is independent; can be batched in a single
todo plan. Step 5 (vault note) per repo.

---

## Session notes — `rahulnyk/knowledge_graph` (2026-07-26)

This was the session this recipe was verified in. Key results:

| Metric | Value |
|---|---|
| Repo size | 49 MB, 22 source files |
| MemPalace before / after | 6,026 / 7,994 drawers (+1,968) |
| MemPalace wing | new: `knowledge_graph` |
| Graphify output | 20 nodes, 19 edges, 3 communities |
| God nodes | `df2ConceptsList`, `df2Graph`, `extractConcepts`, `graphPrompt` |
| Star / fork count | 3,463 / 549 (verified via GitHub API) |
| Total wall time | ~25 minutes |
| Foreground timeout? | No, but mining hit ~20 min — could have used background |

`GRAPH_REPORT.md` is at `C:/Users/shrey/.graphify/repos/rahulnyk/knowledge_graph/graphify-out/`.
Vault note is at `/vault/wiki/knowledge_graph_repo.md`.
