---
name: second-brain
description: Search and query the user's Obsidian vault (second brain) via the /second-brain slash command.
platforms: [linux, macos, windows]
---

# Second Brain (/second-brain command)

When the user sends `/second-brain` (with or without a query), treat it as a request to query their second brain — the Obsidian vault.

## Recognising the command

The command may arrive as:

- `/second-brain <query>` — search the vault for `<query>` and return the most relevant notes.
- `/second-brain` (no query) — list the top-level folders of the vault.
- `/second-brain help` — show usage info.

## Vault path

The vault is cloned from `https://github.com/pshreyas77/MYOBSIDIAN-VAULT` at container startup and lives at `/vault` inside the running container.

**CRITICAL**: You MUST explicitly pass paths under `/vault/...` when calling file tools. The `OBSIDIAN_VAULT_PATH` environment variable is set but file tools do NOT auto-resolve it. Always use `/vault/...` as the path prefix.

If `/vault` does not exist or is empty, tell the user the vault isn't synced yet.

## Behaviour

1. **Parse the command.** If no query follows `/second-brain`, list top-level folders using `search_files(target="files", pattern="*", path="/vault")`.

2. **Search the vault.** For a query like `/second-brain resume`, run `search_files(target="content", pattern="resume", path="/vault", file_glob="*.md")`.

3. **Open the top 3 hits.** Read with `read_file(path="/vault/<relative_path>")`.

3. **Compose answer.** Short summary + bulleted list with paths and one-line excerpts. Stay under ~1500 chars.

## Safety

- Only **read** from `/vault`. No write/edit/delete.
- Never execute shell commands.
- Present paths relative to `/vault` or as wikilinks `[[Note Name]]`.
