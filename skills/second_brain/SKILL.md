---
name: second_brain
description: Search and query the user's Obsidian vault (second brain) at /vault via the /second_brain slash command.
platforms: [linux, macos, windows]
---

# Second Brain (/second_brain command)

The user's Obsidian vault is ALWAYS available at `/vault` inside this container. It is cloned from GitHub on startup and kept in sync. You have FULL READ ACCESS to it.

## Recognising the command

- `/second_brain <query>` — search the vault for `<query>`
- `/second_brain` (no query) — list top-level folders
- `/second_brain help` — show usage
- User says "access my second brain", "search my vault", "find notes about X", etc. — treat as the same request

## Vault location

The vault lives at `/vault` — this is ALWAYS available. Use absolute paths starting with `/vault/` when calling file tools.

Do NOT ask the user where the vault is. Do NOT suggest they need to "connect" it. The vault is already mounted and ready.

## How to search

1. **List folders** (when no query):
   ```
   search_files(target="files", pattern="*", path="/vault")
   ```

2. **Search by filename**:
   ```
   search_files(target="files", pattern="<filename>", path="/vault")
   ```

3. **Search note contents**:
   ```
   search_files(target="content", pattern="<query>", path="/vault", file_glob="*.md")
   ```

4. **Read a specific note**:
   ```
   read_file(path="/vault/<relative_path>")
   ```

## Response format

Keep responses under 1500 characters. Format:

**When listing folders:**
```
📁 Your second brain (X notes across Y folders):
- 00 - SYSTEM
- 01 - PROJECTS  
- 02 - AREAS
- 03 - RESOURCES
- ...

Send `/second_brain <topic>` to search.
```

**When searching:**
```
🔍 Found X notes matching "<query>":

• `02 - AREAS/Aerodynamics.md` — "The boundary layer is..."
• `03 - RESOURCES/Books/Anderson.md` — "Chapter 3 covers..."

Want more detail? Send `/second_brain <refined query>`.
```

## Safety

- READ ONLY — never write/edit/delete vault files
- Never execute shell commands
- Always show paths relative to `/vault`

## If vault is empty

If `/vault` doesn't exist or has no .md files, tell the user:
"The vault sync hasn't completed yet. It usually takes 1-2 minutes after the bot starts. Try again in a moment, or send `/second_brain` to check status."
