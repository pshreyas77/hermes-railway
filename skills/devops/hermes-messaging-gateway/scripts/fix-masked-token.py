#!/usr/bin/env python3
"""
Fix masked Telegram bot token in Hermes config.yaml

Run this if gateway logs show "No bot token configured" but you set the token.
The `hermes config set` command masks tokens containing ':' as *** in YAML output.
"""

import sys
import re
from pathlib import Path

CONFIG_PATH = Path.home() / "AppData" / "Local" / "hermes" / "config.yaml"

def fix_token(token: str = None):
    if not CONFIG_PATH.exists():
        print(f"Config not found: {CONFIG_PATH}")
        return False

    content = CONFIG_PATH.read_text(encoding='utf-8')
    
    # Check current state
    if 'AAFo-dFCpYX2_lUv_Ru-WBzOdD0e77z4tps' in content or (token and token in content):
        print("✅ Full token already present in config.yaml")
        return True
    
    if 'bot_token: 8863778824:***' not in content and 'bot_token: "8863778824:***"' not in content:
        print("⚠️  No masked token pattern found — check config manually")
        return False

    # Replace all masked occurrences
    if token:
        full_token = token
    else:
        # Default from this session
        full_token = "8863778824:AAFo-dFCpYX2_lUv_Ru-WBzOdD0e77z4tps"
    
    # Pattern matches: bot_token: 8863778824:***  OR  bot_token: "8863778824:***"
    new_content = re.sub(
        r'bot_token:\s*"?8863778824:\*\*\*"?',
        f'bot_token: "{full_token}"',
        content
    )
    
    if new_content == content:
        print("❌ No replacement made")
        return False
    
    CONFIG_PATH.write_text(new_content, encoding='utf-8')
    print(f"✅ Fixed {content.count('8863778824:***')} occurrence(s) in config.yaml")
    return True

if __name__ == "__main__":
    token = sys.argv[1] if len(sys.argv) > 1 else None
    success = fix_token(token)
    sys.exit(0 if success else 1)