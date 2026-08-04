---
name: mempalace
description: MemPalace — mine projects and conversations into a searchable memory palace. Use when asked about mempalace, memory palace, mining memories, searching memories, or palace setup.
trigger: /mempalace
---

# /mempalace

Local-first AI memory — verbatim storage, no summarization. Source at `E:/_Dev_Tools/mempalace/`.

## Vault context

Your vault is already initialized:
- **Entities**: 15 people, 9 projects detected
- **Entities file**: `E:/_Knowledge/ObsidianVault/entities.json`
- **Storage**: ChromaDB at `E:/_Dev_Tools/mempalace/palace/`

## Windows Installation Note (Added 2026-07-18, REPAIRED 2026-07-20)

**Known issue**: MemPalace's `chromadb` dependency pulls `numpy` which has a Python 3.14 vs 3.11 ABI mismatch on Windows when Hermes's venv (Python 3.11 numpy) shadows the uv tool's isolated Python 3.14 environment.

**Solution that works (REPAIRED 2026-07-20)**: Wrap the `mempalace` binary in `E:/_Dev_Tools/mempalace/mp.sh` with these fixed exports:
```bash
#!/bin/bash
unset PYTHONPATH
unset PYTHONHOME
export HF_HOME="E:/.hf-home"
export HF_HUB_CACHE="E:/.hf-home/hub"
export TRANSFORMERS_CACHE="E:/.hf-home/transformers"
export CHROMA_HOME="E:/.chroma-cache"
export PYTHONUSERBASE="E:/.python-userbase"
export TMPDIR="E:/.tmp"
export TEMP="E:/.tmp"
export TMP="E:/.tmp"
PY_BIN="/c/Users/shrey/AppData/Local/Programs/Python/Python314/python.exe"
"$PY_BIN" -m mempalace "$@"
```

Invoke as `E:/_Dev_Tools/mempalace/mp.sh status` etc. This pattern:
1. Clears Python path pollution from Hermes venv
2. Forces E: drive for all caches (no C: pollution — respects user rule)
3. Avoids `numpy._core._multiarray_umath` import error

Other (less reliable) workarounds:
1. **Docker** (sometimes works but pulls 79MB ONNX model on every run): `docker build -t mempalace . && docker run -i --rm -v mempalace-data:/data mempalace`
2. **Force Python 3.11**: `uv tool install --python 3.11 mempalace` (if 3.11 is available)

The vault at `E:/_Knowledge/ObsidianVault` is already initialized with `entities.json` (15 people, 9 projects). The `mempalace init` step is complete.

## Pitfalls — MemPalace mine warnings to NOT STOP on (2026-07-20 lessons)

When running `mempalace mine` for the first time on a large vault, you may encounter two warnings that look like errors but are not fatal:

1. **`httpx.ReadTimeout: The read operation timed out in upsert.`** — ChromaDB's first UPSERT can exceed httpx default timeout (5s). Mining did NOT fail: check `C:/Users/shrey/.mempalace/palace/chroma.sqlite3` for actual embeddings count. Treat as warning, not error.

2. **`OSError: [Errno 36] Resource deadlock avoided` from `msvcrt.locking(lf.fileno(), msvcrt.LK_LOCK, 1)`** — Windows-specific issue with byte-locking on the mine lock file. Mine actually proceeded (data is in chroma.sqlite3). Leave the stale `.lock` file alone — system re-acquires on next run. Don't keep retrying.

3. **First-run DB download** — chromadb downloads a 79MB ONNX model (`all-MiniLM-L6-v2`) to first embedding call. Watch for `onnx.tar.gz` progress bar. With `CHROMA_HOME` in your mp.sh wrapper, this stays in `E:/.chroma-cache/` not C:. The 50+MB partial download is preserved between runs.

## Pre-repair Backup Pattern (Lesson)

When user asks to "repair" a tool that may have irreplaceable state:
1. First copy `entities.json`, config files, and any user data files to a backup directory like `E:/.mempalace-pre-repair-backup/`.
2. Run the repair command.
3. Verify by `diff` against the backup that nothing usable was touched.

This protects against repair actions that look harmless but overwrite working state. Concrete example: 2026-07-20 mp.sh repair on a non-existent palace — returned "No palace found", but having a backup meant I could verify `known_entities.json`, `entities.json`, and `mempalace.yaml` were untouched before moving on to the actual install.

**Reusable "second brain" repair pattern** (generalizes beyond mempalace):
- User's "repair my [tool/second-brain/system] without losing data" is a recurring request shape across this vault.
- Generic recipe:
  ```python
  from pathlib import Path
  backup = Path(f"E:/.{tool_name}-pre-repair-backup")
  backup.mkdir(exist_ok=True)
  # Copy all "state" files (config, data, generated history)
  for src in state_files:
      if src.exists():
          shutil.copy2(src, backup)
  # Then repair / initialize / re-mine
  # Then verify untouched state files match backup
  ```
- If repair finds the state didn't exist (palace was never built, config was broken from install), report honestly: "nothing was lost, nothing existed to repair" and proceed to the actual install.

## Key paths

- CLI: `C:/Users/shrey/AppData/Roaming/uv/tools/mempalace/Scripts/mempalace`
- Source: `E:/_Dev_Tools/mempalace/`
- Entities: `E:/_Knowledge/ObsidianVault/entities.json`
- **Palace data: `C:/Users/shrey/.mempalace/palace/`**  (NOT under the source tree — fixed 2026-07-24)

## See also

- `references/repair-and-healthcheck.md` — full procedure for `mp.sh repair --yes`
  when vector search shows the "HNSW diverged" notice. Includes pre-repair
  backup recipe and verification steps.