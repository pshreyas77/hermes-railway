# Telegram Bot Commands Reference

## Bot Setup
```bash
# 1. Create bot with @BotFather
# 2. Get BOT_TOKEN
# 3. Get your USER_ID from @userinfobot
# 4. Add to E:/_Dev_Tools/jarvis/.env:
JARVIS_TELEGRAM_BOT_TOKEN=your_token_here
JARVIS_TELEGRAM_USER_ID=123456789
```

## Command Reference

### System Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Show main menu with inline buttons | `/start` |
| `/help` | Show all commands | `/help` |
| `/status` | System health check | `/status` |
| `/brief` | Daily briefing from graphify | `/brief` |
| `/maintenance` | Run vault maintenance | `/maintenance` |

### Knowledge Graph (graphify)

| Command | Description | Example |
|---------|-------------|---------|
| `/graph "question"` | BFS query (broad context) | `/graph "Justice Party 1937 election"` |
| `/graph "q" --mode dfs` | DFS query (deep dive) | `/graph "Periyar ideological evolution" --mode dfs` |
| `/path "A" "B"` | Shortest path A→B | `/path "Justice Party" "DMK"` |
| `/explain "concept"` | Plain-language explanation | `/explain "Communal G.O. 3136"` |
| `/god` | Top connected nodes | `/god` |

### Memory (MemPalace)

| Command | Description | Example |
|---------|-------------|---------|
| `/mem "query"` | Search verbatim memories | `/mem "Periyar 1932 USSR visit"` |
| `/wake` | L0+L1 context for session | `/wake` |

### Vault Operations

| Command | Description | Example |
|---------|-------------|---------|
| `/note "Title" "Content"` | Create daily note | `/note "Research idea" "Explore G.O. 3136 impact"` |
| `/run "command"` | Execute shell in vault | `/run "ls -la"` |

### AI Assistant

| Command | Description | Example |
|---------|-------------|---------|
| `/hermes "prompt"` | Ask Hermes directly | `/hermes "Summarize G.O. 3136"` |

## Interactive Menu

`/start` shows inline keyboard:
```
┌─────────────────────────────────────┐
│ 🤖 Jarvis Online                    │
│ Vault: E:/_Knowledge/ObsidianVault  │
│ Graph: 50k nodes │ 97k edges        │
├─────────────────────────────────────┤
│ 📋 Daily Brief    📊 Status         │
│ 🔍 Graph Query    🧠 Mem Search     │
│ ⚙️ Maintenance    📝 Create Note    │
└─────────────────────────────────────┘
```

## Callback Handlers

| Button | Callback Data | Action |
|--------|---------------|--------|
| 📋 Daily Brief | `brief` | Runs `/brief` |
| 📊 Status | `status` | Runs `/status` |
| 🔍 Graph Query | `graph` | Prompts for query |
| 🧠 Mem Search | `mem` | Prompts for query |
| ⚙️ Maintenance | `maintenance` | Runs graphify update |
| 📝 Create Note | `note` | Prompts for title/content |

## Natural Language Fallback

Any non-command text is treated as a graphify query:
```
User: "What happened in 1937 Justice Party election?"
Jarvis: 🔍 **Graph Query**: What happened in 1937 Justice Party election?
        [graphify BFS result...]
```

## Authorization

Only `JARVIS_TELEGRAM_USER_ID` can use the bot:
```python
ALLOWED_USER_ID = int(os.getenv("JARVIS_TELEGRAM_USER_ID", "0"))

async def check_user(update):
    return update.effective_user.id == ALLOWED_USER_ID
```

## Running the Bot

```bash
# Development
python E:/_Dev_Tools/jarvis/telegram/bot.py

# Production (systemd)
# /etc/systemd/system/jarvis-telegram.service
[Unit]
Description=Jarvis Telegram Bot
After=network.target

[Service]
Type=simple
User=shrey
WorkingDirectory=E:/_Dev_Tools/jarvis/telegram
EnvironmentFile=E:/_Dev_Tools/jarvis/.env
ExecStart=python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

## Message Formatting

All responses use Markdown parsing:
```python
await update.message.reply_text(
    f"🔍 **Graph Query**: {query}\n\n{output[:3500]}",
    parse_mode="Markdown"
)
```

**Length limits**: Telegram max 4096 chars. Truncate with `[:3500] + "\n\n... (truncated)"`

## Error Handling

```python
async def error_handler(update, context):
    logger.error(f"Update {update} caused error: {context.error}")
    if update and update.message:
        await update.message.reply_text("⚠️ Something went wrong. Try again.")
```

## Testing Commands

```bash
# Test graphify
python -c "
import subprocess
result = subprocess.run(['graphify', 'query', 'Justice Party', '--budget', '500'], 
                       cwd='E:/_Knowledge/ObsidianVault', capture_output=True, text=True)
print(result.stdout[:500])
"

# Test telegram bot locally
python E:/_Dev_Tools/jarvis/telegram/bot.py
# In Telegram: /start, /help, /graph "test"
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Bot not responding | Check `JARVIS_TELEGRAM_BOT_TOKEN` and `JARVIS_TELEGRAM_USER_ID` in `.env` |
| "Unauthorized" | Verify `JARVIS_TELEGRAM_USER_ID` matches your `@userinfobot` ID |
| Graphify timeout | Increase timeout or lower `--budget` |
| Command not found | Ensure `graphify` is on PATH or use full path |
| Bot not starting | Check `JARVIS_TELEGRAM_BOT_TOKEN` is valid from @BotFather |