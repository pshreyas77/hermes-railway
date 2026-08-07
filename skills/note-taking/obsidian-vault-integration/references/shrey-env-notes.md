# Shrey's Environment Notes

## Vault Path
- **Vault:** `/vault`
- **Set via:** `OBSIDIAN_VAULT_PATH` in `~/.hermes/.env`
- **Convention:** All installs/clones/builds → E: drive ONLY (never C:)

## Dev Tools Location
- **/home/hermes/** — graphify, mempalace, openclaude, openresearchclaw, nano, OPENSPEC
- **/home/hermes/_AI_Tools/** — Atomic Chat, LM-Studio, ollama, opencode, openresearchclaw

## Critical Windows Path Bug

### search_files (ripgrep) fails silently on paths with spaces
This vault is at `/home/hermes/` with spaces in folder names (e.g., `02 - AREAS/`).
`search_files` with `target: "content"` returns zero results without error.

**Workaround — always use terminal grep:**
```bash
terminal cd "/vault" && grep -rl "pattern" . --include="*.md"
```

**file tools (read_file, write_file, patch)** work fine with quoted absolute paths — only `search_files` is broken.

## Python Environment Poisoning

hermes-agent sets `PYTHONPATH` to its venv (`C:/Users/shrey/AppData/Local/hermes/hermes-agent/venv/Lib/site-packages`). This poisons isolated tools like `mempalace` and `graphify` when they run in the same shell.

**Fix:** Run external tools in a clean environment:
```bash
env -i PATH="/c/Users/shrey/AppData/Roaming/uv/tools/mempalace/Scripts:/c/Users/shrey/AppData/Roaming/uv/tools/graphify" mempalace mine ...
```
Or use Docker for complete isolation.