#!/usr/bin/env python3
"""
Obsidian Graph Color Watchdog
Polls graph.json every 5s and restores 23 color groups if Obsidian clears them.
Survives Obsidian restarts; runs between Obsidian reads.

Usage: python3 graph-color-watchdog.py &
       (runs in background; Ctrl+C to stop)
"""

import json
import time
import os
import sys
from pathlib import Path

GRAPH_FILE = Path("E:/_Knowledge/ObsidianVault/.obsidian/graph.json")

CORRECT_CONFIG = {
    "collapse-filter": False,
    "search": "",
    "showTags": True,
    "showAttachments": False,
    "hideUnresolved": True,
    "showOrphans": False,
    "collapse-color-groups": False,
    "colorGroups": [
        {"query": "path:/02 - AREAS/03 Ancient Civilizations", "color": {"r": 249, "g": 115, "b": 22}},
        {"query": "path:/02 - AREAS/01 Philosophy & Religion", "color": {"r": 168, "g": 85, "b": 247}},
        {"query": "path:/02 - AREAS/02 AI & Technology", "color": {"r": 16, "g": 185, "b": 129}},
        {"query": "path:/02 - AREAS/04 Political Analysis", "color": {"r": 239, "g": 68, "b": 68}},
        {"query": "path:/02 - AREAS/05 Knowledge Management", "color": {"r": 59, "g": 130, "b": 246}},
        {"query": "path:/02 - AREAS/06 Personal Development", "color": {"r": 236, "g": 72, "b": 153}},
        {"query": "path:/02 - AREAS/07 Society & Culture", "color": {"r": 234, "g": 179, "b": 8}},
        {"query": "path:/01 - LITERATURE/", "color": {"r": 6, "g": 182, "b": 212}},
        {"query": "path:/03 - PROJECTS/Active", "color": {"r": 245, "g": 158, "b": 11}},
        {"query": "path:/03 - PROJECTS/Completed", "color": {"r": 132, "g": 204, "b": 22}},
        {"query": "path:/03 - PROJECTS/concepts", "color": {"r": 132, "g": 204, "b": 22}},
        {"query": "path:/03 - PROJECTS/people", "color": {"r": 99, "g": 102, "b": 241}},
        {"query": "path:/03 - PROJECTS/questions", "color": {"r": 20, "g": 184, "b": 166}},
        {"query": "path:/04 - DAILY", "color": {"r": 100, "g": 116, "b": 139}},
        {"query": "path:/05 - MEMORY", "color": {"r": 14, "g": 165, "b": 233}},
        {"query": "path:/05 - INTELLIGENCE", "color": {"r": 139, "g": 92, "b": 246}},
        {"query": "path:/05 - OUTPUTS", "color": {"r": 244, "g": 114, "b": 182}},
        {"query": "path:/06 - OUTPUTS", "color": {"r": 244, "g": 114, "b": 182}},
        {"query": "tag:#moc", "color": {"r": 255, "g": 255, "b": 255}},
        {"query": "tag:#index", "color": {"r": 209, "g": 213, "b": 219}},
        {"query": "tag:#dravidian", "color": {"r": 249, "g": 115, "b": 22}},
        {"query": "tag:#ancient-civilization", "color": {"r": 251, "g": 146, "b": 60}},
        {"query": "tag:#ai", "color": {"r": 16, "g": 185, "b": 129}}
    ],
    "collapse-display": True,
    "showArrow": True,
    "textFadeMultiplier": 0.3,
    "nodeSizeMultiplier": 1.3,
    "lineSizeMultiplier": 0.7,
    "collapse-forces": True,
    "centerStrength": 0.6,
    "repelStrength": 15,
    "linkStrength": 0.8,
    "linkDistance": 180,
    "scale": 0.3,
    "close": False
}

def check_and_restore():
    try:
        with open(GRAPH_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        color_groups = data.get('colorGroups', [])
        if not color_groups or color_groups == []:
            # Obsidian cleared it — restore
            with open(GRAPH_FILE, 'w', encoding='utf-8') as f:
                json.dump(CORRECT_CONFIG, f, indent=2)
            print(f"[{time.strftime('%H:%M:%S')}] ✅ Restored 23 color groups")
            return True
    except (json.JSONDecodeError, FileNotFoundError):
        # File missing or corrupted — write fresh
        with open(GRAPH_FILE, 'w', encoding='utf-8') as f:
            json.dump(CORRECT_CONFIG, f, indent=2)
        print(f"[{time.strftime('%H:%M:%S')}] ✅ Created fresh graph.json with 23 color groups")
        return True
    return False

def main():
    print(f"🔍 Watchdog started — polling {GRAPH_FILE} every 5s")
    print("   (Ctrl+C to stop)")
    
    # Initial check
    check_and_restore()
    
    while True:
        try:
            time.sleep(5)
            check_and_restore()
        except KeyboardInterrupt:
            print("\n🛑 Watchdog stopped")
            break
        except Exception as e:
            print(f"⚠️  Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()