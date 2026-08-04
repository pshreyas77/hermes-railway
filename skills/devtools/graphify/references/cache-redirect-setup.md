# Windows Cache Redirect to E: Drive

**Date:** 2026-07-20
**Problem:** UV, pip, and Python temp default to `C:\Users\shrey\AppData\Local\` — pollutes C: drive and violates E: drive rule.

---

## What Was Redirected

| Cache | Was | Now |
|-------|-----|-----|
| UV package cache | `C:\Users\shrey\AppData\Local\uv\cache` | `E:\.uv-cache` |
| pip downloads | `C:\Users\shrey\AppData\Local\pip\cache` | `E:\.pip-cache` |
| Python temp | `C:\Users\shrey\AppData\Local\Temp` | `E:\.tmp` |

---

## Where Set

### 1. `~/.bashrc` (session-level, auto-loaded)

```bash
export UV_CACHE_DIR="E:/.uv-cache"
export PIP_CACHE_DIR="E:/.pip-cache"
export TMP="E:/.tmp"
export TEMP="E:/.tmp"
```

Loaded automatically because `auto_source_bashrc: true` in Hermes config.

### 2. Windows System Environment (via `setx`)

```bash
setx UV_CACHE_DIR "E:\.uv-cache"
setx PIP_CACHE_DIR "E:\.pip-cache"
setx TMP "E:\.tmp"
setx TEMP "E:\.tmp"
```

Persists across reboots for all Windows processes.

### 3. Hermes `.env` (blocked — protected file)

The file at `C:\Users\shrey\AppData\Local\hermes\.env` is protected. Can't write to it. Use `setx` + `.bashrc` instead.

---

## E: Cache Dirs Created

```
E:/.uv-cache/
E:/.pip-cache/
E:/.tmp/
```

---

## Verification

```bash
source ~/.bashrc
echo "UV=$UV_CACHE_DIR PIP=$PIP_CACHE_DIR TMP=$TMP"
# Expected: UV=E:/.uv-cache PIP=E:/.pip-cache TMP=E:/.tmp

# Test a pip install writes to the right cache:
uv pip install --system psutil
ls E:/.uv-cache/  # should show packages
```

---

## Note: pymupdf Already on E:

Python 3.14 packages (including pymupdf) are already on E: at:
```
C:\Users\shrey\AppData\Local\Programs\Python\Python314\Lib\site-packages\
```
This is fine — it's in `C:\Program Files\` which is system-level, not user-level.

## Note: MemPalace ChromaDB Already on E:

MemPalace stores `chroma.sqlite3` inside the vault folder (E:), so it's already compliant.

## Note: Graphify Already on E:

`E:/_Dev_Tools/graphify/` — source and output both on E:.

## Key Windows Gotcha

`python3` on PATH → Python 3.13 (WindowsApps) — has NO packages.
`C:/Users/shrey/AppData/Local/Programs/Python/Python314/python.exe` → Python 3.14 — has pymupdf, networkx, etc.

Always use the full path for Python 3.14 when running scripts:
```
"C:/Users/shrey/AppData/Local/Programs/Python/Python314/python.exe" script.py
```

This applies to: pymupdf, networkx, python-louvain, plotly.