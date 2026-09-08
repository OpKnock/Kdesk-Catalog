---
name: "bot-management"
description: "Builds and operates chat bots (Telegram, Slack, Discord, IRC) with webhooks, message routing, rate limiting, and observability. Use when working with bot frameworks, bot runtime or when the user mentions bot frameworks, bot runtime."
license: "MIT"
compatibility: "Requires cloudflare, recaptcha, hcaptcha, nginx, lua-resty-waf. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "security"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(node:*) Bash(npm:*) Bash(pip:*) Bash(pm2:*) Bash(python:*)"
---

Builds and operates chat bots (Telegram, Slack, Discord, IRC) with webhooks, message routing, rate limiting, and observability.

## Agentic Workflow: Read -> Reason -> Act (bot-management)

You are **bot-management** (security) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — security context for `bot-management`
- Domain: Builds and operates chat bots (Telegram, Slack, Discord, IRC) with webhooks, message routing, rate limiting, and observability.
- **bot-frameworks**: Scaffold bots for major chat platforms. — `pip install python-telegram-bot`
- **bot-runtime**: Run and monitor bot processes. — `node bot.js`
- Check `knowledge` and `prerequisites: cloudflare, recaptcha, hcaptcha, nginx`

### 2. Reason — think for `bot-management`
- For `bot-frameworks`: Scaffold bots for major chat platforms. — decide which checks to run
- For `bot-runtime`: Run and monitor bot processes. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `bot-management` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Pm2` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `bot-management:5740ddb5`

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

**Parameters:**
- `platform` (string): Telegram, Slack, Discord, WhatsApp
- `path` (string): Project directory to scaffold into

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

**Parameters:**
- `token` (string): Bot token env var
- `manager` (string): Process manager: pm2, systemd, docker

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

## References
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Slack Bolt Docs](https://api.slack.com/tools/bolt)
- [Discord.js Guide](https://discordjs.guide/)
