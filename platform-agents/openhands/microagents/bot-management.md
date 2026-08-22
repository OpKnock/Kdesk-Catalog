---
name: "bot-management"
description: "Builds and operates chat bots (Telegram, Slack, Discord, IRC) with webhooks, message routing, rate limiting, and observability."
type: knowledge
triggers: ["bot-management", "bot-frameworks", "bot-runtime"]
---

# bot-management

Builds and operates chat bots (Telegram, Slack, Discord, IRC) with webhooks, message routing, rate limiting, and observability.

## Instructions

# Bot Management

Build and operate chat platform bots.

## When to Use

- Customer support triage on chat channels
- Notifications and alerting into team chats
- Automation commands (slash commands)
- Community moderation

## Commands

```bash
# Setup
pip install python-telegram-bot
npm install slack-bolt
npm install discord.js

# Verify a Telegram bot token
curl -s https://api.telegram.org/bot$TOKEN/getMe

# Check webhook registration
curl -s https://api.telegram.org/bot$TOKEN/getWebhookInfo

# Run and manage
python bot.py
node bot.js
pm2 start bot.js --name telegram-bot
pm2 logs telegram-bot
pm2 restart telegram-bot
```

## Telegram Example

```python
from telegram.ext import Application, CommandHandler

async def start(update, context):
    await update.message.reply_text("Hello!")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
```

## Best Practices

- Store tokens in env vars or secret managers, never in code
- Use webhooks over polling in production where possible
- Rate limit outgoing messages to avoid platform bans
- Log all incoming messages and errors with correlation IDs
- Pin a message rate and handle platform-specific limits
- Set up monitoring so a dead bot is detected quickly

## Capabilities

### bot-frameworks
Scaffold bots for major chat platforms.

**Commands:**
- `pip install python-telegram-bot`
- `npm install slack-bolt`
- `npm install discord.js`
- `npm install grammY`
- `python -m venv .venv`

**Examples:**
- npm install @slack/bolt
- pip install aiogram
- npm install whatsapp-web.js

### bot-runtime
Run and monitor bot processes.

**Commands:**
- `node bot.js`
- `python bot.py`
- `pm2 start bot.js --name telegram-bot`
- `pm2 logs telegram-bot`
- `curl -s https://api.telegram.org/bot$TOKEN/getMe`

**Examples:**
- pm2 restart telegram-bot
- curl -s https://api.telegram.org/bot$TOKEN/getWebhookInfo
- pm2 save
