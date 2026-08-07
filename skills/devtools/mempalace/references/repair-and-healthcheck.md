# MemPalace — Repair and Healthcheck Procedures (added 2026-07-24)

Procedures for when the user's palace exists but produces degraded output (e.g.
"vector search disabled" notices, slow search, divergent indices, "match: 0.000"
results). Reproduces the recovery path proven on 2026-07-24 against a
6,026-drawer palace in 4 minutes, in front of the user.

## When the user sees a vector-search disabled notice

`mp.sh search "..."` may emit:

```
NOTICE: vector search disabled — HNSW index has diverged from SQLite.
        Showing BM25-only results. Run `mempalace repair` to restore vector search.
```

This is repairable. **Do not** recommend reinstalling or losing data — the SQLite
ground truth is intact and `repair` rebuilds vectors from it without touching
the rest of the system.

## Canonical palace paths on this system

| What | Path |
|------|------|
| CLI wrapper | `/home/hermes/mempalace/mp.sh` |
| Source tree | `/home/hermes/mempalace/` |
| **Palace data** | `C:/Users/shrey/.mempalace/palace/` |
| **Repo-mirrored palace in source tree** | `/home/hermes/mempalace/palace/` (does not exist on this system — the palace lives outside the source repo) |
| Entities | `/vault/entities.json` |
| Pre-repair safety backups | `/home/hermes/.mempalace-pre-repair-backup/` |

**Pitfall — misreading the source tree**: `/home/hermes/mempalace/` contains
plugin-style directories (`.claude-plugin/`, `.codex-plugin/`, `.cursor-plugin/`,
`.agents/`, `.agent/`). These belong to **MemPalace** — MemPalace ships MCP-server
plugin manifests for multiple IDEs (`mcp.json` at repo root). They look like
claude-mem's layout because both tools target the same agent ecosystem. Verify
identity with `cat pyproject.toml` or `cat README.md` first sentence —
MemPalace by Milla Jovovich (Python, `pyproject.toml`, MIT); claude-mem by
thedotmack (Node/Bun, `package.json`, Apache-2.0).

## Repair procedure (verified 2026-07-24, 6,026 drawers, ~4 minutes)

### 1. Pre-repair safety backup

The `repair` command itself takes a backup to `palace.backup/` automatically,
but always take a separate copy with a timestamp first — cheap insurance
against an abnormal exit mid-repair.

```bash
TS=$(date +%Y%m%dT%H%M%S)
cp "C:/Users/shrey/.mempalace/palace/chroma.sqlite3" \
   "/home/hermes/.mempalace-pre-repair-backup/chroma.sqlite3.pre-repair-${TS}"
cp "/vault/entities.json" \
   "/home/hermes/.mempalace-pre-repair-backup/entities.json.pre-repair-${TS}" 2>/dev/null
```

### 2. Run repair interactively without `--yes` first to preview

```bash
/home/hermes/mempalace/mp.sh repair
# Expected output:
#   MemPalace Repair
#   Palace: C:\Users\shrey\.mempalace\palace
#   Drawers found: N
#   Repair will replace data in: C:\Users\shrey\.mempalace\palace
#   A backup will be created first, then the palace will be rebuilt.
#   Continue? [y/N]:
```

If the prompt shows the right drawer count (matches a recent `status`), proceed.

### 3. Confirm and run

```bash
/home/hermes/mempalace/mp.sh repair --yes
```

The wrapper auto-creates a backup at `C:/Users/shrey/.mempalace/palace.backup/`

### 4. Verify vector search works again

```bash
/home/hermes/mempalace/mp.sh search "any test query"
```

Success: results show numeric `Match:` with vector scores (e.g.
`Match: 0.545`, `Match: 0.453`) and **no** BM25-only notice.

Failure: notice reappears. Re-run `repair --yes`. Repeat up to 2 times; if it
still fails, see "When repair fails" below.

### 5. Confirm drawer count and structure unchanged

```bash
/home/hermes/mempalace/mp.sh status
```

The drawer count and per-room totals should match what they were before repair.

## When repair fails or stalls

Likely causes, in order of likelihood:

1. **Stale lock file** at `C:/Users/shrey/.mempalace/palace/<segment>/` —
   byte-lock left over from a previous crash. See `msvcrt.locking` pitfall in
   main SKILL.md. Solution: leave alone; repair will retry. Don't `rm` the lock
   without thinking — Windows itself may hold it briefly.

2. **ChromaDB version mismatch** — once had a 3.0.0 → 3.1.0 migration oddity.
   Run `mp.sh migrate --dry-run` to preview; `mp.sh migrate --yes` to apply.
   Re-run repair after migrate.

3. **Underlying vault corruption** — if SQLite ground truth is also bad, repair
   cannot rebuild vectors without a working corpus. Re-mine or re-init.

## Forensic pattern after a noisy search session

The user is most likely to encounter HNSW divergence after:

- A previous aborted `repair` (the user's session shipped `repair` mid-write
  then exited).
- A Chroma version upgrade (off-cycle).
- A crash during `mine` / `sweep` while embeddings were being upserted.

In all three cases: SQLite has the truth, HNSW diverged. Repair fixes it.

## Cache locations when wrapped

The `mp.sh` wrapper redirects all caches to E: — important because if you call
mempalace without the wrapper, you can pick up stale C: sidecars that
contradict E: state (Chroma's cache dir in particular). Always:

```bash
/home/hermes/mempalace/mp.sh <anything>
```

## Pitfall — flag positioning with `mp.sh`

`mp.sh --palace <path> status` works. `mp.sh status --palace <path>` does
**not** — the wrapper intercepts `--palace` before passing args through, and
the inner `python -m mempalace` only accepts `--palace` in its own arg parser.
Thread it on the **left**:

```bash
mp.sh --palace C:/Users/shrey/.mempalace/palace status   # works
mp.sh status --palace C:/Users/shrey/.mempalace/palace   # "error: unrecognized"
```

If a user copy-paste gives you the right-side form, fix it before running.

## Commands added since this skill was last edited (2026-07-24)

`mp.sh` now exposes more subcommands than the early-version SKILL.md called
out. The full list:

```
init, mine, sweep, sync, search, compress, wake-up, split, hook,
instructions, repair, mcp, serve, migrate, migrate-wings, hallways,
status, palace
```

Notable additions:

- `mp.sh sync` — incremental palace sync (faster than `mine` for small diffs).
- `mp.sh daemon` — run a long-lived background daemon for hook capture.
- `mp.sh mcp` — print the MCP setup line; helpful for wiring Claude Desktop
  or other graph clients.
- `mp.sh serve` — start an HTTP reader for the palace.
- `mp.sh migrate` / `migrate-wings` — schema upgrades.
- `mp.sh hallways` / `palace` — walk the palace structure.
- `mp.sh wake-up` — L0+L1 short context (600-900 tokens) for prompt priming.
