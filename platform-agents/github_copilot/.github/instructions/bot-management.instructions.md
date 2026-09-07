---
applyTo: "**/*.go **/*.py **/*.r **/*.sh"
---

Builds and operates chat bots (Telegram, Slack, Discord, IRC) with webhooks, message routing, rate limiting, and observability.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `pip install python-telegram-bot`, `node bot.js`
- Check `knowledge` references and prerequisites before proceeding

### 2. Reason
Analyze and plan:
- Compare current state vs desired state (drift, checksums, policy)
- Evaluate trust, compatibility, and risk: use `kdesk trust` and `kdesk doctor` patterns
- Decide: which capabilities/tools are needed, which can be skipped

### 3. Act
Execute with guards:
- Run only `allowed-tools` (see frontmatter); use `safe_path` for writes
- Prefer `Bash` with explicit binaries (`curl`, `kubectl`, `kdesk`) over generic shell
- Record evidence: file paths, checksums, and tool outputs for verification

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
