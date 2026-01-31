# Telegram Bot for CEO Agent

This bot serves as the primary communication channel between the Founder (User) and the CEO Agent.

## Setup

1. **Create Bot**:
   - Talk to `@BotFather` on Telegram
   - Send `/newbot`
   - Get your `TELEGRAM_BOT_TOKEN`

2. **Install Dependencies**:
   ```bash
   pip install python-telegram-bot
   ```

3. **Run Locally**:
   ```bash
   export TELEGRAM_BOT_TOKEN="your_token_here"
   python bot.py
   ```

## Architecture

- **Inputs**: User text messages via Telegram
- **Process**: `bot.py` sends HTTP POST to `functions/ceo` (Cloud Function)
- **Outputs**: CEO Agent response text sent back to Telegram chat

## Security

- Ensure `TELEGRAM_BOT_TOKEN` is kept in `.env` or Secrets Manager.
- In production, implement a whitelist of allowed `user_id`s to prevent strangers from commanding your CEO.
