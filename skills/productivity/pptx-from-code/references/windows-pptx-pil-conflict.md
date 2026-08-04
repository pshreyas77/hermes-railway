# python-pptx on Windows — PIL Conflict & Fix

## The hermes-agent venv PIL contamination

**Problem:** Importing `pptx` fails with:
```
ImportError: cannot import name '_imaging' from 'PIL'
```
The hermes-agent venv at `C:/Users/shrey/AppData/Local/hermes/hermes-agent/venv/` has a broken PIL that gets injected via `PYTHONPATH` or `sys.path`, shadowing any clean PIL you install.

**Diagnosis:** The error is specifically about `_imaging` not being importable from `PIL`. This means the PIL's C extension (`_imaging.cpython-xxx.so`) is missing or corrupt. python-pptx depends on Pillow's image handling, so this breaks the import chain at `pptx.parts.image`.

**The fix — isolated venv + PYTHONPATH="":**

```bash
# 1. Create clean venv with python3.14
uv venv C:/Users/shrey/AppData/Local/Temp/pptx_venv --python python3.14 -q

# 2. Install into the venv's Python (NOT system)
uv pip install --python C:/Users/shrey/AppData/Local/Temp/pptx_venv/Scripts/python.exe python-pptx -q

# 3. Run with PYTHONPATH="" — CRITICAL on Windows
PYTHONPATH="" C:/Users/shrey/AppData/Local/Temp/pptx_venv/Scripts/python.exe your_script.py
```

**Why `PYTHONPATH=""` is needed:** On Windows, bash environment variables from the hermes startup can persist in the session. Setting `PYTHONPATH=""` explicitly clears `sys.path` of the hermes venv entry, preventing its broken PIL from loading. Without this, even the isolated venv's Python gets the hermes PIL prepended to `sys.path`.

**On Linux/macOS:** Not needed. Just use `uv run --with python-pptx python your_script.py`.

---

## Quick diagnostic

```bash
# Check which Python is default
python3 -c "import sys; print(sys.version, sys.executable)"

# Check if pptx is importable
python3 -c "from pptx import Presentation; print('ok')"

# If PIL error, use the venv:
PYTHONPATH="" C:/Users/shrey/AppData/Local/Temp/pptx_venv/Scripts/python.exe -c "from pptx import Presentation; print('ok')"
```

## Why this matters

Every time you need to generate a `.pptx` from code, you now have a tested pattern that works regardless of the hermes venv's state. The key signal is the `_imaging` import error from PIL — that means PIL is present but broken, and python-pptx is picking it up instead of a clean install.