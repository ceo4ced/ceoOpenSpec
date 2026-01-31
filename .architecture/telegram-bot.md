# Telegram Bot Specification

## Overview

The Telegram bot is the primary communication channel between the Human (Chairman) and the AI agents, particularly the CEO.

---

## Bot Configuration

```yaml
telegram:
  bot_token_secret: projects/{project}/secrets/telegram-bot-token
  
  # Authorized users (Human only)
  authorized_users:
    - telegram_user_id: "[HUMAN_TELEGRAM_ID]"
      name: "[HUMAN_NAME]"
      role: "chairman"
      
  # Group chat (optional)
  management_group_id: "[GROUP_ID]"  # If Human wants group updates
```

---

## Message Flow

### Human → System

```
Human sends message to bot
        ↓
Bot authenticates sender (must be authorized)
        ↓
Parse message intent
        ↓
Route to appropriate agent
        ↓
Agent processes
        ↓
Response sent back to Human
```

### System → Human

```
Agent needs Human attention
        ↓
Agent creates notification
        ↓
CEO aggregates (for reports)
        ↓
Bot sends to Human
        ↓
Human responds (if needed)
        ↓
Response routed to originating agent
```

---

## Command Interface

### Human Commands

| Command | Description | Routes To |
|---------|-------------|-----------|
| `/status` | Business status summary | CEO |
| `/costs` | Token/spending report | CFO |
| `/approve` | View pending approvals | CXA |
| `/mcp` | MCP server status | CIO |
| `/agents` | All agent status | CEO |
| `/emergency` | Emergency pause | CFO (kills non-essential) |
| `/help` | Command list | Bot |

### Approval Commands

| Command | Description |
|---------|-------------|
| `/approve [id]` | Approve pending item |
| `/reject [id] [reason]` | Reject with reason |
| `/approvals` | List all pending |

---

## Message Types

### 1. Status Updates

```
📊 DAILY STATUS

Revenue: $1,234 (+12%)
Costs: $567 (-5%)
Net: $667

Agent Activity:
• CEO: 5 decisions
• CMO: 3 content pieces approved
• CXA: 12 emails routed

No action required.
```

### 2. Approval Requests

```
📋 APPROVAL REQUIRED

Type: Content Publish
From: CMO
Priority: Normal

Content: TikTok video about [topic]
Caption: "[caption text]"
Target: All ages

[Preview Video]

Reply:
• /approve apr_abc123
• /reject apr_abc123 [reason]

Expires: 24 hours
```

### 3. 🔴 RED PHONE

```
🔴 RED PHONE 🔴

URGENT: Legal Notice Received

From: CLO
Time: 2024-01-31 10:30:00 EST

A cease and desist letter has been received 
from [Company] regarding [issue].

IMMEDIATE ACTION REQUIRED.

[View Full Details]

Reply to acknowledge.
```

### 4. Agent Escalations

```
⚠️ ESCALATION

From: CFO
Re: Budget Alert

Token spend is 80% of monthly budget 
with 10 days remaining.

Options:
1. Increase budget
2. Switch to cost-tier models
3. Pause non-essential agents

Reply with 1, 2, or 3.
```

---

## Bot Implementation

### Python (python-telegram-bot)

```python
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler

async def start(update: Update, context):
    """Handle /start command."""
    user_id = update.effective_user.id
    
    if not is_authorized(user_id):
        await update.message.reply_text("Unauthorized. This bot is private.")
        return
    
    await update.message.reply_text(
        "Welcome, Chairman. I'm your C-suite interface.\n"
        "Use /help to see available commands."
    )

async def status(update: Update, context):
    """Handle /status command."""
    if not is_authorized(update.effective_user.id):
        return
    
    # Get status from CEO
    status = await ceo_agent.get_status()
    await update.message.reply_text(format_status(status))

async def approve(update: Update, context):
    """Handle /approve command."""
    if not is_authorized(update.effective_user.id):
        return
    
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /approve [approval_id]")
        return
    
    approval_id = context.args[0]
    result = await process_approval(approval_id, approved=True)
    await update.message.reply_text(f"Approved: {result['summary']}")

async def reject(update: Update, context):
    """Handle /reject command."""
    if not is_authorized(update.effective_user.id):
        return
    
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /reject [approval_id] [reason]")
        return
    
    approval_id = context.args[0]
    reason = ' '.join(context.args[1:])
    result = await process_approval(approval_id, approved=False, reason=reason)
    await update.message.reply_text(f"Rejected: {result['summary']}")

async def handle_message(update: Update, context):
    """Handle free-form messages."""
    if not is_authorized(update.effective_user.id):
        return
    
    message = update.message.text
    
    # Route to CEO for processing
    response = await ceo_agent.process_human_message(message)
    await update.message.reply_text(response)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("approve", approve))
    app.add_handler(CommandHandler("reject", reject))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    app.run_polling()
```

---

## Notification Scheduling

### Immediate (Real-time)

- 🔴 RED PHONE alerts
- Critical escalations
- Security incidents

### Batched (Hourly)

- Approval requests (unless urgent)
- Status updates
- Non-critical notifications

### Daily Summary (8 AM)

- Yesterday's activity
- Today's pending items
- Budget status

### Weekly Report (Monday 9 AM)

- Week's performance
- Key decisions made
- Upcoming items

---

## Security

### Authentication

```python
AUTHORIZED_USERS = os.environ.get('AUTHORIZED_TELEGRAM_IDS', '').split(',')

def is_authorized(user_id: int) -> bool:
    return str(user_id) in AUTHORIZED_USERS
```

### Rate Limiting

```python
# Prevent abuse
RATE_LIMIT = 60  # messages per minute
user_message_counts = {}

async def check_rate_limit(user_id: int) -> bool:
    # Implementation
    pass
```

### Logging

All interactions logged to BigQuery:

```sql
INSERT INTO telegram_log (
    message_id,
    user_id,
    username,
    message_type,  -- command, message, callback
    content,
    response,
    routed_to,
    processed_at
) VALUES (...);
```

---

## Deployment

### Cloud Functions

```yaml
telegram_bot:
  runtime: python311
  entry_point: telegram_webhook
  trigger: HTTP
  
  env_vars:
    BOT_TOKEN_SECRET: projects/{p}/secrets/telegram-bot-token
    AUTHORIZED_IDS_SECRET: projects/{p}/secrets/authorized-telegram-ids
```

### Webhook vs Polling

```yaml
# Production: Use webhook
webhook:
  url: https://[region]-[project].cloudfunctions.net/telegram-webhook
  
# Development: Use polling
polling:
  enabled: true
```

---

*The Human's direct line to the business. Secure. Immediate. Actionable.*
