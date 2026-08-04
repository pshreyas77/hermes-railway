# Mempalace Invocation (Cross-Tool Pitfall)

**Local rule:** do NOT call `mempalace <cmd>` directly from the bare `mempalace`
executable on PATH (at `~/.local/bin/mempalace.exe` →
`C:/Users/shrey/AppData/Local/Programs/Python/Python314/Scripts/mempalace.exe`).
It resolves to **system Python 3.14**, which lacks `numpy._core._multiarray_umath`
and crashes immediately on every command:

```
ModuleNotFoundError: No module named 'numpy._core._multiarray_umath'
```

The toolchain installed at `E:/_Dev_Tools/mempalace/` has its own venv with the
correct ABI-linked numpy and chromadb. Run from there:

```
cd E:/_Dev_Tools/mempalace && python -m mempalace status
cd E:/_Dev_Tools/mempalace && python -m mempalace sweep "C:/Users/shrey/.claude/projects/<proj>/"
```

(Use `"..."` quoted Windows-style paths in `sweep` — POSIX paths raised
`Not a file or directory`.)

## Other quirks observed (2026-07-23 cron run)

- **Embedder identity warning:** new collections log
  `EmbedderIdentityUnknownWarning: palace collection 'mempalace_drawers' has
  no recorded embedder identity`. Silence it with `python -m mempalace
  palace set-embedder --model minilm`.
- **Fresh sweeps land in `WING: ? / ROOM: ?`** until the miner classifies them
  on the next index pass. This is cosmetic, not an error.
- **`sweep <dir>` is idempotent and counter-safe.** Re-running on a dir with
  no new `.jsonl` files reports `+0 new, 0 already present, 0 skipped` and
  returns exit 0. Safe to run on a cron.

## Typical cron-job combo (graphify + mempalace sweep)

```bash
cd E:/_Knowledge/ObsidianVault && graphify update E:/_Knowledge/ObsidianVault --update
cd E:/_Dev_Tools/mempalace     && python -m mempalace sweep "C:/Users/shrey/.claude/projects/E---Knowledge-ObsidianVault/"
```
