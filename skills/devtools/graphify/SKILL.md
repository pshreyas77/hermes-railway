---
name: graphify
description: "any input (code, docs, papers, images, videos) to knowledge graph. Use when user asks any question about a codebase, documents, or project content - especially if graphify-out/ exists, treat the question as a /graphify query."
trigger: /graphify
---

# /graphify

Turn any folder of files into a navigable knowledge graph with community detection, an honest audit trail (EXTRACTED/INFERRED/AMBIGUOUS), and three outputs: interactive HTML, GraphRAG-ready JSON, and a plain-language GRAPH_REPORT.md.

**User rule: ALL work on E: drive. Source is at `E:/_Dev_Tools/graphify/` — never use C: for installs.**

**Windows cache redirect:** All tool caches redirected to E: — `UV_CACHE_DIR=E:/.uv-cache`, `PIP_CACHE_DIR=E:/.pip-cache`, `TMP=E:/.tmp`, `TEMP=E:/.tmp`. Set in `~/.bashrc` (auto-loaded via `auto_source_bashrc: true`) and via Windows `setx` for system-wide persistence. See `E:/_Dev_Tools/graphify/references/cache-redirect-setup.md` for the full setup (created 2026-07-20).

## Vault-specific context

| | |
|---|---|
| Vault graph | `E:/_Knowledge/ObsidianVault/graphify-out/` |
| Graph stats | 50,137 nodes, 97,449 edges, 3,889 communities (Jul-24 regen ran community detection over 9,236 files / 16.7M words) |
| Generated | 2026-07-24 (commit `ee85bbfb`) — previous regeneration: 2026-07-18 |
- `references/vault-research-pipeline.md` — PDF reading (pymupdf on Python 3.14), research note template, evidence grading, linking pattern
- `references/cjp-live-monitor.md` — cron-based live news monitor: Python scraping script → vault file. JSON-LD extraction (NOT h2/h3 regex) for Hindustan Times. Scroll.in as best live-updating source. User said NO Telegram delivery — use `deliver='local'`.
- `references/obsidian-canvas-generation.md` — programmatic `.canvas` building, slug cover matching, case-insensitive genre classification
- `references/mempalace-venv.md` — bare `mempalace` on PATH uses Python 3.14 and crashes on numpy ABI; use `cd E:/_Dev_Tools/mempalace && python -m mempalace …`
| CLI binary | `C:/Users/shrey/AppData/Local/Programs/Python/Python314/Scripts/graphify` |
| Source | `E:/_Dev_Tools/graphify/` |

**Support scripts in this skill's `scripts/` directory** (keyed by the pitfall they fix):
- `scripts/find-tag.py` — vault-wide tag search that distinguishes real tags from prose mentions
- `scripts/scan-broken-links.py` — wiki-link audit + orphan detection
- `scripts/vault-only-nodes.py` — strips vendor-repo code symbols out of `graph.json` so `graphify query` on topical questions returns vault notes, not AST neighbours (added 2026-07-25 after the daily-briefing cron hit code-symbol noise 3x)

## Obsidian Vault Integration (Added 2026-07-18)

The vault at `E:/_Knowledge/ObsidianVault` has been indexed with graphify. The graph includes:
- Markdown notes (wiki, research, daily logs)
- Code files (Python, TypeScript, etc.)
- Community detection reveals 3,910 clusters
- God nodes in GRAPH_REPORT.md identify central concepts

**Key vault paths:**
- Graph output: `E:/_Knowledge/ObsidianVault/graphify-out/graph.json` + `GRAPH_REPORT.md`
- Wiki notes: `E:/_Knowledge/ObsidianVault/wiki/`
- Research: `E:/_Knowledge/ObsidianVault/Research/`
- Daily logs: `E:/_Knowledge/ObsidianVault/04 - DAILY/`
- MOCs: `E:/_Knowledge/ObsidianVault/05 - MAPS/`

**AGENTS.md rules created:** `E:/_Knowledge/ObsidianVault/AGENTS.md` contains graphify usage rules (read GRAPH_REPORT.md first, prefer graphify query over grep).

### What Actually Works for CJP News
```python
sources = [
    ("Scroll", "https://scroll.in/latest"),
    ("Hindustan Times", "https://www.hindustantimes.com/india-news/"),
    ("The Hindu", "https://www.thehindu.com/news/national/"),
    ("Indian Express", "https://indianexpress.com/section/india/"),
    ("Al Jazeera", "https://www.aljazeera.com/news/2026/youth-led-protesters-answer-call..."),
    ("CJP Official Site", "https://cockroachjantaparty.raizian.in/"),
    ("CJP Protest Schedule", "https://cockroachjantaparty.raizian.in/protest-schedule"),
]
```

## CJP Social Media Discovery (2026-07-21 — Real Handles Found)

| Platform | Handle | URL |
|----------|--------|-----|
| X/Twitter | **@Cockroachisback** | (not @CockroachParty) |
| Telegram | **@thecockroachchannel** | t.me/thecockroachchannel |
| WhatsApp | CJP Official Updates | (via cockroachjantaparty.raizian.in) |
| Instagram | @cockroachjantaparty | |
| Facebook | Cockroach Janta Party | |

Nitter/Twitter mirrors ALL failed: poast.org (403), privacydev.net (DNS fail), cz (cert expired).

## Crowd-Size Verification Workflow (2026-07-21)

When user asks "how many protesters?" or surfaces a claim like "1 lakh+":

1. **Bracketed estimate, never a single number** — provide RANGE (low/high) from multiple sources
2. **Identify the SOURCE** — organizer self-report vs. independent media vs. police vs. eyewitness
3. **Apply plausibility filter:**
   - Jantar Mantar physical capacity: ~10K–15K max (seated + standing combined)
   - Metro cordons + barricades cap crowd regardless of claims
   - Wire services (Reuters/AP/AFP) lead with crowd numbers — if they didn't say "X lakh", they didn't verify it
4. **Distinguish organizational stats from attendance** — "20 lakh registered members" ≠ "20 lakh at one march"; "22M Instagram followers" ≠ "22M at protest"
5. **Contradict unverified claims directly but respectfully** — "I couldn't verify X; here's what multiple sources confirm; please share the source if you have one"

**Wrong:** Accept "1 lakh" and cite it (unverified).
**Right:** "I found 10K-20K in Delhi confirmed by Reuters, HT, NDTV, Delhi Police. I could not verify the '1 lakh' claim — no non-godi source cites it, and it likely conflates CJP's 20-lakh registered member base with march attendance."

**Confirmed crowd data (July 20, 2026 — Delhi):**
| Source | Estimate |
|--------|-----------|
| Reuters / AP | 10,000+ |
| Hindustan Times | 10,000–20,000 |
| Delhi Police (via HT) | 10,000 |
| NDTV | 20,000 |
| Scroll.in | "thousands" |
| Al Jazeera | "thousands" |

```
/graphify                           # full pipeline on current dir
/graphify <path>                    # full pipeline on path
/graphify <path> --update           # incremental re-extract (AST-only, no API cost)
/graphify query "<question>"        # BFS traversal query
/graphify path "A" "B"              # shortest path A→B
/graphify explain "<concept>"       # plain-language explain
/graphify <path> --watch             # watch folder, auto-rebuild on code changes
```

## Title-based classification fallback

Books with empty genres need title-keyword matching. Also: classify banned titles BEFORE fiction, and check consciousness before psychology (since "psychology" appears in some consciousness genres).

```python
BANNED_TITLES = {"1984","brave new world","naked lunch","lolita",...}
CONSCIOUSNESS_TITLES = {"consciousness explained","gödel, escher, bach","meditations",...}
INTROVERT_TITLES = {"quiet","introvert power","solo",...}

# Order matters:
if any(t in title_lower for t in BANNED_TITLES):       return "Banned"
elif any(t in title_lower for t in CONSCIOUSNESS_TITLES): return "Consciousness"
elif any(t in title_lower for t in INTROVERT_TITLES):  return "Introvert"
elif "psychology" in all_text:                          return "Psychology"
elif any(k in all_text for k in ["fiction","novel",...]): return "Fiction & Philosophy"
elif title_lower in TITLE_FALLBACK_MAP:                return TITLE_FALLBACK_MAP[title_lower]
else:                                                   return "General"
```

**Books needing title-based fallback** (empty genre + ambiguous tags):
- Beyond Good and Evil → Fiction & Philosophy (Nietzsche)
- Heart of Darkness → Fiction & Philosophy (Conrad)
- Predictably Irrational → Psychology (Ariely)
- The Catcher in the Rye → Fiction & Philosophy (Salinger)
- The Stranger → Fiction & Philosophy (Camus)

## Workflow

Always `cd` to the vault before running graphify commands. Do NOT run from `C:\Users\shrey\` — that creates AGENTS.md pollution on C:.

After modifying code files, run `graphify update E:/_Knowledge/ObsidianVault` to keep the graph current.

**Pitfall — `graphify update` is code-only:** the `--update` / `update` subcommand re-extracts **code files only** (AST, no LLM calls). Markdown notes, PDFs, and images are NOT picked up. If the vault had doc/paper/image changes, run a full `/graphify --update` from the assistant, or the graph will silently stay stale on those surfaces. The cron job that runs `graphify update` only refreshes the code slice.

Before answering architecture/codebase questions, read `graphify-out/GRAPH_REPORT.md` for god nodes and community structure.

**Pitfall — `graph.html` skipped on large vaults:** with >5,000 nodes, Graphify prints `[graphify watch] Skipped graph.html: Graph has N nodes - too large for HTML viz` and refuses to emit the interactive viz. This is expected, not an error. Override with `GRAPHIFY_VIZ_NODE_LIMIT=...`, `--no-viz`, or by reducing input scope.

## execute_code Workaround

`execute_code` is blocked for arbitrary Python scripts that write output files (canvas generation, data processing, etc.). When you need to run a multi-step Python script that produces a file:

1. Write the script to `E:/_Dev_Tools/graphify/<descriptive-name>.py` using `write_file`
2. Run it via `terminal`: `cd E:/_Dev_Tools/graphify && python <descriptive-name>.py`
3. Verify output with targeted `terminal` commands, not execute_code

This pattern was used for:
- books-flashcards.canvas generation (55-book canvas with HTML cards, genre classification, local cover matching)
- CJP live protest monitor (news scraper → vault daily note, runs every 15 min via cron)

## Dead Community Links in GRAPH_REPORT.md (Pitfall + Fix)

Graphify generates a "Community Hubs (Navigation)" section at the top of GRAPH_REPORT.md with 2,500+ wiki-links like `[[_COMMUNITY_Community N|Community N]]`. These links point to **separate .md files** that **Graphify never generates** — the community details are embedded inline in the same report file. All wiki-links are dead.

**Symptoms:** Clicking any community link in Obsidian opens a blank/dead page. User will say "community links are empty," "many community links are empty please check and fix it," or paste an `obsidian://open?vault=...&file=graphify-out%2FGRAPH_REPORT` deep-link. The deep-link is a strong signal: the user is *already inside* the broken file, so the fix must touch GRAPH_REPORT.md directly, not the script that generated it.

**One-page fix script** lives at `E:/_Dev_Tools/graphify/scripts/fix-community-links.py` and is idempotent. It:
1. Locates the `## Community Hubs (Navigation)` block.
2. Collects every `[[_COMMUNITY_Community N|Community N]]` link number.
3. Replaces them with internal anchor links `[Community N](#community-N-community-N)`.
4. Falls back communities to "Communities (3889 total ...)" if no H3 heading exists (trim/thin).

**Run pattern:**
```
python E:/_Dev_Tools/graphify/scripts/fix-community-links.py \
    --report E:/_Knowledge/ObsidianVault/graphify-out/GRAPH_REPORT.md
```

**Permanent automation (added 2026-07-24):** the user's `vault-maintenance` cron (id `8c79d585c3b5`, daily 02:00 IST) now invokes `E:/_Dev_Tools/graphify/scripts/graphify-with-fix.py` after every graphify run, so dead community links **cannot reappear** without manual intervention. The wrapper chains:

1. `E:/_Dev_Tools/graphify/scripts/fix-community-links.py` — idempotent post-processor (atomic write via `os.replace`, auto-backup at `<report>.pre-fix-<YYYYMMDDTHHMMSS>`). Run standalone with `--report <path>` or `--report-only` (skip graphify).
2. `E:/_Dev_Tools/graphify/scripts/graphify-with-fix.py` — wrapper that runs graphify then the fixer. Continues to apply the fix even if graphify errors out.

Standard invocation:
```bash
"C:/Users/shrey/AppData/Local/Programs/Python/Python314/python.exe" \
  E:/_Dev_Tools/graphify/scripts/graphify-with-fix.py --report-only
# or full chain:
"C:/Users/shrey/AppData/Local/Programs/Python/Python314/python.exe" \
  E:/_Dev_Tools/graphify/scripts/graphify-with-fix.py cluster-only .
```

If a user-visible complaint of "empty community links" comes in, the user is likely looking at a stale state mid-afternoon *before* the next cron run. Run `--report-only` immediately; the fix takes <1s.

**Verified result (Jul-24 regen):** 2,507 dead `_COMMUNITY_` wiki-links → 1,122 in-file anchor links, 1,121 matched to `### Community N - "..."` H3 headings; 1 unmatched (a thin community graphify legitimately skipped). File 373,788 → ~354 KB. Commits `da94a670` (fix) + `b25c5dd1` (runbook docs).

**Critical recurring pattern — always check for an automated runbook whenever fixing a recurring bug:**
1. Write the one-shot fix script (idempotent, atomic, with backup).
2. Wrap it to chain after whatever generated the bug (graphify-with-fix.sh).
3. Wire the wrapper into a cron that runs on the bug's natural cycle (vault-maintenance 02:00 IST).
4. Document the chain in a vault runbook (`GRAPHIFY_INTEGRATION.md`).

This three-layer pattern cost two files + one cron-edit and made the problem permanently unobservable. The user wanted the *best* fix, not the fastest one.

**Anchor pattern verified correct on Jul-24 report:**

| Heading text in body | Obsidian slug |
|---|---|
| `### Community 0 - "Community 0"` | `#community-0-community-0` |
| `### Community 7 - "Top Indian Politicians 2026"` | `#community-7---top-indian-politicians-2026` |

Obsidian anchors are: heading text → lowercase → drop non-`[a-z0-9 -]` → spaces to hyphens → collapse repeats. **Do NOT pre-compute or invent the slug — extract it from the actual heading text in the file at fix time** (the spec/quote in older versions of this skill got the slug format wrong; only the live-slug-extraction version is correct).

The same family of bug also affects `Surprising Connections` and `God Nodes` headings — those exist as H2 in the same report and are valid anchor targets, so the rewritten Community Hubs section links directly to them.

**Pitfall — never claim the dead-link fix works without re-verifying in code:** the snippet earlier in this skill showed `#community-0---community-0` — but the **actual** Obsidian slug is `#community-0-community-0` (double-dash only appears between title words, not after the number). Always derive slug from heading text in the current file. See script `scripts/fix-community-links.py` for the working implementation.

**Backup before fixing:** copy the file to `E:/.mempalace-pre-repair-backup/GRAPH_REPORT.md.pre-fix-<timestamp>` (mempalace-pre-repair-backup is the user's pre-existing routine backup directory — fine to reuse as a one-off safety net). The script is idempotent, so a botched rewrite on a re-run is rare — but still.

**Do NOT:** Re-run `graphify cluster-only` thinking it'll fix anything — it regenerates the same dead links. The fix is **post-process the report**, not regenerate the graph.

**Trigger:** User complains about empty community links, especially with an explicit `obsidian://` deep-link to `graphify-out/GRAPH_REPORT`.

## Vault-wide tag search (cron-job pattern)

When a cron job is gated on a tag (e.g. "process every note tagged `content-pipeline`"), do NOT just grep the string — distinguish *real tags* from *prose mentions*. The string `content-pipeline` can appear in:
- YAML frontmatter array: `tags: [content-pipeline, ...]`
- YAML frontmatter block: `tags:\n  - content-pipeline`
- Body inline: `#content-pipeline`
- Plain prose ("content pipelines", in VISION.md etc.) — NOT a tag

Use `scripts/find-tag.py` (exercises the execute_code workaround pattern above):

```
cd E:/_Dev_Tools/graphify && python scripts/find-tag.py E:/_Knowledge/ObsidianVault content-pipeline
```

It reports two sections:
- **REAL TAGS**: notes that actually carry the tag (frontmatter or inline `#tag`)
- **PROSE ONLY**: string appears in body but as prose, not a tag

Pitfall: `grep -rl "content-pipeline" --include="*.md"` across the full vault times out (~8k files, large embedded web-archive transcripts). Python with `pathlib.rglob` + a binary-byte guard (`b"\x00"` test on first 1MB) finishes in under 30 seconds. Always skip `graphify-out/` and any `node_modules`-like dirs.

Concrete past run (2026-07-20): vault had 8,403 .md files. `content-pipeline` matched 0 real tags; 2 prose-only mentions in `AGENTS.md` and `tolaria/docs/VISION.md`. The cron correctly reported "no drafts to create" instead of fabricating work for prose mentions.

## Vault-wide broken-link scan

`scripts/scan-broken-links.py <VAULT_PATH>` walks the vault, computes total notes + total wiki-links + unique links, then surfaces (1) targets that don't exist with their file-count impact, ranked, and (2) orphaned notes (exist but never linked to). Useful when user complains "many community links are empty please check" or asks for a vault health audit.

Run pattern when triggered by user request like "check why my community links are broken":
```
python E:/_Dev_Tools/graphify/scripts/scan-broken-links.py E:/_Knowledge/ObsidianVault
```

Important: most "broken" targets in a typical vault are LLM-generated topic tags in `00_Index.md` / `00_Qwen_Index.md`-style auto-generated files. These look like missing notes but were never intended as real notes — they are categorization tags that don't have corresponding pages. Different from `_COMMUNITY_Community N.md` missing files (which is a graphify report-emission bug fixed by the Dead Community Links section above).

Concrete run (2026-07-20): 4,734 notes, 26,914 wiki-links, 2,202 broken-link targets — but ~75% of those were LLM-generated topic tags in `02 - AREAS/01 Philosophy & Religion/00_Index.md` and `00_Qwen_Index.md`, NOT real missing notes.

## Pitfall — `graphify query` on large vault graphs returns code-symbol noise, not topical content

**Symptom (seen 2026-07-25, cron-generated daily briefing):** Running `graphify query "<English topic question>"` against a vault graph that contains tens of thousands of code files (from embedded repos like `GitNexus/`, `tolaria/`, `ruflo/`, `InfiniteBrain/`, `consciousness-symphony/`) returns **code-symbol neighbors**, not vault topical notes. Concrete examples that hit this in one session:
- `query "Justice Party CJP protest youth movement India"` → returns `extractParty()`, `mcp-tools.ts`, `legal-contracts/`, `.movementTranscendence()`, `consciousness-symphony`. Zero topical matches.
- `query "Jammu Kashmir elections Dravidian movement language families"` → returns `getLanguageFromFilename()`, `isProductionLanguage()`, `parse-worker.ts`, `tree-sitter/parser-loader.ts`. Zero topical matches.

**Why it happens:** The graph is dominated by AST-extracted symbols from JS/TS/Python code in nested vendor repos. BFS-with-keyword-seeding cannot distinguish a function named `mcp-server/index.js#extractParty` from a vault wiki note called `Justice Party`. The vocabulary overlap is high (every code repo has "Party", "Language", "Movement", "Transcendence", "Awakening" as identifiers).

**Workaround (use this for any topic question on the vault graph):**

1. **Filter the graph to vault-only nodes first.** The vault notes live under paths like `wiki/`, `Research/`, `02 - AREAS/`, `03 - PROJECTS/`, `04 - DAILY/`, `05 - MAPS/`, `06 - OUTPUTS/`, `07 - SYSTEM/`. Everything under `tolaria/`, `ruflo/`, `GitNexus/`, `consciousness-symphony/`, `genericagent/`, `copilot/`, `.smart-env/`, `_keys/`, `node_modules/`, etc. is **embedded code, not user notes**.
2. **Use `scripts/vault-only-nodes.py --graph graph.json --out graph-vault-only.json`** to materialise a filtered graph (saves a fresh graph.json whose nodes are restricted to vault paths). Then `graphify query --graph graph-vault-only.json` returns topical results.
3. **Cheaper alternative for one-off queries:** `search_files target=content path=E:/_Knowledge/ObsidianVault file_glob=*.md pattern="<topic-keyword>"` then `read_file` the hits. For cron jobs that aggregate "what's new in the vault", this is faster and skips the noise entirely. Topic keywords here = "CJP", "Justice Party", "Dravidian", "Jammu", "language family", etc. — strings that *only* appear in user-authored vault notes, never in vendor code symbols.
4. **For `explain "<concept>"`:** if the BUT NOT the exact concept name appears as a code symbol (e.g., a function literally called `justiceParty()` or `dravidian()`), the explain route still hits the noise. Use `read_file` on the corresponding `wiki/concepts/<Concept>.md` directly instead.

**Concrete 2026-07-25 cron run:** A daily-briefing cron asked "what's important in the vault today" and tried `graphify query "<topic>"` 3 times. All 3 returned code-symbol noise. Falling back to `find . -mtime -7 ...` + targeted `read_file` on `Research/India/`, `wiki/concepts/`, `04 - DAILY/`, `05 - MAPS/` produced the actual briefing content in ~6 read_file calls. The script `scripts/vault-only-nodes.py` was created to avoid this on future cron runs.

**Trigger:** When a cron job or user asks "what's in the vault about <topic>", do NOT lead with `graphify query`. Lead with filesystem search (`search_files` + `find` + `read_file`) for the topic keyword; use `graphify query` only after confirming the topic exists in vault notes, and even then prefer `graph-vault-only.json` if one was last materialised.