---
name: philosophy-playlist
description: Indian Philosophers & Batman Video Playlist — generates a dark-themed interactive HTML playlist with all video/book links organized by philosopher
triggers:
  - "make a playlist of Indian philosophy videos"
  - "open philosophy video playlist"
  - "batman philosophy playlist"
  - "open the playlist i made earlier"
when_to_load: always_available
---

# Indian Philosophers & Batman — Video Playlist

## Files in vault
- **HTML (interactive):** `E:/_Knowledge/ObsidianVault/03 - RESOURCES/Indian Philosophers — Video & Book Playlist.html`
- **Markdown note:** `E:/_Knowledge/ObsidianVault/03 - RESOURCES/Indian Philosophers — Video & Book Playlist.md`

## Quick restore (rebuild from source canvases if HTML is lost)
1. Read `E:/_Knowledge/ObsidianVault/03 - RESOURCES/Philosophy_Links_Tracker.canvas` → extract all `https://` URLs from text nodes (group by x-position: Osho<-500, JK-300, UGK<300, Nag<750, Char≥900)
2. Read `E:/_Knowledge/ObsidianVault/03 - RESOURCES/Batman Philosophy Archive.canvas` → extract all `[YouTube](url)` links
3. Inject into the HTML template (dark theme, Inter font, video-card + book-row layout)
4. Copy to `/c/Users/shrey/AppData/Local/Temp/playlist.html` for browser viewing

## Playlist contents (verified 2025-07-13)
| Philosopher | Videos | Books | Color |
|-------------|--------|-------|-------|
| Osho | 5 | 3 | 🧡 orange |
| J. Krishnamurti | 6 | 5 | 💜 purple |
| U.G. Krishnamurti | 5 | 2 | 💙 cyan |
| Nagarjuna | 2 | 3 | 🟡 amber |
| Charvaka | 2 | 2 | 🌸 pink |
| Batman | 16 | 0 | 🦇 slate |
| **Total** | **36** | **15** | |